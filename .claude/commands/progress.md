---
description: Roster-wide progress report — which stage every student is at (wraps tools/progress_dashboard.py)
---

Run `python tools/progress_dashboard.py` and show me its output as-is.

This is a pure report, not a workflow — nothing to plan or decide. Don't enter plan mode, don't
read any student's `status.md` first; the tool derives every student's stage straight from
`profile.json`, `preferences.json`, `master_list.csv` and `reports/`, the same signals
`workflows/resume.md` uses for one student at a time.
