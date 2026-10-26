# Carry-over: intake form drift after form access (2026-10-27)

**Goal:** Claude reads all four Google Forms (questions and answers) itself, and the intake form matches what `ingest_form_csv.py` expects before the next student answers.
**Where it stands:** Form access is done and committed. The first `--check` found six mismatches (F1–F6) between the live intake form and the reading program. None fixed yet. No student has answered since 14 Oct, so nobody is affected yet.

## Done this session
- `answers` action in [tools/appsscript/Code.gs](../../tools/appsscript/Code.gs) + new [tools/fetch_form_answers.py](../../tools/fetch_form_answers.py); README setup step 5 fixed · checked by: live run, all four forms (intake 10, report fb 12, sheet fb 15, survey 84 = the manual export). Commit `f433672`.
- All four forms' questions → [forms/](../../forms/) · checked by: live run; no emails in them. Commit `9822ac6`.
- `--check` run on the intake form (findings below) · checked by: output seen; F1, F2 and the comma false alarm checked against the code.
- Build log, Now box and `decisions/log.md` updated (not committed).

## Decisions (don't re-ask)
- `answers` is read-only even for intake, and lives in its own tool so answers never land in tracked `forms/`. Claude suggested, Evan said go.
- The form IDs in `.env` are form IDs (from `/forms/d/<ID>/edit`), not spreadsheet IDs. One script reaches every form because it runs as Evan. Explained to Evan; he understood.
- The budget's three plain-number options are intended (decision 2026-10-26). Only its checkbox type is the problem (F3).

## Not done yet
F1–F6 = the intake `--check` findings:
- **F1 🔴** The grades grid is now titled "Select the grades for your subjects…". `SUBJECT_GRID_MARKER` (`ingest_form_csv.py:333`) is "forecast grades for your subjects", so every new student's grades come out blank. Code fix: match both wordings.
- **F2 🟠** "Choose your desired course" is now CHECKBOX with Other. The code (`ingest_form_csv.py` ~826–839) assumes a single choice, so two ticks become one glued string and recognition matching fails. Default: Evan switches it to Multiple choice. Ask whether he wants several courses first.
- **F3 🟠** The budget question is CHECKBOX. Default: Evan switches it to Multiple choice.
- **F4 🟡** Three new questions aren't mapped in `QUESTION_MAP`: "What did you take for ur secondary school?", lesson language, and "what are you applying with?" (this replaced "forecast result or actual", so `grade_status` is no longer read). Ask Evan what each should feed.
- **F5 🟡** The consent text shows "[12 months]" / "[12 bulan]". This is the only check failure (exit 1). Default: Evan deletes the brackets.
- **F6 🟢** The grid column "Doesn't matter" is missing from `TICK_IMPORTANCE_NORMALIZE`. Default: add it as 0.
- The check's 36 "checkbox option with a comma" warnings are false alarms: courses and budget never go through `_split_multi`. Narrow that check to fields that are split.
- Earlier carry-over leftovers: set both feedback sheets to Restricted, then switch `fetch_feedback.py` to `fetch_form_answers.py`; `.env.example` lacks the FORM_ID keys (a deny rule blocks reading it); one Notion task still says "27 testers"; "$" on the sample spreadsheet's MYR column (Evan).
- Commit STATUS.md, `plans/build-log.md`, `decisions/log.md` and this note (Evan to approve).

## Next steps
1. Fix F1 + F6 in `ingest_form_csv.py`, and narrow the comma check in `fetch_form_questions.py`. Then run `python -X utf8 tools/fetch_form_questions.py --check`.
2. Give Evan the form clicks for F2, F3 and F5 in one message. Ask the F2 and F4 questions with defaults.
3. Once he's done: rerun `--check` until clean, and commit `forms/intake.json`.
4. Then I12 and I11 (backlog group 2 step 11), and the feedback-sheet switch.

## Read first
- [plans/carry-overs/2026-10-26-form-access.md](2026-10-26-form-access.md) → Next steps 1–3 (marked done) — how the access was set up.
- [business/additionals.md](../../business/additionals.md) → I10, I11, I12.
- `ingest_form_csv.py` `QUESTION_MAP` and `SUBJECT_GRID_MARKER`.

## Gotchas
- The auto-mode check blocks any read of `.env`, even printing ID lengths. Debug a form ID by calling the tool per form (`--form <name>`), or `call_endpoint(url, token, 'questions')` with no ID (the sheet-link fallback).
- `data/form/intake_answers.csv` is all intake answers; `responses.csv` is only the pending Stage 1 batch. Don't mix them.
- Explain the whole picture to Evan before giving steps. He mixed up form vs spreadsheet IDs because "the script lives in the spreadsheet".
