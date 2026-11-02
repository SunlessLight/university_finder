# Build log: hand-off between sessions

Every working session **reads the newest entry first** and **adds an entry at the end**. Newest entry goes at the bottom. Add only; don't rewrite old entries. Current status is the Now box in `STATUS.md`, not here.

Entry format:

```
## YYYY-MM-DD · <task or topic>
- Done:
- Decisions (and why):
- Problems / lessons:
- Next step:
```

---

## 2026-10-21 · Claude toolkit rollout (toolkit PLAN.md T14)
- Done: project copies of `/commit`, `commit-drafter`, `/catchup` and `/mentor` moved to `archives/` (global or template versions replace them). CLAUDE.md rewritten to the claude-md-layout (≈3,370 → see toolkit PROGRESS.md). Adopted project-status (`STATUS.md`, this log, `/catchup` skill), advisor (`/mentor` skill + `mentor` helper, brief merged into `business/launchx/mentor.md`), decision-log (`decisions/log.md`). Agent/skill descriptions shortened; finished-history lines moved out of the memory index.
- Decisions (and why): see `decisions/log.md` 2026-10-21.
- Problems / lessons: `notes/` is gitignored, so moved text can't go there. A second colon in an unquoted `description:` can break frontmatter, so descriptions are quoted.
- Next step: Evan reviews the diff and decides whether to commit.

## 2026-10-21 · Catch-up + R10 decided
- Done: `/catchup` checked the Now box against the files. Toolkit rollout is committed (8f330de). `business/launchx/status.md` still listed R13 as blocking Part A, but R13 was done 20 Oct (bbd68fb), so that line was fixed. R10 decided and ticked in `business/additionals.md`.
- Decisions (and why): R10, keep the predicted grades in the sample pack as an example. Nothing ties them to a real person (stand-in name, no school; the real name is absent from the pack and prototype, checked). See `decisions/log.md`.
- Problems / lessons: a backlog fix ticked in `additionals.md` doesn't update `launchx/status.md` by itself. Check both when closing an item a status note names.
- Next step: finish iLabs Part A (Drive folder of screenshots + samples); nothing in the files blocks it now. Rehearse with `business/launchx/qa_drill.md` on 23 Oct.

## 2026-10-22 · Mentor: iLabs check-in feedback
- Done: Evan finished Part A and showed Parts A + B at the iLabs check-in. Feedback and the two open questions (edge vs ChatGPT, one-time vs B2B) recorded in `business/launchx/status.md`. Short web search on how AI-wrapper businesses build an edge (summary in the chat; not saved).
- Decisions (and why): pre-sell to the 24 survey leads before fixing bugs, so fixes match what paying customers see. See `decisions/log.md`.
- Problems / lessons: none.
- Next step: draft the RM50 pre-sale message; send after 24 Oct.

