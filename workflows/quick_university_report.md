# Workflow: Quick University Report — facts only, no student needed

## Objective

Produce a full 15-section university report for a student who already knows which university
(and, usually, which course) they want, and just wants the facts — without going through Stage 1
(`01_intake.md`) or Stage 3 (`03_discover_longlist.md`) first.

This is a **utility, not a pipeline stage** — it sits outside the four-stage student pipeline,
alongside `resume.md`, `08_application_prep.md`, and `social_media.md`, and touches **no student
data at all**: no `profile.json`, no `preferences.json`, no `master_list.csv`, no student folder
under `data/students/`. Report `04_university_report.md` for how the *pipeline* version of this
report works — this file only covers what's different when there's no student behind it.

**Offer the full pipeline instead when it's a better fit.** If the student is still comparing
options, wants a scored/balanced shortlist, or wants this university weighed against others,
that's Stage 3→4, not this. This workflow is specifically for "I already know I want X, just
tell me about it" — one university (or a short named list), no comparison, no scoring.

## Why this is cheap to run

`tools/build_report.py` never reads `profile.json`, `preferences.json`, `weights.json`, or
`master_list.csv` — it only needs a valid report JSON. The two-way split between "facts" and
"fit" in a normal report lives in the *instructions* the research agent follows
(`.claude/agents/report-writer.md`), not in the rendering code, so a facts-only report is a
different brief to the same agent, not a different tool. The only two Snapshot fields that don't
apply without a student — `admission_likelihood` and `priorities` — are already optional and
silently skipped by the renderer when absent.

## What's different from the normal Stage 4 report

**Same 13 content sections, same research depth, same sourcing standard, same writing rules**
(second person, tables over prose, blockquote callouts, the acronym auto-glossary). Only:

- **Snapshot** omits `admission_likelihood` and `priorities` — there's no grade margin and no
  student priorities to state.
- **`who_its_for`, `getting_in`, `why_here`** keep their factual half and drop the personalized
  half (fit-check, achievements comparison, priorities-based synthesis). The exact per-section
  rule is written once, in `.claude/agents/report-writer.md`'s "Quick mode" section — read it
  there, don't re-derive it here.
- **No finalist marker, no `corrections`, no CSV flip, ever.** There is no `master_list.csv` row
  to claim or correct.
- **Output lives at `data/quick_reports/<slug>.md`**, not `data/students/<slug>/reports/`.
  Because the report carries no student-specific content, it's naturally reusable — two
  different students asking about the same university produce the same file; a re-run just
  overwrites it, same as any other report.

## Tools used

> **Dispatch to the same `report-writer` subagent used by Stage 4** (`.claude/agents/report-writer.md`,
> pinned to Opus) — one call per university, in parallel if the student names more than one. Tell
> it explicitly in the invocation prompt that this is a **quick/standalone dispatch**: no student
> slug, which university (+ course, or university alone for `--mode university`), and the mode.
> The agent's own file has a "Quick mode" section covering exactly what to research, what to
> render, and how — don't re-paste that brief here.

1. *(agent research)* gather the facts for the 13 content sections, same standard as Stage 4:
   official sources for hard facts, free search first and Firecrawl when free is blocked
   (guardrail 6 in `00_overview.md`), decision-texture sections stay free-search-only.
2. *(agent step)* assemble `.tmp/quick/report_<slug>.json` (or `uni_<slug>.json` for
   `--mode university`) — same shape as a normal report JSON, minus `admission_likelihood`/
   `priorities`, and with no `corrections`.
3. *(agent step)* render and check, then export:
   ```powershell
   python tools/build_report.py --quick --input .tmp/quick/report_<slug>.json [--mode university]
   python tools/check_report.py --file data/quick_reports/<slug>.md --quick
   python tools/report_to_pdf.py --file data/quick_reports/<slug>.md   # optional, on request
   ```
   `build_report.py --quick` writes only the `.md` — no finalist marker, nothing for a later
   main-session step to fold in. There is no equivalent of `flip_finalists.py`/
   `check_master_list.py` to run afterward; the report is the whole deliverable.

## Edge cases & rules

- **Official sources for hard facts** — identical rule to Stage 4: fees, requirements, visa rules,
  and recognition come from official sites, not aggregators, each source stamped with its cycle
  year.
- **Capture social/forum/video links, don't scrape them** — identical rule to Stage 4, for the
  same sections (`getting_in`, `culture_vibe`, `student_life`, `city_and_belonging`).
- **A student who later does full intake gets a fresh report, not a promoted one.** A quick
  report is never "upgraded" into a Stage 4 finalist report or linked to a student folder — if
  the student goes through intake and this university survives to Shortlist/Finalist, Stage 4
  runs its normal dispatch and writes a normal, personalized report. The quick report was a
  standalone answer to a standalone question; it doesn't carry state forward.
- **Multiple universities in one ask** — dispatch one `report-writer` call per university, in
  parallel, same concurrency reasoning as Stage 4 (each dispatch writes only its own report and
  marker-equivalent-of-nothing, so there's nothing to race).

## Done when

Every named university has a report at `data/quick_reports/<slug>.md`, `check_report.py --quick`
came back clean on each (or every finding was reviewed and judged a false positive), and — if
requested — a `.pdf` sits alongside each `.md`.
