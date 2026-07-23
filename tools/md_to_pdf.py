"""
md_to_pdf.py — manually convert a single dossier or application-prep Markdown file to PDF.

The pipeline tools (dossier_to_pdf.py, apply_prep_to_pdf.py) only take a --student slug and
render every .md inside that student's dossiers/ or application_prep/ folder, writing the PDF
beside the source. That's right for the pipeline but awkward for one-off / sales work, where the
source is a redacted copy that doesn't live in a student folder (see sales/sample_pack/README.md).

This tool converts an *arbitrary* .md file to a PDF at an *arbitrary* output path. It reuses the
exact styling and render engines from the two pipeline tools (imported, not duplicated), so a
dossier rendered here is identical to one from dossier_to_pdf.py, and likewise for apply guides.
Both now render with WeasyPrint (dossier_to_pdf migrated off xhtml2pdf 2026-07):
  - --type dossier  -> dossier_to_pdf.render_pdf (glossary + callouts) via `markdown` + WeasyPrint
  - --type apply    -> apply_prep_to_pdf's CSS + checkbox pass via `markdown` + WeasyPrint

Neither pipeline tool is modified; only their module-level constants/helpers are imported (sibling
import works because running `python tools/md_to_pdf.py` puts tools/ on sys.path).

Usage:
    python tools/md_to_pdf.py --type dossier --input path/to/dossier.md
    python tools/md_to_pdf.py --type apply --input path/to/us.md --output out/apply.pdf

    # --output is optional; it defaults to the input path with a .pdf suffix.
"""

import argparse
import sys
from pathlib import Path

import markdown

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _render_dossier(md_path, out_path):
    """Render a dossier .md exactly as dossier_to_pdf.py does, to out_path."""
    import dossier_to_pdf as dossier
    from apply_prep_to_pdf import _load_weasyprint

    weasyprint = _load_weasyprint()
    dossier.render_pdf(md_path, weasyprint, out_path=out_path)


def _render_apply(md_path, out_path):
    """Render an application-prep .md exactly as apply_prep_to_pdf.py does, to out_path."""
    import apply_prep_to_pdf as apply

    weasyprint = apply._load_weasyprint()
    text = apply._checkboxes(md_path.read_text(encoding="utf-8"))
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html"],
    )
    html = apply.HTML_TEMPLATE.format(css=apply.PAGE_CSS, body=body)
    weasyprint.HTML(string=html, base_url=str(md_path.parent)).write_pdf(str(out_path))


RENDERERS = {"dossier": _render_dossier, "apply": _render_apply}


def main():
    parser = argparse.ArgumentParser(
        description="Manually convert a dossier or application-prep Markdown file to PDF."
    )
    parser.add_argument(
        "--type", required=True, choices=RENDERERS.keys(),
        help="Which styling to use: 'dossier' or 'apply' (both render with WeasyPrint).",
    )
    parser.add_argument("--input", required=True, help="Path to the source .md file.")
    parser.add_argument(
        "--output", help="Output .pdf path (default: input path with a .pdf suffix).",
    )
    args = parser.parse_args()

    md_path = Path(args.input)
    if not md_path.exists():
        sys.exit(f"ERROR: input file not found: {md_path}")

    out_path = Path(args.output) if args.output else md_path.with_suffix(".pdf")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    RENDERERS[args.type](md_path, out_path)
    print(f"Wrote PDF: {out_path}")


if __name__ == "__main__":
    main()
