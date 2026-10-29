# Plan: the student list becomes a PDF, with checked facts (before 10 Nov 2026)

*Written 2026-10-29 for Evan and for the Claude sessions that run it. Replaces backlog steps 2b and
2c in `business/additionals.md` (R27, R28, R29, R30 part a, R32, then R23, R25, R31).*

**Goal:** a paying student on 10 Nov gets a tidy portrait PDF of their universities. Every fact is
a plain number or a fixed wording from the official page, dated. Every judgment label is explained
on the same page it appears. Nothing hedged or chatty gets past the checks.

## Decisions this plan builds on (don't re-ask)

From `decisions/log.md` (2026-10-28 and 2026-10-29) and `plans/discussions.md`:

1. **The PDF replaces the spreadsheet download.** Portrait. In order:
   1. Student profile (the details that used to repeat in every row, plus the date the list was prepared).
   2. Summary table (about 8 columns).
   3. Key explaining the judgment labels.
   4. One card per university.
   5. Glossary at the back.
2. **`master_list.csv` stays the internal working file.** Before 10 Nov no column is deleted from
   it. The PDF simply doesn't show List status, Tier, Student grades (shown once in the profile),
   Notes, Student life or Money to show (visa). Deleting them from the file waits until after 10 Nov.
   *(Claude's default, 2026-10-29: the 13 scripts that read the file keep working.)*
3. **Two new columns**, added at the end of the file:
   - `Application requirements`: a fixed vocabulary, joined with " · ": `Personal statement`,
     `Essay`, `N supplemental essays`, `N recommendation letters`, `Interview`,
     `Test: <name>`, `Portfolio`, `Audition`. Or the fixed value `Not published`.
   - `Checked on`: the date (YYYY-MM-DD) the row's facts were read on the official page. The PDF
     prints Info source as "Official page, checked on 29 Oct 2026".
4. **Numbers only.** These cells hold a currency code and a number, nothing else:
   - Money cells look like `GBP 46,872`: Annual tuition, Total tuition, Est. living/yr.
   - Rank cells hold a bare number (`8`, `=12`, `601-650`) or `Not ranked`. The ranking's name and
     year go once in the PDF column header, from a constant in `tools/shortlist_schema.py`.
     *(Default: QS World University Rankings and QS by Subject, current edition.)*
   - Calculations and notes go to `research_notes.md`.
5. **Fixed wordings:**
   - A missing deadline is `Not published`. The old `Not published — check portal` stays accepted
     so old lists still pass.
   - The recognition flag is `Recognition risk: not found on <body> list`.
   - "Urban+Rural both ticked" leaves Warnings and becomes a Stage 1 `_needs_review` item.
6. **Cost breakdown** on every university card, made by the script, not the AI:
   - Total tuition, plus living × years, in the local currency.
   - Then the exchange rate and its date.
   - Then the RM total, which must equal `Approx total (MYR)`.
7. **Judgment labels** get one definition each, starting "Our label, not the university's:" plus
   the rule in one line: Desirability, Admission likelihood (Reach/Match/Safety, "not a promise of
   admission"), Grades vs entry bar. Tier is not shown, so it needs no entry.
8. **Rows with List status `Rejected` are left out of the PDF.**

## Tasks

| ID | Goal | Who | Needs | Touches | Size |
|---|---|---|---|---|---|
| T1 | Form reader: "Forecast Grades" read correctly (R27); Urban+Rural → `_needs_review` | Claude | none | `tools/ingest_form_csv.py` | S |
| T2 | Glossary: advice lines rewritten (R30a); judgment-label definitions added (R32) | Claude | none | `tools/apply_glossary.py` | M |
| T3 | Column contract: new columns, number formats, fixed wordings (R29) | Claude | none | `tools/shortlist_schema.py`, `tools/merge_candidates.py`, `tools/sync_shortlist.py` | M |
| T4 | Checks: hedge/advice/chatter check (R28), numbers-only check, requirements vocabulary | Claude | T3 | `tools/check_master_list.py`, `tools/apply_backfill.py`, new `tests/test_list_checks.py` | M |
| T5 | Research instructions: helpers write the new fields and formats | Claude | T3 | `.claude/agents/row-filler.md`, `workflows/03_discover_longlist.md`, `workflows/03b_candidate_schema.md` | M |
| T6 | The PDF builder, tested on the public sample | Claude | T2, T3 | new `tools/build_list_pdf.py`, new `tools/templates/list_pdf.html` (+ `.css`), new `business/sales/sample_pack/sample_profile.json` | L |
| E1 | Evan reads the sample PDF and says what to change | **Evan** | T6 | none | — |
| T7 | Re-check the sample's facts on official pages (R23, R25, R31) in the source list | Claude | T4, T5, E1 | the source student's `data/students/<slug>/` files, `workflows/countries/uk.md` | M |
| T8 | Rebuild the sample pack (now a PDF list) and the demo website's download | Claude | T7 | `business/sales/sample_pack/`, `prototype/data.js`, `prototype/_build/` | M |
| T9 | Docs and backlog brought in line | Claude | T8 | `README.md`, `workflows/00_overview.md`, `business/sales/sample_pack/README.md`, `business/additionals.md`, `CLAUDE.md` | S |

Size key: S under 20k tokens, M 20–60k, L 60–100k.

## Run order

```
STAGE 1 (parallel) → T1, T2, T3            three sessions Evan opens side by side
STAGE 2 (parallel) → T4, T5, T6            three sessions          (needs T3; T6 also T2)
STAGE 3            → E1                     Evan, 10 minutes        (needs T6)
STAGE 4            → T7, then T8            one session each        (needs T4, T5, E1)
STAGE 5            → T9                     one short session       (needs T8)
```

**Target dates:** Stage 1 by 31 Oct, Stage 2 by 3 Nov, E1 by 4 Nov, Stage 4 by 7 Nov, T9 by 8 Nov.
That leaves 9 Nov spare.

**Rules for parallel sessions:**
- Each session only writes the files in its own "Touches" column.
- Commit one session at a time: `git add <your files>`, then `git commit`. Never `git add -A`.
  Another session may have staged files.
- `decisions/log.md` and `plans/build-log.md`: append only, never rewrite. Re-read the file just
  before appending.
- The STATUS.md Now box and the Notion mirror: only the **last session of each stage** updates
  them. A session that isn't last skips the Notion mirror and says why.

## Progress

Each session ticks its own row when it's done (re-read this file just before editing), in the same
commit as its work.

| Task | Done | Commit | Note for the next stage |
|---|---|---|---|
| T1 | | | |
| T2 | | | |
| T3 | | | |
| T4 | | | |
| T5 | | | |
| T6 | | | |
| E1 | | | |
| T7 | | | |
| T8 | | | |
| T9 | | | |

## Done when (checks anyone can run)

- **T1:**
  - The form reader turns the live option "Forecast Grades" into `predicted`. Proved by a
    one-line Python call in the session.
  - `python tools/fetch_form_questions.py --check` is all "ok".
  - The old profiles with a "Forecast" raw answer stored as `expected` are listed for Evan by
    count. Nothing is changed without his yes.
- **T2:**
  - `grep -nE "Avoid it if|so check what|check its register|register and sit" tools/apply_glossary.py`
    finds nothing.
  - The three judgment-label definitions exist and start "Our label, not the university's:".
  - `python tools/build_glossary_sheet.py --file business/sales/sample_pack/sample_master_list.csv --out .tmp/glossary_test.csv` runs.
- **T3:**
  - `python tools/shortlist_schema.py --contract` shows:
    - the two new columns;
    - `Not published` as a deadline value, with the old one still accepted;
    - the new recognition wording;
    - the number formats.
  - `sync_shortlist.py` on a copy of the sample list in `.tmp/` still works on an old-format file
    (the new columns come out blank).
- **T4:**
  - `python -m unittest tests.test_list_checks -v` passes. Its cases cover:
    - a hedge word on an "Official page" row (fail);
    - the same on a "Not verified" row (warning);
    - `~RM` (allowed);
    - text in a money cell (fail);
    - an unknown requirements word (fail).
  - `check_master_list.py` on the current sample list now **fails** with hedge findings. That's
    expected; don't loosen the check.
- **T5:** `grep -rn "check portal" .claude/agents workflows` finds only dated history notes. The
  row-filler sheet names the two new fields, the number formats and the vocabulary.
- **T6:**
  - The command below makes a portrait PDF with the five parts in order:
    `.venv/Scripts/python.exe tools/build_list_pdf.py --file business/sales/sample_pack/sample_master_list.csv --profile business/sales/sample_pack/sample_profile.json --out .tmp/sample_list.pdf`
  - Its text, read with `pypdf`, contains none of: "List status", "Tier", "Notes", "Student life",
    "Money to show".
  - Every card's RM total equals its row's `Approx total (MYR)`.
- **E1:** Evan's changes are written in this plan's Progress table, row E1.
- **T7:**
  - The source list's 15 sample rows pass `check_master_list.py` with the new checks.
  - Every changed cell was read on the official page in this session, and written through
    `apply_backfill.py --overwrite`, dry run first.
- **T8:**
  - `sample_list.pdf` is in `business/sales/sample_pack/`.
  - The demo website's download button opens it.
  - The sample pack's privacy scan is clean.
  - `node prototype/_build/smoke.js` passes.
- **T9:**
  - Steps 2b and 2c in `business/additionals.md` point here and are marked done.
  - The "After 10 Nov" list below is in the backlog.
  - The build log has an entry.

## Prompts (paste one into a fresh session)

Every prompt starts the same way, so a fresh session needs nothing from the chat that made this plan.

### T1
```
Read plans/list_pdf_plan.md ("Decisions" and the T1 rows) and business/additionals.md entries R27
and R29. Do task T1 only. Write only tools/ingest_form_csv.py. R27: the live intake form's grade-type
option is "Forecast Grades"; map it to `predicted`, not `expected`. R29 part: stop the "Urban+Rural
both ticked" note reaching Warnings by making it a Stage 1 `_needs_review` item in the ingest
(T3 removes the stamp from shortlist_schema.py; don't edit that file). Add a dated note at the top
of the file like the others. Verify with the T1 "Done when" checks. Report to Evan, who is
non-technical, in plain English: what changed, and how many old profiles look affected (counts
only, no names). Then tick T1 in the plan's Progress table and offer the commit.
```

### T2
```
Read plans/list_pdf_plan.md ("Decisions" items 7 and the T2 rows) and business/additionals.md
entries R30 and R32, plus fact_audit/04_spreadsheet_text.md findings #1-11 for the exact lines.
Do task T2 only. Write only tools/apply_glossary.py (it is 75 KB: grep for the lines, don't read
it whole). Part a of R30: rewrite every definition that tells the reader what to do ("Avoid it
if", "check", "make sure", "register and sit") as a plain definition. Leave R30 part b (dated and
money figures) alone; it's after 10 Nov. R32: add definitions for Desirability, Admission
likelihood (Reach/Match/Safety) and Grades vs entry bar, each starting "Our label, not the
university's:" and stating the rule that makes it in one line, taken from tools/shortlist_schema.py
(classify_admission, the entry_margin labels, the score). Safety must say it is not a promise of
admission. Make them available to tools/build_list_pdf.py (T6) as a named constant. Verify with
the T2 "Done when" checks; tick T2 in the plan; offer the commit. Explain to Evan in plain English.
```

### T3
```
Read plans/list_pdf_plan.md ("Decisions" items 3-5 and the T3 rows) and business/additionals.md
entry R29. Do task T3 only. Write only tools/shortlist_schema.py, tools/merge_candidates.py and
tools/sync_shortlist.py. Start with `python tools/shortlist_schema.py --contract`.
1) Add columns "Application requirements" and "Checked on" at the END of SHORTLIST_HEADERS, with
   candidate fields `application_requirements` and `checked_on`. Old lists without them must still
   sync (blank).
2) Define the number formats as constants plus one validator function the checks (T4) and the PDF
   (T6) can import: money = "<ISO currency> <number with commas>"; rank = bare number, "=N",
   "N-M", or "Not ranked"; a RANKING_EDITION constant naming the ranking and year for the PDF header.
3) The requirements vocabulary as a constant (see Decisions item 3) plus "Not published".
4) R29: deadline value "Not published" (keep "Not published — check portal" accepted);
   feasibility flag "Recognition risk: not found on <body> list"; remove the Urban+Rural stamp
   from Warnings (T1 moves it to Stage 1).
Add a dated note at the top of each file you change. Don't delete any existing column (Decisions
item 2). Verify with the T3 "Done when" checks; tick T3 in the plan with a one-line note naming
the new constants for T4/T5/T6; offer the commit. Explain to Evan in plain English.
```

### T4
```
Read plans/list_pdf_plan.md (T4 rows and the T3 note in the Progress table), business/additionals.md
entry R28, and the regex table in fact_audit/08_output_sweep.md. Do task T4 only. Write only
tools/check_master_list.py, tools/apply_backfill.py and a new tests/test_list_checks.py.
Add check_hedges over the fact columns: fail on rows stamped "Official page", warn on "Not
verified"; "~" allowed only as "~RM"; research_notes.md is skipped (internal, Evan's call). Add a
numbers-only check and a requirements-vocabulary check, importing the constants and validator T3
added to tools/shortlist_schema.py (don't redefine them). apply_backfill.py runs the same checks on
what it writes. Old lists will fail: that's intended, don't loosen. Verify with the T4 "Done when"
checks; tick T4; offer the commit. Explain to Evan in plain English.
```

### T5
```
Read plans/list_pdf_plan.md ("Decisions" items 3-5, T5 rows, the T3 note in the Progress table)
and run `python tools/shortlist_schema.py --contract`. Do task T5 only. Write only
.claude/agents/row-filler.md, workflows/03_discover_longlist.md and workflows/03b_candidate_schema.md.
Tell the research helper: fill `application_requirements` from the official admissions page with
the fixed vocabulary only; fill `checked_on` with today's date; money and rank cells are numbers
only (calculations go to research_notes.md); a missing deadline is "Not published"; no hedge words
("likely", "usually", "confirm", "~") in any cell. Replace every instruction that uses
"Not published — check portal". Keep these files terse and technical (they are read by agents).
Verify with the T5 "Done when" check; tick T5; offer the commit. Explain to Evan in plain English.
```

### T6
```
Read plans/list_pdf_plan.md (all "Decisions", T6 rows, the T2 and T3 notes in the Progress table).
Do task T6 only. Write only tools/build_list_pdf.py, tools/templates/list_pdf.html (+ .css) and
business/sales/sample_pack/sample_profile.json. Read prototype/screens/list.js and
prototype/data.js (columnGroups, student) for the layout and grouping to copy, and tools/html_to_pdf.py
for the WeasyPrint engine to reuse (run with .venv/Scripts/python.exe). Use the brainstorming skill
briefly for the visual design, but the five parts and their order are fixed (Decisions item 1).
- Profile: from the student's profile.json (--student <slug>) or --profile <file>; for the sample,
  build sample_profile.json from the anonymised "Arif" in prototype/data.js. Never read real
  students' data for testing.
- Summary table, about 8 columns: University, Course, City + Country, Desirability, Admission
  likelihood, Grades vs entry bar, Approx total (RM), Key deadline; Warnings marked.
- Key under the table: the judgment definitions T2 added.
- One card per university, grouped like the website; cost breakdown table (Decisions item 6);
  "Official page, checked on <date>" or "Not verified"; Course URL as a link.
- Glossary at the back: apply_glossary.present_terms() over the list's text.
- Hidden: see Decisions items 2 and 8. Old-format money cells with extra text: take the first
  number and mark the card "figure needs re-checking" rather than crashing.
Output for a real student: data/students/<slug>/list.pdf (gitignored; never commit it).
Verify with the T6 "Done when" checks. Show Evan the sample PDF path and ask him to read it (E1).
Tick T6; offer the commit (not the PDF in .tmp/).
```

### T7
```
Read plans/list_pdf_plan.md (T7 rows, E1 note) and business/additionals.md entries R23, R25 and
R31, and its "Rules for every step session". Do task T7 only. The sample pack's 15 rows come from
the source student's list (named in business/sales/sample_pack/build_sample_pack.py); facts are
fixed there, never in sample_master_list.csv. For each row, re-read the facts on the official page
(free search first, then tools/firecrawl_search.py), using row-filler helpers in BACKFILL mode for
volume (results to files, reply with path + count only), and fill the new fields
(Application requirements, Checked on) and number-only formats. Apply with
`apply_backfill.py --overwrite`, dry run first, and show Evan the dry run before writing (it
rewrites student files). Fix the uk.md note (R25). Then check_master_list.py must be clean on
those rows. Tick T7; offer the commit (workflow files only; data/ is gitignored).
```

### T8
```
Read plans/list_pdf_plan.md (T8 rows) and business/sales/sample_pack/README.md. Do task T8 only.
Rebuild the sample pack with .venv/Scripts/python.exe business/sales/sample_pack/build_sample_pack.py,
extended to also produce sample_list.pdf through tools/build_list_pdf.py. Point the demo website's
list download (prototype/data.js `files.list`) at sample_list.pdf and regenerate prototype data as
SP1 did (prototype/_build/gen.py). Run the privacy scan and `node prototype/_build/smoke.js`.
Verify with the T8 "Done when" checks; tick T8; offer the commit.
```

### T9
```
Read plans/list_pdf_plan.md (Progress table and "After 10 Nov") and business/additionals.md
"Start here". Do task T9 only. Mark steps 2b and 2c done with a pointer to this plan; add the
"After 10 Nov" items below as backlog entries in the right section, with the index updated. Update
README.md, workflows/00_overview.md and business/sales/sample_pack/README.md wherever they describe
the student's download as a spreadsheet. Add a plan-done banner here. Write the build-log entry,
update the STATUS.md Now box and do the Notion mirror (CLAUDE.md -> Status). Offer the commit.
```

## After 10 Nov (not in this plan; T9 moves these into the backlog)

- Delete List status, Tier, Notes, Student life and Money to show (visa) from `master_list.csv`
  and every script that reads them (List status alone is in 27 files).
- Stop researching Student life, Notes and Money to show in Stage 3. That's fewer tokens per
  university, which also helps the pricing question in `plans/discussions.md`.
- Money to show (visa) goes into the how-to-apply guide (Stage 8).
- Student life is covered by the university report.
- Reports and guides: one "Our assessment (a judgment, not a fact)" box (R34, step 9).
- R30 part b: dated and money figures out of the glossary.
