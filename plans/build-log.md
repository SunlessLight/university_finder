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
