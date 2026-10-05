import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.check_repository import ROOT, check_claim, digest, repository_errors
from scripts.reproduce_sofr import differences


class EvidenceControls(unittest.TestCase):
    def test_labeled_controls(self):
        path = ROOT / 'examples/sofr-curve/inputs/results.json'
        source = json.loads(path.read_text())
        for case in json.loads((ROOT / 'tests/fixtures/evidence-cases.json').read_text()):
            with self.subTest(case=case['name']):
                self.assertEqual(check_claim(case, source, digest(path)), case['expected'])

    def test_import_tampering_is_detected(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'copy'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
            path = root / 'examples/sofr-curve/inputs/results.json'
            path.write_text(path.read_text() + '\n')
            self.assertIn('Imported identity mismatch: examples/sofr-curve/inputs/results.json', repository_errors(root))

    def test_changed_evidence_breaks_previous_claim(self):
        path = ROOT / 'examples/sofr-curve/inputs/results.json'
        source = json.loads(path.read_text())
        case = json.loads((ROOT / 'tests/fixtures/evidence-cases.json').read_text())[0]
        changed = copy.deepcopy(source)
        changed['forward_smoothness']['A']['max_jump_bp'] = 1.0
        self.assertEqual(check_claim(case, changed, digest(path)), 'not met: value mismatch')


class NumericalReproductionControls(unittest.TestCase):
    def test_roundoff_allowed(self):
        self.assertEqual(differences({'x': 59.71}, {'x': 59.710000000001}), [])

    def test_material_number_change_detected(self):
        self.assertEqual(differences({'x': 59.71}, {'x': 59.72}), ['$.x'])

    def test_scope_and_structure_changes_detected(self):
        self.assertTrue(differences({'date': '2026-09-18'}, {'date': '2026-09-19'}))
        self.assertTrue(differences({'bp': 1.0}, {'percent': 1.0}))
        self.assertTrue(differences([1, 2], [1]))
        self.assertTrue(differences(1, True))
        self.assertTrue(differences(1.0, float('nan')))


if __name__ == '__main__':
    unittest.main()
