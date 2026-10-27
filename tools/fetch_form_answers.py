"""
fetch_form_answers.py — save every response to each Google Form as a local CSV.

Added 2026-10-27 (carry-over 2026-10-26-form-access). Sibling of fetch_form_questions.py:
same forms, same .env IDs, same Apps Script web app and token (action `answers` in
tools/appsscript/Code.gs). Questions are tracked in forms/; answers are personal data
(PDPA), so they go only to gitignored folders:

    intake               -> data/form/intake_answers.csv
    report_feedback      -> data/feedback/report_feedback.csv
    spreadsheet_feedback -> data/feedback/spreadsheet_feedback.csv
    survey               -> data/feedback/survey.csv

Read-only: unlike fetch_form_responses.py this never stamps `Ingested at`, and it does not
touch data/form/responses.csv (that file is the pending batch `--confirm` reads back).
The feedback paths are the ones the retired fetch_feedback.py wrote (public-CSV route, deleted
2026-10-27 so the feedback sheets can be Restricted); this is now the only feedback reader.

Usage:
    python tools/fetch_form_answers.py                       # every configured form
    python tools/fetch_form_answers.py --form survey intake  # one or more by name

Requires in .env: the same keys as fetch_form_questions.py.
"""

import argparse
import csv
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_form_questions import FORMS  # noqa: E402
from fetch_form_responses import call_endpoint, load_config  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
FORM_DIR = REPO_ROOT / "data" / "form"
FEEDBACK_DIR = REPO_ROOT / "data" / "feedback"

OUTPUTS = {
    "intake": FORM_DIR / "intake_answers.csv",
    "report_feedback": FEEDBACK_DIR / "report_feedback.csv",
    "spreadsheet_feedback": FEEDBACK_DIR / "spreadsheet_feedback.csv",
    "survey": FEEDBACK_DIR / "survey.csv",
}


def fetch_one(url, token, name):
    """Fetch one form's answers and write its CSV. Exits before writing on a bad payload."""
    form_id = os.getenv(FORMS[name], "").strip()
    if not form_id and name != "intake":
        sys.exit(f"ERROR: {FORMS[name]} is not set in .env (the ID from the form's edit address).")
    payload = call_endpoint(url, token, "answers", {"form": form_id} if form_id else None)

    headers = payload.get("headers") if isinstance(payload, dict) else None
    rows = payload.get("rows") if isinstance(payload, dict) else None
    if headers is None or rows is None:
        sys.exit("ERROR: endpoint response has no headers/rows — is the deployed Code.gs out of date?")
    # A short/long row would shift every later answer into the wrong column.
    for n, row in enumerate(rows, start=2):
        if len(row) != len(headers):
            sys.exit(f"ERROR: {name} sheet row {n} has {len(row)} cells but there are {len(headers)} headers.")

    path = OUTPUTS[name]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"{name}: {len(rows)} response(s), {len(headers)} column(s) -> {path.relative_to(REPO_ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="Save every Google Form response to a local, gitignored CSV.")
    parser.add_argument("--form", nargs="+", choices=sorted(FORMS), help="Which form(s); default: every configured one.")
    args = parser.parse_args()

    url, token = load_config()  # also loads .env for the ID lookups below
    if args.form:
        names = args.form
    else:
        names = [n for n in FORMS if n == "intake" or os.getenv(FORMS[n], "").strip()]
        skipped = [FORMS[n] for n in FORMS if n not in names]
        if skipped:
            print(f"Skipping forms with no ID in .env: {', '.join(skipped)}\n")

    for name in names:
        fetch_one(url, token, name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
