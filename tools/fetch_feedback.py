"""
fetch_feedback.py — pull the two feedback Google Sheets down as local CSVs.

Both sheets are shared "Anyone with the link can view", so unlike
fetch_form_responses.py (which needs an Apps Script web app + token) this just
hits Google's built-in CSV export endpoint for a Sheet:

    https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=csv

No auth, no deployment. Exports whichever tab is the sheet's first/default one.

Usage:
    python tools/fetch_feedback.py

Requires in .env:
    REPORT_FEEDBACK_URL       Sheet URL for feedback on Stage 4 university reports
    SPREEDSHEET_FEEDBACK_URL  Sheet URL for feedback on the master list spreadsheet
    (names kept exactly as set in .env)

Writes:
    data/feedback/report_feedback.csv
    data/feedback/spreadsheet_feedback.csv

data/feedback/ is gitignored — feedback rows may carry names/comments (PII),
same class as data/form/ and data/students/.
"""

import csv
import io
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
import os

REPO_ROOT = Path(__file__).resolve().parent.parent
FEEDBACK_DIR = REPO_ROOT / "data" / "feedback"
HTTP_TIMEOUT = 60

SHEETS = {
    "REPORT_FEEDBACK_URL": FEEDBACK_DIR / "report_feedback.csv",
    "SPREEDSHEET_FEEDBACK_URL": FEEDBACK_DIR / "spreadsheet_feedback.csv",
}


def sheet_id_from_url(url):
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not match:
        sys.exit(f"ERROR: could not find a sheet ID in {url!r} — is this a normal Google Sheets URL?")
    return match.group(1)


def fetch_csv(sheet_id):
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        with urllib.request.urlopen(export_url, timeout=HTTP_TIMEOUT) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        sys.exit(
            f"ERROR: sheet {sheet_id} returned HTTP {exc.code} {exc.reason}. "
            "Check it's still shared as \"Anyone with the link can view\"."
        )
    except urllib.error.URLError as exc:
        sys.exit(f"ERROR: could not reach Google Sheets ({exc.reason}).")

    text = raw.decode("utf-8-sig")
    if text.lstrip().startswith("<"):
        sys.exit(
            f"ERROR: sheet {sheet_id} returned HTML instead of CSV — usually means it's not "
            "actually shared as \"Anyone with the link can view\"."
        )
    return text


def main():
    load_dotenv(REPO_ROOT / ".env")

    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)

    for env_name, out_path in SHEETS.items():
        url = os.getenv(env_name)
        if not url:
            sys.exit(f"ERROR: {env_name} is not set in .env")

        sheet_id = sheet_id_from_url(url)
        csv_text = fetch_csv(sheet_id)
        rows = list(csv.reader(io.StringIO(csv_text)))

        out_path.write_text(csv_text, encoding="utf-8")

        header = rows[0] if rows else []
        data_rows = rows[1:] if rows else []
        print(f"{env_name}: wrote {len(data_rows)} row(s) -> {out_path.relative_to(REPO_ROOT)}")
        print(f"  columns: {header}")


if __name__ == "__main__":
    main()
