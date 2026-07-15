"""
apply_prep_to_pdf.py — export a rendered application-prep guide to a clean, readable PDF.

The student-facing deliverable of Stage 8 is the per-region "how to apply" guide, which
build_application_prep.py writes as Markdown to
data/students/<slug>/application_prep/<region>.md. Great for the pipeline, but a student
wants something they can open and skim. This tool converts an existing guide .md into a
document-style .pdf (title block, clickable Contents, styled "Key terms", tickable
checklists, page-number footer, A4) written alongside the .md.

It only ever *reads* the existing Markdown — no research, never touches master_list.csv.
Build first (build_application_prep.py), export on request (here). Sibling of
dossier_to_pdf.py, which does the same for dossiers.

Engine = WeasyPrint (real CSS: reliable internal links for the Contents/glossary jumps,
paged footers, proper list styling). On Windows WeasyPrint needs the native GTK/Pango/Cairo
DLLs; this script adds the MSYS2 (or a configured) DLL directory before importing it, so it
runs on this machine without a system-wide PATH change. If those libraries can't be found it
exits with instructions rather than a cryptic ctypes error.

Usage:
    python tools/apply_prep_to_pdf.py --student toru --region us
    python tools/apply_prep_to_pdf.py --student toru --all

    # --region accepts the slug with or without the .md extension.
"""

import argparse
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# Where the native GTK/Pango/Cairo DLLs live on Windows. Override with the
# WEASYPRINT_DLL_DIRECTORIES env var; otherwise we try the usual MSYS2 locations.
_DLL_CANDIDATES = [
    os.environ.get("WEASYPRINT_DLL_DIRECTORIES", ""),
    r"C:\msys64\ucrt64\bin",
    r"C:\msys64\mingw64\bin",
    r"C:\Program Files\GTK3-Runtime Win64\bin",
]


def _load_weasyprint():
    """Add the native-lib dir (Windows) then import weasyprint, or exit with help."""
    if sys.platform == "win32":
        for d in _DLL_CANDIDATES:
            if d and Path(d, "libgobject-2.0-0.dll").exists():
                os.add_dll_directory(d)
                break
    try:
        import weasyprint  # noqa: WPS433 (import inside function is intentional)
        return weasyprint
    except OSError as exc:
        sys.exit(
            "ERROR: WeasyPrint could not load its native GTK/Pango/Cairo libraries.\n"
            f"  ({exc})\n"
            "  Install them (MSYS2: `pacman -S mingw-w64-ucrt-x86_64-gtk3`) and either put the\n"
            "  bin dir on PATH or set WEASYPRINT_DLL_DIRECTORIES to it (e.g. C:\\msys64\\ucrt64\\bin)."
        )


# xhtml2pdf handled task lists as literal text; WeasyPrint needs a real glyph. Convert
# GFM task items to ballot-box glyphs before the Markdown pass (so `- [ ]` still lives in
# the .md for GitHub/VS Code, but the PDF shows a tickable box).
_TASK_OPEN = re.compile(r"^(\s*)([-*])\s+\[ \]\s+", re.MULTILINE)
_TASK_DONE = re.compile(r"^(\s*)([-*])\s+\[[xX]\]\s+", re.MULTILINE)


def _checkboxes(md_text):
    md_text = _TASK_OPEN.sub(r"\1\2 ☐ ", md_text)   # ☐
    md_text = _TASK_DONE.sub(r"\1\2 ☑ ", md_text)   # ☑
    return md_text


