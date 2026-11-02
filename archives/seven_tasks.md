# Seven tasks before 10 Nov, then one clean-up

Made 2026-11-02 from Evan's order of work. Evan pastes one short prompt per session; this file
holds the detail, so a fresh session needs nothing else. Entry details are in
`plans/additionals.md`. Where this file corrects an entry, this file wins: the entries were checked
against the code on 2026-11-02 and some of their wording is out of date.

## Run order

Run each stage's sessions at the same time if you like. Start a stage only when the stage before
it is finished.

```
STAGE 1 (parallel) -> T1, T2, T3, T4
STAGE 2 (parallel) -> T5 (needs T2), T6 (needs T3)
STAGE 3            -> T7 (needs T1, T6)
STAGE 4            -> MASTER (needs all seven)
```

| ID | Entry | Goal | Writes | Size | Evan needed? |
|---|---|---|---|---|---|
| T1 | R34 | Reports hold sourced facts plus one labelled opinion box | `tools/build_report.py`, `tools/check_report.py`, `workflows/04_university_report.md`, `workflows/quick_university_report.md`, `.claude/agents/report-writer.md`, a new or existing test file for reports | L | Approves the plan |
| T2 | R42 | Every regulated row has a checked accreditation result | `workflows/sources.md`, `workflows/03b_candidate_schema.md`, `.claude/agents/row-filler.md`, `tools/check_master_list.py`, `tests/test_list_checks.py` | L | Approves the plan |
| T3 | R30 (part) | Glossary loses dated and money facts written from memory | `tools/apply_glossary.py` | M | No |
| T4 | R37 | Sales lines stop promising checks that don't exist | `business/sales/positioning.md`, `business/product_report/longlist_report.md` | S | Approves the wording |
| T5 | R50 | One date per deadline cell, and a rule for which round | `.claude/agents/row-filler.md`, `workflows/03b_candidate_schema.md`, `tools/check_master_list.py`, `tests/test_list_checks.py` | S | No |
| T6 | R51 | Monash link fixed; sample list rebuilt with T3's glossary | the source student's `master_list.csv`; `business/sales/sample_pack/`; `prototype/data.js`, `prototype/_build/` if the build changes them | S | No |
| T7 | R52 | Public report and guide samples are clean | the source student's report and guide JSON and outputs; `business/sales/sample_pack/` | L | Only if the guide can't be fixed |

## Shared rules for T1 to T7

1. **Check the start.** If your task has a "Needs", confirm each needed task's hand-back file
   exists and says `Status: done`. If not, stop and tell Evan which one is missing. Run
   `git log -p -- <your files>` too, in case the work is already done.
2. **Stay inside your Writes list.** Anything else you think should change is a new finding, not
   an edit. Other sessions are working in the same folder at the same time.
3. **Do not commit, stage or push.** This replaces the usual "Commit this?" step. MASTER makes
   every commit. Say so instead of offering one.
4. **Do not edit** `plans/additionals.md`, `plans/build-log.md`, `decisions/log.md`, `STATUS.md`,
   `CLAUDE.md`, `README.md`, or anything in Notion. This replaces the usual end-of-session steps.
   All of that goes in your hand-back file, and MASTER writes it.
5. **Past clients are parked** (Evan, 2026-11-02). Never touch any student's files except the
   source student's, and only in T6 and T7, because the public sample is built from them. Copy a
   student file to `.tmp/` before a program rewrites it. Run `apply_backfill.py` as a dry run first.
6. **New problems are wanted.** Anything you notice that is outside your task goes under "New
   findings" in your hand-back, even if small. Don't fix it, and don't drop it.
7. **A test failing in a file you didn't touch** may be another session mid-edit. Don't fix it. Run
   it again before you finish, and if it still fails, record it in your hand-back.
8. Explain things to Evan in plain English: he is a beginner.
9. **Finish by writing `.tmp/inbox/<ID>.md`**, for example `.tmp/inbox/T1.md`. Your task isn't done
   until that file exists. Use exactly this shape, leaving no student's name, grades, income or
   school in it:

```
# <ID> hand-back
Status: done | not done (why)

## Files changed
- path (one per line, every file, including gitignored ones marked "not in git")

## Commit
Subject: plain-English, 72 characters or fewer
- why, 1 to 3 bullets

## Checks run
- command -> result

## Additionals edits
- what MASTER should delete or rewrite in plans/additionals.md for this entry, including any part left open

## Decisions
- one line each, or "none"

## Build log
- Done / Problems or lessons, 2 to 4 lines

## New findings
For each one, or "none":
### <short title>
- Urgent? yes or no, and why
- Tool gap (the system will keep making this mistake) or stale data (old files only)
- What is true: the evidence, with file and line
- Suggested fix
```

