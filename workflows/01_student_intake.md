# Workflow: Stage 1 — Student Intake (→ profile.json)

## Objective

Build a complete, honest picture of **who the student is** — grades, qualifications, English, budget,
and any recognition needs — so later stages can judge fit, cost, and admissibility accurately. Output is
`data/students/<slug>/profile.json`.

## How to start

Run the scaffold first (creates the folder + template JSON):

```powershell
python tools/init_student.py "Aisyah Rahman"
```

Then fill `profile.json` conversationally. Don't interrogate — have a natural conversation and fill fields
as they come up. Any field you genuinely can't get stays `null`/empty; never invent values.

## Conversational checklist (map answers to profile.json)

- **Identity** — `name`, `age`, `gender`, `nationality`, `country_of_residence`. `home_country` defaults
  to **Malaysia** (where they intend to live/work after); confirm it.
- **Current qualification** — `current_program.type` (A-Level / STPM / UEC / IB / Foundation / Matriculation /
  Diploma), institution, expected completion. Add prior schooling to `education_history`.
- **Subjects & grades** — `subjects` as `{subject, grade_or_predicted}`. Set **`grade_status`** to
  `"actual"` if results are out, else `"predicted"`. *This is the single most important input for
  admissibility later — get it right and label it honestly.*
- **English** — `english_proficiency.{test, score, test_date_or_planned}`. If no test yet, record that
  it's planned (it becomes a timeline item). MUET counts but many overseas unis want IELTS/TOEFL.
- **Budget** — `financial.{budget_per_year, total_budget, currency, funding_source, scholarship_dependent}`.
  Default `currency` is **MYR**. Capture **total** budget (full programme), not just per-year — total cost
  is what Stage 4 compares. If they can only proceed with a scholarship, set `scholarship_dependent: true`.
- **Recognition needs** — if the student is aiming at a **regulated profession** (medicine→MMC,
  engineering→BEM/Washington Accord, law→LPQB, accounting→MIA/ACCA, pharmacy, dentistry, architecture→LAM,
  nursing), set `recognition_targets` (e.g. `["MQA","MMC"]`). Leave empty for non-regulated fields.
- **Personal needs** (only if the student raises them) — `needs.{halal_food, prayer_facilities,
  malaysian_community, proximity_to_family}`.

## Interest-discovery branch (undecided student)

If the student **can't name a field/course**, don't force one. Instead fill `interest_discovery`:
`{decided: false, career_goal, subjects_enjoyed, work_styles, values, constraints}`. Capture what they
enjoy, what they're good at, what kind of life/work they want, and any constraints. Then hand off to
Stage 2's **career-backwards** mode, which turns this into candidate fields before discovery.

## Edge cases & rules

- **Predicted vs actual grades** — always label with `grade_status`. Predicted grades make most options a
  Reach/Match until results confirm; say so.
- **Consent & PDPA** — financials and anything sensitive are collected only with consent and kept local
  (`data/students/` is gitignored). Don't push for data the student is uncomfortable sharing.
- **Don't guess** — a `null` is more useful than a fabricated grade or budget. Note open questions in `notes`.

## Done when

`profile.json` has grades (+ `grade_status`), English status, a total budget, and — if relevant —
`recognition_targets`. Then proceed to **Stage 2** (`02_aspirations_intake.md`).
