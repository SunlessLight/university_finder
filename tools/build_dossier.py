"""
build_dossier.py — render a standardized deep-research dossier for one finalist.

Reads a research JSON the agent assembles in Stage 5 and renders a fixed-order,
14-section Markdown dossier so every finalist is directly comparable. Writes it to
data/students/<slug>/dossiers/<uni-course-slug>.md and flips that row in
master_list.csv to Dossier status = Done (and List status = Finalist).

The fixed section order is enforced: every content section must be present and
non-empty, or the build fails loudly — this is what keeps dossiers comparable and
stops half-researched finalists slipping through.

Usage:
    python tools/build_dossier.py --student aisyah-rahman --input .tmp/aisyah-rahman/dossier_manchester-cs.json

Input JSON shape (see workflows/05_university_dossier.md for the full spec):
    {
      "university": "...", "course": "...", "country": "...", "city": "...",
      "overall_rank": "...", "subject_rank": "...",
      "application_system": "...", "admission_likelihood": "...",
      "slug": "manchester-cs",                # optional; derived if absent
      "sections": {
        "course_details": "markdown...",
        "entry_and_fit": "markdown...",
        "costs": "markdown...",
        "scholarships": "markdown...",
        "visa_immigration": "markdown...",
        "recognition_back_home": "markdown...",
        "cost_of_living": "markdown...",
        "employability": "markdown...",
        "environment_community": "markdown...",
        "student_sentiment": "markdown...",
        "how_to_apply": "markdown...",
        "key_dates": "markdown..."
      },
      "sources": [
        {"title": "...", "url": "...", "authority": "Official"|"Aggregator", "as_of": "2026"}
      ]
    }
"""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import SHORTLIST_HEADERS, course_key, slugify  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# (section key, heading). Snapshot (1) is generated; Sources (14) is a list.
CONTENT_SECTIONS = [
    ("course_details", "Course details & structure"),
    ("entry_and_fit", "Entry requirements & this student's fit"),
    ("costs", "Costs (full)"),
    ("scholarships", "Scholarships & financial aid"),
    ("visa_immigration", "Visa & immigration"),
    ("recognition_back_home", "Recognition back home"),
    ("cost_of_living", "Cost of living & accommodation"),
    ("employability", "Employability & outcomes"),
    ("environment_community", "Environment, community & student life"),
    ("student_sentiment", "Student sentiment"),
    ("how_to_apply", "How to apply — step by step"),
    ("key_dates", "Key dates & deadlines"),
]

STATUS_COL = SHORTLIST_HEADERS.index("List status")
DOSSIER_COL = SHORTLIST_HEADERS.index("Dossier status")
UNI_COL = SHORTLIST_HEADERS.index("University")
COURSE_COL = SHORTLIST_HEADERS.index("Course")


def validate(data):
    """Fail loudly if required identity fields or content sections are missing/empty."""
    for field in ("university", "course"):
        if not (data.get(field) or "").strip():
            sys.exit(f"ERROR: dossier JSON is missing required field '{field}'.")
    sections = data.get("sections") or {}
    missing = [key for key, _ in CONTENT_SECTIONS if not (sections.get(key) or "").strip()]
    if missing:
        sys.exit(
            "ERROR: dossier is incomplete — these sections are empty: "
            + ", ".join(missing)
            + ".\nEvery finalist dossier must fill all 12 content sections (research them, "
            "or write 'Not found — <why>')."
        )
    if not data.get("sources"):
        sys.exit("ERROR: dossier has no sources. Every hard fact needs a citation.")


def render_snapshot(data):
    rows = [
        ("University", data.get("university")),
        ("Course", data.get("course")),
        ("Country / City", " / ".join(x for x in [data.get("country"), data.get("city")] if x)),
        ("Overall rank", data.get("overall_rank")),
        ("Subject rank", data.get("subject_rank")),
        ("How to apply", data.get("application_system")),
        ("Admission likelihood", data.get("admission_likelihood")),
    ]
    return "\n".join(f"- **{label}:** {value or '—'}" for label, value in rows)


def render_sources(sources):
    lines = []
    for s in sources:
        title = s.get("title") or s.get("url") or "source"
        url = s.get("url") or ""
        authority = s.get("authority") or ""
        as_of = s.get("as_of") or ""
        suffix = " — ".join(x for x in [authority, f"as of {as_of}" if as_of else ""] if x)
        link = f"[{title}]({url})" if url else title
        lines.append(f"- {link}{(' — ' + suffix) if suffix else ''}")
    return "\n".join(lines)


def render_dossier(data):
    parts = [f"# Dossier — {data['university']}: {data['course']}", ""]
    parts.append("## 1. Snapshot")
    parts.append(render_snapshot(data))
    parts.append("")
    sections = data.get("sections") or {}
    for i, (key, heading) in enumerate(CONTENT_SECTIONS, start=2):
        parts.append(f"## {i}. {heading}")
        parts.append(sections[key].strip())
        parts.append("")
    parts.append("## 14. Sources")
    parts.append(render_sources(data["sources"]))
    parts.append("")
    return "\n".join(parts)


def update_master_list(csv_path, university, course):
    """Flip the matching row to Dossier status = Done and List status = Finalist."""
    if not csv_path.exists():
        print(f"  ! {csv_path.name} not found — dossier written, but no row to update.")
        return
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return
    target = course_key(university, course)
    matched = False
    for row in rows[1:]:
        if len(row) <= max(UNI_COL, COURSE_COL, STATUS_COL, DOSSIER_COL):
            continue
        if course_key(row[UNI_COL], row[COURSE_COL]) == target:
            row[DOSSIER_COL] = "Done"
            if row[STATUS_COL] != "Finalist":
                row[STATUS_COL] = "Finalist"
            matched = True
            break
    if not matched:
        print(f"  ! No master_list row matched {university} — {course}. Dossier written; CSV unchanged.")
        return
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    print(f"  master_list.csv: {university} — {course} -> Finalist / Dossier Done")


def main():
    parser = argparse.ArgumentParser(description="Render a standardized finalist dossier.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--input", required=True, help="Path to the dossier research JSON.")
    args = parser.parse_args()

    student_dir = STUDENTS_DIR / args.student
    if not student_dir.exists():
        sys.exit(f"ERROR: {student_dir} not found. Run init_student.py first.")

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = REPO_ROOT / input_path
    if not input_path.exists():
        sys.exit(f"ERROR: {input_path} not found.")

    data = json.loads(input_path.read_text(encoding="utf-8"))
    validate(data)

    slug = data.get("slug") or slugify(f"{data['university']} {data['course']}")
    dossiers_dir = student_dir / "dossiers"
    dossiers_dir.mkdir(parents=True, exist_ok=True)
    out_path = dossiers_dir / f"{slug}.md"
    out_path.write_text(render_dossier(data), encoding="utf-8")
    print(f"Wrote dossier: {out_path}")

    update_master_list(student_dir / "master_list.csv", data["university"], data["course"])


if __name__ == "__main__":
    main()
