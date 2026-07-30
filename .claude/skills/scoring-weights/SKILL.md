---
name: scoring-weights
description: >
  Use when deriving, tuning, or reviewing a student's desirability scoring weights —
  i.e. creating data/students/<slug>/weights.json before running sync_shortlist.py
  (Stage 3 / workflows/03_discover_longlist.md), or re-tuning after a student's
  priorities change. ALSO use if you are tempted to edit weights, SCORE_WEIGHTS, or any
  weighting inside tools/shortlist_schema.py — don't: that file is shared source, weights
  are per-student and live in the data bank, and hand-editing it collides with concurrent
  sessions.
---

# Deriving per-student scoring weights

The desirability score is a weighted sum of eight 0-5 sub-scores. **The weights are that
student's values, expressed as numbers.** They are per-student data — never shared source.

## Where weights live (and why it matters)

`data/students/<slug>/weights.json`. **Nothing student-specific goes in
`tools/shortlist_schema.py`.** That file is shared and git-tracked: a weight hardcoded there
is a weight two concurrent sessions overwrite for each other, silently, with no error and
no trace in the CSV. That is the exact bug this file structure retired. `compute_score()`
takes weights as a required argument and has no default — there is no fallback to fall into.

`sync_shortlist.py` **hard-errors** without a valid `weights.json`. That's intended: scoring
under weights nobody chose produces numbers indistinguishable from chosen ones.

## The file

```json
{
  "weights_id": "lai-zheng-yi-v1",
  "student": "lai-zheng-yi",
  "derived_from": "preferences.json / form response (2026-07-13)",
  "derived_on": "2026-07-15",
  "rationale": "Ranking is his #1 priority (importance 5/5). Scholarship ties it at the top despite not being in his 3 priorities, because scholarship_required=true is a hard gate. ...",
  "weights": { "subject_reputation": 0.20, "scholarship_opportunity": 0.20, "course_match": 0.15,
               "post_study_work_fit": 0.13, "total_cost_fit": 0.10, "recognition_fit": 0.10,
               "location_pref_fit": 0.07, "experiential_fit": 0.05 }
}
```

- `weights_id` — `<slug>-v<n>`. **Bump on re-tune; never edit in place** — old `score_log.jsonl`
  lines carry the old id and must stay interpretable.
- `student` — cross-checked against `--student`; catches a copy-pasted sibling file.
- `rationale` — **required** (`load_weights` rejects a blank one). It is the only thing that
  makes a weight set reviewable. Name every non-floor weight and every modifier you applied.

## Mapping: priority token -> weight key

The form's priority dropdown normalizes to these tokens (`PRIORITY_NORMALIZE` in
`ingest_form_csv.py`), which map 1:1 onto weight keys:

| priority token | weight key |
|---|---|
| `ranking` | `subject_reputation` |
| `scholarship` | `scholarship_opportunity` |
| `cost` | `total_cost_fit` |
| `recognition` | `recognition_fit` |
| `employability` | `post_study_work_fit` |
| `location` | `location_pref_fit` |
| `hands-on experience` | `experiential_fit` |
| `course_quality` | `course_match` |

The current form's **eight 1-8 priority sliders** produce a full 8-way ranking (not just 3), including a
**Course Ranking** slider → `course_quality` → `course_match`. So `course_quality` is no longer
non-form-only — form students now supply it directly.

## Procedure — judgement, not arithmetic

`preferences.priorities` now arrives as a **complete 8-way ordering**, one entry per weight key, derived
from the eight 1-8 sliders (highest first; ties broken by the form's column order — see
`01_intake.md`). That is far more signal than the old 3-priority form gave, and it changes the job: you
are **shaping a full ranking**, not inventing seven keys from three. Still do not build a formula and
trust it — the ordering is only as good as the student's slider discipline, and the gates below
outrank it.

1. **The ordering anchors every key, not just the top.** Rank 1 sits in the top band, rank 8 at the
   floor, the rest spread between — but **rank 8 ≠ zero**: every key keeps a floor, and `course_match`
   keeps a *raised* floor ("is this even the right course?" is never irrelevant).
2. **Distrust flat and near-flat slider sets.** A student who drags everything to 7-8, or leaves them
   all at the default, has ranked nothing — the tie-break then hands you the *form's column order*
   (Cost → Scholarship → University Ranking → Course Ranking → Employability → Recognition → Location →
   Hands-On), which is arbitrary, not a preference. Check the spread before you lean on the order; if
   it's flat, say so in `rationale` and derive from the modifiers, `notes` and `deal_breakers` instead.
