import argparse
import json
import math
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.reproduce_sofr import main, positive_seconds, reproduce


@unittest.skipUnless(os.name == 'posix', 'Bounded helper requires POSIX process groups')
class ReproductionEvidence(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.root = self.directory / 'source'
        self.example = self.root / 'examples/sofr-curve'
        (self.example / 'model').mkdir(parents=True)
        (self.example / 'inputs').mkdir()
        (self.example / 'model/hagan_west.py').write_text('# synthetic test dependency\n')
        (self.example / 'inputs/quotes.csv').write_text('id,value\nA,1\n')
        (self.example / 'inputs/sofr-fixing.json').write_text('{"fixing": 1}\n')
        (self.example / 'inputs/results.json').write_text('{"value": 1.0}\n')
        self.output = self.directory / 'run'

    def run_fixture(self, body, timeout=5):
        (self.example / 'model/bootstrap.py').write_text('from pathlib import Path\n' + body + '\n')
        return reproduce(self.root, self.output, {'python': 'synthetic-test'}, timeout)

    def execution(self):
        return json.loads((self.output / 'execution.json').read_text())

    def test_success_retains_selected_identities_and_observed_settlement(self):
        result = self.run_fixture('Path("out/results.json").write_text(\'{"value": 1.0}\')')
        self.assertTrue(result['matches'])
        self.assertEqual(result['status'], 'compared')
        execution = self.execution()
        self.assertTrue(execution['settled'])
        self.assertEqual(execution['return_code'], 0)
        self.assertEqual(execution['launch_attempts'], 1)
        self.assertEqual(execution['retries'], 0)
        self.assertFalse(execution['timed_out'])
        self.assertTrue(execution['source_hashes_match'])
        self.assertTrue(execution['staged_hashes_match'])
        self.assertEqual(len(execution['source_hashes_before']), 5)
        self.assertIsNotNone(execution['result_sha256'])
        self.assertEqual(json.loads((self.output / 'comparison.json').read_text()), result)

    def test_successful_process_can_have_numerical_mismatch(self):
        result = self.run_fixture('Path("out/results.json").write_text(\'{"value": 2.0}\')')
        self.assertEqual(self.execution()['return_code'], 0)
        self.assertFalse(result['matches'])
        self.assertEqual(result['differences'], ['$.value'])

    def test_failed_process_does_not_accept_a_matching_partial_file(self):
        result = self.run_fixture('Path("out/results.json").write_text(\'{"value": 1.0}\')\nraise SystemExit(7)')
        self.assertEqual(self.execution()['return_code'], 7)
        self.assertTrue(self.execution()['settled'])
        self.assertIsNone(result['matches'])
        self.assertEqual(result['status'], 'not performed')
        self.assertTrue((self.output / 'out/results.json').is_file())

    def test_timeout_retains_partial_output_and_native_termination(self):
        result = self.run_fixture('Path("out/results.json").write_text(\'{"value": 1.0}\')\nimport time\ntime.sleep(60)', timeout=2)
        execution = self.execution()
        self.assertTrue(execution['timed_out'])
        self.assertTrue(execution['settled'])
        self.assertLess(execution['return_code'], 0)
        self.assertEqual(execution['termination'], 'process-group SIGKILL requested')
        self.assertIsNone(result['matches'])
        self.assertTrue((self.output / 'out/results.json').is_file())

    def test_missing_output_is_unavailable_not_a_numeric_mismatch(self):
        result = self.run_fixture('print("process completed without result")')
        self.assertEqual(self.execution()['return_code'], 0)
        self.assertIsNone(result['matches'])
        self.assertIsNone(result['differences'])
        self.assertIsNotNone(result['reason'])

    def test_invalid_output_is_retained_without_acceptance(self):
        for i, text in enumerate(['{broken', '{"value": NaN}', '{"value": Infinity}',
                                  '{"value": 1e400}', '{"value": 2, "value": 1}']):
            with self.subTest(text=text):
                self.output = self.directory / f'bad-{i}'
                result = self.run_fixture(f'Path("out/results.json").write_text({text!r})')
                self.assertEqual(self.execution()['return_code'], 0)
                self.assertEqual((self.output / 'out/results.json').read_text(), text)
                self.assertIsNone(result['matches'])

    def test_modified_staged_input_prevents_acceptance(self):
        result = self.run_fixture('Path("out/quotes.csv").write_text("changed")\nPath("out/results.json").write_text(\'{"value": 1.0}\')')
        self.assertFalse(self.execution()['staged_hashes_match'])
        self.assertTrue(self.execution()['source_hashes_match'])
        self.assertIsNone(result['matches'])

    def test_modified_source_prevents_acceptance(self):
        target = str(self.example / 'inputs/quotes.csv')
        result = self.run_fixture(f'Path({target!r}).write_text("changed")\nPath("out/results.json").write_text(\'{{"value": 1.0}}\')')
        self.assertFalse(self.execution()['source_hashes_match'])
        self.assertTrue(self.execution()['staged_hashes_match'])
        self.assertIsNone(result['matches'])

    def test_launch_failure_has_a_record_without_claimed_settlement(self):
        with patch('scripts.reproduce_sofr.subprocess.Popen', side_effect=OSError('synthetic launch failure')):
            result = self.run_fixture('pass')
        execution = self.execution()
        self.assertEqual(execution['launch_attempts'], 1)
        self.assertIsNone(execution['pid'])
        self.assertFalse(execution['settled'])
        self.assertEqual(execution['error'], 'synthetic launch failure')
        self.assertIsNone(result['matches'])

    def test_keyboard_interrupt_requests_termination_and_retains_result(self):
        with patch('scripts.reproduce_sofr.subprocess.Popen') as launch, \
             patch('scripts.reproduce_sofr.os.killpg') as terminate:
            launch.return_value.pid = 987654
            launch.return_value.wait.side_effect = [KeyboardInterrupt(), -9]
            result = self.run_fixture('pass')
        terminate.assert_called_once()
        self.assertTrue(self.execution()['interrupted'])
        self.assertFalse(self.execution()['timed_out'])
        self.assertTrue(self.execution()['settled'])
        self.assertIsNone(result['matches'])

    def test_reused_or_source_nested_output_is_refused(self):
        self.run_fixture('Path("out/results.json").write_text(\'{"value": 1.0}\')')
        before = (self.output / 'execution.json').read_bytes()
        with self.assertRaises(ValueError):
            reproduce(self.root, self.output, {}, 5)
        self.assertEqual((self.output / 'execution.json').read_bytes(), before)
        with self.assertRaises(ValueError):
            reproduce(self.root, self.root / 'new-output', {}, 5)

    def test_invalid_timeout_never_launches(self):
        for value in [0, -1, math.inf, math.nan]:
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                positive_seconds(value)

    def test_version_mismatch_never_launches_or_creates_output(self):
        with patch('sys.argv', ['reproduce_sofr.py', '--output', str(self.output)]), \
             patch('scripts.reproduce_sofr.importlib.metadata.version', return_value='wrong-version'), \
             patch('scripts.reproduce_sofr.subprocess.Popen') as launch:
            with self.assertRaises(SystemExit):
                main()
        launch.assert_not_called()
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
