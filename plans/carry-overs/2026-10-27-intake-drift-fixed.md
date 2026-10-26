# Carry-over: intake form drift fixed (2026-10-27)

**Goal:** Claude reads all four Google Forms itself, and the intake form matches what `ingest_form_csv.py` expects before the next student answers.
**Where it stands:** The drift is fixed and `fetch_form_questions.py --check` is clean (exit 0). Two questions for Evan are still unanswered (below). No student has answered since 14 Oct, so nobody was affected.

## Done this session
- `ingest_form_csv.py`: `SUBJECT_GRID_MARKER` widened to "grades for your subjects" (F1); `"doesn't matter": 0` in `TICK_IMPORTANCE_NORMALIZE` (F6); `("what are you applying with", "grade_status")` added to `QUESTION_MAP`; two `COURSE_ACCREDITATION_MAP` keys renamed to the live titles ("Humanities & Philosophy", "Business Administration & Management"); `_course_title()` also splits on " - " (the live Psychology option uses a hyphen). → [tools/ingest_form_csv.py](../../tools/ingest_form_csv.py) · checked by: live `--check` exit 0, plus a fake row built from the live headers through `map_row` (grades, course, grade_status=actual, all 8 priorities with "Doesn't matter" last, no review flags). Calendar tests pass.
- `fetch_form_questions.py`: the comma check only covers the split fields (`SPLIT_KEYS` = needs, target_countries, location_prefs). → [tools/fetch_form_questions.py](../../tools/fetch_form_questions.py) · checked by: 36 false alarms gone.
- Evan had already changed the form himself: course and budget are now single-choice dropdowns (F2, F3); consent retention is filled in as "3 months" / "3 bulan" (F5). `forms/intake.json` refreshed. · checked by: diff of `forms/intake.json`.
- [workflows/01_intake.md](../../workflows/01_intake.md) and [google_form_notes.md](../../google_form_notes.md) updated to the new wording.
- Committed as `2a629a1`. Build log, Now box and the Notion "Shortlisted — Now" page updated.

## Decisions (don't re-ask)
- "Doesn't matter" ranks last rather than being skipped, because `derive_weights.py` refuses a priorities list missing any of the 8 tokens. Claude decided (it was the default in the previous note).
- "What are you applying with?" maps to `grade_status` without asking Evan: it replaced the old "forecast result or actual" question. Claude decided.
- Course and budget stay single choice. Evan decided by changing the form.

## Not done yet
- **Waiting on Evan (asked, not yet answered):**
  1. F4: should the program copy "What did you take for ur secondary school?" (IGCSE/SPM) and the lesson-language answer into the profile as-is now? Default: yes, as raw fields, and the years-of-English rule comes later under backlog S9 (group 2 step 3). These are the only two unmapped headers left.
  2. Is "3 months" retention in the consent text intended (it was "[12 months]")? Default: keep it.
- The second commit (`STATUS.md`, `plans/build-log.md`, this note) is being made at hand-over. If `git status` still shows them modified, commit them.
- Earlier leftovers: set both feedback sheets to Restricted, then switch `fetch_feedback.py` to `fetch_form_answers.py`; `.env.example` lacks the FORM_ID keys (a deny rule blocks reading it); one Notion task still says "27 testers"; "$" on the sample spreadsheet's MYR column (Evan).

## Next steps
1. Get Evan's answers to the two questions. If F4 is yes: add two `QUESTION_MAP` entries + raw profile fields, rerun `--check --offline` until no unmapped headers, and rerun the scratch-style `map_row` smoke test.
2. Then I12 and I11 (backlog group 2 step 11), and the feedback-sheet switch.

## Read first
- [business/additionals.md](../../business/additionals.md) → S9 (lesson language, decided 2026-10-25), I11, I12.
- `ingest_form_csv.py` `map_row()` (returns 5 values: slug, profile, prefs, needs_review, skip_reason).

## Gotchas
- The auto-mode check blocks any read of `.env`. Debug form IDs per form (`--form <name>`).
- `data/form/intake_answers.csv` is all intake answers; `responses.csv` is only the pending Stage 1 batch.
- `--check --offline` uses the saved `forms/intake.json`; drop `--offline` to fetch the live form (it rewrites that file).
- A commit (`55de8d4`) landed between sessions with the previous logs; check `git log` before assuming files are uncommitted.
