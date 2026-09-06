"""
build_report.py — render a standardized deep-research report for one finalist.

Reads a research JSON the agent assembles in Stage 4 and renders a fixed-order,
15-section Markdown report (Snapshot + 13 content sections + Sources) built to
answer three decision questions — can I get in? will I belong & thrive? what will
it take to apply? — so the student can decide, not just compare. Writes it to
data/students/<slug>/reports/<slug>.md, plus a small FINALIST MARKER fragment at
.tmp/<slug>/finalists/<report-slug>.json.

This tool does NOT touch master_list.csv. It used to — it read and rewrote the
whole file to flip one row to Finalist, which is exactly why report-writer
dispatches had to run one at a time (two in flight could silently drop a flip).
Now it writes a fragment and flip_finalists.py folds every fragment into the CSV
in ONE pass, after the whole batch is back. Same fragments-in / one-write-out
pattern Stage 3 uses (row-filler -> merge_candidates.py), and the same payoff:
the dispatches are parallel-safe.

One schema, every country, since 2026-09-06 (see report_merge_plan.md). --mode no
longer picks which sections render — every report gets the same 13 content
sections (REPORT_SECTIONS). --mode only selects:
  * the Snapshot shape — course mode renders Course + subject rank; university
    mode renders Setting / Type & size / est. net cost instead.
  * what the finalist marker claims (see workflows/04_university_report.md):
      - course      (default) — the marker carries university + course, and
                    flip_finalists.py matches the row by
                    course_key(university, course). Every master_list row is a
                    University+Course pair, so this is the default claim.
      - university  — US-only. The marker carries no course; flip_finalists.py
                    matches by UNIVERSITY NAME only (ignoring Course) and refuses
                    any matched row whose Country is not USA — because US
                    undergrads apply to the institution and declare a major in
                    year 2, so one report legitimately speaks for every row.

The fixed section order is enforced: every content section must be present and
non-empty, or the build fails loudly — this is what keeps reports comparable and
stops half-researched finalists slipping through.

Usage:
    python tools/build_report.py --student <slug> --input .tmp/<slug>/report_<report-slug>.json
    python tools/build_report.py --student <slug> --input .tmp/<slug>/uni_<uni-slug>.json --mode university

JSON shape (see the workflow for the full spec). Course mode requires "course";
university mode omits it and adds "setting" / "type" / "size" / "net_cost" for the
whole-institution Snapshot:
    {
      "university": "...", "course": "...",          # course omitted in university mode
      "country": "...", "city": "...",
      "setting": "urban | college town | rural",       # university mode only
      "type": "private research university | public | liberal arts college",  # university mode only
      "size": "~4,500 undergrads",                     # university mode only
      "net_cost": "~RM XXk/yr after aid (approx)",     # university mode only, est. your-share MYR
      "overall_rank": "...", "subject_rank": "...",    # subject_rank is course mode only
      "application_system": "...", "admission_likelihood": "...",
      "priorities": "1. Funding · 2. Hands-on · 3. ...",  # optional; shown in the Snapshot
      "slug": "manchester-cs",                # optional; derived if absent
      "sections": {
        "identity_mission": "...", "who_its_for": "...", "getting_in": "...",
        "what_youll_study": "...", "signature_experiences": "...", "culture_vibe": "...",
        "student_life": "...", "city_and_belonging": "...", "costs": "...",
        "scholarships": "...", "outcomes": "...", "unique_facts": "...", "why_here": "..."
      },
      "sources": [
        {"title": "...", "url": "...", "authority": "Official"|"Aggregator", "as_of": "2026"}
      ],
      # optional — ONLY cells this report's deeper research proves wrong. Copied
      # verbatim into the marker; flip_finalists.py validates and applies them.
      # In university mode, "Course at a glance" is a WARNING: a university-mode
      # marker can match several course rows at once, and one course sentence is
      # wrong for all but one of them. "Student life" is fine (campus-wide).
      "corrections": {"Course at a glance": "...", "Student life": "..."}
    }

dated_items (optional, top-level, unchanged by the 2026-09-06 merge): a list of
{"item": "...", "date": "..."} the Stage 5 calendar tool globs for directly out of
this JSON — see build_calendar.py. sources and corrections are unchanged too.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import slugify  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# (section key, heading). Snapshot (1) is generated; Sources (last) is a list.
# ONE schema for every country since 2026-09-06 (see report_merge_plan.md). --mode no longer
# selects sections — it selects the Snapshot shape and what the finalist marker claims.
# Ordered: who is this place -> can I get in -> what I'd study -> will I belong -> money ->
# payoff -> colour -> should I.
REPORT_SECTIONS = [
    ("identity_mission", "Identity & what it's known for"),
    ("who_its_for", "Who it's for — the archetype & your fit"),
    ("getting_in", "Getting in — requirements, who gets in & your fit"),
    ("what_youll_study", "What you'll actually study"),
    ("signature_experiences", "Signature academic experiences"),
    ("culture_vibe", "Culture & vibe"),
    ("student_life", "Student life, housing & food"),
    ("city_and_belonging", "The city, the area & belonging"),
    ("costs", "Costs (full)"),
    ("scholarships", "Scholarships & financial aid"),
    ("outcomes", "Outcomes, network & practising in Malaysia"),
    ("unique_facts", "Unique facts & quirks"),
    ("why_here", "Why here / why hesitate"),
]

# READ-ONLY history. Reports built before 2026-09-06 use these; check_report.py needs them to
# lint what is already on disk. build_report.py NEVER emits them again — do not add to them,
# do not "fix" them, and do not route new work through them.
LEGACY_COURSE_SECTIONS = [
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

LEGACY_UNIVERSITY_SECTIONS = [
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

# Every schema check_report.py may encounter. Only "report" is buildable.
SCHEMAS = {
    "report": REPORT_SECTIONS,
    "legacy_course": LEGACY_COURSE_SECTIONS,
    "legacy_university": LEGACY_UNIVERSITY_SECTIONS,
}


def validate(data, mode):
    """Fail loudly if required identity fields or content sections are missing/empty.

    Course mode needs both university + course; university mode needs only university
    (there is no single course — you declare a major in year 2)."""
    required = ("university", "course") if mode == "course" else ("university",)
    for field in required:
        if not (data.get(field) or "").strip():
            sys.exit(f"ERROR: report JSON is missing required field '{field}'.")
    sections = data.get("sections") or {}
    schema = REPORT_SECTIONS
    missing = [key for key, _ in schema if not (sections.get(key) or "").strip()]
    if missing:
        sys.exit(
            "ERROR: report is incomplete — these sections are empty: "
            + ", ".join(missing)
            + f".\nEvery report must fill all {len(schema)} content sections "
            "(research them, or write 'Not found — <why>')."
        )
    if not data.get("sources"):
        sys.exit("ERROR: report has no sources. Every hard fact needs a citation.")


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


def render_report(data, mode):
    if mode == "university":
        title = f"# University Report — {data['university']}"
        snapshot = render_university_snapshot(data)
    else:
        title = f"# University Report — {data['university']}: {data['course']}"
        snapshot = render_snapshot(data)
    schema = REPORT_SECTIONS
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


def write_finalist_marker(student_slug, slug, data, mode):
    """Write the finalist marker fragment this report is claiming a CSV flip with.

    One file per report at .tmp/<student>/finalists/<slug>.json, named with the SAME
    slug as the report itself, so marker and report are obviously a pair
    (manchester-cs.json <-> manchester-cs.md) and a re-render overwrites its own
    marker instead of stacking duplicates.

    Deliberately dumb: it records the claim (this university[+course] earned a report,
    here are the cells the research contradicted) and nothing else. All the judgement —
    does a row match, is it already Rejected, is a correction a real column within its
    cell budget, is a university-mode marker really pointing at US rows — belongs to
    flip_finalists.py, which is the only thing that opens master_list.csv.

    There is no "Report status" column: the report file existing under reports/ is the
    fact, and a column duplicating it just goes stale when a file is deleted or renamed.
    """
    corrections = data.get("corrections") or {}
    if not isinstance(corrections, dict):
        sys.exit(
            "ERROR: 'corrections' must be an object of master-list column -> new value "
            f"(got {type(corrections).__name__}). See the JSON shape in this file's header."
        )

    marker = {
        "university": data["university"],
        # University mode has no course by design — the marker matches on name alone.
        "course": data.get("course") if mode == "course" else None,
        "mode": mode,
        "corrections": {str(k): v for k, v in corrections.items()},
    }
    marker_dir = REPO_ROOT / ".tmp" / student_slug / "finalists"
    marker_dir.mkdir(parents=True, exist_ok=True)
    marker_path = marker_dir / f"{slug}.json"
    marker_path.write_text(json.dumps(marker, indent=2, ensure_ascii=False), encoding="utf-8")

    detail = f" + {len(corrections)} correction(s)" if corrections else ""
    print(f"Wrote finalist marker: {marker_path}{detail}")
    return marker_path


def main():
    parser = argparse.ArgumentParser(description="Render a standardized finalist report.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--input", required=True, help="Path to the report research JSON.")
    parser.add_argument(
        "--mode", choices=("course", "university"), default="course",
        help="What this report claims: course (default) = one University+Course row, US-only "
             "university = every row for that university. Both render the same 13 sections.",
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
        # Slug on the university alone so a general report (massachusetts-institute-of-technology.md)
        # never collides with a course report (mit-bs-mechanical.md) — both can coexist for one uni.
        default_slug = slugify(data["university"])
    else:
        default_slug = slugify(f"{data['university']} {data['course']}")
    slug = data.get("slug") or default_slug
    reports_dir = student_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_path = reports_dir / f"{slug}.md"
    out_path.write_text(render_report(data, args.mode), encoding="utf-8")
    print(f"Wrote report: {out_path}")

    write_finalist_marker(args.student, slug, data, args.mode)
    print(
        f"\nNext (main session, ONCE after every dispatch is back):\n"
        f"      python tools/flip_finalists.py --student {args.student}\n"
        f"      python tools/check_master_list.py --student {args.student}\n"
        f"      Nothing in master_list.csv changes until that first command runs."
    )


if __name__ == "__main__":
    main()
