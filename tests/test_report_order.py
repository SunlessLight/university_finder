"""
test_report_order.py — a report sold without a list (plans/intake_forms_plan.md T5, 2026-10-30).

A report buyer has a student folder but no master_list.csv. What these pin down:
  - build_report.py stops after the report: no finalist marker, because there is no row to flip;
  - a student with a master list still gets the marker;
  - check_report.py asks that report for "Your priorities" and "Admit rate" like any other, because
    the report form has asked the importance grid since 2026-10-30;
  - progress_dashboard.py shows "Report order", not stuck at Stage 1;
  - a student's report opens with their profile (never their race), a quick report doesn't, and the
    PDF's "Key terms" still lands after the Snapshot;
  - check_report.py flags halal/prayer wording the student never asked for.

Facts plus one opinion box (R34, plans/seven_tasks.md T1, 2026-11-02):
  - the new headings render, the box carries our label, and the report prints its date;
  - a JSON written the old way fails, a quick report has no box, Reach/Match/Safety never prints;
  - hedges, advice and chatter each catch a bad line and pass a good one, including the words the
    audit's trial showed would be false alarms;
  - a report in the old shape is still recognised, and doesn't get the new checks.

Everything runs in a temporary folder.

Run (stdlib only, no pytest needed):
    python -m unittest tests.test_report_order -v
"""

import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
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

    def test_every_student_report_needs_the_published_admit_rate(self):
        findings = self.findings("Admit rate")
        self.assertEqual(len(findings), 1)
        self.assertIn("Admit rate", findings[0])

    def test_a_quick_report_keeps_the_admit_rate_because_it_is_a_fact(self):
        self.assertEqual(len(self.findings("Admit rate", quick=True)), 1)


def report_data(**extra):
    """A report JSON, with every field the Snapshot and box print."""
    return {"university": "Test University", "course": "BSc Test", "country": "Malaysia",
            "overall_rank": "#1", "subject_rank": "#2", "application_system": "UCAS",
            "admit_rate": "12% (university's figure)", "priorities": "Must have: Cost",
            "grades_vs_bar": "At the bar", "sources": [{"title": "s"}],
            "sections": dict(SECTIONS), **extra}


class ReportShape(unittest.TestCase):
    def test_the_new_headings_render(self):
        report = build_report.render_report(report_data(), "course")
        for heading in ("Who it's for", "Getting in — requirements and who gets in", "Campus culture",
                        "Notable facts", "Our assessment (a judgment, not a fact)"):
            self.assertRegex(report, rf"(?m)^## \d+\. {re.escape(heading)}$")

    def test_no_heading_asks_for_a_verdict(self):
        report = build_report.render_report(report_data(), "course")
        for old in ("your fit", "Why here", "hesitate", "vibe", "quirks"):
            self.assertNotIn(old, report)

    def test_the_box_is_a_box_opening_with_our_label(self):
        report = build_report.render_report(report_data(), "course")
        box = report[report.index("## 14."):report.index("## 15.")]
        self.assertIn('<div class="callout-note" markdown="1">', box)
        self.assertIn("**Grades vs entry bar: At the bar.** Our label:", box)
        self.assertIn("</div>", box)

    def test_reach_match_safety_never_prints(self):
        report = build_report.render_report(report_data(admission_likelihood="Reach"), "course")
        self.assertNotIn("Reach", report)
        self.assertNotIn("Admission likelihood", report)
        self.assertIn("| **Admit rate** | 12% (university's figure) |", report)

    def test_the_date_prints_under_the_title(self):
        self.assertEqual(build_report.prepared_line(date(2026, 11, 2)), "_Prepared on 2 November 2026._")
        report = build_report.render_report(report_data(), "course")
        self.assertEqual(report.splitlines()[2], build_report.prepared_line())

    def test_old_json_fails_the_build(self):
        sections = {("why_here" if k == "our_assessment" else k): v for k, v in SECTIONS.items()}
        with self.assertRaises(SystemExit) as stop:
            build_report.validate(report_data(sections=sections), "course")
        self.assertIn("our_assessment", str(stop.exception))

    def test_quick_needs_no_box_and_prints_none(self):
        sections = {k: v for k, v in SECTIONS.items() if k != "our_assessment"}
        data = report_data(sections=sections)
        build_report.validate(data, "course", quick=True)
        report = build_report.render_report(data, "course", quick=True)
        self.assertNotIn("Our assessment", report)
        self.assertIn("## 14. Sources", report)


