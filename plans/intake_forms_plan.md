# Plan: split the intake form into a List form and a Report form

## Context

Evan sells two products: the list of 20–30 universities (RM50) and one deep university report
(RM30). Both buyers get the same 23-question form, so report buyers answer about 10 questions
nothing uses. The grade grid also only fits A-levels, while the bunting names STPM, UEC, IB,
Foundation and Matriculation.

Agreed with Evan on 30 Oct:
- Two forms. The current form stays as the list form (same ID). The report form is a copy with
  questions removed.
- The RM30 report includes "your fit".
- Grades = a programme dropdown + one free-text box. AI tidies, a script checks.
- Budget stays a dropdown.
- A 30-second human look at tidied grades until 20 forms in a row need no correction.

**Corrections to what Claude said earlier in chat:**
- "Under RM 100,000" would have been silently wrong: the script reads any label with "under" as
  RM 500,000. The option is a plain **100,000**, matching the others.
- No branching is needed any more. One text box replaces the grid for everyone, A-levels too.
- The grade checker was going to wait until after 10 Nov. It's small and pilot students will
  depend on it, so it's now before the pilot.
- Keep the Location labels "Urban / City" and "Rural / Campus-based" (no code change), rather than
  the new labels suggested.
- Fixing typos in question titles is not cosmetic: the script matches some typos on purpose
  ("perferences", "Chose", "ur"), so those need code first.
- New scope: Stage 3 (the research step) assumes A-levels in places. Accepting other programmes
  means telling the research helpers to look up the right entry bar (T4).

**Answer to "what needs the forms first?"** Almost nothing. The code is updated first to accept
both the old and new wording, so the switch is safe in either order. Only the checks at the end
and the report form's ID need the real forms.

## Where this stands (30 Oct, end of the build session)

- **Done and tested:** T1, T2, T3, T4, T5, T7 (72 tests pass). Old-form rows: all 10 real rows give
  the same answers as before.
- **T6, half done:** `REQUIRED_KEYS` and the report-form check are in. The list form's check is
  clean. The report form's check fails on the first two items below, which is right.
- **E1 was done before the code**, so the code follows the real forms, not the drafts below.

**Changed 30 Oct, after Evan read this plan:** the report form now asks budget, race and preferences
as well, and still has no importance grid. Its consent stays as it is, so the old fix "remove race
and halal from the consent" is cancelled. The report compares cost with the budget, says which funds
the student can apply for, and shows halal or prayer content only if ticked. Every student report
opens with a "Your profile" table (never their race). `--check` lists the five missing questions.

### Evan's fix list (report form unless it says otherwise)

1. **Add 5 questions, copied from the list form with the exact same title and options:** the grades
   question (B7), Race, the budget question, Location preferences, and "Any other perferences?".
2. **Consent notice (not the answer):** in both languages, remove "country choices" and "priorities"
   from the "What we collect" list, because this form doesn't ask them. Keep race, budget and preferences.
