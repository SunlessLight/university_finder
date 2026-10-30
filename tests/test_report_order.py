"""
test_report_order.py — a report sold without a list (plans/intake_forms_plan.md T5, 2026-10-30).

A report buyer has a student folder but no master_list.csv. What these pin down:
  - build_report.py stops after the report: no finalist marker, because there is no row to flip;
  - a student with a master list still gets the marker;
  - check_report.py doesn't ask that report for "Your priorities", which the form never asked,
    but does still ask for "Admission likelihood";
  - progress_dashboard.py shows "Report order", not stuck at Stage 1.

Everything runs in a temporary folder.

Run (stdlib only, no pytest needed):
    python -m unittest tests.test_report_order -v
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import build_report  # noqa: E402
import check_report  # noqa: E402
import progress_dashboard  # noqa: E402

SECTIONS = {key: "Filled in." for key, _ in build_report.REPORT_SECTIONS}
REPORT = {"university": "Test University", "course": "BSc Test", "country": "Malaysia", "sources": [],
          **SECTIONS}


class BuildReport(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.student = self.root / "data" / "students" / "buyer"
        self.student.mkdir(parents=True)
        self.json = self.root / "input.json"
        self.json.write_text(json.dumps(REPORT), encoding="utf-8")

    def build(self):
        argv = ["build_report", "--student", "buyer", "--input", str(self.json)]
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(build_report, "REPO_ROOT", self.root), \
                mock.patch.object(build_report, "STUDENTS_DIR", self.student.parent), \
                mock.patch.object(build_report, "validate"), \
                mock.patch.object(build_report, "render_report", return_value="# Report\n"), \
                redirect_stdout(io.StringIO()) as out:
            build_report.main()
        return out.getvalue()

    def marker(self):
        return self.root / ".tmp" / "buyer" / "finalists" / "test-university-bsc-test.json"

    def test_no_master_list_means_a_report_and_no_marker(self):
        printed = self.build()
        self.assertTrue((self.student / "reports" / "test-university-bsc-test.md").exists())
        self.assertFalse(self.marker().exists())
        self.assertNotIn("flip_finalists", printed)

    def test_a_master_list_still_gets_the_marker(self):
        (self.student / "master_list.csv").write_text("University,Course\n", encoding="utf-8")
        self.build()
        self.assertTrue(self.marker().exists())


class CheckReport(unittest.TestCase):
    def findings(self, leave_out, **flags):
        """Snapshot findings for a table holding every required row except leave_out."""
        wanted = list(check_report.NEW_SNAPSHOT_CORE)
        for rows in check_report.NEW_SNAPSHOT_BY_SCOPE.values():
            wanted += rows
        body = [f"| **{label}** | filled |" for label in dict.fromkeys(wanted) if label != leave_out]
        return check_report.check_snapshot([(1, "Snapshot", body)], "report", **flags)

    def test_a_report_order_needs_no_priorities_row(self):
        self.assertEqual(self.findings("Your priorities", report_order=True), [])

    def test_a_report_order_still_needs_admission_likelihood(self):
        findings = self.findings("Admission likelihood", report_order=True)
        self.assertEqual(len(findings), 1)
        self.assertIn("Admission likelihood", findings[0])

    def test_a_normal_report_still_needs_priorities(self):
        findings = self.findings("Your priorities")
        self.assertEqual(len(findings), 1)
        self.assertIn("Your priorities", findings[0])

    def test_only_a_student_with_no_master_list_is_a_report_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            student = Path(tmp) / "buyer"
            (student / "reports").mkdir(parents=True)
            (student / "profile.json").write_text("{}", encoding="utf-8")
            report = student / "reports" / "x.md"
            self.assertTrue(check_report.is_report_order(report))
            (student / "master_list.csv").write_text("University\n", encoding="utf-8")
            self.assertFalse(check_report.is_report_order(report))
            self.assertFalse(check_report.is_report_order(Path(tmp) / "quick_reports" / "x.md"))


class Dashboard(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.student = Path(tmp.name) / "buyer"
        self.student.mkdir()

    def write(self, **profile):
        (self.student / "profile.json").write_text(json.dumps(profile), encoding="utf-8")
        (self.student / "preferences.json").write_text("{}", encoding="utf-8")

    def test_report_buyer_shows_as_report_order(self):
        self.write(report_orders=[{"university": "X"}], _needs_review=["tidy grades"])
        summary = progress_dashboard.summarize_student(self.student)
        self.assertEqual(summary["overall"], "Report order")
        self.assertEqual(summary["detail"], "1 ordered, 0 reports")

    def test_report_buyer_with_a_list_keeps_the_normal_stage(self):
        self.write(report_orders=[{"university": "X"}])
        (self.student / "master_list.csv").write_text("University,List status\nX,Longlist\n", encoding="utf-8")
        summary = progress_dashboard.summarize_student(self.student)
        self.assertEqual(summary["overall"], "Stage 3 in progress")


if __name__ == "__main__":
    unittest.main()
