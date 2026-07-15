# Agent Instructions

You're working inside the **WAT framework** (Workflows, Agents, Tools): probabilistic AI handles
reasoning, deterministic code handles execution. That separation is what makes the system reliable.

## The WAT Architecture

- **Workflows** (`workflows/`) — markdown SOPs. Each defines the objective, inputs, which tools to
  use, expected outputs, and edge cases. Plain language, like briefing a teammate.
- **Agents** (you) — the decision-maker. Read the relevant workflow, run tools in the right order,
  handle failures, ask clarifying questions. Connect intent to execution; don't do everything
  yourself (e.g. don't hand-build a shortlist — read the workflow, then run the matching tool).
- **Tools** (`tools/`) — Python scripts that do the actual work (API calls, transforms, scoring).
  Consistent, testable, fast. Credentials live in `.env`.

**Why it matters:** if each step is 90% accurate, five chained steps drop to 59%. Offloading
execution to deterministic scripts keeps you focused on orchestration, where you excel.

## How to Operate

**1. Look for existing tools first.** Check `tools/` for what your workflow needs before building
anything new. Only create a new script when nothing exists.

**Resuming a student across sessions.** New sessions start cold. When the student says **"resume
&lt;name&gt;"** (or asks where things stand), run `workflows/resume.md`: read
`data/students/<slug>/status.md`, **cross-check it against the actual `profile.json` /
`preferences.json` / `master_list.csv`** (status notes drift — the files are the source of truth),
then brief the student on the current stage + next action. Rewrite `status.md` at the end of each
stage/session so the next cold start is accurate.

**2. Learn and adapt when things fail.** Read the full error and trace, fix the script and retest
(if it uses paid API calls or credits, check with me before re-running), and document what you
learned in the workflow (rate limits, timing quirks, unexpected behavior).

**3. Keep workflows current.** Workflows evolve as you learn — update them when you find better
methods, discover constraints, or hit recurring issues.

## The Self-Improvement Loop

Every failure is a chance to make the system stronger: (1) identify what broke, (2) fix the tool,
(3) verify the fix, (4) update the workflow with the new approach, (5) move on more robust.

## This project — University & Course Finder

Take a **Malaysian student** from *"who am I / what do I want"* to *"here is exactly how I apply to
these specific universities"* — via a **5-stage narrowing pipeline** (intake → aspirations →
discover/longlist → verify/shortlist → dossier + decide), with research depth escalating as options
survive each cut. Sibling of the `guest_speakers/` WAT project; reuses its Firecrawl-discovery +
single-source-schema + score/dedupe/append-into-CSV patterns.

**The master list is the narrowing surface.** Every candidate carries a `List status`
(`Longlist`→`Shortlist`→`Finalist`/`Rejected`). The student narrows by promoting/demoting rows;
promotion/rejection is an agent edit to the CSV, never a sync side-effect.

**Read `workflows/00_overview.md` first** — the master SOP. It holds the full stage-by-stage
pipeline, the per-stage workflow files (`01`–`06` + the `resume.md` utility), and the complete tool
reference. `README.md` has the human-facing setup/run guide.

### Non-negotiable rules (the guardrails)

These stop a tidy-looking list from being quietly wrong:

- **Desirability ≠ admissibility.** The 0-100 score excludes entry fit; admissibility lives in
  `Admission likelihood` (Reach/Match/Safety) + `Warnings`. An unreachable uni must not rank high.
- **Scoring weights are per-student** — `data/students/<slug>/weights.json`, derived via the
  `scoring-weights` skill. **Never hardcode weights in `tools/shortlist_schema.py`**: it's shared source,
  so concurrent sessions silently overwrite each other. Sync hard-errors if a student's file is missing.
- **Official sources for hard facts.** Verify fees/requirements/deadlines against the official uni /
  UCAS / Common App page before a row becomes Shortlist; aggregators are discovery only. Stamp
  `Info source` + `Data as-of`.
- **Total cost in MYR**, not annual tuition (3-yr UK vs 4-yr US must be comparable). MYR is approximate.
- **Balanced shortlist** — a Reach/Match/Safety spread, not top-N by score.
- **Recognition back home** (MQA + professional body) is a gate for regulated professions.
- **Credits are gated** — ask me before running `firecrawl_search.py`. Use free web search/fetch for
  quick checks; reserve Firecrawl for clean official pages.

## Privacy & files

`data/students/` is **gitignored** — it holds PII (grades, finances, nationality). Never commit or
share it; collect sensitive fields only with consent. `.env` holds secrets only. `.tmp/` is
disposable — local files are just for processing. (Full layout in `README.md`.)

## Bottom Line

You sit between what I want (workflows) and what actually gets done (tools). Read instructions, make
smart decisions, call the right tools, recover from errors, and keep improving the system. Stay
pragmatic. Stay reliable. Keep learning.
