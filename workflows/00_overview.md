# Workflow: University & Course Finder — Overview (master SOP)

## Objective

Take a (Malaysian) student from *"who am I / what do I want"* all the way to *"here is exactly how I
apply to these specific universities"* — producing a ranked, **narrowed**, decision-ready set of
options with deep per-university dossiers, in one local data bank that opens in Excel / Google Sheets.

This is **agent-driven**. You (Claude) read these workflows, run the deterministic tools in `tools/`
in the right order, exercise judgement where research is needed, and recover from errors. The student
just talks to you.

## The 5-stage narrowing pipeline

Research depth **escalates** as options survive each cut. Never burn deep-research effort on a
university that hasn't passed the cheap cut first.

| Stage | Workflow | Output | What it does |
|---|---|---|---|
| 1 | `01_student_intake.md` | `profile.json` | Who the student is (grades, budget, English, recognition needs) |
| 2 | `02_aspirations_intake.md` | `preferences.json` | What they want (countries, field, priorities) — incl. *interest-discovery* if undecided |
| 3 | `03_discover_longlist.md` | `master_list.csv` (Longlist) | Broad, cheap, snippet-level discovery — 20-40 candidates |
| 4 | `04_verify_shortlist.md` | `master_list.csv` (Shortlist) | Verify hard facts from official sources; Reach/Match/Safety; feasibility gates; comparison tables — cut to 8-12 |
| 5a | `05_university_dossier.md` | `dossiers/<uni>.md` | Full 16-section decision dossier per finalist — 3-5 |
| 5b | `06_decide_and_apply.md` | `recommendation.md` + `calendar.md` | Recommendation, application strategy, one deadline calendar |

**Cross-cutting:** `resume.md` (utility, not a stage) — when a returning student says **"resume
&lt;name&gt;"**, it reconstructs state from `status.md` (cross-checked against the files) so a fresh
session skips the cold start. Update each student's `status.md` at the end of every stage.

**Apply-prep deliverable:** `08_application_prep.md` (utility, not a stage) — when a student has decided
to **apply broadly and compare offers first, research fit later**, this produces a per-region, action-only
"how to apply" guide grouped by application system (checklist + fees + tests + financial-aid forms/dates +
deadlines) via `build_application_prep.py`. Dossier-free and **read-only** (never changes `List status`).

**Alternate on-ramp:** `07_form_intake.md` replaces the conversational Stages 1-2 with a **Google
Form**. Others fill the form; you export the CSV to `data/form/` and run `ingest_form_csv.py`, which
batch-creates `profile.json` + `preferences.json` per respondent. You then finalize a few
judgment-heavy fields (grades → subjects, recognition targets, undecided students) and continue at
Stage 3. Use this to help many students without driving each intake by hand.

## The data bank (one folder per student)

```
data/students/<student-slug>/
  status.md            # Session-handoff note — where we are / next action (resume.md; updated each stage)
  profile.json         # Stage 1
  preferences.json     # Stage 2
  weights.json         # Stage 3: this student's desirability weights (scoring-weights skill; sync refuses without it)
  master_list.csv      # Stages 3-4: every candidate + a "List status" column
  score_log.jsonl      # Stage 3: append-only audit — weights_id + sub-scores + entry_margin behind each scored row
  dossiers/<uni>.md    # Stage 5a  (dossiers/<uni>.pdf — optional, on request via dossier_to_pdf.py)
  recommendation.md    # Stage 5b
  calendar.md          # Stage 5b
  application_prep/<region>.md  # 08_application_prep.md — per-region "how to apply" guide (optional)
```

**The master list is the narrowing surface.** Every candidate has a **`List status`**:
`Longlist` → `Shortlist` → `Finalist` (or `Rejected`). The student narrows by promoting/demoting rows;
`compare_universities.py` renders side-by-side tables for any subset at any time (use `--country <name>`
to work one destination at a time on a large list). `sync_shortlist.py` only ever *appends* new Longlist
rows — promotion/rejection is an agent edit to the CSV, never a sync side-effect.

The columns are defined once in `shortlist_schema.py` (`SHORTLIST_HEADERS`). Cell **values** should be
plain-English sentences, not jargon. Quick glossary of the less-obvious columns:
- **`Info source`** — how far a row's hard facts have been checked: `Not verified` (found via web search /
  rankings sites — discovery only) or `Official page` (confirmed on the uni's own page / UCAS / Common
  App). Every row must read `Official page` by Stage 4.