3. **Link to Sheets** (E1d): Responses tab.
4. **`.env`:** `FORM_ID_REPORT_INTAKE=16FgLQvxA-BA1wCBbJuMYMgKmqe6oYady9CA2QWjpRnM` (E1e).
5. **Check "Collect email addresses" is on.** It's how a buyer's existing folder is found.
6. **Submit one test answer on each form** (E1f), using a plus-address (`you+test3@gmail.com`).
7. **Both forms: decide O10** (name vs the notice's "nickname"). **List form: decide O11** (the year).
8. **Small, either way:** the report form has no Disclaimer page or the B13 note. The list form's
   grades box has no STPM/CGPA example and is a short answer, not a paragraph. Location has no
   "No preference". Race has no "Other". The scripts handle all of these.

Then say "T6", and Claude finishes the check. Only then E2.

### What the live forms say, where it differs from the tables below

| Planned | Live | Code |
|---|---|---|
| "Type your subjects and grades" | "Type you subject and grades (eg. physic A, Chemistry B, etc)" | Both match |
| "What month does your final result come out?" | "What month does your actual result come out?", made from the year question, so there's no year now | New match; "no year" review line |
| "Which course?" text box | "Choose your desired course" + the specific-field box | Reuses the list form's course logic |
| "Which university is this report for?" | "Which University do you want a report of?" | `want a report` |
| "Name you used when paying" | "Full Name (as in IC)" | Existing `full name` |
| "What did you take for your secondary school?" | List: unchanged ("ur"). Report: "for Secondary school?" | All match |
| Typos fixed in "Chose" and "perferences" | Left as they were | Old and new both match |

### Added while building (not in the plan)

- `merge_duplicate_columns()`: the sheet keeps a replaced question's column, so without it every new
  student read as "no consent" and was skipped.
- A same-name folder with a different email is never merged.
- `check_report.py` drops the "Your priorities" row for a report order.
- `grade_status` "Not sure" (report form) stays blank, for finalize to ask.
- `check_report.py` flags halal or prayer wording the student didn't ask for (`faith`).
- `preferences.other_preferences` keeps the exact ticks. "Muslim Facilities/Halal Food" sets both flags.

## The forms as drafted (the live wording is in forms/*.json)

### Form A: list form (edit the current form)

| # | Question | Change | Code needed? |
|---|---|---|---|
| A1 | NEW, after secondary school: **Which pre-university programme are you doing?** Dropdown: A-Level / STPM / UEC / IB / Foundation / Matriculation / Diploma / Other. Required | Add | Yes |
| A2 | Delete the grade grid. NEW: **Type your subjects and grades**. Paragraph, required. Help text: `e.g. Physics A*, Chemistry A, Maths A. STPM: Physics A-, Maths B+. Foundation or Diploma: CGPA 3.6` | Replace | Yes |
| A3 | **What month does your final result come out?** Options: January … December | Reword, new options | No |
| A4 | **What did you take for your secondary school?** Add UEC, O-Level, Other | Fix "ur", add options | Yes |
| A5 | Race: add Other, Prefer not to say | Add options | No |
| A6 | **Choose your countries**. Make it required | Fix typo | Yes |
| A7 | Budget: add **100,000** as the first option | Add option | Yes |
| A8 | Location preferences: remove "Near family" and "Close to public transport", add **No preference** | Change options | Yes |
| A9 | **Any other preferences?** Make it optional | Fix typo | Yes |
| A10 | Disclaimer page title: fix "Disclamer" | Typo | No |

Keep every other title word-for-word.

### Form B: report form (Make a copy of Form A, then delete and edit)

| # | Question | Type | Required |
|---|---|---|---|
| B1 | Name you used when paying (so I can match your payment) | Short text | ✔ |
| B2 | Which university is this report for? Add the campus if it has several (e.g. Monash Malaysia) | Short text | ✔ |
| B3 | Which course? Write "Not sure yet" if undecided | Short text | ✔ |
| B4 | Which year do you want to start? 2027 / 2028 / Not sure | Choice | ✔ |
| B5 | Which pre-university programme are you doing? (same as A1) | Dropdown | ✔ |
| B6 | what are you applying with? Forecast Grades / Actual Grades (keep) | Choice | ✔ |
| B7 | Type your subjects and grades (same as A2) | Paragraph | ✔ |
| B8 | What did you take for your secondary school? (same as A4) | Choice | ✔ |
| B9 | Lesson language question (keep word-for-word) | Choice | ✔ |
| B10 | English Test Taken + "If English test taken, what's the score?" (keep) | Choice + text | ✔ / optional |
| B11 | Achievements / activities… (keep) | Paragraph | |
| B12 | Anything specific you want this report to answer? | Paragraph | |
| B13 | Note: "Bought the list too? Fill that form as well." | Description only | |
| B14 | Consent + disclaimer: keep the word "consent" in the title. Race and halal stay in the answer, because the form now asks them | Choice | ✔ |
| B15 | NEW 30 Oct: Race, budget, Location preferences and "Any other perferences?", copied from Form A | Same as A | Same as A |

## How the report's "fit" part will work

A report buyer gets a small student folder (`data/students/<slug>/`). It's already kept out of git
and it's where reports already go. `data/quick_reports/` must not be used because it's meant for
reports with no personal data, and two buyers of the same university would overwrite each other.
The same intake script reads both forms, so consent checks and grade handling aren't rebuilt.

## Tasks

### [x] T1. Save the notes and this plan
- **Who:** Claude. **Needs:** none. **Size:** S.
- **Touches:** `plans/intake_forms_plan.md` (copy of this file), `plans/discussions.md`,
  `decisions/log.md`, `business/additionals.md`, `business/launchx/status.md`, `STATUS.md`,
  `plans/build-log.md`, Notion "Shortlisted — Now" and Tasks.
- **Do:**
  - Log the decisions (Context above) in `decisions/log.md`, append-only.
  - Add a section to `plans/discussions.md`, including the 20-clean-forms tally (starts at 0).
  - Add a backlog entry for "no human look at grades after 20 clean forms".
  - In `status.md`, replace the "Not doing A-levels?" item with this plan's steps, and update
    "After payment the customer gets the existing Google Form".
- **Done when:** the plan is in `plans/`, the Now box names it as the form work, Notion is updated.

### [x] T2. Teach the intake script the new list-form wording (old wording keeps working)
- **Who:** Claude. **Needs:** none (**forms not needed**). **Size:** M.
- **Touches:** `tools/ingest_form_csv.py`, `tools/fetch_form_questions.py`,
  `tests/test_intake_forms.py` (new).
- **Do:**
  - Add to `QUESTION_MAP`, keeping the old entries: `("subjects and grades", "grades_raw")`,
    `("pre-university programme", "program_type")`, `("your secondary school", ...)`,
    `("choose your countries", ...)`, `("any other preferences", "needs")`.
  - Set `profile["current_program"]["type"]` from `program_type`; blank stays "A-Level" so old
    rows are unchanged. `build_list_pdf.py` then prints the right programme by itself.
  - Add `"100000": 100000` to `BUDGET_LIMIT_EXACT`.
  - Turn "No preference" into an empty `location_prefs`, so it doesn't steer the location score.
  - Update the `_needs_review` line for free-text grades to mention the programme and check_grades.
  - Add `grades_raw` and `program_type` to `REQUIRED_KEYS` only in T6, once the form has them,
    otherwise `--check` fails on the live form today. Check first that the students' pending
    rows from the old form still run.
- **Done when:** the new test passes for: an old-form row (grid) giving the same result as before,
  a new-form row (free text) landing in `_intake_raw.grades`, and 100,000 → RM 100,000.
- **Prompt:** "Read plans/intake_forms_plan.md and do T2 only. Run the tests. Offer the commit."

### [x] T3. Build the grade checker
- **Who:** Claude. **Needs:** none (**forms not needed**). **Size:** S–M.
- **Touches:** `tools/check_grades.py` (new), `tests/test_check_grades.py` (new).
- **Do:** `python tools/check_grades.py --student <slug>` reads `profile.json` and fails on any
  grade impossible for `current_program.type`, using `current_program.type` as the scale:
  - A-Level: A*–E
  - STPM: A, A-, B+, B, B-, C+, C, C-, D+, D, F
  - UEC: A1, A2, B3–B6, C7, C8, F9
  - IB: 1–7 per subject, total up to 45
  - Foundation / Matriculation / Diploma: CGPA 0–4.0
  - Other: no scale, always raises a review line

  Also fail when the tidied list has fewer subjects than the raw text appears to name, so a dropped
  subject is caught. Print raw text and tidied list side by side for the 30-second look.
- **Done when:** the test proves "A*" in STPM and "50" in IB fail, and a correct example passes.
- **Prompt:** "Read plans/intake_forms_plan.md and do T3 only. Offer the commit."

### [x] T4. Tell the research helpers about non-A-level students
- **Who:** Claude. **Needs:** none (**forms not needed**). **Size:** S.
- **Touches:** `.claude/agents/row-filler.md`, `workflows/03_discover_longlist.md`.
- **Do:** Add one rule: read `current_program.type` and compare against the entry bar published
  for that programme. If the university doesn't publish one, use `Not published`, and never
  convert to A-level grades by guesswork.
- **Done when:** the rule is in both files and names `Not published`.
- **Prompt:** "Read plans/intake_forms_plan.md and do T4 only. Offer the commit."

### [x] T5. Report form route (report with "your fit")
- **Who:** Claude. **Needs:** T2, and don't run alongside backlog step 9 (R33/R34): both edit
  `build_report.py` and `report-writer.md`. **Forms not needed to write it; a fake CSV tests it.**
  **Size:** M.
- **Touches:** `tools/ingest_form_csv.py`, `tools/fetch_form_questions.py`,
  `tools/fetch_form_answers.py`, `tools/build_report.py`, `tools/progress_dashboard.py`,
  `.claude/agents/report-writer.md`, `tests/test_intake_forms.py`.
- **Do:**
  - Add `"report_intake": "FORM_ID_REPORT_INTAKE"` to `FORMS`, and `data/form/report_answers.csv`
    to the paths in `fetch_form_answers.py`.
  - Confirm a blank ID doesn't break a normal run, as with the other optional forms.
  - Add to `QUESTION_MAP`: `("name you used", "name")`, `("report for", "report_university")`,
    `("which course", "report_course")`, `("anything specific", "report_question")`.
  - When a CSV has `report_university`, append to `profile["report_orders"]`.
  - **If the buyer already has a folder, only add the order and touch nothing else.** Never use
    `--force` here, because `data/students/` has no undo.
  - `build_report.py`: when the student has no `master_list.csv`, stop after writing the report,
    with no finalist marker (same as `--quick`).
  - `report-writer.md`: add this third dispatch type (slug, no master list). Keep the fit halves of
    `who_its_for`, `getting_in` and `why_here`, keep `admission_likelihood`, leave out `priorities`,
    and answer `report_question` inside the report.
  - `progress_dashboard.py`: show these students as "Report order", not stuck at Stage 1.
- **Done when:** a fake report CSV creates a folder with `report_orders` and no country noise, and
  an existing folder keeps every other field unchanged.
- **Prompt:** "Read plans/intake_forms_plan.md and do T5 only. Check step 9 of
  business/additionals.md is finished or not in progress first. Offer the commit."

### [ ] E1. Evan edits and creates the forms
- **Who:** Evan, in Google Forms. **Needs:** T2 for E1a; E1b can happen any time.
- **E1a, wait first:** check the 2 list buyers have submitted, so nobody is mid-form.
- **E1b, Form A:** make changes A1–A10. Existing answers stay in the sheet.
- **E1c, Form B:** ⋮ → Make a copy, then edit to B1–B14.
- **E1d:** in Form B's Responses tab, click **Link to Sheets**. A copied form has no linked sheet,
  and `fetch_form_answers.py` can't read it without one.
- **E1e:** add `FORM_ID_REPORT_INTAKE=<ID>` to `.env`. The ID is the long code in the form's edit
  address.
- **E1f:** submit one test answer on each form.
- **Done when:** Evan tells Claude it's done.

### [ ] T6. Check the real forms (needs the forms)
- **Who:** Claude. **Needs:** T2, T5, E1. **Size:** S.
- **Touches:** `forms/intake.json`, `forms/report_intake.json`, `tools/fetch_form_questions.py`.
- **Do:**
  - Add `grades_raw` and `program_type` to `REQUIRED_KEYS`.
  - Run `python tools/fetch_form_questions.py --check`. Extend the check to Form B's own questions.
  - Add `grades_raw`, `ethnicity`, `total_budget`, `location_prefs` and `needs` to
    `test_report_form_questions_match`, now the saved form has them.
  - Fetch the test answers, then run `python tools/ingest_form_csv.py <csv> --dry-run` on each.
  - Stop and show Evan any problem before anything gets written.
  - Evan deletes the test rows, only when no unconfirmed `responses.csv` is on disk (deleting rows
    shifts the rows below them).
- **Done when:** the check is clean and both dry runs show the test answer in the right fields.
- **Prompt:** "Read plans/intake_forms_plan.md and do T6 only. Do not write to data/students/."

### [x] T7. Update the how-to files (after the wording is final)
- **Who:** Claude. **Needs:** T3, T5, T6. **Size:** M.
- **Touches:** `workflows/01_intake.md`, `workflows/quick_university_report.md`,
  `workflows/00_overview.md`, `workflows/04_university_report.md`, `README.md`.
- **Do:**
  - `01_intake.md`: replace the grid description. Finalize step 1 becomes: tidy
    `_intake_raw.grades` into `subjects[]`, run `check_grades.py`, show Evan raw vs tidied, update
    the tally. The free-text path is no longer "legacy". Note "Prefer not to say" means unknown for
    scholarship research: don't assume eligibility either way.
  - Add the Form B route. In `quick_university_report.md`, say a paid report uses the new route
    while quick reports stay facts-only.
  - Add `check_grades.py` to the tool lists.
- **Done when:** a search for "12-column" and "subject grid" in current instructions finds nothing
  stale, and `README.md` covers both forms.
- **Prompt:** "Read plans/intake_forms_plan.md and do T7 only. Offer the commit."

### [ ] E2. Evan points each buyer at the right form
- **Who:** Evan. **Needs:** T6.
- **Do:** Use the Form A link for list buyers and Form B for report buyers in the after-payment
  message. Send Form B to the 2 report buyers who paid. A buyer of both gets both links.

## Run order

```
STAGE 1 (one session, in order) → T1, T2, T3, T4
STAGE 2 (new session)           → T5            (needs T2; not alongside step 9)
STAGE 3 (Evan, by hand)         → E1            (needs T2)
STAGE 4 (one session, in order) → T6, T7        (needs T3, T5, E1)
STAGE 5 (Evan)                  → E2            (needs T6)
```

- Stage 1 tasks don't clash, but they're small enough (about 60k tokens) to run in one session.
- Stage 1 should finish before the booth prep on 3 Nov. Everything is due before 10 Nov.
- **If time runs out:** Form A's route (T2–T4, E1b, T6) is what the pilot needs. Report buyers can
  be handled in the meantime by Claude reading Form B's answers one at a time.

**Hand-off:** tick each task in `plans/intake_forms_plan.md` in the same commit. Each session adds
to `plans/build-log.md`, updates the Now box, and syncs Notion.

## Verification

1. `python -m unittest tests.test_intake_forms tests.test_check_grades tests.test_list_checks tests.test_calendar_dates`
2. `python tools/fetch_form_questions.py --check` is clean on the live forms.
3. `--dry-run` shows a test answer from each form landing in the right fields.
4. An old-form CSV still gives the same result as before (protects the 2 list buyers).
5. The first real STPM or UEC student: Evan reads the raw vs tidied grades, and the list PDF shows
   the right programme.

Only files each task touched get committed. The unrelated changes already in
`forms/survey.json`, `business/launchx/survey.md` and `workflows/countries/uk.md` stay out.
