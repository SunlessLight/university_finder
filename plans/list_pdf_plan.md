# Plan: the student list becomes a PDF, with checked facts (before 10 Nov 2026)

*Written 2026-10-29 for Evan and for the Claude sessions that run it. Replaces backlog steps 2b, 2c
and 2d in `business/additionals.md` (R27, R28, R29, R30 part a, R32, R39, R40, R38, then R23, R25,
R31). Amended 2026-10-29 (Evan: "all new changes now, no waiting"): T2b, T3b, T10, T11, T12 added.
Amended 2026-10-30 after E1 (Evan read the sample): Decisions items 7, 11, 12; T3c and T5b added.*

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
   the rule in one line: Desirability, Grades vs entry bar. The key also explains Admit rate (item
   9). Admission likelihood and Tier are not shown, so they need no entry.
   *Amended 2026-10-30 (E1, Evan): one short sentence each, least effort to read. Each still says
   whose it is ("Our score", "Our label", "The university's own figure"), and Desirability and
   Admit rate still say they are not your chance of getting in.*
8. **Rows with List status `Rejected` are left out of the PDF.**
9. **Admit rate replaces Admission likelihood in everything the student sees** (Evan, 2026-10-29,
   R40). We can't judge whether a student gets in; a university's published admit rate is a fact.
   - A third new column, `Admit rate`, after `Checked on`. Fixed shape:
     `<N.N>% of <all|international> applicants <admitted|offered a place>, <YYYY-YY>`, e.g.
     `4.5% of all applicants admitted, 2024-25`. Or `Not published`.
   - Source: the university's own figures. US: Common Data Set section C1. Other countries: the
     source T11 names in each country file, else `Not published`.
   - `Admission likelihood` stays in `master_list.csv` (item 2) and still drives the balanced
     Reach/Match/Safety shortlist, internally only. The PDF and its key don't show it.
10. **Score weights come from the tick levels** (R39): Must have 3 points, Important 2, Nice to
    have 1, Doesn't matter 0; a topic's weight = its points ÷ total points. Equal ticks, equal weight.