- **`Backup entry route`** — a way in if direct entry is a stretch (foundation year / INTO-Kaplan-Navitas
  pathway / community-college transfer).
- **Scholarship columns** — `Scholarship & portal`, `Scholarship coverage`, `Scholarship competitiveness`
  (with stats where they exist — never invented), `How to get the scholarship`.
- **`Approx total (MYR)`** — the whole-programme cost, roughly converted. Computed from the candidate
  JSON's `currency` + `total_cost_programme`/`total_tuition`, none of which have columns of their own.
- Jargon to explain in cells, not headers: *"honours entry"* = a 4-year degree with a final research/
  project year; *"need-blind"* = the uni admits you without considering your ability to pay.

> **The schema was slimmed 41 → 34 columns on 2026-07-16.** It is read in Google Sheets, and seven columns
> were blank in practice, duplicated another column, or were internal bookkeeping: `Meets English?`,
> `Total cost (programme)`, `Currency`, `Student community links`, `Student life`, `Data as-of`,
> `Dossier status`. **Removing a column ≠ removing the fact** — `currency` and `meets_english` are still
> required candidate-JSON fields feeding `Approx total (MYR)` and the `English short` warning, and
> student-life research now lives in the Stage 5 dossier where paragraphs belong. `Info source` values were
> renamed `Aggregator`→`Not verified` and `Official`→`Official page` at the same time.

## How to start

Tell Claude the student's name and say **"run student intake."** Claude runs `init_student.py`, then
walks Stage 1 → 2 → 3 → 4 → 5. Or by hand from the repo root with the venv active:

```powershell
.\.venv\Scripts\Activate.ps1
python tools/init_student.py "Aisyah Rahman"
#   ...then follow workflows 01 -> 06...
```

## Non-negotiable design rules (the anti-loophole guardrails)

These are *why this project exists* — they stop a tidy-looking list from being quietly wrong:

1. **Desirability ≠ admissibility.** The 0-100 desirability score deliberately excludes entry fit.
   Whether the student can actually get in lives in **`Admission likelihood`** (Reach/Match/Safety) and
   **`Warnings`**, shown next to the score. A university you can't enter must never rank highly
   on price alone. **This rule is now enforced in code:** `validate_weights()` rejects `entry_fit`,
   `admission_fit`, `admissibility`, and `entry_margin_fit` as weight keys.
   Weights themselves are **per-student** (`data/students/<slug>/weights.json`, via the
   `scoring-weights` skill) and never live in shared source — so two students can be scored in parallel.
2. **Official sources for hard facts.** Fees, entry requirements, English, deadlines, and intake must be
   verified against the **official** university / UCAS / Common App page before a row becomes `Shortlist`.
   Aggregators (StudyPortals, rankings, Niche) are for *discovery only*. Record `Info source` on every
   row. Where sources conflict, the official one wins; note the conflict in `Notes`.
3. **Total cost, not annual.** Compare full-programme **total cost in MYR** (3-yr UK vs 4-yr US are not
   comparable per year). `Approx total (MYR)` is a rough offline conversion — flag it as approximate.
4. **Balanced list.** A shortlist is a spread of Reach/Match/Safety, not the top-N by score.
5. **Recognition back home matters.** For regulated professions (medicine, engineering, law, accounting,
   pharmacy, etc.), check **MQA recognition + the relevant Malaysian professional body**. A degree that
   won't let the student practise in Malaysia is a dealbreaker, not a footnote.
6. **Credits are gated.** `firecrawl_search.py` costs money. **Ask the user before running it.** Use
   built-in web search/fetch for quick free checks; reserve Firecrawl for scraping clean prospectus pages.

## Privacy (PDPA)

The student's data bank holds personal data (grades, finances, nationality). `data/students/` is
**gitignored** — never commit it, never share it beyond the student. Collect sensitive fields
(financials, anything about race/religion via `needs`) only with the student's consent, and keep them local.

## Tools (deterministic layer) — see each workflow for usage

`firecrawl_search.py` (discovery) · `init_student.py` (scaffold) · `ingest_form_csv.py` (batch-scaffold
from a Google Form CSV) · `shortlist_schema.py` (single source of truth) · `sync_shortlist.py`
(score/dedupe/append) · `compare_universities.py` (comparison tables) · `build_dossier.py` (16-section
dossier) · `dossier_to_pdf.py` (export a dossier to PDF for the student) · `build_calendar.py`
(deadline calendar) · `build_application_prep.py` (per-region apply guide grouped by application system).
