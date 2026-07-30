---
description: Stage 3 — discover and fill a longlist for one student, one country
argument-hint: <student-slug> [country]
---

Run `workflows/03_discover_longlist.md` for student `$1`, country `$2`.

If `$2` is empty, pick the country per that workflow's "Pick the next country" step: the next
entry in `preferences.target_countries` with **no rows yet in `master_list.csv`**. The CSV is the
oracle, not `status.md` — if they disagree, trust the CSV. Every target country already having rows
means Stage 3 is done; say so instead of inventing another pass.

**One country per pass.** That's a hard gate (`--country` on both tools), and it's what keeps this
session's context small enough to fill 35 columns a row.

Read `data/students/$1/status.md` first and cross-check it against `profile.json`,
`preferences.json` and `master_list.csv` (files win over the note). Confirm `weights.json` exists —
`sync_shortlist.py` hard-errors without it; derive it via the `scoring-weights` skill if missing.

Keep to the workflow's own division of labour: roster sweep and the country constants stay in
**this** session, then dispatch **one `row-filler` subagent per university, in parallel**, then
merge → sync → check. Clear `.tmp/$1/candidates/` before the pass — `merge_candidates.py` reads
every `*.json` in there and a stale fragment merges just as happily as a fresh one.

`python tools/check_master_list.py --student $1` must come back clean before this list goes
anywhere (CLAUDE.md).

Rewrite `status.md` at the end, naming the specific next country.

This workflow IS the plan. Do not enter plan mode (CLAUDE.md).
