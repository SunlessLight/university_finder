"""
test_list_checks.py — the master-list fact checks added in plans/list_pdf_plan.md T4 (2026-10-30).

What these pin down (backlog R28, Decisions items 3-5):
  - a hedge word fails a row stamped "Official page" and only warns on a "Not verified" one;
  - "~" is allowed only as "~RM"; whole-cell sentinels (incl. the legacy deadline wording) and
    the GREAT Scholarships name are not hedges;
  - a money cell holds a currency code and a number, nothing else;
  - "Application requirements" accepts only the fixed vocabulary;
  - an old list missing only the appended columns still FAILS schema, but its cells are checked;
  - apply_backfill.py refuses (or warns on) the same things before it writes;
  - the list PDF adds "Deadline passed" itself when Key deadline has gone by (R49);
  - a row reaches Finalist only as "Official page": flip_finalists.py refuses it, and
    check_master_list.py fails a Finalist still reading "Not verified" (R33);
  - a row for a student with recognition_targets carries one fixed accreditation result (R42);
  - a Key deadline cell holds one date, whether it is written YYYY-MM-DD or in words (R50).

Rows are built in memory from SHORTLIST_HEADERS; no student file is read or written (the one
full flip_finalists.py run uses a temporary folder).

Run (stdlib only, no pytest needed):
    python -m unittest tests.test_list_checks -v
"""

import contextlib
import csv
import io
import json
import re
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))

import apply_backfill  # noqa: E402
import check_master_list as cml  # noqa: E402
import flip_finalists  # noqa: E402
from build_list_pdf import build_html  # noqa: E402
from shortlist_schema import ADDED_COLUMNS, SHORTLIST_HEADERS  # noqa: E402

OFFICIAL = "Official page"
UNVERIFIED = "Not verified"


def make_row(**cells):
    """A full row as {column: value}; keyword names use _ for spaces, e.g. Info_source."""
    row = {h: "" for h in SHORTLIST_HEADERS}
    row.update({"University": "Test University", "Course": "BSc Test", "Country": "United Kingdom",
                "Info source": OFFICIAL})
    for key, value in cells.items():
        column = key.replace("_", " ")
        assert column in row, column
        row[column] = value
    return row


def rows_as_dicts(*rows):
    return list(enumerate(rows, start=2))


class HedgeCheck(unittest.TestCase):
    def test_hedge_on_official_row_fails(self):
        row = make_row(English_req="IELTS 6.5, likely waived for SPM English; confirm with admissions")
        failures, warnings = cml.check_hedges(rows_as_dicts(row))
        self.assertEqual(len(failures), 1)
        self.assertIn("likely", failures[0])
        self.assertIn("confirm", failures[0])
        self.assertEqual(warnings, [])

    def test_same_hedge_on_unverified_row_warns(self):
        row = make_row(English_req="IELTS 6.5, likely waived for SPM English; confirm with admissions",
                       Info_source=UNVERIFIED)
        failures, warnings = cml.check_hedges(rows_as_dicts(row))
        self.assertEqual(failures, [])
        self.assertEqual(len(warnings), 1)

    def test_tilde_allowed_only_before_rm(self):
        self.assertEqual(cml.cell_hedges("Money to show (visa)", "GBP 13,347 living (~RM 75,000)"), [])
        self.assertEqual(cml.cell_hedges("Money to show (visa)", "GBP 13,347 (~ RM 75,000)"), [])
        self.assertTrue(cml.cell_hedges("Scholarship competitiveness", "~5% of applicants win it"))
        self.assertTrue(cml.cell_hedges("Subject rank", "~top 40"))

    def test_advice_and_chatter_words_are_hedges(self):
        self.assertTrue(cml.cell_hedges("Key deadline", "15 January 2027; apply early"))
        self.assertTrue(cml.cell_hedges("Notes", "Note: I couldn't find the fee page"))

    def test_neutral_words_pass(self):
        # "recommended", "considered", "confirmed" quote the university; GREAT is a scheme name.
        for column, text in [
            ("Entry requirements", "A-level Maths recommended; all applicants considered equally"),
            ("Scholarship & portal", "GREAT Scholarships 2027, apply via the university portal"),
            ("Notes", "Offer confirmed by email within 6 weeks"),
        ]:
            self.assertEqual(cml.cell_hedges(column, text), [], text)

    def test_whole_cell_sentinels_are_not_hedges(self):
        self.assertEqual(cml.cell_hedges("Key deadline", "Not published — check portal"), [])
        self.assertTrue(cml.cell_hedges("Key deadline", "Not published yet, check portal in March"))

    def test_computed_and_student_columns_not_scanned(self):
        row = make_row(Student_grades="AAA expected", Warnings="Recognition risk: not found on BEM list")
        self.assertEqual(cml.check_hedges(rows_as_dicts(row)), ([], []))

    def test_recommendation_letters_vocabulary_not_a_hedge(self):
        cell = "Essay · 2 recommendation letters · Test: SAT"
        self.assertEqual(cml.cell_hedges("Application requirements", cell), [])
        self.assertTrue(cml.cell_hedges("Notes", "We recommend applying early"))


