---
description: Stage 5 — recommendation, application strategy, and one deadline calendar
argument-hint: <student-slug>
---

Run `workflows/05_decide_and_apply.md` for student `$1`.

Read `data/students/$1/status.md` first and cross-check it against `master_list.csv` (files win
over the note). This stage needs finalists with built reports under `data/students/$1/reports/` —
if there are none, say so and go back to Stage 4 rather than recommending off unverified rows.

1. Final comparison, walked through with the student across cost, quality, fit, visa, deadlines:
   ```powershell
   python tools/compare_universities.py --student $1 --status Finalist --dimensions all --save
   ```
2. Write `data/students/$1/recommendation.md` — ranked picks each tied back to the student's own
   `priorities`, confirmation the set spans Reach/Match/Safety, the application strategy under the
   real constraints (UCAS 5 choices and no Oxford+Cambridge in one cycle; Common App per-school
   fees budgeted; direct-application portals for Singapore/Malaysia/China), and the open risks.
3. Build the calendar:
   ```powershell
   python tools/build_calendar.py --student $1
   ```
   Review it and flag the earliest actions. Scholarship deadlines sequence *before* deposits.

**The decision is the student's** — present the recommendation and the trade-offs, don't
over-promise. Keep the strategy conditional where grades are still predicted.

Rewrite `status.md` at the end.

This workflow IS the plan. Do not enter plan mode (CLAUDE.md).
