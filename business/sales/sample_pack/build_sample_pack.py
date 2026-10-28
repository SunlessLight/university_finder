"""
build_sample_pack.py — regenerate business/sales/sample_pack/ from a real, verified student's data
with identity redacted (name -> stand-in, school/family finances generalized; university
facts, fees, deadlines and aid numbers left intact, since that's the part that's real and
public). See README.md for the redaction policy and what each output file shows.

Re-run this whenever the source student's master_list.csv or reports/ change materially
(a report rebuild, a corrected fact, a re-scored row) so the sample pack stops drifting
from what the pipeline actually produces today.

Usage:
    python business/sales/sample_pack/build_sample_pack.py [--report REPORT_SLUG]

    --report defaults to the MIT report. Pass a different reports/<slug>.md name to
    regenerate the sample university-report PDF from a different finalist instead.

Also builds sample_apply-guide_US.pdf from the source student's application_prep/us.md, with
the same redaction contract as the report (explicit pairs, hard stop on a missing target).
"""

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
TOOLS_DIR = REPO_ROOT / "tools"

SOURCE_STUDENT = "toru"
STUDENT_DIR = REPO_ROOT / "data" / "students" / SOURCE_STUDENT
STAND_IN_NAME = "Arif"

# Same 15-university spread as the existing demo: a Reach cluster, a Shortlist safety net,
# a Longlist safety/match tail, and one Rejected row (shows the tool demotes bad fits, not
# just adds universities). Keeping the same set means each regeneration refreshes facts
# without re-litigating which universities to show.
# 2026-10-28 (SP1): Cambridge replaces Oxford and the first five are the bunting's demo
# picture (MIT, NUS, Monash, Cambridge, Tsinghua). Branch bunting-demo hand-edited the CSV
# to this; listing it here is what stops a rebuild from undoing it. Edit facts in the
# source student's master_list.csv, never in sample_master_list.csv.
SAMPLE_UNIVERSITIES = [
    "Massachusetts Institute of Technology",
    "National University of Singapore",
    "Monash University",
    "University of Cambridge",
    "Tsinghua University",
    "Princeton University",
    "Stanford University",
    "UNSW Sydney",
    "Harvard University",
    "Imperial College London",
    "Nanyang Technological University",
    "Rose-Hulman Institute of Technology",
    "Northeastern University",
    "University of Melbourne",
    "Carnegie Mellon University",
]

BANNER = (
    "**Sample — anonymized demo.** This is a real end-to-end search with the student's "
    "identity removed (name changed, school and personal finances generalized). It shows "
    "the format and depth you get, not a real person's private file."
)

_NAME_RE = re.compile(rf"\b{re.escape(SOURCE_STUDENT.capitalize())}\b")


def redact(text: str) -> str:
    """Swap the source student's name for the stand-in and fix the known mojibake-for-
    em-dash bug (repo-wide, unfixed as of 2026-08-20 — see research_notes.md). Cosmetic
    fix here only; does not touch the source files."""
    text = text.replace("�", "—")
    text = _NAME_RE.sub(STAND_IN_NAME, text)
    return text