class FormatChecks(unittest.TestCase):
    def test_text_in_money_cell_fails(self):
        row = make_row(Annual_tuition="GBP 46,872 (2027 entry)")
        findings = cml.check_numbers(rows_as_dicts(row))
        self.assertEqual(len(findings), 1)
        self.assertIn("Annual tuition", findings[0])

    def test_clean_number_cells_pass(self):
        row = make_row(Annual_tuition="GBP 46,872", Subject_rank="=12", Overall_rank="Not ranked",
                       Checked_on="2026-10-29", Admit_rate="4.5% of all applicants admitted, 2024-25")
        self.assertEqual(cml.check_numbers(rows_as_dicts(row)), [])

    def test_unknown_requirements_word_fails(self):
        row = make_row(Application_requirements="Personal statement · Reference")
        findings = cml.check_requirements(rows_as_dicts(row))
        self.assertEqual(len(findings), 1)
        self.assertIn("Reference", findings[0])

    def test_known_requirements_pass(self):
        row = make_row(Application_requirements="Personal statement · 2 recommendation letters · Test: SAT")
        self.assertEqual(cml.check_requirements(rows_as_dicts(row)), [])


class OldListStillChecked(unittest.TestCase):
    def test_old_header_fails_schema_but_cells_are_checked(self):
        old_header = [h for h in SHORTLIST_HEADERS if h not in ADDED_COLUMNS]
        row = make_row(Intake="September, usually")
        results, warnings = cml.run(old_header, [[row[h] for h in old_header]], cml.CHECKS)
        self.assertTrue(results["schema"])
        self.assertTrue(results["hedges"])


class BackfillRunsTheSameChecks(unittest.TestCase):
    def validate(self, cells, info_source=OFFICIAL):
        header = list(SHORTLIST_HEADERS)
        row = make_row(Info_source=info_source)
        rows = [[row[h] for h in header]]
        index = apply_backfill.index_rows(header, rows)
        fragment = {"university": "Test University", "course": "BSc Test", "cells": cells}
        return apply_backfill.validate([(Path("t.json"), fragment)], header, rows, index,
                                       country=None, overwrite=False)

    def test_hedge_on_official_row_refused(self):
        problems, plan, _, _ = self.validate({"English req": "IELTS 6.5, typically waived"})
        self.assertEqual(len(problems), 1)
        self.assertEqual(plan, [])

    def test_hedge_on_unverified_row_warns_and_writes(self):
        problems, plan, _, warnings = self.validate({"English req": "IELTS 6.5, typically waived"},
                                                    info_source=UNVERIFIED)
        self.assertEqual(problems, [])
        self.assertEqual(len(warnings), 1)
        self.assertEqual(len(plan), 1)

    def test_text_in_money_cell_refused(self):
        problems, _, _, _ = self.validate({"Annual tuition": "about GBP 30,000"})
        self.assertEqual(len(problems), 1)

    def test_legacy_sentinel_refused(self):
        problems, _, _, _ = self.validate({"Key deadline": "Not published — check portal"})
        self.assertEqual(len(problems), 1)

    def test_clean_cells_planned(self):
        problems, plan, _, warnings = self.validate(
            {"Annual tuition": "GBP 46,872", "Application requirements": "Personal statement"})
        self.assertEqual((problems, warnings), ([], []))
        self.assertEqual(len(plan[0][2]), 2)


