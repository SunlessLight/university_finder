# Carry-over: English-test waivers (S9, R21) and family income (S3) (2026-10-27)

**Goal:** finish backlog group 2 step 3 in `business/additionals.md` before the first paid student's form is read in (paid lists due 2026-11-10).
**Where it stands:** S9 and R5 are done and committed. R21's four cells are fixed; its wider sweep is open. S3 is decided by Evan, and the small workflow edit waits on his "go".

## Done this session
- S9 years rule: `LESSON_LANGUAGE_YEARS` + `_years_in_english()` → `english_proficiency.years_in_english_min` → [tools/ingest_form_csv.py](../../tools/ingest_form_csv.py), [tools/init_student.py](../../tools/init_student.py), [workflows/01_intake.md](../../workflows/01_intake.md), [workflows/08_application_prep.md](../../workflows/08_application_prep.md), IELTS line in [tools/apply_glossary.py](../../tools/apply_glossary.py) · checked by: all six form answers, an "Other" answer and a blank through `map_row`; `fetch_form_questions.py --check --offline` ok; calendar tests pass. Commit `259623e`.
- S9 UK half: UCL, Imperial and KCL official pages read via Firecrawl. None waives IELTS for English-taught schooling in Malaysia · checked by: page text seen (saved in `.tmp/s9/`).
- R5: three slider comments fixed in `ingest_form_csv.py` · comment-only.
- R21: four `English req` cells rewritten via `apply_backfill.py --overwrite` from `.tmp/r21/<slug>/` (lai-zheng-yi: UCL, Imperial, KCL; toru: Imperial) · checked by: dry run, `check_master_list.py` (no new findings), a before/after diff (3 + 1 cells changed). Backup of both lists in that session's scratchpad (temporary). Commit `ad95f33`.
- Build log, decision log, Now box and the Notion "Shortlisted — Now" page updated for all of the above (the last edits are not committed yet).

## Decisions (don't re-ask)
- The lesson-language answer becomes a floor of years (all through = 5, pre-university only = 1, Malay/Chinese = 0, DLP / Not sure = null), because a floor never claims a waiver the student lacks. Claude suggested; logged in `decisions/log.md`.
- Fix the four R21 cells: Evan said yes.
- S3: the system never collects family income. A US need-based finalist's report shows the university's own published income-band examples (in MYR) plus a CSS Profile link. Evan decided, because income is sensitive and students rarely know it.

## Not done yet
- Waiting on Evan's "go" for the S3 edit. Claude suggested also linking each university's net price calculator (MyinTuition for MIT and others), because the CSS Profile is the aid application, not an estimate. Default: include it.
- R21 sweep: about 40 more `English req` cells on 11 lists tie a waiver to A-Levels or English-medium schooling. Do Shortlist/Finalist rows first (~15, four students), plus toru's Oxford and Cambridge cells. See R21 in `additionals.md`.
- Commit for the last edits: `plans/build-log.md`, `decisions/log.md`, `STATUS.md`, this note.

## Next steps
1. Ask Evan to commit the last edits, and ask for "go" on S3 if he hasn't given it.
2. On go: in [workflows/04_university_report.md](../../workflows/04_university_report.md), step 10 "Costs" (~line 286) and the `net_cost` example (~line 394), replace the "your-share" figure with 2–3 official income-band examples in MYR (dated) + the net price calculator link (or "none for internationals") + the CSS Profile link. Same in `08_application_prep.md` → Financial aid `covers` (~line 134). Change the `net_cost` sample line in `tools/build_report.py:63`. Then tick S3 in `additionals.md` and add a line under group 2 step 3.
3. Later (after 2026-11-10): the R21 sweep, one student per session, using the same fragment method.

## Read first
- `business/additionals.md` → S3 (~line 1206) and R21 (end of file): the open work.
- `workflows/04_university_report.md` steps 10–11: where the cost and aid text lives.

## Gotchas
- Free WebFetch gets 403/404 on UCL, Imperial and KCL pages. `tools/firecrawl_search.py "<query>" --scrape-top 1 --out <file>` worked.
- `py -I` can't find `tests.test_calendar_dates`. Run `python -m unittest tests.test_calendar_dates -v` without `-I`.
- `map_row` returns `(slug, profile, prefs, needs_review, err)`, and it needs a nickname column plus `assume_consent=True` for a fake row.
- lai-zheng-yi's `status.md` is already over its 3000-character budget, so don't add lines to it.
- Another session was editing `STATUS.md` at the same time; read it before editing.
