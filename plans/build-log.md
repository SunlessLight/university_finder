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
