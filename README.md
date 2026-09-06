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
| 4 Verify + Report | `reports/<uni>.md` | Student picks 3-5 finalists; verify their facts against official sources (Reach/Match/Safety), then a deep 15-section **university report** each |
| 5 Decide | `recommendation.md` + `calendar.md` | Ranked picks, application strategy, deadlines |

There is **no Stage 2** — intake and aspirations merged into Stage 1 on 2026-07-25, when the Google
Form became the only on-ramp. Stages 3-5 kept their numbers rather than renumber the whole repo.

Stage 4's per-finalist research-and-report step also runs on a different model — Claude dispatches it
to a subagent pinned to **Opus** (it's the deepest, highest-stakes writing task in the pipeline), while
everything else, including Stage 4's own pick/verify/cut checkpoint with you, runs on the normal session
model. This happens automatically; there's nothing you need to run or configure.

**`/social [topic]`** is outside the student pipeline — a repo-maintenance utility that drafts a
confidentiality-checked Twitter/X post or thread about recent repo work (a commit, an incident
writeup, a decision), never about a student. It's pull-only and never posts anything itself; see
[workflows/social_media.md](workflows/social_media.md).

## Setup (first time)

```powershell
# 1. Create + activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Firecrawl key(s) to .env  (copy .env.example -> .env)
#    FIRECRAWL_API_KEY=fc-...
#    # optional: add more keys as FIRECRAWL_API_KEY_<label> — the tool rotates to the
#    # next one automatically once a key runs out of credits (HTTP 402)
#    FIRECRAWL_API_KEY_blaze=fc-...
#    FIRECRAWL_API_KEY_kon=fc-...
```

**4. Wire up the form-response feed** (one time, so intake can pull responses instead of you
downloading a CSV every run):

1. Open the form's **responses spreadsheet** → Extensions → Apps Script. Paste the contents of
   [tools/appsscript/Code.gs](tools/appsscript/Code.gs) over whatever's there and save.
2. Project Settings → Script Properties → add **`FORM_TOKEN`** = a long random string. It never goes
   in the source; `Code.gs` is committed to git.
3. Deploy → New deployment → type **Web app**, *Execute as* **Me**, *Who has access* **Anyone**. Copy
   the `/exec` URL. (It has to be "Anyone" — anything narrower returns a Google login page instead of
   JSON. The token is the gate.)
4. Add both to `.env`:
   ```
   FORM_WEBAPP_URL=https://script.google.com/macros/s/.../exec
   FORM_WEBAPP_TOKEN=<the same string you set as FORM_TOKEN>
   ```

The deployed URL is public and the token is the only gate — keep it long and random, and keep it in
`.env` (already gitignored). **To revoke access**, change `FORM_TOKEN` in Script Properties, redeploy,
and update `.env`. You don't need to create the `Ingested at` column yourself — the script appends it
as the last column on first call. If any of this isn't set up, intake still works via the manual CSV
export; see [workflows/01_intake.md](workflows/01_intake.md).

## Run

**Intake is a Google Form.** Students request a search by filling it in; the responses become student
data banks in bulk. Build the form once — the exact questions, sections, and consent gate are in
[workflows/01_intake.md](workflows/01_intake.md) — then pull responses with
`tools/fetch_form_responses.py`, which writes **`data/form/responses.csv`** (gitignored — PII) and
hands back only respondents not yet ingested. Manual export still works as a fallback.

Easiest: open this folder in VSCode and tell Claude **"ingest the form responses"** — Claude reads the
workflows, finalizes the judgment-heavy fields per student (grades → subjects, recognition targets,
degree level), and drives the remaining stages. Or by hand:

```powershell
python tools/fetch_form_responses.py --dry-run                        # who's pending
python tools/fetch_form_responses.py                                  # -> data/form/responses.csv
python tools/ingest_form_csv.py "data/form/responses.csv" --dry-run   # preview
python tools/ingest_form_csv.py "data/form/responses.csv"             # create folders
#   ...Stage 1: finalize each student's _needs_review items, then delete the key...
python tools/fetch_form_responses.py --confirm                        # LAST: mark them done in the sheet

#   ...Stage 3: ask Claude to derive data/students/<slug>/weights.json (the 'scoring-weights' skill)
#      — per-student scoring weights; sync refuses to run without them...

python tools/firecrawl_search.py --student <slug> "BSc Computer Science UK entry requirements" --limit 6 --scrape-top 2
#   ...review .tmp/<slug>/search_results.json, write .tmp/<slug>/uni_candidates.json (schema in workflow 03)...
python tools/sync_shortlist.py --student <slug>          # add --dry-run to preview

python tools/compare_universities.py --student <slug> --status Shortlist --dimensions all
#   ...narrow by editing the List status column; promote finalists...

python tools/build_report.py --student <slug> --input .tmp/<slug>/report_manchester-cs.json
#   ...one build_report.py per finalist; each writes a report + a marker, not a CSV change...
python tools/flip_finalists.py --student <slug>    # ONCE: folds every marker into the CSV
python tools/build_calendar.py --student <slug>
```

`tools/init_student.py` still scaffolds a single student folder by hand (and its templates are the
schema source of truth that `ingest_form_csv.py` imports), but the form is the normal way in.

Full instructions — the per-destination query playbook, scoring rubric, the 15-section university-report template,
and the narrowing rules — live in [workflows/](workflows/), starting with
[00_overview.md](workflows/00_overview.md).

### Running a stage with Claude

**Don't use plan mode for a normal run.** The workflow files already *are* the plan, so planning one
re-derives what's on disk and costs a whole extra pass. Say what you want ("build the longlist",
"resume <slug>") and let Claude read the workflow and execute. Save plan mode for changing the
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
