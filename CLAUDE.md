# University & Course Finder

## What this is

Takes a **Malaysian student** from "who am I / what do I want" to "here is exactly how I apply to
these universities": intake (Google Form) → longlist (officially sourced) → university reports →
decide, plus per-region application prep. Runs on Evan's laptop; students receive the files.

Built on **WAT** (Workflows, Agents, Tools): `workflows/` are plain-language how-tos, you make the
decisions, `tools/` (Python scripts) do the repeatable work. Why: at 90% accuracy per step, five
chained guesses drop to 59%; scripts don't drift.

## Human docs

- `README.md`: setup, and how to run every stage by hand.
- `business/README.md`: index of the business side (product review, stage explainers, LaunchX).

When you change how a stage runs, check whether these need updating too.

## Commands

```
python tools/progress_dashboard.py                    # which stage every student is at
python tools/shortlist_schema.py --contract           # the CSV/fragment contract (never read the source for it)
python tools/check_master_list.py --student <slug>    # gate before a list goes to a student
python tools/fetch_form_questions.py --check          # live form questions -> forms/*.json, checked vs ingest
python tools/check_grades.py --student <slug>         # tidied grades vs the programme's scale
python -m unittest tests.test_intake_forms tests.test_report_order tests.test_check_grades tests.test_list_checks tests.test_calendar_dates   # the automatic tests
```

Each `/command` (`/intake`, `/longlist`, `/report`, `/decide`, `/apply-prep`, `/quick-report`,
`/catchup`, `/notion`, `/social`, `/mentor`) is a thin launcher onto its workflow; the workflow
file stays the source of truth.

## How it fits together

| Part | Where | What it does |
|---|---|---|
| How-tos | `workflows/` (start at `00_overview.md`; there is no `02`) | One file per stage: objective, tools in order, edge cases |
| Scripts | `tools/` | Fetch/ingest the form, sync the master list, build reports, run the checks |
| Helpers | `.claude/agents/row-filler.md`, `report-writer.md` (Opus) | Volume only: one per university (Stage 3), one per finalist (Stage 4) |
| Student files | `data/students/<slug>/` (gitignored) | profile, preferences, `weights.json`, `master_list.csv`, `research_notes.md`, `status.md` |
| Form exports | `data/form/` (gitignored) | Google Form responses CSV |
| Business | `business/` | LaunchX pitch (`launchx/`), sales, backlog `additionals.md` |
| Scratch | `.tmp/` | Throwaway fragments and JSON inputs |

## Guardrails

