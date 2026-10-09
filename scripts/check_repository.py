"""Offline integrity and explicitly mapped numerical checks; no prose judgment."""
import hashlib
import json
import math
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_claim(record, source, source_sha256):
    """Check one fixture's explicit field/unit mapping, not its prose meaning.

    Paths and units are reviewer-supplied bindings. They are not inferred from
    Markdown. Changing a binding changes the question this function answers.
    """
    if record['source_sha256'] != source_sha256:
        return 'unresolved: source identity'
    value = source
    try:
        for part in record['field'].split('.'):
            value = value[part]
    except (KeyError, TypeError):
        return 'unresolved: missing field'
    if record['unit'] != record['source_unit']:
        return 'not met: unit mismatch'
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 'unresolved: nonnumeric field'
    if not math.isclose(value, record['value'], rel_tol=0, abs_tol=record['rounding_tolerance']):
        return 'not met: value mismatch'
    return 'met'


def local_reference_errors(root):
    errors = []
    # Repository uses inline Markdown links. External URLs and local anchors
    # are excluded; this verifies file existence, not remote sites or anchors.
    for path in root.rglob('*.md'):
        if any(p.startswith('.') for p in path.relative_to(root).parts):
            continue
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^\s)]+)\)', path.read_text()):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                continue
            target_path = (path.parent / unquote(target.split('#')[0])).resolve()
            if not target_path.is_relative_to(root.resolve()) or not target_path.exists():
                errors.append(f'Broken or escaping link: {path.relative_to(root)} -> {target}')
    return errors


def repository_errors(root):
    errors = []
    manifest = json.loads((root / 'provenance/import.json').read_text())
    for item in manifest['files']:
        path = root / item['path']
        if not path.is_file() or digest(path) != item['sha256']:
            errors.append('Imported identity mismatch: ' + item['path'])
    errors.extend(local_reference_errors(root))
    source_path = root / 'examples/sofr-curve/inputs/results.json'
    source = json.loads(source_path.read_text())
    cases = json.loads((root / 'tests/fixtures/evidence-cases.json').read_text())
    for case in cases:
        actual = check_claim(case, source, digest(source_path))
        if actual != case['expected']:
            errors.append(f"Evidence control {case['name']}: {actual}, expected {case['expected']}")
    return errors


if __name__ == '__main__':
    errors = repository_errors(ROOT)
    if errors:
        raise SystemExit('\n'.join(errors))
    print('PASS: imported identities, local file links and explicit evidence controls')
    print('No arbitrary prose assessment or live execution is performed.')
