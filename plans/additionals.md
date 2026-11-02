# Additionals — the one list of open tasks and questions

**Anything new goes here** (Evan, 2026-10-31): a problem, a small task, or a question for Evan. A
separate plan file is only for one big job with many steps, and its leftovers come back here when it
ends. Evan's dated business to-dos stay in `business/launchx/status.md`, which Notion copies.

*One entry per problem, each with a suggested fix. **Only open entries live here.** When one is
done, delete it and its line in the steps below, and write one line in `plans/build-log.md`.
History: the full file up to 2026-10-28 (every closed entry, the old lane and round plans) is in
git: `git show 10b847c:business/additionals.md`. Decisions are in `decisions/log.md`.*

*Adding an entry: the next number is **R54**. Say whether it is **urgent**, and whether it is a
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
| O12 | The list form no longer asks for achievements | Fine to leave off: the list doesn't use them. Stage 4 and the apply guide do, so ask at that point if a list buyer goes on to a report | 2026-10-30 |
| O13 | How does each buyer's list get its MQA check? | A small script that looks each university up live, plus a short file of matched register names. No full database. Build after 10 Nov. 27 lists hold 493 rows but 207 universities, so a lookup is quick; the catch is matching names ("MELBOURNE" also returns RMIT). The site's addresses are in `workflows/sources.md` | 2026-10-30 |
| O14 | Run longlists and picked reports overnight from a job list? (designed 2026-09, never built) | Not before 2 Dec. Revisit if hands-on time is what limits the 20 lists. It must run on the laptop, because student files aren't in git and cloud routines can't see them. Stage 1 finalize, the Stage 4 pick and Stage 5 stay with Evan | 2026-10-31 |

### Steps — one session each. Type: "Execute step N of `plans/additionals.md`"

**Before the 10 Nov paid lists and the 12 Nov booth** (a customer would see them)

