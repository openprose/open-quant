"""Optional historical reproduction in a new directory; never install or fetch."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL_TOL = 1e-10
ABS_TOL = 1e-12
VERSIONS = {'QuantLib': '1.43', 'scipy': '1.18.1', 'numpy': '2.5.3', 'matplotlib': '3.11.2'}


def differences(expected, actual, path='$'):
    if isinstance(expected, bool) or expected is None or isinstance(expected, str):
        return [] if type(expected) is type(actual) and expected == actual else [path]
    if isinstance(expected, (int, float)):
        return [] if not isinstance(actual, bool) and isinstance(actual, (int, float)) and math.isclose(expected, actual, rel_tol=REL_TOL, abs_tol=ABS_TOL) else [path]
    if type(expected) is not type(actual):
        return [path]
    if isinstance(expected, dict):
        errors = [path + ': keys'] if expected.keys() != actual.keys() else []
        for key in sorted(expected.keys() & actual.keys()):
            errors.extend(differences(expected[key], actual[key], path + '.' + key))
        return errors
    if isinstance(expected, list):
        errors = [path + ': length'] if len(expected) != len(actual) else []
        for i, (left, right) in enumerate(zip(expected, actual)):
            errors.extend(differences(left, right, f'{path}[{i}]'))
        return errors
    raise TypeError(type(expected))


def positive_seconds(value):
    seconds = float(value)
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError('timeout must be a finite positive number of seconds')
    return seconds


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result

    def invalid(value):
        raise ValueError('Nonfinite JSON value: ' + value)

    def finite_float(value):
        number = float(value)
        if not math.isfinite(number):
            invalid(value)
        return number

    return json.loads(path.read_text(), object_pairs_hook=pairs, parse_constant=invalid,
                      parse_float=finite_float)


def run_calculation(output, timeout):
    """One launch; retain observed settlement separately from output validity."""
    record = {'started_at': datetime.now(timezone.utc).isoformat(), 'command': [sys.executable, 'bootstrap.py'],
              'timeout_seconds': timeout, 'launch_attempts': 1, 'retries': 0, 'pid': None,
              'settled': False, 'timed_out': False, 'interrupted': False,
              'return_code': None, 'termination': None, 'error': None}
    start = time.monotonic()
    with (output / 'bootstrap.log').open('x') as log:
        try:
            process = subprocess.Popen(record['command'], cwd=output, stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=True)
        except OSError as error:
            record['error'] = str(error)
        else:
            record['pid'] = process.pid
            try:
                record['return_code'] = process.wait(timeout=timeout)
                record['settled'] = True
            except (subprocess.TimeoutExpired, KeyboardInterrupt) as interruption:
                record['timed_out'] = isinstance(interruption, subprocess.TimeoutExpired)
                record['interrupted'] = isinstance(interruption, KeyboardInterrupt)
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                    record['termination'] = 'process-group SIGKILL requested'
                except ProcessLookupError:
                    record['termination'] = 'process group already absent'
                except OSError as error:
                    record['error'] = str(error)
                try:
                    record['return_code'] = process.wait(timeout=5)
                    record['settled'] = True
                except subprocess.TimeoutExpired:
                    record['error'] = 'Launched process did not settle within five seconds of the termination attempt'
    record['wall_seconds'] = time.monotonic() - start
    record['log_sha256'] = digest(output / 'bootstrap.log')
    return record


def reproduce(root, output, observed, timeout):
    """Stage one exact selection, then retain execution and comparison records."""
    root, output = root.resolve(), output.resolve()
    positive_seconds(timeout)
    if os.name != 'posix':
        raise ValueError('Bounded reproduction currently requires a POSIX process-group environment')
    if output.exists() or output.is_relative_to(root):
        raise ValueError('output must not exist and must be outside this checkout')
    example = root / 'examples/sofr-curve'
    sources = {'model/bootstrap.py': 'bootstrap.py', 'model/hagan_west.py': 'hagan_west.py',
               'inputs/quotes.csv': 'out/quotes.csv', 'inputs/sofr-fixing.json': 'out/sofr_fixing.json',
               'inputs/results.json': 'expected-results.json'}
    for source in sources:
        if not (example / source).is_file():
            raise ValueError('Missing selected source: ' + source)
    read_json(example / 'inputs/results.json')
    before = {source: digest(example / source) for source in sources}
    output.mkdir(parents=True)
    (output / 'out').mkdir()
    for source, target in sources.items():
        shutil.copy2(example / source, output / target)
    staged = {target: digest(output / target) for target in sources.values()}
    if any(before[source] != staged[target] for source, target in sources.items()):
        raise ValueError('Source changed while staging; no calculation launched, staging retained')
    execution = run_calculation(output, timeout)
    after = {source: digest(example / source) for source in sources}
    staged_after = {target: digest(output / target) for target in sources.values()}
    execution.update({'versions': observed, 'helper_sha256': digest(Path(__file__)),
                      'source_hashes_before': before, 'source_hashes_after': after,
                      'staged_hashes_before': staged, 'staged_hashes_after': staged_after,
                      'source_hashes_match': before == after, 'staged_hashes_match': staged == staged_after,
                      'result_sha256': digest(output / 'out/results.json')})
    comparison = {'versions': observed, 'relative_tolerance': REL_TOL, 'absolute_tolerance': ABS_TOL,
                  'status': 'not performed', 'differences': None, 'matches': None, 'reason': None}
    if not execution['settled'] or execution['return_code'] != 0 or execution['timed_out'] or execution['interrupted']:
        comparison['reason'] = 'Calculation did not complete successfully; partial outputs are not accepted as a completed result'
    elif before != after or staged != staged_after:
        comparison['reason'] = 'Selected source or staged input identities changed during the calculation'
    else:
        try:
            errors = differences(read_json(output / 'expected-results.json'), read_json(output / 'out/results.json'))
        except (OSError, ValueError) as error:
            comparison['reason'] = str(error)
        else:
            comparison.update({'status': 'compared', 'differences': errors, 'matches': not errors})
    for filename, record in [('execution.json', execution), ('comparison.json', comparison)]:
        with (output / filename).open('x') as file:
            json.dump(record, file, indent=2, allow_nan=False)
            file.write('\n')
    return comparison


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='New directory outside this checkout')
    parser.add_argument('--timeout-seconds', type=positive_seconds, default=120.0,
                        help='One calculation attempt; default 120 seconds, then terminate its process group')
    args = parser.parse_args()
    observed = {'python': platform.python_version()}
    for package in VERSIONS:
        try:
            observed[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            observed[package] = 'missing'
    expected = {'python': '3.12.14', **VERSIONS}
    if observed != expected:
        raise SystemExit('Version preflight failed; nothing executed or installed.\n' + json.dumps({'expected': expected, 'observed': observed}, indent=2))
    try:
        receipt = reproduce(ROOT, args.output, observed, args.timeout_seconds)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(receipt, indent=2))
    return 0 if receipt['matches'] is True else 1


if __name__ == '__main__':
    sys.exit(main())
