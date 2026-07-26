# Workflow: University & Course Finder — Overview (master SOP)

## Objective

Take a (Malaysian) student from *"who am I / what do I want"* all the way to *"here is exactly how I
apply to these specific universities"* — producing a ranked, **narrowed**, decision-ready set of
options with deep per-university reports, in one local data bank that opens in Excel / Google Sheets.

This is **agent-driven**. You (Claude) read these workflows, run the deterministic tools in `tools/`
in the right order, exercise judgement where research is needed, and recover from errors. The student
just talks to you.

## The four-stage narrowing pipeline (numbered 1, 3, 4, 5)

Research depth **escalates** as options survive each cut. Never burn deep-research effort on a
university that hasn't passed the cheap cut first.

| Stage | Workflow | Output | What it does |
|---|---|---|---|
| 1 | `01_intake.md` | `profile.json` + `preferences.json` | Who the student is (grades, budget, English, recognition needs) **and** what they want (countries, field, priorities) — batch-built from the Google Form CSV, then finalized by you |
| 3 | `03_discover_longlist.md` | `master_list.csv` (Longlist) | Broad, cheap, snippet-level discovery — 20-40 candidates |
| 4 | `04_university_dossier.md` | `dossiers/<uni>.md` | Student picks 3-5 finalists off the Longlist; **verify their hard facts from official sources** (Reach/Match/Safety, feasibility gates), then a full 16-section decision **university report** per finalist. Two paths (`--mode`): course-specific (default) or **university-general (US-only)** for whole-institution fit |
| 5 | `05_decide_and_apply.md` | `recommendation.md` + `calendar.md` | Recommendation, application strategy, one deadline calendar |

**Cross-cutting:** `resume.md` (utility, not a stage) — when a returning student says **"resume
&lt;name&gt;"**, it reconstructs state from `status.md` (cross-checked against the files) so a fresh
session skips the cold start. Update each student's `status.md` at the end of every stage.

**Apply-prep deliverable:** `08_application_prep.md` (utility, not a stage) — when a student has decided
to **apply broadly and compare offers first, research fit later**, this produces a per-region, action-only
"how to apply" guide grouped by application system (checklist + fees + tests + financial-aid forms/dates +
deadlines) via `build_application_prep.py`. Report-free and **read-only** (never changes `List status`).

> **Stage 2 was merged into Stage 1 on 2026-07-25.** Every student now arrives through the **Google
> Form**, which captures who-they-are and what-they-want in one sitting — so the two conversational
> SOPs (`01_student_intake.md`, `02_aspirations_intake.md`) were deleted and `07_form_intake.md`
> became `01_intake.md`. Stages 3-5 keep their file numbers, so **there is no Stage 2** — that gap is
> deliberate, not a missing file. The career-backwards interest-discovery branch went with them: the
> form stopped asking those questions, so the branch had no input data.

## The data bank (one folder per student)

```
data/students/<student-slug>/
  status.md            # Session-handoff note — where we are / next action (resume.md; updated each stage)
  profile.json         # Stage 1
  preferences.json     # Stage 1
  weights.json         # Stage 3: this student's desirability weights (scoring-weights skill; sync refuses without it)
  master_list.csv      # Stages 3-4: every candidate + a "List status" column
  score_log.jsonl      # Stage 3: append-only audit — weights_id + sub-scores + entry_margin behind each scored row
  dossiers/<uni>.md    # Stage 4  (dossiers/<uni>.pdf — optional, on request via dossier_to_pdf.py)
  recommendation.md    # Stage 5
  calendar.md          # Stage 5
  application_prep/<region>.md  # 08_application_prep.md — per-region "how to apply" guide (optional)
```

**The master list is the narrowing surface.** Every candidate has a **`List status`**:
`Longlist` → `Shortlist` → `Finalist` (or `Rejected`). The student narrows by promoting/demoting rows;
`compare_universities.py` renders side-by-side tables for any subset at any time (use `--country <name>`
to work one destination at a time on a large list). `sync_shortlist.py` only ever *appends* new Longlist
rows — promotion/rejection is an agent edit to the CSV, never a sync side-effect.

