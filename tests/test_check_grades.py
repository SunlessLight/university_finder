"""
test_check_grades.py — the grade checker (plans/intake_forms_plan.md T3, 2026-10-30).

AI tidies a student's free-text grades into subjects[]; check_grades.py is the check on that step.
What these pin down:
  - a grade impossible for the programme fails ("A*" in STPM, "50" in IB);
  - a correct example of every programme passes;
  - a subject dropped while tidying fails (raw names more subjects than the tidied list);
  - "Other" has no scale, so it never fails on a grade and always asks for a human look.

Profiles are built in memory; no student file is read.

Run (stdlib only, no pytest needed):
    python -m unittest tests.test_check_grades -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import check_grades as cg  # noqa: E402


def profile(program, grades, raw=None):
    data = {"current_program": {"type": program},
            "subjects": [{"subject": s, "grade_or_predicted": g} for s, g in grades]}
    if raw is not None:
        data["_intake_raw"] = {"grades": raw}
    return data


class GradeScales(unittest.TestCase):
    def test_correct_examples_pass(self):
        cases = [
            ("A-Level", [("Physics", "A*"), ("Maths", "e")]),
            ("STPM", [("Physics", "A-"), ("Maths", "B+"), ("Pengajian Am", "C-")]),
            ("UEC", [("Physics", "A1"), ("Maths", "B6"), ("History", "F9")]),
            ("IB", [("Physics HL", "7"), ("Maths SL", "1"), ("Total", "38")]),
            ("Foundation", [("CGPA", "3.6")]),
            ("Matriculation", [("CGPA", "CGPA 4.00")]),
            ("Diploma", [("CGPA", "0")]),
        ]
        for program, grades in cases:
            failures, reviews = cg.check(profile(program, grades))
            self.assertEqual((failures, reviews), ([], []), program)

    def test_a_star_is_impossible_in_stpm(self):
        failures, _ = cg.check(profile("STPM", [("Physics", "A*")]))
        self.assertEqual(len(failures), 1)
        self.assertIn("A*", failures[0])

    def test_50_is_impossible_in_ib(self):
        self.assertEqual(len(cg.check(profile("IB", [("Physics HL", "50")]))[0]), 1)
        self.assertEqual(len(cg.check(profile("IB", [("Total", "50")]))[0]), 1)

    def test_other_programmes_impossible_grades_fail(self):
        for program, grade in [("A-Level", "F"), ("UEC", "A3"), ("Foundation", "4.5"), ("Diploma", "A")]:
            self.assertEqual(len(cg.check(profile(program, [("Physics", grade)]))[0]), 1, program)

    def test_blank_grade_fails(self):
        self.assertEqual(len(cg.check(profile("STPM", [("Physics", None)]))[0]), 1)

    def test_other_never_fails_on_a_grade_and_always_asks_for_a_look(self):
        failures, reviews = cg.check(profile("Other: CIMP", [("Physics", "99")]))
        self.assertEqual(failures, [])
        self.assertEqual(len(reviews), 1)


class DroppedSubjects(unittest.TestCase):
    def test_raw_naming_more_subjects_than_tidied_fails(self):
        data = profile("A-Level", [("Physics", "A"), ("Maths", "A")], raw="Physics A*, Chemistry A, Maths A")
        failures, _ = cg.check(data)
        self.assertEqual(len(failures), 1)
        self.assertIn("3", failures[0])

    def test_raw_and_tidied_agree(self):
        for raw in ("Physics A*\nChemistry A\nMaths A", "Physics A*; Chemistry A; Maths A",
                    "Physics A*, Chemistry A and Maths A", "Physics A*, Chemistry A, Maths A."):
            data = profile("A-Level", [("Physics", "A*"), ("Chemistry", "A"), ("Maths", "A")], raw=raw)
            self.assertEqual(cg.check(data)[0], [], raw)

    def test_cgpa_decimal_is_not_two_subjects(self):
        data = profile("Foundation", [("CGPA", "3.6")], raw="CGPA 3.6")
        self.assertEqual(cg.check(data)[0], [])

    def test_no_grades_at_all_fails(self):
        self.assertEqual(len(cg.check(profile("A-Level", []))[0]), 1)


if __name__ == "__main__":
    unittest.main()
