"""Exercise failure cases in an isolated fixture; never change real source."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import verify_baseline as baseline


class FrozenBaselineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'spriggit' / 'record.yaml'
        self.source.parent.mkdir()
        self.source.write_bytes(b'FormKey: 028A02:Starfield.esm\n')
        self.release = self.root / 'original.esm'
        self.release.write_bytes(b'original released bytes')
        self.lock = self.root / 'manifest.json'
        self.lock.write_text(json.dumps({
            'source_roots': ['spriggit'],
            'recovered_source_sha256': {'spriggit/record.yaml': baseline.source_digest(self.source)},
            'release_files': [{'path': 'original.esm', 'sha256': baseline.digest(self.release)}]
        }))
        self.root_patch = patch.object(baseline, 'ROOT', self.root)
        self.lock_patch = patch.object(baseline, 'LOCK', self.lock)
        self.root_patch.start()
        self.lock_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.addCleanup(self.lock_patch.stop)

    def test_accepts_same_text_with_windows_line_endings(self):
        self.source.write_bytes(self.source.read_bytes().replace(b'\n', b'\r\n'))
        baseline.verify()

    def test_rejects_changed_source(self):
        self.source.write_bytes(b'FormKey: 253A16:Starfield.esm\n')
        with self.assertRaisesRegex(ValueError, 'Missing or modified source'):
            baseline.verify()

    def test_rejects_deleted_source(self):
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing or modified source'):
            baseline.verify()

    def test_rejects_added_source(self):
        (self.source.parent / 'new.yaml').write_bytes(b'New fix')
        with self.assertRaisesRegex(ValueError, 'Unexpected source file'):
            baseline.verify()

    def test_rejects_changed_release_bytes(self):
        self.release.write_bytes(b'different released bytes')
        with self.assertRaisesRegex(ValueError, 'Release file mismatch'):
            baseline.verify()


if __name__ == '__main__':
    unittest.main()