def build_master_list() -> Path:
    with open(STUDENT_DIR / "master_list.csv", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        by_uni = {row["University"]: row for row in reader}

    missing = [u for u in SAMPLE_UNIVERSITIES if u not in by_uni]
    if missing:
        sys.exit(f"ERROR: universities missing from {SOURCE_STUDENT}'s master_list.csv: {missing}")

    out_path = OUT_DIR / "sample_master_list.csv"
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for uni in SAMPLE_UNIVERSITIES:
            writer.writerow({k: redact(v) for k, v in by_uni[uni].items()})
    print(f"Wrote {out_path}")
    return out_path


def build_glossary(master_list_path: Path) -> Path:
    out_path = OUT_DIR / "sample_glossary.csv"
    subprocess.run(
        [sys.executable, str(TOOLS_DIR / "build_glossary_sheet.py"),
         "--file", str(master_list_path), "--out", str(out_path)],
        check=True,
    )
    return out_path


# Redactions specific to report prose (income figure, school name in three different
# grammatical contexts). Applied after the generic redact() pass. Keeping these as
# explicit find/replace pairs (not regex) so a failed match is loud (ValueError) rather
# than silently leaving PII in a sales asset.
REPORT_TEXT_REDACTIONS = [
    ("the family income on your file is under about RM 150,000 a year, roughly USD 37,000, far below",
     "the family income on your file is in a lower-income band, far below"),
    ("You study in English at Sunway,", "You study in English at your college,"),
    ("Ask Sunway early;", "Ask your college early;"),
    ("if Sunway has no humanities", "if your college has no humanities"),
    ("Confirm Sunway can send", "Confirm your college can send"),
    ("than Bandar Sunway,", "than a Malaysian suburb,"),
    ("Not open to a Sunway College student", "Not open to a private-college student"),
]


def build_report_pdf(report_slug: str) -> Path:
    src_md = STUDENT_DIR / "reports" / f"{report_slug}.md"
    if not src_md.exists():
        sys.exit(f"ERROR: {src_md} not found.")

    text = redact(src_md.read_text(encoding="utf-8"))
    for before, after in REPORT_TEXT_REDACTIONS:
        before_r, after_r = redact(before), redact(after)
        if before_r not in text:
            sys.exit(
                f"ERROR: expected redaction target not found in {src_md.name}:\n  {before_r!r}\n"
                "The source report text has likely changed — update REPORT_TEXT_REDACTIONS."
            )
        text = text.replace(before_r, after_r)

    # Insert the banner right after the H1 title, before the first ## section.
    lines = text.splitlines()
    h2_at = next(i for i, ln in enumerate(lines) if ln.startswith("## "))
    text = "\n".join(lines[:h2_at] + [BANNER, ""] + lines[h2_at:])

    tmp_md = OUT_DIR / ".sample_report_redacted.md"
    tmp_md.write_text(text, encoding="utf-8")
    try:
        out_pdf = OUT_DIR / "sample_university-report_MIT.pdf"
        subprocess.run(
            [sys.executable, str(TOOLS_DIR / "md_to_pdf.py"),
             "--type", "report", "--input", str(tmp_md), "--output", str(out_pdf)],
            check=True,
        )
    finally:
        tmp_md.unlink(missing_ok=True)
    print(f"Wrote {out_pdf}")
    return out_pdf


# Same contract as REPORT_TEXT_REDACTIONS, for the apply guide's prose.
APPLY_TEXT_REDACTIONS = [
    ("On the income in your file (under about RM 150,000 a year, roughly USD 37,000) you sit",
     "On the income in your file (a lower-income band) you sit"),
    ("your Sunway counselor", "your college counselor"),
    ("Have Sunway send", "Have your college send"),
    ("with Sunway for February", "with your college for February"),
    ("Ask a Sunway teacher", "Ask a teacher"),
    ("**Sunway official transcript**", "**Official transcript**"),
    ("Ask Sunway to send it", "Ask your college to send it"),
]


def build_apply_guide_pdf(region: str = "us") -> Path:
    src_md = STUDENT_DIR / "application_prep" / f"{region}.md"
    if not src_md.exists():
        sys.exit(f"ERROR: {src_md} not found.")

    text = redact(src_md.read_text(encoding="utf-8"))
    for before, after in APPLY_TEXT_REDACTIONS:
        before_r, after_r = redact(before), redact(after)
        if before_r not in text:
            sys.exit(
                f"ERROR: expected redaction target not found in {src_md.name}:\n  {before_r!r}\n"
                "The source guide text has likely changed — update APPLY_TEXT_REDACTIONS."
            )
        text = text.replace(before_r, after_r)

    # The guide opens with a "How to use this guide" block, so the banner goes right under the title.
    lines = text.splitlines()
    h1_at = next(i for i, ln in enumerate(lines) if ln.startswith("# "))
    text = "\n".join(lines[:h1_at + 1] + ["", BANNER, ""] + lines[h1_at + 1:])

    tmp_md = OUT_DIR / ".sample_apply_redacted.md"
    tmp_md.write_text(text, encoding="utf-8")
    try:
        out_pdf = OUT_DIR / f"sample_apply-guide_{region.upper()}.pdf"
        subprocess.run(
            [sys.executable, str(TOOLS_DIR / "md_to_pdf.py"),
             "--type", "apply", "--input", str(tmp_md), "--output", str(out_pdf)],
            check=True,
        )
    finally:
        tmp_md.unlink(missing_ok=True)
    print(f"Wrote {out_pdf}")
    return out_pdf


def scan_for_leaks(*paths: Path) -> None:
    """Same check the README promises: zero hits for the name/school/income figures."""
    needles = [SOURCE_STUDENT.capitalize(), "Sunway", "RM 150,000", "USD 32,000",
               # The 2026-10 rebuilds state the income at USD 4.04. Grades stay by policy (README).
               "USD 37,000", "37,000 a year", "RM 150k"]
    hits = []
    for path in paths:
        blob = path.read_bytes().decode("utf-8", errors="ignore") if path.suffix != ".pdf" else None
        if blob is None:
            from pypdf import PdfReader
            blob = "\n".join(p.extract_text() for p in PdfReader(str(path)).pages)
        for needle in needles:
            if needle in blob:
                hits.append((path.name, needle))
    if hits:
        sys.exit(f"ERROR: redaction leak(s) found: {hits}")
    print("Scan clean: zero hits for name / school / income figures.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="massachusetts-institute-of-technology",
                         help="Report slug under reports/ to render as the sample PDF.")
    args = parser.parse_args()

    csv_path = build_master_list()
    glossary_path = build_glossary(csv_path)
    pdf_path = build_report_pdf(args.report)
    apply_path = build_apply_guide_pdf()
    scan_for_leaks(csv_path, glossary_path, pdf_path, apply_path)


if __name__ == "__main__":
    main()
