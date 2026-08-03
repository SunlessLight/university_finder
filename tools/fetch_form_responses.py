"""
fetch_form_responses.py — pull pending Google Form responses straight from the sheet.

Replaces the manual Stage 1 chore (Form -> Responses -> Download responses (.csv)
-> rename -> move into data/form/) with one command, and adds an explicit
"already ingested" marker so a respondent is never handed back twice.

The marker lives IN THE RESPONSES SPREADSHEET, in a column called `Ingested at`
(blank = pending, timestamp = already turned into a data/students/<slug>/ folder).
Keeping it there rather than on disk means it survives a wiped data/ folder and a
different machine. The Apps Script that serves it is tools/appsscript/Code.gs.

Usage:
    # pull everything not yet ingested -> data/form/responses.csv
    python tools/fetch_form_responses.py

    # see what's pending without writing anything
    python tools/fetch_form_responses.py --dry-run

    # AFTER ingest_form_csv.py succeeded: stamp those rows as done in the sheet
    python tools/fetch_form_responses.py --confirm

Order matters: --confirm runs LAST, only once ingest has actually created the
student folders. A crashed ingest leaves the rows pending, so re-running the
fetch simply hands them back.

Row identity is the SHEET ROW NUMBER, carried in a trailing `_row` column that
this tool appends to the CSV. It only has to hold between a fetch and its
--confirm. Forms appends responses and never reorders them, so this is safe —
but SORTING THE RESPONSES SHEET BY HAND WOULD BREAK IT.

`_row` and `Ingested at` are inert to ingest_form_csv.py: it matches headers by
substring against QUESTION_MAP, and neither name matches anything. That is why
that tool needs no changes and the manual-export path still works as a fallback.

Requires in .env (see README, "Setup (first time)"):
    FORM_WEBAPP_URL    the Apps Script web app /exec URL
    FORM_WEBAPP_TOKEN  the shared secret, same value as the FORM_TOKEN script property

data/form/ is gitignored (PII), same class as data/students/.
"""

import argparse
import csv
import json
import sys
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
FORM_DIR = REPO_ROOT / "data" / "form"
RESPONSES_CSV = FORM_DIR / "responses.csv"

# Trailing bookkeeping column this tool adds to the CSV. Must match nothing in
# ingest_form_csv.py's QUESTION_MAP (verified — see the module docstring).
ROW_COLUMN = "_row"

# Header of the marker column in the sheet. Kept here only so the two sides of
# the contract are greppable together; Code.gs STRIPS this column from the
# payload, so this tool never actually receives it.
INGESTED_HEADER = "Ingested at"

# Apps Script deployed as "Anyone" answers with a 302 to googleusercontent.com.
# urllib follows that fine for GET — which is exactly why Code.gs has no doPost().
HTTP_TIMEOUT = 60

# Error codes Code.gs can return, mapped to something actionable. Anything not
# listed here still surfaces verbatim rather than being swallowed.
ERROR_HELP = {
    "unauthorized": (
        "the endpoint rejected the token. FORM_WEBAPP_TOKEN in .env must match the "
        "FORM_TOKEN script property exactly (Apps Script -> Project Settings -> Script Properties)."
    ),
    "server_misconfigured": (
        "the Apps Script project has no FORM_TOKEN script property set. "
        "Add it under Project Settings -> Script Properties (scroll to the bottom) and save. "
        "No redeploy needed — script properties are read at request time."
    ),
    "unknown_action": "the endpoint did not recognise the action — is the deployed Code.gs out of date?",
    "script_error": "the Apps Script threw. Check the execution log in the Apps Script editor.",
    "no_rows": "confirm was called without a usable row list (no _row values were sent).",
}


def load_config():
    """Read the endpoint URL + token from .env, or exit with a clear message."""
    load_dotenv(REPO_ROOT / ".env")
    url = os.getenv("FORM_WEBAPP_URL")
    token = os.getenv("FORM_WEBAPP_TOKEN")
    if not url:
        sys.exit("ERROR: FORM_WEBAPP_URL is not set in .env")
    if not token:
        sys.exit("ERROR: FORM_WEBAPP_TOKEN is not set in .env")
    return url, token