PAGE_CSS = """
@page {
    size: A4 portrait;
    margin: 1.9cm 1.9cm 2cm 1.9cm;
    @bottom-left  { content: string(doctitle); color: #8a97a6; font-size: 8pt; }
    @bottom-right { content: "Page " counter(page) " of " counter(pages);
                    color: #8a97a6; font-size: 8pt; }
}
body { font-family: "Segoe UI", "DejaVu Sans", Arial, sans-serif; font-size: 10.5pt;
       line-height: 1.5; color: #1a1a1a; }

/* Title block (cover header, not a full cover page — this is an action guide). */
h1 { string-set: doctitle content(); font-size: 21pt; color: #10233f; margin: 0 0 2pt 0;
     line-height: 1.12; }
h1::after { content: ""; display: block; width: 2.4cm; height: 3px;
            background: #c0392b; margin-top: 8pt; }

h2 { font-size: 14pt; color: #10233f; margin: 20pt 0 7pt 0;
     border-bottom: 1px solid #d3dbe6; padding-bottom: 3pt; }
h3 { font-size: 11.5pt; color: #123a66; margin: 14pt 0 4pt 0; }

/* h4 = a numbered university ("1. Princeton …"). Bigger, bolder; keep its title with
   the first section below it so a number never strands at a page bottom. */
h4 { font-size: 12.5pt; font-weight: 700; color: #10233f; margin: 15pt 0 5pt 0;
     break-after: avoid; break-inside: avoid; }

/* h5 = a lettered section inside a university ("a. Deadlines"). The bold, bigger
   section title the guide is built around (default h5 is tiny). */
h5 { font-size: 11pt; font-weight: 700; color: #123a66; margin: 11pt 0 3pt 0;
     break-after: avoid; }

/* Section body sits indented beneath its lettered title. */
.apply-body { padding-left: 12pt; }
.apply-body > :last-child { margin-bottom: 0; }

/* Long checklists ("Filed once", "Gather once") flow into two columns. */
.cols2 ul { column-count: 2; column-gap: 22pt; margin-top: 2pt; }
.cols2 li { break-inside: avoid; }

p { margin: 0 0 7pt 0; }
ul, ol { margin: 0 0 8pt 0; padding-left: 18pt; }
li { margin: 0 0 4pt 0; }
strong { color: #10233f; }
em { color: #333; }

/* Links = the "highlighted, tappable" jargon + Contents jumps. */
a { color: #1157b8; text-decoration: underline; }

/* The "How to use this guide" intro callout (a Markdown blockquote). */
blockquote { margin: 10pt 0 14pt 0; padding: 8pt 12pt; background: #f2f6fb;
             border-left: 3px solid #1157b8; color: #223; }
blockquote p { margin: 0 0 5pt 0; }
blockquote p:last-child { margin: 0; }

/* Contents list — compact. */
h2#toc + ul { line-height: 1.35; }

table { border-collapse: collapse; margin: 6pt 0 10pt 0; width: 100%; }
th, td { border: 0.5pt solid #b7c2d0; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background-color: #eef2f7; color: #10233f; }
code { font-family: "DejaVu Sans Mono", Consolas, monospace; font-size: 9.5pt;
       background: #f4f6f9; padding: 0 2px; }
hr { border: none; border-top: 0.5pt solid #cfd8e3; margin: 10pt 0; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{css}</style></head>
<body>{body}</body></html>"""


def render_pdf(md_path, weasyprint):
    """Convert one application-prep .md to a .pdf beside it. Returns the output Path."""
    import markdown

    text = _checkboxes(md_path.read_text(encoding="utf-8"))
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html"],
    )
    html = HTML_TEMPLATE.format(css=PAGE_CSS, body=body)

    out_path = md_path.with_suffix(".pdf")
    weasyprint.HTML(string=html, base_url=str(md_path.parent)).write_pdf(str(out_path))
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Export an application-prep guide (Markdown) to PDF.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--region", help="Region slug to convert (with or without .md), e.g. us.")
    group.add_argument("--all", action="store_true", help="Convert every region guide for this student.")
    args = parser.parse_args()

    prep_dir = STUDENTS_DIR / args.student / "application_prep"
    if not prep_dir.exists():
        sys.exit(f"ERROR: {prep_dir} not found. Run build_application_prep.py first.")

    if args.all:
        md_files = sorted(prep_dir.glob("*.md"))
        if not md_files:
            print(f"  ! No guide .md files in {prep_dir}. Nothing to convert.")
            return
    else:
        name = args.region[:-3] if args.region.endswith(".md") else args.region
        md_path = prep_dir / f"{name}.md"
        if not md_path.exists():
            sys.exit(f"ERROR: {md_path} not found. Check the region slug (list: {prep_dir}).")
        md_files = [md_path]

    weasyprint = _load_weasyprint()
    for md_path in md_files:
        out_path = render_pdf(md_path, weasyprint)
        print(f"Wrote PDF: {out_path}")


if __name__ == "__main__":
    main()
