"""
dossier_to_pdf.py — export a rendered dossier Markdown file to a clean, readable PDF.

The student-facing deliverable of Stage 5a is the per-finalist dossier, which
build_dossier.py writes as Markdown to data/students/<slug>/dossiers/<uni>.md. That's
great for the pipeline but awkward to hand to a student. This tool converts an existing
dossier .md into a document-style .pdf (styled headings/tables/lists/links, a warning
callout for make-or-break rules, tickable checklists, an auto-linked "Key terms"
glossary, A4 margins, footer page numbers) written alongside the .md, so a student who
asks for their dossiers gets something they can open and skim directly.

It only ever *reads* the existing Markdown — it does no research and never touches
master_list.csv. Build first (build_dossier.py), export on request (here). Sibling of
apply_prep_to_pdf.py, which does the same for the application-prep guides.

Engine = WeasyPrint (real CSS: styled callouts, reliable internal links for the glossary
jumps, paged footers, proper table/list styling). On Windows WeasyPrint needs native
GTK/Pango/Cairo DLLs; we reuse apply_prep_to_pdf's _load_weasyprint(), which adds the DLL
directory before importing it, so this runs on this machine without a system-wide PATH
change. Migrated off xhtml2pdf (2026-07) so both PDF pipelines share one capable engine.

Two readability passes run before the Markdown->HTML step, both reused from siblings:
  * apply_prep_to_pdf._checkboxes()  — turn GFM `- [ ]` task items into tickable glyphs.
  * apply_glossary                    — build a "Key terms" block from the acronyms the
    dossier actually uses, insert it after the Snapshot, and link each term's first use
    per section to it (so a student can tap MAE / OPT / MQA / CSS Profile to see it).

Usage:
    python tools/dossier_to_pdf.py --student aisyah-rahman --dossier manchester-cs
    python tools/dossier_to_pdf.py --student aisyah-rahman --all

    # --dossier accepts the slug with or without the .md extension.
"""

import argparse
import sys
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_glossary  # noqa: E402
from apply_prep_to_pdf import _checkboxes, _load_weasyprint  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# WeasyPrint gives us real CSS. Navy dossier palette kept; the load-bearing additions vs
# the old xhtml2pdf sheet are: a paged footer via counter(page), a red *warning callout*
# (blockquotes are reserved for make-or-break rules — see workflows/05), and tables that
# actually render. Markdown extensions attr_list + md_in_html let a section drop a
# `<div class="callout-note">` when it needs a softer aside.
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

h1 { string-set: doctitle content(); font-size: 20pt; color: #10233f; margin: 0 0 12pt 0;
     border-bottom: 2px solid #10233f; padding-bottom: 5pt; line-height: 1.15; }
h2 { font-size: 13.5pt; color: #123a66; margin: 17pt 0 6pt 0;
     border-bottom: 1px solid #cfd8e3; padding-bottom: 2pt; break-after: avoid; }
h3 { font-size: 11.5pt; color: #123a66; margin: 12pt 0 4pt 0; break-after: avoid; }

p { margin: 0 0 7pt 0; }
ul, ol { margin: 0 0 8pt 0; padding-left: 18pt; }
li { margin: 0 0 4pt 0; }
a { color: #1157b8; text-decoration: underline; }
strong { color: #10233f; }
em { color: #333; }

/* Warning / critical callout — the one make-or-break rule (e.g. "request aid at
   application or be barred forever") must be unmissable. workflows/05 reserves
   blockquotes for these. */
blockquote { margin: 10pt 0 12pt 0; padding: 8pt 12pt; background: #fdecea;
             border-left: 4px solid #c0392b; color: #611a15; break-inside: avoid; }
blockquote p { margin: 0 0 5pt 0; }
blockquote p:last-child { margin: 0; }

/* Softer neutral aside when a section wants a note rather than a warning:
   <div class="callout-note" markdown="1"> ... </div> */
.callout-note { margin: 10pt 0 12pt 0; padding: 8pt 12pt; background: #f2f6fb;
                border-left: 4px solid #1157b8; color: #223; break-inside: avoid; }
.callout-note > :last-child { margin-bottom: 0; }

table { border-collapse: collapse; margin: 6pt 0 10pt 0; width: 100%; }
th, td { border: 0.5pt solid #b7c2d0; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background-color: #eef2f7; color: #10233f; }
/* Snapshot fact table: the first column is a shaded label so it reads as a key-value card. */
table td:first-child { background-color: #f6f8fb; white-space: nowrap; }

/* Long checklists can flow into two columns with <div class="cols2" markdown="1">. */
.cols2 ul { column-count: 2; column-gap: 22pt; margin-top: 2pt; }
.cols2 li { break-inside: avoid; }

code { font-family: "DejaVu Sans Mono", Consolas, monospace; font-size: 9.5pt;
       background: #f4f6f9; padding: 0 2px; }
pre { padding: 6pt; border: 0.5pt solid #dde3ea; background: #f4f6f9; }
hr { border: none; border-top: 0.5pt solid #cfd8e3; margin: 10pt 0; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{css}</style></head>
<body>{body}</body></html>"""

MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html"]


def _insert_key_terms(text, block):
    """Insert the 'Key terms' glossary block right after the Snapshot section — i.e.
    before the *second* level-2 heading (`## 2. ...`; the first is `## 1. Snapshot`).
    Falls back to appending if the document has fewer than two `##` headings."""
    if not block.strip():
        return text
    lines = text.splitlines()
    h2_idxs = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    if len(h2_idxs) < 2:
        return text + "\n\n" + block
    at = h2_idxs[1]
    return "\n".join(lines[:at] + [block, ""] + lines[at:])


def _prepare_markdown(text):
    """Run the readability passes on the raw dossier Markdown, returning the final
    Markdown string to hand to the HTML renderer. Glossary terms are detected from the
    raw text (so the 'Key terms' list matches what's used), jargon in the body is linked
    to those anchors, then the Key terms block is dropped in after the Snapshot."""
    text = _checkboxes(text)
    glossary_md = apply_glossary.build_glossary_section(text, title="Key terms")
    linked = apply_glossary.link_terms(text)
    return _insert_key_terms(linked, glossary_md)


def render_pdf(md_path, weasyprint, out_path=None):
    """Convert one dossier .md to a .pdf (beside it by default). Returns the output Path.

    `weasyprint` is the loaded module (load once in the caller). `out_path` lets the
    manual/sales path (md_to_pdf.py) write to an arbitrary location; the pipeline leaves
    it None to write <slug>.pdf next to the source."""
    text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(_prepare_markdown(text), extensions=MD_EXTENSIONS)
    html = HTML_TEMPLATE.format(css=PAGE_CSS, body=body)

    out_path = out_path or md_path.with_suffix(".pdf")
    weasyprint.HTML(string=html, base_url=str(md_path.parent)).write_pdf(str(out_path))
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

    weasyprint = _load_weasyprint()
    for md_path in md_files:
        out_path = render_pdf(md_path, weasyprint)
        print(f"Wrote PDF: {out_path}")


if __name__ == "__main__":
    main()