## The tasks

### T1: R34, reports

Read R34 in `plans/additionals.md`, and the fact audit findings it names in `fact_audit/`. Plan
first, in plan mode, and wait for Evan's yes. Two report buyers have paid, so new reports must come
out right.

- R33 is finished (`bb562cb`). Don't redo it. `tools/flip_finalists.py` is not yours.
- Line numbers in R34 moved: the headings are now around lines 131 to 179 of `tools/build_report.py`.
- `workflows/quick_university_report.md` uses the same headings, so it is in scope.
- Don't change the source student's report: that is T7.

**Done when:** the renamed headings and the "Our assessment (a judgment, not a fact)" box render;
the report prints its date; `check_report.py` has working `hedges`, `advice` and `chatter` checks
with tests; existing tests pass.

### T2: R42, accreditation

Read R42 in `plans/additionals.md`. Plan first, in plan mode, and wait for Evan's yes.

- Corrections to R42: engineering's routes are already written in
  `workflows/03b_candidate_schema.md` (around lines 170 to 205), so link to them instead of writing
  them twice. `check_master_list.py` does look at `Recognised in Malaysia?`, but only to see that it
  isn't blank. The gap is the rest of R42.
- Evan said no testing in advance: add a field's table rows when a real buyer needs them.
- All old lists already fail the checker, so more failures on them don't matter. Don't change them.
- `tools/ingest_form_csv.py` isn't in your list and doesn't need changing.

**Done when:** the table exists; helpers have the required step; the checker fails a row with
targets and no fixed result, with tests; a sample row passes and a bad one fails. Proving it on the
first real buyer stays open, so say that under "Additionals edits".

### T3: R30, dated and money facts only

Read R30 in `plans/additionals.md` and `fact_audit/04_spreadsheet_text.md`. `tools/apply_glossary.py`
prints into every list PDF, so paying buyers read it.

- In scope: dated and money facts in definitions, such as "Opens 1 October", "Roughly AUD 650-800 a
  year", Graduate Route length; and finding 04 #6, where two lines contradict the sample's own rows.
- Out of scope, stays in R30: the "usually / typically" lines and findings 04 #5 and #10.
- Don't touch `business/sales/sample_pack/`: T6 rebuilds it.

**Done when:** a search of the file finds no dated or money figure left in a definition, each
removal listed in the hand-back; a test list PDF built into `.tmp/` shows the new text.

### T4: R37, sales lines

Read R37 in `plans/additionals.md` and finding numbers 09 #2 to #5 and #14 in
`fact_audit/09_promises_vs_reality.md`. These are Evan's words, so show him each line before and
after, and change nothing until he says yes.

- `longlist_report.md:186` is now true, because of R33. Leave it.
- Still wrong: `positioning.md` around lines 71 and 76 to 77, and `longlist_report.md:304`.
- Don't fix R11's column counts or "spreadsheet" wording. That is a separate entry.

**Done when:** Evan has approved each line and it is in the file.

### T5: R50, one date per deadline cell

Read R50 in `plans/additionals.md`, but follow this instead of its Suggested fix.

- The helper sheet already allows only `YYYY-MM-DD`, `Rolling` or `Not published` in `key_deadline`
  (`row-filler.md` around line 172), so "regular deadline goes first" is out of date. What's
  missing: no rule says which round's date to use, and no check catches two dates.
- The fix: the cell holds the regular round's date only. Early rounds go in `research_notes`. Say so
  in both instruction files, and make `check_master_list.py` fail a cell with more than one date.
- Don't edit student files or `tools/shortlist_schema.py`. If the sample's source rows now fail,
  write that as a new finding.

**Done when:** the rule is in both files and a test shows a two-date cell fails and a one-date cell
passes.

### T6: R51, Monash link

Read R51 in `plans/additionals.md`, and rule 4 of its "Rules for every step session".

- Change `Course URL` through `apply_backfill.py`, dry run first. It isn't part of the row's key, so
  no re-score. Never type into `sample_master_list.csv`.
- Rebuild with `business/sales/sample_pack/build_sample_pack.py`, then the demo. This also brings
  T3's glossary into `sample_list.pdf`.
- The URL is in `prototype/data.js`, so see how `prototype/_build/` makes that file before running it.

**Done when:** the sample and demo show the new link, the builder's privacy scan is clean, and the
page opens to the right course.

### T7: R52, public samples

Read R52 in `plans/additionals.md`, and rule 4 of its "Rules for every step session".

- Report: rewrite the source student's MIT report JSON into T1's new shape, rebuild it with
  `build_report.py`, and pass `check_report.py`. Never edit the report output by hand.
