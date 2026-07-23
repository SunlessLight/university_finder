"""
build_dossier.py — render a standardized deep-research dossier for one finalist.

Reads a research JSON the agent assembles in Stage 4 and renders a fixed-order,
16-section Markdown dossier (Snapshot + 14 content sections + Sources) built to
answer three decision questions — can I get in? will I belong & thrive? what will
it take to apply? — so the student can decide, not just compare. Writes it to
data/students/<slug>/dossiers/<slug>.md and flips the matching row(s) in
master_list.csv to List status = Finalist.

Two paths, chosen with --mode (see workflows/04_university_dossier.md):
  * course      (default) — the course-specific dossier: "should I do THIS course
                here?". Every master_list row is a University+Course pair, so it
                matches/flips the row by course_key(university, course).
  * university  — US-only. The whole-institution dossier: "should I go to THIS
                university?", because US undergrads apply to the institution and
                declare a major in year 2. It matches/flips by UNIVERSITY NAME
                only (ignoring Course) and refuses any matched row whose Country
                is not USA.

The fixed section order is enforced per mode: every content section must be present
and non-empty, or the build fails loudly — this is what keeps dossiers comparable
and stops half-researched finalists slipping through.

Usage:
    python tools/build_dossier.py --student aisyah-rahman --input .tmp/aisyah-rahman/dossier_manchester-cs.json
    python tools/build_dossier.py --student toru --input .tmp/toru/uni_mit.json --mode university

Course-mode JSON shape (see the workflow for the full spec):
    {
      "university": "...", "course": "...", "country": "...", "city": "...",
      "overall_rank": "...", "subject_rank": "...",
      "application_system": "...", "admission_likelihood": "...",
      "priorities": "1. Funding · 2. Hands-on · 3. ...",  # optional; shown in the Snapshot
      "slug": "manchester-cs",                # optional; derived if absent
      "sections": {
        "entry_and_fit": "...", "admitted_profiles": "...", "course_details": "...",
        "costs": "...", "scholarships": "...", "cost_of_living": "...",
        "visa_immigration": "...", "recognition_back_home": "...", "employability": "...",
        "student_life_culture": "...", "city_and_belonging": "...",
        "application_checklist": "...", "key_dates": "...", "why_here": "..."
      },
      "sources": [
        {"title": "...", "url": "...", "authority": "Official"|"Aggregator", "as_of": "2026"}
      ]
    }

University-mode JSON shape (no "course"; a whole-institution snapshot + 14 uni sections):
    {
      "university": "...", "country": "...", "city": "...",
      "setting": "urban | college town | rural",
      "type": "private research university | public | liberal arts college",
      "size": "~4,500 undergrads",
      "overall_rank": "...", "application_system": "...", "admission_likelihood": "...",
      "net_cost": "~RM XXk/yr after aid (approx)",   # est. your-share, MYR
      "priorities": "1. Funding · 2. Hands-on · 3. ...",  # optional; shown in the Snapshot
      "slug": "massachusetts-institute-of-technology",  # optional; derived from university
      "sections": {
        "identity_mission": "...", "who_its_for": "...", "admissions_fit": "...",
        "academic_structure": "...", "majors_minors": "...", "signature_experiences": "...",
        "culture_vibe": "...", "student_life_food": "...", "city_belonging": "...",
        "costs_aid": "...", "how_to_apply": "...", "outcomes_network": "...",
        "unique_facts": "...", "why_here": "..."
      },
      "sources": [ ... ]
    }
"""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import SHORTLIST_HEADERS, canonical_uni, course_key, slugify  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# (section key, heading). Snapshot (1) is generated; Sources (last) is a list.
# Ordered decision-first: can I get in? → course & cost → gates & payoff → will I
# belong? → what it takes to apply → should I? Every content section is enforced
# non-empty (see validate); the numbering below is auto-derived from this order.
COURSE_SECTIONS = [
    ("entry_and_fit", "Entry requirements & this student's fit"),
    ("admitted_profiles", "Who actually gets in"),
    ("course_details", "Course details & structure"),
    ("costs", "Costs (full)"),
    ("scholarships", "Scholarships & financial aid"),
    ("cost_of_living", "Cost of living & accommodation"),
    ("visa_immigration", "Visa & immigration"),
    ("recognition_back_home", "Recognition back home"),
    ("employability", "Employability & outcomes"),
    ("student_life_culture", "Student life & culture"),
    ("city_and_belonging", "The city, the area & belonging"),
    ("application_checklist", "Application prep checklist"),
    ("key_dates", "Key dates & deadlines"),
    ("why_here", "Why here / why hesitate"),
]

