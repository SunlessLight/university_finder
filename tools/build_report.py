"""
build_report.py — render a standardized deep-research report for one finalist.

Reads a research JSON the agent assembles in Stage 4 and renders a fixed-order,
15-section Markdown report (Snapshot + 13 content sections + Sources) built to
answer three decision questions — can I get in? will I belong & thrive? what will
it take to apply? — so the student can decide, not just compare. Writes it to
data/students/<slug>/reports/<slug>.md, plus a small FINALIST MARKER fragment at
.tmp/<slug>/finalists/<report-slug>.json, plus — when the JSON carries "dated_items" —
a permanent copy of them at data/students/<slug>/dated_items/<report-slug>.json.

This tool does NOT touch master_list.csv. It used to — it read and rewrote the
whole file to flip one row to Finalist, which is exactly why report-writer
dispatches had to run one at a time (two in flight could silently drop a flip).
Now it writes a fragment and flip_finalists.py folds every fragment into the CSV
in ONE pass, after the whole batch is back. Same fragments-in / one-write-out
pattern Stage 3 uses (row-filler -> merge_candidates.py), and the same payoff:
the dispatches are parallel-safe.

One schema, every country, since 2026-09-06. --mode no
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

--quick (workflows/quick_university_report.md) renders a standalone report with no student
involved at all: no profile.json/preferences.json/master_list.csv, no finalist marker, no flip
step. Output goes to data/quick_reports/<slug>.md instead of data/students/<slug>/reports/.
Use it instead of --student when a student already knows the university and just wants the
facts, without going through Stage 1 (intake) or Stage 3 (longlist) first. The input JSON is the
same shape, just without "priorities"/"grades_vs_bar"/"our_assessment" (meaningless with no student
profile to compare against) — the Snapshot table already skips a row when empty, and --quick skips
the box.

Changed 2026-10-30 (Evan): a student's report opens with "Your profile", the same facts as the
list PDF plus their location and other preferences, read from profile.json + preferences.json.
Never their race: the Scholarships section uses it, the first page doesn't need it. It is a ###
heading on purpose: report_to_pdf.py places "Key terms" by counting ## headings, and check_report.py
only reads numbered ones. A --quick report has no student, so no block.

Changed 2026-11-02 (R34, Evan): every section is sourced fact; all opinion goes in one box, section
14 "Our assessment (a judgment, not a fact)", key our_assessment. The key changed from why_here on
purpose, so a JSON written the old way fails the build instead of pouring a verdict into the new
shape. The Snapshot prints the published admit_rate, not Reach/Match/Safety (internal only). The box
opens with grades_vs_bar, explained in JUDGMENT_LABELS' words. Reports print "Prepared on <build
date>". --quick is sold as facts only, so it has no box: 12 content sections, numbered 1 to 14.

Usage:
    python tools/build_report.py --student <slug> --input .tmp/<slug>/report_<report-slug>.json
    python tools/build_report.py --student <slug> --input .tmp/<slug>/uni_<uni-slug>.json --mode university
    python tools/build_report.py --quick --input .tmp/quick/report_<slug>.json

JSON shape (see the workflow for the full spec). Course mode requires "course";
university mode omits it and adds "setting" / "type" / "size" / "net_cost" for the
whole-institution Snapshot:
    {
      "university": "...", "course": "...",          # course omitted in university mode
      "country": "...", "city": "...",
      "setting": "urban | college town | rural",       # university mode only
      "type": "private research university | public | liberal arts college",  # university mode only
      "size": "4,500 undergraduates",                  # university mode only
      "net_cost": "By family income: ~RM Xk-Yk/yr (uni's examples, 20XX; approx)",  # university mode only; no single your-share (S3)
      "overall_rank": "...", "subject_rank": "...",    # subject_rank is course mode only
      "application_system": "...",
      "admit_rate": "4.6% overall, 2.0% international (MIT, 2025)",  # the published figure, or "Not published"
      "grades_vs_bar": "Not published",                # our label; printed in the box, not the Snapshot
      "priorities": "1. Funding · 2. Hands-on · 3. ...",  # optional; shown in the Snapshot
      "slug": "manchester-cs",                # optional; derived if absent
      "sections": {
        "identity_mission": "...", "who_its_for": "...", "getting_in": "...",
        "what_youll_study": "...", "signature_experiences": "...", "culture_vibe": "...",
        "student_life": "...", "city_and_belonging": "...", "costs": "...",
        "scholarships": "...", "outcomes": "...", "unique_facts": "...",
        "our_assessment": "..."                        # left out with --quick
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

dated_items (optional, top-level): every deadline this report's research turned up, for
the Stage 5 calendar (build_calendar.py):
    "dated_items": [
      {"date": "2027-01-15", "label": "UCAS deadline", "action": "Submit application"}
    ]
"date" is YYYY-MM-DD where the page gives one (anything else lands in the calendar's
"Undated / to confirm" list), "label" names the event, "action" is optional. This tool
copies the list to data/students/<slug>/dated_items/<report-slug>.json, because the input
JSON lives in .tmp/ and .tmp/ is disposable: a calendar built after a cleanup used to
lose every date that was not in master_list.csv. A rebuild whose JSON has no dated_items
leaves an earlier copy alone. --quick saves nothing (no student folder).
sources and corrections are unchanged by the 2026-09-06 merge.
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_glossary import JUDGMENT_LABELS  # noqa: E402
from build_list_pdf import load_profile, student_items  # noqa: E402
from shortlist_schema import slugify  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# Folder inside a student's (permanent, gitignored) folder holding one dated_items file per
# report. build_calendar.py imports this name, so writer and reader cannot drift apart.
DATED_ITEMS_DIRNAME = "dated_items"

# (section key, heading). Snapshot (1) is generated; Sources (last) is a list.
# ONE schema for every country since 2026-09-06. --mode no longer
# selects sections — it selects the Snapshot shape and what the finalist marker claims.
# Ordered: who is this place -> can I get in -> what I'd study -> will I belong -> money ->
# payoff -> notable facts -> our judgment. Facts only, except the last (R34).
REPORT_SECTIONS = [
    ("identity_mission", "Identity & what it's known for"),
    ("who_its_for", "Who it's for"),
    ("getting_in", "Getting in — requirements and who gets in"),
    ("what_youll_study", "What you'll actually study"),
    ("signature_experiences", "Signature academic experiences"),
    ("culture_vibe", "Campus culture"),
    ("student_life", "Student life, housing & food"),
    ("city_and_belonging", "The city, the area & belonging"),
    ("costs", "Costs (full)"),
    ("scholarships", "Scholarships & financial aid"),
    ("outcomes", "Outcomes, network & practising in Malaysia"),
    ("unique_facts", "Notable facts"),
    ("our_assessment", "Our assessment (a judgment, not a fact)"),
]

# A quick report is sold as facts only, so it has no box.
QUICK_SECTIONS = [s for s in REPORT_SECTIONS if s[0] != "our_assessment"]

# READ-ONLY history. Reports built before 2026-11-02 use these; check_report.py needs them to
# lint what is already on disk. build_report.py NEVER emits them again — do not add to them,
# do not "fix" them, and do not route new work through them.
LEGACY_REPORT_SECTIONS = [
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

# READ-ONLY history, as above, for reports built before 2026-09-06.
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
    "legacy_report": LEGACY_REPORT_SECTIONS,
    "legacy_course": LEGACY_COURSE_SECTIONS,
    "legacy_university": LEGACY_UNIVERSITY_SECTIONS,
}


def validate(data, mode, quick=False):
    """Fail loudly if required identity fields or content sections are missing/empty.

    Course mode needs both university + course; university mode needs only university
    (there is no single course — you declare a major in year 2)."""
    required = ("university", "course") if mode == "course" else ("university",)
    for field in required:
        if not (data.get(field) or "").strip():
            sys.exit(f"ERROR: report JSON is missing required field '{field}'.")
    sections = data.get("sections") or {}
    schema = QUICK_SECTIONS if quick else REPORT_SECTIONS
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


def render_student_profile(student_dir):
    """The "Your profile" block for the report's first page, or "" with no profile on disk."""
    profile_path = Path(student_dir) / "profile.json"
    if not profile_path.exists():
        return ""
    preferences_path = Path(student_dir) / "preferences.json"
    profile = load_profile(profile_path, preferences_path if preferences_path.exists() else None)
    prefs = profile.get("preferences") or {}
    rows = student_items(profile)
    rows.append(("Location", ", ".join(prefs.get("location_prefs") or [])))
    rows.append(("Preferences", ", ".join(prefs.get("other_preferences") or [])))
    return f"### Your profile\n{_fact_table(rows)}"