class PdfDeadlineWarning(unittest.TestCase):
    """Built for a fixed day, so the result never depends on the real date."""
    TODAY = "2026-10-31"

    def build(self, **cells):
        html, _ = build_html([make_row(**cells)], {"name": "Test"}, self.TODAY)
        return html

    def card_warning(self, html):
        m = re.search(r'<p class="card-warn"><strong>Warning\.</strong> (.*?)</p>', html)
        return m.group(1) if m else None

    def summary_marked(self, html):
        return 'Test University<span class="warn-mark">' in html

    def test_passed_date_warns_on_card_and_summary(self):
        html = self.build(Key_deadline="2026-10-15", Warnings="None")
        self.assertEqual(self.card_warning(html), "Deadline passed")
        self.assertTrue(self.summary_marked(html))

    def test_passed_date_joins_an_existing_warning(self):
        html = self.build(Key_deadline="2026-10-15", Warnings="English short")
        self.assertEqual(self.card_warning(html), "Deadline passed; English short")

    def test_blank_warnings_shows_only_the_warning(self):
        html = self.build(Key_deadline="2026-10-15", Warnings="")
        self.assertEqual(self.card_warning(html), "Deadline passed")

    def test_future_date_stays_quiet(self):
        html = self.build(Key_deadline="2027-01-15", Warnings="None")
        self.assertIsNone(self.card_warning(html))
        self.assertFalse(self.summary_marked(html))

    def test_deadline_today_has_not_passed(self):
        html = self.build(Key_deadline="2026-10-31", Warnings="None")
        self.assertIsNone(self.card_warning(html))

    def test_no_real_date_gets_no_warning(self):
        for cell in ("Rolling", "Not published", "Not published — check portal", ""):
            with self.subTest(cell=cell):
                html = self.build(Key_deadline=cell, Warnings="None")
                self.assertIsNone(self.card_warning(html))
                self.assertFalse(self.summary_marked(html))

    def test_rolling_cell_holding_an_old_date_gets_no_warning(self):
        html = self.build(Key_deadline="Rolling (priority 2026-01-15)", Warnings="None")
        self.assertIsNone(self.card_warning(html))

    def test_row_already_flagged_shows_it_once(self):
        html = self.build(Key_deadline="2026-10-15", Warnings="Deadline passed; English short")
        self.assertEqual(self.card_warning(html), "Deadline passed; English short")

    def test_build_leaves_the_rows_unchanged(self):
        row = make_row(Key_deadline="2026-10-15", Warnings="None")
        before = dict(row)
        build_html([row], {"name": "Test"}, self.TODAY)
        self.assertEqual(row, before)