# The US "university-general" path (--mode university). Same rigor, whole-institution
# lens: US undergrads apply to the institution and declare a major in year 2, so this
# asks "should I GO here?" not "should I do this course here?". Ordered: who it is &
# who it's for → can I get in → how the degree works → the hands-on texture → will I
# belong → cost & apply → payoff → colour → should I?
UNIVERSITY_SECTIONS = [
    ("identity_mission", "Identity & mission"),
    ("who_its_for", "Who it's for — the archetype & this student's fit"),
    ("admissions_fit", "Getting in — admissions & this student's fit"),
    ("academic_structure", "Academic structure & the four years"),
    ("majors_minors", "Majors, minors & flexibility"),
    ("signature_experiences", "Signature academic experiences"),
    ("culture_vibe", "Culture & vibe"),
    ("student_life_food", "Student life & food"),
    ("city_belonging", "The city, the area & belonging"),
    ("costs_aid", "Costs & financial aid"),
    ("how_to_apply", "How to apply"),
    ("outcomes_network", "Outcomes & network"),
    ("unique_facts", "Unique facts & quirks"),
    ("why_here", "Why here / why hesitate"),
]

# Section schema per --mode. Course is the default; university is US-only.
SECTIONS_BY_MODE = {"course": COURSE_SECTIONS, "university": UNIVERSITY_SECTIONS}

STATUS_COL = SHORTLIST_HEADERS.index("List status")
UNI_COL = SHORTLIST_HEADERS.index("University")
COURSE_COL = SHORTLIST_HEADERS.index("Course")
COUNTRY_COL = SHORTLIST_HEADERS.index("Country")

# Country values that count as US for the university-mode guard (the CSV uses "USA").
US_COUNTRY_VALUES = {"usa", "us", "united states", "united states of america"}


def validate(data, mode):
    """Fail loudly if required identity fields or content sections are missing/empty.

    Course mode needs both university + course; university mode needs only university
    (there is no single course — you declare a major in year 2)."""
    required = ("university", "course") if mode == "course" else ("university",)
    for field in required:
        if not (data.get(field) or "").strip():
            sys.exit(f"ERROR: dossier JSON is missing required field '{field}'.")
    sections = data.get("sections") or {}
    schema = SECTIONS_BY_MODE[mode]
    missing = [key for key, _ in schema if not (sections.get(key) or "").strip()]
    if missing:
        sys.exit(
            "ERROR: dossier is incomplete — these sections are empty: "
            + ", ".join(missing)
            + f".\nEvery {mode} dossier must fill all {len(schema)} content sections "
            "(research them, or write 'Not found — <why>')."
        )
    if not data.get("sources"):
        sys.exit("ERROR: dossier has no sources. Every hard fact needs a citation.")


def _fact_table(rows):
    """Render (label, value) pairs as a clean 2-column Markdown table, skipping empty
    values. Snapshots read far better as a scannable key-value table than as a bullet
    list (see tools/report.md) — and giving each field its own cell kills the nested-
    bracket soup the old 'Location (setting (sub-setting))' bullet produced."""
    out = ["| Field | Value |", "| --- | --- |"]
    for label, value in rows:
        if not value:
            continue
        cell = str(value).replace("|", "\\|").replace("\n", " ").strip()
        out.append(f"| **{label}** | {cell} |")
    return "\n".join(out)


def render_snapshot(data):
    rows = [
        ("University", data.get("university")),
        ("Course", data.get("course")),
        ("Country / City", " / ".join(x for x in [data.get("country"), data.get("city")] if x)),
        ("Overall rank", data.get("overall_rank")),
        ("Subject rank", data.get("subject_rank")),
        ("How to apply", data.get("application_system")),
        ("Admission likelihood", data.get("admission_likelihood")),
        ("Your priorities", data.get("priorities")),
    ]
    return _fact_table(rows)


def render_university_snapshot(data):
    """Whole-institution snapshot (no course/subject rank; adds setting, type & size,
    and the est. your-share net cost in MYR). Setting is its own row, not folded into
    Location in parentheses."""
    location = " / ".join(x for x in [data.get("country"), data.get("city")] if x)
    type_size = " · ".join(x for x in [data.get("type"), data.get("size")] if x)
    rows = [
        ("University", data.get("university")),
        ("Location", location),
        ("Setting", data.get("setting")),
        ("Type & size", type_size),
        ("Overall rank", data.get("overall_rank")),
        ("How to apply", data.get("application_system")),
        ("Admission likelihood", data.get("admission_likelihood")),
        ("Est. net cost after aid (MYR)", data.get("net_cost")),
        ("Your priorities", data.get("priorities")),
    ]
    return _fact_table(rows)


def render_sources(sources):
    """Render the source list, de-noised: when authority/as-of are uniform (the common
    case — every source Official, same cycle), state it once in a lead note and drop the
    repeated '— Official — as of 2026' suffix from every line, tagging only exceptions
    (e.g. an Aggregator, or a source from a different year)."""
    from collections import Counter

    auths = Counter((s.get("authority") or "").strip() for s in sources if (s.get("authority") or "").strip())
    years = Counter((s.get("as_of") or "").strip() for s in sources if (s.get("as_of") or "").strip())
    default_auth = auths.most_common(1)[0][0] if auths else ""
    default_year = years.most_common(1)[0][0] if years else ""

    lines = []
    note_bits = []
    if default_year:
        note_bits.append(f"as of the {default_year} cycle")
    if default_auth:
        note_bits.append(f"{default_auth} unless tagged otherwise")
    if note_bits:
        lines += ["_Sources " + "; ".join(note_bits) + "._", ""]

    for s in sources:
        title = s.get("title") or s.get("url") or "source"
        url = s.get("url") or ""
        authority = (s.get("authority") or "").strip()
        as_of = (s.get("as_of") or "").strip()
        link = f"[{title}]({url})" if url else title
        tags = []
        if authority and authority != default_auth:
            tags.append(authority)
        if as_of and as_of != default_year:
            tags.append(f"as of {as_of}")
        suffix = f" — {', '.join(tags)}" if tags else ""
        lines.append(f"- {link}{suffix}")
    return "\n".join(lines)


