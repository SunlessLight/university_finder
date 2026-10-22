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