The columns are defined once in `shortlist_schema.py` (`SHORTLIST_HEADERS`). Cell **values** should be
plain-English sentences, not jargon — and that is **enforced**, by
`python tools/check_master_list.py --student <slug>`, which must come back clean before a list goes to a
student. Quick glossary of the less-obvious columns:
- **`Info source`** — how far a row's hard facts have been checked: `Not verified` (found via web search /
  rankings sites — discovery only) or `Official page` (confirmed on the uni's own page / UCAS / Common
  App). Every row must read `Official page` by Stage 4.
- **`Grades vs entry bar`** — `Well above` / `Above` / `Meets` / `Below` / `Well below`, or
  `Not published` where the university sets no academic cutoff. It answers **grades only**. Why a row is
  hard to get into lives next door in `Admission likelihood`, which can carry a short reason —
  `Reach (very selective)`. Keeping those two apart is the whole point; see guardrail 1.
- **`Course at a glance`** / **`Student life`** — one tight sentence each. Blank until someone has
  actually researched it (Stage 4 fills them on promotion); an invented sentence is a fabricated fact.
- **Cell length budgets** — `CELL_BUDGETS` in `shortlist_schema.py`. The list is a *scanning* surface;
  long-form research goes to `data/students/<slug>/research_notes.md` instead, and nothing is ever
  silently truncated.
- **Scholarship columns** — `Scholarship & portal`, `Scholarship coverage`, `Scholarship competitiveness`
  (with stats where they exist — never invented), `How to get the scholarship`. When researching these,
  respect **eligibility**: `preferences.scholarship_interests` says which scholarships the student wants
  looked into, and `profile.ethnicity` gates ethnicity-restricted Malaysian funds (e.g. Bumiputra-only vs
  open) — surface only ones the student can actually claim. Ethnicity is a research signal only, never a
  desirability input.
- **`Approx total (MYR)`** — the whole-programme cost, roughly converted. Computed from the candidate
  JSON's `currency` + `total_cost_programme`/`total_tuition`, none of which have columns of their own.
- Jargon to explain in cells, not headers: *"honours entry"* = a 4-year degree with a final research/
  project year; *"need-blind"* = the uni admits you without considering your ability to pay.

