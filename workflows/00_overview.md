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
| 5a | `05_university_dossier.md` | `dossiers/<uni>.md` | Full 14-section dossier per finalist — 3-5 |
| 5b | `06_decide_and_apply.md` | `recommendation.md` + `calendar.md` | Recommendation, application strategy, one deadline calendar |

**Cross-cutting:** `resume.md` (utility, not a stage) — when a returning student says **"resume
&lt;name&gt;"**, it reconstructs state from `status.md` (cross-checked against the files) so a fresh
session skips the cold start. Update each student's `status.md` at the end of every stage.

## The data bank (one folder per student)

```
data/students/<student-slug>/
  status.md            # Session-handoff note — where we are / next action (resume.md; updated each stage)
  profile.json         # Stage 1
  preferences.json     # Stage 2
  master_list.csv      # Stages 3-4: every candidate + a "List status" column
  dossiers/<uni>.md    # Stage 5a
  recommendation.md    # Stage 5b
  calendar.md          # Stage 5b
```

**The master list is the narrowing surface.** Every candidate has a **`List status`**:
`Longlist` → `Shortlist` → `Finalist` (or `Rejected`). The student narrows by promoting/demoting rows;
`compare_universities.py` renders side-by-side tables for any subset at any time (use `--country <name>`
to work one destination at a time on a large list). `sync_shortlist.py` only ever *appends* new Longlist
rows — promotion/rejection is an agent edit to the CSV, never a sync side-effect.

The columns are defined once in `shortlist_schema.py` (`SHORTLIST_HEADERS`). Cell **values** should be
plain-English sentences, not jargon. Quick glossary of the less-obvious columns:
- **`Info source`** — where a fact came from: `Official` (the uni's own page / UCAS / Common App) or
  `Aggregator` (rankings sites, StudyPortals — discovery only). Hard facts must be `Official` by Stage 4.
- **`Dossier status`** — internal pipeline flag: whether the full 14-section deep-profile has been built
  yet (`Not started` / `Done`). The student can ignore it.
- **`Backup entry route`** — a way in if direct entry is a stretch (foundation year / INTO-Kaplan-Navitas
  pathway / community-college transfer).
- **Scholarship columns** — `Scholarship & portal`, `Scholarship coverage`, `Scholarship competitiveness`
  (with stats where they exist — never invented), `How to get the scholarship`.
- **`Student community links` / `Student life`** — student society / Discord / Reddit links, and a short
  run-through of student life with YouTube/Instagram links.
- Jargon to explain in cells, not headers: *"honours entry"* = a 4-year degree with a final research/
  project year; *"need-blind"* = the uni admits you without considering your ability to pay.

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
   on price alone.
2. **Official sources for hard facts.** Fees, entry requirements, English, deadlines, and intake must be
   verified against the **official** university / UCAS / Common App page before a row becomes `Shortlist`.
   Aggregators (StudyPortals, rankings, Niche) are for *discovery only*. Record `Info source` +
   `Data as-of` (cycle year) on every row. Where sources conflict, the official one wins; note the conflict.
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

`firecrawl_search.py` (discovery) · `init_student.py` (scaffold) · `shortlist_schema.py` (single source
of truth) · `sync_shortlist.py` (score/dedupe/append) · `compare_universities.py` (comparison tables) ·
`build_dossier.py` (14-section dossier) · `build_calendar.py` (deadline calendar).
