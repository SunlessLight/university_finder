---
description: Resume a student — brief where we are and what's next (wraps workflows/resume.md)
argument-hint: <student-slug>
---

Resume student `$1` by running `workflows/resume.md`.

If `$1` is empty or doesn't match a folder under `data/students/`, list the folders and ask which
student — don't guess.

The non-negotiable part of that workflow is step 3: **read `data/students/$1/status.md`, then
cross-check it against `profile.json`, `preferences.json` and `master_list.csv`.** Status notes
drift; **the files win over the note.** Specifically reconcile: `target_countries` vs the
destinations actually in the CSV, the `List status` counts, stale `Notes` cells, any row still
reading `Info source = Not verified`, and whether `profile.json` still carries `_needs_review` or
`_intake_raw` (⇒ Stage 1 never finished — go finish it before any discovery).

Finish by briefing me on the true current stage, the single next action, and any drift you
reconciled. Then rewrite `status.md` if it was wrong.

**Never search to resume** — state lives in local files; this is a read, not research.

This workflow IS the plan. Do not enter plan mode (CLAUDE.md).