> **The schema went 34 → 35 columns on 2026-07-25** (a student review found the list unreadable in
> Google Sheets). `Fits grades?` → **`Grades vs entry bar`**, now derived from `entry_margin` alone;
> `Backup entry route` moved into the Stage-4 university report; **`Course at a glance`** and **`Student life`**
> added. Two companion files per student came with it: **`research_notes.md`** (the long-form research
> the cells no longer hold) and **`glossary.csv`** (a Glossary tab explaining the shorthand that
> student's list actually uses, from `tools/build_glossary_sheet.py`).

> **The schema was slimmed 41 → 34 columns on 2026-07-16.** It is read in Google Sheets, and seven columns
> were blank in practice, duplicated another column, or were internal bookkeeping: `Meets English?`,
> `Total cost (programme)`, `Currency`, `Student community links`, `Student life`, `Data as-of`,
> `Dossier status`. **Removing a column ≠ removing the fact** — `currency` and `meets_english` are still
> required candidate-JSON fields feeding `Approx total (MYR)` and the `English short` warning, and
> student-life research now lives in the Stage 4 university report where paragraphs belong. `Info source` values were
> renamed `Aggregator`→`Not verified` and `Official`→`Official page` at the same time.

## How to start

Export the Google Form responses to CSV, drop it in `data/form/` (gitignored — PII), and tell Claude
**"ingest the form responses."** Claude runs `ingest_form_csv.py`, finalizes the judgment-heavy fields
per student (Stage 1), then walks Stage 3 → 4 → 5. Or by hand from the repo root with the venv active:

```powershell
.\.venv\Scripts\Activate.ps1
python tools/ingest_form_csv.py "data/form/responses.csv" --dry-run   # preview first
python tools/ingest_form_csv.py "data/form/responses.csv"
#   ...then follow workflows 01 -> 03 -> 04 -> 05 (there is no 02)...
```

`init_student.py` still exists for scaffolding one student's folder by hand, and its templates are the
schema source of truth — but the normal path is the form.

## Non-negotiable design rules (the anti-loophole guardrails)

These are *why this project exists* — they stop a tidy-looking list from being quietly wrong:

1. **Desirability ≠ admissibility.** The 0-100 desirability score deliberately excludes entry fit.
   Whether the student can actually get in lives in **`Admission likelihood`** (Reach/Match/Safety) and
   **`Warnings`**, shown next to the score. A university you can't enter must never rank highly
   on price alone. **This rule is now enforced in code:** `validate_weights()` rejects `entry_fit`,
   `admission_fit`, `admissibility`, and `entry_margin_fit` as weight keys.
   Weights themselves are **per-student** (`data/students/<slug>/weights.json`, via the
   `scoring-weights` skill) and never live in shared source — so two students can be scored in parallel.
   **The same rule applies one level down, inside admissibility itself** (learned the hard way,
   2026-07-25): *can I meet the grades?* and *will they take me?* are different questions.
   `entry_margin` answers only the first and produces **`Grades vs entry bar`**; holistic selectivity,
   capped international quotas and need-aware admission go in the `admission_likelihood` override, which
   renders `Reach (very selective)`. Conflating them printed "doesn't fit the grades" for a student with
   A\*A\*A\*A at Duke. `check_master_list.py` now fails on that contradiction.
   **Provisional grades:** when `profile.grade_status == "expected"` (grades the student is only
   *confident of getting*, e.g. from the form intake), admission likelihood is still computed but is
   **provisional** — `sync_shortlist.py` stamps a "Grades unverified (self-predicted)" warning on every
   row. The list must not read as settled until actual/official predicted results arrive.
2. **Official sources for hard facts.** Fees, entry requirements, English, deadlines, and intake must be
   verified against the **official** university / UCAS / Common App page before you build a row's report
   (the Stage 4 pre-flight — a row can't become `Finalist` on unverified facts). Aggregators (StudyPortals,
   rankings, Niche) are for *discovery only*. Record `Info source` on every row. Where sources conflict,
   the official one wins; note the conflict in `Notes`.
3. **Total cost, not annual.** Compare full-programme **total cost in MYR** (3-yr UK vs 4-yr US are not
   comparable per year). `Approx total (MYR)` is a rough offline conversion — flag it as approximate.
4. **Balanced list.** A shortlist is a spread of Reach/Match/Safety, not the top-N by score.
5. **Recognition back home matters.** For regulated professions (medicine, engineering, law, accounting,
   pharmacy, etc.), check **MQA recognition + the relevant Malaysian professional body**. A degree that
   won't let the student practise in Malaysia is a dealbreaker, not a footnote. The
   profession → body mapping (MMC / BEM+Washington Accord / LPQB / MIA+ACCA / LAM / …) lives in
   `01_intake.md`, finalize step 4 — `ingest_form_csv.py` auto-fills it best-effort, and you verify.
6. **Right scraper for the job — no permission needed.** `firecrawl_search.py` costs credits; **spend
   them, don't ask** (the gate was removed 2026-07-27 — it stalled every stage for no safety gain).
   What survives is *routing*, and it is about what works, not what costs: **free WebSearch/WebFetch
   for decision texture** (Reddit, The Student Room, YouTube, student societies — IG/FB/TikTok/X are
   hard-skipped inside `firecrawl_search.py`, so credits buy nothing there), **Firecrawl for official
   pages that block a plain fetch** (fee tables, fee PDFs, walled scholarship/visa pages), where an
   exact figure beats "confirm later". Tune `--limit`/`--scrape-top` for signal, not for spend:
   scraped pages land in context and dilute it.

## Privacy (PDPA)

The student's data bank holds personal data (grades, finances, nationality). `data/students/` is
**gitignored** — never commit it, never share it beyond the student. Collect sensitive fields
(financials, anything about race/religion via `needs`) only with the student's consent, and keep them local.

## Tools (deterministic layer) — see each workflow for usage

`firecrawl_search.py` (discovery) · `init_student.py` (scaffold) · `ingest_form_csv.py` (batch-scaffold
from a Google Form CSV) · `shortlist_schema.py` (single source of truth) · `sync_shortlist.py`
(score/dedupe/append) · `compare_universities.py` (comparison tables) · `build_dossier.py` (16-section
university report; `--mode course` default or `--mode university` for US whole-institution) · `dossier_to_pdf.py`
(export a report to PDF for the student) · `build_calendar.py`
(deadline calendar) · `build_application_prep.py` (per-region apply guide grouped by application system).