3. **Apply the modifiers**, and name each one you used in `rationale`:
   - `scholarship_required: true` → `scholarship_opportunity` to the top band **regardless of
     priority rank** (it's a hard gate).
   - **`total_budget_ceiling: null` no longer means "cost doesn't matter."** Under the four-band budget
     dropdown, `null` is produced by *two different answers* — read `profile.financial.notes`, which
     carries the verbatim label, before deciding:
     - `Above RM 1,000,000` → a genuine no-ceiling student. Cost is a weak differentiator here;
       `total_cost_fit` low unless the Cost slider says otherwise.
     - `Not sure - no fixed budget` → the ceiling is *unknown*, not absent. **Let the Cost slider
       decide**: a student who ranked Cost near the top means it, ceiling or no ceiling.
     - Only floor `total_cost_fit` when there's no ceiling **and** Cost sits low in the ordering.
       A real band (`500000` / `1000000`) makes cost genuine — weight it accordingly.
   - `intent_to_migrate: true`, or work-abroad Yes/High → `post_study_work_fit` up.
   - Regulated profession (Engineering / Medicine / Law / Accounting / Pharmacy) →
     `recognition_fit` above floor.
   - Contradictory `location_prefs` (Urban *and* Rural both ticked) → `location_pref_fit`
     near floor: they're telling you not to filter on setting.
4. **Read `notes` and `deal_breakers` — they override the structured fields.** The structured
   fields are a lossy compression of intent; the notes are the intent. (Zafri's accreditation
   deal-breaker beats his `ranking_importance: 4`.)
5. **`priorities` order wins over `ranking_importance`** on conflict. `ranking_importance`
   only modulates *within* the band the priority order already assigned.
6. **Sum to exactly 1.00; every weight ≤ 0.5.** If `validate_weights` rejects it, **fix the
   derivation — never fudge a key to make the sum work.**

### Never weight admissibility

`entry_fit`, `admission_fit`, `admissibility`, `entry_margin_fit` are **forbidden keys** and
`validate_weights` rejects them. Desirability and admissibility are deliberately separate: a
university the student can't get into must not rank highly. Admissibility lives in
`Admission likelihood` (Reach/Match/Safety) and `Warnings`. This is guardrail #1 of
`00_overview.md`, and it is now enforced in code.

### Reading `ranking_importance` — check the scale before you read the number

`ranking_importance` steers `subject_reputation`, and **the same integer means different things
depending on which form the student filled.** Establish the scale first; a `5` is near-top on one and
mid-pack on the other.

| Source | Scale | How to read it |
|---|---|---|
| Current form (2026-07-29+) — the **[University Ranking]** slider | **1-8** | 7-8 = top band, 4-6 = middle, 1-3 = floor-ish. `derived_from` will name a recent form response. |
| A dedicated *"how much does your subject's strength matter"* question, if the form ever gains one | **1-5** | The tool prefers this over the slider when present. |
| Pre-slider form students | **1-7** | Same shape as 1-8; scale it before comparing. |
| Prose students (`toru`, `law-jia-herng` — predate the form) | none | `"medium"` / a whole sentence. `low`/`medium`/`high` → 2/3/4 on a 1-5 reading; for a sentence, judge it and **quote the phrase you judged from** in the `rationale`. |

When the scale is ambiguous, **say which one you assumed in `rationale`** — it is the difference
between a top-band `subject_reputation` and a middling one.

## Worked example — Lai Zheng Yi (real, verified)

His inputs: Biomedical Engineering; priorities `ranking > ...`; `ranking_importance: 5` **on the
pre-slider scale** (top band — not a mid-pack 5 out of 8; see the scale table above);
`scholarship_required: **true**`; ~RM500k total budget; `intent_to_migrate: true`, work
abroad Yes; `location_prefs` = Urban **+** Rural **+** near family.

| key | weight | why |
|---|---|---|
| `subject_reputation` | 0.20 | #1 priority, importance 5/5 |
| `scholarship_opportunity` | 0.20 | **not in his 3 priorities at all** — `scholarship_required: true` is a hard gate, so it *ties for top* |
| `course_match` | 0.15 | never listed it; still a raised floor |
| `post_study_work_fit` | 0.13 | `intent_to_migrate` + work abroad: Yes |
| `total_cost_fit` | 0.10 | a real ~RM500k ceiling makes cost genuine |
| `recognition_fit` | 0.10 | Biomedical Eng is regulated (BEM/EAC, Washington Accord) |
| `location_pref_fit` | 0.07 | Urban *and* Rural *and* near-family all ticked → don't over-filter |
| `experiential_fit` | 0.05 | not emphasised |

**This is the point of the example:** his highest weight is tied by a key he never named. The
modifiers did the heavy lifting. (This set reproduces all 11 of his stored scores exactly.)

## Re-tuning

Never mutate in place: bump `weights_id` (`-v2`), rewrite the file, keep the old id readable
in `score_log.jsonl`. Re-syncing re-scores only the rows you sync; already-baked scores in
`master_list.csv` don't change until re-synced.

## Done when

- `validate_weights` accepts it: 8 exact keys, no forbidden keys, sums to 1.00, each ≤ 0.5.
- `rationale` names each non-floor weight and every modifier applied.
- `tools/shortlist_schema.py` is **untouched**.
- `python tools/sync_shortlist.py --student <slug> --country <name> --dry-run` prints the expected
  `weights_id`. (`--country` is **required** — one country per pass; see `03_discover_longlist.md`.)
