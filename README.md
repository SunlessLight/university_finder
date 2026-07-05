# University & Course Finder

A self-contained **WAT** (Workflows, Agents, Tools) project: probabilistic AI handles the reasoning,
deterministic Python handles execution. It takes a **Malaysian student** from *"who am I / what do I want"*
to *"here is exactly how I apply to these specific universities"* — through a 5-stage narrowing pipeline
that ends in deep per-university dossiers, a ranked recommendation, and a deadline calendar. Everything
lives in one local data bank that opens in Excel / Google Sheets / LibreOffice.

Sibling of the `guest_speakers/` project; reuses its proven discovery + scoring patterns.

See [CLAUDE.md](CLAUDE.md) for the agent operating instructions, and
[workflows/00_overview.md](workflows/00_overview.md) for the full pipeline.

## Layout

```
workflows/   Markdown SOPs (00_overview … 06_decide_and_apply)
tools/       Python execution scripts (firecrawl_search, init_student, shortlist_schema,
             sync_shortlist, compare_universities, build_dossier, build_calendar)
data/students/   One private data bank per student (gitignored — PII)
.tmp/        Disposable intermediates (gitignored)
.env         Secrets only (gitignored)
```

## The pipeline at a glance

| Stage | Output | What you get |
|---|---|---|
| 1 Intake | `profile.json` | Grades, budget, English, recognition needs |
| 2 Aspirations | `preferences.json` | Countries, field, priorities (interest-discovery if undecided) |
| 3 Discover | `master_list.csv` (Longlist) | 20-40 candidates, scored |
| 4 Verify | `master_list.csv` (Shortlist) | 8-12, official facts, Reach/Match/Safety, comparison tables |
| 5a Dossier | `dossiers/<uni>.md` | 3-5 deep 14-section dossiers |
| 5b Decide | `recommendation.md` + `calendar.md` | Ranked picks, application strategy, deadlines |

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

Easiest: open this folder in VSCode and tell Claude **"run student intake for &lt;name&gt;"** — Claude reads
the workflows and drives all 5 stages, asking before any paid Firecrawl run. Or by hand:

```powershell
python tools/init_student.py "Aisyah Rahman"
#   ...Stage 1-2: fill profile.json / preferences.json in conversation...

python tools/firecrawl_search.py "BSc Computer Science UK entry requirements" --limit 6 --scrape-top 2
#   ...review .tmp/search_results.json, write .tmp/<slug>/uni_candidates.json (schema in workflow 03)...
python tools/sync_shortlist.py --student aisyah-rahman          # add --dry-run to preview

python tools/compare_universities.py --student aisyah-rahman --status Shortlist --dimensions all
#   ...narrow by editing the List status column; promote finalists...

python tools/build_dossier.py --student aisyah-rahman --input .tmp/aisyah-rahman/dossier_manchester-cs.json
python tools/build_calendar.py --student aisyah-rahman
```

Full instructions — the per-destination query playbook, scoring rubric, the 14-section dossier template,
and the narrowing rules — live in [workflows/](workflows/), starting with
[00_overview.md](workflows/00_overview.md).

## Notes

- **`Approx total (MYR)`** uses a rough offline FX table in `tools/shortlist_schema.py` — update the rates
  periodically; it's for apples-to-apples comparison, not financial precision.
- **Privacy:** `data/students/` is gitignored. It holds personal data (grades, finances, nationality) —
  keep it local, don't commit or share it.
