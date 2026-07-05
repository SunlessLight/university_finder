"""
build_calendar.py — aggregate every deadline across a student's finalists into one
chronological calendar.

Reads the finalist rows in master_list.csv (persistent) for application deadlines and
intakes, plus any .tmp/<slug>/dossier_*.json files that carry a structured "dated_items"
list (scholarship deadlines, admissions-test dates, visa lead times). Renders a single
chronological data/students/<slug>/calendar.md so nothing gets missed.

Read-only/derived — it documents deadlines, it does NOT track submission state
(consistent with "research + how-to-apply mechanics only").

Usage:
    python tools/build_calendar.py --student aisyah-rahman
    python tools/build_calendar.py --student aisyah-rahman --status Finalist

Optional structured dates in a dossier JSON:
    "dated_items": [
      {"date": "2027-01-15", "label": "UCAS deadline", "action": "Submit application"},
      {"date": "2026-11-01", "label": "Scholarship X deadline", "action": "Apply separately"}
    ]
"""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import _parse_iso_date  # noqa: E402

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


def items_from_dossiers(slug, finalist_unis):
    """Pull structured dated_items from any .tmp/<slug>/dossier_*.json present."""
    items = []
    tmp_dir = REPO_ROOT / ".tmp" / slug
    if not tmp_dir.exists():
        return items
    for jpath in sorted(tmp_dir.glob("dossier_*.json")):
        try:
            data = json.loads(jpath.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        uni = f"{data.get('university','?')} — {data.get('course','?')}"
        for it in data.get("dated_items", []) or []:
            items.append({
                "date": _parse_iso_date(it.get("date")),
                "raw": it.get("date") or "",
                "label": it.get("label") or "Date",
                "uni": uni,
                "action": it.get("action") or "",
            })
    return items


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
    args = parser.parse_args()

    student_dir = STUDENTS_DIR / args.student
    csv_path = student_dir / "master_list.csv"
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found. Build the shortlist first.")

    finalists = load_finalists(csv_path, args.status)
    if not finalists:
        sys.exit(f"No rows with List status = {args.status} in {csv_path.name}.")

    items = items_from_master(finalists) + items_from_dossiers(args.student, finalists)
    out_path = student_dir / "calendar.md"
    out_path.write_text(render_calendar(args.student, args.status, items), encoding="utf-8")

    dated = sum(1 for i in items if i["date"])
    print(f"Wrote {out_path} — {dated} dated item(s), {len(items) - dated} undated, across {len(finalists)} {args.status}.")


if __name__ == "__main__":
    main()
