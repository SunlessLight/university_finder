"""
html_to_pdf.py — convert a self-contained HTML page to PDF.

Built for the sales one-pager (sales/pitch/one-pager.html), which is a fully-styled A4 page
(`@page { size: A4; margin: 0 }`, flexbox + grid). Nothing in the repo regenerated the committed
sales/pitch/one-pager.pdf; this tool does, and works for any self-contained HTML file.

Engine = WeasyPrint (real CSS: flexbox/grid, @page sizing, print colors). It's reused from
apply_prep_to_pdf.py via that tool's _load_weasyprint(), which adds the native GTK/Pango/Cairo DLL
directory on Windows before importing WeasyPrint, so this runs on this machine without a system-wide
PATH change. Rendering `filename=<input>` sets base_url to the file's own folder, so relative assets
resolve.

Usage:
    python tools/html_to_pdf.py --input sales/pitch/one-pager.html
    python tools/html_to_pdf.py --input sales/pitch/one-pager.html --output out/one-pager.pdf

    # --output is optional; it defaults to the input path with a .pdf suffix.
"""

import argparse
import sys
from pathlib import Path

from apply_prep_to_pdf import _load_weasyprint

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Convert a self-contained HTML page to PDF.")
    parser.add_argument("--input", required=True, help="Path to the source .html file.")
    parser.add_argument(
        "--output", help="Output .pdf path (default: input path with a .pdf suffix).",
    )
    args = parser.parse_args()

    html_path = Path(args.input)
    if not html_path.exists():
        sys.exit(f"ERROR: input file not found: {html_path}")

    out_path = Path(args.output) if args.output else html_path.with_suffix(".pdf")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    weasyprint = _load_weasyprint()
    weasyprint.HTML(filename=str(html_path)).write_pdf(str(out_path))
    print(f"Wrote PDF: {out_path}")


if __name__ == "__main__":
    main()