def render_snapshot(data):
    rows = [
        ("University", data.get("university")),
        ("Course", data.get("course")),
        ("Country / City", " / ".join(x for x in [data.get("country"), data.get("city")] if x)),
        ("Overall rank", data.get("overall_rank")),
        ("Subject rank", data.get("subject_rank")),
        ("How to apply", data.get("application_system")),
        ("Admit rate", data.get("admit_rate")),
        ("Your priorities", data.get("priorities")),
    ]
    return _fact_table(rows)


def render_university_snapshot(data):
    """Whole-institution snapshot (no course/subject rank; adds setting, type & size,
    and the net cost in MYR by income band). Setting is its own row, not folded into
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
        ("Admit rate", data.get("admit_rate")),
        ("Est. net cost after aid (MYR)", data.get("net_cost")),
        ("Your priorities", data.get("priorities")),
    ]
    return _fact_table(rows)


def render_assessment(body, grades_vs_bar):
    """Section 14: the one box that may hold opinion, opening with our grades label."""
    lines = ['<div class="callout-note" markdown="1">', ""]
    if grades_vs_bar:
        definition = JUDGMENT_LABELS["Grades vs entry bar"]["definition"]
        lines += [f"**Grades vs entry bar: {grades_vs_bar}.** {definition}", ""]
    lines += [body.strip(), "", "</div>"]
    return "\n".join(lines)


def prepared_line(day=None):
    """The date under the title, so a printed fee or deadline can be seen to have aged."""
    day = day or date.today()
    return f"_Prepared on {day.day} {day:%B %Y}._"


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


def render_report(data, mode, student_profile="", quick=False):
    if mode == "university":
        title = f"# University Report — {data['university']}"
        snapshot = render_university_snapshot(data)
    else:
        title = f"# University Report — {data['university']}: {data['course']}"
        snapshot = render_snapshot(data)
    schema = QUICK_SECTIONS if quick else REPORT_SECTIONS
    parts = [title, "", prepared_line(), ""]
    if student_profile:
        parts += [student_profile, ""]
    parts.append("## 1. Snapshot")
    parts.append(snapshot)
    parts.append("")
    sections = data.get("sections") or {}
    for i, (key, heading) in enumerate(schema, start=2):
        parts.append(f"## {i}. {heading}")
        if key == "our_assessment":
            parts.append(render_assessment(sections[key], data.get("grades_vs_bar")))
        else:
            parts.append(sections[key].strip())
        parts.append("")
    parts.append(f"## {len(schema) + 2}. Sources")
    parts.append(render_sources(data["sources"]))
    parts.append("")
    return "\n".join(parts)


def normalize_dated_items(raw):
    """Return dated_items as a list of {"date", "label", "action"} strings.

    Absent/empty is fine (the field is optional) and returns []. Anything that is not a
    list of objects fails loudly, same as an empty section. The old {"item", "date"}
    wording — which this file's header documented until 2026-10-13, so real JSONs carry
    it — is accepted and saved as "label", so the calendar never shows a nameless date.
    """
    if not raw:
        return []
    if not isinstance(raw, list) or not all(isinstance(it, dict) for it in raw):
        sys.exit(
            "ERROR: 'dated_items' must be a list of objects like "
            '{"date": "2027-01-15", "label": "UCAS deadline", "action": "Submit application"}. '
            "See the JSON shape in this file's header."
        )
    items = []
    for it in raw:
        label = str(it.get("label") or it.get("item") or "").strip()
        if not label:
            sys.exit(f"ERROR: a 'dated_items' entry has no 'label' (what the date is for): {it}")
        items.append({
            "date": str(it.get("date") or "").strip(),
            "label": label,
            "action": str(it.get("action") or "").strip(),
        })
    return items


def save_dated_items(student_dir, slug, data, mode, overwrite=True):
    """Keep a permanent copy of a report's dated_items in the student's own folder.

    One file per report at <student_dir>/dated_items/<slug>.json, named with the SAME slug
    as the report (and its finalist marker), so a re-render replaces its own dates instead
    of stacking a second copy. Carries university + course + mode so build_calendar.py can
    match it to a master_list row the way flip_finalists.py matches a marker: course mode by
    University+Course, university mode (US-only, no course) by university name alone.

    Returns the path written, or None when there was nothing to save — no dated_items in
    the JSON, or overwrite=False and a file is already there. Never deletes: a rebuild from
    a JSON without dated_items must not wipe dates an earlier build found.
    """
    items = normalize_dated_items(data.get("dated_items"))
    if not items:
        return None
    out_dir = Path(student_dir) / DATED_ITEMS_DIRNAME
    out_path = out_dir / f"{slug}.json"
    if out_path.exists() and not overwrite:
        return None
    out_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "university": data["university"],
        # University mode has no course by design — the calendar matches on name alone.
        "course": data.get("course") if mode == "course" else None,
        "mode": mode,
        "dated_items": items,
    }
    out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


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
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--student", help="Student slug (folder under data/students/).")
    target.add_argument(
        "--quick", action="store_true",
        help="Standalone report, no student folder: no profile/preferences/master_list.csv "
             "involved, no finalist marker written. Writes to data/quick_reports/<slug>.md "
             "instead of data/students/<slug>/reports/.",
    )
    parser.add_argument("--input", required=True, help="Path to the report research JSON.")
    parser.add_argument(
        "--mode", choices=("course", "university"), default="course",
        help="What this report claims: course (default) = one University+Course row, US-only "
             "university = every row for that university. Both render the same sections.",
    )
    args = parser.parse_args()

    if not args.quick:
        student_dir = STUDENTS_DIR / args.student
        if not student_dir.exists():
            sys.exit(f"ERROR: {student_dir} not found. Run init_student.py first.")

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = REPO_ROOT / input_path
    if not input_path.exists():
        sys.exit(f"ERROR: {input_path} not found.")

    data = json.loads(input_path.read_text(encoding="utf-8"))
    validate(data, args.mode, quick=args.quick)
    # Before anything is written: a malformed dated_items stops the build, like an empty section.
    dated_items = normalize_dated_items(data.get("dated_items"))

    if args.mode == "university":
        # Slug on the university alone so a general report (massachusetts-institute-of-technology.md)
        # never collides with a course report (mit-bs-mechanical.md) — both can coexist for one uni.
        default_slug = slugify(data["university"])
    else:
        default_slug = slugify(f"{data['university']} {data['course']}")
    slug = data.get("slug") or default_slug
    reports_dir = (REPO_ROOT / "data" / "quick_reports") if args.quick else (STUDENTS_DIR / args.student / "reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_path = reports_dir / f"{slug}.md"
    student_profile = "" if args.quick else render_student_profile(STUDENTS_DIR / args.student)
    out_path.write_text(render_report(data, args.mode, student_profile, quick=args.quick), encoding="utf-8")
    print(f"Wrote report: {out_path}")

    if args.quick:
        # No master_list.csv row exists for a quick report — nothing to flip, nothing to reconcile.
        return
    if not (STUDENTS_DIR / args.student / "master_list.csv").exists():
        # A report order (report form, no list bought): same, the student just has a folder.
        print("No master_list.csv for this student, so no finalist marker: the report is the deliverable.")
        return

    write_finalist_marker(args.student, slug, data, args.mode)
    dates_path = save_dated_items(STUDENTS_DIR / args.student, slug, data, args.mode)
    if dates_path:
        print(f"Saved {len(dated_items)} dated item(s) for the calendar: {dates_path}")
    else:
        kept = STUDENTS_DIR / args.student / DATED_ITEMS_DIRNAME / f"{slug}.json"
        note = f" The earlier saved dates are kept: {kept}" if kept.exists() else ""
        print(f"No dated_items in this JSON — nothing saved for the calendar.{note}")
    print(
        f"\nNext (main session, ONCE after every dispatch is back):\n"
        f"      python tools/flip_finalists.py --student {args.student}\n"
        f"      python tools/check_master_list.py --student {args.student}\n"
        f"      Nothing in master_list.csv changes until that first command runs."
    )


if __name__ == "__main__":
    main()
