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

**2. Learn and adapt when things fail.** Read the full error and trace, fix the script and retest,
and document what you learned in the workflow (rate limits, timing quirks, unexpected behavior).

**3. Keep workflows current.** Workflows evolve as you learn — update them when you find better
methods, discover constraints, or hit recurring issues.

**4. Running a workflow is not a planning exercise.** The files in `workflows/` **are** the plan —
objective, tools in order, expected output, edge cases. Re-planning them wastes a whole pass. For a
routine pipeline run (intake, longlist, university report, application prep, resume): read the
workflow, then execute. **Don't enter plan mode.** Plan mode is for changing the *system* — a schema
change, a new tool, a workflow rewrite — not for running it.

That is about *planning overhead*, not about judgement. These checkpoints stay, and they are
conversations with me, not permission prompts:
- **Stage 1 finalize** — settle the `_needs_review` items with me before Stage 3 scores anything.
- **Stage 4** — *I* pick the finalists. Render `compare_universities.py` and wait; don't self-select.
- **Anything destructive** — `--force` on an existing student folder, or demoting/rejecting a row I
  haven't agreed to drop. `data/students/` is **gitignored**, so there is no `git checkout` undo.
- **`check_master_list.py` must come back clean** before a list goes to a student.

**Entry points are slash commands.** `/catchup <slug>` · `/intake` · `/longlist <slug> [country]` ·
`/report <slug>` · `/decide <slug>` · `/apply-prep <slug> <region>` (`.claude/commands/`). Each is a thin
launcher onto its workflow file — the workflow stays the source of truth, the command just saves a cold
session from re-deriving which file to read. (`/catchup`, not `/resume` — that name is taken by the
built-in.) `/commit` is the odd one out: it launches repo *maintenance*, not a pipeline stage — it
dispatches `commit-drafter` to read the working tree and draft a commit split into `.tmp/commit_plan.md`.
I approve the split; nothing stages itself.

**5. Subagents fan out over volume; you keep the judgement.** A subagent is a stateless worker: fresh
context every dispatch, nothing from the conversation, no per-agent history and **no way to ask a
question**. So the split is by volume, not by stage — `row-filler` (parallel, one per university) and
`report-writer` (parallel, one per finalist) exist because those are 8-12 and 3-5 near-identical
research units; Stages 1, 5 and 8 stay in the main session because each is one unit wrapped in a
conversation with me. Don't build stage-owning agents: the checkpoints above live inside exactly those
stages, and an agent that hit one would stall or guess. Continuity is **per student** (`status.md`), never
per stage. Parallelism rule and each agent's write fence: `workflows/00_overview.md` → "Subagents".

The same volume test is why `commit-drafter` is allowed to exist outside the pipeline: a full `git diff`
is read-once volume that would otherwise sit in this session's transcript for the rest of its life. It
absorbs the diff and hands back `.tmp/commit_plan.md`. It ends at a *plan* — it never stages, commits or
pushes — so it isn't owning a checkpoint, it's preparing one for me.

**6. Bulk file generation belongs in a fresh session, not the tail of a long one.** Same principle
as the subagent rule above — keep volume out of the judgement session. If a session produces a big
plan (many files to write, a large split/rewrite), write the plan to a file where it was produced,
then open a fresh session to execute the bulk writes from that file. Don't `/compact` to make room
first — compaction re-reads the whole window, pays for a summary, and invalidates the cache; a new
session reading the plan cleanly off disk is cheaper on every axis.

**Within one session, the same rule is: repetitive edits go through a script, not N tool calls.**
Updating many near-identical sections of one file — appending a note to each of 9 `## University X`
blocks in `research_notes.md` — is **one** read-modify-write Python pass, never 9 sequential `Edit`
calls. Each of those needs a large `old_string` purely to disambiguate the match: no new
information, pure overhead, and it sits in the transcript being re-read for every remaining turn.
This has cost real tokens twice (2026-08-01, 2026-08-02) in sessions that had *already* done the
CSV correctly as a single Python pass and then hand-edited the second file anyway. If a tool
already owns the write, use it — `apply_backfill.py` writes both `master_list.csv` and
`research_notes.md` from fragments on disk, so neither file needs an `Edit` at all.

