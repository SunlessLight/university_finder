"""
progress_dashboard.py — roster-wide progress report across every student in data/students/.

There is no single place that shows "who's stuck where" across the roster. Each student's
status.md answers that for one student, but status.md is prose written at the end of a
session — workflows/resume.md itself treats it as fallible ("a stale note... lies with
confidence... if they conflict, the files win"). This tool never reads status.md. It derives
each student's stage the same way resume.md tells a human to reconcile one: from
profile.json/preferences.json presence, master_list.csv's List status counts, the reports/
folder vs Finalist rows, and recommendation.md/calendar.md — the same signals, run across
everyone instead of one slug at a time.

Usage:
    python tools/progress_dashboard.py
"""

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import INFO_SOURCE_UNVERIFIED, LIST_STATUSES  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# rank = how far along overall, used both to bucket the summary counts and to sort the table
# furthest-along first.
STAGE_LABELS = {
    0: "Stage 1 not started",
    1: "Stage 1 needs review",
    2: "Stage 3 not started",
    3: "Stage 3 in progress",
    4: "Stage 3 finalists picked",
    5: "Stage 4 in progress",
    6: "Stage 4 done",
    7: "Stage 5 done",
}


def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def load_csv_rows(path):
    if not path.exists():
        return None
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def stage1_status(profile, preferences):
    """('not started' | 'needs review' | 'done', flags-if-needs-review)."""
    if profile is None or preferences is None:
        return "not started", None
    flags = [k for k in ("_needs_review", "_intake_raw") if profile.get(k)]
    if flags:
        return "needs review", flags
    return "done", None


def stage3_detail(rows, preferences):
    """Counts by List status, countries covered vs in-scope, unverified-row count."""
    counts = {status: 0 for status in LIST_STATUSES}
    countries = set()
    unverified = 0
    for row in rows:
        status = (row.get("List status") or "").strip()
        if status in counts:
            counts[status] += 1
        if status != "Rejected":
            country = (row.get("Country") or "").strip()
            if country:
                countries.add(country)
            if (row.get("Info source") or "").strip() == INFO_SOURCE_UNVERIFIED:
                unverified += 1
    target_countries = set((preferences or {}).get("target_countries") or [])
    missing_countries = sorted(c for c in target_countries if c not in countries)
    return {
        "counts": counts,
        "countries": countries,
        "missing_countries": missing_countries,
        "unverified": unverified,
        "total_rows": len(rows),
    }


def stage4_detail(reports_dir, finalist_count):
    """(reports_done, finalist_count) — 'done' once every Finalist row has a report."""
    reports_done = len(list(reports_dir.glob("*.md"))) if reports_dir.exists() else 0
    return reports_done, finalist_count


def stage5_status(student_dir):
    has_rec = (student_dir / "recommendation.md").exists()
    has_cal = (student_dir / "calendar.md").exists()
    if has_rec and has_cal:
        return "done"
    if has_rec or has_cal:
        return "in progress"
    return "not started"


def summarize_student(student_dir):
    profile = load_json(student_dir / "profile.json")
    preferences = load_json(student_dir / "preferences.json")
    s1, s1_flags = stage1_status(profile, preferences)

    rows = load_csv_rows(student_dir / "master_list.csv")
    s3 = stage3_detail(rows, preferences) if rows is not None else None
    finalist_count = s3["counts"].get("Finalist", 0) if s3 else 0

    reports_done, reports_total = stage4_detail(student_dir / "reports", finalist_count)
    s5 = stage5_status(student_dir)

    apply_prep_dir = student_dir / "application_prep"
    has_apply_prep = apply_prep_dir.exists() and any(apply_prep_dir.glob("*.md"))

    if s1 == "not started":
        rank = 0
    elif s1 == "needs review":
        rank = 1
    elif rows is None:
        rank = 2
    elif s5 == "done":
        rank = 7
    elif reports_total and reports_done >= reports_total:
        rank = 6
    elif reports_done or reports_total:
        rank = 5
    elif finalist_count:
        rank = 4
    else:
        rank = 3

    overall = STAGE_LABELS[rank]
    if rank == 1:
        overall = f"Stage 1 needs review ({', '.join(s1_flags)})"
    elif rank == 5:
        overall = f"Stage 4 in progress ({reports_done}/{reports_total} reports)"

    parts = []
    if s3:
        c = s3["counts"]
        parts.append(
            f"{s3['total_rows']} rows (L{c.get('Longlist', 0)}/S{c.get('Shortlist', 0)}/"
            f"F{c.get('Finalist', 0)}/R{c.get('Rejected', 0)})"
        )
        n_countries = len(s3["countries"])
        parts.append(f"{n_countries} {'country' if n_countries == 1 else 'countries'}")
        if s3["missing_countries"]:
            parts.append(f"missing: {', '.join(s3['missing_countries'])}")
        if s3["unverified"]:
            parts.append(f"{s3['unverified']} unverified")
    if finalist_count or reports_done:
        parts.append(f"{reports_done}/{finalist_count} reports")
    if has_apply_prep:
        parts.append("apply-prep started")

    return {
        "slug": student_dir.name,
        "overall": overall,
        "rank": rank,
        "detail": ", ".join(parts) if parts else "no master list yet",
    }


def main():
    if not STUDENTS_DIR.exists():
        sys.exit(f"ERROR: {STUDENTS_DIR} not found.")

    students = [d for d in sorted(STUDENTS_DIR.iterdir()) if d.is_dir()]
    if not students:
        sys.exit(f"No student folders found under {STUDENTS_DIR}.")

    summaries = [summarize_student(d) for d in students]

    print(f"Progress across {len(summaries)} students\n")
    for rank in sorted(STAGE_LABELS):
        n = sum(1 for s in summaries if s["rank"] == rank)
        if n:
            print(f"  {STAGE_LABELS[rank]:<28} {n}")
    print()

    name_width = max(len(s["slug"]) for s in summaries)
    stage_width = max(len(s["overall"]) for s in summaries)
    for s in sorted(summaries, key=lambda s: (-s["rank"], s["slug"])):
        print(f"{s['slug']:<{name_width}}  {s['overall']:<{stage_width}}  {s['detail']}")


if __name__ == "__main__":
    main()
