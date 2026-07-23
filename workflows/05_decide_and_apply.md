# Workflow: Stage 5b — Decide & Apply (recommendation + strategy + calendar)

## Objective

Turn the finalist dossiers into a **decision**: a ranked recommendation with reasoning, a realistic
application strategy, and one consolidated deadline calendar so nothing gets missed. This stage is
research/decision support — it documents *how* to apply and *when*; it does **not** track the actual
application (no submission/offer state in v1).

## Step-by-step

### 1. Final comparison
```powershell
python tools/compare_universities.py --student <slug> --status Finalist --dimensions all --save
```
Walk the student through it across cost, quality, fit, visa, and deadlines. This is the last narrowing
surface before the recommendation.

### 2. Write `recommendation.md`
Save to `data/students/<slug>/recommendation.md`. Include:

- **Ranked recommendation** — the finalists in recommended order, each with 2-3 sentences of *why* (tie it
  back to the student's `priorities`: cost, employability, recognition, ranking, location).
- **The balanced picture** — confirm the set spans Reach/Match/Safety so the student isn't betting on
  long-shots alone.
- **Application strategy** — respect the real constraints:
  - **UK / UCAS**: a maximum of **5 choices**, and you **cannot apply to both Oxford and Cambridge** in the
    same cycle. Help choose the 5.
  - **USA / Common App**: each school charges an **application fee** (and often extra essays/tests) — factor
    total application cost into how many to apply to.
  - **Budget across the set** — total deposits + application fees + visa costs should fit the student's means.
  - **Direct-application destinations** (Singapore/Malaysia, China) have their own portals and timelines.
- **Open risks / to-confirm** — predicted-grade dependencies, pending English test, scholarship outcomes.

### 3. Build the deadline calendar
```powershell
python tools/build_calendar.py --student <slug>
```
This aggregates every dated item across finalists — application deadlines (from `master_list.csv`) plus any
`dated_items` in the dossier JSONs (scholarship deadlines, test dates, visa lead times) — into one
chronological `calendar.md`. Review it with the student and flag the earliest actions.

### 4. Per-finalist how-to-apply recap
In `recommendation.md` (or pointing back to each dossier's section 12), restate for each recommended
university: the portal, the steps, and the documents needed (transcripts, personal statement/essays,
references, English test, portfolio/interview if required). For reference and planning — not tracked as
state in v1.

## Edge cases & rules

- **Predicted grades** — make the strategy conditional: which choices hold if results come in lower, and
  where the pathway/foundation fallbacks (from Stage 4/5a) kick in.
- **Scholarship-dependent students** — sequence scholarship deadlines *before* the student commits deposits;
  the calendar should make those the earliest items.
- **Don't over-promise** — present a recommendation and the trade-offs; the decision is the student's.

## Done when

`recommendation.md` and `calendar.md` exist, the student understands the ranked options and the application
plan, and the earliest deadlines are clearly flagged. The pipeline is complete.

## Future scope (not in v1)

A stateful application tracker (documents / references / submission / offers / deposits) and admissions-test
+ personal-statement planning are deliberately out of scope this round — see the plan's "future
enhancements".
