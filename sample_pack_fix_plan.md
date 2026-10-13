# Sample pack fix plan — stale FX + stale sample rows

Written 2026-10-12. Source of the findings: `business/additionals.md` → L1, plus a read of the
sample PDF, the sample CSV, the prototype and the poster in the session that wrote this file.

## How to run this file

- **One task per fresh session.** Read "Shared facts" plus your own task. Nothing else in this file.
- **Do not enter plan mode and do not re-plan.** The task is the plan. Execute it.
- **Do not commit, stage or push.** Parallel sessions share one git index. Evan runs `/commit`
  himself: once after Task 5, once after Task 9, and after any of Tasks 10-12 that lands later.
- **Preconditions are checked against the files, not against the tick boxes below.** Each dependent
  task carries its own precondition command.
- **Code blocks are indented to sit under their step.** Dedent them before running, or the heredoc
  terminator and the Python both break. If a long heredoc still dies with `unexpected EOF while
  looking for matching` a quote (seen 2026-10-12 on this machine), save the Python to a file in the
  scratchpad and run the file instead — do not fight the quoting.
- When done: tick your box in "Status", then reply with what changed and the verify output.

### Order

```
Wave 1 (parallel, 3 sessions)   Task 1  source list rows      DONE 2026-10-12, except Rose-Hulman
                                Task 1b Rose-Hulman course fix + 2 unchecked rows
                                                              (slow: web research, 3 subagents)
                                Task 2  source MIT report     (fast: one scripted edit)
                                Task 3  poster                (fast: one line + re-render)
Wave 2 (after 1b AND 2)         Task 4  rebuild sample pack
Wave 3 (after 4)                Task 5  prototype + final sweep

--- second round, added 2026-10-12: the items Tasks 1-5 left for later ---

Wave 4 (parallel, 3 sessions)   Task 6  two sample rows on the list   (2 subagents)
                                Task 7  MIT report, 15-section        (slow: 1 Opus subagent)
                                Task 11 ringgit prose, source student (new tool + 13 subagents)
Wave 5 (after 7)                Task 8  US apply guide                (slow: Stage 8 research)
       (after 6)                Task 10 the 14 unverified rows        PARKED 2026-10-12 (Evan)
       (after 11)               Task 12 ringgit prose, other students PARKED 2026-10-12 (Evan)
Wave 6 (after 6, 7 AND 8)       Task 9  rebuild sample pack + prototype + sweep
```

Wave 1 tasks write disjoint files, so they are safe side by side. Task 3 depends on nothing and may
run at any point.

**Second round.** Task 9 is the one that changes what a prospect sees; it needs 6, 7 and 8 only.
Tasks 10, 11 and 12 fix the real students' files and can land before or after it.
**Tasks 10 and 12 are parked (Evan, 2026-10-12): do not run them in this round.** They are
tracked as P1 and P2 in `business/additionals.md` → "Sample pack fix round". What is left of this
plan is Task 8, then Task 9.
`master_list.csv` has three writers — Task 6, Task 7 (its last step only) and Task 10. Task 10
waits for Task 6; Task 7's step 5 must not run while a Task 6 session is between its steps 5 and 7.

### Status

- [x] Task 1 — source list rows
  - Run 2026-10-12. **Do not re-run.** MIT + Northeastern applied, `Warnings` pass written,
    `check_master_list.py` clean. It hit its stop condition on Rose-Hulman (no robotics major
    exists, minor only): that row was left untouched and `Not verified`, so step 8 fails on that
    one assert. Evan's call: fix the row — carried by Task 1b. Detail: the student's `status.md`.
- [x] Task 1b — Rose-Hulman course fix + the two unchecked rows
  - Run 2026-10-12. **Do not re-run.** 21 cells across 3 rows; Rose-Hulman is now
    `BS Mechanical Engineering (Robotics minor)`, `Official page`, total 1147360 → 1365391. Step 7
    prints `Task 1 + 1b OK: 43 rows; 14 Not verified left`; `check_master_list.py` 0 findings.
    Step 6's `feasibility_flags` call passes only the deadline, so it cannot see "Over budget" —
    checked separately: the profile has no budget ceiling, the flag cannot fire. `status.md` was
    over its 3000-char budget after Task 1; its history moved to `research_notes.md`
    ("Session history — 2026-10-12"). Row not re-scored, as planned.
- [x] Task 2 — source MIT report (2026-10-12; script prints `replaced 18 figures`, not 19 — the
  counts in `PAIRS` sum to 18, all 14 asserts passed, diffed against the backup)
- [x] Task 3 — poster (2026-10-12; re-render also moved the page-2 contact line from WhatsApp to
  Email — the HTML has said Email since 3caedbc, the committed PDF was never re-rendered after it)
- [x] Task 4 — rebuild sample pack (2026-10-12; `Scan clean`, `0 finding(s)`, `Task 4 OK: 19
  pages`; the glossary gained 5 terms from the re-verified rows, so `sample_glossary.csv` changed too)
- [x] Task 5 — prototype + final sweep (2026-10-12; `data.js: 15 rows x 35 columns`, step 6 no hits,
  step 9 only this file + `business/additionals.md`, smoke `147/147`.) Two things the steps did not
  foresee, both in `data.template.js` findings and both caused by the list getting cleaner:
  - Finding 4 printed `The other 0 () stay marked "Not verified"` once no sample row was
    unverified — now a zero-case sentence. `smoke.js` expected 13 verified rows; now 15.
  - Finding 3 dropped MIT: Task 1b's cell says "Need blind" (MIT's spelling), the template matched
    `/need-blind/` only — now `/need[- ]blind/`. Two smoke checks added for these (seen failing
    first), hence 147 not 145.
- [x] Task 6 — source list: re-score Rose-Hulman, re-read Northeastern's descriptive cells
  - Run 2026-10-12. **Do not re-run.** Rose-Hulman `81 A Safety` → `71 B Safety`, `Warnings`
    `None` → `English short`, total unchanged (1365391). Northeastern: 7 cells applied, row still
    `Official page`. `check_master_list.py`: list checks all ok; the only finding is `status.md`
    over its 3000-char budget (Tasks 9/10 trim it). Dispatch file:
    `plans/backfill_2026-10-12c_neu_descriptive.md`. Three things the steps did not foresee:
    - `score_log.jsonl` keys on a normalised `course_key` (`rose hulman ...`, no hyphen), so
      step 1's and step 7's `"rose-hulman" in l.lower()` never match. A July line for the old
      course name (`bs robotics engineering`, 81/A) was there all along; the log now holds both.
      Step 7 was run matching the new `course_key` exactly. Task 10: do not grep the log by hyphen.
    - The discovery fragment put `I-20` in `Work rights after graduating` (jargon finding after
      sync). Fixed with a one-cell `apply_backfill.py --overwrite` fragment, wording only.
    - This task's fragments were moved out afterwards: `.tmp/toru/backfill_applied_2026-10-12c/`
      and `.tmp/toru/candidates_applied_2026-10-12c/`. Both live folders are empty for Task 10.
- [x] Task 7 — source MIT report: rebuild in the 15-section layout
  - Run 2026-10-12. **Do not re-run.** `check_report.py` prints `mode report ... 0 finding(s)`, not
    `mode university` — since the schema merge the one current layout is named `report`; the
    expected strings in Tasks 7 and 8 are corrected below. `Task 7 report OK`. Snapshot figures
    unchanged from the old report. `flip_finalists.py`: no status change, one MIT `Student life`
    correction. `check_master_list.py`: all 7 list checks ok, 1 finding — `status.md` over its
    3000-char budget from this round's appends (Tasks 9/10 trim it).
  - For Task 9: the PDF is now 25 pages (was 19); the section headings changed ("How to apply" is
    no longer its own section; "Scholarships & financial aid" is), so expect
    `REPORT_TEXT_REDACTIONS` targets and the prototype's section list to need re-matching.
  - Leftovers that neither Task 8 nor Task 9 needs are in `business/additionals.md` → "Sample
    pack fix round" (S1-S7): the calendar skipping US reports, the MQA lookup, what the student
    has not been told yet.
- [x] Task 8 — source apply guide (US): Stage 8 re-run
  - Run 2026-10-12. **Do not re-run.** `master_list.csv: OK`, then `Task 8 OK: 9 universities;
    # Application prep — United States: 9 universities`. PDF eyeballed: lists, two-column
    tick-boxes and the calendar all render. Research JSON kept at `.tmp/toru/apply_prep_us.json`
    (a re-render costs no research); July copy in `.tmp/sample_pack_fix/task8/`.
  - **For Task 9:** the PDF is **27 pages** (was 15 — the README table says 15). The guide has a new
    `## Visa & immigration` section and a forms table under "5. Financial-aid forms cheat-sheet".
    It states the family-income band once (overview §3) and the college by name in several
    checklists, so the apply-guide redaction list needs both.
  - Facts the July guide had wrong, re-read on official pages: Princeton's aid form is the PFAA
    alone (no CSS Profile, no IDOC); Yale does not ask international applicants for the CSS Profile
    up front; Harvard (USD 95) and MIT (USD 75) charge an application fee; Stanford's is USD 100;
    Cornell's international aid deadline is the application date; Columbia is confirmed
    test-optional for Fall 2027. The DHS fixed-period rule (final 2026-07-17) was postponed by a
    federal court on 2026-09-14 — USCIS is on the previous rules.
  - Two things the steps did not foresee:
    - `tools/apply_glossary.py` changed, outside the task's write list: its `PFAA` definition said
      "filed alongside the CSS Profile" and its `ISAFA` entry had the wrong full name. Both print
      into the guide's Key terms, so they were fixed at the source.
    - Firecrawl was needed for Columbia's admissions site, Princeton's aid page and
      travel.state.gov (all HTTP 403 to free fetch).
  - **For Task 10 / Evan — the list was not edited (read-only here), and three cells now disagree
    with official pages:** Brown's `Key deadline` says Regular Decision 2027-01-01, Brown's
    checklist says 5 January; Princeton's and Yale's `How to get the scholarship` name the CSS
    Profile. None of the three is a `Not verified` row, so Task 10 will not reach them unprompted.
- [ ] Task 8b — **proposed 2026-10-13, not yet approved by Evan**: the Princeton cells the new
  apply guide contradicts. See the "Before you start" block at the top of Task 9.
- [ ] Task 9 — rebuild the sample pack (with the apply guide) + prototype + sweep
- [ ] Task 10 — source list: the other 14 `Not verified` rows
  - **PARKED 2026-10-12 (Evan). Do not run in this round.** Tracked as P1 in
    `business/additionals.md`. Its steps below stay valid; read Task 6's notes above first.
- [x] Task 11 — ringgit prose: the tool, then the source student's other files
  - Run 2026-10-12. **Do not re-run.** Self-test matched. 13 fragments, `0 refused`, no `WARN`:
    231 figures replaced, 11 left alone; `findings unchanged` (16 reports, 0 findings); re-run
    inventory shows every stated rate at current. `recommendation.md` and `calendar.md` each hold
    one ringgit-native figure — no fragment. PDFs re-rendered one `--report` at a time, MIT untouched.
  - One flag, rewritten by hand: Oxford's cost section said the master-list row double-counts the
    college fee and is "RM 200k too high" — the row has since been fixed (tuition = 4 × the single
    fee), so the sentence now says that.
  - **For Task 12 — the tool cannot see a bare-number MYR table column** (`| 72,500 | 341,000 |`):
    `RM_FIGURE` needs `RM`/`MYR` in front. Six of the 13 reports had one. The agents caught them
    only because the dispatch file said to — copy its "Clarifications" section
    (`data/students/toru/plans/fx_prose_2026-10-12.md`) into Task 12's shared file. After the dry
    run, also diff old vs would-be text and list unchanged rows of any table whose header says MYR.
  - Also changed: one USD figure in Brown's report that was a ringgit-native amount converted the
    other way at the old rate. Left for others: `application_prep/us.md` states USD 4.08 (0.99%
    off, Task 8 rebuilds it).
  - Follow-up, same day, on Evan's say-so: the NUS report said the list records S$20,250/yr
    tuition; the row holds S$18,050. Sentence corrected by hand, PDF re-rendered, 0 findings.
    Still open in that report: its verdict table says the list records the subject rank as
    "top 10–15"; the row now says #3.
- [ ] Task 12 — ringgit prose: the other students' reports
  - **PARKED 2026-10-12 (Evan). Do not run in this round.** Tracked as P2 in
    `business/additionals.md`. Its steps below stay valid; read Task 11's notes above first.

## Shared facts

- **The defect.** The sample pack was built before the 2026-09-05 FX refresh. `FX_TO_MYR["USD"]` in
  `tools/shortlist_schema.py` is now `4.04` (`FX_AS_OF = "2026-09-05"`); the sample shows `4.70`.
  MIT four-year sticker: USD 371,040 → was RM 1,743,888, now RM 1,499,002.
- **Source student.** `SOURCE_STUDENT = "toru"` in `business/sales/sample_pack/build_sample_pack.py`.
  The sample is that student's `master_list.csv` (15 named rows) and MIT report, redacted. Fix the
  source, then rebuild — never hand-edit a file under `business/sales/sample_pack/`.
