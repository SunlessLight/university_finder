# University & Course Finder

A self-contained **WAT** (Workflows, Agents, Tools) project: probabilistic AI handles the reasoning,
deterministic Python handles execution. It takes a **Malaysian student** from *"who am I / what do I want"*
to *"here is exactly how I apply to these specific universities"* — through a four-stage narrowing pipeline
that ends in deep per-university reports, a ranked recommendation, and a deadline calendar. Everything
lives in one local data bank that opens in Excel / Google Sheets / LibreOffice.

Sibling of the `guest_speakers/` project; reuses its proven discovery + scoring patterns.

See [CLAUDE.md](CLAUDE.md) for the agent operating instructions, and
[workflows/00_overview.md](workflows/00_overview.md) for the full pipeline.

## Layout

```
workflows/   Markdown SOPs (00_overview, 01_intake, 03_discover_longlist, 04_university_report,
             05_decide_and_apply, + 08_application_prep, resume)
tools/       Python execution scripts (firecrawl_search, init_student, ingest_form_csv,
             shortlist_schema, sync_shortlist, compare_universities, build_report, build_calendar)
data/students/   One private data bank per student (gitignored — PII)
data/form/       Google Form CSV exports dropped here for batch intake (gitignored — PII)
.tmp/        Disposable intermediates (gitignored)
.env         Secrets only (gitignored)
```

## The pipeline at a glance

| Stage | Output | What you get |
|---|---|---|
| 1 Intake | `profile.json` + `preferences.json` | Grades, budget, English, recognition needs — plus countries, field and priorities. Built from the Google Form CSV |
| 3 Discover | `master_list.csv` (Longlist) | 20-40 candidates, scored |
| 4 Verify + Report | `reports/<uni>.md` | Student picks 3-5 finalists; verify their facts against official sources (Reach/Match/Safety), then a deep 16-section **university report** each |
| 5 Decide | `recommendation.md` + `calendar.md` | Ranked picks, application strategy, deadlines |

There is **no Stage 2** — intake and aspirations merged into Stage 1 on 2026-07-25, when the Google
Form became the only on-ramp. Stages 3-5 kept their numbers rather than renumber the whole repo.

Stage 4's per-finalist research-and-report step also runs on a different model — Claude dispatches it
to a subagent pinned to **Opus** (it's the deepest, highest-stakes writing task in the pipeline), while
everything else, including Stage 4's own pick/verify/cut checkpoint with you, runs on the normal session
model. This happens automatically; there's nothing you need to run or configure.

## Setup (first time)

```powershell
# 1. Create + activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Firecrawl key to .env  (copy .env.example -> .env)
#    FIRECRAWL_API_KEY=fc-...
```

## Run

**Intake is a Google Form.** Students request a search by filling it in; the responses become student
data banks in bulk. Build the form once — the exact questions, sections, and consent gate are in
[workflows/01_intake.md](workflows/01_intake.md) — then export responses as CSV and drop the file in
**`data/form/`** (gitignored — PII).

Easiest: open this folder in VSCode and tell Claude **"ingest the form responses"** — Claude reads the
workflows, finalizes the judgment-heavy fields per student (grades → subjects, recognition targets,
degree level), and drives the remaining stages. Or by hand:

```powershell
python tools/ingest_form_csv.py "data/form/responses.csv" --dry-run   # preview
python tools/ingest_form_csv.py "data/form/responses.csv"             # create folders
#   ...Stage 1: finalize each student's _needs_review items, then delete the key...

#   ...Stage 3: ask Claude to derive data/students/<slug>/weights.json (the 'scoring-weights' skill)
#      — per-student scoring weights; sync refuses to run without them...

python tools/firecrawl_search.py --student aisyah-rahman "BSc Computer Science UK entry requirements" --limit 6 --scrape-top 2
#   ...review .tmp/<slug>/search_results.json, write .tmp/<slug>/uni_candidates.json (schema in workflow 03)...
python tools/sync_shortlist.py --student aisyah-rahman          # add --dry-run to preview

python tools/compare_universities.py --student aisyah-rahman --status Shortlist --dimensions all
#   ...narrow by editing the List status column; promote finalists...

python tools/build_report.py --student aisyah-rahman --input .tmp/aisyah-rahman/report_manchester-cs.json
python tools/build_calendar.py --student aisyah-rahman
```

`tools/init_student.py` still scaffolds a single student folder by hand (and its templates are the
schema source of truth that `ingest_form_csv.py` imports), but the form is the normal way in.

Full instructions — the per-destination query playbook, scoring rubric, the 16-section university-report template,
and the narrowing rules — live in [workflows/](workflows/), starting with
[00_overview.md](workflows/00_overview.md).

### Running a stage with Claude

**Don't use plan mode for a normal run.** The workflow files already *are* the plan, so planning one
re-derives what's on disk and costs a whole extra pass. Say what you want ("build Aisyah's longlist",
"resume ong-kyan") and let Claude read the workflow and execute. Save plan mode for changing the
*system* — a schema change, a new tool, a workflow rewrite.

Run in **`acceptEdits`** mode, not `bypassPermissions`. `.claude/settings.json` allowlists every
`tools/*.py` script and the read-only git commands, so the whole pipeline runs without prompts —
while `--force`, `rm` and `git push` still stop and ask. That last stop matters more here than in a
normal repo: `data/students/` is **gitignored**, so an overwritten `profile.json` or `master_list.csv`
has no git history to restore from.

**Stage 4 quietly switches models for its research-and-report step.** When it reaches the per-finalist
"Tools used" work in `04_university_report.md` (research → assemble JSON → `build_report.py`), Claude
dispatches that one step to a subagent pinned to Opus (`.claude/agents/report-writer.md`) instead of
writing the report itself on whichever model is running your session. It happens automatically, once
per finalist — you don't run or configure anything differently. The pick/verify/cut checkpoint earlier
in Stage 4, where you choose the finalists, still happens in your normal session.

## Notes

- **`Approx total (MYR)`** uses a rough offline FX table in `tools/shortlist_schema.py` — update the rates
  periodically; it's for apples-to-apples comparison, not financial precision.
- **A list with blank cells has a repair path.** `sync_shortlist.py` only ever *adds* universities —
  it skips any already on the list, so it can't fill holes in an existing row. For that, run
  `python tools/check_master_list.py --student <slug> --blanks` to see what's missing, then ask Claude
  to backfill it; `tools/apply_backfill.py` writes the results in. Mostly affects older lists, which
  predate the "every column filled" rule.
- **Privacy:** `data/students/` is gitignored. It holds personal data (grades, finances, nationality) —
  keep it local, don't commit or share it.
