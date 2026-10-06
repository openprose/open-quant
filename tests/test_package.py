"""Ensure the explicitly selected package remains self-contained."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.check_repository import repository_errors

ROOT = Path(__file__).resolve().parents[1]


class PackageContents(unittest.TestCase):
    def test_selected_files_support_examples_and_offline_checks(self):
        manifest = json.loads((ROOT / 'prose-package.json').read_text())
        self.assertEqual(manifest['schema'], 'prose-package-directory-v1')
        self.assertEqual(len(manifest['files']), len(set(manifest['files'])))
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
            for target in manifest['exports'].values():
                self.assertTrue((destination / target).is_file())
            self.assertEqual(repository_errors(destination), [])


if __name__ == '__main__':
    unittest.main()
