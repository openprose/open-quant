"""Ensure the explicitly selected package remains self-contained."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.check_repository import local_reference_errors

ROOT = Path(__file__).resolve().parents[1]


class PackageContents(unittest.TestCase):
    def test_contract_package_is_complete_and_self_contained(self):
        manifest = json.loads((ROOT / 'prose-package.json').read_text())
        self.assertEqual(manifest['schema'], 'prose-package-directory-v1')
        self.assertEqual(len(manifest['files']), len(set(manifest['files'])))
        definitions = {str(path.relative_to(ROOT)) for path in (ROOT / 'contracts').glob('*.md') if path.name != 'README.md'}
        self.assertEqual(set(manifest['files']), definitions | {'LICENSE', 'PACKAGE.md', 'prose-package.json'})
        self.assertEqual(manifest['exports']['default'], 'contracts/documentation.md')
        self.assertEqual(manifest['exports']['README'], 'PACKAGE.md')
        self.assertTrue(definitions.issubset(manifest['exports'].values()))
        self.assertTrue(set(manifest['exports'].values()).issubset(manifest['files']))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            for relative in manifest['files']:
                source = ROOT / relative
                self.assertFalse(source.is_symlink())
                self.assertTrue(source.resolve().is_relative_to(ROOT.resolve()))
                self.assertFalse(any(part in ('results', '__pycache__', '.git') for part in source.parts))
                target = destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                self.assertEqual(target.read_bytes(), source.read_bytes())
            for target in manifest['exports'].values():
                self.assertTrue((destination / target).is_file())
            self.assertEqual(local_reference_errors(destination), [])
            # A missing adopted definition must be observable, even if every
            # remaining file is an exact source copy.
            (destination / 'contracts/claim-evidence.md').unlink()
            self.assertTrue(any('claim-evidence.md' in error for error in local_reference_errors(destination)))


if __name__ == '__main__':
    unittest.main()