class ReportChecks(unittest.TestCase):
    def results(self, line="Tuition is GBP 29,000 a year.", section="costs", **flags):
        data = report_data(sources=[{"title": "s", "url": "https://x.edu", "authority": "Official",
                                     "as_of": "2026"}])
        data["sections"][section] = line
        quick = flags.get("quick", False)
        if quick:
            del data["sections"]["our_assessment"]
        return check_report.run(build_report.render_report(data, "course", quick=quick),
                                check_report.CHECKS, **flags)

    def assertFlagged(self, check, *lines):
        for line in lines:
            with self.subTest(line=line):
                self.assertEqual(len(self.results(line)[1][check]), 1)

    def assertPasses(self, check, *lines):
        for line in lines:
            with self.subTest(line=line):
                self.assertEqual(self.results(line)[1][check], [])

    def test_a_built_report_passes_the_shape_checks(self):
        mode, found = self.results()
        self.assertEqual(mode, "report")
        self.assertEqual(found["structure"], [])
        self.assertEqual(found["snapshot"], [])

    def test_a_built_quick_report_passes_structure(self):
        self.assertEqual(self.results(quick=True)[1]["structure"], [])

    def test_a_quick_report_with_a_box_fails_structure(self):
        text = build_report.render_report(report_data(), "course")
        self.assertTrue(check_report.run(text, ["structure"], quick=True)[1]["structure"])

    def test_no_date_fails_structure(self):
        text = build_report.render_report(report_data(), "course").replace("_Prepared on", "_Made on")
        self.assertIn("Prepared on", " ".join(check_report.run(text, ["structure"])[1]["structure"]))

    def test_the_box_needs_our_label(self):
        data = report_data(grades_vs_bar="")
        data["sections"]["our_assessment"] = "| Topic | Our judgment |\n|---|---|\n| Cost | Hard (§10) |"
        found = check_report.run(build_report.render_report(data, "course"), ["tables"])[1]["tables"]
        self.assertTrue(any("Grades vs entry bar" in line for line in found))
        data["grades_vs_bar"] = "At the bar"
        found = check_report.run(build_report.render_report(data, "course"), ["tables"])[1]["tables"]
        self.assertFalse(any("Grades vs entry bar" in line for line in found))

    def test_hedges_catch_guesses_and_verdicts(self):
        self.assertFlagged("hedges", "Fees will likely rise.", "Offers usually arrive in March.",
                           "Around 200 students join.", "Tuition is ~USD 60,000.",
                           "About A$25,000 a year.", "Predicted grades put you well above the bar.")

    def test_hedges_leave_ordinary_words_and_ringgit_alone(self):
        self.assertPasses("hedges", "Total ~RM 400,000 at the 2026 rate.", "About RM 5,000 a year.",
                          "Students are certain about medicine.", "Around the campus are three parks.",
                          "It costs about the same as Year 1.")

    def test_a_hedge_is_fine_in_the_box_and_nowhere_else(self):
        line = "| Cost | Likely a stretch (§10) |"
        self.assertEqual(self.results(line, section="our_assessment")[1]["hedges"], [])
        self.assertEqual(len(self.results(line, section="costs")[1]["hedges"]), 1)

    def test_advice_catches_orders(self):
        self.assertFlagged("advice", "You should apply in October.", "We recommend the foundation year.",
                           "Check the fee page each year.", "**Ask your college early.**",
                           "- [ ] Confirm your second referee.", "The score is 7.5. Take it if offered.",
                           "| Letters | Bring one thing you enjoy |", "Apply early for housing.")

    def test_advice_leaves_rules_and_nouns_alone(self):
        self.assertPasses("advice", "You must declare fitness to practise.", "The SAT is recommended.",
                          "| JPA | Check: Bumiputera only |", "A background check is required.",
                          "Staff will verify your documents.", "Check-in opens at 9am.")

    def test_the_box_gets_no_pass_on_orders(self):
        found = self.results("| Offer | Take it if offered |", section="our_assessment")[1]["advice"]
        self.assertEqual(len(found), 1)

    def test_chatter_catches_notes_to_self(self):
        self.assertFlagged("chatter", "Not found — free search cannot read Reddit.", "Note: fees vary.",
                           "**Note:** fees vary.", "I found no transfer figures.", "Let me explain.",
                           "The pages read here give no numbers.", "Not checked (eSISRAF needs a browser).",
                           "It's worth noting the fees.")

    def test_chatter_leaves_ordinary_words_alone(self):
        self.assertPasses("chatter", "Phase I covers anatomy.", "The Great Dome is open.",
                          "A great many students cycle.", "Not found — MIT publishes no transfer figures.")

    def test_sources_are_not_read(self):
        section = [(15, "Sources", ["- You should read this forum thread, it seems"])]
        self.assertEqual(check_report.check_advice(section), [])
        self.assertEqual(check_report.check_chatter(section), [])
        self.assertEqual(check_report.check_hedges(section), [])

    def test_a_url_is_not_prose(self):
        line = "See [the fees page](https://x.edu/you-should-apply-early-likely)."
        self.assertPasses("advice", line)
        self.assertPasses("hedges", line)

    def old_report(self):
        lines = ["# University Report — Old", ""]
        labels = check_report.LEGACY_REPORT_SNAPSHOT_CORE + check_report.NEW_SNAPSHOT_BY_SCOPE["course"]
        rows = "\n".join(f"| **{label}** | filled |" for label in labels)
        lines += ["## 1. Snapshot", rows, ""]
        for i, (_, heading) in enumerate(build_report.LEGACY_REPORT_SECTIONS, start=2):
            lines += [f"## {i}. {heading}", "You should expect fees to be likely higher.", ""]
        lines += ["## 15. Sources", "- [s](https://x.edu)", ""]
        return "\n".join(lines)

    def test_an_old_report_is_recognised_and_parked(self):
        mode, found = check_report.run(self.old_report(), check_report.CHECKS)
        self.assertEqual(mode, "legacy_report")
        self.assertEqual(found["structure"], [])
        self.assertEqual(found["snapshot"], [])
        for check in ("hedges", "advice", "chatter"):
            self.assertNotIn(check, found)

    def test_an_old_report_keeps_the_faith_check(self):
        text = self.old_report().replace("You should", "Halal food means you should")
        self.assertTrue(check_report.run(text, ["faith"])[1]["faith"])


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
