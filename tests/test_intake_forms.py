"""
test_intake_forms.py — the two-form intake (plans/intake_forms_plan.md T2, T5; 2026-10-30).

What these pin down:
  - an old-form row (grade grid) still maps exactly as it did, so the students who answered the
    old form are unchanged;
  - a new-form row (free-text grades + programme) lands in _intake_raw.grades with the right
    current_program.type, using the LIVE titles in forms/intake.json;
  - the sheet keeps a deleted question's column beside its replacement, so an answer in either
    column counts (otherwise every new student is skipped for "no consent");
  - RM 100,000 is a ceiling of 100,000, and "No preference" steers nothing;
  - a report-form row makes a small folder with report_orders, and only ever ADDS an order to a
    folder that exists (data/students/ has no undo);
  - the report form's budget, race and preference answers reach the folder, the exact ticks are
    kept, and "Muslim Facilities/Halal Food" opens both the halal and the prayer flag;
  - two ticks on one row of the importance grid count as the higher one, with a review line, so no
    priority goes missing;
  - a list row never overwrites a folder that a report order made, even with --force.

Student files are written to a temporary folder only.

Run (stdlib only, no pytest needed):
    python -m unittest tests.test_intake_forms -v
"""

import csv
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import fetch_form_questions as questions  # noqa: E402
import fetch_form_responses as responses  # noqa: E402
import ingest_form_csv as ingest  # noqa: E402

GRID = "Select the grades for your subjects based on the option you chose above.  "
OLD_CONSENT = "Do you consent giving me your information? It'll be used for finding and ranking universities"
NEW_CONSENT = "Consent to use your information / Persetujuan penggunaan maklumat anda (PDPA)"
AGREE = "I agree to Shortlisted collecting and using my answers as described above."
GRADES = "Type you subject and grades (eg. physic A, Chemistry B, etc)"
PROGRAMME = "Which pre-university programme are you doing? "
OLD_MONTH = "What month does your actual final result comes out? "
NEW_MONTH = "What month does your actual result come out?"
OLD_STATUS = "Are you applying with forecast result or actual? "
NEW_STATUS = "what are you applying with? "
BUDGET = "What's your limit (RM) for the whole degree. (include tuition, living cost, etc)"
REPORT_UNI = ("Which University do you want a report of? Add the campus if it has several "
              "(e.g. Monash Malaysia vs Monash Australia)")
REPORT_QUESTION = "Anything specific you want the report to answer?"
COURSE = "Choose your desired course"
RACE = "Race ( For checking government scholarship eligibility )"
LOCATION = "Location preferences"
OTHER_PREFS = "Any other perferences? "
TICK = "Tick the importance of each topic below\nWill be used to score each university for you. "
TICKS = [f"{TICK} [{row}]" for row in (
    "Affordable Cost", "Scholarship availability", "University Ranking", "Course Ranking",
    "Employability", "Recognition back home", "Location", "Hands-On Experience")]

# The live sheet's layout: deleted questions keep their columns, new ones sit further right.
SHEET_HEADERS = [
    "Timestamp", "Email Address", "Full Name (As in IC)", f"{GRID}[Physic]", f"{GRID}[Math]",
    OLD_MONTH, OLD_STATUS, COURSE, "Chose your countries", BUDGET, "Location preferences",
    OLD_CONSENT, "What did you take for ur secondary school? ", NEW_STATUS, NEW_CONSENT,
    PROGRAMME, GRADES, NEW_MONTH,
]

REPORT_HEADERS = [
    "Timestamp", "Email Address", "Full Name (as in IC)", REPORT_UNI, COURSE,
    "Which year do you want to start? ", PROGRAMME, "What are you applying with? ",
    "What did you take for Secondary school? ", GRADES, REPORT_QUESTION, NEW_CONSENT,
    RACE, BUDGET, LOCATION, OTHER_PREFS,
]


def mapped(cells, headers=SHEET_HEADERS):
    """Run one row through the same steps as main(); returns (profile, prefs, needs_review)."""
    row = {h: "" for h in headers}
    row.update(cells)
    rows = [row]
    ingest.merge_duplicate_columns(rows, headers)
    slug, profile, prefs, review, skip = ingest.map_row(
        rows[0], ingest.build_col_index(headers),
        slider_cols=ingest._slider_columns(headers), subject_cols=ingest._subject_columns(headers),
        grid_cols=ingest._grid_columns(headers), subject_grid_cols=ingest._subject_grid_columns(headers))
    return profile, prefs, review, skip