class FinalistMustBeVerified(unittest.TestCase):
    """R33: no Finalist on unverified facts, in the flip and in the gate before a list goes out."""

    def plan(self, rows, marker=None):
        header = SHORTLIST_HEADERS
        csv_rows = [[row[h] for h in header] for row in rows]
        marker = marker or {"university": "Test University", "course": "BSc Test", "mode": "course"}
        return flip_finalists.plan_marker(Path("marker.json"), marker, header, csv_rows)

    def test_gate_fails_a_finalist_that_is_not_verified(self):
        row = make_row(List_status="Finalist", Info_source=UNVERIFIED)
        failures = cml.check_values(rows_as_dicts(row))
        self.assertEqual(len(failures), 1)
        self.assertIn("row 2 Test University", failures[0])

    def test_gate_allows_a_verified_finalist(self):
        row = make_row(List_status="Finalist", Info_source=OFFICIAL)
        self.assertEqual(cml.check_values(rows_as_dicts(row)), [])

    def test_gate_allows_an_unverified_row_that_is_not_a_finalist(self):
        for status in ("Longlist", "Shortlist", "Rejected"):
            with self.subTest(status=status):
                row = make_row(List_status=status, Info_source=UNVERIFIED)
                self.assertEqual(cml.check_values(rows_as_dicts(row)), [])

    def test_flip_refuses_anything_but_official_page(self):
        for source in (UNVERIFIED, ""):
            with self.subTest(source=source):
                outcome, _, detail, matches, _, _ = self.plan(
                    [make_row(List_status="Shortlist", Info_source=source)])
                self.assertEqual(outcome, "not_verified")
                self.assertEqual(matches, [])
                self.assertIn("BSc Test", detail)

    def test_flip_accepts_an_official_row(self):
        outcome, *_ = self.plan([make_row(List_status="Shortlist")])
        self.assertEqual(outcome, "flipped")

    def test_flip_refuses_a_row_that_is_already_finalist_but_unverified(self):
        outcome, *_ = self.plan([make_row(List_status="Finalist", Info_source=UNVERIFIED)])
        self.assertEqual(outcome, "not_verified")

    def test_one_unverified_course_stops_a_university_mode_marker(self):
        rows = [
            make_row(Country="USA", Course="BA One", List_status="Shortlist"),
            make_row(Country="USA", Course="BA Two", List_status="Shortlist", Info_source=UNVERIFIED),
        ]
        outcome, _, detail, matches, _, _ = self.plan(
            rows, {"university": "Test University", "course": None, "mode": "university"})
        self.assertEqual(outcome, "not_verified")
        self.assertEqual(matches, [])
        self.assertIn("BA Two", detail)
        self.assertNotIn("BA One", detail)

    def test_report_that_verified_the_row_can_stamp_it_in_the_same_marker(self):
        marker = {"university": "Test University", "course": "BSc Test", "mode": "course",
                  "corrections": {"Info source": OFFICIAL}}
        outcome, *_ = self.plan(
            [make_row(List_status="Shortlist", Info_source=UNVERIFIED)], marker)
        self.assertEqual(outcome, "corrected")

    def test_a_rejected_row_still_reads_as_rejected(self):
        outcome, *_ = self.plan([make_row(List_status="Rejected", Info_source=UNVERIFIED)])
        self.assertEqual(outcome, "already_rejected")

    def test_run_flips_the_verified_row_and_keeps_the_refused_marker(self):
        rows = [
            make_row(University="Good University", List_status="Shortlist"),
            make_row(University="Unchecked University", List_status="Shortlist",
                     Info_source=UNVERIFIED),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            students = Path(tmp) / "students"
            (students / "test-student").mkdir(parents=True)
            csv_path = students / "test-student" / "master_list.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=SHORTLIST_HEADERS)
                writer.writeheader()
                writer.writerows(rows)
            frags = Path(tmp) / "finalists"
            frags.mkdir()
            good, bad = frags / "good.json", frags / "bad.json"
            for path, uni in ((good, "Good University"), (bad, "Unchecked University")):
                path.write_text(json.dumps(
                    {"university": uni, "course": "BSc Test", "mode": "course"}), encoding="utf-8")

            argv = ["flip_finalists.py", "--student", "test-student",
                    "--fragments", str(frags), "--csv", str(csv_path)]
            with mock.patch.object(flip_finalists, "STUDENTS_DIR", students), \
                    mock.patch.object(sys, "argv", argv), \
                    contextlib.redirect_stdout(io.StringIO()) as printed, \
                    self.assertRaises(SystemExit) as stopped:
                flip_finalists.main()

            self.assertEqual(stopped.exception.code, 1)
            self.assertIn("Unchecked University", printed.getvalue())
            with csv_path.open(newline="", encoding="utf-8") as f:
                status = {r["University"]: r["List status"] for r in csv.DictReader(f)}
            self.assertEqual(status, {"Good University": "Finalist",
                                      "Unchecked University": "Shortlist"})
            self.assertFalse(good.exists())
            self.assertTrue(bad.exists())


class AccreditationCheck(unittest.TestCase):
    """R42: a regulated row states what the accreditor's own list said, in one fixed shape."""
    TARGETS = ["MQA", "BEM", "Washington Accord"]
    TODAY = date(2026, 11, 2)
    GOOD = "Accredited · ABET · 2026-11-02 · https://amspub.abet.org/"

    def check(self, cell, targets=TARGETS):
        row = make_row(**{"Recognised_in_Malaysia?": cell})
        return cml.check_accreditation(rows_as_dicts(row), targets, today=self.TODAY)

    def test_each_fixed_result_passes(self):
        for result in ("Accredited", "Not accredited", "Not on list"):
            with self.subTest(result=result):
                self.assertEqual(self.check(f"{result} · ABET · 2026-11-02 · https://amspub.abet.org/"),
                                 ([], []))

    def test_not_checked_passes_with_a_warning(self):
        failures, warnings = self.check("Not checked · EAC · 2026-11-02 · http://www.eac.org.my/")
        self.assertEqual(failures, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("row 2 Test University", warnings[0])

    def test_cell_without_a_fixed_result_fails(self):
        for cell in ("ABET-accredited; confirm MQA equivalence",
                     "",
                     "accredited · ABET · 2026-11-02 · https://amspub.abet.org/",
                     "Probably accredited · ABET · 2026-11-02 · https://amspub.abet.org/"):
            with self.subTest(cell=cell):
                failures, warnings = self.check(cell)
                self.assertEqual(len(failures), 1)
                self.assertIn("row 2 Test University", failures[0])
                self.assertEqual(warnings, [])

    def test_missing_part_fails(self):
        for cell in ("Accredited",
                     "Accredited · ABET",
                     "Accredited · 2026-11-02 · https://amspub.abet.org/",
                     "Accredited · ABET · https://amspub.abet.org/",
                     "Accredited · ABET · 2026-11-02",
                     "Accredited · ABET · 2026-11-02 · amspub.abet.org"):
            with self.subTest(cell=cell):
                self.assertEqual(len(self.check(cell)[0]), 1)

    def test_text_after_the_link_fails(self):
        self.assertEqual(len(self.check(self.GOOD + " · see notes")[0]), 1)

    def test_bad_or_future_date_fails(self):
        for stamp in ("2026-13-02", "2 Nov 2026", "2026-11-03"):
            with self.subTest(stamp=stamp):
                cell = f"Accredited · ABET · {stamp} · https://amspub.abet.org/"
                self.assertEqual(len(self.check(cell)[0]), 1)

    def test_student_with_no_targets_is_ignored(self):
        self.assertEqual(self.check("MQA recognised; no professional body needed", targets=[]), ([], []))

    def test_unknown_targets_warn_instead_of_passing_quietly(self):
        failures, warnings = self.check("ABET-accredited", targets=None)
        self.assertEqual(failures, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("profile.json", warnings[0])

    def test_cell_passes_the_hedge_and_jargon_checks_on_the_same_row(self):
        for cell in (self.GOOD,
                     "Not checked · Washington Accord · 2026-11-02 · http://www.eac.org.my/",
                     "Accredited · EAC · 2026-11-02 · https://www2.mqa.gov.my/mqr/"):
            with self.subTest(cell=cell):
                row = make_row(**{"Recognised_in_Malaysia?": cell})
                self.assertEqual(cml.check_hedges(rows_as_dicts(row)), ([], []))
                self.assertEqual(cml.check_jargon(rows_as_dicts(row)), [])

    def run_tool(self, cell, profile):
        """check_master_list.py as it really runs, on a CSV with a profile.json beside it."""
        row = make_row(**{"Recognised_in_Malaysia?": cell})
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "master_list.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=SHORTLIST_HEADERS)
                writer.writeheader()
                writer.writerow(row)
            if profile is not None:
                (Path(tmp) / "profile.json").write_text(json.dumps(profile), encoding="utf-8")
            argv = ["check_master_list.py", "--file", str(csv_path), "--check", "accreditation"]
            with mock.patch.object(sys, "argv", argv), \
                    contextlib.redirect_stdout(io.StringIO()) as printed, \
                    self.assertRaises(SystemExit) as stopped:
                cml.main()
        return stopped.exception.code, printed.getvalue()

    def test_tool_passes_a_sample_row_and_fails_a_bad_one(self):
        profile = {"recognition_targets": self.TARGETS}
        code, printed = self.run_tool(self.GOOD, profile)
        self.assertEqual(code, 0, printed)
        code, printed = self.run_tool("ABET-accredited", profile)
        self.assertEqual(code, 1, printed)
        self.assertIn("FAIL accreditation", printed)

    def test_tool_says_so_when_there_is_no_profile(self):
        code, printed = self.run_tool("ABET-accredited", None)
        self.assertEqual(code, 0)
        self.assertIn("warn accreditation", printed)


class OneDatePerDeadlineCell(unittest.TestCase):
    """R50: an early round in the cell reads as "Deadline passed" while the regular one is open."""

    def findings(self, cell):
        return cml.check_deadlines(rows_as_dicts(make_row(Key_deadline=cell)))

    def test_two_date_cell_fails(self):
        findings = self.findings("2026-11-01 (EA); 2027-01-05 (RD)")
        self.assertEqual(len(findings), 1)
        self.assertIn("Key deadline", findings[0])
        self.assertIn("2 dates", findings[0])

    def test_one_date_cell_passes(self):
        self.assertEqual(self.findings("2027-01-05"), [])

    def test_regular_date_first_still_fails_with_an_early_date_after_it(self):
        self.assertEqual(len(self.findings("2027-01-04 (Regular Action; Early Action 2026-11-01)")), 1)

    def test_window_written_in_words_counts_as_two_dates(self):
        self.assertEqual(len(self.findings("16 Dec 2026 - 17 Feb 2027")), 1)
        self.assertEqual(len(self.findings("December 16, 2026 to February 17, 2027")), 1)

    def test_iso_date_beside_a_written_date_counts_as_two_dates(self):
        self.assertEqual(len(self.findings("2027-01-05; Early Action 1 November")), 1)

    def test_one_date_with_a_label_passes(self):
        self.assertEqual(self.findings("2027-01-13 (UCAS equal consideration)"), [])

    def test_month_and_year_alone_is_not_a_date(self):
        self.assertEqual(self.findings("2027-02-17 (AY2027/28, opens December 2026)"), [])

    def test_cells_with_no_date_pass(self):
        for cell in ("Rolling", "Not published", "Not published — check portal", ""):
            with self.subTest(cell=cell):
                self.assertEqual(self.findings(cell), [])

    def test_run_reports_it_under_its_own_name(self):
        row = make_row(Key_deadline="2026-11-01 (EA); 2027-01-05 (RD)")
        header = list(SHORTLIST_HEADERS)
        results, _ = cml.run(header, [[row[h] for h in header]], ["deadlines"])
        self.assertEqual(len(results["deadlines"]), 1)


if __name__ == "__main__":
    unittest.main()
