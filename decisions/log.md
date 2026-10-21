# Decision log

Append-only. When a meaningful decision is made (a change of direction, a trade-off, something worth remembering later), add an entry at the bottom. Never edit or delete past entries; if a decision is reversed, add a new entry that says so.

Format: [YYYY-MM-DD] DECISION: ... | REASONING: ... | CONTEXT: ...

- **DECISION:** what was decided, in one sentence.
- **REASONING:** why, including what was traded off.
- **CONTEXT:** what led to it, options rejected, and links to files with the detail.

Earlier decisions stay where they were written (`business/launchx/status.md` → "Decided", the memory notes, commit history). New ones go here.

---

[2026-10-21] DECISION: Adopt Evan's claude-toolkit in this project: global copies replace `/commit`, `commit-drafter`, the "Talking to Evan" and subagent/context sections; templates add `STATUS.md`, `plans/build-log.md`, this log, `/catchup` and `/mentor` skills. | REASONING: one shared copy can't drift between projects, and a shorter CLAUDE.md leaves more room in every session. | CONTEXT: toolkit PLAN.md T14; old files kept in `archives/`.

[2026-10-21] DECISION: The project's single Now box lives in a new root `STATUS.md`, which points to the LaunchX status, the backlog and per-student notes instead of copying them. | REASONING: the LaunchX status covers only the business side, so system work had nowhere to go. | CONTEXT: rejected option: Now box at the top of `business/launchx/status.md`.

[2026-10-21] DECISION: The mentor no longer rewrites `business/launchx/status.md` on its own; it drafts the change as soon as it happens and asks "Update the notes?". | REASONING: Evan's call, so he sees every change to the note. Asking straight away (not at the end) keeps the old protection against sessions closing without warning. | CONTEXT: clash between the old brief and the toolkit's advisor template.