def old_row(**extra):
    return {"Email Address": "a@b.com", "Full Name (As in IC)": "Old Student", f"{GRID}[Physic]": "A*",
            f"{GRID}[Math]": "A", OLD_MONTH: "January", OLD_STATUS: "Forecast",
            COURSE: "Economics — markets, public policy, econometrics", "Chose your countries": "UK",
            BUDGET: "500,000", OLD_CONSENT: "Yes", **extra}


def new_row(**extra):
    return {"Email Address": "c@d.com", "Full Name (As in IC)": "New Student", PROGRAMME: "STPM",
            GRADES: "Physics A-, Maths B+", NEW_MONTH: "June", NEW_STATUS: "Forecast Grades",
            COURSE: "Economics — markets, public policy, econometrics", "Chose your countries": "UK",
            BUDGET: "100,000", NEW_CONSENT: AGREE, **extra}


class ListFormIdReachesTheScript(unittest.TestCase):
    """pending and confirm send the form's ID, so the script follows it to the linked sheet."""

    def test_pending_sends_the_form_id(self):
        payload = {"headers": [], "rows": [], "row_numbers": []}
        with mock.patch.dict("os.environ", {responses.LIST_FORM_ENV: "form123"}), \
                mock.patch.object(responses, "call_endpoint", return_value=payload) as call:
            responses.fetch_pending("url", "token")
        self.assertEqual(call.call_args.args[2:], ("pending", {"form": "form123"}))

    def test_no_id_sends_no_form(self):
        with mock.patch.dict("os.environ", {responses.LIST_FORM_ENV: ""}):
            self.assertEqual(responses.list_form_param(), {})

    def test_the_setting_has_one_name(self):
        self.assertEqual(questions.FORMS["intake"], "FORM_ID_LIST_INTAKE")


class ImportanceTicks(unittest.TestCase):
    def ticked(self, ranking):
        cells = {header: "Important" for header in TICKS}
        cells[f"{TICK} [University Ranking]"] = ranking
        return mapped(new_row(**cells), headers=SHEET_HEADERS + TICKS)

    def test_two_ticks_on_a_row_count_as_the_higher_one(self):
        _profile, prefs, _review, _skip = self.ticked("Must have, Important")
        self.assertEqual(prefs["priority_levels"]["ranking"], 3)
        self.assertEqual(len(prefs["priority_levels"]), 8)
        self.assertEqual(prefs["priorities"][0], "ranking")
        self.assertEqual(len(prefs["priorities"]), 8)

    def test_two_ticks_raise_a_review_line(self):
        _profile, _prefs, review, _skip = self.ticked("Must have, Important")
        self.assertTrue(any("ranking" in line and "more than one" in line for line in review))

    def test_one_tick_raises_no_review_line(self):
        _profile, prefs, review, _skip = self.ticked("Must have")
        self.assertEqual(prefs["priority_levels"]["ranking"], 3)
        self.assertFalse(any("more than one" in line for line in review))


class OldFormRows(unittest.TestCase):
    def test_grid_row_keeps_subjects_and_the_a_level_default(self):
        profile, _prefs, review, skip = mapped(old_row())
        self.assertIsNone(skip)
        self.assertEqual(profile["subjects"], [
            {"subject": "Physics", "grade_or_predicted": "A*"},
            {"subject": "Mathematics", "grade_or_predicted": "A"}])
        self.assertEqual(profile["current_program"]["type"], "A-Level")
        self.assertEqual(profile["grade_status"], "predicted")
        self.assertNotIn("_intake_raw", profile)
        self.assertFalse(any("grades" in line for line in review))


