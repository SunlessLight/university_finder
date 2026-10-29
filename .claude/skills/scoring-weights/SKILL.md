---
name: scoring-weights
description: "Use when a student's weights.json must be made or redone (before sync_shortlist.py, or after their priorities change), or if tempted to edit weights inside tools/shortlist_schema.py (don't)."
---

## When to use

Use when a student needs data/students/<slug>/weights.json created or re-derived — before running sync_shortlist.py (Stage 3 / workflows/03_discover_longlist.md), or after a student's priorities change. As of 2026-09-17 this is a mechanical derivation (tools/derive_weights.py), not agent judgment — run the tool, don't hand-write the file. ALSO use if you are tempted to edit weights, SCORE_WEIGHTS, or any weighting inside tools/shortlist_schema.py — don't: that file is shared source, weights are per-student and live in the data bank, and hand-editing it collides with concurrent sessions.

# Deriving per-student scoring weights

> Changed 2026-10-29 (plans/list_pdf_plan.md T10; additionals R39): weights now come from the
> tick **points** (`preferences.priority_levels`), not the 1–8 order, so equal ticks get equal
> weight. Profiles with only `priorities` (older forms) keep the rank formula. The
> Urban+Rural flag moved to Stage 1 `_needs_review` (T1).

The desirability score is a weighted sum of eight 0-5 sub-scores. The weights are
**per-student data** — never shared source — and, as of 2026-09-17, a **pure function
of `preferences.json`**, computed by `tools/derive_weights.py`. No agent judgment is
involved in the normal case: run the tool.

## Why this changed (2026-09-17)

The weights used to be derived by reading the student's priorities plus half a dozen
qualitative modifiers (regulated profession, contradictory location, budget-null
interpretation, notes/deal-breakers overriding structured fields, distrust of flat
slider spreads). That was a real judgment step with a real error rate, on a number
almost nobody downstream actually looks at — students and parents read the research,
not the weight vector. Evan's call: make it mechanical, and move everything that used
to *adjust a weight* into a **Warnings-column flag** instead (surfaced next to the
score, the same place "Over budget" and "Deadline passed" already live) — see
`feasibility_flags()` in `tools/shortlist_schema.py`:
- `Recognition risk — check <targets>` — fires when the student
  has `recognition_targets` set and the row's `recognition_fit` sub-score is low
  (≤2/5), regardless of that row's weight.
- Urban+Rural both ticked is no longer a Warnings flag: since 2026-10-29 it is a
  Stage 1 `_needs_review` item (`ingest_form_csv.py`), settled at finalize.

## Run it

```
python tools/derive_weights.py --student <slug>
python tools/derive_weights.py --student <slug> --dry-run   # preview only
```

That's the whole procedure. It picks one of two formulas, applies the ONE remaining
override (below), floors `course_match`, and writes `weights.json` with an
auto-generated `rationale` and an auto-bumped `weights_id`. Full formula and reasoning
live in the tool's own docstring — read that, not this file, if you need the mechanics.

- **`preferences.priority_levels` present** (the current tick form): Must have 3 points,
  Important 2, Nice to have 1, Doesn't matter 0; weight = points ÷ total points. Equal
  ticks, equal weight; all equal (or all 0) → 0.125 each. A "Doesn't matter" topic gets
  0 (except `course_match`, floored). No key above 0.5: an over-cap key is cut and the
  excess shared out.
- **Only `preferences.priorities`** (older slider/dropdown forms): the 8-way ranking,
  linear 0.20 (rank 1) → 0.05 (rank 8). Unchanged since 2026-09-17.

Old students' `preferences.json` has no `priority_levels` (it was only kept from
2026-10-29), so their weights still come from the order. To move one onto points, re-read
the tick answers from the form export into `priority_levels` (no `--force` re-ingest),
then re-run the tool and re-sync — only for a list being re-sent (R39).

## The one override that survived

`scholarship_required: true` makes scholarship a Must have (3 points) in the points
formula, or moves `scholarship_opportunity` to rank 1 in the rank formula, regardless of
what the student ticked. This is not "judgment" — it's a hard financial gate: a student
can rate scholarship low on "what I care about" while still being unable to attend
anything without one. Everything else the old modifiers did is gone (see "Why this
changed" above).

## Where weights live (and why it matters)

`data/students/<slug>/weights.json`. **Nothing student-specific goes in
`tools/shortlist_schema.py`.** That file is shared and git-tracked: a weight
hardcoded there is a weight two concurrent sessions overwrite for each other,
silently, with no error and no trace in the CSV.

`sync_shortlist.py` **hard-errors** without a valid `weights.json`. That's intended:
scoring under weights nobody derived produces numbers indistinguishable from chosen
ones.

## The file

```json
{
  "weights_id": "<slug>-v1",
  "student": "<slug>",
  "derived_from": "preferences.json (mechanical derivation, tools/derive_weights.py, 2026-09-17)",
  "derived_on": "2026-09-17",
  "rationale": "Mechanically derived by tools/derive_weights.py from preferences.priority_levels (...). Formula: Must have 3 points, Important 2, ...",
  "weights": { "subject_reputation": 0.20, "scholarship_opportunity": 0.1914, "course_match": 0.08,
               "post_study_work_fit": 0.1571, "total_cost_fit": 0.1786, "recognition_fit": 0.1143,
               "location_pref_fit": 0.05, "experiential_fit": 0.0929 }
}
```

- `weights_id` — `<slug>-v<n>`, auto-bumped by the tool on every run. **Never edit in
  place** — old `score_log.jsonl` lines carry the old id and must stay interpretable.
- `rationale` — auto-generated by the tool; `load_weights` still rejects a blank one.

## Mapping: priority token -> weight key

```
ranking -> subject_reputation        recognition -> recognition_fit
scholarship -> scholarship_opportunity   employability -> post_study_work_fit
cost -> total_cost_fit               location -> location_pref_fit
hands-on experience -> experiential_fit  course_quality -> course_match
```

The same tokens key `priority_levels`. Either input must be **complete** (all 8
tokens). `priority_levels` missing a token (a blank tick) → the tool refuses; ask the
student and add the level. A partial/legacy `priorities` list (an old 3-priority form
response) → the tool refuses; derive `weights.json` by hand for that one student,
following the shape above.

`ranking_importance` is **no longer read** by weight derivation — `priority_levels` /
`priorities` supersede it. It's kept in `preferences.json` for context only
(e.g. Stage 4 write-ups quoting how strongly a student felt about it).

### Never weight admissibility

`entry_fit`, `admission_fit`, `admissibility`, `entry_margin_fit` are **forbidden
keys** and `validate_weights` rejects them. Desirability and admissibility are
deliberately separate: a university the student can't get into must not rank highly.
Admissibility lives in `Admission likelihood` (Reach/Match/Safety) and `Warnings`.
This is guardrail #1 of `00_overview.md`, enforced in code.

## Re-tuning

Just re-run `tools/derive_weights.py --student <slug>` after `preferences.json`
changes — it reads the current file, computes fresh, and bumps `weights_id`
automatically. Re-syncing re-scores only the rows you sync; already-baked scores in
`master_list.csv` don't change until re-synced.

## Done when

- The tool ran clean (`validate_weights` passes inside it — 8 exact keys, no
  forbidden keys, sums to 1.00, each ≤ 0.5).
- `python tools/sync_shortlist.py --student <slug> --country <name> --dry-run` prints
  the expected `weights_id`. (`--country` is **required** — one country per pass; see
  `03_discover_longlist.md`.)