Running the pipeline:
- Don't enter plan mode for a routine run, because the workflow file is the plan. Plan mode is for changing the system (schema, new tool, workflow rewrite).
- Stop and talk to Evan at: **Stage 1 finalize** (settle `_needs_review` before Stage 3 scores anything) · **Stage 4** (Evan picks finalists: render `compare_universities.py` and wait) · **anything destructive** (`--force` on a student folder, demoting/rejecting a row he hasn't agreed to drop), because `data/students/` has no git undo.
- Don't send a list to a student until `check_master_list.py` is clean, or call a social draft ready until `check_social_post.py` is clean.
- Don't hand-build what a tool owns (a shortlist, `master_list.csv` + `research_notes.md` via `apply_backfill.py`). Check `tools/` before writing a new script.
- Don't build stage-owning helpers, because Stages 1, 5 and 8 are conversations with Evan. Helper write fences: `00_overview.md` → "Subagents".
- When something breaks: fix the tool, retest, write the lesson into the workflow.

Facts and scoring:
- Desirability ≠ admissibility: the 0–100 score excludes entry fit, which lives in `Admission likelihood` (Reach/Match/Safety) + `Warnings`. An unreachable uni must not rank high.
- Don't put weights in `tools/shortlist_schema.py`, because it's shared and concurrent sessions overwrite each other. Weights are per student (`weights.json`, `scoring-weights` skill).
- Hard facts (fees, requirements, deadlines) come from the official uni / UCAS / Common App page. Stage 3 verifies and stamps `Info source = Official page`; no Finalist on unverified facts. Aggregators are for discovery only.
- Cost is total in MYR (approximate), not annual tuition, so a 3-year UK and a 4-year US degree compare.
- Shortlists are a balanced Reach/Match/Safety spread, not top-N by score.
- Recognition back home (MQA + professional body) gates regulated professions.
- `List status` (Longlist → Shortlist → Finalist/Rejected) changes only by a deliberate edit to the CSV, never as a sync side-effect.
- Free search first; `firecrawl_search.py` (credits already paid for) the moment free search errors or comes back without the fact. No need to ask. Full rule: `00_overview.md` guardrail 6.

Privacy and wording:
- Never commit or share `data/students/`, `data/form/`, `data/feedback/` (personal data under PDPA: grades, finances, nationality) or `notes/` (names real students). `.env` holds secrets only.
- Workflow files and tool docstrings are written for agents, so they stay terse and technical. Repo names (`entry_margin`, `row-filler`) get a plain gloss when they reach Evan.

## Things that break silently

- If a form question's wording changes, its `QUESTION_MAP` substring in `ingest_form_csv.py` stops matching. Looks like: one field null for **every** respondent. Fix the map, not the profiles. Catch it before anyone answers: `fetch_form_questions.py --check` after every form edit.
- If a question is replaced on a form, the sheet keeps the old column beside the new one, so one field has two columns. `merge_duplicate_columns()` handles that in `ingest_form_csv.py`; without it a new student reads as "no consent" and is skipped. Looks like: every new respondent skipped.
- If `FORM_ID_LIST_INTAKE` holds a spreadsheet's ID instead of the form's, every form tool stops with `Invalid ID`. It wants the code from the form's edit address. The Apps Script lives in the old sheet "List Intake (Responses)", which also holds the pre-30 Oct answers, so that file must never be deleted.
- If a report JSON's course isn't exactly the CSV `Course` string, `build_report.py` course mode still renders but never flips the row to Finalist. Looks like: report exists, row still Shortlist.

## Generated files: never edit by hand

- Student reports, application guides and `calendar.md`: made by `build_report.py`, `build_application_prep.py` and `build_calendar.py` from JSON inputs. Edit the JSON and rebuild.

## Status

- Current status: the **Now** box at the top of `STATUS.md`. Start a session with `/catchup` (or `/catchup <slug>` for one student).
- Ideas and open questions under discussion with Evan: `plans/discussions.md` (one running file, dated sections). Add to it whenever a session raises an idea or question that isn't settled.
- At the end of a session that changed files or decided something, add an entry to `plans/build-log.md` (done / decisions / problems / next step) and update the Now box.
- Then mirror it to Notion, without asking, so Evan can follow on his phone: rewrite the "Shortlisted — Now" page (`40525bdf03ad8167895cf78073e5a1ac`, under 🗓️ Everything) from the Now box, and bring the Tasks database in line with the open items in `business/launchx/status.md` (new item → new task, ticked → Done, new date → Due). Files are the source; Notion is the copy. Only touch tasks that match an item in the files (the rest are Evan's own) and only `Project Area = University Research Agent` (a new task gets its Area from its `Project`). End the reply with "Notion updated" or why not. Addresses: `workflows/notion_sync.md`.

## Decision log

Log meaningful decisions (direction changes, trade-offs, things worth remembering) in `decisions/log.md`. Append-only: never edit or delete past entries. Format: `[YYYY-MM-DD] DECISION: … | REASONING: … | CONTEXT: …`.

## Where the detail lives

- Google Sheets: the Google Drive connector (`search_files`, then `read_file_content`) is for a quick look only. It returns a *sample* of rows (5 of ~15 on a test sheet) and cuts long cells, and it can't see Google Forms at all. Full answers: `fetch_form_answers.py` (all four forms, feedback included), `fetch_form_responses.py` (intake, the pending batch for Stage 1). Forms' questions: `forms/*.json`.
- `workflows/00_overview.md`: read first for any pipeline run (stages, tool reference, subagent fences, guardrails in full).
- `business/additionals.md`: known problems not yet fixed. Start at its "Start here" index; leftovers a task won't fix go there.
- `business/launchx/mentor.md` + `status.md`: the business mentor brief and LaunchX state (`/mentor`).
- `token_cost_report.md` and the dated notes at the top of each `tools/*.py`: the why behind past changes.
- `archives/`: old copies replaced on 2026-10-21. History only, not instructions.