def render_dossier(data, mode):
    if mode == "university":
        title = f"# Dossier — {data['university']}"
        snapshot = render_university_snapshot(data)
    else:
        title = f"# Dossier — {data['university']}: {data['course']}"
        snapshot = render_snapshot(data)
    schema = SECTIONS_BY_MODE[mode]
    parts = [title, ""]
    parts.append("## 1. Snapshot")
    parts.append(snapshot)
    parts.append("")
    sections = data.get("sections") or {}
    for i, (key, heading) in enumerate(schema, start=2):
        parts.append(f"## {i}. {heading}")
        parts.append(sections[key].strip())
        parts.append("")
    parts.append(f"## {len(schema) + 2}. Sources")
    parts.append(render_sources(data["sources"]))
    parts.append("")
    return "\n".join(parts)


def update_master_list(csv_path, university, course, mode):
    """Flip the matching row(s) to List status = Finalist.

    Course mode matches one row by course_key(university, course). University mode
    (US-only) matches by UNIVERSITY NAME only — a US general dossier certifies the
    whole institution, and the student applies undeclared — so it flips every row for
    that university, after asserting each is a US row.

    There is no "Dossier status" column: the dossier file existing under dossiers/ is the
    fact, and a column duplicating it just goes stale when a file is deleted or renamed.
    """
    if not csv_path.exists():
        print(f"  ! {csv_path.name} not found — dossier written, but no row to update.")
        return
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return

    max_col = max(UNI_COL, COURSE_COL, STATUS_COL, COUNTRY_COL)
    if mode == "university":
        target = canonical_uni(university)
        matches = [
            row for row in rows[1:]
            if len(row) > max_col and canonical_uni(row[UNI_COL]) == target
        ]
        if not matches:
            print(f"  ! No master_list row matched university '{university}'. Dossier written; CSV unchanged.")
            return
        # US-only guard: the whole-institution path is defined for US admissions only.
        non_us = sorted({row[COUNTRY_COL] for row in matches
                         if (row[COUNTRY_COL] or "").strip().lower() not in US_COUNTRY_VALUES})
        if non_us:
            sys.exit(
                f"ERROR: --mode university is US-only, but rows for '{university}' have "
                f"Country = {', '.join(non_us)}. Use the default course mode for non-US universities."
            )
        for row in matches:
            row[STATUS_COL] = "Finalist"
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(rows)
        courses = ", ".join(row[COURSE_COL] for row in matches) or "(no course)"
        print(f"  master_list.csv: {university} -> Finalist ({len(matches)} row(s): {courses})")
        return

    target = course_key(university, course)
    matched = False
    for row in rows[1:]:
        if len(row) <= max(UNI_COL, COURSE_COL, STATUS_COL):
            continue
        if course_key(row[UNI_COL], row[COURSE_COL]) == target:
            if row[STATUS_COL] != "Finalist":
                row[STATUS_COL] = "Finalist"
            matched = True
            break
    if not matched:
        print(f"  ! No master_list row matched {university} — {course}. Dossier written; CSV unchanged.")
        return
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    print(f"  master_list.csv: {university} — {course} -> Finalist")


def main():
    parser = argparse.ArgumentParser(description="Render a standardized finalist dossier.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--input", required=True, help="Path to the dossier research JSON.")
    parser.add_argument(
        "--mode", choices=("course", "university"), default="course",
        help="course (default) = course-specific dossier; university = US-only whole-institution dossier.",
    )
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
    validate(data, args.mode)

    if args.mode == "university":
        # Slug on the university alone so a general dossier (massachusetts-institute-of-technology.md)
        # never collides with a course dossier (mit-bs-mechanical.md) — both can coexist for one uni.
        default_slug = slugify(data["university"])
    else:
        default_slug = slugify(f"{data['university']} {data['course']}")
    slug = data.get("slug") or default_slug
    dossiers_dir = student_dir / "dossiers"
    dossiers_dir.mkdir(parents=True, exist_ok=True)
    out_path = dossiers_dir / f"{slug}.md"
    out_path.write_text(render_dossier(data, args.mode), encoding="utf-8")
    print(f"Wrote dossier: {out_path}")

    update_master_list(student_dir / "master_list.csv", data["university"], data.get("course"), args.mode)


if __name__ == "__main__":
    main()
