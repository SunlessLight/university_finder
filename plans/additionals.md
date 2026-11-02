# Additionals — the one list of open tasks and questions

**Anything new goes here** (Evan, 2026-10-31): a problem, a small task, or a question for Evan. A
separate plan file is only for one big job with many steps, and its leftovers come back here when it
ends. Evan's dated business to-dos stay in `business/launchx/status.md`, which Notion copies.

*One entry per problem, each with a suggested fix. **Only open entries live here.** When one is
done, delete it and its line in the steps below, and write one line in `plans/build-log.md`.
History: the full file up to 2026-10-28 (every closed entry, the old lane and round plans) is in
git: `git show 10b847c:business/additionals.md`. Decisions are in `decisions/log.md`.*

*Adding an entry: the next number is **R84**. Say whether it is **urgent**, and whether it is a
**tool gap** (the system will keep making the mistake) or **stale data** (old files only). Plain
English, no student named, no grades, income or school. Then add it to a step below.*

---

## Start here

### Questions for Evan (each has a default)

| # | Question | Default | Raised |
|---|---|---|---|
| O5 | Is RM 50 for 20-30 universities too cheap? | Don't change the price before the pilot. Measure the real cost and hours on the first paid lists: type `/cost` after each country pass, add it to `notes/token_cost_report.md`. One measured US pass: about 700,000 tokens, USD 2-3 at API prices. A full client is a guess of USD 8-15, about RM 50, so capacity is the limit, not a bill | 2026-10-29 |
| O6 | Turn it into an app at USD 5 for 8-12 universities? | Not now. Per university it's the same price (about RM 2), and an app needs a server, logins, payments and PDPA-safe storage. Revisit after the pilot | 2026-10-29 |
| O7 | Store researched universities and reuse them for the next student | Good idea, after the pilot. Fees and deadlines change yearly, so a stored fact needs its `Checked on` date. First version: reuse a row under X months old and only re-check it | 2026-10-29 |
| O13 | How does each buyer's list get its MQA check? | A small script that looks each university up live, plus a short file of matched register names. No full database. Build after 10 Nov. 27 lists hold 493 rows but 207 universities, so a lookup is quick; the catch is matching names ("MELBOURNE" also returns RMIT). The site's addresses are in `workflows/sources.md` | 2026-10-30 |
| O14 | Run longlists and picked reports overnight from a job list? (designed 2026-09, never built) | Not before 2 Dec. Revisit if hands-on time is what limits the 20 lists. It must run on the laptop, because student files aren't in git and cloud routines can't see them. Stage 1 finalize, the Stage 4 pick and Stage 5 stay with Evan | 2026-10-31 |

### New from the seven tasks: not started

Found 2026-11-02 while doing `plans/seven_tasks.md`. Urgent ones first. Nothing here has been worked on.

| # | Problem | Urgent? | Type |
|---|---|---|---|
| R82 | The demo website still shows halal and Muslim wording | **Yes, before the 12 Nov booth** if the demo is shown | Both |
| R70 | `scripts.md` and `service-tiers.md` read "Not verified" as "not yet" | **Yes, small:** said aloud at the booth | Stale data |
| R71 | Four rows of the public sample fail the new deadline check | Before the booth, by default | Stale data |
| R77 | The sample list says "robotics track", and the sample report says there isn't one | With R71 | Stale data |
| R72 | Students lose sight of early rounds in the list PDF | **Yes, as a decision:** before a list with a live early round goes out | Tool gap |
| R55 | The apply guide tool still prints Reach/Match/Safety | Before the first buyer's guide | Tool gap |
| R56 | Sales docs and the live feedback form use the old report headings | No | Stale data |
| R57 | Facts-only reports may trip the "you" rule | No, watch the first real report | Tool gap |
| R58 | Glossary text and the PDF footer sit outside the report checks | No | Tool gap |
| R59 | Hedged numbers in Snapshot fields are now flagged | No, watch the first real report | Tool gap |
| R60 | A bad accreditation or two-date cell gets through the merge and backfill | No | Tool gap |
| R61 | The recognition warning says "not found" whatever the reason | No | Tool gap |
| R62 | A backfill can change the result but leave the score and warning old | No, until R16 is applied | Tool gap |
| R63 | A Finalist can still be `Not checked` | No, decide after the first regulated buyer | Tool gap |
| R64 | The list PDF prints the accreditation link as plain text | No | Tool gap |
| R65 | Nothing stops dated facts coming back into the glossary | No | Tool gap |
| R66 | University-specific course facts in definitions are still from memory | No | Tool gap |
| R67 | Stanford's row gives one of ISAFA's two reasons | No | Stale data |
| R68 | One `Info source` label covers a whole row | No | Tool gap |
| R69 | "None" in Warnings hides every skipped check on the list itself | No | Tool gap |
| R73 | Nothing checks that a deadline cell is only a date | No | Tool gap |
| R74 | The Monash row's course name isn't the one on the page it links to | No | Stale data |
| R75 | The Monash link could open straight at the specialisation | No | Small improvement |
| R76 | `apply_backfill.py` changes line endings in `research_notes.md` | No | Tool gap |
| R78 | The sample guide still argues from the student's family income | No | Stale data |
| R79 | The sample guide goes out of date in five weeks | No, rebuild before 2 Dec | Stale data |
| R80 | `check_report.py` flags a table header as an order | No | Tool gap |
| R81 | The faith check can't read old-style profiles | No | Stale data |