class NewFormRows(unittest.TestCase):
    def test_free_text_grades_land_in_intake_raw(self):
        profile, _prefs, review, skip = mapped(new_row())
        self.assertIsNone(skip)
        self.assertEqual(profile["_intake_raw"]["grades"], "Physics A-, Maths B+")
        self.assertEqual(profile["subjects"], [])
        self.assertTrue(any("check_grades.py" in line and "STPM" in line for line in review))

    def test_programme_answer_sets_current_program_type(self):
        profile, *_ = mapped(new_row())
        self.assertEqual(profile["current_program"]["type"], "STPM")

    def test_both_forms_programme_spellings_give_one_label(self):
        for answer, label in [("A-levels", "A-Level"), ("A-Levels", "A-Level"), ("foundation", "Foundation"),
                              ("Foundation", "Foundation"), ("IB", "IB"), ("Other: CIMP", "Other: CIMP")]:
            profile, *_ = mapped(new_row(**{PROGRAMME: answer}))
            self.assertEqual(profile["current_program"]["type"], label)

    def test_consent_in_the_new_column_counts(self):
        _profile, _prefs, _review, skip = mapped(new_row())
        self.assertIsNone(skip)

    def test_applying_with_in_the_new_column_counts(self):
        profile, *_ = mapped(new_row())
        self.assertEqual(profile["grade_status"], "predicted")

    def test_month_with_no_year_is_kept_and_flagged(self):
        profile, _prefs, review, _skip = mapped(new_row())
        self.assertEqual(profile["current_program"]["expected_completion"], "June")
        self.assertTrue(any("no year" in line for line in review))

    def test_fixed_typo_titles_still_match(self):
        headers = SHEET_HEADERS + ["Type your subjects and grades", "Choose your countries",
                                   "Any other preferences?", "What did you take for your secondary school?"]
        index = ingest.build_col_index(headers[-4:])
        self.assertEqual(set(index), {"grades_raw", "target_countries", "needs", "secondary_qualification"})

    def test_budget_100000_is_a_real_ceiling(self):
        profile, prefs, *_ = mapped(new_row())
        self.assertEqual(profile["financial"]["total_budget"], 100000)
        self.assertEqual(prefs["total_budget_ceiling"], 100000)

    def test_no_preference_steers_nothing(self):
        _profile, prefs, *_ = mapped(new_row(**{"Location preferences": "No preference"}))
        self.assertEqual(prefs["location_prefs"], [])
        _profile, prefs, *_ = mapped(new_row(**{"Location preferences": "Urban / City"}))
        self.assertEqual(prefs["location_prefs"], ["Urban / City"])

    def test_the_exact_ticks_are_kept(self):
        _profile, prefs, *_ = mapped(new_row(**{OTHER_PREFS: "Cold Weather, Low crime rate"}),
                                     SHEET_HEADERS + [OTHER_PREFS])
        self.assertEqual(prefs["other_preferences"], ["Cold Weather", "Low crime rate"])

    def test_the_muslim_facilities_tick_opens_halal_and_prayer(self):
        profile, *_ = mapped(new_row(**{OTHER_PREFS: "Muslim Facilities/Halal Food"}),
                             SHEET_HEADERS + [OTHER_PREFS])
        self.assertTrue(profile["needs"]["diet_halal"])
        self.assertTrue(profile["needs"]["worship_facilities"])


def report_row(**extra):
    return {"Timestamp": "30/10/2026 12:00:00", "Email Address": "buyer@b.com", "Full Name (as in IC)": "Report Buyer",
            REPORT_UNI: "Monash Malaysia", COURSE: "Law — become a lawyer; legal research, paralegal work",
            "Which year do you want to start? ": "2027", PROGRAMME: "UEC",
            "What are you applying with? ": "Actual Grades", "What did you take for Secondary school? ": "UEC",
            GRADES: "Physics A1, Maths B3", REPORT_QUESTION: "Can I do a law conversion?", NEW_CONSENT: AGREE, **extra}


