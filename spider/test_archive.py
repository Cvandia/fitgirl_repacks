import csv
import tempfile
import unittest
from pathlib import Path

from archive import HEADER, cleanup


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "data").mkdir()
        (self.root / "spider").mkdir()
        (self.root / "spider/config.txt").write_text("2", encoding="utf-8")
        (self.root / "spider/template.txt").write_text(
            "data/repacks-{{lastupdated}}.csv year-month-day", encoding="utf-8"
        )
        (self.root / "index.htm").write_text("old page", encoding="utf-8")
        (self.root / "data/popular-repacks.json").write_text("[]", encoding="utf-8")

    def snapshot(self, version, ids):
        path = self.root / "data" / f"repacks-{version}.csv"
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(HEADER)
            for item_id in ids:
                writer.writerow([item_id, "Game", "2026-09-29T00:00:00+03:00", "magnet:?xt=test", "", "", ""])
        return path

    def test_latest_complete_and_page_reference(self):
        old = self.snapshot("20260901000000", [1, 2])
        keep = self.snapshot("20260929000000", [1, 2, 3])
        invalid = self.snapshot("20260930000000", [1])
        self.assertEqual(cleanup(self.root), keep)
        self.assertFalse(old.exists())
        self.assertFalse(invalid.exists())
        self.assertIn(keep.name, (self.root / "index.htm").read_text(encoding="utf-8"))
        self.assertTrue((self.root / "data/popular-repacks.json").exists())
        self.assertEqual(cleanup(self.root), keep)

    def test_no_complete_snapshot_preserves_everything(self):
        duplicate = self.snapshot("20260929000000", [1, 1])
        with self.assertRaises(ValueError):
            cleanup(self.root)
        self.assertTrue(duplicate.exists())
        self.assertEqual((self.root / "index.htm").read_text(encoding="utf-8"), "old page")

    def test_dry_run_does_not_write_or_delete(self):
        old = self.snapshot("20260901000000", [1, 2])
        keep = self.snapshot("20260929000000", [1, 2])
        self.assertEqual(cleanup(self.root, dry_run=True), keep)
        self.assertTrue(old.exists())
        self.assertEqual((self.root / "index.htm").read_text(encoding="utf-8"), "old page")


if __name__ == "__main__":
    unittest.main()