| Step | Entries | Files it writes | Waits for | Size |
|---|---|---|---|---|
| **2b, 2c, 2d** | ✅ Done 2026-10-30, as [plans/list_pdf_plan.md](list_pdf_plan.md). What they left is R30 (step 10) and R39 (waiting on a real case) | — | — | — |
| **2e** | R42 (accreditation check on every regulated row; plan first) | `workflows/sources.md`, `workflows/03b_candidate_schema.md`, `.claude/agents/row-filler.md`, `tools/check_master_list.py` | an approved plan | Medium |
| **2g** | R51 (Monash's link in the sample) | the source student's `master_list.csv`; `business/sales/sample_pack/`; `prototype/data.js`, `prototype/_build/` | nothing | Small |
| **2h** | R50 (deadline cells that open with an early round) | `.claude/agents/row-filler.md`, `workflows/03b_candidate_schema.md` | not alongside 2e (same files) | Small |
| **2i** | R53 (China rows: stale dates, scholarship routes the programme may not allow) | the affected student's `master_list.csv`, report JSONs and calendar; `.claude/agents/row-filler.md`, `.claude/agents/report-writer.md` | Tsinghua's and the embassy's replies for the last two cells; the rest needs nothing | Medium |
| **2i** | R52 (the public report and guide samples) | the source student's report and guide JSON; `business/sales/sample_pack/` | step 9 | Medium |
| **9** | R33, R34 (reports; plan R34 first). **Moved up 2026-10-31: two report buyers have paid**, so this comes before the first paid report goes out | `tools/flip_finalists.py`, `tools/build_report.py`, `tools/check_report.py`, `workflows/04_university_report.md`, `.claude/agents/report-writer.md` | nothing | Medium |

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
| **11** | R46, then R45, then R44 (plan first) | `tools/shortlist_schema.py`, `.claude/agents/row-filler.md`, `tools/build_application_prep.py`, every script that reads the columns | an approved plan | Large |
| **12** | R47, R48 | `tools/flip_finalists.py`, `tools/shortlist_schema.py`, `tools/build_list_pdf.py` | nothing | Small |

**Not a session** (Evan's own, a reply someone owes, or a measurement): I3, I4, R9, R11, N1 / U4 / V2, V3, R41, **R37 (before 10 Nov; a session drafts the wording, Evan approves it)**.

**Waiting on a real case:** R43 (a buyer of both, report form first), R39 (an old list being re-sent).

**The fact audit (2026-10-28)** is behind R26–R37: [fact_audit/00_START_HERE.md](../fact_audit/00_START_HERE.md),
with nine detailed reports beside it. Each entry names its report and finding numbers (e.g. "03 #16").

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
- **Past clients, on request only (Evan, 2026-11-02):** they were all free trials, so nothing is
  done for them until one asks. Parked, entries kept for that day: steps 4, 5, 6 and I9, L2, R16,
  R17, R21, R39, R47, I3, I4. Sample pack work on the source student's list (R51, R52) is for the
  public, so it stays.

---

## Before 10 Nov

#### R53. China rows carry last cycle's dates and a scholarship route the programme may not allow

**Urgent for one client (a real deadline on 20 Nov). Both tool gap and stale data.** A live re-check on 2 Nov found four China finalists wrong in the CSV, reports and calendar. Four things: (1) Tsinghua now has two rounds and the first closes 20 Nov, but only the 28 Feb date is on file. (2) The Chinese Government Scholarship is written up as a full ride on English-taught rows, yet ZJU and BIT both publish it as Chinese-taught only, and Tsinghua's own programme guide doesn't list it. (3) BIT and ZJU rows still offer Type B, which ZJU says doesn't cover undergraduates. (4) CSCA dates are guesses and "every applicant must sit it" is too broad, because Tsinghua only lists it as one accepted test. Detail is in that student's `research_notes.md`, 2026-11-02. Later the same day: (5) the Tsinghua report says the Department of Mechanical Engineering degree is closed to international students. It's wrong: that major is offered in Tsinghua's Chinese-English track at RMB 30,000 a year, with HSK 5 or a waiver. No report compares it yet.

**Why the system keeps doing it:** nothing tells a helper to check a scholarship against the programme's teaching language, and China dates get projected from an old embassy notice, whose country and cycle aren't recorded.

**Suggested fix:** correct the rows through `apply_backfill.py`, the report JSONs and the calendar, then rebuild. Add two lines to `row-filler` and `report-writer`: check each scholarship against the teaching language, and record the cycle and country of any embassy notice. Link it to R50 and R42.

#### R52. The public report and guide samples still show AI notes and coaching

- **Added 2026-10-31.** **Stale data the public sees, urgent:** both go on the Linktree and in print
  before the 12 Nov booth.
- **What is true:** `sample_university-report_MIT.pdf` says "Not found — free search cannot read
  Reddit" and has "The verdict", "Honest read on your fit" and "Ask your college early".
  `sample_apply-guide_US.pdf` says "Recommendation: spend the early card on…", shows Reach beside
  its universities, and leads with a 1 Nov 2026 early deadline that will have passed.
  `sample_list.pdf` is clean on the same search. Step 9 only changes new reports, and the guide's
  fix is R35 (step 10).
- **Suggested fix:** the list goes on the Linktree and in print first. After step 9, rebuild the
  sample report in the new shape with `build_sample_pack.py` (rule 4). Fix the sample guide's
  wording the same way, or keep it off the Linktree until R35 is done.

#### R51. The Monash row in the sample links to the general engineering page

- **Added 2026-10-31** (step 2f). **Stale data the public sees, small** (the booth opens 12 Nov).
- **What is true:** `Course URL` is `https://www.monash.edu/engineering`; the course page is
  `https://www.monash.edu/study/courses/find-a-course/engineering-e3001`. That page is headed
  Bachelor of Engineering, so a reader needs `Course at a glance` to see it is the same degree.
- **Suggested fix:** change the cell through `apply_backfill.py` (not part of the row's key, so no
  re-score) in the source list, then rebuild the sample and the demo. Demo text lives in
  `prototype/_build/data.template.js`, not `data.js`.

#### R50. A deadline cell that opens with an early round reads as passed while the regular round is open

- **Added 2026-10-31** (R49's note). **Tool gap, urgent before 10 Nov only if a paid list has one.**
  A student sees it.
- **What is true:** `_parse_iso_date` reads a cell's first date, so `2026-11-01 (EA); 2027-01-05 (RD)`
  is flagged once 1 Nov goes by, by `sync_shortlist.py` and now by every PDF build. Up to 8 rows
  across 5 old lists start that way; the sample doesn't (it leads with the regular date).
- **Suggested fix:** the regular deadline goes first in the cell: a line in the row-filler sheet and
  `workflows/03b_candidate_schema.md`, and those rows through `apply_backfill.py`. Not "use the last
  date": some cells end with a date that isn't a deadline.

#### R42. Nothing proves a degree is accredited before it reaches a list

- **Added 2026-10-30 (Evan).** **Tool gap, urgent:** every list for a regulated course (engineering,
  medicine, law, accounting, architecture, pharmacy, nursing and allied health). Evan wants it in the
  workflow, not only as a repair of old rows (that is R16).
- **What is true:**
  - **Which body matters is solved:** `COURSE_ACCREDITATION_MAP` in `tools/ingest_form_csv.py` maps
    the form's 38 courses to their bodies and fills `profile.recognition_targets`.
  - **Where to check is not:** `workflows/sources.md` lists Malaysian bodies only. Nothing names the
    accreditor per field and country, and the routes differ (engineering goes through the degree's
    home-country accreditor and the Washington Accord; medicine through Malaysia's own list).
  - **Nothing forces the check:** helpers fill `Recognised in Malaysia?` and a 0–5 `recognition_fit`,
    usually from the university's own page. `check_master_list.py` doesn't look at that cell. Michigan's
    robotics degree said ABET-accredited and wasn't (R16).
  - **Blocked sites:** BEM, EAC and MIA refused a plain script on 2026-10-30, and EAC's programme PDFs
    return 403. Front pages only were tested, so what works shows up on the first real buyer.
- **Suggested fix (plan first):**
  1. A table in `workflows/sources.md`: field + country → the accreditor's own list, its address and
     how to read it. Add a field's rows when a real buyer needs them (Evan, 2026-10-30: no testing
     in advance).
  2. A required step for helpers: when `recognition_targets` is not empty, read the exact degree on
     that list and start the cell with one fixed result: `Accredited`, `Not accredited`,
     `Not on list` or `Not checked`, plus the body, the checked date and a source link.
  3. `check_master_list.py` fails a row with targets whose cell has no fixed result.
  4. Prove it on the first real buyer's regulated course.
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

#### R33. A row can become a Finalist without its facts being verified

- **Added 2026-10-28** (fact audit 09 #2). **Tool gap.** The sales copy and product reports say it
  cannot happen (`longlist_report.md:186`, `university_report.md:128`).
- **What is true:** `tools/flip_finalists.py:326-333` sets `List status` to Finalist without reading
  `Info source`; `check_master_list.py` accepts `Not verified` on a Finalist row.
- **Suggested fix:** `flip_finalists.py` refuses a row that is not `Official page` (names it, exit 1),
  and `check_master_list.py` fails a Finalist row that is `Not verified`.

#### R34. The university report asks for verdicts and coaching, and nothing checks for them

- **Added 2026-10-28** (fact audit 05 #16–31, 06 #1–2, #6, #10–12). **Tool gap.** Plan first.
- **What is true:** fixed headings in `tools/build_report.py` ask for a fit verdict ("Who it's for —
  the archetype & your fit", "Why here / why hesitate", lines 124–135). The sample MIT report has
  verdict tables ("Honest read on your fit", "The verdict"), orders ("Ask your college early") and
  AI notes ("free search cannot read Reddit"). Reports print no "prepared on" date.
  `check_report.py` has no hedge, advice or chatter check. Real reports: 1,827 hedge words, 193
  advice phrases and 43 notes-to-self across 42 reports (08 #25–27).
- **Decided 2026-10-28 (Evan):** every section is facts with sources; all opinion goes in one box
  headed "Our assessment (a judgment, not a fact)".
- **Suggested fix:** rename the headings, add the box, print the date, add `hedges` / `advice` /
  `chatter` checks to `check_report.py`, and rewrite `04_university_report.md` + `report-writer.md`
  to match. Where reports and guides show our labels, reuse `JUDGMENT_LABELS` from
  `tools/apply_glossary.py` (the wording the list PDF's key uses).

#### R30. The glossary carries facts written from memory

- **Added 2026-10-28** (fact audit 04 #1–11, 06 #19–20, 07 #9–10). **Tool gap.** The advice lines
  (part a) were fixed 2026-10-29 (T2 in `plans/list_pdf_plan.md`).
- **What is true** (`tools/apply_glossary.py`; grep, line numbers moved): dated or money facts with
  no source or year ("Opens 1 October", "Roughly AUD 650–800 a year", Graduate Route length), plus
  about 15 "usually / typically" lines, including UAC's "usually … instead". Two contradict the
  sample's own rows (ESAT names Oxford; ISAFA vs the Stanford row, 04 #6). Never owned by a task:
  04 #5 recognition promises, 04 #10 opinion clauses.
- **Suggested fix:** take dated and money figures out of definitions (they belong in the cells,
  with a source), drop the hedges, and settle 04 #5, #6 and #10. The list PDF prints the glossary
  fresh on every build, so only lists being sent need rebuilding.

#### R35. The calendar and apply guide show estimates and self-set dates as real ones

- **Added 2026-10-28** (fact audit 07 #1–5, #12–14, #18–19, #23–24). **Tool gap.**
- **What is true:** `tools/build_calendar.py:72` keeps only the first date in a cell, so
  "2027-01-15 (estimated)" shows as a plain date. Calendar rows carry no source. The sample US guide
  shows a self-set "Choose by 25 Oct 2026" in the same bold as real deadlines, a "budget about 5%
  above" price guess (`build_application_prep.py:510`), and a "strategy" section of coaching
  ("Recommendation: spend the early card on…").
- **Suggested fix:** the calendar keeps the cell's qualifier text and a source column; self-set
  dates are marked "suggested, not a university date"; the strategy section is labelled as our
  advice (decision 2); the price-rise line is removed. Update the `application-guide` skill.

#### R36. The longlist instructions still let helpers write memory facts and notes into cells

- **Added 2026-10-28** (fact audit 02, 36 Medium findings). **Tool gap.** Do it inside L5's plan
  (step 7): same files, same question of what a missing fact looks like.
- **What is true:** the hedge-word ban covers one column (`English req`); helpers may put
  "couldn't reach…" notes in `Notes`; country files cache undated fees, ranks and visa rules (the
  Japan file has no dates or sources at all); several examples show "~" in a hard-fact cell; four
  country files tell helpers to give advice ("tell the student…"); default sub-scores feed the
  score with no evidence.
- **Suggested fix:** per-finding fixes are in `fact_audit/02_longlist_instructions.md`. One rule
  covers most of them: a cell holds a sourced fact or the fixed "not published / not found" wording,
  nothing else.

#### R41. Evan still looks at every student's tidied grades by hand
Not urgent, and on purpose. A measurement, not a bug. Since 30 Oct AI tidies free-text grades and
`check_grades.py` checks them, and Evan looks at raw vs tidied for 30 seconds. **Suggested fix:**
once 20 forms in a row need no correction, drop the look from `workflows/01_intake.md` finalize
step 1. Keep the script. **Tally: 0 of 20** (+1 for a clean form, back to 0 for a correction).


#### R44. Five columns the student never sees are still in `master_list.csv`

- **Added 2026-10-31** (T9, Decisions item 2 of `plans/list_pdf_plan.md`). **Design change, not
  urgent.** Do R46 first, so nothing is lost.
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

#### R46. Money to show (visa) and Student life need a new home before R44

- **Added 2026-10-31** (T9). **Design change, not urgent.**
- **What is true:** a student needs the visa money figure when applying, and only the hidden column
  holds it. Student life is covered by the university report.
- **Suggested fix:** add the visa figure to the how-to-apply guide (Stage 8). Confirm the report's
  student-life section stands alone without the column.

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

## Not a session

- **I3. Five older-record students have no spending limit.** Evan is asking them (decided
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
- **R37. The sales copy promises checks no program makes** (fact audit 09 #2–5, #14). Urgent:
  Evan says these lines at the booth. `positioning.md:71` "until a human has confirmed the fact"
  (the AI stamps its own rows); `positioning.md:76-77` "a row can't reach Shortlist on aggregator
  facts" (nothing gates Shortlist); `longlist_report.md:304` "the student knows it was checked"
  (Warnings "None" can't check cost when there is no budget). Default wording: "Every row says
  whether its facts came from the university's own page." Evan's wording, so Evan's edit.
- **V3. Why nine students picked only one university.**
  [decide_report.md](../business/product_report/decide_report.md) guesses it is the poster's "pick 1 uni to go
  deep on"; no student has said so. Ask two or three of them before that report is shown outside.
