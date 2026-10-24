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

[2026-10-23] DECISION: Pre-sale capped at 15 list spots; replies close 25 Oct, then count leads as paid / yes-not-paid / no / silent. | REASONING: capacity is set by Evan's hands-on hours in exam season (about 1 hour per student), not by Claude usage limits; only payment counts as demand. | CONTEXT: survey grew to 79 responses; 35 left a number but 6 misread the question, leaving 29 real leads, all messaged by 23 Oct.

[2026-10-23] DECISION: Continue-bar is 20 paying customers by 2 Dec. | REASONING: a clear number decides whether to continue, not mood on the day. | CONTEXT: 29 real leads messaged; 20 exceeds the 15-spot pre-sale cap, so capacity must grow. What happens on a miss is still open.

[2026-10-23] DECISION: Paid customers fill the existing Google Form, sent right after payment; not WhatsApp. | REASONING: the form feeds the intake tools automatically; WhatsApp answers would be retyped by hand. | CONTEXT: paid lists due 2 Nov. iLabs' email-over-WhatsApp point left for later.

[2026-10-23] DECISION: Single-university report RM30; the 20-30 university list stays RM50. | REASONING: Evan's call; some leads said too expensive. | CONTEXT: mentor advised counting the 25 Oct replies at the old price first, then announcing RM30 in the nudge.

[2026-10-23] DECISION: If short of 20 paying customers on 2 Dec, pause and decide continue / pivot / stop by 10 Dec. | REASONING: a pause with an end date can't drift for weeks. | CONTEXT: follows the 20-payer continue-bar set the same day.

[2026-10-24] DECISION: Main track becomes a B2B test with the current workflow (small family-paid consultancies); families become a side track (light advertising, referrals). Backend reopens, limited to measured cost cuts and fixes a customer or consultant would see; consultancy messages go first. | REASONING: Evan thinks free ChatGPT is good enough for families and prefers B2B; changing the customer keeps the product and evidence, changing the product throws both away. | CONTEXT: after the 24 Oct panel ("ChatGPT can do the research too"); Evan had considered a full pivot to a "bigger problem".

[2026-10-24] DECISION: 2 Dec continue-bar is now 1 consultancy on a paid pilot and 10 paying families (replaces 20 paying customers). | REASONING: the old bar measured only families, which are now the side track. | CONTEXT: the 10 Dec continue / pivot / stop gate is unchanged.
