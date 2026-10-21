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
