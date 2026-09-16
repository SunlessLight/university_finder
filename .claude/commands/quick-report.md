---
description: Facts-only university report, no intake/longlist needed (dispatches report-writer)
argument-hint: <university>[: course][; university2[: course2]; ...] [--mode university]
---

Run `workflows/quick_university_report.md`. This is for when I already know which university
(and usually course) I want and just want the facts — **no student slug, no
`data/students/` folder, no intake, no longlist.** Don't ask for a student slug; there isn't
one for this command.

Parse `$ARGUMENTS`: one or more `University` or `University: Course` entries separated by `;`
(same syntax `/report` uses for named finalists), plus an optional trailing `--mode university`
that applies to every entry in this call (US whole-institution report instead of the
course-mode default).

If nothing follows `/quick-report`, ask me which university (and course, unless `--mode
university`) before dispatching anything — don't guess.

For each entry, **dispatch the `report-writer` subagent** (`.claude/agents/report-writer.md`),
all in parallel when there's more than one. Tell each dispatch explicitly that this is a
**quick/standalone dispatch** (no student slug) plus the university (+ course) and the mode —
the agent's own "Quick mode" section has the rest of the brief; don't re-paste it here.

When every dispatch is back, report each report's path (`data/quick_reports/<slug>.md`) and
any `"Not found — <why>"` gaps it left. There is no CSV to fold anything into and no gate to
run in this session — `check_report.py --quick` already ran inside each dispatch.

If I ask for a PDF and the agent didn't already produce one, run
`python tools/report_to_pdf.py --file data/quick_reports/<slug>.md`.

This is a launcher, not a planning exercise. Do not enter plan mode (CLAUDE.md).
