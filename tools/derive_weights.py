"""
derive_weights.py — mechanically derive data/students/<slug>/weights.json.

Weights used to be an agent judgment call (the 'scoring-weights' skill): read the
student's 8-way priority ranking, apply half a dozen qualitative modifiers (regulated
profession, contradictory location, budget-null interpretation, notes/deal-breakers
overriding structured fields...), write a rationale. That judgment step had a real
error rate, and per Evan (2026-09-17): weights aren't what students/parents look at —
the raw research is. So the derivation is now a pure function of preferences.json,
with exactly ONE deterministic override, and everything else that used to adjust a
weight instead becomes a Warnings-column flag in feasibility_flags()
(tools/shortlist_schema.py) — surfaced next to the score, never folded into it.

The formula:
    1. Take preferences.priorities — the student's full 8-way ranking (must name every
       WEIGHT_KEYS token exactly once; this only works for the current form's complete
       ranking, not a legacy 3-priority list — the tool refuses rather than guessing).
    2. Map rank 1..8 to a weight linearly from 0.20 down to 0.05 (evenly spaced, sums
       to 1.00 by construction: 8 * (0.20+0.05)/2 = 1.00).
    3. The ONE override: if preferences.scholarship_required is true, move
       scholarship_opportunity to rank 1 (pop + insert-at-front), shifting everything
       between its old and new position down by one rank. This is a hard financial
       gate, not a preference — a student can rank scholarship low on "what I care
       about" while still being unable to attend anything without one.
    4. course_match keeps a raised floor (0.08): "is this even the right course" is
       never allowed to fall to the bare bottom-rank value, even if the student ranked
       course quality last. The shortfall is taken from whichever key currently holds
       the largest weight.
    5. Round to 4dp and nudge the largest weight by any leftover residual so the sum
       is exactly 1.0 (validate_weights()'s tolerance is 1e-6).

Everything else the old skill did by judgment is gone:
  - regulated-profession recognition boost -> dropped. recognition_fit gets whatever
    the plain priority rank gives it; the actual gate is now the "Recognition/
    accreditation risk" Warnings flag (checks recognition_fit against
    profile.recognition_targets regardless of weight).
  - contradictory Urban+Rural location -> dropped as a weight adjustment. Now the
    "Location preference contradictory" Warnings flag instead.
  - budget-null interpretation, notes/deal-breakers overriding structured fields,
    "distrust a flat slider spread", ranking_importance scale-reading -> all dropped.
    ranking_importance is no longer read by this tool at all; the full 8-way
    `priorities` ranking supersedes it.

Usage:
    python tools/derive_weights.py --student <slug>
    python tools/derive_weights.py --student <slug> --dry-run
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import WEIGHT_KEYS, validate_weights  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# Priority token (preferences.priorities, PRIORITY_NORMALIZE in ingest_form_csv.py) ->
# weight key (WEIGHT_KEYS in shortlist_schema.py). 1:1, per the scoring-weights skill.
PRIORITY_TOKEN_TO_WEIGHT_KEY = {
    "ranking": "subject_reputation",
    "scholarship": "scholarship_opportunity",
    "cost": "total_cost_fit",
    "recognition": "recognition_fit",
    "employability": "post_study_work_fit",
    "location": "location_pref_fit",
    "hands-on experience": "experiential_fit",
    "course_quality": "course_match",
}

BASE_TOP = 0.20
BASE_BOTTOM = 0.05
COURSE_MATCH_FLOOR = 0.08


def rank_weight(rank, n=len(WEIGHT_KEYS), top=BASE_TOP, bottom=BASE_BOTTOM):
    """Linear weight for a 1-based rank out of n, from `top` (rank 1) to `bottom` (rank n)."""
    step = (top - bottom) / (n - 1)
    return top - step * (rank - 1)


def derive(preferences):
    """Return (weights_dict, rationale_str) from a preferences.json dict.

    Raises ValueError with a clear message if `priorities` isn't a complete,
    recognizable 8-way ranking — that case still needs a human, not a guess.
    """
    priorities = preferences.get("priorities")
    if not isinstance(priorities, list) or len(priorities) != len(WEIGHT_KEYS):
        raise ValueError(
            f"preferences.priorities must be a complete {len(WEIGHT_KEYS)}-way ranking "
            f"(got {priorities!r}). A partial/legacy priority list can't be derived "
            f"mechanically — derive weights.json by hand for this student instead."
        )

    unknown = [p for p in priorities if p not in PRIORITY_TOKEN_TO_WEIGHT_KEY]
    if unknown:
        raise ValueError(
            f"unrecognized priority token(s): {unknown!r}. "
            f"Known tokens: {sorted(PRIORITY_TOKEN_TO_WEIGHT_KEY)}."
        )

    order = [PRIORITY_TOKEN_TO_WEIGHT_KEY[p] for p in priorities]
    if len(set(order)) != len(WEIGHT_KEYS):
        raise ValueError(f"priorities list has a duplicate weight key after mapping: {order!r}.")

    scholarship_forced = False
    old_rank = None
    if preferences.get("scholarship_required") is True and order[0] != "scholarship_opportunity":
        old_rank = order.index("scholarship_opportunity") + 1
        order.remove("scholarship_opportunity")
        order.insert(0, "scholarship_opportunity")
        scholarship_forced = True

    raw = {key: rank_weight(i + 1) for i, key in enumerate(order)}

    course_match_floored = False
    donor = None
    pre_floor_value = raw["course_match"]
    if pre_floor_value < COURSE_MATCH_FLOOR:
        deficit = COURSE_MATCH_FLOOR - pre_floor_value
        donor = max((k for k in raw if k != "course_match"), key=lambda k: raw[k])
        raw[donor] -= deficit
        raw["course_match"] = COURSE_MATCH_FLOOR
        course_match_floored = True

    rounded = {k: round(v, 4) for k, v in raw.items()}
    residual = round(1.0 - sum(rounded.values()), 6)
    if residual:
        top_key = max(rounded, key=lambda k: rounded[k])
        rounded[top_key] = round(rounded[top_key] + residual, 6)

    rationale = (
        f"Mechanically derived by tools/derive_weights.py from preferences.priorities "
        f"({', '.join(priorities)}). Formula: linear {BASE_TOP} (rank 1) -> {BASE_BOTTOM} "
        f"(rank {len(WEIGHT_KEYS)}), evenly spaced, sums to 1.00. "
    )
    if scholarship_forced:
        rationale += (
            f"scholarship_required=true moved scholarship_opportunity from rank {old_rank} "
            f"to rank 1 (hard financial gate, overrides stated priority order). "
        )
    if course_match_floored:
        rationale += (
            f"course_match floored at {COURSE_MATCH_FLOOR} (raised from {pre_floor_value:.4f}); "
            f"{COURSE_MATCH_FLOOR - pre_floor_value:.4f} taken from {donor}. "
        )
    rationale += (
        "No other modifiers applied — regulated-profession recognition risk and "
        "contradictory Urban+Rural location preferences are surfaced as Warnings-column "
        "flags instead (feasibility_flags() in shortlist_schema.py), not folded into the weights."
    )

    return validate_weights(rounded), rationale


def next_weights_id(slug, existing_path):
    if not existing_path.exists():
        return f"{slug}-v1"
    try:
        meta = json.loads(existing_path.read_text(encoding="utf-8"))
        old_id = meta.get("weights_id", "")
    except json.JSONDecodeError:
        old_id = ""
    m = re.match(rf"^{re.escape(slug)}-v(\d+)$", old_id)
    if m:
        return f"{slug}-v{int(m.group(1)) + 1}"
    return f"{slug}-v1"


def main():
    parser = argparse.ArgumentParser(description="Mechanically derive a student's weights.json.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--dry-run", action="store_true", help="Compute and print but do not write.")
    args = parser.parse_args()

    slug = args.student
    student_dir = STUDENTS_DIR / slug
    if not student_dir.exists():
        sys.exit(f"ERROR: {student_dir} not found. Run init_student.py first.")

    prefs_path = student_dir / "preferences.json"
    if not prefs_path.exists():
        sys.exit(f"ERROR: {prefs_path} not found.")
    preferences = json.loads(prefs_path.read_text(encoding="utf-8"))

    try:
        weights, rationale = derive(preferences)
    except ValueError as exc:
        sys.exit(f"ERROR: {exc}")

    weights_path = student_dir / "weights.json"

    # Idempotency guard (learned 2026-09-21, shean-v3 incident): if preferences.json hasn't
    # changed since the last derivation, the formula reproduces IDENTICAL weight values —
    # bumping the id anyway would desync weights.json from whatever weights_id is already
    # baked into score_log.jsonl/master_list.csv, with nothing to show for it. Only bump
    # when the numbers actually differ.
    if weights_path.exists():
        try:
            existing = json.loads(weights_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
        if existing.get("weights") == weights:
            print(
                f"No change: preferences.json produces the same weights as the existing "
                f"{existing.get('weights_id', '(unknown)')}. Nothing written."
            )
            return

    weights_id = next_weights_id(slug, weights_path)

    doc = {
        "weights_id": weights_id,
        "student": slug,
        "derived_from": f"preferences.json (mechanical derivation, tools/derive_weights.py, {date.today()})",
        "derived_on": str(date.today()),
        "rationale": rationale,
        "weights": weights,
    }

    print(f"weights_id: {weights_id}")
    for key in WEIGHT_KEYS:
        print(f"  {key}: {weights[key]}")
    print(f"rationale: {rationale}")

    if args.dry_run:
        print("[dry run] nothing written.")
        return

    weights_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {weights_path}")


if __name__ == "__main__":
    main()
