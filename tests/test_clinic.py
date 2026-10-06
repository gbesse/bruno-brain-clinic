import datetime as dt
import tempfile
import unittest
from pathlib import Path

from brain_clinic import scan


class ClinicTests(unittest.TestCase):
    def test_conflicts_staleness_and_secret_are_reported_without_values(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.md").write_text(
                "---\nsources:\n  - https://example.com/a\nfact_key: customer.status\nfact_value: active\nstale_after: 2025-01-01\n---\nA fact.\n",
                encoding="utf-8",
            )
            (root / "b.md").write_text(
                "---\nsources:\n  - https://example.com/b\nfact_key: customer.status\nfact_value: closed\n---\npassword: abcdefghijklmnopqrstuv\n",
                encoding="utf-8",
            )
            report = scan(root, today=dt.date(2026, 10, 6), lang="es")
            codes = {item["code"] for item in report["issues"]}
            self.assertEqual(codes, {"stale", "fact_conflict", "secret_pattern"})
            self.assertNotIn("abcdefghijklmnopqrstuv", str(report))
            self.assertIn("Valores incompatibles", str(report))

    def test_clean_multilingual_report(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "a.md").write_text(
                "---\nsources: [https://example.com]\nstale_after: 2027-01-01\n---\nSafe fact.\n",
                encoding="utf-8",
            )
            for lang in ("fr", "en", "es"):
                self.assertEqual(scan(directory, today=dt.date(2026, 10, 6), lang=lang)["status"], "clean")

    def test_plain_markdown_accepts_source_link(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "note.md").write_text(
                "Source: https://example.com/source\n\nA sourced note.\n", encoding="utf-8"
            )
            self.assertEqual(scan(directory, today=dt.date(2026, 10, 6))["status"], "clean")


if __name__ == "__main__":
    unittest.main()