- Guide: fix the sentences R52 names in the guide's JSON, and rebuild. The 1 Nov early deadline has
  passed, so it can't lead. If this needs tool changes from R35, stop and tell Evan: the default is
  to keep the guide off the Linktree until R35 is done.
- Build with `business/sales/sample_pack/build_sample_pack.py`. Update `REPORT_TEXT_REDACTIONS` or
  `APPLY_TEXT_REDACTIONS` there if the text they match has changed; never skip them.
- Update page and section counts in the sample pack `README.md`.

**Done when:** a text search of both PDFs finds none of R52's phrases, the privacy scan is clean,
and Evan is told which PDFs are safe for the Linktree.

## MASTER: clean up, record and commit

Run alone, after T1 to T7. Run it even if a task isn't done: commit only what is finished.

1. **Check nothing else is running.** Use ListAgents. If another session is open on this repo, stop
   and tell Evan.
2. **Read every `.tmp/inbox/T*.md`.** List for Evan any missing or `Status: not done`. Leave that
   task's files out of the commits and tell him which ones.
3. **Check the work against the claims.** For each finished task, run `git diff` on its files and
   confirm it did what its "Done when" says. Run every `python -m unittest` module from `CLAUDE.md`,
   plus any new test file, and `python tools/check_report.py` where T1 says to. Fix nothing yourself
   if it fails: stop and report that task as not done.
4. **Commit, one at a time, in this order,** only the files listed, never `git add -A` or `git add .`.
   Run `git add <files>`, then `git commit` as a second command. Check no `.env`, secret, `data/` or
   `notes/` file is staged. Never push.
   - First: the past-clients leftovers (`decisions/log.md`, `plans/additionals.md`,
     `plans/build-log.md`, `plans/seven_tasks.md`), before you edit any of them.
   - One commit each: T1, T3, T4.
   - One commit for T2 + T5, and one for T6 + T7: each pair changes the same files, so they can't be
     split cleanly. Name both entries in the subject.
   - Use each hand-back's Subject and bullets.
5. **Update `plans/additionals.md`,** by exact edits:
   - Do each hand-back's "Additionals edits". Finished entries go, with their lines in the steps.
   - Delete R33, R46 and O12 (all closed, checked 2026-11-02), and the 2b-2d row. Step 9 goes if R34
     is done. Step 11 starts at R45. Remove the mentions of R23: the sample's US rows are correct.
   - Add R53 as in `plans/build-log.md` entry 23, and add it to the parked line under "Closed on
     2026-10-28". Move R47 out of step 12.
   - Fix counts: I3 says 11 students, not five; R21 says 49 cells, not about 40; R17: `Admission
     likelihood` no longer balances it, because the PDF hides that column; 23 non-source US rows.
   - Rewrite R36: the hedge check now covers nearly every column and the PDF hides `Notes`. What's
     left is undated facts in country files (Japan most), the advice line in `singapore.md:134`, and
     default sub-scores (not re-tested).
   - Rewrite R35: the "5%" line isn't in `build_application_prep.py`. It comes from each guide's
     written content, so that fix belongs in `.claude/skills/application-guide/SKILL.md` and
     `workflows/08_application_prep.md`.
   - Add R54: "No real student has gone through the new form and PDF flow." **Urgent, tool gap
     unproven.** No student folder has `list.pdf` or `priority_levels`. Run the first buyer's form
     through as soon as it arrives, not on 10 Nov.
   - Add every "New findings" item as an entry, numbered from R55, in the file's usual format. Then
     list them in a new table under "Start here" headed "New from the seven tasks: not started".
     Move "next number" on. Don't work on them.
6. **Update the main files.** Add one `plans/build-log.md` entry from the hand-backs, and the
   decisions to `decisions/log.md`. Refresh the Now box in `STATUS.md`. Add `data/resources/` to
   `.gitignore` (default from build-log entry 23). Read `CLAUDE.md`, `README.md`,
   `business/README.md` and `workflows/00_overview.md`, and change only what these tasks made untrue,
   such as new checks in the Commands list. Leave `business/launchx/status.md` alone unless Evan says.
7. **Close out.** Move this file to `archives/`, and add it to `archives/README.md`. Commit all of
   step 5 to 7 as one last commit. Delete `.tmp/inbox/` only after that commit exists.
8. **Mirror to Notion** as `CLAUDE.md` says, and end with "Notion updated" or why not.
9. **Report to Evan** in plain English: what was committed (hash and one line each); anything not
   done; then every new finding, with urgent ones first, your recommended order, and a default for
   each. Stop there. Evan decides what happens next.
