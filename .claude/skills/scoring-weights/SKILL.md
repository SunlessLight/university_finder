---
name: scoring-weights
description: >
  Use when deriving, tuning, or reviewing a student's desirability scoring weights —
  i.e. creating data/students/<slug>/weights.json before running sync_shortlist.py
  (Stage 3 / workflows/03_discover_longlist.md), or re-tuning after a student's
  priorities change. ALSO use if you are tempted to edit weights, SCORE_WEIGHTS, or any
  weighting inside tools/shortlist_schema.py — don't: that file is shared source, weights
  are per-student and live in the data bank, and hand-editing it collides with concurrent
  sessions. Covers the priorities->weight-key mapping, the modifiers, and validation.
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
| `course_quality` *(non-form students only)* | `course_match` |

## Procedure — judgement, not arithmetic

The form gives only **3** ranked priorities but there are **8** keys, so **most of the weight
comes from the modifiers, not the ranking.** Do not build a formula and trust it.

1. **The 3 named priorities anchor the top.** But **unlisted ≠ zero** — every key keeps a
   floor, and `course_match` keeps a *raised* floor: "is this even the right course?" is
   never irrelevant.
2. **Apply the modifiers**, and name each one you used in `rationale`:
   - `scholarship_required: true` → `scholarship_opportunity` to the top band **regardless of
     priority rank** (it's a hard gate).
   - `total_budget_ceiling: null` → `total_cost_fit` at floor.
   - `intent_to_migrate: true`, or work-abroad Yes/High → `post_study_work_fit` up.
   - Regulated profession (Engineering / Medicine / Law / Accounting / Pharmacy) →
     `recognition_fit` above floor.
   - Contradictory `location_prefs` (Urban *and* Rural both ticked) → `location_pref_fit`
     near floor: they're telling you not to filter on setting.
3. **Read `notes` and `deal_breakers` — they override the structured fields.** The structured
   fields are a lossy compression of intent; the notes are the intent. (Zafri's accreditation
   deal-breaker beats his `ranking_importance: 4`.)
4. **`priorities` order wins over `ranking_importance`** on conflict. `ranking_importance`
   only modulates *within* the band the priority order already assigned.
5. **Sum to exactly 1.00; every weight ≤ 0.5.** If `validate_weights` rejects it, **fix the
   derivation — never fudge a key to make the sum work.**

### Never weight admissibility

`entry_fit`, `admission_fit`, `admissibility`, `entry_margin_fit` are **forbidden keys** and
`validate_weights` rejects them. Desirability and admissibility are deliberately separate: a
university the student can't get into must not rank highly. Admissibility lives in
`Admission likelihood` (Reach/Match/Safety) and `Warnings`. This is guardrail #1 of
`00_overview.md`, and it is now enforced in code.

### Prose fields (toru / law-jia-herng predate the form)

`ranking_importance` may be `"5"`, `"medium"`, or a whole sentence. Numeric → int;
`low`/`medium`/`high` → 2/3/4; prose → judge it, and **quote the phrase you judged from** in
the `rationale`.

## Worked example — Lai Zheng Yi (real, verified)

His inputs: Biomedical Engineering; priorities `ranking > ...`; `ranking_importance: 5`;
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
- `python tools/sync_shortlist.py --student <slug> --dry-run` prints the expected `weights_id`.
