# Additionals — the backlog of known problems not yet fixed

*One entry per problem, each with a suggested fix. **Only open entries live here.** When one is
done, delete it and its line in the steps below, and write one line in `plans/build-log.md`.
History: the full file up to 2026-10-28 (every closed entry, the old lane and round plans) is in
git: `git show 10b847c:business/additionals.md`. Decisions are in `decisions/log.md`.*

*Adding an entry: the next number is **R41**. Say whether it is **urgent**, and whether it is a
**tool gap** (the system will keep making the mistake) or **stale data** (old files only). Plain
English, no student named, no grades, income or school. Then add it to a step below.*

---

## Start here

### Steps — one session each. Type: "Execute step N of `business/additionals.md`"

**Before the 10 Nov paid lists and booth** (allowed under the freeze: a customer would see them)

| Step | Entries | Files it writes | Waits for | Size |
|---|---|---|---|---|
| **2b** | R28, R29, R30 part a, R32 (the fact audit's spreadsheet fixes) | `tools/shortlist_schema.py`, `tools/check_master_list.py`, `tools/apply_glossary.py`, `tools/build_glossary_sheet.py` | nothing | Medium |
| **2c** | R23, R25, then R31 | the source student's `master_list.csv`, `research_notes.md`, `score_log.jsonl`; `business/sales/sample_pack/`; `prototype/data.js`, `prototype/_build/`; `workflows/countries/uk.md` (R25) | step 2b (so the rebuilt sample carries the new wording and passes the new check) | Small to medium |
| **2d** | R39, R40: **now tasks T10, T2b + T3b + T11 in [plans/list_pdf_plan.md](../plans/list_pdf_plan.md)** (Evan, 2026-10-29: no waiting). Run them from the plan, not from here | see the plan | see the plan | Small to medium |

**After 10 Nov** (the old students' lists, then the bigger system changes)

| Step | Entries | Files it writes | Waits for | Size |
|---|---|---|---|---|
| **3** | R19 | `tools/apply_backfill.py`, `workflows/03_discover_longlist.md`, `.claude/agents/row-filler.md` | nothing. Not while a backfill is running | Small |
| **4** | I9, then L2 (the 22 rows) | other students' `profile.json`, `master_list.csv`, `research_notes.md` | step 3 | Large. One student per session if the 22 rows span many |
| **5** | R16 lookups (parts a, b, c) | `notes/r16_*`, `.tmp/r16/` | nothing. Can run beside step 4 | Large: about 45 agents plus browser lookups. Split a/b/c across sessions |
| **6** | Per student: R16 apply, R17, R21 (all three touch the same list, so do them together) | that student's `master_list.csv`, `research_notes.md`, `status.md` | steps 3 and 5 | Medium per student. Never the same student as step 4 |
| **7** | L5 + R36 (plan first, in plan mode) | `tools/shortlist_schema.py`, `tools/sync_shortlist.py`, `tools/check_master_list.py`, the row-filler sheet, `workflows/03_discover_longlist.md`, `workflows/countries/*.md` | an approved plan | Medium to large. Not alongside step 4 or 6 |
| **8** | R20 (plan first) | to be planned | nothing | Large, a new build |
| **9** | R33, R34 (reports; plan R34 first). **Before the first paid report goes out**, even if that is before 10 Nov | `tools/flip_finalists.py`, `tools/build_report.py`, `tools/check_report.py`, `workflows/04_university_report.md`, `.claude/agents/report-writer.md` | nothing | Medium |
| **10** | R30 part b, R35 (glossary facts, calendar, apply guide) | `tools/apply_glossary.py`, `tools/build_calendar.py`, `tools/build_application_prep.py`, `.claude/skills/application-guide/SKILL.md`, `workflows/05_decide_and_apply.md`, `workflows/08_application_prep.md` | step 2b (same glossary file) | Medium |

**Not a session** (Evan's own, a reply someone owes, or a measurement): I3, I4, R9, R11, N1 / U4 / V2, V3, **R26 and R37 (before 10 Nov)**.

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

#### R28. No check looks for hedge, advice or chatter words in the spreadsheet

- **Added 2026-10-28** (fact audit 03 #16, 08 #1–24). **Tool gap, urgent:** the one change that
  stops guesses reaching every list after it.
- **What is true:** `check_master_list.py` scans prose columns for jargon only (`check_jargon`).
  Across real lists, 162 of 280 "Official page" rows hold a hedge word ("confirm", "likely",
  "typically", "~"), and 22 cells give advice. That is how "likely waived… confirm" reached about 40 cells.
- **Suggested fix:** a new `check_hedges` over the fact columns, word lists from
  `fact_audit/08_output_sweep.md` (regex table). Fails on rows stamped `Official page`, warns on
  `Not verified` rows. "~" is allowed only before a converted MYR figure ("~RM"). `apply_backfill.py`
  runs the same check on what it writes. Expect old lists to fail: that is the point (they are not
  being re-sent). `research_notes.md` is internal, never sent (Evan, 2026-10-28), so its notes-to-self
  (08 #38–41) are fine and the check skips it.

#### R29. Three fixed sentences the scripts write into cells are advice or notes about the student

- **Added 2026-10-28** (fact audit 03 #1–3, 02 #1). **Tool gap, urgent.**
- **What is true:** in `tools/shortlist_schema.py`, the only allowed "no date" deadline is
  `"Not published — check portal"` (line 109), an instruction. `feasibility_flags` writes
  `"Recognition risk — check MQA/BEM"` (542), also an instruction, and stamps
  `"Urban+Rural both ticked"` (550), a note about the student's form, into every row's Warnings.
- **Suggested fix:** sentinel → `"Not published"` (keep the old value accepted, so old lists still
  pass); flag → `"Recognition risk: not found on <body> list"`; move "Urban+Rural" to Stage 1
  `_needs_review`. Search the workflows and row-filler sheet for the old sentinel text and update them.

#### R30. The glossary carries advice and facts written from memory

- **Added 2026-10-28** (fact audit 04 #1–11, 06 #19–20, 07 #9–10). **Tool gap.** Part a is urgent:
  every student sheet has the Glossary tab, and every report and guide prints it.
- **What is true** (`tools/apply_glossary.py`): advice inside definitions ("Avoid it if you need to
  compare aid offers", line 33; "so check what's left for you", 69; "check its register to confirm",
  492–494; "register and sit it in autumn", 170). Dated or money facts with no source or year
  ("Opens 1 October", 90; "Roughly AUD 650–800 a year", 982; Graduate Route length, 883), plus
  about 15 "usually / typically" lines. Two contradict the sample's own rows (ESAT names Oxford; ISAFA).
- **Suggested fix:** part a (step 2b): rewrite the advice lines as plain definitions. Part b (step 10):
  take dated and money figures out of definitions (they belong in the cells, with a source), and drop
  the hedges. Rebuild glossaries only for lists being sent.

#### R31. The public sample still holds hedged, advice and cut-off cells beyond SP1

- **Added 2026-10-28** (fact audit 04 #14–32, 08 #42–47; counted on the post-SP1 files). **Stale
  data the public sees** (sample pack + demo website; the booth opens 10 Nov).
- **What is true** (sample CSV / demo `data.js`): 11 / 15 "QS ~" ranks with no edition year; 3 / 3
  "~Apr 2027" deadlines; 2 / 2 "confirm exact 2027 date"; 3 / 3 "MQA: verify"; 1 "most likely under its
  BSc row"; 1 "Count yours"; 5 / 5 "student visa form financial documentation" with no amount (the
  I-20 jargon swap emptied the cell, `apply_glossary.py:1207`); 13 cells cut off mid-sentence;
  opinions in fact cells ("China's most competitive university"). Demo copy: "make sure the rest of
  your list carries the weight" (`data.js:1090`).
- **Suggested fix:** after step 2b, re-read each fact on the official page and fix it in the source
  list (`apply_backfill.py --overwrite`, dry run first), never in the sample CSV. Rebuild the sample
  and the demo as SP1 did, then `check_master_list.py` (with R28's check) must be clean.

#### R39. Topics a student ticks the same are ranked by the form's question order

- **Added 2026-10-29 (Evan).** **Tool gap, urgent:** every list scored from the tick form is
  affected. Fix before the 10 Nov lists are scored: task T10 in
  [plans/list_pdf_plan.md](../plans/list_pdf_plan.md).
- **What is true:** the form's "Tick the importance of each topic" grid (Must have / Important /
  Nice to have / Doesn't matter) is turned into a strict 1–8 ranking
  (`_build_priorities_from_sliders` in `tools/ingest_form_csv.py`). Equal ticks are ordered by
  the form's question order (`CANONICAL_SLIDER_ORDER`: Cost first, Hands-On Experience last), and
  `tools/derive_weights.py` then gives rank 1 a 20% weight and rank 8 5%. In the 10 answers on file
  (counted 2026-10-29): all 10 have ties (most put 3–6 topics on Important), and 1 ticked all eight
  "Must have", so that student's weights are pure form order (Cost counts 4× Hands-On). Only the
  order is kept in `preferences.json`, not the tick levels.
- **Why not change the form:** a Google Forms grid can only limit each column to one tick in the
  whole grid, which allows one Must have and one Important across 8 topics.
- **Suggested fix:** keep the levels as `preferences.priority_levels` (token → 3/2/1/0). In
  `derive_weights.py`, each topic's weight = its points ÷ total points (Must have 3, Important 2,
  Nice to have 1, Doesn't matter 0): equal ticks get equal weight; all equal, or all 0, gives equal
  weights. Keep the `course_match` floor; `scholarship_required` sets scholarship to Must have.
  Profiles with only a ranking (older forms) keep today's rank formula. Update the `scoring-weights`
  skill and the generated `rationale`. Prove: all Must have → 12.5% each; 2 Must have + 6
  Important → 16.7% and 11.1%.
- **Old lists:** stale data, not urgent. Re-derive weights and re-sync only a list that is being
  re-sent (re-read the tick answers from the form export; no `--force` re-ingest).

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

#### R32. The score and label columns are explained nowhere a student can see

- **Added 2026-10-28** (fact audit 03 #4–6, 04 #22, 06 #4, #26, 07 #11). **Design gap.** Step 2b,
  because the 10 Nov lists show them.
- **What is true:** `Desirability` (0–100), `Tier`, `Admission likelihood` (Reach/Match/Safety) and
  `Grades vs entry bar` are our rule-made labels, built from AI-picked 0–5 sub-scores. The glossary
  defines acronyms only. "Safety" reads like a promise of admission.
- **To decide (Evan). Default:** keep the columns, and add one Glossary-tab row per column, starting
  "Our label, not the university's:", plus the rule in one line (e.g. Safety = grades above the
  published bar; not a promise). The same wording goes in reports and apply guides in step 9.

#### R33. A row can become a Finalist without its facts being verified

- **Added 2026-10-28** (fact audit 09 #2). **Tool gap.** The sales copy and product reports say it
  cannot happen (`longlist_report.md:186`, `university_report.md:128`).
- **What is true:** `tools/flip_finalists.py:326-333` sets `List status` to Finalist without reading
  `Info source`; `check_master_list.py` accepts `Not verified` on a Finalist row.
- **Suggested fix:** `flip_finalists.py` refuses a row that is not `Official page` (names it, exit 1),
  and `check_master_list.py` fails a Finalist row that is `Not verified`.

#### R34. The university report asks for verdicts and coaching, and nothing checks for them

- **Added 2026-10-28** (fact audit 05 #16–31, 06 #1–2, #6, #10–12). **Tool gap.** Plan first; needs
  decision 2 in `fact_audit/00_START_HERE.md`.
- **What is true:** fixed headings in `tools/build_report.py` ask for a fit verdict ("Who it's for —
  the archetype & your fit", "Why here / why hesitate", lines 124–135). The sample MIT report has
  verdict tables ("Honest read on your fit", "The verdict"), orders ("Ask your college early") and
  AI notes ("free search cannot read Reddit"). Reports print no "prepared on" date.
  `check_report.py` has no hedge, advice or chatter check. Real reports: 1,827 hedge words, 193
  advice phrases and 43 notes-to-self across 42 reports (08 #25–27).
- **To decide (Evan). Default:** every section is facts with sources; all opinion goes in one box
  headed "Our assessment (a judgment, not a fact)".
- **Suggested fix:** rename the headings, add the box, print the date, add `hedges` / `advice` /
  `chatter` checks to `check_report.py`, and rewrite `04_university_report.md` + `report-writer.md`
  to match.

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

#### R40. Replace "Admission likelihood" with the university's published admit rate

- **Added 2026-10-29 (Evan).** **Design change, now in progress:** Evan chose to do it all before
  10 Nov. The plan is [plans/list_pdf_plan.md](../plans/list_pdf_plan.md) Decisions item 9 and tasks
  T2b (done), T3b, T11; it overrides the parts a/b split below. Kept for the reasoning.
- **Why:** the column reads as our verdict on whether the student gets in. We can't give one:
  holistic admission weighs activities, essays and interviews, and the form collects none of them
  (and shouldn't: nobody predicts holistic admission from a list of clubs). Today the column is
  grades (a coarser repeat of `Grades vs entry bar`) plus a hand-set "very selective" override,
  which is a fact about the university presented as our judgment.
- **What is true:** `classify_admission()` in `tools/shortlist_schema.py` makes it. Two rules lean
  on it: shortlists are a balanced Reach/Match/Safety spread, and "an unreachable uni must not rank
  high" (`CLAUDE.md`, `workflows/00_overview.md`). The 10 Nov PDF (T6 in
  `plans/list_pdf_plan.md`) shows the column with its T2 definition (`JUDGMENT_LABELS`).
- **Part a (before 10 Nov):** reword the `Admission likelihood` definition in
  `tools/apply_glossary.py` to say what it uses: "Uses only your grades and how selective the
  university is. We don't know your activities, essays or interviews, so it is not a prediction
  about you. Safety is not a promise of admission."
- **Part b (after 10 Nov, plan first):** a sourced `Admit rate` column in place of the label, e.g.
  "4.5% of all applicants (Common Data Set 2024–25)".
  - US: Common Data Set section C1 (applied, admitted). It counts all applicants, not
    international ones; where a university publishes an international rate, use that and say so.
  - UK and the other countries: not known yet. The plan's first job: per country, which official
    sources give an admit or offer rate (Oxford and Cambridge publish per-course figures; most UK
    universities may not), and what the cell says when none exists ("Not published"). Where entry
    is set by grades alone, `Grades vs entry bar` already answers the question.
  - Decide in the plan what replaces Reach/Match/Safety in the balanced-shortlist rule (e.g. kept
    for balancing only and not shown, or balance on grades + admit rate). Then update the
    `CLAUDE.md` guardrail, the T2 definition, the PDF and the sample, and log it in `decisions/log.md`.

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
- **R26. The intake form's budget choices start at RM 500,000** (fact audit 01 #4, #18). Urgent,
  before 10 Nov; Evan's form. A family with RM 150,000 must pick 500,000, so "Over budget" never
  shows. Default: replace the three choices with a number box (or add lower bands). The opening text
  ("Hihi! … your data is safe with me 🤩🥰") is chatty and clashes with the consent text. Default:
  "We use your answers to research universities for your course and countries." After the edit:
  `fetch_form_questions.py --check`, and Claude updates the budget reader in `ingest_form_csv.py`.
- **R37. The sales copy promises checks no program makes** (fact audit 09 #2–5, #14). Urgent:
  Evan says these lines at the booth. `positioning.md:71` "until a human has confirmed the fact"
  (the AI stamps its own rows); `positioning.md:76-77` "a row can't reach Shortlist on aggregator
  facts" (nothing gates Shortlist); `longlist_report.md:304` "the student knows it was checked"
  (Warnings "None" can't check cost when there is no budget). Default wording: "Every row says
  whether its facts came from the university's own page." Evan's wording, so Evan's edit.
- **V3. Why nine students picked only one university.**
  [decide_report.md](product_report/decide_report.md) guesses it is the poster's "pick 1 uni to go
  deep on"; no student has said so. Ask two or three of them before that report is shown outside.
