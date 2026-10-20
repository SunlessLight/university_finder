"""
test_calendar_dates.py — regression tests for build_calendar.py's date-keeping (lane 1, 2026-10-13).

What these pin down, because each one protects a calendar that has no git undo
(data/students/ is gitignored):
  - the shrink refusal: a rebuild with fewer items never overwrites a longer calendar.md
    unless --allow-shrink is passed;
  - --rescue-dates: copies dated_items from .tmp/<slug>/ into data/students/<slug>/dated_items/,
    writes no calendar, never overwrites a saved file;
  - US whole-university reports (uni_*.json, no course) reach the calendar, matched by
    university name, listed once;
  - saved dated_items win over a scratch copy of the same report (no double count);
  - the old {"item": ...} wording still gets its label.

Every test runs in a throwaway temp folder: STUDENTS_DIR and REPO_ROOT are patched, so no
real student file is read or written.

Run (stdlib only, no pytest needed):
    python -m unittest tests.test_calendar_dates -v
"""

import contextlib
import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))

import build_calendar  # noqa: E402

SLUG = "test-student"
CSV_FIELDS = ["University", "Course", "List status", "Key deadline", "How to apply"]


class CalendarDatesTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.students = root / "data" / "students"
        self.student_dir = self.students / SLUG
        self.scratch = root / ".tmp" / SLUG
        self.student_dir.mkdir(parents=True)
        self.scratch.mkdir(parents=True)
        for p in (mock.patch.object(build_calendar, "STUDENTS_DIR", self.students),
                  mock.patch.object(build_calendar, "REPO_ROOT", root)):
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self._tmp.cleanup)

    # --- helpers -------------------------------------------------------------------------

    def write_master(self, rows):
        with (self.student_dir / "master_list.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in CSV_FIELDS})

    def write_json(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    def run_main(self, *args):
        """Run build_calendar.main() with argv; return (stdout, SystemExit or None)."""
        out = io.StringIO()
        argv = ["build_calendar.py", "--student", SLUG, *args]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(out):
            try:
                build_calendar.main()
            except SystemExit as e:
                return out.getvalue(), e
        return out.getvalue(), None

    def calendar_text(self):
        return (self.student_dir / "calendar.md").read_text(encoding="utf-8")

    def finalist(self, uni, course, deadline="2027-01-15"):
        return {"University": uni, "Course": course, "List status": "Finalist",
                "Key deadline": deadline, "How to apply": "UCAS"}

    def course_report(self, uni, course, items):
        return {"university": uni, "course": course, "dated_items": items}

    # --- shrink refusal ------------------------------------------------------------------

    def test_refuses_to_shrink_existing_calendar(self):
        self.write_master([self.finalist("University of Testford", "BSc Physics")])
        longer = ("# Application calendar\n\n| Date | What | University | Action |\n| --- | --- | --- | --- |\n"
                  "| 2026-11-01 | A | U | x |\n| 2026-12-01 | B | U | x |\n| 2027-01-15 | C | U | x |\n")
        (self.student_dir / "calendar.md").write_text(longer, encoding="utf-8")

        _, exit_ = self.run_main()

        self.assertIsNotNone(exit_)
        self.assertIn("REFUSED", str(exit_.code))
        self.assertEqual(self.calendar_text(), longer, "the longer calendar must be left untouched")

    def test_allow_shrink_overwrites(self):
        self.write_master([self.finalist("University of Testford", "BSc Physics")])
        (self.student_dir / "calendar.md").write_text(
            "| 2026-11-01 | A | U | x |\n| 2026-12-01 | B | U | x |\n", encoding="utf-8")

        _, exit_ = self.run_main("--allow-shrink")

        self.assertIsNone(exit_)
        self.assertEqual(build_calendar.count_calendar_items(self.calendar_text()), 1)

    def test_same_or_more_items_writes_without_flag(self):
        self.write_master([self.finalist("University of Testford", "BSc Physics")])
        (self.student_dir / "calendar.md").write_text("| 2026-11-01 | A | U | x |\n", encoding="utf-8")
        self.write_json(self.student_dir / "dated_items" / "testford-physics.json", self.course_report(
            "University of Testford", "BSc Physics",
            [{"date": "2026-11-30", "label": "Scholarship deadline", "action": "Apply"}]))

        _, exit_ = self.run_main()

        self.assertIsNone(exit_)
        self.assertEqual(build_calendar.count_calendar_items(self.calendar_text()), 2)

    def test_count_calendar_items_counts_rows_and_undated_bullets(self):
        text = ("| Date | What | University | Action |\n| --- | --- | --- | --- |\n"
                "| 2026-11-01 | A | U | x |\n\n## Undated / to confirm\n- **B** — U: y\n")
        self.assertEqual(build_calendar.count_calendar_items(text), 2)

    # --- --rescue-dates ------------------------------------------------------------------

    def test_rescue_copies_scratch_and_writes_no_calendar(self):
        self.write_json(self.scratch / "report_testford-physics.json", self.course_report(
            "University of Testford", "BSc Physics",
            [{"date": "2026-11-30", "label": "Scholarship deadline", "action": "Apply"}]))
        self.write_json(self.scratch / "uni_example-tech.json", {
            "university": "Example Institute of Technology", "mode": "university",
            "dated_items": [{"date": "2026-11-01", "label": "Early Action", "action": "Submit"}]})

        _, exit_ = self.run_main("--rescue-dates")

        self.assertIsNone(exit_)
        saved = sorted(p.name for p in (self.student_dir / "dated_items").glob("*.json"))
        self.assertEqual(len(saved), 2)
        self.assertFalse((self.student_dir / "calendar.md").exists(), "rescue must not write a calendar")
        uni = json.loads((self.student_dir / "dated_items" / "example-institute-of-technology.json")
                         .read_text(encoding="utf-8"))
        self.assertEqual(uni["mode"], "university")
        self.assertIsNone(uni["course"])

    def test_rescue_never_overwrites_a_saved_file(self):
        saved_path = self.student_dir / "dated_items" / "testford-physics.json"
        original = self.course_report("University of Testford", "BSc Physics",
                                      [{"date": "2026-10-01", "label": "Original", "action": ""}])
        self.write_json(saved_path, original)
        self.write_json(self.scratch / "report_testford-physics.json", {
            **self.course_report("University of Testford", "BSc Physics",
                                 [{"date": "2026-12-25", "label": "Scratch copy", "action": ""}]),
            "slug": "testford-physics"})

        self.run_main("--rescue-dates")

        self.assertEqual(json.loads(saved_path.read_text(encoding="utf-8")), original)

    def test_rescue_skips_files_that_are_not_reports(self):
        # Some uni_*.json in .tmp/ are plain lists of notes — skipped, not an error.
        (self.scratch / "uni_notes.json").write_text(json.dumps(["a note"]), encoding="utf-8")

        _, exit_ = self.run_main("--rescue-dates")

        self.assertIsNone(exit_)
        self.assertFalse((self.student_dir / "dated_items").exists())

    # --- what reaches the calendar -------------------------------------------------------

    def test_us_whole_university_report_matched_by_name_and_listed_once(self):
        uni = "Example Institute of Technology"
        self.write_master([self.finalist(uni, "BS Physics", "2027-01-01"),
                           self.finalist(uni, "BS Mathematics", "2027-01-01")])
        self.write_json(self.student_dir / "dated_items" / "example-institute-of-technology.json", {
            "university": uni, "course": None, "mode": "university",
            "dated_items": [{"date": "2026-11-01", "label": "Early Action", "action": "Submit"}]})

        self.run_main()

        text = self.calendar_text()
        self.assertEqual(text.count("Early Action"), 1, "one uni report speaks for every course row once")
        self.assertIn(f"| 2026-11-01 | Early Action | {uni} | Submit |", text)

    def test_saved_copy_wins_over_scratch_copy(self):
        self.write_master([self.finalist("University of Testford", "BSc Physics")])
        report = self.course_report("University of Testford", "BSc Physics",
                                    [{"date": "2026-11-30", "label": "Scholarship deadline", "action": "Apply"}])
        self.write_json(self.student_dir / "dated_items" / "testford-physics.json", report)
        self.write_json(self.scratch / "report_testford-physics.json", report)

        _, exit_ = self.run_main()

        self.assertIsNone(exit_)
        self.assertEqual(self.calendar_text().count("Scholarship deadline"), 1)
        self.assertEqual(build_calendar.count_calendar_items(self.calendar_text()), 2)

    def test_reports_for_non_finalists_are_left_out(self):
        self.write_master([self.finalist("University of Testford", "BSc Physics"),
                           {**self.finalist("Rejected University", "BSc Physics"), "List status": "Rejected"}])
        self.write_json(self.student_dir / "dated_items" / "rejected-physics.json", self.course_report(
            "Rejected University", "BSc Physics",
            [{"date": "2026-11-15", "label": "Should not appear", "action": ""}]))

        self.run_main()

        self.assertNotIn("Should not appear", self.calendar_text())

    def test_legacy_item_key_keeps_its_label(self):
        self.write_master([self.finalist("University of Testford", "BSc Physics")])
        self.write_json(self.scratch / "report_testford-physics.json", self.course_report(
            "University of Testford", "BSc Physics", [{"date": "2026-11-30", "item": "Old-style label"}]))

        out, _ = self.run_main()

        self.assertIn("| 2026-11-30 | Old-style label |", self.calendar_text())
        self.assertIn("--rescue-dates", out, "a calendar fed from .tmp/ must tell you to rescue")


if __name__ == "__main__":
    unittest.main()
