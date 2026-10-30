# Carry-over: T7 sample re-check (2026-10-30)

**Goal:** finish task T7 of [plans/list_pdf_plan.md](../list_pdf_plan.md): the public sample's 15 rows (source student `toru`) re-checked on official pages, so `check_master_list.py` is clean on them and the T6 PDF command builds without `--draft`.
**Where it stands:** all research is done and reviewed. A full rehearsal on a copy passes. **toru's real files are not written yet.** Evan was asked "write it?" and chose a new session instead. Ask him once more, then write.

## Done this session
- 15 backfill fragments researched, then patched by the main session → `.tmp/toru/backfill_t7/` (helpers' originals: `.tmp/t7/backfill_t7_helpers_original/`) · checked by: `.tmp/t7/selfcheck.py` OK on all 15; `apply_backfill.py --dry-run` = 264 cells, 15 rows, 0 refused.
- Main-session readings in Chrome: all 30 QS ranks (`.tmp/t7/qs_ranks.json`), Home Affairs AUD 29,710, Melbourne's scholarships (Malaysia not eligible for MIUS; Excellence Scholarship swapped in). Applied by `.tmp/t7/patch_fragments.py --letters` (re-runnable).
- Checker fix: `Application requirements` skipped by the hedge scan → [tools/check_master_list.py](../../tools/check_master_list.py), +1 test in [tests/test_list_checks.py](../../tests/test_list_checks.py) · checked by: 18 tests pass (`py -X utf8 -m unittest tests.test_list_checks`).
- R25: [workflows/countries/uk.md](../../workflows/countries/uk.md) Cambridge note now says "(2027 entry)" · not checked beyond the edit.
- Rehearsal `py -X utf8 .tmp/t7/rehearse.py` (copies only, `.tmp/t7/preview/`): backfill → recompute → check 0 findings on 15 rows → PDF built without `--draft` (14 universities). Old → new list: `.tmp/t7/dryrun_review.md` (279 cells).
- Build log and `decisions/log.md` entries written.

## Decisions (don't re-ask)
- Checker exemption above. Evan chose it over dropping letter counts.
- Harvard Annual tuition includes mandatory fees: USD 68,442. Evan agreed.
- R23: Rose-Hulman → "Safety (high admit rate)" (80.9%); Northeastern → "Reach (very selective)" (5.6%); both "Grades vs entry bar" → Not published (`.tmp/t7/r23.json`). Claude's call, shown in the dry-run summary.
- Cambridge admit rate uses Table 3.2's Malaysia row, written "15.2% of international applicants offered a place". Claude's call, told to Evan.
- Living cost: the university's own figure, else the visa benchmark AUD 29,710 (Monash, Melbourne).

## Not done yet
- Evan's yes to write toru's files.
- Unverified this session, kept from the helpers (say so in the hand-back): Tsinghua living CNY 40,000 (no official figure; old value reformatted); NUS living = official parts + midpoint of the hostel range; Melbourne fee = 2027 Master's rate × 5 (BSc rate unreadable); MQA eSISRAF not checked on any row (browser-only); Northeastern Application requirements lists only letters (Common App essay not read).
- Hand-back for the backlog (outside T7's files): Monash's Course is the Monash Malaysia title (Clayton = BEng (Hons), Robotics & Mechatronics specialisation); CMU Warnings says "clashes with his #1 priority" (a note about the student).
- STATUS.md Now box + Notion mirror: skipped, because only the last session of a stage updates them (plan rule) and T7 isn't finished.

## Next steps
1. Ask Evan: "Write the T7 changes into toru's files?" (summary in `.tmp/t7/dryrun_review.md`).
2. On yes: back up `data/students/toru/{master_list.csv,research_notes.md,score_log.jsonl}` to `.tmp/t7/backup/`.
3. `py -I -X utf8 tools/apply_backfill.py --student toru --fragments .tmp/toru/backfill_t7 --overwrite`
4. `py -I -X utf8 .tmp/t7/recompute.py` (real CSV; appends 2 score_log lines). Expect 15 changes, as in `.tmp/t7/preview/2_recompute.txt`.
5. `py -I -X utf8 .tmp/t7/extract15.py` then `check_master_list.py --file .tmp/t7/sample15.csv` = 0 findings. The T6 PDF check needs the sample CSV, which is T8's file, so build on a redacted copy as `rehearse.py` does.
6. Tick T7 in the plan's Progress table, with a note for T8. Offer the commit: `tools/check_master_list.py`, `tests/test_list_checks.py`, `workflows/countries/uk.md`, `plans/list_pdf_plan.md`, `plans/build-log.md`, `decisions/log.md`, this note.

## Read first
- [plans/list_pdf_plan.md](../list_pdf_plan.md): T7 row, "Done when", Progress table.
- [business/additionals.md](../../business/additionals.md) "Rules for every step session": back up first, dry run first.

## Gotchas
- `.tmp/toru/backfill/` (the default) holds 10 OLD fragments. Always pass `--fragments .tmp/toru/backfill_t7`.
- Run tests without `-I` (it hides the project folder from Python).
- `apply_backfill.py` refuses the whole batch if one cell fails.
- QS: plain fetch gets 403. In Chrome, `fetch('/rankings/endpoint?nid=<drupalSettings.qs_rankings_rest_api.nid>&page=0&items_per_page=500')` on the ranking page.
