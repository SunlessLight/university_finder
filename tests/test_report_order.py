"""
test_report_order.py — a report sold without a list (plans/intake_forms_plan.md T5, 2026-10-30).

A report buyer has a student folder but no master_list.csv. What these pin down:
  - build_report.py stops after the report: no finalist marker, because there is no row to flip;
  - a student with a master list still gets the marker;
  - check_report.py asks that report for "Your priorities" and "Admission likelihood" like any
    other, because the report form has asked the importance grid since 2026-10-30;
  - progress_dashboard.py shows "Report order", not stuck at Stage 1;
  - a student's report opens with their profile (never their race), a quick report doesn't, and the
    PDF's "Key terms" still lands after the Snapshot;
  - check_report.py flags halal/prayer wording the student never asked for.

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


class StudentProfileBlock(unittest.TestCase):
    PROFILE = {
        "name": "Buyer", "ethnicity": "Chinese", "grade_status": "actual",
        "current_program": {"type": "UEC"},
        "subjects": [{"subject": "Physics", "grade_or_predicted": "A1"}],
        "english_proficiency": {"test": "IELTS", "score": "7.0"},
        "financial": {"total_budget": 200000}}
    PREFS = {"specific_courses": ["Law"], "target_countries": [], "total_budget_ceiling": 200000,
             "location_prefs": ["Urban / City"], "other_preferences": ["Low crime rate", "Cold Weather"],
             "priorities": ["cost"]}

    def block(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "profile.json").write_text(json.dumps(self.PROFILE), encoding="utf-8")
            (folder / "preferences.json").write_text(json.dumps(self.PREFS), encoding="utf-8")
            return build_report.render_student_profile(folder)

    def full(self, student=""):
        data = {"university": "Test University", "course": "BSc Test", "sources": [{"title": "s"}],
                "sections": SECTIONS}
        return build_report.render_report(data, "course", student_profile=student)

    def test_the_block_shows_what_they_told_us(self):
        block = self.block()
        for shown in ("UEC", "Physics A1", "IELTS 7.0", "Law", "RM 200,000", "Urban / City",
                      "Low crime rate, Cold Weather"):
            self.assertIn(shown, block)

    def test_race_is_never_printed(self):
        self.assertNotIn("Chinese", self.block())

    def test_priorities_stay_in_the_snapshot_only(self):
        self.assertNotIn("What matters most", self.block())

    def test_it_sits_above_the_snapshot(self):
        report = self.full(self.block())
        self.assertLess(report.index("### Your profile"), report.index("## 1. Snapshot"))

    def test_a_report_with_no_student_has_no_block(self):
        self.assertNotIn("Your profile", self.full())

    def test_no_profile_on_disk_is_not_a_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(build_report.render_student_profile(Path(tmp)), "")

    def test_key_terms_still_land_after_the_snapshot(self):
        import report_to_pdf
        text = report_to_pdf._insert_key_terms(self.full(self.block()), "## Key terms\n")
        self.assertLess(text.index("## 1. Snapshot"), text.index("## Key terms"))
        self.assertLess(text.index("## Key terms"), text.index("## 2. "))


class FaithWording(unittest.TestCase):
    def findings(self, line):
        sections = [(2, "Student life, housing & food", [line]), (15, "Sources", ["- Halal guide"])]
        return check_report.check_faith(sections)

    def test_unasked_halal_is_flagged(self):
        self.assertEqual(len(self.findings("Halal food is easy to find on campus.")), 1)

    def test_a_neutral_line_passes(self):
        self.assertEqual(self.findings("Three dining halls serve food until 9pm."), [])

    def folder(self, profile=None, prefs=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        student = Path(tmp.name) / "buyer"
        (student / "reports").mkdir(parents=True)
        (student / "profile.json").write_text(json.dumps(profile or {}), encoding="utf-8")
        (student / "preferences.json").write_text(json.dumps(prefs or {}), encoding="utf-8")
        return student / "reports" / "x.md"

    def test_a_tick_allows_it(self):
        self.assertTrue(check_report.faith_allowed(self.folder({"needs": {"diet_halal": True}})))

    def test_their_own_question_allows_it(self):
        path = self.folder({"report_orders": [{"question": "Is halal food easy to find?"}]})
        self.assertTrue(check_report.faith_allowed(path))

    def test_nothing_ticked_allows_nothing(self):
        path = self.folder({"needs": {"diet_halal": None}, "report_orders": [{"question": "Is it cold?"}]},
                           {"other_preferences": ["Cold Weather"]})
        self.assertFalse(check_report.faith_allowed(path))

    def test_a_quick_report_has_no_student_to_allow_it(self):
        self.assertFalse(check_report.faith_allowed(Path("data/quick_reports/x.md")))


class CheckReport(unittest.TestCase):
    def findings(self, leave_out, **flags):
        """Snapshot findings for a table holding every required row except leave_out."""
        wanted = list(check_report.NEW_SNAPSHOT_CORE)
        for rows in check_report.NEW_SNAPSHOT_BY_SCOPE.values():
            wanted += rows
        body = [f"| **{label}** | filled |" for label in dict.fromkeys(wanted) if label != leave_out]
        return check_report.check_snapshot([(1, "Snapshot", body)], "report", **flags)

    def test_every_student_report_needs_priorities(self):
        findings = self.findings("Your priorities")
        self.assertEqual(len(findings), 1)
        self.assertIn("Your priorities", findings[0])

    def test_every_student_report_needs_admission_likelihood(self):
        findings = self.findings("Admission likelihood")
        self.assertEqual(len(findings), 1)
        self.assertIn("Admission likelihood", findings[0])


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