- **State of the source today.**
  - `data/students/toru/master_list.csv`: `Approx total (MYR)` at current rates. 43 rows. As of
    2026-10-12 (Task 1): no blank `Warnings`; MIT's test rule, deadline and aid dates corrected;
    Northeastern re-verified and `Official page` (its `Course` was renamed, total now 1588884).
    After Task 1b (same day): Rose-Hulman's `Course` is `BS Mechanical Engineering (Robotics
    minor)` and the row is `Official page`. 14 rows are `Info source = Not verified`, none of them
    a sample row.
  - `data/students/toru/reports/massachusetts-institute-of-technology.md`: prose still at 4.70. No
    research JSON survives, so the `.md` is the source — edit it directly.
- **`data/students/` is gitignored — no git undo.** Back up before writing:
  `mkdir -p .tmp/sample_pack_fix` and copy the file there first.
- **PII.** This file is tracked. Never paste the student's grades, income or school into it, into a
  commit message, or into anything under `business/` or `prototype/`.
- Console output mangles em-dashes on this machine. Prefix Python runs with
  `PYTHONIOENCODING=utf-8`. A `�` in terminal output is the console, not the file.

**Added for Tasks 6-12 (state after Task 5, 2026-10-12):**

- **The sample is current on its figures.** `sample_master_list.csv` and the MIT PDF are at USD
  4.04; the prototype's `data.js` was regenerated from them and `smoke.js` passes 147/147. What
  is left is listed task by task below — none of it is a wrong exchange rate in the sample.
- **Source list today.** 43 rows; 29 `Official page`, 14 `Not verified` (3 UK, 11 USA, all
  `Longlist`, none a sample row). `score_log.jsonl` holds the sub-scores for 34 of the 43 rows —
  Rose-Hulman is not one of them.
- **Current rates** (`FX_TO_MYR`, `FX_AS_OF = "2026-09-05"`): GBP 5.47 · USD 4.04 · AUD 2.91 ·
  SGD 3.19 · CNY 0.60 · CAD 2.93. Read them from the file at run time; these are for orientation.
- **`status.md` is appended to, never rewritten, by a task in this round** — several sessions may
  be open. One command, at the end of your task:
  `printf '\n- %s Task N: <what changed>\n' "$(date +%F)" >> data/students/toru/status.md`.
  The file has a 3000-character budget; Task 9 trims it (Task 10 would have too — parked).
- **Subagents.** A dispatch prompt is a file path plus a number, never pasted context
  (`workflows/00_overview.md` → "Dispatch by reference, not by paste"). An agent cannot ask a
  question, so every judgement it might need is written into the shared file first.
- **Other students' slugs are real names.** They never go in this file. Task 12 keeps them in
  `notes/` and `.tmp/`, both gitignored.

---

## Task 1 — Source list: bring the sample rows current

**Runs:** Wave 1, parallel-safe. **Depends on:** nothing.

**Writes:** `data/students/toru/master_list.csv`, `data/students/toru/research_notes.md`,
`data/students/toru/glossary.csv`, `data/students/toru/status.md`,
`data/students/toru/plans/backfill_2026-10-12_sample_rows.md` (new), `.tmp/toru/backfill/*.json`.

**Goal:** three sample rows carry official-source facts, and no row has a blank `Warnings`.

- [ ] **1. Back up.**
  ```bash
  mkdir -p .tmp/sample_pack_fix
  cp data/students/toru/master_list.csv data/students/toru/research_notes.md .tmp/sample_pack_fix/
  ```
- [ ] **2. Read the repair path.** `workflows/03_discover_longlist.md` → "Backfilling an existing
  longlist"; the backfill half of `.claude/agents/row-filler.md`;
  `python tools/shortlist_schema.py --contract` for cell budgets and sentinels. Format precedent for
  the shared-context file: `data/students/toru/plans/backfill_2026-08-08.md`.
- [ ] **3. Write the shared context once** →
  `data/students/toru/plans/backfill_2026-10-12_sample_rows.md`. Three dispatches:

  | # | University | Columns to research | Why |
  |---|---|---|---|
  | 1 | Rose-Hulman Institute of Technology | `Course`, `Entry requirements`, `English req`, `Annual tuition`, `Total tuition`, `Est. living/yr`, `Duration (yrs)`, `Scholarship & portal`, `Scholarship coverage`, `Scholarship competitiveness`, `How to get the scholarship`, `Key deadline`, `Intake`, `Course URL`, `Info source` | Row is `Not verified`. Its own `Notes` doubt the degree exists as named; `Entry requirements` ends "confirm" on SAT/ACT. |
  | 2 | Northeastern University | same column list as #1 | Row is `Not verified`; `Entry requirements` ends "confirm" on SAT/ACT; tuition is "approx". |
  | 3 | Massachusetts Institute of Technology | `Entry requirements`, `Key deadline`, `How to get the scholarship` | Row says "SAT/ACT optional-ish" — MIT requires the SAT or ACT. Row says Regular Action 2027-01-01 — the student's MIT report says 4 January 2027. Scholarship cell repeats the Jan 1 date. Official pages are already listed in §16 of the student's MIT report. |

  Constraints to state in that file: `Info source` becomes `Official page` only when every
  researched fact came from the university's own pages, otherwise it stays `Not verified`; keep
  `Key deadline` ISO-first (`2027-01-04 (Regular Action; Early Action 2026-11-01)`) because
  `_parse_iso_date` reads the first date in the cell; fees are sticker price in USD, scholarships
  stay in their own columns.
- [ ] **4. Dispatch three `row-filler` agents in BACKFILL mode, in parallel.** Each prompt = the plan
  file path, the dispatch number, the university. Nothing else.
- [ ] **5. Apply.** These cells are already filled, so `--overwrite` is required. The dry run is the
  gate: confirm it touches only these three rows and only the listed columns.
  ```bash
  PYTHONIOENCODING=utf-8 python tools/apply_backfill.py --student toru --country USA --overwrite --dry-run
  PYTHONIOENCODING=utf-8 python tools/apply_backfill.py --student toru --country USA --overwrite
  ```
- [ ] **6. Recompute `Approx total (MYR)` where a cost cell moved.** `apply_backfill.py` prints a
  NOTICE naming the stale computed columns and does not recompute them. For Rose-Hulman and
  Northeastern only, if any of `Total tuition` / `Est. living/yr` / `Duration (yrs)` changed:
  `round((total_tuition + living_per_year × years) × 4.04)`, written as a plain integer like the
  other rows. Check against the current values first — Rose-Hulman is `(220000 + 16000×4) × 4.04 =
  1147360` today, which proves the formula.
- [ ] **7. Warnings pass — all 43 rows, one read-modify-write.** A clean row must read `None`, not
  blank (`tools/sync_shortlist.py:108-118`). Run it as shown for a dry run and read the printed
  changes; then run it again with the first line changed to `python - --write <<'EOF'`. A dry run
  on 2026-10-12 gave `None` for all 40 blank cells — a different result means a deadline has since
  passed or Task 1's backfill moved one, so read it before writing.
  ```bash
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv, json, sys
  sys.path.insert(0, "tools")
  from shortlist_schema import feasibility_flags

  base = "data/students/toru/"
  profile = json.load(open(base + "profile.json", encoding="utf-8"))
  prefs = json.load(open(base + "preferences.json", encoding="utf-8"))
  with open(base + "master_list.csv", encoding="utf-8", newline="") as f:
      reader = csv.DictReader(f)
      fields, rows = reader.fieldnames, list(reader)

  changed = 0
  for r in rows:
      if r["Warnings"].strip():
          continue                      # a flag written at sync time stays as it is
      flags = feasibility_flags({"key_deadline": r["Key deadline"]}, profile, prefs)
      r["Warnings"] = "; ".join(flags) if flags else "None"   # mirrors WARNINGS_NONE
      changed += 1
      print(f'{r["University"][:45]:45} -> {r["Warnings"]}')
  print(changed, "blank cells filled")

  if "--write" in sys.argv:
      with open(base + "master_list.csv", "w", encoding="utf-8", newline="") as f:
          w = csv.DictWriter(f, fieldnames=fields)
          w.writeheader(); w.writerows(rows)
      print("written")
  EOF
  ```
  Limit of this pass, to record in `status.md`: `English short` and `Recognition risk` need candidate fields the CSV does
  not hold, so they cannot be re-derived here; a blank cell means neither fired when the row was
  first written.
- [ ] **8. Verify.**
  ```bash
  PYTHONIOENCODING=utf-8 python tools/check_master_list.py --student toru
  PYTHONIOENCODING=utf-8 python tools/build_glossary_sheet.py --student toru
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv, re
  rows = list(csv.DictReader(open("data/students/toru/master_list.csv", encoding="utf-8", newline="")))
  src = open("business/sales/sample_pack/build_sample_pack.py", encoding="utf-8").read()
  sample = re.findall(r'^    "([^"]+)",$', src, flags=re.M)
  assert len(sample) == 15, sample
  by = {r["University"]: r for r in rows}
  assert not [r["University"] for r in rows if not r["Warnings"].strip()], "blank Warnings left"
  bad = [u for u in sample if by[u]["Info source"] != "Official page"]
  assert not bad, bad
  mit = by["Massachusetts Institute of Technology"]
  assert "optional" not in mit["Entry requirements"].lower(), mit["Entry requirements"]
  assert mit["Key deadline"].startswith("2027-01-04"), mit["Key deadline"]
  print("Task 1 OK:", len(rows), "rows")
  EOF
  ```
  Expected: `0 finding(s)`, then `Task 1 OK: 43 rows`.
- [ ] **9. Update `data/students/toru/status.md`** with a dated note: which cells changed in the three
  rows, the `Warnings` migration and its limit from step 7.

**Stop and report instead of forcing it** if a row-filler cannot confirm Rose-Hulman's or
Northeastern's facts on official pages, or finds the Rose-Hulman course does not exist as listed.
Do not stamp `Official page`, do not drop the row. The fallback (swapping the row out of
`SAMPLE_UNIVERSITIES`, which also touches `IDS` in `prototype/_build/gen.py`) is Evan's call.

**Tell Evan:** this changes the real student's list. Name the cells that changed so he can decide
whether to re-send it.

---

## Task 1b — Rose-Hulman course fix + the two unchecked rows

**Runs:** Wave 1, parallel-safe with Tasks 2 and 3. **Depends on:** Task 1 (done).

**Writes:** `data/students/toru/master_list.csv`, `data/students/toru/research_notes.md`,
`data/students/toru/glossary.csv`, `data/students/toru/status.md`, `.tmp/toru/backfill/*.json`.

**Why it exists.** Task 1 hit its stop condition on 2026-10-12: Rose-Hulman has no robotics major,
only a minor, so the row was left untouched. **Evan decided the same day: fix the row to the real
degree path (BS Mechanical Engineering + Robotics minor); do not swap it out of the sample.** Task 1
also left three descriptive cells unchecked on rows it had just re-verified. Both are closed here.

**Goal:** the Rose-Hulman row names a degree that exists and is `Official page`; MIT's and
Northeastern's unchecked cells say only what an official page says; Task 1's step-8 check passes
in full.

- [ ] **1. Precondition and backup.** `.tmp/sample_pack_fix/master_list.csv` is the pre-Task-1 copy —
  never overwrite it; this task backs up into a subfolder.
  ```bash
  mkdir -p .tmp/sample_pack_fix/task1b
  cp data/students/toru/master_list.csv data/students/toru/research_notes.md .tmp/sample_pack_fix/task1b/
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv, os
  rows = list(csv.DictReader(open("data/students/toru/master_list.csv", encoding="utf-8", newline="")))
  by = {r["University"]: r for r in rows}
  assert by["Massachusetts Institute of Technology"]["Key deadline"].startswith("2027-01-04"), "Task 1 not applied"
  assert by["Northeastern University"]["Info source"] == "Official page", "Task 1 not applied"
  assert not [r for r in rows if not r["Warnings"].strip()], "Task 1 Warnings pass not written"
  assert by["Rose-Hulman Institute of Technology"]["Course"] == "BS Robotics Engineering", "Task 1b already ran"
  assert os.path.exists("data/students/toru/plans/backfill_2026-10-12b_rhit_and_notes.md"), "dispatch file missing"
  print("preconditions OK")
  EOF
  ```
- [ ] **2. Stage the held fragment.** Task 1's Rose-Hulman research (13 cells, all read on
  rose-hulman.edu / rhit.edu) was kept out of the apply. Move it in; the dispatch extends it in place.
  ```bash
  mkdir -p .tmp/toru/backfill
  mv .tmp/toru/backfill_held/rose-hulman-institute-of-technology.json .tmp/toru/backfill/
  ls .tmp/toru/backfill
  ```
  Expected: that one file and nothing else. A stale fragment in that folder gets applied with
  `--overwrite`, so move anything else out first. If the held file is gone (`.tmp/` is disposable),
  carry on — the dispatch file tells the agent to research those columns too.
- [ ] **3. The shared context is already written** —
  `data/students/toru/plans/backfill_2026-10-12b_rhit_and_notes.md`. Read it; do not rewrite it.
  Its three dispatches:

  | # | University | Columns | Why |
  |---|---|---|---|
  | 1 | Rose-Hulman Institute of Technology | adds `Course`, `Course URL`, `Course at a glance`, `Subject rank`, `Recognised in Malaysia?`, `Notes`, re-decides `Info source`; keeps the 13 held cells | Four cells besides `Course` still describe the non-existent degree. Two scholarship flags from the first pass are open (international eligibility not stated; one award published for 2026-27 only). |
  | 2 | Massachusetts Institute of Technology | `Notes`, `Scholarship coverage` | "Need-blind" was never read on an official page; "one of ~9 US schools" and "~4% admit rate" ride in the same cells. |
  | 3 | Northeastern University | `Notes`, `Course at a glance` | "90%+ of ME students complete a co-op" is unchecked; "typically 5-yr" contradicts the row's `Duration (yrs)` = 4. |

  Northeastern's `Course` was renamed by Task 1 — the dispatch file carries the current string.
- [ ] **4. Dispatch three `row-filler` agents in BACKFILL mode, in parallel.** Each prompt = the
  dispatch file's path, the dispatch number, the university. Nothing else.
- [ ] **5. Apply.** The dry run is the gate: exactly three rows; MIT and Northeastern at most two
  cells each, only the columns in the table; Rose-Hulman about 17 cells, none outside the table's
  list plus Task 1's column list.
  ```bash
  PYTHONIOENCODING=utf-8 python tools/apply_backfill.py --student toru --country USA --overwrite --dry-run
  PYTHONIOENCODING=utf-8 python tools/apply_backfill.py --student toru --country USA --overwrite
  ```
- [ ] **6. Recompute, re-check the deadline flag, rename the notes heading — one pass.** Run as shown
  for a dry run; then again with the first line changed to `python - --write <<'EOF'`.
  ```bash
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv, json, re, sys
  sys.path.insert(0, "tools")
  from shortlist_schema import FX_TO_MYR, feasibility_flags

  base = "data/students/toru/"
  fx = FX_TO_MYR["USD"]
  with open(base + "master_list.csv", encoding="utf-8", newline="") as f:
      reader = csv.DictReader(f)
      fields, rows = reader.fieldnames, list(reader)
  by = {r["University"]: r for r in rows}
  num = lambda s: int(re.search(r"\d+", s.replace(",", "")).group())
  calc = lambda r: round((num(r["Total tuition"]) + num(r["Est. living/yr"]) * num(r["Duration (yrs)"])) * fx)
  assert calc(by["Massachusetts Institute of Technology"]) == 1499002   # proves the formula
  assert calc(by["Northeastern University"]) == 1588884

  rh = by["Rose-Hulman Institute of Technology"]
  print("Rose-Hulman Approx total (MYR):", rh["Approx total (MYR)"], "->", calc(rh))
  rh["Approx total (MYR)"] = str(calc(rh))

  profile = json.load(open(base + "profile.json", encoding="utf-8"))
  prefs = json.load(open(base + "preferences.json", encoding="utf-8"))
  flags = feasibility_flags({"key_deadline": rh["Key deadline"]}, profile, prefs)
  assert rh["Warnings"] == "None" and not flags, (rh["Warnings"], flags)   # deadline cell moved

  old = b"## Rose-Hulman Institute of Technology - BS Robotics Engineering"
  new = ("## Rose-Hulman Institute of Technology - " + rh["Course"]).encode("utf-8")
  raw = open(base + "research_notes.md", "rb").read()
  assert raw.count(old) == 1, raw.count(old)
  print("notes heading ->", new.decode("utf-8"))

  if "--write" in sys.argv:
      with open(base + "master_list.csv", "w", encoding="utf-8", newline="") as f:
          w = csv.DictWriter(f, fieldnames=fields)
          w.writeheader(); w.writerows(rows)
      open(base + "research_notes.md", "wb").write(raw.replace(old, new))
      print("written")
  EOF
  ```
  Expected if the agent left the held cost cells alone: `1147360 -> 1365391`
  (`(239088 + 24720×4) × 4.04`). A different figure means a cost cell moved — read the fragment's
  `gaps` for why before writing. A failed `Warnings` assert means a flag now fires: write the flag
  into the cell by hand instead of `None`.
- [ ] **7. Verify.** The first half is Task 1's step 8, which could not pass until now.
  ```bash
  PYTHONIOENCODING=utf-8 python tools/check_master_list.py --student toru
  PYTHONIOENCODING=utf-8 python tools/build_glossary_sheet.py --student toru
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv, re
  rows = list(csv.DictReader(open("data/students/toru/master_list.csv", encoding="utf-8", newline="")))
  src = open("business/sales/sample_pack/build_sample_pack.py", encoding="utf-8").read()
  sample = re.findall(r'^    "([^"]+)",$', src, flags=re.M)
  assert len(sample) == 15, sample
  by = {r["University"]: r for r in rows}
  assert not [r["University"] for r in rows if not r["Warnings"].strip()], "blank Warnings left"
  bad = [u for u in sample if by[u]["Info source"] != "Official page"]
  assert not bad, bad
  mit = by["Massachusetts Institute of Technology"]
  assert "optional" not in mit["Entry requirements"].lower(), mit["Entry requirements"]
  assert mit["Key deadline"].startswith("2027-01-04"), mit["Key deadline"]
  assert "~9" not in mit["Scholarship coverage"], mit["Scholarship coverage"]
  rh = by["Rose-Hulman Institute of Technology"]
  assert "Mechanical" in rh["Course"] and "Robotics Engineering" not in rh["Course"], rh["Course"]
  assert "robotics-engineering/index.html" not in rh["Course URL"], rh["Course URL"]
  assert "Robotics Engineering BS" not in rh["Subject rank"] + rh["Recognised in Malaysia?"]
  assert "Verify degree path" not in rh["Notes"], rh["Notes"]
  assert rh["Approx total (MYR)"] != "1147360", "total not recomputed"
  assert "5-yr" not in by["Northeastern University"]["Course at a glance"] or "4" in by["Northeastern University"]["Course at a glance"]
  print("Task 1 + 1b OK:", len(rows), "rows;", sum(r["Info source"] == "Not verified" for r in rows), "Not verified left")
  EOF
  ```
  Expected: `0 finding(s)`, then `Task 1 + 1b OK: 43 rows; 14 Not verified left`.
- [ ] **8. Update `data/students/toru/status.md`.** Dated note naming the cells that changed in each
  of the three rows and every claim an agent removed. Replace "Next action" item 0 (the pending
  Rose-Hulman decision) with what is left: tell the student about MIT's corrected test rule and aid
  deadlines. State plainly that the Rose-Hulman row was **not re-scored** (see below).

**If Rose-Hulman comes back `Info source = Not verified`:** apply it anyway — the course fix is
decided and the row is more accurate with it than without — but do not stamp it. Step 7 then fails
on the `bad` assert only and Task 4 stays blocked; report which fact could not be sourced and stop.
Swapping the row out of `SAMPLE_UNIVERSITIES` remains Evan's call.

**Not re-scored, on purpose.** `Desirability` 81 / `Tier` A / `Admission likelihood` Safety were set
when the row was believed to be a dedicated robotics degree. `apply_backfill.py` has cells, not
sub-scores, so they stand. See "Not in this plan".

**Tell Evan:** the cells that changed on the real student's list, row by row; every claim that was
removed for lack of an official source; and that the Rose-Hulman score is unchanged.

---

## Task 2 — Source MIT report: re-convert the ringgit prose

**Runs:** Wave 1, parallel-safe. **Depends on:** nothing.

**Writes:** `data/students/toru/reports/massachusetts-institute-of-technology.md` and its `.pdf`.
Does **not** write `status.md` (Task 1 owns it in Wave 1; Task 4 adds this task's line).

**Goal:** every ringgit figure in the report converted at 4.04. USD figures are untouched.

- [ ] **1. Back up and take the baseline.**
  ```bash
  mkdir -p .tmp/sample_pack_fix
  cp data/students/toru/reports/massachusetts-institute-of-technology.md .tmp/sample_pack_fix/
  PYTHONIOENCODING=utf-8 python tools/check_report.py --student toru --report massachusetts-institute-of-technology
  ```
  Expected baseline: `mode legacy_university ... 0 finding(s)`.
- [ ] **2. Apply the replacements — one scripted pass, no `Edit` calls.** Counts were measured on
  2026-10-12; a mismatch means the report changed, so the script stops without writing.
  ```bash
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  from pathlib import Path
  p = Path("data/students/toru/reports/massachusetts-institute-of-technology.md")
  t = p.read_text(encoding="utf-8")
  PAIRS = [  # (old, new, expected count)          USD basis x 4.04
      ("(~RM 4.70 per USD)", "(~RM 4.04 per USD)", 1),
      ("~RM 313,600", "~RM 269,500", 1),           # 66,720
      ("| 420 | ~RM 2,000 |", "| 420 | ~RM 1,700 |", 1),
      ("~RM 66,200", "~RM 56,900", 1),             # 14,090
      ("~RM 38,100", "~RM 32,700", 1),             # 8,104
      ("~RM 4,400", "~RM 3,800", 1),               # 930
      ("~RM 11,700", "~RM 10,100", 1),             # 2,496
      ("RM 436,000", "RM 375,000", 2),             # 92,760  (table + warning box)
      ("~RM 1.74 million", "~RM 1.50 million", 1), # 371,040
      ("~RM 25,400", "~RM 21,800", 1),             # 5,400
      ("RM 25,000", "RM 22,000", 3),               # 5,400 rounded (snapshot, table, section 15)
      ("~RM 102,000", "~RM 87,000", 2),            # 21,600
      ("(about RM 350)", "(about RM 300)", 1),     # 75
      ("(about RM 629,000)", "(about RM 541,000)", 1),  # 133,793
  ]
  for old, _, n in PAIRS:
      assert t.count(old) == n, (old, t.count(old), n)
  for old, new, _ in PAIRS:
      t = t.replace(old, new)
  assert "4.70" not in t and "1.74 million" not in t
  p.write_text(t, encoding="utf-8")
  print("replaced", sum(n for *_, n in PAIRS), "figures")
  EOF
  ```
  Expected: `replaced 19 figures`.
- [ ] **3. Leave these alone.** The two `RM 0` cells, and the family-income sentence near line 331:
  it is a ringgit-native figure, and it is one of the exact strings `REPORT_TEXT_REDACTIONS` in
  `build_sample_pack.py` matches on — changing it breaks Task 4.
- [ ] **4. Re-render the student's own PDF and re-check.**
  ```bash
  PYTHONIOENCODING=utf-8 python tools/report_to_pdf.py --student toru --report massachusetts-institute-of-technology
  PYTHONIOENCODING=utf-8 python tools/check_report.py --student toru --report massachusetts-institute-of-technology
  ```
  Expected: still `0 finding(s)`.

**Tell Evan:** the real student's MIT report changed (ringgit figures only, all lower). Nine other
reports for this student still state the old rate — out of scope here, see "Not in this plan".

---

## Task 3 — Poster

**Runs:** any time, parallel-safe. **Depends on:** nothing.

**Writes:** `business/sales/pitch/university-research-service-poster.html`,
`business/sales/pitch/University_research_service_poster.pdf`.

- [ ] **1. Edit one line** (`university-research-service-poster.html:663`):
  `≈RM 1.74M total, 4 years` → `≈RM 1.50M total, 4 years`. It is the only ringgit figure in the file.
- [ ] **2. Re-render.** Read the docstring at the top of `tools/html_to_pdf.py` first. The committed
  PDF's name differs from the HTML's (capital U, underscores), so `--output` is mandatory — the
  default would write a second, differently-named PDF beside it.
  ```bash
  PYTHONIOENCODING=utf-8 python tools/html_to_pdf.py \
    --input business/sales/pitch/university-research-service-poster.html \
    --output business/sales/pitch/University_research_service_poster.pdf
  ```
- [ ] **3. Verify.** Open the PDF with the Read tool: same page count as `git show HEAD:` had, the MIT
  row reads `≈RM 1.50M`, nothing else moved. Then:
  ```bash
  git status --short business/sales/pitch/
  ```
  Expected: exactly two modified files, no new untracked PDF.

---

## Task 4 — Rebuild the sample pack

**Runs:** Wave 2. **Depends on:** Task 1, Task 1b and Task 2.

**Writes:** `business/sales/sample_pack/sample_master_list.csv`, `sample_glossary.csv`,
`sample_university-report_MIT.pdf`, `README.md`; `business/additionals.md`;
`data/students/toru/status.md` (one line).

- [ ] **1. Precondition — stop if this fails.**
  ```bash
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv
  t = open("data/students/toru/reports/massachusetts-institute-of-technology.md", encoding="utf-8").read()
  assert "(~RM 4.04 per USD)" in t and "4.70" not in t, "Task 2 not done"
  rows = list(csv.DictReader(open("data/students/toru/master_list.csv", encoding="utf-8", newline="")))
  assert not [r for r in rows if not r["Warnings"].strip()], "Task 1 not done (blank Warnings)"
  by = {r["University"]: r for r in rows}
  for u in ("Rose-Hulman Institute of Technology", "Northeastern University"):
      assert by[u]["Info source"] == "Official page", f"Task 1 not done ({u})"
  print("preconditions OK")
  EOF
  ```
- [ ] **2. Rebuild.**
  ```bash
  PYTHONIOENCODING=utf-8 python business/sales/sample_pack/build_sample_pack.py
  ```
  Expected last line: `Scan clean: zero hits for name / school / income figures.` If it exits with
  `expected redaction target not found`, the source report's wording moved: update
  `REPORT_TEXT_REDACTIONS` to match. Never comment the check out — it is the PII gate.
- [ ] **3. Verify.**
  ```bash
  PYTHONIOENCODING=utf-8 python tools/check_master_list.py --file business/sales/sample_pack/sample_master_list.csv
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv
  from pypdf import PdfReader
  d = "business/sales/sample_pack/"
  rows = list(csv.DictReader(open(d + "sample_master_list.csv", encoding="utf-8", newline="")))
  by = {r["University"]: r for r in rows}
  assert len(rows) == 15
  assert by["Massachusetts Institute of Technology"]["Approx total (MYR)"].replace(",", "") == "1499002"
  assert all(r["Info source"] == "Official page" for r in rows)
  assert all(r["Warnings"].strip() for r in rows)
  pdf = PdfReader(d + "sample_university-report_MIT.pdf")
  text = " ".join(" ".join((p.extract_text() or "").split()) for p in pdf.pages)
  for must in ("4.04 per USD", "1.50 million", "RM 375,000", "anonymized demo"):
      assert must in text, must
  for never in ("4.70", "1.74", "436,000", "102,000", "629,000"):
      assert never not in text, never
  print("Task 4 OK:", len(pdf.pages), "pages")
  EOF
  git status --short business/sales/sample_pack/
  ```
  Expected: `0 finding(s)`, `Task 4 OK: 19 pages` (if the page count moved, fix it in the README
  table), and only sample-pack files modified.
- [ ] **4. `business/sales/sample_pack/README.md`.** Under "How they were built", add the rebuild date
  and the rate stamp it was built at (`FX_AS_OF 2026-09-05`). Leave the apply-guide paragraph as it
  is — that file is still not covered.
- [ ] **5. `business/additionals.md` → L1.** Tick the box and add a dated "Resolved" line. Correct the
  record while there: L1's suggested fix said a rebuild alone would also fill the empty `Warnings`
  cells and clear the two `Not verified` rows. It would not — the source list had the same gaps.
  Task 1 of this plan fixed those at the source.
- [ ] **6. Append one line to `data/students/toru/status.md`:** MIT report ringgit figures
  re-converted at USD 4.04 on <date>, PDF re-rendered; nine other reports still state the old rate.

**Tell Evan:** open the CSV and the PDF once himself before the next send — the README makes him the
last gate.

---

## Task 5 — Prototype + final sweep

**Runs:** Wave 3. **Depends on:** Task 4.

**Writes:** `prototype/_build/data.template.js`, `prototype/_build/gen.py`, `prototype/data.js`
(generated), `prototype/_build/smoke.js`, `prototype/app.js` (comments), `prototype/BUILD_PLAN.md`.

- [ ] **1. Precondition.**
  ```bash
  grep -c "1499002" business/sales/sample_pack/sample_master_list.csv
  ```
  Expected: `1`. If `0`, Task 4 has not run.
- [ ] **2. Report figures in the template** (`prototype/_build/data.template.js:171-172`), hand-copied
  from the report's Snapshot and now changed there:
  `NET_COST_PER_YEAR = 25000` → `22000`; `NET_COST_TOTAL = 102000` → `87000`.
- [ ] **3. Retire the SAT override in `prototype/_build/gen.py`.** `OVERRIDES` patches MIT's
  `entryRequirements` because the old CSV said "optional-ish". Task 1 fixed the CSV, so the
  override's `assert row[key] == old` will now fail. Empty the dict (`OVERRIDES = {}`), keep the
  loop and the comment explaining the mechanism, and add one line saying the MIT entry was retired
  on <date> once the sample CSV caught up.
- [ ] **4. Regenerate `data.js`.** Never hand-edit it.
  ```bash
  PYTHONIOENCODING=utf-8 python prototype/_build/gen.py . prototype/_build/data.template.js
  ```
  Expected: `data.js: 15 rows x 35 columns, 15 report sections` and `stubs: 0 written, 14 existing
  screen files left alone`. Then confirm `prototype/data.js` holds `"approxTotalMyr": 1499002` and
  that MIT's `entryRequirements` says the SAT or ACT is required.
- [ ] **5. Update the self-test's hard-coded expectation** (`prototype/_build/smoke.js:346`):
  `'RM 1,743,888|RM 1.74M|RM 452k'` → `'RM 1,499,002|RM 1.50M|RM 383k'`. The three parts are
  `myr(MIT)`, `myrShort(MIT)`, `myrShort(NUS)`; confirm MIT and NUS against the regenerated
  `data.js` rather than trusting these literals (NUS is `383438` unless Task 1 moved it). Fix the
  matching example comments too: `smoke.js:252` (`"RM 451,500"`) and `app.js:18-19`.
- [ ] **6. Look for figures typed into a screen.**
  ```bash
  grep -rnE "1\.74|1,743|451,?500|25,000|102,000|optional-ish" prototype/ --include=*.js --include=*.html --include=*.css
  ```
  Expected: no hits at all. Before this task the only hits were the three lines step 5 fixes plus
  `data.js` itself, and none were in `screens/`. A new hit in `screens/` is a number that should
  have come from `DATA` — replace it with the `DATA` read, do not retype the new value.
- [ ] **7. Run the click-through.**
  ```bash
  mkdir -p .tmp/proto-shots && node prototype/_build/smoke.js . .tmp/proto-shots
  ```
  Expected: `N/N checks passed`, exit 0 (it was 145/145 on 2026-10-10). If a previous run was
  killed, end the `chrome.exe` whose command line contains `proto-smoke` first (port 9347).
- [ ] **8. `prototype/BUILD_PLAN.md`, decisions 5 and 6.** Both are now false. Rewrite them as
  resolved on <date>: the sample CSV says the SAT or ACT is required and the `gen.py` override is
  gone; ringgit totals are at the 2026-09-05 rates.
- [ ] **9. Final sweep across the repo.**
  ```bash
  grep -rnE "1\.74 ?(M|million)|1,743,888|1743888|4\.70? per USD" . \
    --include=*.md --include=*.html --include=*.js --include=*.py --include=*.csv \
    --exclude-dir=data --exclude-dir=.tmp --exclude-dir=.git --exclude-dir=node_modules
  ```
  Expected hits, and only these: this plan file, and `business/additionals.md` (L1 quotes the old
  figure as history). Anything else is a miss — fix it or report it. On 2026-10-12 the misses were
  the poster HTML, the sample CSV, `prototype/app.js`, `prototype/BUILD_PLAN.md`,
  `prototype/data.js` and `prototype/_build/smoke.js`.

**Tell Evan:** everything is done; run `/commit` to split and save the changes.

---

## Task 6 — Source list: re-score Rose-Hulman, re-read Northeastern's descriptive cells

**Runs:** Wave 4, parallel-safe with Tasks 7 and 11 (see the `master_list.csv` rule under "Order").
**Depends on:** Task 1b.

**Writes:** `data/students/toru/master_list.csv`, `research_notes.md`, `score_log.jsonl`,
`glossary.csv`, `status.md` (one appended line),
`data/students/toru/plans/backfill_<date>_neu_descriptive.md` (new), `.tmp/toru/country_usa.json`,
`.tmp/toru/candidates/*.json`, `.tmp/toru/backfill/*.json`.

**Goal:** the Rose-Hulman row's `Desirability` / `Tier` / `Admission likelihood` are computed for
the degree it now names, with its eight sub-scores on file; the seven Northeastern cells Task 1
never re-read say only what an official page says.

**Why a swap, not an edit.** The three score cells are computed from eight 0-5 sub-scores.
`score_log.jsonl` has no Rose-Hulman line (34 lines for 43 rows, checked 2026-10-12), so there is
nothing to recompute from. `sync_shortlist.py` is the only tool that scores, and it **skips** a
university+course already on the list. So: research the row afresh, take the old row out, sync the
new one in.

- [ ] **1. Precondition, backup, clear stale fragments.** `.tmp/toru/backfill/` still holds the
  three fragments Task 1b applied; `apply_backfill.py --overwrite` would apply them again.
  ```bash
  mkdir -p .tmp/sample_pack_fix/task6 .tmp/toru/backfill_applied_2026-10-12b
  cp data/students/toru/master_list.csv data/students/toru/research_notes.md data/students/toru/score_log.jsonl .tmp/sample_pack_fix/task6/
  mv .tmp/toru/backfill/*.json .tmp/toru/backfill_applied_2026-10-12b/ 2>/dev/null
  ls .tmp/toru/backfill .tmp/toru/candidates 2>/dev/null
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv
  rows = list(csv.DictReader(open("data/students/toru/master_list.csv", encoding="utf-8", newline="")))
  rh = [r for r in rows if r["University"] == "Rose-Hulman Institute of Technology"]
  assert len(rows) == 43 and len(rh) == 1, (len(rows), len(rh))
  assert rh[0]["Course"] == "BS Mechanical Engineering (Robotics minor)", rh[0]["Course"]
  assert rh[0]["List status"] == "Longlist" and rh[0]["Info source"] == "Official page"
  assert "rose-hulman" not in open("data/students/toru/score_log.jsonl", encoding="utf-8").read().lower(), "already re-scored"
  print("preconditions OK; old score:", rh[0]["Desirability"], rh[0]["Tier"], rh[0]["Admission likelihood"])
  EOF
  ```
  Expected: both folders listed empty (or missing), then `preconditions OK; old score: 81 A Safety`.
- [ ] **2. Country constants.** `.tmp/toru/country_usa.json` does not exist (`.tmp/` is disposable).
  Write it as `workflows/03_discover_longlist.md` → "Step 2 — Country constants" describes, from
  the known-good sources in `workflows/countries/usa.md`.
- [ ] **3. Write the Northeastern shared context** →
  `data/students/toru/plans/backfill_<date>_neu_descriptive.md`. Copy the "The student", "Sourcing —
  hard rule" and budget-format sections from `plans/backfill_2026-10-12b_rhit_and_notes.md`; take
  the budgets from `python tools/shortlist_schema.py --contract`. One dispatch:

  | # | University | Columns | Why |
  |---|---|---|---|
  | 1 | Northeastern University | `Student life`, `Overall rank`, `Subject rank`, `Work rights after graduating`, `Recognised in Malaysia?`, `Money to show (visa)`, `How to apply` | The row is `Official page` on its hard-fact columns only. These seven were written before the 2026-07-29 rebuild and never re-read. |

  The row's `Course` is `Mechanical Engineering, BSME (Boston) with Robotics Minor (co-op)` — the
  dispatch file must carry that string exactly; it is how `apply_backfill.py` finds the row.
- [ ] **4. Dispatch two `row-filler` agents in parallel.**
  - **Backfill** — prompt = the dispatch file's path, dispatch number 1, the university. Nothing else.
  - **Discovery**, Rose-Hulman — prompt = student slug `toru`; the university; the course string
    `BS Mechanical Engineering (Robotics minor)` to be used **verbatim** as `course`; city and
    course URL copied from the row; country `USA`; the path `.tmp/toru/country_usa.json`. Add
    these three sentences: "This row is already on the list and is being re-scored, not
    discovered. Its hard-fact cells were verified on official pages on 2026-10-12 — read that one
    row of `data/students/toru/master_list.csv` and the block under its heading in
    `research_notes.md`, re-use what is there, and spend your fetches on the eight sub-scores and
    `entry_margin`. Score the degree that exists — a Mechanical Engineering BS with a Robotics
    minor — not a dedicated robotics degree."
- [ ] **5. Apply Northeastern.** The dry run is the gate: one row, at most seven cells, only the
  columns in the table.
  ```bash
  PYTHONIOENCODING=utf-8 python tools/apply_backfill.py --student toru --country USA --overwrite --dry-run
  PYTHONIOENCODING=utf-8 python tools/apply_backfill.py --student toru --country USA --overwrite
  ```
- [ ] **6. Swap Rose-Hulman.** Merge first — it writes nothing to the list and exits 1 naming any
  missing field. Re-dispatch once with that list if it does.
  ```bash
  PYTHONIOENCODING=utf-8 python tools/merge_candidates.py --student toru --country USA
  ```
  Then take the old row out and free its notes heading (`sync_shortlist.py` also skips a
  `research_notes.md` block whose heading already exists). Dry run as shown; then again with the
  first line changed to `python - --write <<'EOF'`.
  ```bash
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv, sys
  base = "data/students/toru/"
  with open(base + "master_list.csv", encoding="utf-8", newline="") as f:
      reader = csv.DictReader(f)
      fields, rows = reader.fieldnames, list(reader)
  keep = [r for r in rows if r["University"] != "Rose-Hulman Institute of Technology"]
  assert len(rows) - len(keep) == 1, len(rows) - len(keep)
  old = b"## Rose-Hulman Institute of Technology - BS Mechanical Engineering (Robotics minor)"
  raw = open(base + "research_notes.md", "rb").read()
  assert raw.count(old) == 1, raw.count(old)
  print("would remove 1 row, leaving", len(keep), "and mark the old notes heading [pre-rescore]")
  if "--write" in sys.argv:
      with open(base + "master_list.csv", "w", encoding="utf-8", newline="") as f:
          w = csv.DictWriter(f, fieldnames=fields)
          w.writeheader(); w.writerows(keep)
      open(base + "research_notes.md", "wb").write(raw.replace(old, old + b" [pre-rescore]"))
      print("written")
  EOF
  PYTHONIOENCODING=utf-8 python tools/sync_shortlist.py --student toru --country USA --dry-run
  ```
  Expected from the dry run: `1 candidates in file | 0 duplicates skipped | 1 new`, then one line
  with the new tier, score and Reach/Match/Safety. `1 duplicates skipped` means the row is still
  there. Then run the same command without `--dry-run`. If anything after the removal fails, copy
  the three files back from `.tmp/sample_pack_fix/task6/` and stop.
- [ ] **7. Verify.**
  ```bash
  PYTHONIOENCODING=utf-8 python tools/check_master_list.py --student toru
  PYTHONIOENCODING=utf-8 python tools/build_glossary_sheet.py --student toru
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv, json, re
  rows = list(csv.DictReader(open("data/students/toru/master_list.csv", encoding="utf-8", newline="")))
  rh = [r for r in rows if r["University"] == "Rose-Hulman Institute of Technology"]
  assert len(rows) == 43 and len(rh) == 1, (len(rows), len(rh))
  rh = rh[0]
  assert rh["Course"] == "BS Mechanical Engineering (Robotics minor)", rh["Course"]
  assert rh["List status"] == "Longlist" and rh["Info source"] == "Official page", (rh["List status"], rh["Info source"])
  assert rh["Approx total (MYR)"].replace(",", "").isdigit() and rh["Warnings"].strip()
  log = [json.loads(l) for l in open("data/students/toru/score_log.jsonl", encoding="utf-8") if "rose-hulman" in l.lower()]
  assert len(log) == 1 and len(log[0]["scores"]) == 8, log
  src = open("business/sales/sample_pack/build_sample_pack.py", encoding="utf-8").read()
  sample = re.findall(r'^    "([^"]+)",$', src, flags=re.M)
  by = {r["University"]: r for r in rows}
  assert len(sample) == 15 and all(by[u]["Info source"] == "Official page" and by[u]["Warnings"].strip() for u in sample)
  print("Task 6 OK: Rose-Hulman 81 A Safety ->", rh["Desirability"], rh["Tier"], rh["Admission likelihood"], "| sub-scores", log[0]["scores"])
  EOF
  ```
  Expected: `0 finding(s)`, then `Task 6 OK: ...`. `Info source` comes from the fragment's
  `source_authority`; `Not verified` there means the agent could not source a fact — read its
  "Gaps/flags" line, do not hand-stamp the cell.
- [ ] **8. Append one line to `status.md`** (the one-shot append in "Shared facts"): the old and new
  Rose-Hulman score, and that seven Northeastern cells were re-read.

**The row moves to the bottom of the CSV** (sync appends). Nothing reads row order: the sample pack
and the prototype both pick rows by university name.

**Tell Evan:** Rose-Hulman's old and new score, tier and Reach/Match/Safety on the real student's
list; any Northeastern claim an agent removed for lack of an official source.

---

## Task 7 — Source MIT report: rebuild in the 15-section layout

**Runs:** Wave 4, parallel-safe with Tasks 6 and 11. **Depends on:** Task 1 (the MIT row is current).

**Writes:** `data/students/toru/reports/massachusetts-institute-of-technology.md` and `.pdf`,
`.tmp/toru/uni_*.json`, `.tmp/toru/finalists/*.json`, `data/students/toru/master_list.csv` (step 5
only, MIT rows only), `status.md` (one appended line).

**Goal:** the source student's MIT report is a current 15-section report at USD 4.04, so the sample
shows what the pipeline produces today. This is new research, not a re-layout: no research JSON
survives from the old report, so `report-writer` researches it again. It supersedes Task 2's edit.

- [ ] **1. Back up and take the baseline.** `data/students/` has no git undo and `.tmp/` is
  disposable — do not clear `.tmp/sample_pack_fix/task7/` until Evan has read the new report.
  ```bash
  mkdir -p .tmp/sample_pack_fix/task7
  cp data/students/toru/reports/massachusetts-institute-of-technology.md data/students/toru/reports/massachusetts-institute-of-technology.pdf .tmp/sample_pack_fix/task7/
  PYTHONIOENCODING=utf-8 python tools/check_report.py --student toru --report massachusetts-institute-of-technology
  ```
  Expected: `mode legacy_university ... 0 finding(s)`. `mode report` means this task already ran.
- [ ] **2. Read** `workflows/04_university_report.md` → "Tools used", and the dispatch inputs in
  `.claude/agents/report-writer.md`. **Skip the pre-flight**: MIT is already a Finalist Evan picked,
  and its row was verified on 2026-10-12.
- [ ] **3. Dispatch one `report-writer`.** Prompt = student slug `toru`; finalist `Massachusetts
  Institute of Technology`; mode `university`. Add: "A 16-section report for this finalist already
  exists at the same path and your render will replace it — that is intended. A copy is at
  `.tmp/sample_pack_fix/task7/massachusetts-institute-of-technology.md`: use its Sources list as
  your starting set of official pages, and re-read each page rather than copying a fact from the
  old prose. Convert ringgit at `FX_TO_MYR` in `tools/shortlist_schema.py` (USD 4.04, as of
  2026-09-05) and state that rate once."
- [ ] **4. Check what came back.** Read the agent's gaps line, then:
  ```bash
  PYTHONIOENCODING=utf-8 python tools/check_report.py --student toru --report massachusetts-institute-of-technology
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import os, re
  d = "data/students/toru/reports/massachusetts-institute-of-technology"
  t = open(d + ".md", encoding="utf-8").read()
  assert len(re.findall(r"^## ", t, flags=re.M)) == 15, len(re.findall(r"^## ", t, flags=re.M))
  assert "4.04" in t and "4.70" not in t
  assert "2027-01-01" not in t and "optional-ish" not in t
  assert os.path.getmtime(d + ".pdf") >= os.path.getmtime(d + ".md") - 5, "PDF not re-rendered"
  print("Task 7 report OK")
  EOF
  ```
  Expected: `mode report ... 0 finding(s)`, then `Task 7 report OK`. If the PDF assert fails:
  `python tools/report_to_pdf.py --student toru --report massachusetts-institute-of-technology`.
- [ ] **5. Fold the finalist marker.** Not while a Task 6 session is between its steps 5 and 7.
  ```bash
  PYTHONIOENCODING=utf-8 python tools/flip_finalists.py --student toru --dry-run
  PYTHONIOENCODING=utf-8 python tools/flip_finalists.py --student toru
  PYTHONIOENCODING=utf-8 python tools/check_master_list.py --student toru
  ```
  The MIT rows are already `Finalist`, so the dry run should show no status change — at most a
  `Student life` correction. Anything else in the dry run: stop and report it.
- [ ] **6. Append one line to `status.md`:** MIT report rebuilt in the 15-section layout on <date>.

**If the report comes back with findings, or the build fails:** copy both files back from
`.tmp/sample_pack_fix/task7/`, delete `.tmp/toru/finalists/*.json`, and report. Task 9 stays
blocked; the sample keeps the 16-section report it has.

**Tell Evan:** the real student's MIT report was re-researched and rewritten. Name any fact that
differs from the old report (compare the two Snapshots), and that the old copy is in `.tmp/`.

---

## Task 8 — Source apply guide (US): Stage 8 re-run

**Runs:** Wave 5. **Depends on:** Task 7 (so the guide and the MIT report agree).

**Writes:** `data/students/toru/application_prep/us.md` and `us.pdf`,
`.tmp/toru/apply_prep_us.json`, `status.md` (one appended line),
`workflows/08_application_prep.md` (two example lines). **Read-only against `master_list.csv`.**

**Goal:** the source student's US guide is current. The one on disk was built 2026-07-26: it covers
6 universities (the list now has 9 US rows at Shortlist or Finalist — 8 Finalist, 1 Shortlist),
converts at USD 4.08, and predates two corrected facts the sample-pack README names (Columbia's
test policy; the DHS rule affecting OPT and STEM-OPT).

- [ ] **1. Precondition and backup.**
  ```bash
  mkdir -p .tmp/sample_pack_fix/task8
  cp data/students/toru/application_prep/us.md data/students/toru/application_prep/us.pdf .tmp/sample_pack_fix/task8/
  md5sum data/students/toru/master_list.csv > .tmp/sample_pack_fix/task8/master_list.md5
  PYTHONIOENCODING=utf-8 python tools/check_report.py --student toru --report massachusetts-institute-of-technology | head -1
  ```
  Expected: the first line says `mode report`. `legacy_university` means Task 7 has not run.
- [ ] **2. Run the workflow.** This is exactly `/apply-prep toru us`: read
  `workflows/08_application_prep.md`, invoke the `application-guide` skill for voice, research the
  apply mechanics of all 9 rows from official admissions and financial-aid pages, assemble
  `.tmp/toru/apply_prep_us.json`. Three things specific to this run:
  - `fx` is `{"rate": "USD 1 ≈ RM 4.04", "as_of": "2026-09-05 (the rate the list is built on)"}`.
  - Re-read Columbia's testing policy and the current OPT / STEM-OPT rule on official pages; do
    not carry either over from the old guide.
  - MIT's dates must match its row: Regular Action 2027-01-04, Early Action 2026-11-01.
  - Added after Task 7: the rebuilt MIT report states three things the guide must not
    contradict — the remaining SAT sittings and their registration closing dates, that the
    maths/science + humanities teacher-letter split is recommended and not required, and a
    health-plan charge on top of the published cost. Read them in the report's "Getting in" and
    "Costs" sections (`data/students/toru/reports/massachusetts-institute-of-technology.md`) and
    re-read each on the official page; if the page disagrees with the report, the page wins —
    say so in your reply.
  Then fix the example that would mislead the next run: `workflows/08_application_prep.md:137`
  and `:151` both show `"rate": "USD 1 ≈ RM 4.08"`. Change both to `RM 4.04` and add one clause
  saying the rate comes from `FX_TO_MYR` in `tools/shortlist_schema.py`, not from the example.
- [ ] **3. Render.**
  ```bash
  PYTHONIOENCODING=utf-8 python tools/build_application_prep.py --student toru --input .tmp/toru/apply_prep_us.json
  PYTHONIOENCODING=utf-8 python tools/apply_prep_to_pdf.py --student toru --region us
  ```
- [ ] **4. Verify.**
  ```bash
  md5sum -c .tmp/sample_pack_fix/task8/master_list.md5
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv
  t = open("data/students/toru/application_prep/us.md", encoding="utf-8").read()
  rows = list(csv.DictReader(open("data/students/toru/master_list.csv", encoding="utf-8", newline="")))
  us = sorted({r["University"] for r in rows if r["Country"] == "USA" and r["List status"] in ("Shortlist", "Finalist")})
  assert t.splitlines()[0].startswith("# "), t.splitlines()[0]
  missing = [u for u in us if u not in t]
  assert not missing, missing
  assert "RM 4.04" in t and "RM 4.08" not in t
  print("Task 8 OK:", len(us), "universities;", t.splitlines()[0])
  EOF
  ```
  Expected: `data/students/toru/master_list.csv: OK`, then `Task 8 OK: 9 universities; # Application prep — United
  States: 9 universities`. A university the guide names differently trips `missing` — check by eye
  before changing the guide.
- [ ] **5. Append one line to `status.md`:** US apply guide rebuilt on <date>, 9 universities, USD 4.04.

**Tell Evan:** the real student's US guide was rebuilt and now covers three more universities;
name any deadline or requirement that differs from the July guide.

---

## Task 9 — Rebuild the sample pack (now with the apply guide) + prototype + sweep

**Runs:** Wave 6. **Depends on:** Tasks 6, 7 and 8.

**Writes:** `business/sales/sample_pack/build_sample_pack.py`, all four sample files plus
`sample_glossary.csv`, `business/sales/sample_pack/README.md`, `prototype/_build/data.template.js`,
`prototype/data.js` (generated), `prototype/_build/smoke.js` (only if an expectation moved),
`prototype/BUILD_PLAN.md`, `data/students/toru/status.md` (one appended line).

**Goal:** every file in the sample pack is built by the script from current sources, and the
prototype shows the same figures.

**Before you start — one open decision (added 2026-10-13, after Task 8).** Princeton is a sample
row (and one of the prototype's rows). Two of its cells on the source list now contradict the
apply guide this task adds to the same pack, so a prospect reading both files would see it:

| Cell (Princeton row) | The list says | The new apply guide says |
|---|---|---|
| `How to get the scholarship` | file the PFAA + CSS Profile + tax docs | Princeton's aid form is the PFAA alone — no CSS Profile |
| `English req` | waived; the student's A-Levels qualify | the waiver needs 3 years of English-medium schooling, and the student's earlier schooling is not on file |

Checked 2026-10-13: both cells read as shown, and the row is `Finalist` / `Official page`. The
guide's side is Task 8's research (`.tmp/toru/apply_prep_us.json`), not re-read since.

- **If Evan has approved Task 8b:** fix the two cells first, the way Task 1b fixed MIT's — one
  `row-filler` in BACKFILL mode for Princeton, columns `How to get the scholarship` and
  `English req`, applied with `apply_backfill.py --student toru --country USA --overwrite` after a
  dry run that shows one row and two cells; then `check_master_list.py`. The `English req` cell
  must state the rule and say the years are to be counted, not conclude that the student
  qualifies. Five more cells on four non-sample rows have the same problems
  (`business/additionals.md` → S8); adding them to the same dispatch file is optional.
- **If he has not:** run this task as written and name the contradiction in your reply. Do not
  edit the list from this task, and do not hand-edit a sample file to hide it.

- [ ] **1. Precondition — stop if this fails.**
  ```bash
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import re
  b = "data/students/toru/"
  # "rose hulman", no hyphen: score_log.jsonl keys on a normalised course_key (Task 6's note).
  assert "rose hulman" in open(b + "score_log.jsonl", encoding="utf-8").read().lower(), "Task 6 not done"
  t = open(b + "reports/massachusetts-institute-of-technology.md", encoding="utf-8").read()
  assert len(re.findall(r"^## ", t, flags=re.M)) == 15, "Task 7 not done"
  assert "RM 4.04" in open(b + "application_prep/us.md", encoding="utf-8").read(), "Task 8 not done"
  print("preconditions OK")
  EOF
  ```
- [ ] **2. Find what must be redacted in the two new source files — before editing the script.**
  Both files are new prose, so every string in `REPORT_TEXT_REDACTIONS` is gone, and the four
  needles in `scan_for_leaks` were written for the old wording. **The income needles are figures at
  the old rate**: a report written at 4.04 states the same family income as a different USD
  number, and the scan would pass straight over it. Read `data/students/toru/profile.json` for the
  three things that identify the student — name, school or college, family income — then list
  every line that could carry one of them. The output is PII: read it, do not paste it anywhere.
  **Checked 2026-10-12: `profile.json` has no income field at all** (its two budget fields are
  empty, and so are the two in `preferences.json`). The family income the new MIT report uses
  came from `data/students/toru/status.md` — read it there, and take the report's own wording of
  it (ringgit and US dollars, every rounding) from the sweep below.
  ```bash
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import ast, re
  src = open("business/sales/sample_pack/build_sample_pack.py", encoding="utf-8").read()
  needles = ast.literal_eval(re.search(r"needles = (\[.*?\])", src, flags=re.S).group(1).replace("SOURCE_STUDENT.capitalize()", '"Toru"'))
  PATTERN = re.compile("(?i)income|household|earn|salary|your (school|college)|counsellor|" + "|".join(map(re.escape, needles)))
  for f in ("reports/massachusetts-institute-of-technology.md", "application_prep/us.md"):
      print("==", f)
      for i, line in enumerate(open("data/students/toru/" + f, encoding="utf-8"), 1):
          m = PATTERN.search(line)
          if m:
              print(f"  {i}: ...{line[max(0, m.start() - 60):m.end() + 80].strip()}")
  EOF
  ```
  Add to `PATTERN` any other identifying word `profile.json` shows. Then decide, per hit, whether
  it identifies the student (redact) or is general advice (leave).
- [ ] **3. Extend `build_sample_pack.py`.** Four edits:
  - Replace the contents of `REPORT_TEXT_REDACTIONS` with one explicit pair per identifying hit in
    the MIT report, in the style of the pairs there now (the exact source phrase → a generalized
    one). Keep them explicit strings, not regex: a missing target must stay a hard stop.
  - In `scan_for_leaks`, extend `needles` with every form the income now takes in either file
    (each currency, each rounding). Keep the four that are there.
  - Change the docstring lines that say the script "Does NOT touch sample_apply-guide_US.pdf".
  - Add the apply guide. After `build_report_pdf`, add:
    ```python
    # Same contract as REPORT_TEXT_REDACTIONS, for the apply guide's prose.
    APPLY_TEXT_REDACTIONS = [
        # one (source phrase, generalized phrase) pair per identifying hit from the PII sweep
    ]


    def build_apply_guide_pdf(region: str = "us") -> Path:
        src_md = STUDENT_DIR / "application_prep" / f"{region}.md"
        if not src_md.exists():
            sys.exit(f"ERROR: {src_md} not found.")

        text = redact(src_md.read_text(encoding="utf-8"))
        for before, after in APPLY_TEXT_REDACTIONS:
            before_r, after_r = redact(before), redact(after)
            if before_r not in text:
                sys.exit(
                    f"ERROR: expected redaction target not found in {src_md.name}:\n  {before_r!r}\n"
                    "The source guide text has likely changed — update APPLY_TEXT_REDACTIONS."
                )
            text = text.replace(before_r, after_r)

        # The guide opens with a "How to use this guide" block, so the banner goes right under the title.
        lines = text.splitlines()
        h1_at = next(i for i, ln in enumerate(lines) if ln.startswith("# "))
        text = "\n".join(lines[:h1_at + 1] + ["", BANNER, ""] + lines[h1_at + 1:])

        tmp_md = OUT_DIR / ".sample_apply_redacted.md"
        tmp_md.write_text(text, encoding="utf-8")
        try:
            out_pdf = OUT_DIR / f"sample_apply-guide_{region.upper()}.pdf"
            subprocess.run(
                [sys.executable, str(TOOLS_DIR / "md_to_pdf.py"),
                 "--type", "apply", "--input", str(tmp_md), "--output", str(out_pdf)],
                check=True,
            )
        finally:
            tmp_md.unlink(missing_ok=True)
        print(f"Wrote {out_pdf}")
        return out_pdf
    ```
    and in `main()`, after `pdf_path = build_report_pdf(args.report)`:
    ```python
    apply_path = build_apply_guide_pdf()
    scan_for_leaks(csv_path, glossary_path, pdf_path, apply_path)
    ```
    (that `scan_for_leaks` call replaces the three-argument one).
- [ ] **4. Rebuild and verify.**
  ```bash
  PYTHONIOENCODING=utf-8 python business/sales/sample_pack/build_sample_pack.py
  PYTHONIOENCODING=utf-8 python tools/check_master_list.py --file business/sales/sample_pack/sample_master_list.csv
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv
  from pypdf import PdfReader
  d = "business/sales/sample_pack/"
  rows = list(csv.DictReader(open(d + "sample_master_list.csv", encoding="utf-8", newline="")))
  assert len(rows) == 15
  assert all(r["Info source"] == "Official page" and r["Warnings"].strip() for r in rows)
  read = lambda f: " ".join(" ".join((p.extract_text() or "").split()) for p in PdfReader(d + f).pages)
  rep, app = read("sample_university-report_MIT.pdf"), read("sample_apply-guide_US.pdf")
  for name, text, never in (("report", rep, ("4.70", "1.74 million")), ("apply guide", app, ("RM 4.08",))):
      assert "anonymized demo" in text and "4.04" in text, name
      assert not [n for n in never if n in text], (name, never)
  print("Task 9 pack OK:", len(PdfReader(d + "sample_university-report_MIT.pdf").pages), "report pages,",
        len(PdfReader(d + "sample_apply-guide_US.pdf").pages), "apply-guide pages")
  EOF
  git status --short business/sales/sample_pack/
  ```
  Expected: last build line `Scan clean: zero hits for name / school / income figures.`, then
  `0 finding(s)`, then `Task 9 pack OK: N report pages, M apply-guide pages`. Then **open both PDFs
  with the Read tool and read the pages the PII sweep pointed at** — the scan only knows the
  needles it was given.
- [ ] **5. `business/sales/sample_pack/README.md`.** In the table: the MIT row becomes a 15-section
  report with the new page count (drop "built under the pre-2026-09-06 schema"); the apply-guide row
  gets its new page count. Under "How they were built": all four files now come from the script;
  delete the paragraph that says the apply guide is not covered; update "Last rebuilt".
- [ ] **6. Prototype — hand-copied MIT facts.** `prototype/_build/data.template.js` holds facts typed
  from the old report. Re-read each against the new report and change the template where they
  differ:
  - `NET_COST_PER_YEAR`, `NET_COST_TOTAL` — the Snapshot's net-cost row.
  - the international admit rate (`2.0%` in the `whyHesitate` text);
  - "Need-blind for internationals, meets 100% of need with grants and no loans, zero expected
    parent contribution";
  - "the SAT — mandatory, no test-optional route".
  Then regenerate and run the click-through:
  ```bash
  PYTHONIOENCODING=utf-8 python prototype/_build/gen.py . prototype/_build/data.template.js
  mkdir -p .tmp/proto-shots && node prototype/_build/smoke.js . .tmp/proto-shots
  ```
  Expected: `data.js: 15 rows x 35 columns, 15 report sections`, then `N/N checks passed`, exit 0
  (147/147 on 2026-10-12). A failing check that hard-codes a figure which legitimately moved
  (`money format`, `15 verified rows`) is updated to the regenerated `data.js`; any other failure
  is a real fault — fix the screen or the template, not the check.
- [ ] **7. `prototype/BUILD_PLAN.md`, decision 4.** It says the downloadable MIT PDF "is the older
  16-section layout; leave it". Rewrite as resolved on <date>: the PDF is now the 15-section layout
  the report screen shows.
- [ ] **8. Final sweep.**
  ```bash
  grep -rnE "16-section|pre-2026-09-06 schema|not\*\* covered by the script|RM 4\.08|1\.74 ?(M|million)|1,743,888" . \
    --include=*.md --include=*.html --include=*.js --include=*.py --include=*.csv \
    --exclude-dir=data --exclude-dir=.tmp --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=notes
  ```
  Expected hits, and only these: this plan file; `business/additionals.md` (L1 quotes the old
  figure as history); `business/product_review_2026-09-25.md` (a dated review that describes the
  old sample). Anything else is a miss — fix it or report it. On 2026-10-12 the misses were
  `sample_pack/README.md` (two lines), `prototype/BUILD_PLAN.md:171` and
  `workflows/08_application_prep.md` (two lines, fixed by Task 8).
  `business/sales/positioning.md:164` quotes "16 sections, 6 pages" as an example of how to phrase
  a claim; it is Evan's wording, so report it rather than edit it.
- [ ] **9. Append one line to `data/students/toru/status.md`**, then bring the file back under its
  3000-character budget by moving older history to `research_notes.md` under a "Session history —
  <date>" heading, the way Task 1b did.

**Tell Evan:** open all four sample files once himself before the next send; then run `/commit`.

---

## Task 10 — Source list: the other 14 `Not verified` rows

**Runs:** Wave 5. **Depends on:** Task 6 (both rewrite `master_list.csv`). Task 9 does not wait
for this — none of the 14 is a sample row.

**Writes:** `data/students/toru/master_list.csv`, `research_notes.md`, `glossary.csv`, `status.md`
(one appended line), `data/students/toru/plans/backfill_<date>_not_verified.md` (new),
`.tmp/toru/backfill/*.json`.

**Goal:** every row on the source list is `Official page`, or says plainly which fact could not be
sourced.

- [ ] **1. Precondition, backup, clear stale fragments.**
  ```bash
  mkdir -p .tmp/sample_pack_fix/task10 .tmp/toru/backfill_applied_task6
  cp data/students/toru/master_list.csv data/students/toru/research_notes.md .tmp/sample_pack_fix/task10/
  mv .tmp/toru/backfill/*.json .tmp/toru/backfill_applied_task6/ 2>/dev/null
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv
  rows = list(csv.DictReader(open("data/students/toru/master_list.csv", encoding="utf-8", newline="")))
  nv = [r for r in rows if r["Info source"] != "Official page"]
  assert "rose-hulman" in open("data/students/toru/score_log.jsonl", encoding="utf-8").read().lower(), "Task 6 not done"
  assert len(rows) == 43 and len(nv) == 14, (len(rows), len(nv))
  for r in nv:
      print(f'{r["Country"]:4} | {r["University"]} | {r["Course"]}')
  EOF
  ```
  Expected: 14 lines — 3 UK (Bath, Sheffield, Bristol) and 11 USA (Notre Dame, Vanderbilt, Rice,
  Northwestern, Duke, Worcester Polytechnic Institute, Case Western Reserve, Michigan-Ann Arbor,
  Dartmouth, Olin, Johns Hopkins). All are `Longlist`. Use each printed `Course` string verbatim
  in the dispatch file.
- [ ] **2. Read the repair path:** `workflows/03_discover_longlist.md` → "Backfilling an existing
  longlist", the backfill half of `.claude/agents/row-filler.md`, and
  `python tools/shortlist_schema.py --contract` for budgets and sentinels.
- [ ] **3. Write the shared context once** →
  `data/students/toru/plans/backfill_<date>_not_verified.md`, modelled on
  `plans/backfill_2026-10-12b_rhit_and_notes.md` (copy its student, sourcing and budget sections).
  Fourteen dispatches, one per row from step 1, each with the same column list:

  `Course`, `Course at a glance`, `Entry requirements`, `English req`, `Annual tuition`,
  `Total tuition`, `Est. living/yr`, `Duration (yrs)`, `Scholarship & portal`,
  `Scholarship coverage`, `Scholarship competitiveness`, `How to get the scholarship`,
  `Key deadline`, `Intake`, `Notes`, `Course URL`, `Info source`.

  Rules to state in that file (each one is a lesson from Tasks 1 and 1b):
  - `Info source` becomes `Official page` only when every researched fact came from the
    university's own pages; otherwise it stays `Not verified` and `gaps` names the fact.
  - **Check that the degree exists as named.** If it does not, write the real degree path in
    `Course` (Evan's 2026-10-12 decision on Rose-Hulman is the precedent), fix
    `Course at a glance` and `Notes` to match, and say so in `gaps`. Never drop the row.
  - A claim no official page supports is removed, not softened. Name it in `gaps`.
  - `Key deadline` is ISO-first; fees are sticker price in the local currency (USD or GBP);
    scholarships stay in their own columns.
  - Country file: `workflows/countries/usa.md` or `workflows/countries/uk.md`, named per dispatch.
- [ ] **4. Dispatch 14 `row-filler` agents in BACKFILL mode, in parallel.** Each prompt = the
  dispatch file's path, the dispatch number, the university. Nothing else. Read every reply's
  "Gaps/flags" line before applying.
- [ ] **5. Apply.** No `--country`: the batch spans two. The dry run is the gate — at most these 14
  rows, only the columns listed.
  ```bash
  PYTHONIOENCODING=utf-8 python tools/apply_backfill.py --student toru --overwrite --dry-run
  PYTHONIOENCODING=utf-8 python tools/apply_backfill.py --student toru --overwrite
  ```
- [ ] **6. Recompute totals, re-check the deadline flag, rename moved notes headings — one pass.**
  `apply_backfill.py` does not recompute. The formula was checked against all 14 rows on
  2026-10-12 and reproduced every existing total. Dry run as shown; then again with the first
  line changed to `python - --write <<'EOF'`.
  ```bash
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv, json, re, sys
  sys.path.insert(0, "tools")
  from shortlist_schema import FX_TO_MYR, feasibility_flags

  base, CUR = "data/students/toru/", {"USA": "USD", "UK": "GBP"}
  before = list(csv.DictReader(open(".tmp/sample_pack_fix/task10/master_list.csv", encoding="utf-8", newline="")))
  with open(base + "master_list.csv", encoding="utf-8", newline="") as f:
      reader = csv.DictReader(f)
      fields, rows = reader.fieldnames, list(reader)
  # apply_backfill.py never reorders rows, so the backup lines up row for row (Course may have changed)
  assert [r["University"] for r in before] == [r["University"] for r in rows], "row order moved"

  num = lambda s: float(re.search(r"\d+(?:\.\d+)?", s.replace(",", "")).group())
  calc = lambda r: round((num(r["Total tuition"]) + num(r["Est. living/yr"]) * num(r["Duration (yrs)"])) * FX_TO_MYR[CUR[r["Country"]]])
  profile = json.load(open(base + "profile.json", encoding="utf-8"))
  prefs = json.load(open(base + "preferences.json", encoding="utf-8"))
  raw = open(base + "research_notes.md", "rb").read()

  for old, r in zip(before, rows):
      if old["Info source"] == "Official page":
          continue                                    # not one of the 14
      assert str(calc(old)) == old["Approx total (MYR)"].replace(",", ""), ("formula", r["University"])
      if str(calc(r)) != r["Approx total (MYR)"].replace(",", ""):
          print(f'{r["University"]}: total {r["Approx total (MYR)"]} -> {calc(r)}')
          r["Approx total (MYR)"] = str(calc(r))
      flags = feasibility_flags({"key_deadline": r["Key deadline"]}, profile, prefs)
      want = "; ".join(flags) if flags else "None"
      if r["Key deadline"] != old["Key deadline"] and r["Warnings"] != want:
          print(f'{r["University"]}: Warnings {r["Warnings"]!r} -> {want!r}  (read before writing)')
          r["Warnings"] = want
      if r["Course"] != old["Course"]:
          a = f'## {r["University"]} - {old["Course"]}'.encode("utf-8")
          assert raw.count(a) == 1, (r["University"], raw.count(a))
          raw = raw.replace(a, f'## {r["University"]} - {r["Course"]}'.encode("utf-8"))
          print(f'{r["University"]}: COURSE RENAMED {old["Course"]!r} -> {r["Course"]!r}')

  if "--write" in sys.argv:
      with open(base + "master_list.csv", "w", encoding="utf-8", newline="") as f:
          w = csv.DictWriter(f, fieldnames=fields)
          w.writeheader(); w.writerows(rows)
      open(base + "research_notes.md", "wb").write(raw)
      print("written")
  EOF
  ```
  A `Warnings` line needs a look before writing: this pass sees only the deadline flag, so if the
  old cell held a different flag (`English short`, `Recognition risk`), keep that flag and add the
  new one by hand.
- [ ] **7. Verify.**
  ```bash
  PYTHONIOENCODING=utf-8 python tools/check_master_list.py --student toru
  PYTHONIOENCODING=utf-8 python tools/build_glossary_sheet.py --student toru
  PYTHONIOENCODING=utf-8 python - <<'EOF'
  import csv
  rows = list(csv.DictReader(open("data/students/toru/master_list.csv", encoding="utf-8", newline="")))
  assert len(rows) == 43 and not [r for r in rows if not r["Warnings"].strip()]
  left = [r["University"] for r in rows if r["Info source"] != "Official page"]
  print("Task 10 OK:", 43 - len(left), "of 43 Official page; still Not verified:", left or "none")
  EOF
  ```
  Expected: `0 finding(s)`, then `Task 10 OK: 43 of 43 Official page; still Not verified: none`. A
  row left `Not verified` is an honest result, not a failure — report which fact blocked it.
- [ ] **8. Append one line to `status.md`**, and keep the file under 3000 characters (move older
  history to `research_notes.md`).

**Not re-scored.** A row whose `Course` was renamed keeps the score it earned under the old name,
exactly as Rose-Hulman did after Task 1b. List those rows for Evan; re-scoring each is Task 6's
swap, one university at a time.

**Tell Evan:** how many of the 14 are now `Official page`; every renamed course; every removed
claim; every row whose total moved.

---

## Task 11 — Ringgit prose: the tool, then the source student's other files

**Runs:** Wave 4, parallel-safe with Tasks 6 and 7 (it never touches the MIT report or the list).
**Depends on:** nothing.

**Writes:** `tools/apply_report_fx.py` (new), `workflows/00_overview.md` (one line in the tool
list), `data/students/toru/reports/*.md` and `*.pdf` except MIT's, `recommendation.md` /
`calendar.md` if step 2 lists them, `data/students/toru/plans/fx_prose_<date>.md` (new),
`.tmp/fx_prose/toru/*.json`, `status.md` (one appended line).

**Goal:** no file delivered to the source student states a ringgit figure at an old exchange rate.

**Why a tool.** The 2026-09 refresh recomputed spreadsheets only. Reports state ringgit in free
prose, worded and rounded differently in each one (`RM 5.90 per £1`, `~S$1 = RM 3.5`, `at roughly
RM 4.70 to the dollar`), so nothing can recompute them: each figure has to be read against its
basis. An agent does that reading once per file and writes a fragment; the tool checks the
fragment and applies it in one pass. Task 2 did the same thing by hand for one report.

- [ ] **1. Create `tools/apply_report_fx.py`** with exactly this content. It was run on 2026-10-12
  against the pre-Task-2 copy of the MIT report with Task 2's pairs and reproduced Task 2's output
  byte for byte.

```python
"""
apply_report_fx.py — re-convert the ringgit prose in a delivered Markdown file, from pairs on disk.

The 2026-09 FX refresh recomputed spreadsheets only. Reports, guides and recommendations state
their ringgit figures in free prose, each worded and rounded differently, so no tool can recompute
them: someone has to read each figure against its foreign-currency basis. That reading is done once
per file (by an agent) and written as a fragment; this tool is the deterministic half — it checks
the fragment against the file and applies it in ONE pass.

Why not a chain of str.replace: with "RM 25,000 -> RM 22,000" and "RM 22,000 -> RM 19,000" in the
same file, the second replace re-converts the first one's output. One regex pass cannot.

Fragment (.tmp/fx_prose/<slug>/<name>.json):
    {"file": "data/students/<slug>/reports/<name>.md",
     "currency": "USD", "old_rate": 4.70,
     "pairs": [{"old": "~RM 313,600", "new": "~RM 269,500", "count": 1, "basis": "USD 66,720"},
               {"old": "(~RM 4.70 per USD)", "new": "(~RM 4.04 per USD)", "count": 1, "kind": "rate"}],
     "left_alone": [{"text": "RM 0", "count": 2, "why": "zero"}]}
A pair may carry its own "currency" + "old_rate" when one file converts two currencies.

Refuses (and writes nothing for that fragment) when: an `old` / `text` does not occur exactly
`count` times; a ringgit figure in the file is covered by neither list; a `new` still holds the old
rate. Warns when new/old is more than 4% away from the rate ratio — rounding is allowed, a slipped
digit is not. Backs the file up beside the fragment before the first write.

Usage:
    python tools/apply_report_fx.py --fragment .tmp/fx_prose/<slug>/<name>.json --dry-run
    python tools/apply_report_fx.py --dir .tmp/fx_prose/<slug>            # every fragment in it
    python tools/apply_report_fx.py --inventory <slug>                    # which files state which rate
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import FX_TO_MYR  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
# A ringgit figure: "RM 313,600", "RM3.19", "~RM 1.74 million", "MYR 84k". The "~" may sit either side.
RM_FIGURE = re.compile(r"(?:RM|MYR)\s?~?\d(?:[\d,]*\d)?(?:\.\d+)?(?:\s?(?:million|bn|[mMkK])\b)?")
SCALE = {"million": 1e6, "m": 1e6, "bn": 1e9, "k": 1e3}
RATIO_TOLERANCE = 0.04
CURRENCY_WORD = r"(?:USD|US\$|GBP|£|AUD|A\$|SGD|S\$|CNY|RMB|EUR|€|JPY|HKD|CAD|TWD|dollar|pound|yuan|euro)"
RATE_LINE = re.compile(
    r"(?i)(exchange rate|\bFX\b|conver(?:t|sion)[^.|\n]{0,40}(?:rate|at)"
    r"|RM\s?\d\.\d{1,3}\b(?!\s*(?:million|m\b|k\b|bn))|\b\d\.\d{1,3}\s*(?:MYR|RM)\b|per\s+" + CURRENCY_WORD + r"|=\s*RM)")
NOT_DELIVERED = {"status.md", "research_notes.md", "plan.md", "student_life_research.md"}


def _number(text):
    """The first ringgit figure in `text` as a float, or None."""
    m = RM_FIGURE.search(text)
    if not m:
        return None
    n = re.search(r"\d(?:[\d,]*\d)?(?:\.\d+)?", m.group())
    unit = re.search(r"(million|bn|[mMkK])$", m.group())
    return float(n.group().replace(",", "")) * (SCALE[unit.group().lower()] if unit else 1)


def apply_fragment(path, dry_run):
    """Validate one fragment and apply it. Returns a list of error strings ([] = applied)."""
    frag = json.loads(path.read_text(encoding="utf-8"))
    target = REPO_ROOT / frag["file"]
    text = target.read_bytes().decode("utf-8")
    pairs, left = frag.get("pairs", []), frag.get("left_alone", [])
    errors, warnings = [], []

    # Longest first, so "~RM 436,000" wins over "RM 436,000" when both are listed.
    targets = {p["old"]: p for p in pairs}
    targets.update({e["text"]: e for e in left if e["text"] not in targets})
    if not targets:
        return [f"{path.name}: no pairs and nothing left alone"]
    pattern = re.compile("|".join(re.escape(t) for t in sorted(targets, key=len, reverse=True)))

    seen, spans = {}, []
    for m in pattern.finditer(text):
        seen[m.group()] = seen.get(m.group(), 0) + 1
        spans.append(m.span())
    for t, entry in targets.items():
        if seen.get(t, 0) != entry["count"]:
            errors.append(f"{t!r}: expected {entry['count']}, found {seen.get(t, 0)}")
    for m in RM_FIGURE.finditer(text):
        if not any(s <= m.start() and m.end() <= e for s, e in spans):
            line = text.count("\n", 0, m.start()) + 1
            errors.append(f"line {line}: {m.group()!r} is in neither pairs nor left_alone")

    for p in pairs:
        cur, old_rate = p.get("currency", frag["currency"]), p.get("old_rate", frag["old_rate"])
        if p.get("kind") == "rate":
            if str(old_rate) in p["new"] or f"{old_rate:.2f}" in p["new"]:
                errors.append(f"{p['old']!r}: the new rate statement still holds {old_rate}")
            continue
        a, b = _number(p["old"]), _number(p["new"])
        if a and b and abs(b / a - FX_TO_MYR[cur] / old_rate) > RATIO_TOLERANCE:
            warnings.append(f"{p['old']!r} -> {p['new']!r}: ratio {b / a:.3f}, rate ratio "
                            f"{FX_TO_MYR[cur] / old_rate:.3f} ({p.get('basis', 'no basis given')})")

    for w in warnings:
        print(f"  WARN {w}")
    if errors:
        return [f"{path.name}: {e}" for e in errors]

    new_text = pattern.sub(lambda m: targets[m.group()].get("new", m.group()), text)
    replaced = sum(p["count"] for p in pairs)
    print(f"  {'would replace' if dry_run else 'replaced'} {replaced} figure(s), "
          f"left {sum(e['count'] for e in left)} alone: {frag['file']}")
    if not dry_run:
        backup = path.parent / "backup" / target.name
        backup.parent.mkdir(exist_ok=True)
        if not backup.exists():
            shutil.copy2(target, backup)
        target.write_bytes(new_text.encode("utf-8"))
    return []


def inventory(slug):
    """Print the lines that state an exchange rate, per delivered file. A reading aid, not a
    verdict: the wording varies too much to classify by pattern, so a person sorts stale from
    current (and skips noise like "converted stair landings")."""
    base = REPO_ROOT / "data" / "students" / slug
    print("current:", {k: v for k, v in FX_TO_MYR.items() if k not in ("MYR", "RMB")})
    files = list(base.glob("reports/*.md")) + list(base.glob("*.md")) + list(base.glob("application_prep/*.md"))
    for f in sorted(files):
        name = f.relative_to(base).as_posix()
        text = f.read_text(encoding="utf-8")
        figures = len(RM_FIGURE.findall(text))
        if name in NOT_DELIVERED or not figures:
            continue
        hits = [(i, line) for i, line in enumerate(text.splitlines(), 1) if RATE_LINE.search(line)]
        print(f"## {name}  ringgit figures={figures}  rate lines={len(hits)}")
        for i, line in hits[:4]:
            m = RATE_LINE.search(line)
            print(f"   {i}: ...{line[max(0, m.start() - 60):m.end() + 50]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fragment", help="One fragment JSON.")
    group.add_argument("--dir", help="A folder of fragment JSONs (each applied independently).")
    group.add_argument("--inventory", metavar="SLUG", help="List the rate statements in a student's files.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and report; write nothing.")
    args = parser.parse_args()
    if args.inventory:
        inventory(args.inventory)
        return

    paths = [Path(args.fragment)] if args.fragment else sorted(Path(args.dir).glob("*.json"))
    failed = []
    for path in paths:
        print(path.name)
        failed += apply_fragment(path, args.dry_run)
    for line in failed:
        print(f"REFUSED {line}")
    print(f"{len(paths)} fragment(s), {len({f.split(':')[0] for f in failed})} refused")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
```

  Then prove it on a throwaway file — a chained pair must not double-convert, and a fragment with a
  wrong count or an unlisted figure must be refused:
  ```bash
  mkdir -p .tmp/fx_prose/_selftest
  printf 'x RM 25,000 y RM 22,000 z RM 500\n' > .tmp/fx_prose/_selftest/t.md
  cat > .tmp/fx_prose/_selftest/good.json <<'EOF'
  {"file": ".tmp/fx_prose/_selftest/t.md", "currency": "USD", "old_rate": 4.70,
   "pairs": [{"old": "RM 25,000", "new": "RM 22,000", "count": 1}, {"old": "RM 22,000", "new": "RM 19,000", "count": 1}],
   "left_alone": [{"text": "RM 500", "count": 1, "why": "test"}]}
  EOF
  PYTHONIOENCODING=utf-8 python tools/apply_report_fx.py --fragment .tmp/fx_prose/_selftest/good.json && cat .tmp/fx_prose/_selftest/t.md
  sed -i 's/"left_alone".*/"left_alone": []}/' .tmp/fx_prose/_selftest/good.json
  PYTHONIOENCODING=utf-8 python tools/apply_report_fx.py --fragment .tmp/fx_prose/_selftest/good.json --dry-run; echo "exit=$?"
  rm -rf .tmp/fx_prose/_selftest
  ```
  Expected: `replaced 2 figure(s), left 1 alone`, the file reads `x RM 22,000 y RM 19,000 z RM 500`
  (not `RM 19,000` twice), then three `REFUSED` lines — `RM 25,000` found 0 times, `RM 19,000` and
  `RM 500` in neither list — and `exit=1`. Measured 2026-10-12.
  Add `apply_report_fx.py` to the tool list in `workflows/00_overview.md` → "Tools (deterministic
  layer)" with a one-clause description.
- [ ] **2. Inventory.** Print every exchange-rate statement in the student's delivered files:
  ```bash
  PYTHONIOENCODING=utf-8 python tools/apply_report_fx.py --inventory toru
  ```
  It prints the current rates, then per file the number of ringgit figures and the lines that
  state a rate. It is a reading aid, not a verdict — some lines are noise ("converted stair
  landings", "offer rate").
  Sort every file into one of three groups. Measured 2026-10-12 for this student's 16 reports:
  - **Old rate stated — 11:** Columbia, Harvard, Princeton, Stanford, Yale (USD 4.70);
    Heriot-Watt, Imperial, Cambridge, Oxford (GBP 5.90); NUS (SGD 3.50); Tsinghua (CNY 0.65).
  - **No rate stated — 2:** Brown, Cornell. The agent works the rate out from a figure and its basis.
  - **Current — 3, skip:** both Zhejiang reports (CNY 0.60) and MIT (Tasks 2 and 7 own it).

  `recommendation.md` and `calendar.md` carry one ringgit figure each — do those two by hand as
  fragments in step 5, no dispatch.
- [ ] **3. Write the shared context once** → `data/students/toru/plans/fx_prose_<date>.md`. One
  dispatch per file in the first two groups: dispatch number, file path, currency, old rate (or
  "not stated — infer"). Then these rules, verbatim:
  - Read `tools/apply_report_fx.py`'s docstring for the fragment shape. Write exactly one file,
    `.tmp/fx_prose/toru/<report file name without .md>.json`, and nothing else.
  - The current rate is `FX_TO_MYR[<currency>]` in `tools/shortlist_schema.py`.
  - For **every** ringgit figure in the file: find its foreign-currency basis (same sentence, same
    table row, or the cost table). `new` = basis × current rate, rounded the way `old` was
    rounded. Put the basis in `basis`. If the file gives no basis, scale `old` by current ÷ old
    rate, same rounding, and write `"basis": "scaled — no basis in file"`.
  - A figure that was never converted goes in `left_alone` with a reason: family income, a budget
    ceiling, a Malaysian salary or fee, a sponsor's award stated in ringgit, a zero.
  - The rate statement itself is a pair with `"kind": "rate"`.
  - `old` must be an exact substring and `count` its exact number of occurrences. When the bare
    figure appears twice with different meanings, widen `old` with the characters around it.
  - A sentence whose **conclusion** depends on the old figure — "blows the budget", "RM X short",
    "more than N times" — is not a figure swap. Leave it out of `pairs` if the conclusion changes,
    and add it to a top-level `"flags": [{"line": N, "text": "...", "why": "..."}]` list. The tool
    ignores `flags`; a person reads them.
  - If the file turns out to be at the current rate already (within 1%), write `"pairs": []`,
    every figure in `left_alone` with `"why": "already current"`.
  - Run `python tools/apply_report_fx.py --fragment <your file> --dry-run` and fix the fragment
    until it is not refused.
  - Reply in two lines: the fragment path; then the number of flags and warnings. Do not quote
    the student's income, grades or school in the reply.
- [ ] **4. Dispatch 13 `general-purpose` agents in parallel** (model `sonnet`). Each prompt = the
  shared file's path and the dispatch number. Nothing else.
- [ ] **5. Apply.** Add the two hand-written fragments for `recommendation.md` and `calendar.md` if
  step 2 showed their figure is converted. Take the baseline first.
  ```bash
  PYTHONIOENCODING=utf-8 python tools/check_report.py --student toru --all > .tmp/fx_prose/toru/check_before.txt
  PYTHONIOENCODING=utf-8 python tools/apply_report_fx.py --dir .tmp/fx_prose/toru --dry-run
  ```
  Read every `WARN` line (a ratio more than 4% off the rate ratio — rounding or a slip?) and every
  fragment's `flags`. Fix a fragment by editing its JSON, not the report. Then:
  ```bash
  PYTHONIOENCODING=utf-8 python tools/apply_report_fx.py --dir .tmp/fx_prose/toru
  PYTHONIOENCODING=utf-8 python tools/report_to_pdf.py --student toru --all
  PYTHONIOENCODING=utf-8 python tools/check_report.py --student toru --all > .tmp/fx_prose/toru/check_after.txt
  strip() { grep -h "finding(s)" "$1" | sed -E 's/, [0-9]+ chars//'; }
  diff <(strip .tmp/fx_prose/toru/check_before.txt) <(strip .tmp/fx_prose/toru/check_after.txt) && echo "findings unchanged"
  ```
  Expected: `N fragment(s), 0 refused`, then `findings unchanged` (the character counts move, the
  findings must not). Each
  original is kept in `.tmp/fx_prose/toru/backup/`.
  `report_to_pdf.py --all` also re-renders the MIT report: if a Task 7 session is open, convert
  the changed reports one at a time with `--report <slug>` instead.
- [ ] **6. Verify.** Re-run the step 2 inventory. No stated rate may differ from `current:` by more
  than 1%. Then work the `flags`: rewrite each flagged sentence by hand so its conclusion matches
  the new figures, or bring it to Evan if the conclusion is a recommendation.
- [ ] **7. Append one line to `status.md`:** which files were re-converted on <date>, and how many
  flagged sentences were rewritten.

**Tell Evan:** the real student's other reports changed — ringgit figures only, all lower, since
every one of these currencies bought more ringgit at the old rate. Quote every flagged sentence
whose conclusion changed, before and after.

---

## Task 12 — Ringgit prose: the other students' reports

**Runs:** Wave 5. **Depends on:** Task 11 (the tool exists and the method is proven).

**Writes:** `data/students/<slug>/reports/*.md` and `*.pdf` for every other student with a stale
report, one appended line in each of those students' `status.md`, `notes/fx_prose_<date>.md`
(new; `notes/` is gitignored because it names real students), `.tmp/fx_prose/<slug>/*.json`.

**Goal:** no delivered report on disk states a ringgit figure at an old exchange rate.

**PII.** Student slugs are real names. They go in `notes/` and `.tmp/`, never in this file, a
commit message, or anything under `business/` or `prototype/`.

- [ ] **1. Precondition and inventory.** `ls tools/apply_report_fx.py` must succeed (Task 11
  creates it). Then, once per student folder:
  ```bash
  for s in $(ls data/students | grep -v '^toru$'); do echo "#### $s"; PYTHONIOENCODING=utf-8 python tools/apply_report_fx.py --inventory "$s"; done
  ```
  It prints the current rates, then per file the lines that state a rate (a reading aid — some
  lines are noise). Sort every report into three groups. Measured 2026-10-12 across the other
  students' 27 reports:
  - **Old rate stated — 14 reports, 8 students:** GBP at 5.90 (4), USD at 4.70 (4), USD at 4.4
    (1), SGD at 3.5 or 3.3 (4), AUD at 3.10 (1).
  - **No rate stated — 6 reports, 4 students.** The agent infers the rate.
  - **Current or within 1% — 7, skip:** GBP 5.47 (2), SGD 3.19 (1), USD 4.04 (1), AUD 2.90 (1),
    CAD 2.90 (2).
  A different count means reports were added or rebuilt since — trust the inventory, not this list.
- [ ] **2. Write the shared context once** → `notes/fx_prose_<date>.md`: one dispatch per report in
  the first two groups (number, file path, currency, old rate or "not stated — infer"), then the
  rules block copied from `data/students/toru/plans/fx_prose_<date>.md` with the fragment folder
  changed to `.tmp/fx_prose/<that report's student slug>/`.
- [ ] **3. Dispatch one `general-purpose` agent per report, in parallel** (model `sonnet`; 20 on the
  2026-10-12 count). Each prompt = the shared file's path and the dispatch number. Nothing else.
- [ ] **4. Apply, one student folder at a time.**
  ```bash
  for d in .tmp/fx_prose/*/; do s=$(basename "$d"); [ "$s" = toru ] && continue
    PYTHONIOENCODING=utf-8 python tools/check_report.py --student "$s" --all > "$d/check_before.txt"
    PYTHONIOENCODING=utf-8 python tools/apply_report_fx.py --dir "$d" --dry-run
  done
  ```
  Read every `WARN` and every fragment's `flags` as in Task 11 step 5. Then the same loop with the
  dry run replaced by:
  ```bash
    PYTHONIOENCODING=utf-8 python tools/apply_report_fx.py --dir "$d" \
      && PYTHONIOENCODING=utf-8 python tools/report_to_pdf.py --student "$s" --all \
      && PYTHONIOENCODING=utf-8 python tools/check_report.py --student "$s" --all > "$d/check_after.txt"
    strip() { grep -h "finding(s)" "$1" | sed -E 's/, [0-9]+ chars//'; }
    diff <(strip "$d/check_before.txt") <(strip "$d/check_after.txt") && echo "$s: findings unchanged"
  ```
  Expected per student: `0 refused`, then `<slug>: findings unchanged`.
- [ ] **5. Verify.** Re-run the step 1 inventory: no stated rate differs from `current:` by more
  than 1%. Work the `flags` by hand as in Task 11 step 6.
- [ ] **6. Append one dated line to each affected student's `status.md`:** report ringgit figures
  re-converted at the 2026-09-05 rates; which reports.

**Tell Evan:** which students' reports changed, so he can decide who gets a corrected copy — these
are delivered work. For each, the largest single change in ringgit, and every flagged sentence
whose conclusion changed.

---

## Not in this plan

- **The 16-section layout of every other report.** Task 7 rebuilds the sample's MIT report only.
  Every other 16-section report on disk is delivered work that `check_report.py` still accepts as
  a legacy layout; converting one is a `report-writer` re-run — new research, one Opus dispatch
  per report.
- **Re-scoring a row whose course Task 10 renames.** Same swap as Task 6, one university at a time,
  once Evan has seen which rows changed.
- **Reports within 1% of the current rate** (AUD 2.90 against 2.91, CAD 2.90 against 2.93). The
  difference is smaller than the rounding in the figures.
- **The legacy backfill of the other students' lists.** Task 10 clears the source student's 14
  rows. The other older lists still owe the same repair
  (`workflows/03_discover_longlist.md` → "Backfilling an existing longlist").
- **`business/sales/positioning.md:164`** ("16 sections, 6 pages" as a phrasing example). Evan's
  wording; Task 9 reports it.
- **Tasks 10 and 12, parked 2026-10-12**, and everything else this round turned up that Tasks 8
  and 9 do not need: `business/additionals.md` → "Sample pack fix round" (S1-S7, P1, P2). That
  file's "Start here" section is the single index of what is open.
