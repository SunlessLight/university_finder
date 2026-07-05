"""
compare_universities.py — side-by-side comparison tables for narrowing the list.

Reads a student's master_list.csv, selects a subset of rows (by List status or by an
explicit list of university|course pairs), and prints a Markdown comparison table with
each university as a column and the chosen decision dimensions as rows. This is the tool
the student uses to make each narrowing cut (Longlist -> Shortlist -> Finalist).

Pure CSV -> table. No API calls, no credits.

Usage:
    # compare the whole shortlist on the default decision dimensions
    python tools/compare_universities.py --student aisyah-rahman --status Shortlist

    # compare specific rows on cost + visa only
    python tools/compare_universities.py --student aisyah-rahman \
        --rows "University of Manchester|BSc Computer Science, University of Melbourne|BSc Computing" \
        --dimensions cost,visa

    # save a copy alongside the run
    python tools/compare_universities.py --student aisyah-rahman --status Finalist --dimensions all --save

Dimension presets: summary, cost, quality, fit, visa, deadline, all.
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import SHORTLIST_HEADERS, course_key  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# Each preset is an ordered list of master-list columns to show as comparison rows.
DIMENSION_PRESETS = {
    "summary": ["List status", "Desirability", "Tier", "Admission likelihood", "Warnings"],
    "cost": ["Total cost (programme)", "Approx total (MYR)", "Annual tuition", "Duration (yrs)"],
    "scholarship": ["Scholarship & portal", "Scholarship coverage", "Scholarship competitiveness",
                    "How to get the scholarship"],
    "life": ["Student community links", "Student life"],
    "quality": ["Subject rank", "Overall rank"],
    "fit": ["Student grades", "Entry requirements", "Fits grades?", "English req", "Meets English?",
            "Admission likelihood", "Backup entry route"],
    "visa": ["Money to show (visa)", "Work rights after graduating", "Recognised in Malaysia?"],
    "deadline": ["How to apply", "Key deadline", "Intake"],
}
DEFAULT_DIMENSIONS = ["summary", "cost", "scholarship", "quality", "fit", "visa", "deadline"]

# Country aliases so "--country AU" and "--country Australia" both work.
COUNTRY_ALIASES = {
    "au": "australia", "aus": "australia", "australia": "australia",
    "us": "usa", "usa": "usa", "united states": "usa", "america": "usa",
    "uk": "uk", "united kingdom": "uk", "britain": "uk",
    "sg": "singapore", "singapore": "singapore",
    "cn": "china", "china": "china",
}


def load_rows(csv_path):
    """Return master_list.csv as a list of {header: value} dicts."""
    with csv_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _country_matches(row_country, wanted):
    """True if a row's Country column matches the wanted country (alias-aware)."""
    canon = COUNTRY_ALIASES.get((row_country or "").strip().lower(), (row_country or "").strip().lower())
    return canon == wanted


def select_rows(rows, status, wanted_pairs, country=None):
    """Filter rows by explicit university|course pairs, else by List status.
    An optional country (name or alias) further narrows the set — the 'one country
    at a time' lever for working through a large list without loading it all."""
    if wanted_pairs:
        wanted = {course_key(u, c) for u, c in wanted_pairs}
        selected = [r for r in rows if course_key(r.get("University"), r.get("Course")) in wanted]
    elif status.lower() == "all":
        selected = [r for r in rows if (r.get("List status") or "") != "Rejected"]
    else:
        selected = [r for r in rows if (r.get("List status") or "").lower() == status.lower()]

    if country:
        wanted_country = COUNTRY_ALIASES.get(country.strip().lower(), country.strip().lower())
        selected = [r for r in selected if _country_matches(r.get("Country"), wanted_country)]
    return selected


def resolve_dimensions(dim_arg):
    """Turn a comma list of preset names into an ordered, de-duplicated column list."""
    names = [d.strip().lower() for d in dim_arg.split(",") if d.strip()]
    if "all" in names:
        names = list(DIMENSION_PRESETS.keys())
    columns = []
    for name in names:
        if name not in DIMENSION_PRESETS:
            valid = ", ".join(list(DIMENSION_PRESETS) + ["all"])
            sys.exit(f"ERROR: unknown dimension '{name}'. Valid: {valid}")
        for col in DIMENSION_PRESETS[name]:
            if col not in columns:
                columns.append(col)
    return columns


def _cell(value):
    """Markdown-safe cell: escape pipes, show em-dash for blanks."""
    text = (value or "").strip().replace("|", "/").replace("\n", " ")
    return text if text else "—"


def render_table(selected, columns):
    """Build the Markdown comparison table (universities as columns)."""
    labels = [f"{r.get('University','?')} — {r.get('Course','?')}" for r in selected]
    lines = []
    header = "| Dimension | " + " | ".join(_cell(l) for l in labels) + " |"
    divider = "|" + " --- |" * (len(labels) + 1)
    lines.append(header)
    lines.append(divider)
    for col in columns:
        cells = [_cell(r.get(col)) for r in selected]
        lines.append(f"| **{col}** | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def parse_pairs(rows_arg):
    """Parse 'Uni A|Course A, Uni B|Course B' into [(uni, course), ...]."""
    pairs = []
    for chunk in rows_arg.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "|" not in chunk:
            sys.exit(f"ERROR: --rows entry '{chunk}' must be 'University|Course'.")
        uni, course = chunk.split("|", 1)
        pairs.append((uni.strip(), course.strip()))
    return pairs


def main():
    parser = argparse.ArgumentParser(description="Side-by-side university comparison tables.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--status", default="Shortlist",
                        help="List status to compare (Longlist/Shortlist/Finalist/all). Default Shortlist.")
    parser.add_argument("--rows", help="Explicit 'University|Course, University|Course' pairs to compare.")
    parser.add_argument("--country", help="Narrow to one destination (name or alias: Australia/AU, USA/US, UK, Singapore/SG, China/CN).")
    parser.add_argument("--dimensions", default=",".join(DEFAULT_DIMENSIONS),
                        help="Comma list of presets: summary,cost,scholarship,life,quality,fit,visa,deadline,all.")
    parser.add_argument("--save", action="store_true", help="Also write the table to .tmp/<slug>/.")
    args = parser.parse_args()

    csv_path = STUDENTS_DIR / args.student / "master_list.csv"
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found. Run discovery (Stage 3) first.")

    rows = load_rows(csv_path)
    wanted_pairs = parse_pairs(args.rows) if args.rows else None
    selected = select_rows(rows, args.status, wanted_pairs, args.country)
    if not selected:
        scope = "rows matched" if wanted_pairs else f"rows with List status = {args.status}"
        if args.country:
            scope += f" in {args.country}"
        sys.exit(f"No {scope} in {csv_path.name}.")

    columns = resolve_dimensions(args.dimensions)

    title = f"# Comparison — {args.student}"
    subtitle = (
        f"_{len(selected)} universities · "
        f"{'explicit selection' if wanted_pairs else 'List status: ' + args.status} · "
        f"{('country: ' + args.country + ' · ') if args.country else ''}"
        f"dimensions: {args.dimensions}_\n\n"
        f"> Approx total (MYR) is a rough offline conversion for comparison only — verify exact figures in each dossier."
    )
    table = render_table(selected, columns)
    output = f"{title}\n\n{subtitle}\n\n{table}\n"

    print(output)

    if args.save:
        out_dir = REPO_ROOT / ".tmp" / args.student
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = out_dir / f"compare_{stamp}.md"
        out_path.write_text(output, encoding="utf-8")
        print(f"(saved to {out_path})")


if __name__ == "__main__":
    main()