**Point at a file; don't paste the file.** Applies to dispatch prompts (N agents sharing context
read one plan file — `workflows/00_overview.md` → "Dispatch by reference, not by paste"), to tool
contracts (`python tools/shortlist_schema.py --contract`, never "read the source"), and to agent
replies (a path and a flag line, never the research).

## The Self-Improvement Loop

Every failure is a chance to make the system stronger: (1) identify what broke, (2) fix the tool,
(3) verify the fix, (4) update the workflow with the new approach, (5) move on more robust.

## This project — University & Course Finder

Take a **Malaysian student** from *"who am I / what do I want"* to *"here is exactly how I apply to
these specific universities"* — via a **four-stage narrowing pipeline** (intake → discover/longlist →
verify + university report → decide), with research depth escalating as options survive each cut. Sibling of the
`guest_speakers/` WAT project; reuses its Firecrawl-discovery + single-source-schema +
score/dedupe/append-into-CSV patterns.

**Intake is a Google Form, not a conversation.** Every student arrives via
`workflows/01_intake.md` — export the responses CSV to `data/form/`, run `ingest_form_csv.py`, then
finalize each student's `_needs_review` items by hand before Stage 3.

**The master list is the narrowing surface.** Every candidate carries a `List status`
(`Longlist`→`Shortlist`→`Finalist`/`Rejected`). The student narrows by promoting/demoting rows;
promotion/rejection is an agent edit to the CSV, never a sync side-effect.

**Read `workflows/00_overview.md` first** — the master SOP. It holds the full stage-by-stage
pipeline, the per-stage workflow files (`01_intake`, `03`, `04`, `05`, plus the `08_application_prep`
and `resume` utilities — **there is no `02`**; intake and aspirations merged on 2026-07-25), and the
complete tool reference. `README.md` has the human-facing setup/run guide. Stage 4 delegates its
research-and-report step to an Opus-pinned subagent (`.claude/agents/report-writer.md`) — see
`00_overview.md` for the full note; everything else in this project runs on the session's default model.

### Non-negotiable rules (the guardrails)

These stop a tidy-looking list from being quietly wrong:

- **Desirability ≠ admissibility.** The 0-100 score excludes entry fit; admissibility lives in
  `Admission likelihood` (Reach/Match/Safety) + `Warnings`. An unreachable uni must not rank high.
- **Scoring weights are per-student** — `data/students/<slug>/weights.json`, derived via the
  `scoring-weights` skill. **Never hardcode weights in `tools/shortlist_schema.py`**: it's shared source,
  so concurrent sessions silently overwrite each other. Sync hard-errors if a student's file is missing.
- **Official sources for hard facts.** Verify fees/requirements/deadlines against the official uni /
  UCAS / Common App page. **Stage 3 owns verification** — rows are built from official pages and stamped
  `Info source = Official page` there; Stage 4 only spot-checks currency. A row can't become Finalist on
  unverified facts. Aggregators are discovery only.
- **Total cost in MYR**, not annual tuition (3-yr UK vs 4-yr US must be comparable). MYR is approximate.
- **Balanced shortlist** — a Reach/Match/Safety spread, not top-N by score.
- **Recognition back home** (MQA + professional body) is a gate for regulated professions.
- **Free search first, Firecrawl when free is blocked — and never ask permission for either.**
  Claude's `WebSearch`/`WebFetch` is the default for *everything*, official pages included. Escalate
  to `firecrawl_search.py` the moment free search is blocked — meaning an error **or a response that
  doesn't contain the fact you went there for** (a JS-rendered fee table returning empty is the
  common case). Then just run it; the credits are there to be spent. Full rule: guardrail 6 in
  `workflows/00_overview.md`.

## Privacy & files

`data/students/` is **gitignored** — it holds PII (grades, finances, nationality). Never commit or
share it; collect sensitive fields only with consent. `.env` holds secrets only. `.tmp/` is
disposable — local files are just for processing. (Full layout in `README.md`.)

## Bottom Line

You sit between what I want (workflows) and what actually gets done (tools). Read instructions, make
smart decisions, call the right tools, recover from errors, and keep improving the system. Stay
pragmatic. Stay reliable. Keep learning.