## 2026-10-23 · Backlog catch-up + mentor: targets, pricing, panel questions
- Done: `/catchup` on the backlog: 41 done, 24 open, nothing touched since 22 Oct; three finished human-lane rows crossed out (a5b01e7). Mentor talk recorded in `business/launchx/status.md`. Notion task "Get feedback from students who tried the list" created (URP Marketing, Not Started). Token-log line added to "Done when" in workflows 03, 04 and quick report (until 2 Dec).
- Decisions (and why): 20 paying by 2 Dec, else decide by 10 Dec; paid customers get the Google Form after payment; report RM30, list RM50; referral reward = free one-university report. See `decisions/log.md`.
- Problems / lessons: personalisation is invisible in the product (testers didn't understand the score), not only unmarketed. `token_cost_report.md` #1 heading carries a student slug in git: Evan to confirm whether it is a real name.
- Next step: slide 10's three merged questions, then the panel on 24 Oct; count leads 25 Oct.

## 2026-10-24 · Panel done, track flip-flop, catch-up
- Done: LaunchX Bootcamp 2 panel (feedback: "ChatGPT can do it"). 4 of 29 leads paid a deposit. LaunchX files and stage explainers moved into folders (00bea30); LaunchX notes trimmed (0292c2f). `/catchup` rewrote the stale Now box.
- Decisions (and why): main track went B2B, then back to families the same day once 4 deposits came in; bar = 20 paid family lists by 2 Dec; cap 20 spots. See `decisions/log.md` 24 Oct (three entries; the last one stands).
  Then: nudge sent (Evan). `deck_content.md` slides 2, 3, 4, 7, 8 and `2min_elevator_pitch.md` updated (survey blanks filled, 4 deposits, booth pilot, 20–30 universities); `survey.md` results recounted from the CSV (84 rows, totals only). Four Notion tasks under URP Marketing: ask payers, update spreadsheet, make the bunting, plan the pilot.
- Problems / lessons: the sheet marks 32 messaged vs 29 leads in the notes; the pre-sale message said lists "ready by 10 Nov" vs 2 Nov in the notes. Evan to confirm both. `survey.md` question 9 was the draft wording; the live form already said 20–30 universities.
- Next step: 25 Oct spreadsheet + payer question (see Now box).

## 2026-10-25 · Real lead count, deck as the only slide source
- Done: committed the 24 Oct updates (9e8fe36). Recounted from Evan's updated form export "(3)" (totals only): 19 real leads, not 29/32 (17 numbers typed by accident, most other boxes are comments); 4 deposits, RM80, 0 strangers, 2 lists + 2 reports. `status.md`, `survey.md`, the elevator pitch and the Now box updated. `deck_content.md` deleted; mentor.md, the catchup skill and business/README now point to the claude.ai Slides deck.
- Decisions (and why): the claude.ai deck is the only copy of the slides; demo day gets a copy, not an edit of the 24 Oct deck. See `decisions/log.md`.
- Problems / lessons: two copies of the slides (an .md draft and the real deck) drifted apart, and a session edited the wrong one. Only 2 of the 4 deposits count toward "20 paid lists" because 2 are for reports.
- Next step: ask the 4 payers the ChatGPT question; count the 19 on 27 Oct.

## 2026-10-25 · Backlog: form answers close I2 and I5, decide S9
- Done: Evan added halal/prayer ticks and a lesson-language question to the live form and counted 3 budget options. `workflows/01_intake.md` now matches the form (3 bands, 8 preference ticks, new question noted as not yet read by the program). `business/additionals.md`: I2 and I5 ticked, S9 decision recorded, group 2 steps 3 and 5 and the decision/human-lane tables updated.
- Decisions (and why): ask lesson language, not years in English, because students can answer it. See `decisions/log.md`.
- Problems / lessons: the "perferences" typo in the form title is what the program matches on; fixing the spelling would blank every student's preferences silently. Evan kept it.
- Next step: group 2 step 3 (read the new question into the profile) before the first paid form is read in; needs a fresh form export first.

## 2026-10-25 · Catch-up, mentor chat, this week's task order
- Done: read the tester feedback forms (`data/feedback/`, to 21 Sept) and two payer/lead chats. `business/launchx/status.md` now has a numbered "This week, in order" list (payers asked → nudge testers who haven't replied → follow up with those who did → ChatGPT side-by-side test) and two new Known rows. Notion: tester-feedback task rewritten; two tasks added (nudge, ChatGPT test due 30 Oct).
- Decisions (and why): product work = what testers actually read plus the ChatGPT test, not a rebuild; the test doubles as the booth demo.
- Problems / lessons: payers corrected by Evan: 5 said yes, 4 paid (2 willingly, 1 to support him, 1 after a push and a discount; the 5th said yes, no deposit). Evan calls the 2 willing ones strangers; the sheet says 0 strangers paid, so check. Paid lists are due **10 Nov** (decision log); every "2 Nov" in status, Now box and additionals.md changed. Notion: "Find better ways…" became "Plan how to get more people (referrals from the 29 testers)", the end of a new tester chain: update list/report (target 7 Nov) → send testers the better version → ask for referrals. Pasted chats sit in `business/` and name people: move to `notes/`.
- Next step: nudge testers (task 2).

## 2026-10-25 · intake_report.md checked against the repo
- Done: `business/product_report/intake_report.md` brought up to date: halal/prayer ticks, the lesson-language question (and that the program doesn't read it yet), "universities in mind" now used, Stage 8 in the stages table, the testing-only consent switch, "about five minutes", and the corrected budget breakdown. `business/additionals.md`: I3 corrected (the 5 "no saved answer" records do have answers), U1 settled at five minutes, I1/I2 note the report caught up.
- Decisions (and why): the form claim becomes five minutes (Evan), not timed.
- Problems / lessons: closing a backlog item updated the files under its "Where", never the report that first quoted the problem, so the report went stale. The I3 error was copied from the same 10 Oct session into both files.
- Next step: Evan puts the formal consent text on the form (title must keep "consent", label must not start with N), then update `workflows/01_intake.md` and report item 7. Poster "2 minutes" (line 772) is Evan's.

## 2026-10-25 · Fresh tester feedback count
- Done: Evan downloaded fresh replies to both feedback forms. New who-replied note `data/feedback/feedback_report_2026-10-25.md` (4 more report replies; none new on the list form). Task 2 in `business/launchx/status.md` and the two Notion tester tasks (nudge; follow-up) now carry the new counts and file.
- Decisions (and why): tofu and zephry are Evan's test students, so they are out of every tester count (27 real testers, not 29).
- Problems / lessons: the report form gained an "Any additional feedback?" question, so its rating column moved; read columns by heading, not position.
- Next step: nudge the 4 who missed both forms, then the rest (task 2).

## 2026-10-26 · Backlog: form-questions tool, budget options, consent
- Done: `business/additionals.md` gained I10 (tool to read the live forms' questions), I11 (budget options become 500000 / 1000000 / 1500000) and I12 (formal consent is live; the workflow and report still describe the casual one), grouped as group 2 step 11, which runs before step 3. I3 decided (Evan asks five students). STATUS Now box points at step 11.
- Decisions (and why): budget stays secondary, no new warnings; build the form tool. See `decisions/log.md`.
- Problems / lessons: the budget question is found by "total budget"/"whole degree" in its title, so a rename to "What's the limit?" would blank every budget. Plain-digit options already parse today, but two only via the legacy fallback.
- Next step: group 2 step 11.

## 2026-10-26 · Form-questions tool, Sheets via Drive, Notion mirror
- Done: I10 built (`tools/fetch_form_questions.py`, `questions` action in `Code.gs`, docs in README setup step 5, `01_intake.md` step 0, CLAUDE.md). `--check` tested on a made-up intake form: caught every planted problem and shows the I11 budget trap (500000 / 1500000 only via the legacy fallback). Google Sheets need no tool: the Drive connector reads them (noted in CLAUDE.md). New Notion page "Shortlisted — Now" under Everything; CLAUDE.md → Status now mirrors the Now box and matching tasks to Notion at session end, and `/catchup` pulls Evan's phone ticks back first. Bunting deadline (27 Oct), payer replies and the done nudge logged.
- Decisions (and why): Notion is a one-way copy of the files except task ticks; summary on one page, tasks stay in the Tasks database. See `decisions/log.md`.
- Problems / lessons: form settings like "collect email addresses" are not form items, so the question list never shows the email column; the check must not require it. The auto-mode classifier blocked one Notion task rename ("27 testers" → 29); the other went through. `.env.example` could not be opened, so it lacks the new FORM_ID keys. The sample spreadsheet shows "$" on the MYR total column.
- Next step: bunting design by 27 Oct. Then Evan's part of I10 (paste Code.gs, New version, Allow, form IDs in .env) and one real `--check`; then I12 and I11.

## 2026-10-26 (later) · Form access: first live run, and a one-door proposal
- Done: committed `e69b19c` and `6a39485`. Evan pasted the new `Code.gs`, deployed a new version and added the three form IDs to `.env`. First real `fetch_form_questions.py` run reached the new action (token and version fine) but failed: the script has no Forms permission yet. Backlog R20 written (Claude as project manager / advisor / marketing director, after 10 Nov). CLAUDE.md's Drive-connector line corrected.
- Decisions (and why): none final. Claude proposed an `answers` action in the same script so all four forms (incl. the survey, which has no answer tool) come through one door, and the feedback sheets can stop being "anyone with the link". Waiting on Evan's "go".
- Problems / lessons: deploying a new version does not ask for new permissions; only running a function in the editor does (`authorizeForms`). The Drive connector returns only sample rows, so it is no answer source. The Drive connector can't list Google Forms.
- Next step: Evan says go → build `answers` → Evan pastes, New version, runs `authorizeForms`, Allow → fetch and `--check`.

## 2026-10-27 · Form access working: all four forms, questions and answers
- Done: `answers` action in `Code.gs` + new `tools/fetch_form_answers.py` (f433672). Evan pasted, deployed and ran `authorizeForms`. All four forms' questions saved to `forms/*.json` (9822ac6) and answers to `data/form/intake_answers.csv` + `data/feedback/*.csv` (intake 10, report fb 12, sheet fb 15, survey 84 = the manual export). README setup step 5 fixed (permission comes from running a function, not deploying).
- Decisions (and why): `answers` is read-only even for intake (never creates `Ingested at`), and a separate tool from the questions one, so personal data can never land in tracked `forms/`. See `decisions/log.md`.
- Problems / lessons: `FORM_ID_INTAKE` held a wrong ID (Evan thought the script wanted the spreadsheet ID; it wants form IDs). Found by calling `questions` with no ID: the sheet-link fallback worked. The first `--check` found the live intake form has drifted from `ingest_form_csv.py` (F1–F6 in the carry-over); worst: the renamed grades grid would blank every new student's grades. Nobody has answered since 14 Oct, so no student is affected yet.
- Next step: fix F1 + F6 in code, Evan fixes F2/F3/F5 in the form, rerun `--check`.

## 2026-10-27 (later) · Intake form drift fixed, check clean
- Done: `ingest_form_csv.py`: grades marker widened to "grades for your subjects" (F1); "Doesn't matter" = 0 in the priority grid (F6); "what are you applying with?" reconnected to `grade_status`; two renamed course titles + spaced-hyphen separator ("Psychology - …") so all 38 courses match. `fetch_form_questions.py`: comma check narrowed to the split fields (needs, countries, location prefs). Evan had already switched courses and budget to dropdowns and filled the consent retention (F2, F3, F5). Live `--check` exit 0; a fake student built from the live headers gives grades, course, grade_status and all 8 priorities. `01_intake.md` and `google_form_notes.md` updated to the new wording.
- Decisions (and why): "Doesn't matter" ranks last instead of being skipped, because `derive_weights.py` refuses a priorities list missing any of the 8.
- Problems / lessons: the check also caught 3 course names that never matched (all non-regulated, so no student harm). Consent retention is now 3 months, not 12.
- Next step: Evan answers what the secondary-school and lesson-language questions should feed (F4; lesson language = backlog S9 step 3). Commit. Then I12, I11, feedback-sheet switch.

## 2026-10-27 (evening) · Last two intake questions now read (F4)
- Done: `ingest_form_csv.py` maps "What did you take for ur secondary school?" → `secondary_qualification` and the lesson-language question → `english_proficiency.lesson_language`, both verbatim; `init_student.py` template has both keys. `--check --offline` now has 0 unmapped headers (exit 0); a fake response from `forms/intake.json` gives "SPM" and the DLP answer word-for-word, no review flags. Calendar tests pass. `01_intake.md` and S9 in `business/additionals.md` updated.
- Decisions (and why): raw answers now, years rule later (S9), so no paid student's answer is lost meanwhile; 3-month consent retention kept (Evan confirmed). See `decisions/log.md`.
- Problems / lessons: none.
- Next step: I12 and I11 (backlog group 2 step 11), then the feedback-sheet switch.

## 2026-10-27 · Files and Notion tasks synced
- Done: `/catchup` sync of `business/launchx/status.md` with the Notion Tasks (URP Marketing + Product Developing). Phone tick brought back: "Message the testers who did fill them" (Notion "Get feedback from students who tried the list", Done). Evan's Notion replan of this morning found: the ChatGPT test was renamed "Make sure the whole workflow is all verified information" and moved to Product Developing (28 Oct); "List down the stuff to improve…" (28 Oct) is tester-chain step 1. File now carries those names and dates. Notion: referrals task moved to 3 Nov, Not Started, "27" → 29 testers; three new URP Marketing tasks (consultancy chats; counsellor / parent / "too expensive" / has-a-list chats; low-priority tester and The Sun checks). Now box and "Shortlisted — Now" page updated.
- Decisions (and why): pilot plan due today, not 31 Oct (Evan: the submission is today), so the ChatGPT test feeds the booth demo, not the plan. Referrals stay last in the tester chain (after testers see the better version).
- Problems / lessons: Evan's own Notion-only tasks left alone ("Send reminder to all that ignored me", "Message 50 parents", the Product Developing fixes). Not made into tasks: "park big-problem ideas" (a habit, not a to-do) and the mentor-session items (Claude's own). A second session was editing STATUS.md at the same time.
- Next step: submit the bunting and the pilot plan today.

## 2026-10-27 · Bunting wording from the customer chats
- Done: bunting text written into the Notion task "Make the bunting and booth materials" from `notes/customer_chats/` (Dakshi, Ilsa, Vee Shen): headline "Don't know where to apply? We'll find them for you.", smaller line (Evan's) "20-30 Universities picked for YOUR course, grades and countries", proof line "Facts from each university's official page.", plus spare and dropped lines with reasons. Backlog L5 + group 2 step 12 added (a source per fact, "Not found on official page").
- Decisions (and why): ChatGPT is not named on the bunting; the proof line answers it. No "fit you" claims. See `decisions/log.md`.
- Problems / lessons: "Universities that fit you" over-promised (the list searches by course + countries and ranks). Old sales files still say "fit" and "20-40" (`business/sales/scripts.md:54`, `service-tiers.md:40`, the old poster); not fixed yet.
- Next step: submit the bunting and the pilot plan today.

## 2026-10-27 (night) · Backlog step 11 done: consent (I12), budget (I11), feedback switch
- Done: I12: live consent checked (title has "consent", option starts "I agree", placeholders filled, 3 months); `01_intake.md` and `intake_report.md` item 7 describe the formal text. I11: live budget options are `500,000` / `1,000,000` / `1,500,000` with commas; new `BUDGET_LIMIT_EXACT` in `ingest_form_csv.py` matches them exactly before the substring list (`500,000` is inside `1,500,000`); old exports unchanged; `--check` shows no fallback route. Feedback: `fetch_form_answers.py` re-run (12 + 15 answers), `tools/fetch_feedback.py` deleted (Evan said yes), CLAUDE.md pointer updated. `intake_report.md` item 5 now says lesson language is stored. Calendar tests pass.
- Decisions (and why): delete the public-CSV feedback reader so the sheets can go Restricted; the script route runs as Evan and doesn't need public sharing. See `decisions/log.md`.
- Problems / lessons: the backlog assumed plain digits; Evan typed commas, so the exact match ignores commas and spaces.
- Next step: Evan sets both feedback sheets to Restricted, then rerun `fetch_form_answers.py --form report_feedback spreadsheet_feedback`. Optional: add `Not sure` to the budget dropdown. Then group 2 step 3 (S9 years rule, S3, R5).

## 2026-10-27 (late) · Backlog group 2 step 3: years-in-English rule (S9), slider notes (R5)
- Done: S9: `LESSON_LANGUAGE_YEARS` in `ingest_form_csv.py` turns the lesson-language answer into `english_proficiency.years_in_english_min` (a floor: 5 / 1 / 0, null for DLP and Not sure; "Other" = null + `_needs_review`). Template, `01_intake.md`, `08_application_prep.md` and the glossary IELTS line updated. UK half checked on official pages (UCL, Imperial, KCL): no waiver for English-taught schooling in Malaysia. R5: three slider comments fixed. Tested all six form answers, an "Other" answer and a blank through `map_row`; `--check --offline` ok; calendar tests pass.
- Decisions (and why): store a floor, not a guess (pre-university length varies, so "pre-U only" = 1, which clears no waiver read so far); DLP stays null (grey area). See `decisions/log.md`.
- Problems / lessons: four student cells already claim a UK waiver that does not exist (new backlog R21, needs Evan's yes). S3 still waits on Evan's income decision.
- Next step: Evan's yes on R21 and his S3 decision; otherwise the 28 Oct ChatGPT test.

## 2026-10-27 (late, 2) · R21: four wrong UK English cells fixed
- Done: Evan said yes. Four `English req` cells (one student's UCL, Imperial and KCL Shortlist rows; the source student's Imperial Finalist row) rewritten via `apply_backfill.py --overwrite` from `.tmp/r21/`, dry run first, backup in the session scratchpad. Each now gives the course's level (read on each course page via Firecrawl) and the accepted English grade. `check_master_list.py`: no new findings; exactly 3 + 1 cells changed.
- Decisions (and why): no `status.md` line, because the first student's is already over its 3000-character budget; the record is in `research_notes.md`.
- Problems / lessons: the same guess is wider: ~40 cells on 11 lists tie a waiver to A-Levels or English-medium schooling (R21 sweep, Shortlist/Finalist first).
- Next step: Evan's S3 decision; the R21 sweep after the 10 Nov lists.

## 2026-10-27 (evening) · Bunting redesign: designer feedback, demo website as the picture
- Done: mentor chat only, no code changed. Evan's first bunting draft (`business/launchx/Bunting_design/1.png`) reviewed against the Notion brief; a designer's feedback (no context, name before the pain, bland, A-level students away during the booth) worked into a new layout. Found the intake form's grade grid takes A-level grades only. Found the demo website's code is `prototype/`, fed from `business/sales/sample_pack/sample_master_list.csv` by `prototype/_build/gen.py`.
- Decisions (and why): the bunting shows the demo website's list, cropped in a device frame, because customers get that website (plus a spreadsheet download), so the picture matches the product. See `decisions/log.md`.
- Problems / lessons: none in code. The two status.md drafts (designer feedback; website delivery) were not written: Evan has not said yes.
- Next step: Evan's "go" on the demo edit plan in `plans/carry-overs/2026-10-27-bunting-redesign.md`.

## 2026-10-27 (late, 3) · S3 decided: no family income in the record
- Done: nothing built. Evan decided S3 in chat.
- Decisions (and why): the system never collects family income (sensitive; students rarely know it). US need-based finalists get the university's own published income-band examples plus a CSS Profile link instead. Claude suggested also linking each university's net price calculator (the CSS Profile applies for aid, it does not estimate it); waiting on Evan's "go". See `decisions/log.md`.
- Problems / lessons: none.
- Next step: on Evan's go, edit `04_university_report.md` (Costs / `net_cost`), `08_application_prep.md` (financial aid `covers`), the `build_report.py` sample line, close S3.

## 2026-10-27 (late, 4) · S3 closed: income-band examples instead of a "your share" figure
- Done: `workflows/04_university_report.md` step 10 (Costs) and its `net_cost` example, `workflows/08_application_prep.md` Financial aid `covers`, the `application-guide` skill's `covers` line, and the `net_cost` sample + docstring in `tools/build_report.py` now ask for 2–3 of the university's own income-band examples (USD + approx MYR, dated), its net price calculator link (or "none for international students") and the CSS Profile link. S3 ticked in `business/additionals.md` (+ the round table, decisions table, step 3 row, items 277/300). Checked: `build_report.py` parses.
- Decisions (and why): net price calculator link included (Evan's "go" on Claude's default), because the CSS Profile applies for aid and does not estimate it. Workflow examples use placeholders, not real MIT figures, so a helper can't copy an unverified number.
- Problems / lessons: none. The existing MIT report still carries its old income-based figure; it changes only when rebuilt.
- Next step: the R21 sweep after the 10 Nov lists (one student per session).

## 2026-10-28 · Backlog decisions and trim
- Done: `/catchup` on the backlog: I10 ticked (proven live 27 Oct, `9822ac6`). Evan decided L2 (22 rows first), D2 and P2 (no; free testers), D5 (source student finished). `business/additionals.md` rewritten from 1,782 to ~270 lines: open entries only, one numbered step list (before / after 10 Nov), a "closed without a fix" list. Four lines in `decisions/log.md`; `business/README.md` and the backlog memory updated.
- Decisions (and why): the source student's list stays fixable only where the sample pack and demo website show it (new SP1: seven wrong cells), because customers see those. R16 apply, R17 and R21 merged into one per-student step, because they rewrite the same list.
- Problems / lessons: R22 (new): the 27 Oct "never assume an English waiver" rule went only into Stage 8, not into the row-filler that wrote the wrong cells. Also R18's UK living-cost rule was decided on 20 Oct but never written into `uk.md`.
- Next step: Evan's yes on R22, then backlog step 1 (R22 + R18), then step 2 (SP1), both before 10 Nov.

## 2026-10-28 (evening) · Bunting submitted
- Done: `/catchup` found the demo edit already committed on branch `bunting-demo` (`d123f53`, the carry-over said "not started"); Now box fixed. Wrote Evan a step-by-step Canva build sheet and tightened his problem/solution lines. Built a throwaway `prototype/bunting-shot.html` in the worktree (resize and hide columns, cells and badges wrap, drag stops at the longest word); tested in Chrome via a local server, not committed. Evan submitted `business/launchx/Bunting_design/SHORTLISTED_v3.png`. `business/launchx/status.md`, the Now box, SP1, the carry-over banner and Notion updated.
- Decisions (and why): see `decisions/log.md` (all pre-U badges, QR to a Linktree of samples, problem/answer pairs, no PDF or ChatGPT claims).
- Problems / lessons: the bunting prints MIT's "Well above" (a known-wrong SP1 cell), fine once SP1 lands. Table columns can't be narrowed by width alone (the table stretches them); pin every column on the first change and shrink-wrap the table.
- Next step: the pilot plan (overdue), then the intake-form question for non-A-level students before 10 Nov.

## 2026-10-28 (2) · Backlog step 1: R22 + R18
- Done: `.claude/agents/row-filler.md` and `workflows/03_discover_longlist.md` (Edge cases) now say the `English req` cell gives the test bar, and a waiver only in the university's own words; never "likely waived" for A-Levels or English-medium schooling. `workflows/countries/uk.md` got the living-cost rule (no university figure → UKVI monthly maintenance figure × 12, read on the day, said in notes). R22, R18 and the step 1 row deleted from `business/additionals.md`.
- Decisions (and why): Evan said yes to R22. The rule went into both the helper's sheet and the Stage 3 workflow, because the helper writes the cell and the main session checks it.
- Problems / lessons: another session (bunting) was editing the backlog and STATUS.md at the same time; bookkeeping waited until it finished (backlog rule 5).
- Next step: backlog step 2 (SP1), after merging `bunting-demo`. Not tested on a live row yet: check the first 10 Nov list's `English req` cells for "likely waived".

## 2026-10-28 (3) · Backlog step 2: SP1 (sample pack + demo website)
- Done: merged `bunting-demo` (`d123f53`, no overlap with main). Source list: five US rows' `Grades vs entry bar` → "Not published" via `grade_fit_label` (admission overrides unchanged, asserted), Cambridge `English req` corrected from its official page (test waived only for majority English-speaking countries), Cambridge 2027/28 fee ported from the demo branch (`apply_backfill.py --overwrite`, MYR total via `candidate_total_myr`), 6 `score_log.jsonl` lines. `build_sample_pack.py` lists Cambridge, not Oxford, in the bunting order. Sample CSV + glossary rebuilt and leak-scanned; `data.js` regenerated; the demo's "clear the bar" sentence now counts only universities that publish a bar. Checks: `check_master_list.py` 0 findings, `smoke.js` 147/147.
- Decisions (and why): the demo branch's hand edits were moved into the source list and build script, because a rebuild from source would have undone them. See `decisions/log.md`.
- Problems / lessons: the demo branch had hand-typed a 212-char Notes cell (budget 200); the backfill tool caught it. `pypdf` is missing, so the leak scan crashes on the PDFs (R24); the PDFs' sources predate their last scanned build, so the committed PDFs were kept. New: R23 (Rose-Hulman, Northeastern grade labels), R25 (uk.md fee year).
- Next step: backlog step 2b (R24 needs Evan's yes on installing `pypdf`).

## 2026-10-28 (4) · R24 closed, old demo worktree removed
- Done: `pypdf` 6.21.3 installed into `.venv` (Evan's yes) and listed in `requirements.txt`; full `build_sample_pack.py` run with `.venv`'s Python: "Scan clean" incl. both PDFs (rebuilt PDFs differed only in build bytes, so the committed ones were kept). Worktree `.claude/worktrees/bunting-demo` removed (Evan's yes; its commit is merged, only the throwaway `bunting-shot.html` was in it). The merged branch label `bunting-demo` is left.
- Decisions (and why): none new.
- Problems / lessons: the system `py` has no `pypdf`; run the sample pack build with `.venv/Scripts/python.exe`.
- Next step: backlog step 2b (R23, R25).

## 2026-10-28 (5) · Fact audit: guesses, advice and chatter
- Done: Evan asked whether the system keeps everything "factual, information not advice". Nine read-only helpers audited one part each (intake, longlist instructions, scoring and checks, spreadsheet text, report instructions, report tools, decide and apply, a count-only sweep of every student's generated files, promises vs reality). Reports in `fact_audit/` with `00_START_HERE.md` (top 10, products, decisions). 282 findings, 139 High; counts recounted from the files; no student named (checked against every folder name). Three findings spot-checked in the code. New backlog R26-R37 with steps 2b, 2c (before 10 Nov), 9 and 10; R36 joins L5 in step 7. Plan: `plans/fact_audit_plan.md`.
- Decisions (and why): none of Evan's yet. Claude's defaults, for Evan to confirm: keep the score/label columns but explain them as "our label" (R32); report opinion goes in one labelled box (R34). Judgments are part of what families pay for, so they get labelled, not deleted.
- Problems / lessons: no automatic check looks for hedge, advice or chatter words (spreadsheet or report), so the "official pages only" rule is written down but not enforced; 58% of "Official page" rows hold a hedge word. The intake form's lowest budget choice is RM 500,000 (R26).
- Next step: Evan's form edit (R26) and sales wording (R37); then backlog step 2b, then 2c, all before 10 Nov.

## 2026-10-29 · Audit decisions settled; the student list becomes a PDF
- Done: Evan's four fact-audit decisions logged (all defaults). R26: Evan added a RM 200,000 budget choice; `ingest_form_csv.py` reads it directly (form check clean, `forms/intake.json` refreshed). New `plans/discussions.md`, one running file for ideas and open questions (CLAUDE.md points to it). New `plans/list_pdf_plan.md`: 9 tasks in 5 stages replacing backlog steps 2b/2c. Counted for the plan (27 real lists, counts only): Annual tuition has extra text in 28% of cells, Total 16%, Living 9%; rank cells average 31-68 characters; script-filled columns are 100% clean.
- Decisions (and why): portrait PDF replaces the spreadsheet download (a CSV has no formatting and one sheet, so the glossary was a second file); columns 35 → about 26 for students (drop Tier, Notes, Student grades → profile; Student life → report; Money to show → apply guide; merge City+Country and the scholarship columns); numbers only in money and rank cells; new Application requirements (fixed vocabulary) and Checked on columns; a missing deadline is "Not published", Info source shows "Official page, checked on <date>"; script-made cost breakdown per university; List status hidden now, removed after 10 Nov; the CSV keeps every column until after 10 Nov; website stays a demo. All in `decisions/log.md`.
- Problems / lessons: decision 3 (2026-10-28) and R29 had two different wordings for the same cell; caught before any code changed. Pricing worry raised (RM 50 for 20-30 universities): only one cost measurement exists, so the next step is `/cost` + hours on the first paid lists (`plans/discussions.md` O5-O7).
- Next step: Stage 1 of `plans/list_pdf_plan.md` (T1, T2, T3 in three sessions).

## 2026-10-29 (2) · List PDF plan T1: form reader
- Done: `ingest_form_csv.py` reads "Forecast Grades" as `predicted` (R27, `1db2d35`) and puts Urban+Rural-both-ticked on the Stage 1 `_needs_review` list instead of every row's Warnings (R29 part). Form check clean. Evan then made the Location question a one-choice dropdown (no "Other"); check still clean, `forms/intake.json` refreshed, reader comment updated. R27 closed; its leftover (7 old profiles with the wrong grade type) is new backlog R38, step 4.
- Decisions (and why): fix old profiles by hand on Evan's yes, never by `--force` re-ingest (it wipes Stage 1 edits); the 10 Urban+Rural profiles are left alone (T3 drops the stamp, the dropdown stops new ones).
- Problems / lessons: profiles don't keep the raw grade-type answer; counting needs the form export, matched by email.
- Next step: Stage 2 of `plans/list_pdf_plan.md` (T4, T5, T6) once T2 and T3 are committed.

## 2026-10-29 (3) · List PDF plan T10: weights from tick points
- Done: `ingest_form_csv.py` now keeps the tick levels as `preferences.priority_levels` (Must have 3 … Doesn't matter 0). `derive_weights.py` weights from them when present (points ÷ total); older profiles with only `priorities` keep the rank formula, proved identical to the committed code on a made-up profile. `scoring-weights` skill and the tool's docstring updated (stale Urban+Rural mention fixed). Checks on `.tmp/t10/` fakes: all Must have → 0.125 each; 2 Must have + 6 Important → 0.1667 / 0.1111. No student file touched.
- Decisions (and why): a key over the 0.5 cap is cut and the excess shared equally, then the `course_match` floor is funded by scaling the others down in proportion (taking it from the biggest key, as the rank formula does, could drop a Must have below an Important). A blank tick is refused, not guessed.
- Problems / lessons: first version floored before capping, which handed course match extra weight over other "Doesn't matter" topics; caught by the one-Must-have fake and swapped.
- Next step: rest of Stage 1b (T3b, T11, T12); `workflows/01_intake.md` and the `init_student.py` template still describe `priorities` only (T9).

## 2026-10-30 · T11 admit-rate sources (list PDF plan)
- Done: `## Admit rate source` added to all 10 `workflows/countries/*.md` (pointers only, no figures); T11 ticked in `plans/list_pdf_plan.md`. Australia confirmed from the dept's 2025 applications-and-offers PDF (Evan downloaded it to `data/resources/`); Singapore from the NUS Indicative Grade Profile page; China by Evan's own check.
- Decisions (and why): only USA (Common Data Set C1), UK Oxford/Cambridge and Japan (each university's 入試結果, international track) publish one; everything else is "None published", so the PDF cell will say `Not published` rather than an aggregator's guess. UCAS data counts acceptances, not offers, so no rate is derived from it.
- Problems / lessons: Chrome can't read some government PDFs as text, and Evan stopped the web-fetch helpers and an extra Chrome tab mid-run. For a page or PDF that's stuck, asking Evan to download or check it by eye was faster.
- Next step: Stage 2 of the list PDF plan (T4, T5, T6), target 3 Nov.

## 2026-10-30 (2) · T5 research instructions (list PDF plan)
- Done: `row-filler.md` has a "Fixed-format cells" rule (money, ranks, Application requirements vocabulary, Checked on = today, Admit rate only from the country file's source, deadline `Not published`) and a no-hedge-words rule; `03b_candidate_schema.md` example fragment rewritten to the new formats (every value passes `cell_format_problem()`); `03_discover_longlist.md` sentinels, column count (38) and country-constants example updated. T5 ticked.
- Decisions (and why): the formats live once, in `row-filler.md`, because backfill helpers read that file and skip 03b; the other two files point there. The Admission likelihood override stays, for balancing the Reach/Match/Safety spread only.
- Problems / lessons: three country files (Australia, China, Japan) still tell helpers to write `Not published — check portal`; outside T5's write list, so left for Evan's yes.
- Next step: the rest of Stage 2 (T4 checks, T6 PDF builder).

## 2026-10-30 (3) · T6 list PDF builder + E1 (list PDF plan)
- Done: `tools/build_list_pdf.py` + `tools/templates/list_pdf.html`/`.css` turn a `master_list.csv` into a portrait PDF (profile, summary table, label key, one card per university, glossary); `business/sales/sample_pack/sample_profile.json` is the anonymised "Arif". Evan read the sample (E1) the same day; after his points: label key cut to one sentence each (`JUDGMENT_LABELS`), a "Useful links" block per card (`OFFICIAL_LINKS` in `apply_glossary.py`, 12 official sites opened today), and no notes to ourselves on the page. Plan amended: Decisions items 7, 11, 12; new tasks T3c + T5b (Apply link, Scholarship link columns).
- Decisions (and why): each card's RM total prints the row's own `Approx total (MYR)`, so card and summary never disagree. A messy money cell or a total that doesn't add up now stops the build (listed on screen) instead of printing a note; `--draft` makes a review copy. A system named only as "not X" gets no link (MIT is "not Common App").
- Problems / lessons: my first build printed "Figure needs re-checking: … we used the first number" on 9 cards because the T6 prompt asked for a mark; a note about our own process never belongs on the student's page. The sample builds only with `--draft` until T7 (12 money cells hold old caveat text; Admit rate and Application requirements blank). T7 leads: Cambridge's passed deadline with Warnings None; Monash/Melbourne say "UAC International".
- Next step: Stage 3b (T3c, T5b, two short sessions), then T7.

## 2026-10-30 (4) · T3c Apply link + Scholarship link columns (list PDF plan)
- Done: `shortlist_schema.py` appends `Apply link` and `Scholarship link` (40 columns now), each one `https://` URL or `Not published` (`LINK_FORMAT`, checked by `cell_format_problem()`); `merge_candidates.py` requires and checks `apply_link`/`scholarship_link`; `sync_shortlist.py` writes them. T3c ticked.
- Decisions (and why): a link must be `https://` plus a dotted host (so `https://` alone or `http://` fail), because the PDF prints it as a clickable link and a broken one reads as breakage.
- Problems / lessons: none. Old lists upgrade in place with the two cells blank (checked on a `.tmp/` copy of the sample).
- Next step: T5b (row-filler sheet names the two fields), then T7.

## 2026-10-30 (5) · T7 sample re-check, part 1 (list PDF plan): researched + rehearsed, not yet written
- Done: 15 row-filler helpers (BACKFILL) re-read the sample's 15 rows on official pages into `.tmp/toru/backfill_t7/`; main session read all 30 QS ranks on QS's own data (Chrome), the Home Affairs subclass 500 living cost, and Melbourne's scholarship pages. Checker fix: `Application requirements` no longer hedge-scanned (`tools/check_master_list.py`, +1 test, 18 pass). R25: `uk.md` Cambridge fee note says "2027 entry". Full rehearsal on a `.tmp/t7/preview/` copy: backfill + recompute → check 0 findings on the 15 rows, PDF builds without `--draft`. toru's real files NOT written yet.
- Decisions (and why): see `decisions/log.md` (2026-10-30, checker exemption; Harvard mandatory fees in tuition).
- Problems / lessons: the hedge regex flagged the vocabulary item "N recommendation letters", so four helpers dropped true letter counts to pass; the write tool refuses the whole batch on one hedge. QS tables are JS-rendered (403 to plain fetch); the page's own `/rankings/endpoint?nid=` JSON in Chrome reads them. Melbourne's undergrad scholarship excludes Malaysia.
- Next step: Evan's yes, then write (carry-over `plans/carry-overs/2026-10-30-t7-sample-recheck.md`).

## 2026-10-30 (6) · T7 sample re-check, part 2 (list PDF plan): written, T7 ticked
- Done: on Evan's yes, backed up toru's three files to `.tmp/t7/backup/`, then wrote 264 cells + 15 research-notes sections with `apply_backfill.py --overwrite` and recomputed (15 changes, 2 score_log lines). Result is byte-identical to the rehearsal copy. The 15 rows pass `check_master_list.py` with 0 findings; the PDF builds without `--draft` on a redacted copy; 18 tests pass. T7 ticked.
- Decisions (and why): Melbourne's fee stays `AUD 333,760`. Read in Chrome after the write: 2027 BSc total AUD 181,310–211,405 and Master's AUD 66,752/yr (220,950 for 3 years), so 3 + 2 years comes to AUD 328,610–358,705 and the figure sits inside that range.
- Problems / lessons: Melbourne's fee pages only show the international fee after the "International students" option is clicked, which is why helpers kept reading the domestic view. Chrome blocks northeastern.edu, so that row's requirements stay unread. The MQA register opens in Chrome but wasn't run. toru's other 28 rows still fail the checks (old format, not in the sample).
- Next step: T8 (rebuild the sample pack); read the T7 row's "T8" note first.

## 2026-10-30 (7) · Mentor session: time on bugs, the database idea, survey recount
- Done: downloaded the survey's live questions and all answers, recounted `business/launchx/survey.md` at 103 rows (22 real leads, 7 deposits RM110, 1 stranger paid, why people said no) and brought `business/launchx/status.md` and the Now box up to date.
- Decisions (and why): no university database before 2 Dec, because tools are a flat RM158 a month, so it saves little and adds a system to maintain. No freeze: Evan keeps building in set time alongside marketing (the mentor advised stopping new columns and checks; Evan's call). Pilot pass line: 5 paid sign-ups across the 4 booth days, a guess. All in `decisions/log.md`.
- Problems / lessons: the sheet's "by accident" column holds the text true/false, so a blank check counted every row as an accident. I wrote "the 2 other payers came another way" into survey.md unchecked; they came from the 7 emails, and that was the finding (email 2 of 7, WhatsApp 5 of 22, small numbers). Read Evan's Reason column first: it already held 7 reasons for "no".
- Next step: finish the pilot plan; Evan says which product the 3 new payers bought.

## 2026-10-30 (8) · T8 sample pack rebuilt with the list PDF (list PDF plan)
- Done: `build_sample_pack.py` also builds `sample_list.pdf` (14 universities, 22 pages, no `--draft`) and scans it; all five pack files rebuilt from toru's re-checked list. Demo website's list button now opens that PDF in a new tab, `gen.py` carries 40 columns, the waiting screen no longer promises a spreadsheet, Apply and Scholarship links are clickable. Checks: `check_master_list.py` 0 findings, leak scan clean, `smoke.js` 147/147, real mouse click on both buttons opens the PDF. T8 ticked.
- Decisions (and why): the list buttons open a new tab instead of using `download`, matching the report button, because the T8 check says the button opens the PDF and the demo tab must stay put. The CSV stays built because `gen.py` reads it; T9 decides how the README describes it.
- Problems / lessons: the task looked like a one-line link change, but three tasks of new columns (35 → 40) had piled up behind `gen.py`'s header check. `smoke.js` failed on NUS RM 383k: the test was stale, not the data (SGD 124,780 × 3.19 = RM 398,048). The fixed-word leak scan is case-sensitive and hand-listed, so a one-off scan drawn from the source profile's real values was run too; its first filter missed `financial` and `education_history`, fixed before trusting it. `report.pages` said 19; the PDF has 25.
- Next step: T9 (docs and backlog). Open questions in `plans/discussions.md` (unconfirmed facts vs "15 of 15 rows are checked", dates passing).

## 2026-10-30 (11) · Report form gains budget, race and preferences; report first page
- Done: `REPORT_REQUIRED_KEYS` gains four questions and the "consent may not name race" check is gone. `ingest_form_csv.py` keeps exact ticks (`preferences.other_preferences`) and "muslim" sets `worship_facilities`. `build_report.py` prints "Your profile" above the Snapshot, sharing `student_items()` with the list PDF. New `faith` check in `check_report.py`. Rules written into `04_university_report.md`, `report-writer.md`, `01_intake.md`; plan and fix list updated. 90 tests pass; a made-up student's report and PDF built and viewed.
- Decisions (and why): see `decisions/log.md`. Evan overruled Claude on race and preferences: early "you can't apply" saves time, and unasked halal content reads as built for Malays. Race stays off the first page (Claude's call).
- Problems / lessons: the tick "Muslim Facilities/Halal Food" never set the prayer flag, and `needs` merges "Cold Weather" with "4 seasons", so the new rules would have hidden or lost real answers. `report_to_pdf.py` places "Key terms" by counting `##` headings, so the profile is a `###`. `sources.md` still says "surface only what they can claim"; `04_university_report.md` overrides it for reports because another session had that file open.
- Next step: Evan's fix list, then T6, which also adds the new keys to `test_report_form_questions_match`.

## 2026-10-30 (10) · Catch-up on O8/O9; MQA register read without a browser
- Done: checked O8 and O9 against the files. Read eSISRAF for the 14 sample universities with a throwaway script (three data addresses, one request a second); results in `plans/discussions.md`. Corrected `workflows/sources.md`. No sample rows or website changed.
- Decisions (and why): none final. Recommended in O13: a small live-lookup script plus a short file of matched names, no database, because 27 lists use only 207 universities and a lookup takes seconds.
- Problems / lessons: the 17 Oct note said the register needs a browser, and I repeated it, sending Evan to do 13 searches by hand. It only meant `WebFetch` couldn't read it. Loose search words land on the wrong institution, so a name match has to be checked, never assumed. A Notion `Status` filter returned nothing with no error; reading all rows worked. `04_university_report.md` still says the register needs a browser: fix it with the O13 script.
- Next step: pilot plan. Then Evan's calls on O8, O9 and O13.
- Added later: Evan wants accreditation checked inside the workflow, so R42 went into the backlog (step 2e, plan first). The course-to-body table already exists; the country-by-country table and the forced check don't. Evan's call: no testing in advance, each field gets checked when a real buyer needs it.

## 2026-10-30 (9) · Two intake forms: scripts, checker, report route, docs (intake forms plan)
- Done: `plans/intake_forms_plan.md` T1-T5 and T7, T6 half. `ingest_form_csv.py` reads both forms; new `tools/check_grades.py`; `report_orders` route (folder for a report buyer, no list); `build_report.py` stops without a master list; `check_report.py` drops the priorities row for those; dashboard shows "Report order"; row-filler told to use the bar for the student's programme. 73 tests pass (3 new test files). All 10 real sheet rows map to the same answers as before.
- Decisions (and why): code follows the forms as Evan really built them, keeping the plan's wording as a second match. An existing folder only gains the order, even with `--force`, and a same-name folder with another email is never merged. See `decisions/log.md`.
- Problems / lessons: read the live form before coding from a plan: "Type you subject and grades", "want a report of" and "Secondary school" would have silently blanked fields. A replaced question keeps its old sheet column, so every new student read as "no consent"; fixed with `merge_duplicate_columns()`. The year question became the month question, so old rows hold the year under a "month" heading. The report form has no grades question, its consent wording names race, it has no linked sheet and its ID isn't in `.env`.
- Next step: Evan's fix list in `plans/intake_forms_plan.md`, then T6, then E2.

## 2026-10-30 (11) · T6: both live forms checked against the scripts (intake forms plan)
- Done: T6. Fetched both forms and Evan's test answers, dry-ran each with nothing written to `data/students/`. Fixed double ticks on the importance grid, report orders now using priorities (`check_report.py` needs the row again, `report-writer.md`), `--check` naming a checkbox grid on both forms, and a list row no longer being told to `--force` over a report-order folder. Brought `01_intake.md`, the plan, `CLAUDE.md` and O10/O11 up to date. 97 tests pass. On the test answers the grade check passes a correct tidy-up, catches a dropped subject, and weights build.
- Decisions (and why): see `decisions/log.md`. Priorities stay on report orders because Evan added the grid; the double tick takes the higher level.
- Problems / lessons: the list form was re-linked at 22:45, so a new first tab holds today's questions only. Old answers and `Ingested at` stamps are safe in `Form Responses 1`, but the scripts read the new tab, so 10 old rows look pending with blank consent. `--check` can't see this. `fetch_form_responses.py --dry-run` added an `Ingested at` column to the new tab: it isn't quite write-free. `fetch_form_answers.py` overwrote the local `intake_answers.csv`; any earlier copy of the old tab's columns went with it, and the sheet still has them. Evan's address was used on both test rows, so they read as one buyer.
- Next step: Evan's fix list, then "recheck", then E2. Rows 2-10 of the new tab still need stamping, and the row with no folder needs Evan's call.

## 2026-10-31 (12) · Forms finished; script follows the form to its sheet (intake forms plan)
- Done: confirmed Evan's edits on the live forms (Multiple choice grids, year question, consent names); `--check` clean. Renamed `FORM_ID_INTAKE` to `FORM_ID_LIST_INTAKE`. `Code.gs` pending and confirm now take a form ID and read that form's linked tab; `fetch_form_responses.py` sends it. O10 and O11 closed. 100 tests pass; `Code.gs` passed 7 checks against fake Google objects, because it can't run locally. With the form's ID set for a single run, the list form reads 0 responses and the report form 0.
- Decisions (and why): see `decisions/log.md`. Script stays in the old sheet and follows the form.
- Problems / lessons: `.env` held the spreadsheet's ID, which gives `Invalid ID`: same mix-up as 27 Oct, so it's now in `CLAUDE.md`. The redeploy isn't proven live yet; it needs Evan's paste. The old-tab stamping question is gone: the new sheet is empty and row 11 was a test.
- Next step: Evan sets the form's ID in `.env`, pastes `Code.gs`, fixes one Malay phrase, says "recheck". Then E2.

## 2026-10-31 (13) · Catch-up on the list PDF plan
- Done: checked T1-T8 against the files: all landed; sample list clean on the new checks; 18 list tests and 61 form tests pass. No Notion ticks to copy back. Now box corrected.
- Decisions (and why): T9 should cover the handover step as well as wording, because a paying student's PDF depends on someone running the builder.
- Problems / lessons: no workflow says to run `build_list_pdf.py` at handover. Stage 3 still ends at `check_master_list.py` and the glossary sheet, and T9's file list leaves out `workflows/03_discover_longlist.md`. T9's "After 10 Nov" items aren't in the backlog yet. The 30-31 Oct forms work is uncommitted and shares files with T9. `?? data/` is one public Australian PDF in `data/resources/`, not student data.
- Next step: commit the forms work, then T9.

## 2026-10-31 (14) · T9: list PDF plan finished, docs and backlog brought in line
- Done: `README.md`, `00_overview.md`, `CLAUDE.md`, the sample pack README, `/longlist`, `notion_sync.md` and the `init_student.py` comment now describe a PDF, not a spreadsheet, and 40 columns. `03_discover_longlist.md` gained Step 8, which builds the PDF after the last country. Backlog: steps 2b, 2c and 2d closed; R23, R25, R28, R29, R32, R40 deleted; R30, R31, R39, R9 cut down; new R44-R48; new steps 2f, 11, 12. Plan marked done.
- Decisions (and why): see `decisions/log.md`. The sample CSVs stay built but aren't sent, because `build_list_pdf.py` and `gen.py` read one. R31 stays open rather than closing with the step.
- Problems / lessons: a plan's tick isn't proof that a backlog entry is finished. R31's demo line survived T7 and T8 because it is typed in `data.js`, outside the sample list the checks read. The `--student` route had never been run; it passed on a made-up folder, so nothing real was touched. The list PDF's sample wording differs from the banner the README described. Correction to entry 13: the forms work was already committed (`f436fc5`); the catch-up relied on the start-of-session snapshot.
- Next step: commit T9, then the pilot plan.

## 2026-10-31 (15) · Forms: script moved to the new list sheet, recheck clean
- Done: Evan moved the Apps Script to "List Intake Form (Responses)" with a new deployment, and fixed `.env` and the report form's Malay notice. All five forms read, `--check` passes, nothing pending. `CLAUDE.md`, `README.md`, `01_intake.md`, the `Code.gs` header, the plan and `status.md` now name the new sheet. Header comment only, so the live script needs no new paste.
- Decisions (and why): see `decisions/log.md`. Reverses today's earlier "script stays in the old sheet", at Evan's request.
- Problems / lessons: a wrong list form ID gave `No item with the given ID`, not `Invalid ID`, so both are now in `CLAUDE.md`. Running one form at a time separated it fast: four forms worked, so only that ID was wrong. With no form ID, `answers` reads the script's own sheet, so a row count shows which sheet it lives in (0 = new, not the old 10). `intake_answers.csv` looks too small to hold the 10 old students, so the old sheet may be the only full copy: not opened, size only.
- Next step: Evan backs up and deletes the old sheet, then E2. T9 is still uncommitted.

## 2026-10-31 (16) · O8 and O9 closed; one file for new tasks
- Done: 14 `Recognised in Malaysia?` cells gained the MQA register reading through `apply_backfill.py --overwrite` (dry run first, backup in `.tmp/o8/backup/`; compared to the backup, 15 cells changed, the 14 plus Carnegie Mellon's Warnings). Demo sentence and Decide headline reworded in `data.template.js`; PDF card says "Estimated living". Sample and demo rebuilt. `additionals.md` is now the one task file: "Questions for Evan" added, `discussions.md` closed as history, R41's tally and R11 updated, review marked history, two finished root plans moved to `archives/`.
- Decisions (and why): see `decisions/log.md`.
- Problems / lessons: `data.js` is generated, so R31's note pointed at the wrong file. Warnings is a computed column that `apply_backfill.py` refuses; Carnegie Mellon's sentence was old typed text, not from a tool, so it was removed by an exact one-cell replace. `Course` can't be changed by backfill because it makes the row's key. `Deadline passed` is stamped at sync only, so it can go stale between syncs. Northeastern's page names no essay, so that cell stays as it was.
- Next step: commit, then the pilot plan.

## 2026-10-31 (17) · Intake forms plan: finish check, E2 done, old sheet backup is the wrong tab
- Done: checked the plan against the files: T1-T7 hold (100 tests pass, `--check` clean, workflows current). Evan sent the form links (E2) and deleted the spare sheet. `data/form/intake_answers.csv` deleted at Evan's request: 0 rows, and `fetch_form_answers.py` remakes it. Plan, `status.md`, Now box and Notion updated.
- Decisions (and why): the plan stays in `plans/` until the old sheet is settled, because it holds those steps. Evan will do the first-STPM check himself when one applies, so it needs no backlog entry.
- Problems / lessons: the backup is tab `Form Responses 2`: 9 rows, all with a blank `Ingested at`. `01_intake.md` puts the stamps and 10 rows on `Form Responses 1`, which isn't in `data/form/`. The old sheet no longer shows in Drive search, so it's probably in the bin. 8 of the 9 match a finished folder by email; the 14 Oct row has blank consent and no folder. Compared by hashed email, so no answers were read.
- Next step: Evan restores the old sheet, downloads `Form Responses 1` and settles the 14 Oct row, then archive the plan and update `01_intake.md` and `CLAUDE.md`.

## 2026-10-31 (17) · Old task files deleted; additionals moved to plans/
- Done: on Evan's word, deleted `plans/discussions.md`, the product review, `plans/fact_audit_plan.md`, `prototype/BUILD_PLAN.md`, the two archived plans and the 9 finished `plans/carry-overs/` notes. Moved `business/additionals.md` to `plans/additionals.md` and pointed every live file, skill, agent and memory at it. The numbers behind O5, O6, O7 and O13 went into "Questions for Evan" first.
- Decisions (and why): see `decisions/log.md`. `plans/list_pdf_plan.md` stays because its Decisions still rule the product and tool notes cite it; `plans/intake_forms_plan.md` stays because it is running; `build-log.md` and `decisions/log.md` keep their old paths because they are history.
- Problems / lessons: the commit stayed one piece because T9, O8 and the move share files. Another session was working here throughout, so edits were exact replacements and these entries were appended last.
- Next step: Evan runs the R31 and R49 prompts; the pilot plan stays first.

## 2026-10-31 (18) · Intake forms plan finished and archived
- Done: Evan's form tidy-ups read back and `--check` is clean (100 tests pass); `forms/*.json` saved. Moved the plan to `archives/intake_forms_plan.md`. `CLAUDE.md`, `README.md`, `01_intake.md`, `status.md`, the Now box and Notion now say the old sheet is gone.
- Decisions (and why): see `decisions/log.md`. Old paths in `tools/`, `tests/` and the logs stay because they are history; `archives/README.md` says where the plan went.
- Problems / lessons: Evan typed the grades example into the question title, not the description. `--check` still matches it, so it stays. "No preference" is on the list form's Location only; the scripts handle both.
- Next step: Evan gets the old students who are needed to refill the form, then the pilot plan.

## 2026-10-31 (19) · R49: the list PDF adds "Deadline passed" itself
- Done: `build_html()` in `tools/build_list_pdf.py` now re-checks `Key deadline` on a copy of each row (`with_deadline_warning`), so the summary "!", the key and the card all follow. 9 new tests in `tests/test_list_checks.py`; 109 tests pass. Sample built without `--draft` into `.tmp/r49_sample_list.pdf`: Cambridge shows it once, and the sample CSV is byte-for-byte unchanged.
- Decisions (and why): it calls `feasibility_flags()` rather than `_parse_iso_date` directly, so the date logic and the wording both stay in one place and `shortlist_schema.py` is untouched. Today's date is `build_html()`'s existing `prepared_on`, so no new argument or `--today` flag: the date printed on the PDF and the date checked can't differ. The flag goes first, as a sync would put it. `short_deadline()` guards Rolling and Not published cells, because `_parse_iso_date` would otherwise find any date inside them.
- Problems / lessons: **`plans/additionals.md` not edited (rule 5):** another session was open on it. Owed there: delete the R49 entry, take R49 out of step 12's row (R47, R48 and its file list stay, because R48 still needs `tools/build_list_pdf.py`), move "next number" to R51, and add R50: "#### R50. A deadline cell that opens with an early round reads as passed while the regular round is open. **Added 2026-10-31** (R49's note). **Tool gap, urgent before 10 Nov only if a paid list has one.** A student sees it. **What is true:** `_parse_iso_date` reads a cell's first date, so `2026-11-01 (EA); 2027-01-05 (RD)` is flagged once 1 Nov goes by, by `sync_shortlist.py` and now by every PDF build. Up to 8 rows across 5 old lists start that way; the sample doesn't (it leads with the regular date). **Suggested fix:** the regular deadline goes first in the cell: a line in the row-filler sheet and `workflows/03b_candidate_schema.md`, and those rows through `apply_backfill.py`. Not 'use the last date': some cells end with a date that isn't a deadline."
- Next step: once no other session is on `plans/additionals.md`, make the edits above. The pilot plan stays first.

## 2026-10-31 (20) · Step 2f: Monash's course title is right, no data changed
- Done: read Monash's course page, the E3001 handbook page and the specialisation's handbook page (RBME-USPEC) in Chrome. The sample's title stays. `master_list.csv`, `research_notes.md`, `score_log.jsonl`, the sample and the demo are untouched, so no backup, re-score or rebuild was needed. `business/sales/sample_pack/README.md` now names the row's link as the open item.
- Decisions (and why): the handbook's E3001 "Award title" list includes "Bachelor of Robotics and Mechatronics Engineering (Honours)". That list also holds Aerospace and Environmental, which the handbook says are "not available in Monash University Malaysia in 2027", so it can't be a Malaysia-only list. RBME-USPEC says the specialisation "is listed in E3001 Bachelor of Engineering (Honours) at Clayton and Malaysia". R31's worry was wrong: both T7's reading and the row are true, one names the course you enrol in, the other the degree you graduate with. No page spells out the award title beside the word Clayton; that link is read from those two lines.
- Problems / lessons: **`plans/additionals.md` not edited (rule 5):** three other sessions were open (all idle). Owed there, on top of entry 19's list: delete the R31 entry, the step 2f row and "R31 (step 2f) and" in the 2b-2d row, move "next number" to R52, add a step 2g row for R51, and add R51: "#### R51. The Monash row in the sample links to the general engineering page. **Added 2026-10-31** (step 2f). **Stale data the public sees, small** (the booth opens 10 Nov). **What is true:** `Course URL` is `https://www.monash.edu/engineering`; the course page is `https://www.monash.edu/study/courses/find-a-course/engineering-e3001`. That page is headed Bachelor of Engineering, so a reader needs `Course at a glance` to see it is the same degree. **Suggested fix:** change the cell through `apply_backfill.py` (not part of the row's key, so no re-score) in the source list, then rebuild the sample and the demo." R51 wasn't fixed here because Evan's step 2 said to change nothing when the title is right.
- Next step: once no other session is on `plans/additionals.md`, make entry 19's and this entry's edits, then do R51. The pilot plan stays first.

## 2026-10-31 (21) · Task list tidied, old notes cleared, prompts for three sessions
- Done: on Evan's word, deleted R26, R31 and R49 from `plans/additionals.md` and made entries 19's and 20's owed edits (R50, R51, steps 2g and 2h, next number R52). Moved step 9 up, took out the old freeze wording, marked R34's decision as made, added O14 (overnight runner). Deleted five notes, all read first: `fx_correction_plan.md`, `fx_prose_2026-10-13.md`, `report_merge_plan.md` (finished work), `overnight_automation.md` (never built, kept as O14), `google_form_notes.md` (the live form has all 38 titles and newer wording on 5 descriptions). Kept `r16_scope.md` (R16 needs it) and `token_cost_report.md` (O5 and three workflows write to it). Every live mention repointed; 109 tests pass.
- Decisions (and why): step 9 goes before 10 Nov because two report buyers have paid. `forms/intake.json` replaces `google_form_notes.md` as the source of truth, because the note had already drifted; the option format rule moved to `workflows/01_intake.md`. `token_cost_report.md` left the screenshot list in the social agent because it names a student.
- Problems / lessons: Notion's Status is a select, so a `status_is` filter returns nothing without an error. The booth task in Notion still says "one page of the spreadsheet" and to circle the Reach/Match/Safety label; both are out of date since the PDF. Left for Evan, it's his task.
- Next step: Evan decides the booth's four open items and the pilot plan; Step 9, R42 and R37 run in their own sessions.

## 2026-10-31 (22) · Pilot plan set; public samples flagged
- Done: Evan set the pilot: 12 and 13 Nov in the school compound, 10 sign-ups, Linktree with the survey, samples and prices, a RM10 deposit QR inside both forms, delivery in 7 days. Updated `business/launchx/status.md`, `mentor.md`, the Now box, `workflows/01_intake.md`, `decisions/log.md`, memory, the two Notion booth tasks and the Now page. Added R52 and step 2i.
- Decisions (and why): see `decisions/log.md`. A sign-up counts as form filled and deposit paid, because a form alone proves nothing. Booth talks are written down, with audio only on a yes.
- Problems / lessons: `sample_list.pdf` is clean, but the report and guide samples still carry AI notes and coaching (R52), so only the list goes public first. Another session was mid-way through step 9, so its edits to `tools/`, `tests/` and `workflows/04_university_report.md` were left out of this commit.
- Next step: Evan builds the Linktree and adds the QR to both forms, then says "recheck". Step 9, then R52.

## 2026-10-31 (23) · R33 committed: no Finalist on unverified facts
- Done: `/commit` saved the step 9 session's leftover R33 work as `bb562cb` (`tools/flip_finalists.py`, `tools/check_master_list.py`, `tests/test_list_checks.py`, `workflows/04_university_report.md`). `tests.test_list_checks` passes, 37 tests; the other test files weren't run. Now box and Notion updated.
- Decisions (and why): the public Australian PDF in `data/resources/` stays out of git (658 KB, no tool needs it). Default: add that folder to `.gitignore` later and keep the PDF on the laptop.
- Problems / lessons: this session didn't write the R33 code. The commit-drafter read the diff, and entry 22 only came to light after the commit, so if the step 9 session is still working, it should check `bb562cb` before redoing anything. **`plans/additionals.md` not edited (rule 5):** two other sessions were open (both idle). Owed there: delete the R33 entry, take R33 and `tools/flip_finalists.py` out of step 9's row (R34 stays), move "next number" to R54, and add R53: "#### R53. Two Finalist rows on one old list aren't stamped Official page. **Added 2026-10-31** (R33's commit). **Stale data, urgent only if that list goes out again.** **What is true:** the commit-drafter counted 2 such rows on 1 of 27 lists; the list and the rows' values weren't read. `check_master_list.py` fails only the value `Not verified`, so the list fails only if the rows read that. **Suggested fix:** verify them on the official pages, then correct them through `apply_backfill.py`."
- Next step: once no other session is on `plans/additionals.md`, make the edits above. Then R34, the rest of step 9.

## 2026-11-02 · Task list checked against today's files; past clients parked
- Done: tested the entries in `plans/additionals.md` against the code and the 27 lists (read-only). Evan parked all past-client work; recorded in the "Closed" section there, `decisions/log.md` and memory.
- Decisions (and why): see `decisions/log.md`.
- Problems / lessons: found but not yet edited in `plans/additionals.md`: R33 is done (entry 23's owed edits still stand), R46 and O12 can close, R36, R50, R42 and R35 need rewriting, R30's dated and money lines print in paid PDFs so should move before 10 Nov. No student folder has a `list.pdf` or tick weights yet, so the first paid list is the first real run.
- Next step: step 9 (R34), because two report buyers have paid.

## 2026-11-02 · One client's NUS and China facts re-checked (/catchup)
- Done: re-read the NUS, Tsinghua, ZJU and BIT reports against live official pages. NUS holds. China dates and scholarship routes are stale or wrong. Fixed that student's `status.md`, wrote the detail to their `research_notes.md`, added R53.
- Decisions (and why): changed no CSV, report or calendar, because Evan asked for a check and two answers are still owed by Tsinghua and the embassy.
- Problems / lessons: NUS pages come back empty through WebFetch but read fine through `firecrawl_search.py --scrape-top`. PDFs that WebFetch can't read open with the Read tool or pypdf. An embassy result for another country looks like Malaysia's in search (mv = Maldives).
- Next step: decide the Tsinghua round this week (Round 1 closes 20 Nov), then R53.

## 2026-11-02 · Chinese-taught routes researched, deadlines put in Notion
- Done: read Tsinghua's and ZJU's rules for Chinese-taught engineering. Added 19 dated tasks and research notes to the student's own Singapore and China projects in Notion, at their request.
- Decisions (and why): NUS tasks sit under the existing NUS task, matching that project. Estimated dates say so in the task title. Reports and CSV still unchanged; R53 now also covers the wrong "closed to internationals" line.
- Problems / lessons: nothing official states textbook language at ZJU, and no first-hand Malaysian account turned up, so the emails carry that question.
- Next step: send the Tsinghua email, then decide track and round by 13 Nov.
