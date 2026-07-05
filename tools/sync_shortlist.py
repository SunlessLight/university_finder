"""
sync_shortlist.py — score, dedupe, and append university candidates to the master list.

Reads .tmp/<student-slug>/uni_candidates.json (written by the agent after reviewing
Firecrawl results in Stage 3), computes a desirability score + A/B/C tier, an
admission likelihood (Reach/Match/Safety), and feasibility flags for each candidate,
drops any already present in the student's master_list.csv (by canonical
university+course key), sorts the rest by desirability, and appends them as new rows
with List status "Longlist".

The master list is a plain CSV (data/students/<slug>/master_list.csv) that opens in
Excel / Google Sheets / LibreOffice. It is created with a header row on first run.

This tool NEVER demotes or overwrites existing rows — promotion (Longlist -> Shortlist
-> Finalist) and rejection are agent edits, not a side-effect of syncing.

Usage:
    python tools/sync_shortlist.py --student aisyah-rahman
    python tools/sync_shortlist.py --student aisyah-rahman --dry-run

candidate JSON: a list of objects — see workflows/03_discover_longlist.md for the
full schema. Each carries a "scores" dict (0-5 sub-scores) and an "entry_margin".
"""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import (  # noqa: E402
    DEFAULT_DOSSIER_STATUS,
    DEFAULT_LIST_STATUS,
    SHORTLIST_HEADERS,
    candidate_total_myr,
    classify_admission,
    compute_score,
    course_key,
    feasibility_flags,
    tier_for,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

UNI_COL = SHORTLIST_HEADERS.index("University")
COURSE_COL = SHORTLIST_HEADERS.index("Course")


def _yn(value):
    """Render a tri-state (True/False/None) as Yes/No/blank."""
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return ""


def read_existing(csv_path):
    """Return existing data rows (list of lists), skipping the header. [] if no file."""
    if not csv_path.exists():
        return []
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[1:] if rows else []


def existing_keys(rows):
    """Build the dedupe key set (canonical university+course) from current rows."""
    keys = set()
    for row in rows:
        uni = row[UNI_COL] if len(row) > UNI_COL else ""
        course = row[COURSE_COL] if len(row) > COURSE_COL else ""
        keys.add(course_key(uni, course))
    return keys


def fits_grades_label(candidate, admission):
    """Prefer an explicit fits_grades; otherwise derive from admission likelihood."""
    explicit = candidate.get("fits_grades")
    if explicit not in (None, ""):
        return explicit if isinstance(explicit, str) else _yn(explicit)
    if admission in ("Safety", "Match"):
        return "Yes"
    if admission == "Reach":
        return "No"
    return ""


def candidate_to_row(c, score, tier, admission, flags):
    """Build a CSV row in SHORTLIST_HEADERS order from a scored candidate."""
    myr = candidate_total_myr(c)
    values = {
        "List status": DEFAULT_LIST_STATUS,
        "Desirability": str(score),
        "Tier": tier,
        "Admission likelihood": admission,
        "Warnings": "; ".join(flags),
        "University": c.get("university", ""),
        "Course": c.get("course", ""),
        "Country": c.get("country", ""),
        "City": c.get("city", ""),
        "Subject rank": c.get("subject_rank", ""),
        "Overall rank": c.get("overall_rank", ""),
        "Entry requirements": c.get("entry_requirements", ""),
        "Student grades": c.get("student_grades", ""),
        "Fits grades?": fits_grades_label(c, admission),
        "English req": c.get("english_req", ""),
        "Meets English?": _yn(c.get("meets_english")),
        "Backup entry route": c.get("pathway_option", ""),
        "Annual tuition": c.get("annual_tuition", ""),
        "Total tuition": c.get("total_tuition", ""),
        "Est. living/yr": c.get("est_living_per_year", ""),
        "Duration (yrs)": c.get("duration_years", ""),
        "Total cost (programme)": c.get("total_cost_programme", ""),
        "Currency": c.get("currency", ""),
        "Approx total (MYR)": "" if myr is None else str(myr),
        # Scholarship detail (Toru's #1 priority). Fall back to a legacy single "scholarships" field.
        "Scholarship & portal": c.get("scholarship_portal", c.get("scholarships", "")),
        "Scholarship coverage": c.get("scholarship_coverage", ""),
        "Scholarship competitiveness": c.get("scholarship_competitiveness", ""),
        "How to get the scholarship": c.get("scholarship_how_to", ""),
        "Student community links": c.get("community_links", ""),
        "Student life": c.get("student_life", ""),
        "Money to show (visa)": c.get("funds_proof", ""),
        "Work rights after graduating": c.get("post_study_work", ""),
        "Recognised in Malaysia?": c.get("recognised_back_home", ""),
        "How to apply": c.get("application_system", ""),
        "Key deadline": c.get("key_deadline", ""),
        "Intake": c.get("intake", ""),
        "Course URL": c.get("course_url", ""),
        "Info source": c.get("source_authority", "Aggregator"),
        "Data as-of": c.get("data_as_of", ""),
        "Dossier status": DEFAULT_DOSSIER_STATUS,
        "Notes": c.get("notes", ""),
    }
    return [values.get(h, "") for h in SHORTLIST_HEADERS]


def needs_leading_newline(csv_path):
    """True if the file exists, is non-empty, and its last byte isn't a newline.
    Appending to such a file would fuse the first new row onto the last row."""
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return False
    with csv_path.open("rb") as f:
        f.seek(-1, 2)
        return f.read(1) not in (b"\n", b"\r")


def reorder_to_header(rows, file_header):
    """Re-map rows (built in SHORTLIST_HEADERS order) to an existing file's column
    order. Guards against schema/header drift: an older master_list.csv may carry the
    same columns in a different order (e.g. "Approx total (MYR)" in a different slot).
    Appending schema-order rows to such a file would silently misalign every column.
    Same columns, different order -> remap. Different column set -> refuse (needs migration).
    """
    if file_header == SHORTLIST_HEADERS:
        return rows
    if set(file_header) == set(SHORTLIST_HEADERS):
        idx = [SHORTLIST_HEADERS.index(h) for h in file_header]
        return [[r[i] for i in idx] for r in rows]
    sys.exit(
        "ERROR: master_list.csv columns differ from the current schema "
        "(SHORTLIST_HEADERS). Migrate the file to the schema columns before syncing."
    )


def write_rows(csv_path, rows):
    """Append rows, creating the file with a header row if it doesn't exist yet.
    When appending to an existing file, rows are written in that file's header order,
    not blindly in SHORTLIST_HEADERS order (see reorder_to_header)."""
    is_new = not csv_path.exists()
    if not is_new:
        with csv_path.open(newline="", encoding="utf-8") as f:
            file_header = next(csv.reader(f), None)
        if file_header:
            rows = reorder_to_header(rows, file_header)
    add_newline = needs_leading_newline(csv_path)
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        if add_newline:
            f.write("\r\n")
        writer = csv.writer(f)
        if is_new:
            writer.writerow(SHORTLIST_HEADERS)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Sync scored university candidates into the master list.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--input", help="Path to uni_candidates.json (default .tmp/<slug>/uni_candidates.json).")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Score and dedupe but do not write; print what would be added.",
    )
    args = parser.parse_args()

    slug = args.student
    student_dir = STUDENTS_DIR / slug
    if not student_dir.exists():
        sys.exit(f"ERROR: {student_dir} not found. Run init_student.py first.")

    input_path = Path(args.input) if args.input else REPO_ROOT / ".tmp" / slug / "uni_candidates.json"
    if not input_path.is_absolute():
        input_path = REPO_ROOT / input_path
    if not input_path.exists():
        sys.exit(f"ERROR: {input_path} not found. Write candidates there first (Stage 3).")

    output_path = student_dir / "master_list.csv"

    # Load profile for feasibility checks (budget). Tolerate a not-yet-filled profile.
    profile = {}
    profile_path = student_dir / "profile.json"
    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            profile = {}

    candidates = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(candidates, list):
        sys.exit("ERROR: uni_candidates.json must be a JSON list of candidate objects.")

    seen = set(existing_keys(read_existing(output_path)))
    scored = []
    skipped = 0
    for c in candidates:
        key = course_key(c.get("university"), c.get("course"))
        if key in seen:
            skipped += 1
            continue
        seen.add(key)
        score = compute_score(c.get("scores", {}))
        admission = classify_admission(c.get("entry_margin"))
        flags = feasibility_flags(c, profile)
        scored.append((score, tier_for(score), admission, flags, c))

    scored.sort(key=lambda t: t[0], reverse=True)
    rows = [candidate_to_row(c, score, tier, admission, flags) for score, tier, admission, flags, c in scored]

    print(f"{len(candidates)} candidates in file | {skipped} duplicates skipped | {len(rows)} new")
    for score, tier, admission, flags, c in scored:
        flag_str = f"  ⚑ {'; '.join(flags)}" if flags else ""
        print(f"  [{tier}] {score:>3}  {admission or '-':<7} {c.get('university','?')} — {c.get('course','?')}{flag_str}")

    if args.dry_run:
        print("\n(dry run — nothing written)")
        return
    if not rows:
        print("\nNothing new to add.")
        return

    write_rows(output_path, rows)
    print(f"\nAppended {len(rows)} rows to {output_path} (as Longlist)")


if __name__ == "__main__":
    main()
