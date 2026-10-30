"""
test_list_checks.py — the master-list fact checks added in plans/list_pdf_plan.md T4 (2026-10-30).

What these pin down (backlog R28, Decisions items 3-5):
  - a hedge word fails a row stamped "Official page" and only warns on a "Not verified" one;
  - "~" is allowed only as "~RM"; whole-cell sentinels (incl. the legacy deadline wording) and
    the GREAT Scholarships name are not hedges;
  - a money cell holds a currency code and a number, nothing else;
  - "Application requirements" accepts only the fixed vocabulary;
  - an old list missing only the appended columns still FAILS schema, but its cells are checked;
  - apply_backfill.py refuses (or warns on) the same things before it writes.

Rows are built in memory from SHORTLIST_HEADERS; no student file is read or written.

Run (stdlib only, no pytest needed):
    python -m unittest tests.test_list_checks -v
"""

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))

import apply_backfill  # noqa: E402
import check_master_list as cml  # noqa: E402
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


if __name__ == "__main__":
    unittest.main()
