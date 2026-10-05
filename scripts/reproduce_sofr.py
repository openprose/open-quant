"""Optional historical reproduction in a new directory; never install or fetch."""
import argparse
import importlib.metadata
import json
import math
import platform
import shutil
import subprocess
import sys
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
        for key in expected.keys() & actual.keys():
            errors.extend(differences(expected[key], actual[key], path + '.' + key))
        return errors
    if isinstance(expected, list):
        errors = [path + ': length'] if len(expected) != len(actual) else []
        for i, (left, right) in enumerate(zip(expected, actual)):
            errors.extend(differences(left, right, f'{path}[{i}]'))
        return errors
    raise TypeError(type(expected))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='New directory outside this checkout')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or output.is_relative_to(ROOT):
        parser.error('output must not exist and must be outside this checkout')
    observed = {'python': platform.python_version()}
    for package in VERSIONS:
        try:
            observed[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            observed[package] = 'missing'
    expected = {'python': '3.12.14', **VERSIONS}
    if observed != expected:
        raise SystemExit('Version preflight failed; nothing executed or installed.\n' + json.dumps({'expected': expected, 'observed': observed}, indent=2))
    output.mkdir(parents=True)
    (output / 'out').mkdir()
    example = ROOT / 'examples/sofr-curve'
    for name in ('bootstrap.py', 'hagan_west.py'):
        shutil.copy2(example / 'model' / name, output / name)
    for source, target in [('quotes.csv', 'quotes.csv'), ('sofr-fixing.json', 'sofr_fixing.json')]:
        shutil.copy2(example / 'inputs' / source, output / 'out' / target)
    with (output / 'bootstrap.log').open('w') as log:
        result = subprocess.run([sys.executable, str(output / 'bootstrap.py')], cwd=output, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise SystemExit(f'Bootstrap failed ({result.returncode}); retained log: {output / "bootstrap.log"}')
    errors = differences(json.loads((example / 'inputs/results.json').read_text()), json.loads((output / 'out/results.json').read_text()))
    receipt = {'versions': observed, 'relative_tolerance': REL_TOL, 'absolute_tolerance': ABS_TOL, 'differences': errors, 'matches': not errors}
    (output / 'comparison.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
