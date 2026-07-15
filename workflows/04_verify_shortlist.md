# Workflow: Stage 4 — Verify → Shortlist (the first real narrowing cut)

## Objective

Turn a broad, provisional Longlist into a **trustworthy, balanced Shortlist of 8-12** by verifying hard
facts against official sources, re-judging admissibility, surfacing feasibility gates, and walking the
student through comparison tables. This is where most options get cut.

## Step-by-step

> **Work one country at a time.** Verifying + researching 23 rows in one pass is token-heavy. Pick a
> destination, pull just its rows with `compare_universities.py --student <slug> --country <name>`, do the
> full treatment below for those, review, then move to the next country in a later session. This is the
> agreed rhythm for Toru (2026-07-05).

### 1. Verify hard facts from OFFICIAL sources
For the top Longlist rows (work down by desirability, but keep a spread — see step 3), confirm against the
**official** source — the university's own course page, UCAS, or Common App — never an aggregator:

- **Tuition** (per year + full programme) and **est. living cost** → recompute total; check `Approx total (MYR)`.
- **Entry requirements** (academic + English) → does the student actually meet them?
- **Key deadline** + **intake** → is the intake offered, and is the deadline still open?
- **Scholarships** the student is realistically eligible for.

Update each verified row: set **`Info source = Official`** and **`Data as-of`** to the cycle year.
Where the official page disagrees with what an aggregator said, **the official figure wins** — put the
discrepancy in `Notes`. (Verifying may need a couple of Firecrawl scrapes of clean official pages —
**ask the user before running**, per `00_overview.md`.)

### 1b. Research the scholarship + student-life columns (Toru's request, 2026-07-05)
The master list now leads with **scholarships** and **student life**. For each row you're keeping, fill the
new columns in **complete, plain-English sentences** (no jargon — this is what the student reads):

- **`Scholarship & portal`** — which scholarship(s) apply + the exact page to apply on (link). Scholarship
  is now a **required** priority: every kept university must have a realistic route documented. But a
  hard-to-win scholarship is **not** a reason to drop a university — document it instead.
- **`Scholarship coverage`** — how much it covers: full ride / tuition-only / a % / a fixed amount.
- **`Scholarship competitiveness`** — how hard it is to win, with **statistics where they exist** (award
  rate, number of awards, typical profile). If no stats are published, say so — never invent numbers.
- **`How to get the scholarship`** — eligibility + steps + any separate scholarship deadline.
- **`Student community links`** — links to student society / Discord / Reddit / Facebook groups for the
  course or uni (these pages don't scrape via Firecrawl — capture the URL from free web search).
- **`Student life`** — a short plain-English run-through of what studying this course there is like, with
  links to YouTube "day in the life" videos, student vlogs, or Instagram pages where you find them.

Also **re-score** the row under the student's `weights.json` (`data/students/<slug>/weights.json` — see the
`scoring-weights` skill) and rewrite `Desirability`/`Tier`, since verification usually changes the facts the
sub-scores were judged from. No weight ordering is stated here on purpose: it is per-student data, and a
shared doc naming one student's ordering is how the old drift started.

### 2. Re-judge admissibility & feasibility
With verified facts, re-confirm each row's:
- **Admission likelihood** (Reach/Match/Safety) — does the student's `grade_status` (predicted vs actual)
  change this? Predicted grades keep most options Reach/Match until results land.
- **Warnings** — `Deadline passed`, `English short`, `Over budget`. These are hard warnings shown
  next to the score; they don't lower the score, they gate the option. (Re-running `sync_shortlist.py` is
  only for *new* candidates — to update an existing row's verified facts, edit `master_list.csv` directly.)

### 3. Build a BALANCED shortlist (not top-N by score)
Promote survivors to **`List status = Shortlist`** so the set is a spread:
- a few **Safety** (clears requirements comfortably, affordable),
- several **Match** (meets requirements), and
- a couple of **Reach** (aspirational) — but only if worth it.

Demote the rest to **`Rejected`** with a one-line reason in `Notes` (e.g. "Over budget even with
scholarship", "Deadline passed for 2027 intake", "Subject rank weak for the field"). Don't silently drop
rows — a recorded reason lets the student push back.

### 4. Compare and walk the student through the cut
Render comparison tables and discuss trade-offs:

```powershell
python tools/compare_universities.py --student <slug> --country Australia --status Longlist --dimensions summary,scholarship,fit
python tools/compare_universities.py --student <slug> --status Shortlist --dimensions all --save
```
Presets: `summary, cost, scholarship, life, quality, fit, visa, deadline, all`. Use `--country <name>` to
work one destination at a time. Show `scholarship` to compare funding (Toru's #1 priority), `life` for
community/student-life, `fit` to explain a Reach. Iterate: the student may want to keep or re-add a row;
that's the narrowing loop working.

### 5. Record pathway options for kept Reaches
For any Reach worth keeping where direct entry is a stretch, fill **`Backup entry route`** (foundation year /
INTO–Kaplan–Navitas / US community-college transfer) and its rough entry bar — so a grades-short student
still has a route, instead of just being told "no".

## Edge cases & rules

- **Predicted grades** — be explicit that admissibility is provisional until actual results; lean toward
  labelling borderline cases Reach.
- **Conflicting fees/deadlines** — official source wins; always stamp `Data as-of` so staleness is visible
  next cycle.
- **Too few survivors** — if the cut leaves <6, go back to Stage 3 and widen discovery (more countries or
  safer options) rather than promoting weak rows.

## Done when

`master_list.csv` has 8-12 **Shortlist** rows with `Info source = Official` on their hard facts, the
scholarship + student-life columns filled in plain English, a healthy Reach/Match/Safety spread, and
rejected rows annotated. Then proceed to **Stage 5a** (`05_university_dossier.md`).
