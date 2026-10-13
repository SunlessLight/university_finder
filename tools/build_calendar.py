"""
build_calendar.py — aggregate every deadline across a student's finalists into one
chronological calendar.

Reads the finalist rows in master_list.csv (persistent) for application deadlines and
intakes, plus each report's structured "dated_items" list (scholarship deadlines,
admissions-test dates, visa lead times). Renders a single chronological
data/students/<slug>/calendar.md so nothing gets missed.

Where dated_items come from, in this order:
  1. data/students/<slug>/dated_items/*.json — the permanent copy build_report.py saves
     per report (since 2026-10-13).
  2. .tmp/<slug>/report_*.json and uni_*.json — the report research JSONs themselves,
     for reports built before that. .tmp/ is disposable, so this half disappears on a
     cleanup; --rescue-dates copies it into (1) while it still exists. A report found
     in both is read from (1) only.

A course report is matched to a row by University+Course. A US whole-university report
(uni_*.json, --mode university) has no course and is matched by university name alone,
the same rule flip_finalists.py uses for its marker.

It will not write a calendar with FEWER items over an existing one unless --allow-shrink
is passed: data/students/ is gitignored, so an overwrite has no undo, and a calendar
rebuilt after .tmp/ was cleaned used to silently lose every report date (78 -> 17 items
for one student).

Read-only/derived — it documents deadlines, it does NOT track submission state
(consistent with "research + how-to-apply mechanics only").

Usage:
    python tools/build_calendar.py --student <slug>
    python tools/build_calendar.py --student <slug> --status Finalist
    python tools/build_calendar.py --student <slug> --rescue-dates   # no calendar written
    python tools/build_calendar.py --student <slug> --allow-shrink

Structured dates in a report JSON (the shape build_report.py documents and saves):
    "dated_items": [
      {"date": "2027-01-15", "label": "UCAS deadline", "action": "Submit application"},
      {"date": "2026-11-01", "label": "Scholarship X deadline", "action": "Apply separately"}
    ]
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_report import DATED_ITEMS_DIRNAME, save_dated_items  # noqa: E402
from shortlist_schema import _parse_iso_date, canonical_uni, course_key, slugify  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"


def load_finalists(csv_path, status):
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows if (r.get("List status") or "").lower() == status.lower()]


def items_from_master(finalists):
    """One application-deadline item per finalist row that has a parseable date."""
    items = []
    for r in finalists:
        uni = f"{r.get('University','?')} — {r.get('Course','?')}"
        d = _parse_iso_date(r.get("Key deadline"))
        system = r.get("How to apply") or "the application portal"
        items.append({
            "date": d,
            "raw": r.get("Key deadline") or "",
            "label": "Application deadline",
            "uni": uni,
            "action": f"Submit via {system}",
        })
    return items


def _read_dated_json(path):
    """A report/dates JSON as a dict, or None if it has no usable dated_items.

    .tmp/<slug>/ holds other things under the same file names (some uni_*.json are plain
    lists of notes), so anything that is not an object with a non-empty dated_items list
    is skipped, not an error.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict):
        return None
    items = data.get("dated_items")
    if not isinstance(items, list) or not any(isinstance(it, dict) for it in items):
        return None
    return data


def _is_whole_university(data):
    """True for a US whole-university report: it names no course."""
    return data.get("mode") == "university" or not (data.get("course") or "").strip()


def _report_key(data):
    """Identity of the report a dated_items list belongs to (same keys flip_finalists uses)."""
    if _is_whole_university(data):
        return (canonical_uni(data.get("university")), None)
    return course_key(data.get("university"), data.get("course"))


def dated_sources(slug):
    """[(data, origin, path)] for every report with dated_items, one entry per report.

    origin is "saved" (the student's permanent dated_items/ folder) or "scratch" (.tmp/).
    Saved files are read first and win: a report present in both is not counted twice.
    """
    saved_dir = STUDENTS_DIR / slug / DATED_ITEMS_DIRNAME
    scratch_dir = REPO_ROOT / ".tmp" / slug
    candidates = []
    if saved_dir.exists():
        candidates += [(p, "saved") for p in sorted(saved_dir.glob("*.json"))]
    if scratch_dir.exists():
        for pattern in ("report_*.json", "uni_*.json"):
            candidates += [(p, "scratch") for p in sorted(scratch_dir.glob(pattern))]

    sources, seen = [], set()
    for path, origin in candidates:
        data = _read_dated_json(path)
        if data is None:
            continue
        key = _report_key(data)
        if key in seen:
            continue
        seen.add(key)
        sources.append((data, origin, path))
    return sources


def items_from_reports(slug, finalists):
    """
    Pull structured dated_items for the reports that belong to the selected rows.

    Scoped to `finalists` on purpose: a dated_items file exists for every university
    ever researched, so an unscoped sweep put Rejected and Shortlist-only universities'
    deadlines into a Finalist calendar — `--status` filtered the master-list half and
    silently not this one.
    """
    wanted_courses = {course_key(r.get("University"), r.get("Course")) for r in finalists}
    wanted_unis = {canonical_uni(r.get("University")) for r in finalists}
    items = []
    for data, origin, _path in dated_sources(slug):
        if _is_whole_university(data):
            # One report speaks for every course row of that university, so its dates are
            # listed once, under the university's name.
            if canonical_uni(data.get("university")) not in wanted_unis:
                continue
            uni = data.get("university") or "?"
        else:
            if course_key(data.get("university"), data.get("course")) not in wanted_courses:
                continue
            uni = f"{data.get('university','?')} — {data.get('course','?')}"
        for it in data["dated_items"]:
            if not isinstance(it, dict):
                continue
            items.append({
                "date": _parse_iso_date(it.get("date")),
                "raw": it.get("date") or "",
                # "item" is the name build_report.py's header wrongly documented until
                # 2026-10-13; JSONs written from it must not show up as a nameless "Date".
                "label": it.get("label") or it.get("item") or "Date",
                "uni": uni,
                "action": it.get("action") or "",
                "origin": origin,
            })
    return items


