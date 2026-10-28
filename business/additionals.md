# Additionals — the backlog of known problems not yet fixed

*One entry per problem, each with a suggested fix. **Only open entries live here.** When one is
done, delete it and its line in the steps below, and write one line in `plans/build-log.md`.
History: the full file up to 2026-10-28 (every closed entry, the old lane and round plans) is in
git: `git show 10b847c:business/additionals.md`. Decisions are in `decisions/log.md`.*

*Adding an entry: the next number is **R26**. Say whether it is **urgent**, and whether it is a
**tool gap** (the system will keep making the mistake) or **stale data** (old files only). Plain
English, no student named, no grades, income or school. Then add it to a step below.*

---

## Start here

### Steps — one session each. Type: "Execute step N of `business/additionals.md`"

**Before the 10 Nov paid lists and booth** (allowed under the freeze: a customer would see them)

| Step | Entries | Files it writes | Waits for | Size |
|---|---|---|---|---|
| **2b** | R23, then R25 | the source student's `master_list.csv`, `research_notes.md`, `score_log.jsonl`; `business/sales/sample_pack/`; `prototype/data.js`; `workflows/countries/uk.md` (R25) | nothing | Small |

**After 10 Nov** (the old students' lists, then the bigger system changes)

| Step | Entries | Files it writes | Waits for | Size |
|---|---|---|---|---|
| **3** | R19 | `tools/apply_backfill.py`, `workflows/03_discover_longlist.md`, `.claude/agents/row-filler.md` | nothing. Not while a backfill is running | Small |
| **4** | I9, then L2 (the 22 rows) | other students' `profile.json`, `master_list.csv`, `research_notes.md` | step 3 | Large. One student per session if the 22 rows span many |
| **5** | R16 lookups (parts a, b, c) | `notes/r16_*`, `.tmp/r16/` | nothing. Can run beside step 4 | Large: about 45 agents plus browser lookups. Split a/b/c across sessions |
| **6** | Per student: R16 apply, R17, R21 (all three touch the same list, so do them together) | that student's `master_list.csv`, `research_notes.md`, `status.md` | steps 3 and 5 | Medium per student. Never the same student as step 4 |
| **7** | L5 (plan first, in plan mode) | `tools/shortlist_schema.py`, `tools/sync_shortlist.py`, `tools/check_master_list.py`, the row-filler sheet, `workflows/03_discover_longlist.md` | an approved plan | Medium to large. Not alongside step 4 or 6 |
| **8** | R20 (plan first) | to be planned | nothing | Large, a new build |

**Not a session** (Evan's own, a reply someone owes, or a measurement): I3, I4, R9, R11, N1 / U4 / V2, V3.

### Rules for every step session

1. Read this section, then only the entries your step names. The "Suggested fix" is the plan.
2. Stay inside the files the step lists; anything else goes in the hand-back.
3. Copy a student file to `.tmp/` before a program rewrites it. Run `apply_backfill.py` as a dry
   run first. Never run the calendar program with `--allow-shrink`.
4. **The source student is finished** (Evan, 2026-10-28). Their list is touched only for the
   sample pack (SP1, R23), never for their own sake. Sample pack facts are fixed in that list and
   rebuilt with `build_sample_pack.py`, never typed into `sample_master_list.csv`.
5. If another session is open on this file, do not edit it: end with a hand-back (done, not done,
   new findings). Otherwise delete the finished entries here yourself.

### Closed on 2026-10-28 without a fix (Evan's calls, so nobody re-raises them)

- **D2, P2's follow-up:** no decision-stage runs and no corrected reports for the free testers.
  Fix the system first; send something to a tester only when Evan wants them to try it.
- **D5, R2, R14, R15, and the source student's share of R16, R17, R18 and R21:** that student is
  finished. Only what the sample pack shows still counts (SP1).
- **S4's open question** (who looks foreign degrees up on the Malaysian register): stays the
  default, a session in Chrome (`workflows/sources.md`).

---

## Before 10 Nov

#### R23. Two US demo rows carry a grade label against a bar that doesn't exist

- **Added 2026-10-28** (SP1 run). **Stale data a customer sees** (sample pack + demo website), so
  before 10 Nov.
- **What is true:** Rose-Hulman ("Above", Safety) and Northeastern ("Meets", Match) both say "no
  minimum grades published" in `Entry requirements`, so `Grades vs entry bar` should read "Not
  published" like the other US rows. They have no hand-set admission label, so `not_published`
  alone blanks `Admission likelihood` (the check fails). Northeastern as "Match" also looks wrong:
  it is a very selective school (admit rate not yet read on its own page).
- **Suggested fix:** read each one's admit rate on its official page (Common Data Set or
  admissions facts). Set `entry_margin` = `not_published` and an `admission_likelihood` override
  with a short reason, the same way as SP1 (`grade_fit_label` / `classify_admission`, one
  `score_log.jsonl` line each). Then rebuild the sample pack (with `.venv`'s Python: it has `pypdf`
  for the privacy scan) and the prototype
  (`gen.py`), run `check_master_list.py --student <source>` and `node prototype/_build/smoke.js`.

#### R25. `uk.md` calls Cambridge's GBP 46,872 a 2026/27 fee

- **Added 2026-10-28** (SP1 run). **Stale note, not urgent.** Cambridge's international fees page
  (read 2026-10-28) gives GBP 46,872 for **2027 entry**, Group 4 (incl. Engineering).
- **Suggested fix:** in the Cambridge College-fee note in `workflows/countries/uk.md`, change
  "(2026/27)" to "(2027 entry)".

---

## After 10 Nov: the old students' lists

#### R19. The backfill tool leaves its applied files where the next run will apply them again

- **Tool gap.** Not urgent while each session remembers to move the files by hand, but it must be
  fixed before steps 4 and 6, which run many backfills.
- **What is true:** `tools/apply_backfill.py` applies every file in `.tmp/<slug>/backfill/` and
  leaves them there. A second run writes them over the list again and copies their notes into
  `research_notes.md` twice. Also seen: 7 of 18 research agents stalled and wrote nothing; the
  ones told to "write the file early and update it as you go" all finished.
- **Suggested fix:** after a successful write, the tool moves the files it applied to
  `.tmp/<slug>/backfill_applied_<date>/`. Add one line to `workflows/03_discover_longlist.md` →
  "Backfilling an existing longlist", and to `.claude/agents/row-filler.md`: write the fragment
  early and update it as you go.

#### I9. Three student records carry the wrong checklist of professional bodies

- **Stale data** (left over from the old keyword method; today's rule matches the course chosen
  in the form, [tools/ingest_form_csv.py](../tools/ingest_form_csv.py) `COURSE_ACCREDITATION_MAP`).
  Do it before L2, because L2 looks up recognition against this list.
- **Where:** `recognition_targets` in `profile.json` (the bodies that decide whether a degree is
  recognised in Malaysia).
  - A Software Engineering student carries the accounting bodies (MIA, ACCA). Confirmed. Their
    recognition cells would check the wrong body.
  - A Computer Science and a Data Science student carry MQA alone; today's rule gives those
    courses an empty list. Harmless.
  - A Data Science student who also typed "Mechanical engineering" has an empty list. Borderline.
- **Suggested fix:** set the Software Engineering student's list to what today's rule gives that
  course. Optionally clear the two MQA-only lists. Ask the borderline student whether mechanical
  engineering is a real option (then it needs the engineering bodies).

#### L2. 212 rows on the other students' lists are still "Not verified"

- **Decided 2026-10-28 (Evan): the 22 Shortlist and Finalist rows first**, the ones students are
  deciding on. The other 190 wait.
- **Stale data.** Eight lists started before the 2026-07-29 rule (every row from official pages)
  hold almost all of them; lists built since are verified (209 of 213 rows).
- **Suggested fix:** `apply_backfill.py` (re-researches only a row's unchecked cells) over the 22
  rows, one student per session if they spread. Lessons from the source student's repair (P1):
  a renamed course must be re-scored, one university at a time (search the score log by the exact
  new course key); re-read the `Recognised in Malaysia?` cell too (R16); move applied files (R19).
- **Pairs with L5:** "Not found on official page" is only honest after this research has looked.

#### R16. The recognition cells on US rows rest on accreditation nobody re-checked

- **Stale data on a hard gate** (recognition back home decides a regulated profession). Decided
  2026-10-20: check every student. Now five students (the source student is dropped). Scope per
  student is in the gitignored `notes/r16_scope.md`; skip universities that appear only on the
  source student's list.
- **What is true:** the US rows say "ABET-accredited" from longlist time in July. Michigan's
  robotics degree turned out not to be (ABET is the US engineering accreditor; it is the route to
  the Board of Engineers Malaysia through the Washington Accord). Most cells also still say
  "confirm MQA equivalence", though the register can now be read in Chrome.
- **Suggested fix:**
  - **a, b (ABET lookup):** write `notes/r16_abet_dispatch.md` (rules + one dispatch per
    university, naming every degree from the scope file). One `general-purpose` agent per
    university, in parallel, split into two sessions. Each reads each degree on ABET's own search
    (`https://amspub.abet.org/`; Firecrawl if it will not load) and writes
    `.tmp/r16/abet/<uni-slug>.json`: accredited yes or no, the name as ABET lists it, date, source.
    Merge into `notes/r16_abet_lookup.csv` with a ready `Recognised in Malaysia?` cell per degree
    (160 characters at most; "Not accredited" says there is no route to BEM registration).
  - **c (Malaysian register):** in Chrome, the universities behind a Finalist or Shortlist row
    (method in `workflows/sources.md`) into `notes/r16_esisraf_lookup.csv`: listed or not, which
    broad-field rows, date.
  - **Apply (step 6):** per student, a script builds one-cell fragments from the lookups, then
    `apply_backfill.py --overwrite` (dry run first), `check_master_list.py`, one line in
    `status.md`. A degree that is not accredited also gets "Recognition risk" in `Warnings` by
    hand, listed in the hand-back for Evan.
- **Not in scope yet:** 174 non-US rows that claim accreditation (a later decision).

#### R17. Older US rows say the grades are "Well above" a bar the university does not publish

- **Stale data.** US universities publish no A-Level bar. The scoring program has had a "Not
  published" value (`entry_margin` = `not_published`) since 2026-07-28; rows scored before that
  compared grades to a guessed bar. `Admission likelihood` already says "Reach", so the ranking
  does not hide how hard these are.
- **Where:** other students' US rows scored before 2026-07-28. Not counted yet. (The sample
  pack's five were fixed on 2026-10-28 as SP1; its last two are R23.)
- **Suggested fix:** in step 6, per student: count them, then set `not_published` through the
  scoring program's label function (never typed), with a line in `score_log.jsonl`.

#### R21. About 40 English-test cells claim a waiver for A-Levels or English-medium schooling

- **Stale data. Not urgent unless one of these lists is about to be re-sent.** The tool gap that
  made them was R22 (fixed 2026-10-28). Four cells were fixed on 2026-10-27 (UCL, Imperial, KCL; Evan said yes).
- **Where:** about 40 `English req` cells on 11 students' lists. Some state a university's real
  rule (Columbia, Northeastern); many are the old guess ("likely waived for English-medium
  A-Levels — confirm", 24 rows on one student, US and Australia). Shortlist and Finalist rows
  first: about 15, across four students.
- **What is true** (official pages, 2026-10-27): UCL and KCL waive only for nationals of, or study
  in, listed countries; Malaysia is not listed. Imperial names no school-level waiver; it accepts
  SPM English 1119 grade A, IGCSE First Language English B/6, or A-Level English Language C.
  Australia does not waive on A-Levels.
- **Find them:** `English req` contains "waive" and ("A-Level" or "English-medium").
- **Suggested fix:** in step 6, one-cell `English req` fragments through `apply_backfill.py
  --overwrite` (dry run first), stating the test bar and the accepted English grades, then
  `check_master_list.py`. Needs Evan's yes per student (it rewrites student files).

---

## After 10 Nov: system changes

#### L5. A row is labelled as a whole, so one missing fact shows "Not verified" on everything

- **Added 2026-10-27 (Evan).** Not a fault; a change to what the spreadsheet promises. Evan wants
  every fact shown with its source, or "Not found on official page" where it was looked for.
- **What is true:** `Info source` is one label per row
  ([tools/shortlist_schema.py](../tools/shortlist_schema.py), `Official page` / `Not verified`)
  plus one `Course URL`. A row missing one fact reads `Not verified` as a whole; the missing fact
  is named only in `Notes`.
- **Honest limit:** relabelling L2's old rows as "Not found" without the research would hide the
  gap, not close it. L2 first, or alongside.
- **Related:** R9. The bunting may add "Not found? We say so, we don't guess" only once this is
  built.
- **Suggested fix:** plan it first (schema, `sync_shortlist.py`, `check_master_list.py`, the
  row-filler sheet, the spreadsheet export).

#### R9. "Official page" records that a fact was checked, not when

- **Design gap, not urgent.** A row labelled `Official page` was read on the day it was built and
  never again. S8 found three such cells that had gone wrong (a deadline, two aid forms).
- **To decide (Evan):** whether rows carry the date they were checked, and how often a Shortlist
  or Finalist row is re-read. Best decided inside L5's plan.

#### R20. Claude only tracks the marketing side; Evan wants a project manager, advisor and marketing director

- **Added 2026-10-26 (Evan). A new build, not a fix. After 10 Nov.**
- **What exists:** `STATUS.md` and `business/launchx/status.md` cover LaunchX and marketing, and
  the Notion mirror only touches tasks matching `business/launchx/status.md`. Notion's Area
  "University Research Agent" has five projects (URP Marketing, Product Developing, Business,
  Pitch deck, Clients); Product Developing and Business have no copy in the files. Advice exists
  in `mentor` / `/mentor`, social posts in `/social`.
- **What Evan wants:** every project in that Area kept in the files and synced with Notion, with
  Claude running plans and deadlines, business calls, and campaigns.
- **Suggested start:** plan mode, brainstorming first. Decide the file layout (e.g. one
  `business/projects/<name>.md` per Notion project), then widen the end-of-session mirror and
  `/catchup` to all five. Build on `mentor` and `/social`.

---

## Not a session

- **I3. Five older-record students have no spending limit.** Evan is asking them (decided
  2026-10-26). When one answers, update `profile.financial.total_budget` and
  `preferences.total_budget_ceiling`, then re-sync their list. (Without a limit the "Over budget"
  warning can never show.)
- **I4. One student's budget is stored as the text range "400000-800000".** Harmless: the cost
  check uses the top figure. Replace it with a plain number once the student confirms RM 800,000.
- **R11. One line of the positioning notes quotes old sizes.**
  [sales/positioning.md:164](sales/positioning.md#L164) says "41 columns" and "16 sections, 6
  pages"; today it is 35 columns and the sample MIT report is 15 sections, 25 pages. Evan's
  wording, so Evan's edit.
- **N1, U4, V2. Three cost claims nobody has measured.** "Roughly 70,000 tokens per university"
  and the cost of a full country ([longlist_report.md](product_report/longlist_report.md)); "it
  costs almost nothing to run" ([intake_report.md](product_report/intake_report.md)); "probably
  the cheapest step to deliver" ([decide_report.md](product_report/decide_report.md)). Settle each
  by writing down time and AI usage on the next real run of that stage (the 10 Nov lists give N1
  and U4). Cost per student is what an investor uses to judge RM 50.
- **V3. Why nine students picked only one university.**
  [decide_report.md](product_report/decide_report.md) guesses it is the poster's "pick 1 uni to go
  deep on"; no student has said so. Ask two or three of them before that report is shown outside.
