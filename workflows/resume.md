# Workflow: Resume — bring a new session up to speed (↔ status.md)

## Objective

Kill the cold-start problem. Every new session, Claude has amnesia: the student has to re-state
who they are and beg you to re-read the data bank. This workflow lets the student say **"resume
&lt;name&gt;"** and get, in one step, an accurate *"here's where we are / here's the next action"*
brief — reconstructed from the student's own files, **cross-checked so stale notes don't mislead
you**. Output/state lives in `data/students/<slug>/status.md`.

This is a **utility** workflow, not a pipeline stage. It wraps around Stages 1-6; it doesn't
replace them.

## When to run

The student says **"resume &lt;name&gt;"**, "where were we", "pick up &lt;name&gt;", or similar.
It's **manual** — you are not expected to auto-run it every session, but if a returning student
starts talking about ongoing work, offer it.

## How to start

1. **Resolve the student → slug.** Match the name to a folder under `data/students/`. If the name
   is ambiguous or missing, list the folders (`data/students/*/`) and ask which student.
2. **Read `status.md` first.** `data/students/<slug>/status.md` is the fast handoff note — read it
   before anything else. It tells you the claimed stage, last actions, and next step.
3. **Cross-check status.md against the real files — do not trust it blindly.** Status notes drift;
   the JSON/CSV are the source of truth. Open `profile.json`, `preferences.json`, and
   `master_list.csv` and reconcile:
   - Does `preferences.target_countries` match the **destinations actually present** in
     `master_list.csv`? (A country in scope with zero rows = discovery gap. Rows for a country not
     in scope = stale scope.)
   - Do the **`List status`** counts in the CSV match what `status.md` claims (Longlist / Shortlist /
     Finalist / Rejected)?
   - Do any **`Notes`** cells contradict current scope/decisions (leftover text from an earlier round)?
   - Are hard facts still `Info source = Aggregator` / `Data as-of` old? (⇒ Stage 4 not done.)

   > **Why this step is non-negotiable:** in the session that created this workflow, two separate
   > cold reads of Toru's files were stale — leading to wrong advice ("demote the China rows") and a
   > wrong stage read ("Stage 3 half-finished"). The files had moved on. **Always reconcile the note
   > against the files, and if they conflict, the files win — then fix `status.md`.**
4. **If `status.md` is missing,** reconstruct the state from the files, **create** `status.md` from
   the template below, and tell the student you generated it fresh.
5. **Brief the student.** Give a concise summary: current stage, the single most important next
   action, and any open questions or drift you found. Confirm before doing paid or destructive work.

## Updating status.md (the discipline that keeps it honest)

`status.md` is only useful if it's current. **Rewrite it (overwrite, don't append) at the end of
every stage and every working session.** Capture:
- what changed this session (dated),
- the current stage and the single next action,
- any open questions / drift left to reconcile.

A stale note is worse than none — it lies with confidence. Treat updating it as part of finishing
any piece of work, the same way you'd stamp `Data as-of` on a verified row.

## The status.md template

```markdown
# Session status — <Name> (<slug>)
_Last updated: YYYY-MM-DD by Claude_

## Current stage
Stage <n> — <done | in progress | blocked>. <one line on where exactly>

## Snapshot
- Scope: <countries> · Field: <field> · Intake: <intake> · Budget: <cap or "no limit">
- Grades: <summary + predicted/actual>

## Master list state
- Rows by List status: Longlist <n>, Shortlist <n>, Finalist <n>, Rejected <n>
- Destinations covered vs in-scope: <e.g. all 5 in scope present; nothing verified yet>

## Recent actions
- YYYY-MM-DD — <what we did>

## Next action
<the single most important next step — what a fresh session should do first after briefing>

## Open questions / drift to reconcile
- <e.g. China rows' Notes still say "Rejected: out of scope" — stale, clean up>
```

## Edge cases & rules

- **Files win over the note.** If `status.md` and the JSON/CSV disagree, the files are truth. Fix
  `status.md`, and tell the student what you reconciled.
- **Never fabricate progress.** If you can't tell whether a stage was done, say so and check the
  files — don't assume the note is complete.
- **One snapshot, not a log.** `status.md` is the *current* state; overwrite it. Put dated history
  under "Recent actions" (keep it short — last few sessions), not by stacking whole old snapshots.
- **PDPA.** `status.md` lives in the gitignored `data/students/<slug>/` folder like the other files.
  It may summarise grades/scope — keep it local, never commit or share.
- **Don't burn credits to resume.** Reconstructing state is a **free** operation (reading local
  files). Never call `firecrawl_search.py` just to figure out where you are.

## Done when

You've briefed the student on the true current stage + next action, `status.md` exists and matches
the files (drift reconciled), and you've named any open questions. Then continue with whatever
pipeline stage is next.