def rescue_scratch_dates(slug):
    """Copy dated_items still sitting only in .tmp/<slug>/ into the student's folder.

    Covers every report in scratch, whatever its row's List status (the calendar scopes
    at read time). Never overwrites a saved file. Returns the paths written.
    """
    written = []
    for data, origin, path in dated_sources(slug):
        if origin != "scratch":
            continue
        if not (data.get("university") or "").strip():
            print(f"  skipped {path.name}: no university name")
            continue
        if _is_whole_university(data):
            mode, default_slug = "university", slugify(data["university"])
        else:
            mode, default_slug = "course", slugify(f"{data['university']} {data['course']}")
        try:
            out = save_dated_items(STUDENTS_DIR / slug, data.get("slug") or default_slug,
                                   data, mode, overwrite=False)
        except SystemExit as e:
            print(f"  skipped {path.name}: {e}")
            continue
        if out:
            written.append(out)
            print(f"  saved {out.name} ({len(data['dated_items'])} dated item(s)) from {path.name}")
    return written


def count_calendar_items(text):
    """How many items a rendered calendar.md holds: dated table rows + undated bullets."""
    lines = text.splitlines()
    dated = sum(1 for ln in lines if re.match(r"\|\s*\d{4}-\d{2}-\d{2}\s*\|", ln))
    undated = sum(1 for ln in lines if ln.startswith("- **"))
    return dated + undated


def render_calendar(slug, status, items):
    dated = sorted([i for i in items if i["date"]], key=lambda i: i["date"])
    undated = [i for i in items if not i["date"]]

    lines = [f"# Application calendar — {slug}", "",
             f"_All dated items across {status} universities, in chronological order._", ""]
    if dated:
        lines.append("| Date | What | University | Action |")
        lines.append("| --- | --- | --- | --- |")
        for i in dated:
            lines.append(f"| {i['date'].isoformat()} | {i['label']} | {i['uni']} | {i['action']} |")
    else:
        lines.append("_No dated items found yet._")
    if undated:
        lines.append("")
        lines.append("## Undated / to confirm")
        for i in undated:
            raw = f" (\"{i['raw']}\")" if i["raw"] else ""
            lines.append(f"- **{i['label']}** — {i['uni']}: {i['action']}{raw}")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Build a chronological deadline calendar for a student.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--status", default="Finalist", help="List status to include (default Finalist).")
    parser.add_argument(
        "--rescue-dates", action="store_true",
        help="Copy dated_items that exist only in .tmp/<slug>/ into the student's dated_items/ "
             "folder, then stop. Writes no calendar and overwrites nothing.",
    )
    parser.add_argument(
        "--allow-shrink", action="store_true",
        help="Write the calendar even if it has fewer items than the calendar.md already there.",
    )
    args = parser.parse_args()

    student_dir = STUDENTS_DIR / args.student
    if args.rescue_dates:
        if not student_dir.exists():
            sys.exit(f"ERROR: {student_dir} not found.")
        written = rescue_scratch_dates(args.student)
        print(f"Rescued {len(written)} report(s)' dated items into {student_dir / DATED_ITEMS_DIRNAME}.")
        return

    csv_path = student_dir / "master_list.csv"
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found. Build the shortlist first.")

    finalists = load_finalists(csv_path, args.status)
    if not finalists:
        sys.exit(f"No rows with List status = {args.status} in {csv_path.name}.")

    items = items_from_master(finalists) + items_from_reports(args.student, finalists)
    out_path = student_dir / "calendar.md"
    text = render_calendar(args.student, args.status, items)

    if out_path.exists() and not args.allow_shrink:
        old_count = count_calendar_items(out_path.read_text(encoding="utf-8"))
        if len(items) < old_count:
            sys.exit(
                f"REFUSED: {out_path} holds {old_count} item(s) and this rebuild would replace it "
                f"with {len(items)}. Nothing was written.\n"
                f"The usual cause: the report dates were only in .tmp/{args.student}/ and that folder "
                f"was cleaned, so only the master_list.csv deadlines are left. The existing calendar "
                f"is then the only copy of those dates, and data/students/ has no undo.\n"
                f"If the shorter calendar is what you want (e.g. finalists were dropped), copy "
                f"calendar.md somewhere safe and re-run with --allow-shrink."
            )

    out_path.write_text(text, encoding="utf-8")

    dated = sum(1 for i in items if i["date"])
    print(f"Wrote {out_path} — {dated} dated item(s), {len(items) - dated} undated, across {len(finalists)} {args.status}.")
    if any(i.get("origin") == "scratch" for i in items):
        print(
            f"NOTE: some of these dates exist only in .tmp/{args.student}/, which is disposable. "
            f"Keep them:  python tools/build_calendar.py --student {args.student} --rescue-dates"
        )


if __name__ == "__main__":
    main()