def call_endpoint(url, token, action, extra=None):
    """
    GET the web app and return the decoded JSON payload.

    Everything is GET on purpose (see the header comment in Code.gs). Any failure
    here exits non-zero BEFORE anything is written, so a broken call can never
    leave a half-written responses.csv behind.
    """
    params = {"token": token, "action": action}
    if extra:
        params.update(extra)
    full_url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(full_url, timeout=HTTP_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        sys.exit(f"ERROR: endpoint returned HTTP {exc.code} {exc.reason}. Is the deployment still live?")
    except urllib.error.URLError as exc:
        sys.exit(f"ERROR: could not reach the endpoint ({exc.reason}). Check FORM_WEBAPP_URL and your connection.")
    except TimeoutError:
        sys.exit(f"ERROR: the endpoint did not respond within {HTTP_TIMEOUT}s.")

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        # Apps Script serves an HTML error page when the deployment is wrong
        # (not deployed as "Anyone", or a stale /dev URL that demands a login).
        sys.exit(
            "ERROR: the endpoint returned something that isn't JSON — usually a Google login page.\n"
            "       Redeploy as: type Web app, Execute as Me, Who has access Anyone, and use the /exec URL.\n"
            f"       First 200 chars: {raw[:200]!r}"
        )

    if isinstance(payload, dict) and payload.get("error"):
        code = payload["error"]
        detail = payload.get("detail")
        message = ERROR_HELP.get(code, "unrecognised error from the endpoint.")
        sys.exit(f"ERROR: {code} — {message}" + (f"\n       detail: {detail}" if detail else ""))

    return payload


def label_columns(headers):
    """
    Indices of the best name / email columns, for the human-readable summary only.

    Deliberately a local substring scan rather than importing QUESTION_MAP: this
    is eyeball output, and it must not start failing because the mapping moved.
    """
    name_idx = email_idx = None
    for i, header in enumerate(headers):
        low = str(header).lower()
        if email_idx is None and "email" in low:
            email_idx = i
        if name_idx is None and ("full name" in low or "your name" in low):
            name_idx = i
    return name_idx, email_idx


def describe_rows(headers, rows, row_numbers):
    """Print one line per pending respondent so the pull can be eyeballed."""
    name_idx, email_idx = label_columns(headers)
    for row, row_num in zip(rows, row_numbers):
        bits = []
        if name_idx is not None and row[name_idx]:
            bits.append(str(row[name_idx]))
        if email_idx is not None and row[email_idx]:
            bits.append(str(row[email_idx]))
        print(f"  row {row_num}: {' — '.join(bits) if bits else '(no name/email answered)'}")


def fetch_pending(url, token):
    """Fetch the pending payload and sanity-check its shape before anything uses it."""
    payload = call_endpoint(url, token, "pending")

    if not isinstance(payload, dict):
        sys.exit(f"ERROR: expected a JSON object from the endpoint, got {type(payload).__name__}.")

    headers = payload.get("headers")
    rows = payload.get("rows")
    row_numbers = payload.get("row_numbers")
    if headers is None or rows is None or row_numbers is None:
        sys.exit("ERROR: endpoint response is missing headers/rows/row_numbers — is the deployed Code.gs out of date?")
    if len(rows) != len(row_numbers):
        sys.exit(f"ERROR: endpoint returned {len(rows)} rows but {len(row_numbers)} row numbers.")

    # A short/long row would silently shift every answer after it into the wrong
    # column, so refuse rather than write a plausible-looking corrupt CSV.
    for row, row_num in zip(rows, row_numbers):
        if len(row) != len(headers):
            sys.exit(
                f"ERROR: sheet row {row_num} has {len(row)} cells but there are {len(headers)} headers. "
                "Has the responses sheet been edited by hand?"
            )

    if ROW_COLUMN in headers:
        sys.exit(
            f"ERROR: the sheet already has a column called {ROW_COLUMN!r}, which this tool appends itself. "
            "Rename or remove it in the responses sheet."
        )

    return headers, rows, row_numbers


def write_csv(headers, rows, row_numbers):
    """
    Write data/form/responses.csv in one shot.

    Built fully in memory first (see fetch_pending) so a failure anywhere upstream
    leaves any previous responses.csv exactly as it was. csv.writer rather than
    DictWriter on purpose: the payload is already positional, and Google Forms
    can legitimately export two identically-named headers — which would collapse
    into one key under DictWriter.
    """
    FORM_DIR.mkdir(parents=True, exist_ok=True)
    with RESPONSES_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(list(headers) + [ROW_COLUMN])
        for row, row_num in zip(rows, row_numbers):
            writer.writerow(list(row) + [row_num])
    return RESPONSES_CSV


def read_pending_rows_from_csv():
    """
    Read the `_row` values back out of data/form/responses.csv.

    The CSV on disk IS the receipt for what was last pulled — there is no local
    state file to drift out of sync with the sheet.
    """
    if not RESPONSES_CSV.exists():
        sys.exit(
            f"ERROR: {RESPONSES_CSV.relative_to(REPO_ROOT)} does not exist — "
            "run the fetch (and then the ingest) before --confirm."
        )

    with RESPONSES_CSV.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or ROW_COLUMN not in reader.fieldnames:
            sys.exit(
                f"ERROR: {RESPONSES_CSV.relative_to(REPO_ROOT)} has no {ROW_COLUMN!r} column. "
                "It was probably a manual export — those can't be confirmed, since there is no row identity. "
                "Stamp the Ingested at cells by hand, or re-pull with this tool."
            )
        row_numbers = []
        for record in reader:
            raw = (record.get(ROW_COLUMN) or "").strip()
            if not raw:
                continue
            try:
                row_numbers.append(int(raw))
            except ValueError:
                sys.exit(f"ERROR: {ROW_COLUMN!r} value {raw!r} is not a row number.")

    if not row_numbers:
        sys.exit(f"ERROR: no {ROW_COLUMN!r} values found in {RESPONSES_CSV.relative_to(REPO_ROOT)}.")
    return row_numbers


def do_confirm(url, token):
    """Stamp the rows recorded in responses.csv as ingested."""
    row_numbers = read_pending_rows_from_csv()
    print(f"Confirming {len(row_numbers)} row(s) from {RESPONSES_CSV.relative_to(REPO_ROOT)}: "
          f"{', '.join(str(n) for n in row_numbers)}")

    payload = call_endpoint(url, token, "confirm", {"rows": ",".join(str(n) for n in row_numbers)})
    stamped = payload.get("stamped", []) if isinstance(payload, dict) else []
    skipped = payload.get("skipped", []) if isinstance(payload, dict) else []

    print(f"Stamped {len(stamped)} row(s) as ingested in the sheet.")
    if skipped:
        # The CSV and the sheet disagree — loud, because the usual cause is that
        # the sheet was sorted or rows were deleted, which breaks row identity.
        print(
            f"WARNING: {len(skipped)} row(s) were out of range and NOT stamped: "
            f"{', '.join(str(n) for n in skipped)}\n"
            "         The CSV and the sheet disagree. Has the responses sheet been sorted or had rows deleted?",
            file=sys.stderr,
        )
        return 1
    return 0


def do_fetch(url, token, dry_run):
    """Pull pending rows and (unless --dry-run) write them to data/form/responses.csv."""
    headers, rows, row_numbers = fetch_pending(url, token)

    if not rows:
        # Explicitly leave any existing responses.csv alone: it is still the
        # receipt for the last pull, and --confirm may not have run yet.
        print("Nothing new — every response in the sheet is already marked ingested.")
        return 0

    print(f"{len(rows)} pending response(s):")
    describe_rows(headers, rows, row_numbers)

    if dry_run:
        print("\n[dry run] nothing written.")
        return 0

    path = write_csv(headers, rows, row_numbers)
    print(f"\nWrote {len(rows)} response(s) to {path.relative_to(REPO_ROOT)}")
    print("Next: python tools/ingest_form_csv.py \"data/form/responses.csv\" --dry-run")
    print("Then, once the real ingest has succeeded: python tools/fetch_form_responses.py --confirm")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Pull pending Google Form responses into data/form/responses.csv, and stamp them ingested."
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Stamp the rows in the existing responses.csv as ingested. Run only AFTER ingest_form_csv.py succeeded.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what is pending without writing responses.csv.",
    )
    args = parser.parse_args()

    if args.confirm and args.dry_run:
        parser.error("--confirm and --dry-run do the opposite things; pick one")

    url, token = load_config()

    if args.confirm:
        return do_confirm(url, token)
    return do_fetch(url, token, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