### Steps — one session each. Type: "Execute step N of `plans/additionals.md`"

**Before the 10 Nov paid lists and the 12 Nov booth** (a customer would see them)

| Step | Entries | Files it writes | Waits for | Size |
|---|---|---|---|---|
| **2i** | R53 (China rows: stale dates, scholarship routes the programme may not allow) | the affected student's `master_list.csv`, report JSONs and calendar; `.claude/agents/row-filler.md`, `.claude/agents/report-writer.md` | Tsinghua's and the embassy's replies for the last two cells; the rest needs nothing | Medium |

**After 10 Nov** (the old students' lists, then the bigger system changes)

| Step | Entries | Files it writes | Waits for | Size |
|---|---|---|---|---|
| **3** | R19 | `tools/apply_backfill.py`, `workflows/03_discover_longlist.md`, `.claude/agents/row-filler.md` | nothing. Not while a backfill is running | Small |
| **4** | I9, then L2 (the 22 rows) | other students' `profile.json`, `master_list.csv`, `research_notes.md` | step 3 | Large. One student per session if the 22 rows span many |
| **5** | R16 lookups (parts a, b, c) | `notes/r16_*`, `.tmp/r16/` | nothing. Can run beside step 4 | Large: about 45 agents plus browser lookups. Split a/b/c across sessions |
| **6** | Per student: R16 apply, R17, R21 (all three touch the same list, so do them together) | that student's `master_list.csv`, `research_notes.md`, `status.md` | steps 3 and 5 | Medium per student. Never the same student as step 4 |
| **7** | L5 + R36 (plan first, in plan mode) | `tools/shortlist_schema.py`, `tools/sync_shortlist.py`, `tools/check_master_list.py`, the row-filler sheet, `workflows/03_discover_longlist.md`, `workflows/countries/*.md` | an approved plan | Medium to large. Not alongside step 4 or 6 |
| **8** | R20 (plan first) | to be planned | nothing | Large, a new build |
| **10** | R30, R35 (glossary facts, calendar, apply guide) | `tools/apply_glossary.py`, `tools/build_calendar.py`, `tools/build_application_prep.py`, `.claude/skills/application-guide/SKILL.md`, `workflows/05_decide_and_apply.md`, `workflows/08_application_prep.md` | nothing | Medium |
| **11** | R45, then R44 (plan first) | `tools/shortlist_schema.py`, `.claude/agents/row-filler.md`, `tools/build_application_prep.py`, every script that reads the columns | an approved plan | Large |
| **12** | R48 | `tools/shortlist_schema.py`, `tools/build_list_pdf.py` | nothing | Small |

**Not a session** (Evan's own, a reply someone owes, or a measurement): I3, I4, R9, R11, N1 / U4 / V2, V3, R41.

**Waiting on a real case:** **R54 (the first buyer's form; run it the day it arrives)**, R42 (the first regulated buyer), R43 (a buyer of both, report form first), R39 (an old list being re-sent).

**The fact audit (2026-10-28)** is behind R26–R37: [fact_audit/00_START_HERE.md](../fact_audit/00_START_HERE.md),
with nine detailed reports beside it. Each entry names its report and finding numbers (e.g. "03 #16").

### Rules for every step session

1. Read this section, then only the entries your step names. The "Suggested fix" is the plan.
2. Stay inside the files the step lists; anything else goes in the hand-back.
3. Copy a student file to `.tmp/` before a program rewrites it. Run `apply_backfill.py` as a dry
   run first. Never run the calendar program with `--allow-shrink`.
4. **The source student is finished** (Evan, 2026-10-28). Their list is touched only for the
   sample pack (SP1), never for their own sake. Sample pack facts are fixed in that list and
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
- **Past clients, on request only (Evan, 2026-11-02):** they were all free trials, so nothing is
  done for them until one asks. Parked, entries kept for that day: steps 4, 5, 6 and I9, L2, R16,
  R17, R21, R39, R47, R83, I3, I4. Also parked: old lists' deadline cells with more than one date
  (R50's leftover, not counted). More fail now than the "up to 8 rows" once said, because a cell
  with the regular date first fails too.

---

## Before 10 Nov

#### R53. China rows carry last cycle's dates and a scholarship route the programme may not allow

**Urgent for one client (a real deadline on 20 Nov). Both tool gap and stale data.** A live re-check on 2 Nov found four China finalists wrong in the CSV, reports and calendar. Four things: (1) Tsinghua now has two rounds and the first closes 20 Nov, but only the 28 Feb date is on file. (2) The Chinese Government Scholarship is written up as a full ride on English-taught rows, yet ZJU and BIT both publish it as Chinese-taught only, and Tsinghua's own programme guide doesn't list it. (3) BIT and ZJU rows still offer Type B, which ZJU says doesn't cover undergraduates. (4) CSCA dates are guesses and "every applicant must sit it" is too broad, because Tsinghua only lists it as one accepted test. Detail is in that student's `research_notes.md`, 2026-11-02. Later the same day: (5) the Tsinghua report says the Department of Mechanical Engineering degree is closed to international students. It's wrong: that major is offered in Tsinghua's Chinese-English track at RMB 30,000 a year, with HSK 5 or a waiver. No report compares it yet.

**Why the system keeps doing it:** nothing tells a helper to check a scholarship against the programme's teaching language, and China dates get projected from an old embassy notice, whose country and cycle aren't recorded.

**Suggested fix:** correct the rows through `apply_backfill.py`, the report JSONs and the calendar, then rebuild. Add two lines to `row-filler` and `report-writer`: check each scholarship against the teaching language, and record the cycle and country of any embassy notice. Corrected rows must pass the `deadlines` and `accreditation` checks.

#### R54. No real student has gone through the new form and PDF flow

- **Added 2026-11-02.** **Urgent, tool gap unproven.**
- **What is true:** no student folder has `list.pdf` or `priority_levels` (0 of 27 folders). The new
  form, the weights and the PDF have only run on test data.
- **Suggested fix:** run the first buyer's form through as soon as it arrives, not on 10 Nov.

#### R42. The accreditation check isn't proven on a real buyer yet

- **Added 2026-10-30 (Evan).** **Tool gap.** Steps 1 to 3 are done (2026-11-02): the table in
  `workflows/sources.md`, the required helper step, and the `accreditation` check.
- **What is true:** which accreditor sites can really be read is still unknown. The rule that
  `Not checked` passes the gate with a warning should be looked at again once it is known.
- **Suggested fix:** prove it on the first real buyer's regulated course, and add that field's table
  rows then (Evan, 2026-10-30: no testing in advance).
- **Related:** R16 repairs old US rows (the 174 non-US rows stay out of scope). O13 in
  "Questions for Evan" is the MQA government-job lookup, a separate and smaller check.

---

## After 10 Nov: the old students' lists

#### R39. Old profiles are still weighted by the old ranking

- **Added 2026-10-29 (Evan).** Fixed for new forms 2026-10-29 (T10: equal ticks now get equal
  weight). **Stale data, not urgent.**
- **What is true:** profiles from before T10 have no `preferences.priority_levels`, so
  `derive_weights.py` keeps the rank formula, which orders equal ticks by the form's question order.
- **Suggested fix:** only for a list being re-sent: re-read the tick answers from the form export
  (no `--force` re-ingest), re-derive the weights, re-sync.

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
    hand, listed in the hand-back for Evan. Results use the cell shape from R42 (`<result> · <body> ·
    YYYY-MM-DD · <link>`), because those rows must pass the `accreditation` check.
- **Not in scope yet:** 174 non-US rows that claim accreditation (a later decision).

#### R17. Older US rows say the grades are "Well above" a bar the university does not publish

- **Stale data.** US universities publish no A-Level bar. The scoring program has had a "Not
  published" value (`entry_margin` = `not_published`) since 2026-07-28; rows scored before that
  compared grades to a guessed bar. `Admission likelihood` no longer balances it, because the PDF
  hides that column.
- **Where:** 23 US rows on other students' lists, scored before 2026-07-28. (The sample pack's rows
  are correct.)
- **Suggested fix:** in step 6, per student: count them, then set `not_published` through the
  scoring program's label function (never typed), with a line in `score_log.jsonl`.

#### R21. 49 English-test cells claim a waiver for A-Levels or English-medium schooling

- **Stale data. Not urgent unless one of these lists is about to be re-sent.** The tool gap that
  made them was R22 (fixed 2026-10-28). Four cells were fixed on 2026-10-27 (UCL, Imperial, KCL; Evan said yes).
- **Where:** 49 `English req` cells on 11 students' lists. Some state a university's real
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

#### R43. A buyer of both who fills the report form first needs a hand merge

- **Added 2026-10-30. Tool gap, not urgent.** `ingest_form_csv.py` now skips that list row safely
  instead of advising `--force`, which wipes the order. The list answers are copied in by hand
  (`workflows/01_intake.md`, "The report form").
- **Build it only if it happens more than once:** a merge that adds list answers to the folder and
  keeps `report_orders` and any tidied `subjects[]`.

#### L5. A row is labelled as a whole, so one missing fact shows "Not verified" on everything

- **Added 2026-10-27 (Evan).** Not a fault; a change to what the list promises. Evan wants
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
  row-filler sheet, `build_list_pdf.py`).

#### R9. Nothing decides how often an "Official page" row is re-read

- **Design gap, not urgent.** A row labelled `Official page` was read on the day it was built and
  never again. S8 found three such cells that had gone wrong (a deadline, two aid forms). Since
  2026-10-29 new rows carry `Checked on` (T3), so the date is recorded; old rows have it blank.
- **To decide (Evan):** how often a Shortlist or Finalist row is re-read. Best decided inside
  L5's plan.

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

#### R30. The glossary still has hedges and opinion lines

- **Added 2026-10-28** (fact audit 04 #1–11, 06 #19–20, 07 #9–10). **Tool gap.** The advice lines
  (part a) were fixed 2026-10-29. Dated and money facts, Graduate Route length and the ESAT/ISAFA
  contradiction (04 #6) were fixed 2026-11-02.
- **What is true** (`tools/apply_glossary.py`; grep, line numbers moved): about 15 "usually /
  typically" lines, including UAC's "usually … instead". Never owned by a task: 04 #5 recognition
  promises, 04 #10 opinion clauses. Also still open: 04 #7, #12 and #13 (for #12, the "New to
  these?" line in `build_glossary_section()`).
- **Suggested fix:** drop the hedges, and settle 04 #5 and #10. The list PDF prints the glossary
  fresh on every build, so only lists being sent need rebuilding.

#### R35. The calendar and apply guide show estimates and self-set dates as real ones

- **Added 2026-10-28** (fact audit 07 #1–5, #12–14, #18–19, #23–24). **Tool gap.**
- **What is true:** `tools/build_calendar.py:72` keeps only the first date in a cell, so
  "2027-01-15 (estimated)" shows as a plain date. Calendar rows carry no source. Nothing labels a
  guide's "strategy" section as advice. The sample guide's self-set "25 Oct" date and its "5%
  above" price guess are gone (2026-11-02), but they were in that guide's own written content, not
  the tool: `build_application_prep.py` holds no "5%" line, so a new guide can write them again.
- **Suggested fix:** the calendar keeps the cell's qualifier text and a source column; self-set
  dates are marked "suggested, not a university date"; the strategy section is labelled as our
  advice (decision 2). The price-guess and self-set-date rules go in
  `.claude/skills/application-guide/SKILL.md` and `workflows/08_application_prep.md`.

#### R36. Country files still hold undated facts

- **Added 2026-10-28** (fact audit 02). **Tool gap.** Do it inside L5's plan (step 7): same files,
  same question of what a missing fact looks like.
- **What is true:** the hedge check now covers nearly every column, and the PDF hides `Notes`.
  What's left: undated facts in country files (Japan most), the advice line in
  `workflows/countries/singapore.md:134`, and default sub-scores, which feed the score with no
  evidence (not re-tested).
- **Suggested fix:** per-finding fixes are in `fact_audit/02_longlist_instructions.md`.

#### R41. Evan still looks at every student's tidied grades by hand
Not urgent, and on purpose. A measurement, not a bug. Since 30 Oct AI tidies free-text grades and
`check_grades.py` checks them, and Evan looks at raw vs tidied for 30 seconds. **Suggested fix:**
once 20 forms in a row need no correction, drop the look from `workflows/01_intake.md` finalize
step 1. Keep the script. **Tally: 0 of 20** (+1 for a clean form, back to 0 for a correction).


#### R44. Five columns the student never sees are still in `master_list.csv`

- **Added 2026-10-31** (T9, Decisions item 2 of `plans/list_pdf_plan.md`). **Design change, not
  urgent.**
- **What is true:** the PDF hides List status, Tier, Notes, Student life and Money to show (visa),
  but the file and its scripts still carry them. List status alone is in 27 files, and it drives
  the whole narrowing step, so plan that one before deleting it.
- **Suggested fix:** plan first. Delete each column from `SHORTLIST_HEADERS` and every script that
  reads it; `upgrade_header()` and the checks must cope with lists that still have them.

#### R45. Stage 3 still researches three columns no student reads

- **Added 2026-10-31** (T9). **Tool gap, not urgent.** Fewer tokens per university, which also feeds
  the pricing question (O5 in "Questions for Evan").
- **What is true:** row-fillers fill Student life, Notes and Money to show (visa) on every row, and
  the PDF prints none of them.
- **Suggested fix:** remove them from `REQUIRED_CANDIDATE_FIELDS` and the row-filler sheet. Do it
  with R44 or just after, then measure the saving on one country pass.

#### R47. `flip_finalists.py` refuses a list in the old layout

- **Added 2026-10-31** (T3's note). **Tool gap, not urgent.** It stops with an error rather than
  doing harm, and only a list from before 29 Oct hits it.
- **What is true:** it requires the exact column set, and it doesn't call `upgrade_header()` as
  `apply_backfill.py`, `build_list_pdf.py` and `check_master_list.py` do. A tester with an old list
  who orders a report would be stopped at the flip.
- **Suggested fix:** call `upgrade_header()` on load, keeping the check for other mismatches.

#### R48. The list PDF prints one exchange-rate date for every currency

- **Added 2026-10-31** (T6's note). **Tool gap, not urgent. A student sees it, only on a Taiwan row.**
- **What is true:** each card's cost breakdown prints `FX_AS_OF` (2026-09-05), but the TWD rate was
  added on 2026-09-23.
- **Suggested fix:** keep a date per currency where it differs, or re-stamp every rate on one date.

---

## New from the seven tasks (2026-11-02)

Not started. All numbered by the order they came in; the table in "Start here" is by urgency.

#### R55. The apply guide tool still prints Reach/Match/Safety

- **Not urgent today, do it before the first buyer's guide. Tool gap.** The public sample is fixed,
  but only because its JSON no longer says it.
- **What is true:** `tools/build_application_prep.py:427-429` adds `admission_likelihood` to each
  university's heading; line 51 and `workflows/08_application_prep.md` still show "Reach".
- **Suggested fix:** stop printing it, and rename or drop the field. Do it with R35.

#### R56. Sales docs and the live feedback form use the old report headings

- **Not urgent, stale data.** Nothing breaks, but the sales description promises an "honest read on
  whether you fit" under the old section names.
- **What is true:** `forms/report_feedback.json:14,19,25,26` (and 39-51, 64-76) list the old names as
  answer choices in a live form. Also `business/product_report/university_report.md:77,87,88,140-141,291`,
  `business/sales/service-tiers.md:83`, `prototype/screens/report.js:3,33`,
  `prototype/_build/data.template.js:337,340`.
- **Suggested fix:** update the product report and service tiers together. The form is Evan's live
  form, so show him the new choices first.

#### R57. Facts-only reports may trip the "you" rule

- **Not urgent, tool gap.** Watch it on the first real report.
- **What is true:** `tools/check_report.py` `MIN_YOU_PER_1K` fails a report under 1.0 "you" per 1,000
  characters. A made-up facts-only report needed "You can read the page" added per section to pass.
  This pushes writers towards "you" sentences, the natural home of advice.
- **Suggested fix:** lower the minimum or drop it if the first real report fails. Don't change it
  before there's evidence.

#### R58. Glossary text and the PDF footer sit outside the report checks

- **Not urgent, tool gap.**
- **What is true:** `tools/report_to_pdf.py` adds "Key terms" after `check_report.py` has run, so
  hedges and advice in glossary lines are never checked (audit 06 #18). The date prints under the
  title only: the footer at `tools/report_to_pdf.py:66` has none, so a single printed page shows no
  date (audit 06 #6).
- **Suggested fix:** run the three word checks on the glossary text, and add the date to the footer.

#### R59. Hedged numbers in Snapshot fields are now flagged

- **Not urgent, tool gap.** Intended behaviour, but writers may hit it often at first.
- **What is true:** a habit of writing "~" before a published figure now shows up under `hedges`. The
  workflow's examples were changed to match.
- **Suggested fix:** none now. Check on the first real report whether the hits are useful.

#### R60. A bad accreditation or two-date cell gets through the merge and backfill

- **Not urgent, tool gap.** The final check still stops it before a list goes out. It costs a repeat
  of the helper's work, not a wrong list.
- **What is true:** `tools/apply_backfill.py:250-260` and `tools/merge_candidates.py:168` run
  `cell_format_problem()`, but `Key deadline` isn't in `FORMATTED_COLUMNS`, and neither tool reads the
  student's targets. `tools/apply_backfill.py:23` says it refuses what the checker would fail, which
  isn't true here.
- **Suggested fix:** have both tools load `recognition_targets` and call
  `check_master_list.recognition_problem()` and `deadline_problem()` before they write.

#### R61. The recognition warning says "not found" whatever the reason

- **Not urgent, tool gap.** The `Not checked` scores 3 at most rule keeps it off those rows, but that
  depends on helpers following the rule.
- **What is true:** `tools/shortlist_schema.py:595` always writes "Recognition risk: not found on
  <targets> list" when `recognition_fit` is 2 or less. A `Not checked` row scored 2 or less would tell
  a student the list was searched when it wasn't.
- **Suggested fix:** base the warning on the cell's result, not the score.

#### R62. A backfill can change the result but leave the score and warning old

- **Not urgent until R16 is applied, then yes:** it's the first run that would hit this. **Tool gap.**
- **What is true:** `row-filler.md` says backfill never writes computed columns or sub-scores. A row
  changed to `Not on list` by backfill keeps its old `recognition_fit`, so it has no `Recognition risk`
  warning.
- **Suggested fix:** after R16's apply step, re-score the rows whose result went negative; or add a
  check that `Not accredited` / `Not on list` rows carry the warning.

#### R63. A Finalist can still be `Not checked`

- **Not urgent, tool gap.** Decide it after the first real buyer, with R42.
- **What is true:** `check_values` in `tools/check_master_list.py` stops a "Not verified" Finalist, but
  the accreditation check only warns on `Not checked`, so a report could be written on an unread
  accreditation for a regulated course.
- **Suggested fix:** fail `Not checked` when `List status` is Finalist.

#### R64. The list PDF prints the accreditation link as plain text

- **Not urgent, tool gap.** The information is correct, only less handy.
- **What is true:** `tools/build_list_pdf.py:371` makes links clickable only for the link columns.
- **Suggested fix:** make URLs in this cell clickable, or show just the result and body on the card.

#### R65. Nothing stops dated facts coming back into the glossary

- **Not urgent, tool gap.** Nothing is wrong today; the risk is the next new entry. Same gap as 04 #13.
- **What is true:** `tools/build_glossary_sheet.py:53` and `tools/build_list_pdf.py:419` copy
  definitions unchanged, and no test covers them. The rule is only a comment above `GLOSSARY`.
- **Suggested fix:** a test that fails if a definition holds a month name, a four-digit year, a
  currency mark or "~". Allow the Medical Act 1971 by name.

#### R66. University-specific course facts in definitions are still from memory

- **Not urgent, tool gap.** Stable course structures, and each prints only when a list uses the term.
- **What is true:** `tools/apply_glossary.py` still holds MIT's IAP "four weeks each January" and HASS
  "eight subjects", Brown's PLME "eight-year" and BRDD "five-year", Cornell's "eight admitting
  undergraduate colleges", and NUS's NOC "six- to twelve-month" placement.
- **Suggested fix:** leave them unless a buyer's list uses the term, then check that one against the
  university's page. Decide with what's left of R30.

#### R67. Stanford's row gives one of ISAFA's two reasons

- **Not urgent, stale data.** Incomplete, not wrong, for a Malaysian student.
- **What is true:** `business/sales/sample_pack/sample_master_list.csv:8` says "ISAFA only if you cannot
  pay the Profile fee". Stanford's page also lists living in a country where the College Board can't
  process payments. `prototype/data.js:509` also holds ISAFA.
- **Suggested fix:** leave it. If the row is reopened, add the second reason through
  `apply_backfill.py`.

#### R68. One `Info source` label covers a whole row

- **Not urgent, tool gap.** The new sales wording is true at row level, but a prospect could push on
  it.
- **What is true:** `tools/shortlist_schema.py:95` holds one label per row, so "Official page" can sit
  beside a single guessed cell (audit 09 #5). The same over-reading is in
  `business/product_report/longlist_report.md:70` and `business/sales/sample_pack/README.md:11`.
- **Suggested fix:** keep the row-level wording for now and tie this to L5. If L5 is far off, reword
  both lines to say the label covers the row as a whole.

#### R69. "None" in Warnings hides every skipped check on the list itself

- **Not urgent, tool gap.** New form answers require a limit, but older students without one still
  get "None".
- **What is true:** `tools/shortlist_schema.py:572-581` skips "Over budget" silently with no limit or
  no MYR total, and `:564` only flags English when `meets_english` is False. The list a student sees
  gives no sign of this (audit 09 #14).
- **Suggested fix:** add a message such as "Budget not given: cost not checked" in
  `feasibility_flags()`, with a test, after checking it won't clash with the "None" handling at
  `tools/shortlist_schema.py:136`.

#### R70. `scripts.md` and `service-tiers.md` read "Not verified" as "not yet"

- **Urgent, small:** Evan may say it at the booth on 12-13 Nov. **Stale data.**
- **What is true:** `business/sales/scripts.md:123` says "rows you haven't checked yet", and
  `business/sales/service-tiers.md:56-57` says "`Not verified` until then. You can see exactly what's
  been checked." `tools/shortlist_schema.py:269-272` says it means an old row or a failed research
  attempt, "not 'not yet'". Both also imply Evan does the checking, and "exactly" overstates a
  one-label-per-row column.
- **Suggested fix:** reword both to match the approved line, for example "rows where the AI researcher
  couldn't read the official page". Evan approves the wording.

#### R71. Four rows of the public sample fail the new deadline check

- **Do before the booth by default. Stale data.** All four lead with the regular date, so none wrongly
  reads as passed today, but a buyer's list wouldn't pass the gate with these rows.
- **What is true:** `check_master_list.py --file sample_master_list.csv` gives FAIL deadlines (4): rows
  2 (MIT, 2 dates), 3 (NUS, 3), 13 (Rose-Hulman, 2), 14 (Northeastern, 4).
- **Suggested fix:** decide R72 first, because this removes the early dates from the public PDF. Then
  move them to the source student's `research_notes` through `apply_backfill.py`, dry run first, and
  rebuild. One small session with R77 and R82.

#### R72. Students lose sight of early rounds in the list PDF

- **Urgent as a decision: before a list with a live early round goes out, e.g. Early Decision II on
  1 Jan. Tool gap.** It's Evan's product decision.
- **What is true:** `tools/build_list_pdf.py:93-96` prints the whole `Key deadline` cell, so a student
  can see an early round today. Under the new rule that date moves to `research_notes`, which is never
  sent. An early round can be the better choice, so the list would no longer show it exists.
  `tools/build_calendar.py:67-81` also reads only this cell, so the calendar shows an early round only
  if a report's `dated_items` names it. Whether reports do wasn't tested.
- **Suggested fix:** a separate "Early round" column shown on the card but ignored by the "Deadline
  passed" warning. It needs `tools/shortlist_schema.py` and a plan. Default until then: keep the rule
  as built, and use the report and calendar to tell students about early rounds.

#### R73. Nothing checks that a deadline cell is only a date

- **Not urgent, tool gap.** A wrongly worded cell is still readable.
- **What is true:** `row-filler.md` allows only `YYYY-MM-DD`, `Rolling` or `Not published`, but nothing
  enforces it. The sample holds "2027-01-13 (UCAS equal consideration)".
- **Suggested fix:** add `Key deadline` to `FORMATTED_COLUMNS` in `tools/shortlist_schema.py`, which
  would also close that half of R60. Old lists will fail in larger numbers, so plan it with L5 + R36.

#### R74. The Monash row's course name isn't the one on the page it links to

- **Not urgent, stale data (one row).** `Course at a glance` explains it.
- **What is true:** the row says "Bachelor of Robotics and Mechatronics Engineering (Honours)", which the
  source student's notes call the Malaysia campus title. The row is for Clayton, where the page shows
  "Engineering - E3001" with a specialisation.
- **Suggested fix:** leave it unless Evan wants the sample exact. `Course` is part of the row's key, so
  changing it means a re-score.

#### R75. The Monash link could open straight at the specialisation

- **Not urgent, small improvement.**
- **What is true:** the page has a link ending `engineering-e3001#overview-1,Robotics_and_mechatronics_engineering`.
  Not tested in a browser.
- **Suggested fix:** leave it. If Evan wants it, click that address in Chrome first, then change the cell
  through `apply_backfill.py`.

#### R76. `apply_backfill.py` changes line endings in `research_notes.md`

- **Not urgent, tool gap, harmless.** No words change, but a before/after comparison looks edited.
- **What is true:** 25 LF lines of the source student's notes became CRLF on one run.
- **Suggested fix:** leave it. If it's ever touched, read and write the file with `newline=""`.

#### R77. The sample list says "robotics track", and the sample report says there isn't one

- **Not urgent, but both are public, side by side. Stale data (one row).**
- **What is true:** `sample_list.pdf` and `sample_master_list.csv` row 2 read "Mechanical Engineering
  (Course 2) — robotics track". The report's "What you'll actually study" says there is no separate
  robotics track.
- **Suggested fix:** rename the `Course` cell. It's part of the row's key, so it needs a re-score. Do it
  with R71, before print if there's time.

#### R78. The sample guide still argues from the student's family income

- **Not urgent, stale data.** The figure is redacted, so nothing private leaks, but it breaks S3 in
  public. `workflows/08_application_prep.md:135` and the skill already forbid it for new guides.
- **What is true:** section 3 of the guide's strategy compares "the income in your file" with each
  university's zero-parent-contribution line, kept through the first pair of `APPLY_TEXT_REDACTIONS`.
- **Suggested fix:** rewrite it as income-band examples when R35 is done.

#### R79. The sample guide goes out of date in five weeks

- **Not urgent, stale data.** Correct for the 12-13 Nov booth.
- **What is true:** its first action registers for the 5 Dec SAT by 20 Nov, and the early-aid rows run
  to 1 Dec. Only MIT and the SAT were re-read on 2 Nov; other dates are from 12 Oct. The guide says so.
- **Suggested fix:** rebuild before the 2 Dec demo day, and take its Start here to the January deadlines.

#### R80. `check_report.py` flags a table header as an order

- **Not urgent, tool gap, small.** A 10-second rewording.
- **What is true:** `ORDER_WORDS` in `tools/check_report.py` matches "| Check | Result |" as an order.
- **Suggested fix:** skip table header rows in the advice check. Default: leave it until it happens again.

#### R81. The faith check can't read old-style profiles

- **Not urgent, stale data.** Old students are parked, and new ones use the new keys.
- **What is true:** `tools/check_report.py:659` reads `needs.diet_halal` and `needs.worship_facilities`.
  Older profiles use `halal_food` and `prayer_facilities`, so a real tick there reads as "not asked".
- **Suggested fix:** read both key names if a past client's report is ever rebuilt.

#### R82. The demo website still shows halal and Muslim wording

- **Urgent before the 12 Nov booth, if the demo is shown there. Both tool gap and stale data.** It's the
  wording Evan took out of reports on 2026-10-30, because it made students feel the report was built
  for Malays. The faith rule covers reports, and nothing checks list cells. `sample_list.pdf` is clean.
- **What is true:** `prototype/data.js:230` (MIT) and `:450` (Princeton) hold it in `studentLife`, which
  comes from `sample_master_list.csv`. `prototype/_build/data.template.js:91` lists `studentLife` in the
  demo's "The course" group, so it looks shown on screen; the page wasn't opened to confirm it.
- **Suggested fix:** reword both cells through `apply_backfill.py` on the source list, then rebuild the
  sample and the demo. One small session with R71.

#### R83. Two Finalist rows on one old list aren't stamped Official page

- **Added 2026-10-31** (R33's commit, numbered R53 in `plans/build-log.md` entry 23; that number went to
  the China rows). **Stale data, urgent only if that list goes out again.** Parked with past clients.
- **What is true:** the commit-drafter counted 2 such rows on 1 of 27 lists; the list and the rows'
  values weren't read. `check_master_list.py` fails only the value `Not verified`, so the list fails
  only if the rows read that.
- **Suggested fix:** verify them on the official pages, then correct them through `apply_backfill.py`.

---

## Not a session

- **I3. 11 older-record students have no spending limit.** Evan is asking them (decided
  2026-10-26). When one answers, update `profile.financial.total_budget` and
  `preferences.total_budget_ceiling`, then re-sync their list. (Without a limit the "Over budget"
  warning can never show.)
- **I4. One student's budget is stored as the text range "400000-800000".** Harmless: the cost
  check uses the top figure. Replace it with a plain number once the student confirms RM 800,000.
- **R11. The sales files don't share one set of numbers, and still sell a spreadsheet.**
  `business/sales/positioning.md`, `scripts.md` and `service-tiers.md` say 35 or 41 columns, "16 sections, 6
  pages" and "a spreadsheet". Today it is a PDF list, 40 columns inside, and the sample MIT report is
  15 sections, 25 pages. The 25 Sept review's other open move is here too: publish a price and a
  turnaround time on the poster. Evan's wording, so Evan's edit.
- **N1, U4, V2. Three cost claims nobody has measured.** "Roughly 70,000 tokens per university"
  and the cost of a full country ([longlist_report.md](../business/product_report/longlist_report.md)); "it
  costs almost nothing to run" ([intake_report.md](../business/product_report/intake_report.md)); "probably
  the cheapest step to deliver" ([decide_report.md](../business/product_report/decide_report.md)). Settle each
  by writing down time and AI usage on the next real run of that stage (the 10 Nov lists give N1
  and U4). Cost per student is what an investor uses to judge RM 50.
- **V3. Why nine students picked only one university.**
  [decide_report.md](../business/product_report/decide_report.md) guesses it is the poster's "pick 1 uni to go
  deep on"; no student has said so. Ask two or three of them before that report is shown outside.