11. **Every link a student needs is on the card** (Evan, 2026-10-30, E1). Each card ends with
    "Useful links":
    - the Course URL;
    - two new columns at the end of the file, `Apply link` (the page where this course is applied
      for: the university's portal, or Common App / UCAS when that is the route) and
      `Scholarship link` (the official page of the scholarship named in `Scholarship & portal`),
      each an `https://` URL or `Not published` (T3c, T5b);
    - the official site of each shared system the card mentions (Common App, CSS Profile, IDOC,
      IELTS…), from `OFFICIAL_LINKS` in `tools/apply_glossary.py`. A system named only as "not X"
      gets no link.
12. **No notes to ourselves on the student's page** (Evan, 2026-10-30, E1). Problems with the data
    (a money cell with extra text, parts that don't add up) stop the build and are listed on
    screen; `--draft` builds a review copy with "Draft, not for sending" in the footer. A list
    goes to a student only from a build without `--draft`. Replaces the T6 prompt's "figure needs
    re-checking" mark.

## Tasks

| ID | Goal | Who | Needs | Touches | Size |
|---|---|---|---|---|---|
| T1 | Form reader: "Forecast Grades" read correctly (R27); Urban+Rural → `_needs_review` | Claude | none | `tools/ingest_form_csv.py` | S |
| T2 | Glossary: advice lines rewritten (R30a); judgment-label definitions added (R32) | Claude | none | `tools/apply_glossary.py` | M |
| T3 | Column contract: new columns, number formats, fixed wordings (R29) | Claude | none | `tools/shortlist_schema.py`, `tools/merge_candidates.py`, `tools/sync_shortlist.py` | M |
| T2b | Glossary key: Admission likelihood out, Admit rate in (R40) | Claude | T2 | `tools/apply_glossary.py` | S |
| T3b | Column `Admit rate` and its fixed shape (R40) | Claude | T3 committed | `tools/shortlist_schema.py`, `tools/merge_candidates.py`, `tools/sync_shortlist.py` | S |
| T10 | Score weights from tick points (R39) | Claude | none | `tools/ingest_form_csv.py`, `tools/derive_weights.py`, `.claude/skills/scoring-weights/SKILL.md` | S |
| T11 | Where each country publishes admit rates (R40 research) | Claude | none | `workflows/countries/*.md` (one "Admit rate source" line each) | M |
| T12 | Seven old profiles' grade type (R38), on Evan's yes | Claude + **Evan** | none | 7 students' `profile.json` (gitignored) | S |
| T4 | Checks: hedge/advice/chatter check (R28), numbers-only check, requirements vocabulary | Claude | T3, T3b | `tools/check_master_list.py`, `tools/apply_backfill.py`, new `tests/test_list_checks.py` | M |
| T5 | Research instructions: helpers write the new fields and formats | Claude | T3, T3b | `.claude/agents/row-filler.md`, `workflows/03_discover_longlist.md`, `workflows/03b_candidate_schema.md` | M |
| T6 | The PDF builder, tested on the public sample | Claude | T2, T2b, T3, T3b | new `tools/build_list_pdf.py`, new `tools/templates/list_pdf.html` (+ `.css`), new `business/sales/sample_pack/sample_profile.json` | L |
| E1 | Evan reads the sample PDF and says what to change | **Evan** | T6 | none | — |
| T3c | Columns `Apply link` and `Scholarship link` (Decisions item 11) | Claude | E1 | `tools/shortlist_schema.py`, `tools/merge_candidates.py`, `tools/sync_shortlist.py` | S |
| T5b | Research instructions: helpers write the two link fields | Claude | E1 | `.claude/agents/row-filler.md`, `workflows/03b_candidate_schema.md` | S |
| T7 | Re-check the sample's facts on official pages (R23, R25, R31) in the source list | Claude | T4, T5, T11, E1, T3c, T5b | the source student's `data/students/<slug>/` files, `workflows/countries/uk.md` | M |
| T8 | Rebuild the sample pack (now a PDF list) and the demo website's download | Claude | T7 | `business/sales/sample_pack/`, `prototype/data.js`, `prototype/_build/` | M |
| T9 | Docs and backlog brought in line | Claude | T8 | `README.md`, `workflows/00_overview.md`, `business/sales/sample_pack/README.md`, `business/additionals.md`, `CLAUDE.md` | S |

Size key: S under 20k tokens, M 20–60k, L 60–100k.

## Run order

```
STAGE 1  (parallel) → T1, T2, T3           done 2026-10-29 (T3 still to commit)
STAGE 1b (parallel) → T3b, T10, T11, T12    T3b needs T3 committed; the others need nothing
STAGE 2  (parallel) → T4, T5, T6            three sessions          (needs T3b; T6 also T2b)
STAGE 3             → E1                    Evan, 10 minutes        (needs T6)
STAGE 3b (parallel) → T3c, T5b              two short sessions      (need E1; field names fixed in item 11)
STAGE 4             → T7, then T8           one session each        (needs T4, T5, T11, E1, T3c, T5b)
STAGE 5             → T9                    one short session       (needs T8)
```

T10, T11 and T12 touch nothing Stage 2 touches, so they can keep running while Stage 2 starts.
T2b was done in the T2 session.

**Target dates:** Stage 1 by 31 Oct, Stage 2 by 3 Nov, E1 by 4 Nov, Stage 3b by 5 Nov, Stage 4 by 7 Nov, T9 by 8 Nov.
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
| T1 | ✅ 2026-10-29 | (this commit) | Ingest now flags Urban+Rural as `_needs_review`; T3 can drop the `feasibility_flags` stamp. Old profiles not changed (await Evan): 5 of 20 `expected` answered "Forecast" (should be `predicted`), 2 answered "Actual", 13 have no grade-type answer on file (older form, genuinely self-predicted); 10 of 27 have Urban+Rural both ticked. |
| T2 | ✅ 2026-10-29 | (this commit) | T6: import `JUDGMENT_LABELS` from `tools/apply_glossary.py` (same shape as `GLOSSARY`: term → `{"definition"}`; keys are the column names Desirability, Admission likelihood, Grades vs entry bar). Show all three under the table; it is NOT in `GLOSSARY` (so not in the Glossary tab yet), because "Safety"/"Match" would auto-link ordinary words. Nine advice lines rewritten (04 #1–4, #9). Not done, no task owns them: 04 #5 recognition promises, #6 ISAFA vs the Stanford row, #10 opinion clauses; UAC "usually … instead" is a hedge, so R30 part b. |
| T3 | ✅ 2026-10-29 | (this commit) | Import from `tools/shortlist_schema.py`: `cell_format_problem(column, value)` (None = fine; judges `FORMATTED_COLUMNS` = `MONEY_COLUMNS`, `RANK_COLUMNS`, Application requirements, Checked on), `MONEY_FORMAT`/`RANK_FORMAT`/`ISO_CURRENCIES`, `RANKING_EDITION` (dict: column → edition name, for T6 headers), `APPLICATION_REQUIREMENTS_VOCAB` + `_SEPARATOR`, `LEGACY_SENTINELS` (T5: never write these). **T4:** old 35-column lists now FAIL the schema check, and `apply_backfill.py` refuses them; call `upgrade_header(header, rows)` on load (pads `ADDED_COLUMNS` blank; sync already does this in place). `merge_candidates.py` now requires the two fields and checks formats, so no Stage 3 run until T5 lands. Not owned by any task: `flip_finalists.py` refuses old lists too; `derive_weights.py` docstring still mentions the Urban+Rural flag. |
| T2b | ✅ 2026-10-29 | (with the plan amendment) | `JUDGMENT_LABELS` keys are now Desirability, Grades vs entry bar, Admit rate (T6 shows all of them in the key). Admission likelihood's definition is gone (not shown, Decisions item 9). |
| T3b | ✅ 2026-10-29 | (this commit) | `Admit rate` is column 38 (last), candidate field `admit_rate`, in `ADDED_COLUMNS`, `REQUIRED_CANDIDATE_FIELDS` and `FORMATTED_COLUMNS`; `SENTINEL_VALUES["Admit rate"] = ["Not published"]`; shape string `ADMIT_RATE_FORMAT` (one decimal required, so `5%` fails; ≤100%; cycle years consecutive). **T4:** 37-column lists (T3 layout) now fail the header check too; `upgrade_header()` pads them. **T5:** `merge_candidates.py` requires `admit_rate` now. **T6:** print the cell as is; blank on old rows = not researched yet. Admission likelihood still computed and written (Decisions item 2). Not owned by any task: "35 columns" comments in `check_master_list.py`/`apply_backfill.py` and `prototype/_build/smoke.js` line 333 (T8 rebuilds the sample). |
| T10 | ✅ 2026-10-29 | (this commit) | Ingest writes `preferences.priority_levels` (token → 3/2/1/0, tick form only; numeric-slider or dropdown answers → None). `derive_weights.py` uses it when present (points ÷ total; cap 0.5, then the `course_match` floor funded proportionally, so equal ticks stay equal); a blank tick is refused. "Doesn't matter" now weighs 0 (was 5% at rank 8). Checks run on `.tmp/t10/` fakes: all Must have 0.125; 2 MH + 6 Imp 0.1667/0.1111; ranking-only identical to HEAD. No student file touched; old profiles have no `priority_levels`, so they stay on the rank formula until re-read from the form export (R39 "Old lists"). Not owned by any task: `workflows/01_intake.md` (~lines 221–233, 420) and the `init_student.py` template still describe `priorities` only (T9). |
| T11 | ✅ 2026-10-30 | (this commit) | Each `workflows/countries/*.md` has `## Admit rate source` just above "Known-good sources". Publishing: **USA** (each university's Common Data Set C1: all applicants, admitted), **UK** (Oxford and Cambridge only; Cambridge Table 3.2 is international, offered), **Japan** (each university's 入試結果, 私費外国人留学生 track: international, admitted). None published: Malaysia, Hong Kong (non-JUPAS), Taiwan, Germany, Australia (dept report is domestic only), Singapore, China (China checked by Evan by eye). **T5:** everything outside those three = `Not published`, and in the UK every university except Oxford/Cambridge. **T7:** UCAS provider data counts acceptances, not offers; never derive a rate from it. |
| T12 | ✅ 2026-10-30 | (this commit) | On Evan's yes, 7 `profile.json` set by hand: 5 `predicted`, 2 `actual` (matched by email to the form answer; backups in `.tmp/t12_backup/`). No list re-synced, so those lists keep "Grades self-predicted" until one is re-synced for re-sending. 13 `expected` remain: no grade-type answer on file, genuinely self-guessed. |
| T4 | ✅ 2026-10-30 | (this commit) | `check_master_list.py` adds `hedges` (fact-audit 08 regex table over `HEDGE_COLUMNS` = every researched column; FAIL on any row not `Not verified`, warning on `Not verified`; `~` only as `~RM`; a whole-cell sentinel is exempt, so the legacy `Not published — check portal` passes), `numbers` and `requirements` (both `cell_format_problem()`). `run()` now returns `(results, warnings)`; warnings never change the exit code. An old list fails `schema` but its cells are now checked on an `upgrade_header()` copy. `apply_backfill.py` pads old headers on load and refuses a bad format, a legacy sentinel or a hedge (warns on `Not verified` rows); `validate()` returns 4 values. 17 tests pass. Sample list: FAIL, 196 findings (75 hedges, 75 numbers, 45 blank new columns). **T7:** two borderline hits to reword, not loosen: Rose-Hulman "Expects 4 yrs math" → "Requires", Melbourne "about 5 years" → "5 years". **T6:** a PDF built from the sample will carry these until T7. |
| T5 | ✅ 2026-10-30 | (this commit) | Formats live once, in `row-filler.md` → "Fixed-format cells" (both modes read it; 03b and 03 point there): money, ranks, requirements vocabulary, `checked_on` = today, `admit_rate` only from the country file's `## Admit rate source`, deadline sentinel `Not published`, no `likely`/`usually`/`confirm`/`~`; override = balancing only, with reason. 03b example fragment passes `cell_format_problem()`. "35 columns" → 38 in current text (dated history notes kept). On Evan's yes, the same fix in `workflows/countries/australia.md`, `china.md`, `japan.md` (outside T5's fence); the "check portal" grep now finds only the dated note in 03. |
| T6 | ✅ 2026-10-30 | (this commit) | `tools/build_list_pdf.py` (`--student <slug>` → their `list.pdf`, or `--file/--profile/--out`); look copies `prototype/styles.css`. Checks: 19 portrait pages, five parts in order, no hidden word in the text, 14/14 card RM totals = `Approx total (MYR)`, Rejected row left out. Card total always prints the row's own figure. After E1: a money cell holding more than `<CODE> <number>`, or parts that don't add up, stops the build (problems listed on screen); `--draft` builds a review copy (sample today: 12 problems, all old caveat text, so it builds only with `--draft`). Admit rate prints "—" (+ key line "Not checked yet") when blank. **T7:** Cambridge's deadline (15 Oct 2026) has passed but its Warnings says None; Monash and Melbourne say "Direct / UAC International" (UAC is the NSW centre; Victoria isn't UAC), so their cards link UAC. **T8:** same command without `--draft`, `--out business/sales/sample_pack/sample_list.pdf`. Not owned by any task: the exchange-rate line prints `FX_AS_OF` for every currency, but the TWD rate is dated 2026-09-23. |
| E1 | ✅ 2026-10-30 | (with T6) | Evan's six points, and what happened: (1) Admit rate "—": sample data not researched yet, T7 fills it; no PDF change. (2, 3) Label key too wordy: `JUDGMENT_LABELS` and the RM line cut to one short sentence each (Decisions item 7 amended; T2's "starts Our label, not the university's" check retired). (4) Every link on the card: "Useful links" block now (Course URL + `OFFICIAL_LINKS` in `apply_glossary.py`, 12 systems, each opened 2026-10-30); per-university Apply and Scholarship links = new T3c + T5b (Decisions item 11), filled for the sample in T7; the PDF already prints them when present. (5) Application requirements missing: they're in the plan and the card; the sample's column is blank until T7. (6) No AI notes to self: the "figure needs re-checking" mark came from the T6 prompt, now replaced by Decisions item 12 (build stops; `--draft` for review). Cell text like "MQA: verify", "Count yours" is R31, caught by T4's check, fixed in T7. |
| T3c | | | |
| T5b | | | |
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
    *(Retired by E1, 2026-10-30: shorter wording, Decisions item 7.)*
  - `python tools/build_glossary_sheet.py --file business/sales/sample_pack/sample_master_list.csv --out .tmp/glossary_test.csv` runs.
- **T3:**
  - `python tools/shortlist_schema.py --contract` shows:
    - the two new columns;
    - `Not published` as a deadline value, with the old one still accepted;
    - the new recognition wording;
    - the number formats.
  - `sync_shortlist.py` on a copy of the sample list in `.tmp/` still works on an old-format file
    (the new columns come out blank).
- **T2b:** `JUDGMENT_LABELS` has Desirability, Grades vs entry bar and Admit rate; the Admit rate
  line says it is not your own chance of getting in.
- **T3b:**
  - `--contract` shows `Admit rate` as the last column, with its shape.
  - `cell_format_problem("Admit rate", "4.5% of all applicants admitted, 2024-25")` is None;
    `"~5%"` and `"very selective"` are problems; `"Not published"` is fine.
  - An old list on a `.tmp/` copy still syncs, `Admit rate` blank.
- **T10:**
  - All eight "Must have" → every weight 0.125.
  - 2 Must have + 6 Important → 0.1667 each and 0.1111 each.
  - An older profile with a ranking only gives the same weights as before (`--dry-run`).
- **T11:** every file in `workflows/countries/` has an "Admit rate source" line naming an official
  page or publication opened in this session, or "None published (checked <date>)".
- **T12:** Evan said yes in the session first; the 7 profiles' `grade_status` match the form answer.
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
    "Money to show", "Admission likelihood".
  - Every card's RM total equals its row's `Approx total (MYR)`.
  - *(Added by E1)* Without `--draft`, a list with a messy money cell is not built (exit 1, the
    cells listed); with `--draft` it is, and the text holds no "re-checking" and says "Draft, not
    for sending". The MIT card ("not Common App") has no Common App link.
- **E1:** Evan's changes are written in this plan's Progress table, row E1.
- **T3c:**
  - `--contract` shows `Apply link` and `Scholarship link` as the last two columns.
  - `cell_format_problem()` passes `https://www.ucas.com/` and `Not published`; fails
    `ucas.com`, `see portal` and a URL with a space.
  - An old list on a `.tmp/` copy still syncs, the two columns blank.
- **T5b:** the row-filler sheet's "Fixed-format cells" names `apply_link` and `scholarship_link`;
  the 03b example fragment has both and passes `cell_format_problem()`.
- **T7:**
  - The source list's 15 sample rows pass `check_master_list.py` with the new checks.
  - Every changed cell was read on the official page in this session, and written through
    `apply_backfill.py --overwrite`, dry run first.
  - The T6 command builds the sample **without** `--draft` (no money problems left).
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

### T3b
```
Read plans/list_pdf_plan.md ("Decisions" items 2 and 9, the T3b rows, the T3 note in the Progress
table) and business/additionals.md entry R40. Do task T3b only. Write only tools/shortlist_schema.py,
tools/merge_candidates.py and tools/sync_shortlist.py. Run `git log -1 -- tools/shortlist_schema.py`
first: T3 must be committed; if not, stop and tell Evan. Add column "Admit rate" at the END of
SHORTLIST_HEADERS (after "Checked on"), candidate field `admit_rate`, in ADDED_COLUMNS so
upgrade_header() pads old lists blank. Add its shape to FORMATTED_COLUMNS so cell_format_problem()
judges it: "<N.N>% of <all|international> applicants <admitted|offered a place>, <YYYY-YY>" or
"Not published". Don't change classify_admission() or remove Admission likelihood (item 2; it still
drives the balanced shortlist). Add a dated note at the top of each file. Verify with the T3b
"Done when" checks; tick T3b with a one-line note for T4/T5/T6; offer the commit. Explain to Evan
in plain English.
```

### T10
```
Read plans/list_pdf_plan.md ("Decisions" item 10, the T10 rows) and business/additionals.md entry
R39, then .claude/skills/scoring-weights/SKILL.md and the docstring of tools/derive_weights.py.
Do task T10 only. Write only tools/ingest_form_csv.py, tools/derive_weights.py and that skill.
Ingest keeps the tick levels as preferences.priority_levels (token -> 3/2/1/0) beside the existing
`priorities` order. derive_weights.py: when priority_levels exists, weight = points / total
(all equal or all 0 -> equal weights); keep the course_match floor; scholarship_required sets
scholarship to 3; profiles with only `priorities` keep today's rank formula. Update the rationale
text, the skill, and the docstring's stale Urban+Rural flag mention. Don't re-ingest or touch any
student file. Add a dated note at the top of each file. Verify with the T10 "Done when" checks (use
.tmp/ copies of made-up preferences, never a real student's); tick T10; offer the commit. Explain
to Evan in plain English.
```

### T11
```
Read plans/list_pdf_plan.md ("Decisions" item 9, the T11 rows) and business/additionals.md entry
R40. Do task T11 only. Write only workflows/countries/*.md. For each country file, find where that
country's universities officially publish an admit or offer rate (e.g. US: Common Data Set C1;
UK: Oxford and Cambridge admissions statistics, UCAS data if per university), using free search
first, then tools/firecrawl_search.py. Open each source. Add one line under a heading "Admit rate
source": the publication, what it counts (all or international applicants; admitted or offered),
and the checked date; or "None published (checked <date>)". Source pointers only: no admit-rate
figures in these files. Keep the files terse (agents read them). Verify with the T11 "Done when"
check; tick T11; offer the commit. Report to Evan in plain English: which countries publish one.
```

### T12
```
Read plans/list_pdf_plan.md (T12 rows) and business/additionals.md entry R38 and its "Rules for
every step session". Do task T12 only. List the 7 profiles for Evan by slug (in the chat only),
with each one's form answer and the grade_status it would get. Wait for his yes. Then copy each
profile.json to .tmp/ and set grade_status by hand (no --force re-ingest). Don't re-sync any list.
Delete R38 from business/additionals.md and its step line; tick T12; offer the commit
(additionals.md and the plan only; data/ is gitignored). Explain to Evan in plain English.
```

### T4
```
Read plans/list_pdf_plan.md (T4 rows and the T3 and T3b notes in the Progress table), business/additionals.md
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
Read plans/list_pdf_plan.md ("Decisions" items 3-5 and 9, T5 rows, the T3 and T3b notes in the
Progress table) and run `python tools/shortlist_schema.py --contract`. Do task T5 only. Write only
.claude/agents/row-filler.md, workflows/03_discover_longlist.md and workflows/03b_candidate_schema.md.
Tell the research helper: fill `application_requirements` from the official admissions page with
the fixed vocabulary only; fill `checked_on` with today's date; fill `admit_rate` in its fixed shape
from the source the country file's "Admit rate source" line names (T11), else "Not published";
the admission_likelihood override stays for balancing only, with its reason; money and rank cells are numbers
only (calculations go to research_notes.md); a missing deadline is "Not published"; no hedge words
("likely", "usually", "confirm", "~") in any cell. Replace every instruction that uses
"Not published — check portal". Keep these files terse and technical (they are read by agents).
Verify with the T5 "Done when" check; tick T5; offer the commit. Explain to Evan in plain English.
```

### T6
```
Read plans/list_pdf_plan.md (all "Decisions", T6 rows, the T2, T2b, T3 and T3b notes in the Progress table).
Do task T6 only. Write only tools/build_list_pdf.py, tools/templates/list_pdf.html (+ .css) and
business/sales/sample_pack/sample_profile.json. Read prototype/screens/list.js and
prototype/data.js (columnGroups, student) for the layout and grouping to copy, and tools/html_to_pdf.py
for the WeasyPrint engine to reuse (run with .venv/Scripts/python.exe). Use the brainstorming skill
briefly for the visual design, but the five parts and their order are fixed (Decisions item 1).
- Profile: from the student's profile.json (--student <slug>) or --profile <file>; for the sample,
  build sample_profile.json from the anonymised "Arif" in prototype/data.js. Never read real
  students' data for testing.
- Summary table, about 8 columns: University, Course, City + Country, Desirability, Admit rate,
  Grades vs entry bar, Approx total (RM), Key deadline; Warnings marked. Never Admission likelihood.
- Key under the table: every entry of JUDGMENT_LABELS (T2, T2b).
- One card per university, grouped like the website; cost breakdown table (Decisions item 6);
  "Official page, checked on <date>" or "Not verified"; Course URL as a link.
- Glossary at the back: apply_glossary.present_terms() over the list's text.
- Hidden: see Decisions items 2 and 8. Old-format money cells with extra text: take the first
  number and mark the card "figure needs re-checking" rather than crashing.
  *(Superseded by Decisions item 12 after E1: no mark on the card; the build stops, --draft.)*
Output for a real student: data/students/<slug>/list.pdf (gitignored; never commit it).
Verify with the T6 "Done when" checks. Show Evan the sample PDF path and ask him to read it (E1).
Tick T6; offer the commit (not the PDF in .tmp/).
```

### T3c
```
Read plans/list_pdf_plan.md ("Decisions" item 11, the T3c rows, the T3b note in the Progress
table). Do task T3c only. Write only tools/shortlist_schema.py, tools/merge_candidates.py and
tools/sync_shortlist.py, the same way T3b added Admit rate. Add columns "Apply link" then
"Scholarship link" at the END of SHORTLIST_HEADERS (after "Admit rate"), candidate fields
`apply_link` and `scholarship_link`, in ADDED_COLUMNS (upgrade_header() pads old lists blank),
REQUIRED_CANDIDATE_FIELDS and FORMATTED_COLUMNS. Shape: one URL starting https://, no spaces, or
"Not published" (add to SENTINEL_VALUES). Add a dated note at the top of each file. Verify with
the T3c "Done when" checks; tick T3c with a one-line note for T5b/T7; offer the commit. Explain to
Evan in plain English.
```

### T5b
```
Read plans/list_pdf_plan.md ("Decisions" item 11, T5b rows, the T5 note in the Progress table).
Do task T5b only. Write only .claude/agents/row-filler.md and workflows/03b_candidate_schema.md.
In row-filler.md's "Fixed-format cells", add: `apply_link` = the official page where this course
is applied for (the university's own portal page, or https://www.commonapp.org/ /
https://www.ucas.com/ when that is the route); `scholarship_link` = the official page of the
scholarship named in `scholarship_portal`; each one URL opened in this session, or "Not
published". Never an aggregator or a search-results page. Add both to the 03b example fragment.
Keep it terse (read by agents). Verify with the T5b "Done when" check; tick T5b; offer the
commit. Explain to Evan in plain English.
```

### T7
```
Read plans/list_pdf_plan.md (T7 rows, E1 note) and business/additionals.md entries R23, R25 and
R31, and its "Rules for every step session". Do task T7 only. The sample pack's 15 rows come from
the source student's list (named in business/sales/sample_pack/build_sample_pack.py); facts are
fixed there, never in sample_master_list.csv. For each row, re-read the facts on the official page
(free search first, then tools/firecrawl_search.py), using row-filler helpers in BACKFILL mode for
volume (results to files, reply with path + count only), and fill the new fields
(Application requirements, Checked on, Admit rate from the source T11 named, Apply link,
Scholarship link) and number-only formats. Also check the T6 note's two leads (Cambridge's passed
deadline; Monash/Melbourne "UAC International"). Apply with
`apply_backfill.py --overwrite`, dry run first, and show Evan the dry run before writing (it
rewrites student files). Fix the uk.md note (R25). Then check_master_list.py must be clean on
those rows, and the T6 command must build the sample without --draft. Tick T7; offer the commit
(workflow files only; data/ is gitignored).
```

### T8
```
Read plans/list_pdf_plan.md (T8 rows) and business/sales/sample_pack/README.md. Do task T8 only.
Rebuild the sample pack with .venv/Scripts/python.exe business/sales/sample_pack/build_sample_pack.py,
extended to also produce sample_list.pdf through tools/build_list_pdf.py (never --draft). Point the demo website's
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
