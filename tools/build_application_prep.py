"""
build_application_prep.py — render an action-only application-prep guide for one
region, grouped by application system.

Reads a research JSON the agent assembles from official admissions/financial-aid
pages and renders a single Markdown guide that answers one question — *what do I
need to do to apply?* — for every Shortlist/Finalist university in a region. It
groups universities by their application system (e.g. Common App vs a school's own
portal) so the student files shared items once, and it foregrounds the hard apply
mechanics: deadlines, tests, essays, fees, and the financial-aid forms/documents/
dates. Writes it to data/students/<slug>/application_prep/<region>.md.

This is a decision-support / how-to-apply deliverable (sibling of build_calendar.py):
read-only against master_list.csv — it does NOT change List status or flip rows.
It complements the per-university dossier (build_dossier.py); it does not replace it.

Every university must carry non-empty deadlines + application_checklist + financial_aid,
or the build fails loudly — a half-researched apply guide shouldn't pass.

Usage:
    python tools/build_application_prep.py --student toru --input .tmp/toru/apply_prep_us.json

Input JSON shape (see workflows/08_application_prep.md for the full spec):
    {
      "student_slug": "toru",
      "region": "us",
      "region_title": "United States",
      "overview": "markdown — the cross-cutting apply strategy for this region",
      "systems": [
        {"system": "Common App",
         "universities": ["Princeton", "Stanford", "UPenn", "Harvard", "Yale"],
         "shared_checklist": "markdown — items filed once across these schools"},
        {"system": "MIT application (own portal, NOT Common App)",
         "universities": ["MIT"], "shared_checklist": "markdown"}
      ],
      "universities": [
        {"name": "Princeton University", "system": "Common App",
         "admission_likelihood": "Reach",
         "deadlines": {"application": "2027-01-01 (RD; SCEA 2026-11-01)", "aid": "..."},
         "tests": "markdown", "essays": "markdown", "fees": "markdown",
         "financial_aid": "markdown — need model, forms, income docs, dates",
         "application_checklist": "markdown", "portal": "https://..."}
      ],
      "consolidated_checklist": "markdown — the gather-once list across the region",
      "dated_items": [
        {"date": "2027-01-01", "label": "Regular Decision deadline", "action": "Submit"}
      ],
      "sources": [
        {"title": "...", "url": "...", "authority": "Official"|"Aggregator", "as_of": "2027"}
      ]
    }
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import _parse_iso_date, slugify  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# Per-university subsection order. deadlines/application_checklist/financial_aid are
# required (enforced in validate); the rest are optional-but-recommended.
UNI_FIELDS = [
    ("tests", "Tests"),
    ("essays", "Essays"),
    ("fees", "Application fee"),
    ("financial_aid", "Financial aid — forms, documents, dates"),
    ("application_checklist", "What to gather / do"),
]
REQUIRED_UNI_FIELDS = ("application_checklist", "financial_aid")


def validate(data):
    """Fail loudly if required top-level fields or per-university fields are missing/empty."""
    if not (data.get("region") or "").strip():
        sys.exit("ERROR: apply-prep JSON is missing required field 'region'.")
    if not (data.get("overview") or "").strip():
        sys.exit("ERROR: apply-prep JSON has an empty 'overview' — write the region apply strategy.")
    if not data.get("systems"):
        sys.exit("ERROR: apply-prep JSON has no 'systems' — group the universities by application system.")
    unis = data.get("universities") or []
    if not unis:
        sys.exit("ERROR: apply-prep JSON lists no 'universities'.")

    problems = []
    for i, u in enumerate(unis):
        name = (u.get("name") or "").strip() or f"university[{i}]"
        if not name.strip() or name == f"university[{i}]":
            problems.append(f"{name}: missing 'name'")
        if not (u.get("deadlines") or {}):
            problems.append(f"{name}: missing 'deadlines'")
        for key in REQUIRED_UNI_FIELDS:
            if not (u.get(key) or "").strip():
                problems.append(f"{name}: empty '{key}'")
    if problems:
        sys.exit(
            "ERROR: apply-prep guide is incomplete —\n  - "
            + "\n  - ".join(problems)
            + "\nEvery university needs deadlines + application_checklist + financial_aid "
            "(research them, or write 'Not found — <why>')."
        )
    if not data.get("sources"):
        sys.exit("ERROR: apply-prep guide has no sources. Every hard fact needs a citation.")


def render_deadlines(deadlines):
    labels = {"application": "Application deadline", "aid": "Financial-aid deadline"}
    lines = []
    for key, value in deadlines.items():
        if not value:
            continue
        lines.append(f"- **{labels.get(key, key.replace('_', ' ').title())}:** {value}")
    return "\n".join(lines) if lines else "- _To confirm._"


def render_snapshot(data, unis):
    systems = data.get("systems") or []
    rows = [
        ("Region", data.get("region_title") or data.get("region")),
        ("Universities", str(len(unis))),
    ]
    lines = [f"- **{label}:** {value or '—'}" for label, value in rows]
    for s in systems:
        members = ", ".join(s.get("universities") or []) or "—"
        lines.append(f"- **{s.get('system', 'System')}:** {members}")
    return "\n".join(lines)


def render_systems(data, unis_by_name):
    parts = []
    for s in data.get("systems") or []:
        system = s.get("system", "Application system")
        parts.append(f"### {system}")
        members = s.get("universities") or []
        if members:
            parts.append(f"_Universities: {', '.join(members)}._")
            parts.append("")
        shared = (s.get("shared_checklist") or "").strip()
        if shared:
            parts.append("**Filed once across these schools:**")
            parts.append(shared)
            parts.append("")
        # Per-university subsections, in the order the system lists them.
        ordered = [unis_by_name[m] for m in members if m in unis_by_name]
        # Any universities tagged with this system but not named in `universities` list.
        ordered += [u for u in data.get("universities", [])
                    if u.get("system") == system and u not in ordered]
        for u in ordered:
            heading = u.get("name", "University")
            likelihood = (u.get("admission_likelihood") or "").strip()
            if likelihood:
                heading += f" — {likelihood}"
            parts.append(f"#### {heading}")
            parts.append(render_deadlines(u.get("deadlines") or {}))
            parts.append("")
            for key, label in UNI_FIELDS:
                value = (u.get(key) or "").strip()
                if not value:
                    continue
                parts.append(f"**{label}**")
                parts.append(value)
                parts.append("")
            portal = (u.get("portal") or "").strip()
            if portal:
                parts.append(f"**Portal:** {portal}")
                parts.append("")
    return "\n".join(parts).rstrip()


def render_calendar(dated_items):
    dated = sorted(
        [(it, _parse_iso_date(it.get("date"))) for it in dated_items],
        key=lambda pair: (pair[1] is None, pair[1] or ""),
    )
    known = [(it, d) for it, d in dated if d]
    unknown = [it for it, d in dated if not d]
    lines = []
    if known:
        lines.append("| Date | What | Action |")
        lines.append("| --- | --- | --- |")
        for it, d in known:
            lines.append(f"| {d.isoformat()} | {it.get('label', '')} | {it.get('action', '')} |")
    if unknown:
        lines.append("")
        lines.append("**To confirm:**")
        for it in unknown:
            raw = f" (\"{it.get('date')}\")" if it.get("date") else ""
            lines.append(f"- {it.get('label', 'Date')} — {it.get('action', '')}{raw}")
    return "\n".join(lines) if lines else "_No dated items yet._"


def render_sources(sources):
    lines = []
    for s in sources:
        title = s.get("title") or s.get("url") or "source"
        url = s.get("url") or ""
        suffix = " — ".join(
            x for x in [s.get("authority") or "", f"as of {s['as_of']}" if s.get("as_of") else ""] if x
        )
        link = f"[{title}]({url})" if url else title
        lines.append(f"- {link}{(' — ' + suffix) if suffix else ''}")
    return "\n".join(lines)


def render_guide(data):
    unis = data.get("universities") or []
    unis_by_name = {u.get("name"): u for u in unis if u.get("name")}
    region_title = data.get("region_title") or data.get("region")

    parts = [f"# Application prep — {region_title}: {len(unis)} universities", ""]
    parts.append("## Snapshot")
    parts.append(render_snapshot(data, unis))
    parts.append("")
    parts.append(f"## {region_title} application strategy")
    parts.append(data["overview"].strip())
    parts.append("")
    parts.append("## Grouped by application system")
    parts.append(render_systems(data, unis_by_name))
    parts.append("")
    gather = (data.get("consolidated_checklist") or "").strip()
    if gather:
        parts.append("## Gather once (across the whole region)")
        parts.append(gather)
        parts.append("")
    parts.append("## Deadline calendar")
    parts.append(render_calendar(data.get("dated_items") or []))
    parts.append("")
    parts.append("## Sources")
    parts.append(render_sources(data.get("sources") or []))
    parts.append("")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(
        description="Render an action-only, per-region application-prep guide grouped by application system."
    )
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--input", required=True, help="Path to the apply-prep research JSON.")
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

    region_slug = slugify(data.get("region"))
    out_dir = student_dir / "application_prep"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{region_slug}.md"
    out_path.write_text(render_guide(data), encoding="utf-8")
    print(f"Wrote application-prep guide: {out_path}  ({len(data.get('universities') or [])} universities)")


if __name__ == "__main__":
    main()