class ReportFormRows(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.students = Path(tmp.name) / "students"
        self.students.mkdir()
        patcher = mock.patch.object(ingest, "STUDENTS_DIR", self.students)
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_ingest(self, rows, *flags, headers=REPORT_HEADERS):
        path = self.students.parent / "report.csv"
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        out = io.StringIO()
        with mock.patch.object(sys, "argv", ["ingest", str(path), *flags]), redirect_stdout(out):
            ingest.main()
        return out.getvalue()

    def read(self, slug, name="profile.json"):
        return json.loads((self.students / slug / name).read_text(encoding="utf-8"))

    def test_the_importance_grid_reaches_preferences(self):
        cells = {header: "Important" for header in TICKS}
        self.run_ingest([report_row(**cells)], headers=REPORT_HEADERS + TICKS)
        prefs = self.read("report-buyer", "preferences.json")
        self.assertEqual(len(prefs["priorities"]), 8)
        self.assertEqual(len(prefs["priority_levels"]), 8)

    def test_a_list_row_never_replaces_a_report_order_folder(self):
        self.run_ingest([report_row()])
        same_buyer = new_row(**{"Email Address": "buyer@b.com", "Full Name (As in IC)": "Report Buyer"})
        for flags in ((), ("--force",)):
            printed = self.run_ingest([same_buyer], *flags, headers=SHEET_HEADERS)
            self.assertIn("report order", printed)
            self.assertNotIn("use --force", printed)
            self.assertEqual(len(self.read("report-buyer")["report_orders"]), 1)

    def test_a_list_folder_still_refuses_a_second_list_row_as_before(self):
        self.run_ingest([new_row()], headers=SHEET_HEADERS)
        printed = self.run_ingest([new_row()], headers=SHEET_HEADERS)
        self.assertIn("use --force", printed)

    def test_row_creates_a_small_folder_with_the_order(self):
        self.run_ingest([report_row()])
        profile = self.read("report-buyer")
        self.assertEqual(len(profile["report_orders"]), 1)
        order = profile["report_orders"][0]
        self.assertEqual(order["university"], "Monash Malaysia")
        self.assertTrue(order["course"].startswith("Law"))
        self.assertEqual(order["start_year"], "2027")
        self.assertEqual(order["question"], "Can I do a law conversion?")
        self.assertEqual(order["submitted"], "30/10/2026 12:00:00")
        self.assertEqual(profile["current_program"]["type"], "UEC")
        self.assertEqual(profile["grade_status"], "actual")
        self.assertEqual(profile["_intake_raw"]["grades"], "Physics A1, Maths B3")
        self.assertIsNone(profile["financial"]["total_budget"])
        prefs = self.read("report-buyer", "preferences.json")
        self.assertEqual(prefs["target_countries"], [])
        self.assertIsNone(prefs["total_budget_ceiling"])
        self.assertEqual(prefs["priorities"], [])

    def test_budget_race_and_preferences_reach_the_folder(self):
        self.run_ingest([report_row(**{BUDGET: "200,000", RACE: "Chinese", LOCATION: "Urban / City",
                                       OTHER_PREFS: "Low crime rate, Cold Weather"})])
        profile = self.read("report-buyer")
        prefs = self.read("report-buyer", "preferences.json")
        self.assertEqual(profile["financial"]["total_budget"], 200000)
        self.assertEqual(prefs["total_budget_ceiling"], 200000)
        self.assertEqual(profile["ethnicity"], "Chinese")
        self.assertEqual(prefs["location_prefs"], ["Urban / City"])
        self.assertEqual(prefs["other_preferences"], ["Low crime rate", "Cold Weather"])
        self.assertTrue(profile["needs"]["personal_safety"])

    def test_existing_folder_gets_the_order_and_nothing_else(self):
        self.run_ingest([report_row()])
        before = self.read("report-buyer")
        before_prefs = (self.students / "report-buyer" / "preferences.json").read_bytes()
        changed = report_row(**{REPORT_UNI: "Sunway", PROGRAMME: "IB", GRADES: "Physics 7"})
        self.run_ingest([changed])
        after = self.read("report-buyer")
        self.assertEqual([o["university"] for o in after["report_orders"]], ["Monash Malaysia", "Sunway"])
        after.pop("report_orders"), before.pop("report_orders")
        self.assertEqual(after, before)
        self.assertEqual((self.students / "report-buyer" / "preferences.json").read_bytes(), before_prefs)

    def test_a_list_student_is_found_by_email_under_another_name(self):
        folder = self.students / "nickname"
        folder.mkdir()
        (folder / "profile.json").write_text(json.dumps({"name": "Nickname", "contact_email": "BUYER@b.com"}),
                                             encoding="utf-8")
        self.run_ingest([report_row()])
        self.assertFalse((self.students / "report-buyer").exists())
        self.assertEqual(len(self.read("nickname")["report_orders"]), 1)

    def test_same_name_with_another_email_is_never_merged(self):
        self.run_ingest([report_row()])
        printed = self.run_ingest([report_row(**{"Email Address": "other@b.com", REPORT_UNI: "Sunway"})])
        self.assertEqual(len(self.read("report-buyer")["report_orders"]), 1)
        self.assertIn("different email", printed)

    def test_force_never_overwrites_a_folder(self):
        self.run_ingest([report_row()])
        (self.students / "report-buyer" / "status.md").write_text("keep", encoding="utf-8")
        self.run_ingest([report_row(**{REPORT_UNI: "Sunway"})], "--force")
        self.assertEqual(len(self.read("report-buyer")["report_orders"]), 2)
        self.assertEqual(self.read("report-buyer")["_intake_raw"]["grades"], "Physics A1, Maths B3")

    def test_rerunning_the_same_answers_adds_no_second_order(self):
        self.run_ingest([report_row()])
        self.run_ingest([report_row()])
        self.assertEqual(len(self.read("report-buyer")["report_orders"]), 1)

    def test_two_orders_in_one_csv_land_in_one_folder(self):
        self.run_ingest([report_row(), report_row(**{REPORT_UNI: "Sunway"})])
        self.assertEqual(len(self.read("report-buyer")["report_orders"]), 2)

    def test_dry_run_writes_nothing(self):
        self.run_ingest([report_row()], "--dry-run")
        self.assertEqual(list(self.students.iterdir()), [])

    def test_declined_consent_is_still_skipped(self):
        self.run_ingest([report_row(**{NEW_CONSENT: ""})])
        self.assertEqual(list(self.students.iterdir()), [])

    def test_no_grades_answer_is_flagged(self):
        self.run_ingest([report_row(**{GRADES: ""})])
        self.assertTrue(any("no grades" in line for line in self.read("report-buyer")["_needs_review"]))


class ReportFormCheck(unittest.TestCase):
    """fetch_form_questions.py --check on the report form."""

    def form(self, *drop, option="I agree to my answers being used."):
        titles = {"Full Name": "name", REPORT_UNI: "uni", COURSE: "course", PROGRAMME: "programme",
                  GRADES: "grades", REPORT_QUESTION: "question", RACE: "race", BUDGET: "budget",
                  LOCATION: "location", OTHER_PREFS: "other"}
        items = [{"title": t, "type": "TEXT", "required": True} for t, tag in titles.items() if tag not in drop]
        items.append({"title": NEW_CONSENT, "type": "MULTIPLE_CHOICE", "required": True, "options": [option]})
        return {"title": "Report form", "items": items}

    def check(self, form):
        out = io.StringIO()
        with redirect_stdout(out):
            code = questions.check_report_form(form)
        return code, out.getvalue()

    def test_a_correct_form_passes(self):
        code, printed = self.check(self.form())
        self.assertEqual(code, 0)
        self.assertNotIn("no question matches", printed)

    def test_a_missing_grades_question_is_named(self):
        _code, printed = self.check(self.form("grades"))
        self.assertIn("grades_raw", printed)

    def test_a_missing_budget_race_or_preference_question_is_named(self):
        for tag, key in [("budget", "total_budget"), ("race", "ethnicity"),
                         ("location", "location_prefs"), ("other", "needs")]:
            _code, printed = self.check(self.form(tag))
            self.assertIn(key, printed)

    def test_consent_may_name_race_now_the_form_asks_it(self):
        code, _printed = self.check(self.form(option="I agree, including my race."))
        self.assertEqual(code, 0)

    def test_a_grid_that_allows_two_ticks_per_row_is_named(self):
        for grid_type, warned in (("CHECKBOX_GRID", True), ("GRID", False)):
            form = self.form()
            form["items"].append({"title": TICK, "type": grid_type, "columns": ["Must have"]})
            code, printed = self.check(form)
            self.assertEqual(code, 0)
            self.assertEqual("Multiple choice grid" in printed, warned)


class LiveFormTitles(unittest.TestCase):
    """Reads the tracked forms/*.json, so a form edit that breaks a match fails here."""

    def titles(self, name):
        """The sheet headers this form produces (page titles never become columns)."""
        items = json.loads((ROOT / "forms" / f"{name}.json").read_text(encoding="utf-8"))["items"]
        return questions.sheet_headers(items)

    def test_list_form_grade_questions_match(self):
        index = ingest.build_col_index(self.titles("intake"))
        for key in ("grades_raw", "program_type", "current_completion", "secondary_qualification",
                    "target_countries", "needs", "consent", "name"):
            self.assertIn(key, index)

    def test_every_list_form_question_goes_somewhere(self):
        headers = self.titles("intake")
        known = set(ingest.build_col_index(headers).values()) | set(ingest._slider_columns(headers).values())
        self.assertEqual([h for h in headers if h not in known], [])

    def test_report_form_questions_match(self):
        index = ingest.build_col_index(self.titles("report_intake"))
        for key in ("consent", "name", "report_university", "report_question", "specific_courses",
                    "program_type", "grade_status", "secondary_qualification", "intake",
                    "english_test", "english_score", "lesson_language", "achievements_text",
                    "grades_raw", "ethnicity", "total_budget", "location_prefs", "needs"):
            self.assertIn(key, index)

    def test_every_report_form_question_goes_somewhere(self):
        headers = self.titles("report_intake")
        known = set(ingest.build_col_index(headers).values()) | set(ingest._slider_columns(headers).values())
        self.assertEqual([h for h in headers if h not in known], [])

    def test_report_form_asks_all_eight_priorities(self):
        self.assertEqual(len(ingest._slider_columns(self.titles("report_intake"))), 8)


if __name__ == "__main__":
    unittest.main()
