"""
match_finalists.py — resolve shorthand university/course names typed by the student
into canonical master_list.csv rows.

Lets /report accept "UCL" or "UCL|mechanical engineering" instead of requiring the
exact CSV strings. Deterministic matching only (shortlist_schema's canonical_uni alias
table, then substring containment) — never guesses when a query is genuinely ambiguous
or absent; it reports the ambiguity/miss and leaves the pick to the student, same as
report-writer refuses to guess a finalist it wasn't given cleanly.

Read-only: never edits master_list.csv. Promoting a resolved pick to Shortlist stays a
separate CSV edit in the /report pre-flight, same as it is for a table-picked finalist.

Usage:
    # one finalist, university only (auto-resolves if it has a single course on the list)
    python tools/match_finalists.py --student <slug> --query "UCL"

    # one finalist, university + course (needed when a university has 2+ courses listed)
    python tools/match_finalists.py --student <slug> --query "UCL|mechanical engineering"

    # multiple finalists in one call
    python tools/match_finalists.py --student <slug> --query "UCL|mechanical engineering" --query "Imperial"

Prints a JSON array, one object per --query, each with a "status":
    resolved            -> "university" + "course" + "list_status" are the match
    ambiguous_course     -> "university" resolved; "options" lists its courses
    ambiguous_university -> more than one distinct university matched; "options" lists them
    not_found            -> nothing matched
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import canonical_uni  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# Below this, a substring match is too likely to hit unrelated rows by accident
# (e.g. a 2-char hint matching half the list) — require the alias/canonical match
# instead of falling back to containment.
MIN_SUBSTRING_HINT_LEN = 3


def load_rows(csv_path):
    with csv_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def normalize(text):
    """Lowercase, punctuation-stripped comparison form for substring matching."""
    text = re.sub(r"[^a-z0-9 ]+", " ", (text or "").strip().lower())
    return re.sub(r"\s+", " ", text).strip()


def match_universities(hint, rows):
    """Distinct 'University' values (as written in the CSV) that `hint` could mean."""
    hint_canon = canonical_uni(hint)
    hint_norm = normalize(hint)
    matched = set()
    for r in rows:
        uni = r.get("University") or ""
        if not uni:
            continue
        if canonical_uni(uni) == hint_canon:
            matched.add(uni)
            continue
        if len(hint_norm) >= MIN_SUBSTRING_HINT_LEN:
            uni_norm = normalize(uni)
            if hint_norm in uni_norm or uni_norm in hint_norm:
                matched.add(uni)
    return sorted(matched)


def match_courses(hint, courses):
    """Courses (as written in the CSV) whose normalized text contains `hint`."""
    hint_norm = normalize(hint)
    if len(hint_norm) < MIN_SUBSTRING_HINT_LEN:
        return []
    return [c for c in courses if hint_norm in normalize(c)]


def resolve_query(query, rows):
    """Resolve one 'University' or 'University|Course' query against the student's rows."""
    if "|" in query:
        uni_hint, course_hint = (p.strip() for p in query.split("|", 1))
    else:
        uni_hint, course_hint = query.strip(), ""

    universities = match_universities(uni_hint, rows)
    if not universities:
        return {"query": query, "status": "not_found"}
    if len(universities) > 1:
        return {"query": query, "status": "ambiguous_university", "options": universities}

    university = universities[0]
    uni_rows = [r for r in rows if (r.get("University") or "") == university]
    courses = [r.get("Course") or "" for r in uni_rows]

    if course_hint:
        matched_courses = match_courses(course_hint, courses)
    elif len(uni_rows) == 1:
        matched_courses = courses
    else:
        matched_courses = []  # multiple courses on the list, no hint to disambiguate

    if not matched_courses:
        return {
            "query": query, "status": "ambiguous_course",
            "university": university, "options": sorted(set(courses)),
        }
    if len(set(matched_courses)) > 1:
        return {
            "query": query, "status": "ambiguous_course",
            "university": university, "options": sorted(set(matched_courses)),
        }

    course = matched_courses[0]
    row = next(r for r in uni_rows if (r.get("Course") or "") == course)
    return {
        "query": query, "status": "resolved",
        "university": university, "course": course,
        "list_status": row.get("List status") or "",
    }


def main():
    parser = argparse.ArgumentParser(description="Resolve shorthand university/course names to master_list.csv rows.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--query", action="append", required=True,
                        help="'University' or 'University|Course'. Repeatable, one per finalist.")
    args = parser.parse_args()

    csv_path = STUDENTS_DIR / args.student / "master_list.csv"
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found. Run discovery (Stage 3) first.")

    rows = load_rows(csv_path)
    results = [resolve_query(q, rows) for q in args.query]
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
