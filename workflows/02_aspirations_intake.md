# Workflow: Stage 2 — Aspirations Intake (→ preferences.json)

## Objective

Capture **what the student wants** — destinations, field/course, budget ceiling, priorities, and
dealbreakers — so discovery is targeted and scoring reflects what actually matters to *this* student.
Output is `data/students/<slug>/preferences.json`.

## Conversational checklist (map answers to preferences.json)

- **Target countries** — `target_countries`, a subset of the five supported sets:
  `["UK","Australia","USA","Singapore/Malaysia","China"]`. Don't accept destinations outside these in v1.
- **Field & course** — `fields_of_interest` and `specific_courses`. If they can name exact courses, great.
  **If `specific_courses` stays empty, run interest-discovery (below) before Stage 3.**
- **Level & intake** — `degree_level` (undergrad / foundation / …) and `intake` (e.g. `"2027 Sept"`). The
  intake drives which deadlines and cycle-year facts are relevant.
- **Budget ceiling** — `budget_ceiling_per_year` **and** `total_budget_ceiling`, `currency` (default MYR),
  and `scholarship_required`. These gate affordability and feed `total_cost_fit` scoring.
- **Priorities** — `priorities`, an **ordered** list (e.g. `["cost","employability","recognition",
  "ranking","location"]`). This tells you which sub-scores to weight most heavily when you judge candidates
  in Stage 3. **`priorities` is the direct input to the student's `weights.json`** (via the
  `scoring-weights` skill) — the **ordering matters**, so capture it faithfully rather than as a rough set.
- **Migration intent** — `intent_to_migrate` (bool) and `post_study_work_importance`. If they want to work
  abroad after, post-study-work rights (UK Graduate Route / AUS 485 / US OPT) become decision-critical.
- **Ranking** — `ranking_importance`, `min_subject_rank_pref`. Steer toward **subject** ranking, not overall
  vanity rank.
- **Dealbreakers & location** — `deal_breakers` (hard no's), `location_prefs` (city vs rural, climate,
  near family). Note anything that should auto-reject options in Stage 4.

## Interest-discovery (career-backwards) mode

When `specific_courses` is empty (or `profile.interest_discovery.decided == false`):

1. Start from `interest_discovery`: career goal, subjects enjoyed, work styles, values, constraints.
2. Work **backwards**: career goal → degree families that lead there → specific course types.
   (e.g. "wants to build apps, enjoys maths, dislikes lab work" → Computer Science / Software Engineering /
   Data Science, *not* Electrical Engineering.)
3. Propose 2-4 candidate fields with a one-line rationale each, and **confirm with the student** before
   committing them to `fields_of_interest`. Only then move to discovery.

Never silently pick a field for an undecided student — surface options and let them choose.

## Edge cases & rules

- **Too many countries** — if they pick all five, gently suggest prioritising 2-3 so research stays deep
  rather than shallow. Record the rest in `notes`.
- **Scholarship-dependent + expensive destinations** — flag the tension now (e.g. USA private universities
  vs a tight budget) so Stage 3 weights cost and scholarships heavily.
- **Constrain to supported destinations** — if they want somewhere unsupported (e.g. Canada, Germany), note
  it in `notes` as future scope; don't run discovery for it in v1.

## Done when

`preferences.json` has target countries, a confirmed field (or course list), intake, a total budget ceiling,
and an ordered priorities list. Then proceed to **Stage 3** (`03_discover_longlist.md`).
