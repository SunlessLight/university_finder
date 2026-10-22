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

[2026-10-21] DECISION: R10: keep the source student's predicted grades in the sample pack (list column + one quote in the MIT report). | REASONING: they serve as an example of the 'do your grades clear the bar' check; with a stand-in name and no school, nothing ties them to a real person. | CONTEXT: rejected option: a redaction pair in build_sample_pack.py + rebuild. Real name confirmed absent from the pack and prototype.

[2026-10-21] DECISION: Pre-sell before fixing: ask the 24 survey leads for a yes/no on RM50 first, then fix only what paying customers would see. | REASONING: a payment or deposit is the only evidence that settles 'why not ChatGPT'; it also sizes pilot capacity and picks which bugs matter. | CONTEXT: iLabs check-in feedback; rejected order: fix bugs and update the product first, then test. Business model (families vs renting the workflow) left open until either side pays.
