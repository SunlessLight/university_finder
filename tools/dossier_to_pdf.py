"""
dossier_to_pdf.py — export a rendered dossier Markdown file to a clean, readable PDF.

The student-facing deliverable of Stage 5a is the per-finalist dossier, which
build_dossier.py writes as Markdown to data/students/<slug>/dossiers/<uni>.md. That's
great for the pipeline but awkward to hand to a student. This tool converts an existing
dossier .md into a document-style .pdf (styled headings/tables/lists/links, A4 margins,
footer page numbers) written alongside the .md, so a student who asks for their dossiers
gets something they can open and skim directly.

It only ever *reads* the existing Markdown — it does no research and never touches
master_list.csv. Build first (build_dossier.py), export on request (here).

Uses `markdown` (md -> HTML) + `xhtml2pdf` (HTML -> PDF). Both are pure-pip with no native
libraries, so this runs on Windows out of the box (pip install -r requirements.txt).

Usage:
    python tools/dossier_to_pdf.py --student aisyah-rahman --dossier manchester-cs
    python tools/dossier_to_pdf.py --student aisyah-rahman --all

    # --dossier accepts the slug with or without the .md extension.
"""

import argparse
import sys
from pathlib import Path

import markdown
from xhtml2pdf import pisa

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# xhtml2pdf's CSS is limited (no flexbox/grid) — stick to block/table/margins/borders/
# colors, which is all a document needs. The @frame footer + <pdf:pagenumber> is
# xhtml2pdf-specific syntax for page numbering.
PAGE_CSS = """
@page {
    size: A4 portrait;
    margin: 2cm 2cm 2.4cm 2cm;
    @frame footer {
        -pdf-frame-content: footerContent;
        bottom: 1.2cm; left: 2cm; right: 2cm; height: 1cm;
    }
}
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 19pt; color: #10233f; margin: 0 0 12pt 0; border-bottom: 2px solid #10233f; padding-bottom: 4pt; }
h2 { font-size: 13.5pt; color: #123a66; margin: 16pt 0 6pt 0; border-bottom: 1px solid #cfd8e3; padding-bottom: 2pt; }
h3 { font-size: 11.5pt; color: #123a66; margin: 12pt 0 4pt 0; }
p { margin: 0 0 7pt 0; }
ul, ol { margin: 0 0 8pt 0; padding-left: 16pt; }
li { margin: 0 0 3pt 0; }
a { color: #1157b8; text-decoration: underline; }
strong { color: #10233f; }
table { -pdf-keep-with-next: true; border-collapse: collapse; margin: 6pt 0 10pt 0; width: 100%; }
th, td { border: 0.5pt solid #b7c2d0; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background-color: #eef2f7; color: #10233f; }
pre, code { font-family: Courier, monospace; font-size: 9.5pt; background-color: #f4f6f9; }
pre { padding: 6pt; border: 0.5pt solid #dde3ea; }
hr { border: none; border-top: 0.5pt solid #cfd8e3; margin: 10pt 0; }
#footerContent { color: #8a97a6; font-size: 8.5pt; text-align: center; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{css}</style></head>
<body>
{body}
<div id="footerContent">Page <pdf:pagenumber /> of <pdf:pagecount /></div>
</body>
</html>"""


def render_pdf(md_path):
    """Convert one dossier .md to a .pdf beside it. Returns the output Path."""
    text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    html = HTML_TEMPLATE.format(css=PAGE_CSS, body=body)

    out_path = md_path.with_suffix(".pdf")
    with out_path.open("w+b") as f:
        status = pisa.CreatePDF(html, dest=f, encoding="utf-8")
    if status.err:
        sys.exit(f"ERROR: PDF rendering failed for {md_path.name} ({status.err} error(s)).")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Export a dossier Markdown file to PDF.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dossier", help="Dossier slug to convert (with or without .md).")
    group.add_argument("--all", action="store_true", help="Convert every dossier for this student.")
    args = parser.parse_args()

    dossiers_dir = STUDENTS_DIR / args.student / "dossiers"
    if not dossiers_dir.exists():
        sys.exit(f"ERROR: {dossiers_dir} not found. Run build_dossier.py first.")

    if args.all:
        md_files = sorted(dossiers_dir.glob("*.md"))
        if not md_files:
            print(f"  ! No dossier .md files in {dossiers_dir}. Nothing to convert.")
            return
    else:
        name = args.dossier[:-3] if args.dossier.endswith(".md") else args.dossier
        md_path = dossiers_dir / f"{name}.md"
        if not md_path.exists():
            sys.exit(f"ERROR: {md_path} not found. Check the dossier slug (list: {dossiers_dir}).")
        md_files = [md_path]

    for md_path in md_files:
        out_path = render_pdf(md_path)
        print(f"Wrote PDF: {out_path}")


if __name__ == "__main__":
    main()
