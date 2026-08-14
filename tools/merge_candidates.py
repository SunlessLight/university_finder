"""
merge_candidates.py — merge per-university candidate fragments into one uni_candidates.json.

Stage 3 fills a country's rows with PARALLEL row-filler subagents (one per university,
see .claude/agents/row-filler.md). Each writes exactly one fragment to
.tmp/<slug>/candidates/<uni-slug>.json. This tool collects them, checks each row is
actually complete, and writes the merged list sync_shortlist.py reads.

It exists because the master list is the client's deliverable and a blank cell reads as
breakage. The gap has to be caught BEFORE the CSV: sync_shortlist.py only ever appends,
and it dedupes by course_key — so a university synced with holes cannot be topped up by
re-running it later, it is simply skipped as a duplicate. Failing here means
re-dispatching the two agents that came back short, not rebuilding the country.

Checks, in the order they fire:
  1. every fragment's `country` matches --country          (one country per pass)
  2. no two fragments claim the same course_key            (duplicate dispatch)
  3. every REQUIRED_CANDIDATE_FIELD present and non-empty  (the completeness gate)
  4. all eight `scores` sub-scores present, numeric, 0-5

Exit 1 lists every (university, problem) pair — the whole point is that one run tells you
exactly which agents to re-dispatch and what each of them missed.

Usage:
    python tools/merge_candidates.py --student <slug> --country "Hong Kong"
    python tools/merge_candidates.py --student <slug> --country "Hong Kong" --dry-run
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import (  # noqa: E402
    OPTIONAL_VALUE_FIELDS,
    REQUIRED_CANDIDATE_FIELDS,
    WEIGHT_KEYS,
    course_key,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent


def is_empty(value):
    """True for a value that counts as 'not filled in'.

    Deliberately NOT falsiness: `meets_english: false` and `entry_margin: 0` are real,
    load-bearing answers. Only None, an empty/whitespace string, and an empty
    list/dict mean nobody filled the field.
    """
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def load_fragments(frag_dir):
    """Read every *.json in frag_dir as (path, candidate). Exits on unreadable JSON."""
    paths = sorted(p for p in frag_dir.glob("*.json"))
    if not paths:
        sys.exit(
            f"ERROR: no candidate fragments in {frag_dir}.\n"
            f"Each row-filler subagent writes one {frag_dir.name}/<uni-slug>.json — "
            f"dispatch them first (workflows/03_discover_longlist.md, step 3)."
        )
    out = []
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            sys.exit(f"ERROR: {path} is not valid JSON ({exc}).")
        # Tolerate an agent that wrapped its single candidate in a list.
        if isinstance(data, list):
            if len(data) != 1:
                sys.exit(
                    f"ERROR: {path} holds {len(data)} candidates. One fragment = one "
                    f"university+course, so re-dispatch that row rather than batching."
                )
            data = data[0]
        if not isinstance(data, dict):
            sys.exit(f"ERROR: {path} must hold one candidate object.")
        out.append((path, data))
    return out


def check_country(fragments, country):
    """[problem] for any fragment whose country isn't the one this pass covers."""
    want = (country or "").strip().lower()
    problems = []
    for path, c in fragments:
        got = str(c.get("country") or "").strip()
        if got.lower() != want:
            problems.append(f"{path.name}: country {got or '(blank)'!r}, expected {country!r}")
    return problems


def check_duplicates(fragments):
    """[problem] for two fragments describing the same university+course.

    sync_shortlist.py would silently drop the second as a duplicate, so a double
    dispatch would quietly cost a row off the longlist.
    """
    seen = {}
    problems = []
    for path, c in fragments:
        key = course_key(c.get("university"), c.get("course"))
        if key in seen:
            problems.append(
                f"{path.name}: same university+course as {seen[key].name} "
                f"({c.get('university', '?')} — {c.get('course', '?')})"
            )
        else:
            seen[key] = path
    return problems


def check_fields(candidate):
    """[missing field] for one candidate, per REQUIRED_CANDIDATE_FIELDS."""
    problems = []
    for field in REQUIRED_CANDIDATE_FIELDS:
        if field not in candidate:
            problems.append(f"{field} (absent)")
        elif field not in OPTIONAL_VALUE_FIELDS and is_empty(candidate[field]):
            problems.append(f"{field} (empty)")
    return problems


def check_scores(candidate):
    """[problem] for the eight 0-5 sub-scores compute_score() consumes."""
    problems = []
    scores = candidate.get("scores")
    if not isinstance(scores, dict):
        return ["scores (missing the 0-5 sub-score object)"]
    for key in WEIGHT_KEYS:
        if key not in scores:
            problems.append(f"scores.{key} (absent)")
            continue
        value = scores[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            problems.append(f"scores.{key} must be a number 0-5, got {value!r}")
        elif not 0 <= value <= 5:
            problems.append(f"scores.{key} is {value}, outside 0-5")
    return problems


def main():
    parser = argparse.ArgumentParser(
        description="Merge + validate per-university candidate fragments for one country."
    )
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--country", required=True, help="The ONE country this pass covers.")
    parser.add_argument(
        "--fragments",
        help="Fragment directory (default .tmp/<slug>/candidates/).",
    )
    parser.add_argument(
        "--out",
        help="Merged output path (default .tmp/<slug>/uni_candidates.json).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate only; write nothing.")
    args = parser.parse_args()

    slug = args.student
    frag_dir = Path(args.fragments) if args.fragments else REPO_ROOT / ".tmp" / slug / "candidates"
    if not frag_dir.is_absolute():
        frag_dir = REPO_ROOT / frag_dir
    out_path = Path(args.out) if args.out else REPO_ROOT / ".tmp" / slug / "uni_candidates.json"
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path

    if not frag_dir.exists():
        sys.exit(f"ERROR: {frag_dir} not found. Row-filler subagents write their fragments there.")

    fragments = load_fragments(frag_dir)
    print(f"student: {slug} | country: {args.country} | {len(fragments)} fragment(s) in {frag_dir}")

    failures = check_country(fragments, args.country) + check_duplicates(fragments)

    for path, c in fragments:
        problems = check_fields(c) + check_scores(c)
        label = f"{c.get('university') or path.stem} — {c.get('course') or '?'}"
        if problems:
            failures.append(f"{label}: {'; '.join(problems)}")
        else:
            print(f"  ok   {label}")

    if failures:
        print(f"\nFAIL — {len(failures)} problem(s); nothing merged:")
        for line in failures:
            print(f"  ! {line}")
        print(
            "\nRe-dispatch only the row-filler(s) named above with the missing fields.\n"
            "A fact that genuinely does not exist takes a sentinel (SENTINEL_VALUES in "
            "tools/shortlist_schema.py), never a guess."
        )
        sys.exit(1)

    candidates = [c for _, c in fragments]
    if args.dry_run:
        print(f"\n(dry run — {len(candidates)} candidate(s) would be written to {out_path})")
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(candidates, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {len(candidates)} candidate(s) to {out_path}")
    print(f"Next: python tools/sync_shortlist.py --student {slug} --country \"{args.country}\"")


if __name__ == "__main__":
    main()
