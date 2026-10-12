# Sample pack fix plan — stale FX + stale sample rows

Written 2026-10-12. Source of the findings: `business/additionals.md` → L1, plus a read of the
sample PDF, the sample CSV, the prototype and the poster in the session that wrote this file.

## How to run this file

- **One task per fresh session.** Read "Shared facts" plus your own task. Nothing else in this file.
- **Do not enter plan mode and do not re-plan.** The task is the plan. Execute it.
- **Do not commit, stage or push.** Parallel sessions share one git index. Evan runs `/commit` once
  after Task 5.
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
```

Wave 1 tasks write disjoint files, so they are safe side by side. Task 3 depends on nothing and may
run at any point.

### Status

- [x] Task 1 — source list rows
  - Run 2026-10-12. **Do not re-run.** MIT + Northeastern applied, `Warnings` pass written,
    `check_master_list.py` clean. It hit its stop condition on Rose-Hulman (no robotics major
    exists, minor only): that row was left untouched and `Not verified`, so step 8 fails on that
    one assert. Evan's call: fix the row — carried by Task 1b. Detail: the student's `status.md`.
- [ ] Task 1b — Rose-Hulman course fix + the two unchecked rows
- [x] Task 2 — source MIT report (2026-10-12; script prints `replaced 18 figures`, not 19 — the
  counts in `PAIRS` sum to 18, all 14 asserts passed, diffed against the backup)
- [x] Task 3 — poster (2026-10-12; re-render also moved the page-2 contact line from WhatsApp to
  Email — the HTML has said Email since 3caedbc, the committed PDF was never re-rendered after it)
- [ ] Task 4 — rebuild sample pack
- [ ] Task 5 — prototype + final sweep

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
    15 rows are `Info source = Not verified`, one of them a sample row — Rose-Hulman, whose listed
    degree does not exist (Task 1b).
  - `data/students/toru/reports/massachusetts-institute-of-technology.md`: prose still at 4.70. No
    research JSON survives, so the `.md` is the source — edit it directly.
- **`data/students/` is gitignored — no git undo.** Back up before writing:
  `mkdir -p .tmp/sample_pack_fix` and copy the file there first.
- **PII.** This file is tracked. Never paste the student's grades, income or school into it, into a
  commit message, or into anything under `business/` or `prototype/`.
- Console output mangles em-dashes on this machine. Prefix Python runs with
  `PYTHONIOENCODING=utf-8`. A `�` in terminal output is the console, not the file.

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

## Not in this plan

- **`sample_apply-guide_US.pdf`.** Its ringgit figures use about 4.08 and are within 1% of current,
  so the FX fault does not apply. It is stale for other reasons the sample-pack README already
  lists (two facts corrected after it was built). Fixing it is a Stage 8 run for the source student
  (`/apply-prep toru us`) followed by a manual `md_to_pdf.py --type apply` render.
- **Old-rate prose in other students' reports.** 17 of the 43 report files under `data/students/`
  state an old rate, across 7 students; 9 of them are the source student's other reports. These are
  delivered work, not sales assets. The 2026-09 recompute covered spreadsheets only.
- **The sample MIT report's 16-section layout.** New reports are 15-section. Converting it means
  re-running `report-writer` on MIT, which is research, not a rebuild.
- **The other 14 `Not verified` rows on the source list.** Not sample rows. Part of the legacy
  backfill already owed for the older lists.
- **Re-scoring the Rose-Hulman row.** Task 1b changes its course from a dedicated robotics degree
  to Mechanical Engineering + a Robotics minor but leaves `Desirability` 81 / `Tier` A / `Admission
  likelihood` Safety as they were. A true re-score needs the eight sub-scores, which no file
  holds: it is a discovery-mode `row-filler` run on that one university, then
  `merge_candidates.py` + `sync_shortlist.py` (which appends a new row under the new course name)
  and removing the old row by hand. That shows in the sample, so it is worth doing before the
  sample is next relied on for its scores — but it is research, not a rebuild.
- **The descriptive cells on the other re-verified rows.** `Info source = Official page` was earned
  on the hard-fact columns in Task 1's list. `Student life`, `Overall rank`, `Subject rank`,
  `Work rights after graduating`, `Recognised in Malaysia?`, `Money to show (visa)` and
  `How to apply` on the Northeastern row were not re-read (Task 1b covers only its `Notes` and
  `Course at a glance`).
