"""
build_glossary_sheet.py — generate the master list's companion "Glossary" tab.

The master list is read in Google Sheets by an 18-year-old who has not met EAC, IGP,
COMPASS, subclass 485 or STEM OPT before. The cells themselves are written
plain-English-first (see workflows/03_discover_longlist.md), but some shorthand has to
survive because the student will meet it on the official pages — UCAS, MQA, IELTS. This
tool renders a second sheet explaining exactly the terms THAT student's list actually
uses, so nothing has to be looked up elsewhere.

It is a thin wrapper: apply_glossary.GLOSSARY is the single source of definitions and
apply_glossary.present_terms() does the filtering, both shared with the Stage 8 apply
guides. A term added for a guide shows up here for free.

Usage:
    python tools/build_glossary_sheet.py --student <slug>
    python tools/build_glossary_sheet.py --file csvs/master_list3.csv --out csvs/glossary3.csv
"""

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_glossary import GLOSSARY, present_terms  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

GLOSSARY_HEADERS = ["Term", "What it means"]


def plain(text):
    """Strip the markdown the definitions carry — a spreadsheet shows ** literally."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def csv_text(csv_path):
    """Every cell of a master list as one blob, for term detection."""
    with csv_path.open(newline="", encoding="utf-8") as f:
        return "\n".join(" ".join(row) for row in csv.reader(f))


def build_rows(text):
    """[(term, plain definition)] for the glossary terms present in `text`."""
    return [(term, plain(GLOSSARY[term]["definition"])) for term in present_terms(text)]


def write_glossary(out_path, rows):
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(GLOSSARY_HEADERS)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Build the glossary sheet for a student's master list.")
    parser.add_argument("--student", help="Student slug (folder under data/students/).")
    parser.add_argument("--file", help="Path to a master list CSV, instead of --student.")
    parser.add_argument("--out", help="Output path (default alongside the input, as glossary.csv).")
    args = parser.parse_args()

    if bool(args.student) == bool(args.file):
        sys.exit("ERROR: pass exactly one of --student or --file.")

    if args.student:
        source = STUDENTS_DIR / args.student / "master_list.csv"
        default_out = STUDENTS_DIR / args.student / "glossary.csv"
    else:
        source = Path(args.file)
        if not source.is_absolute():
            source = REPO_ROOT / source
        default_out = source.parent / "glossary.csv"

    if not source.exists():
        sys.exit(f"ERROR: {source} not found.")

    out_path = Path(args.out) if args.out else default_out
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path

    rows = build_rows(csv_text(source))
    if not rows:
        print(f"No glossary terms found in {source} — nothing written.")
        return

    write_glossary(out_path, rows)
    print(f"{len(rows)} term(s) -> {out_path}")
    print("  " + ", ".join(term for term, _ in rows))


if __name__ == "__main__":
    main()
