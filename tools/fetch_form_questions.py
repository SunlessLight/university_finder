"""
fetch_form_questions.py — save each live Google Form's QUESTIONS to forms/<name>.json.

Added 2026-10-26 (backlog I10). Until now no session could see a form's wording or answer
options, so every form edit was found by Evan describing it or by the next export — after
real students had answered. This reads the questions (never answers) through the same
Apps Script web app as fetch_form_responses.py (action `questions` in
tools/appsscript/Code.gs, same token).

The JSON holds no student data, so forms/ is TRACKED: `git diff forms/` after a run shows
exactly what changed on a form. Nothing time-varying is written (no fetch timestamp), so an
unchanged form gives an empty diff.

Usage:
    # every configured form
    python tools/fetch_form_questions.py

    # one or more by name
    python tools/fetch_form_questions.py --form intake survey

    # fetch the intake form, then check it against ingest_form_csv.py
    python tools/fetch_form_questions.py --check

    # check the saved forms/intake.json without fetching
    python tools/fetch_form_questions.py --check --offline

--check compares the intake form with the matching rules in ingest_form_csv.py: every
question title against QUESTION_MAP (by rebuilding the sheet headers the form would
produce), and the options of the budget, countries, course, "other preferences" and
priority-grid questions against their normalise maps. It prints anything unmatched and
exits 1 only on the consent rules (I12), because a broken consent question silently
skips every new student. When FORM_ID_REPORT_INTAKE is set it also checks the report form
(its own required questions, plus: the consent wording may not name race or halal/prayer,
because that form doesn't ask them).

Requires in .env (see README, "Setup (first time)"):
    FORM_WEBAPP_URL, FORM_WEBAPP_TOKEN   same as fetch_form_responses.py
    FORM_ID_INTAKE                       optional; blank = the form linked to the responses sheet
    FORM_ID_REPORT_INTAKE, FORM_ID_REPORT_FEEDBACK, FORM_ID_SPREADSHEET_FEEDBACK, FORM_ID_SURVEY
        the ID is the long code in the form's EDIT address: docs.google.com/forms/d/<ID>/edit
        (not the /e/... share link). IDs are not secrets; .env is just where form settings live.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_form_responses import call_endpoint, load_config  # noqa: E402
from ingest_form_csv import (  # noqa: E402
    BUDGET_BAND_NORMALIZE,
    COUNTRY_NORMALIZE,
    COURSE_ACCREDITATION_MAP,
    NEEDS_NORMALIZE,
    TICK_IMPORTANCE_NORMALIZE,
    TICK_MARKER,
    _UNMATCHED_BAND,
    _budget_band,
    _check_headers,
    _course_title,
    _grid_columns,
    _slider_columns,
    _subject_columns,
    _subject_grid_columns,
    build_col_index,
)
from shortlist_schema import budget_ceiling  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
FORMS_DIR = REPO_ROOT / "forms"

# name -> .env key holding its form ID. Only intake may be blank (Code.gs then opens the
# form linked to its own responses sheet).
FORMS = {
    "intake": "FORM_ID_INTAKE",
    "report_intake": "FORM_ID_REPORT_INTAKE",
    "report_feedback": "FORM_ID_REPORT_FEEDBACK",
    "spreadsheet_feedback": "FORM_ID_SPREADSHEET_FEEDBACK",
    "survey": "FORM_ID_SURVEY",
}

# Items that hold no answer, so they never become a sheet column.
LAYOUT_TYPES = {"SECTION_HEADER", "PAGE_BREAK", "IMAGE", "VIDEO"}

# QUESTION_MAP keys the current intake form must hit; a miss blanks that field for every
# new student. Email is NOT here: "collect email addresses" is a form setting, not an item,
# so it never appears in the question list (the sheet still gets the column).
REQUIRED_KEYS = ["consent", "name", "total_budget", "target_countries", "specific_courses",
                 "grades_raw", "program_type"]
REPORT_REQUIRED_KEYS = ["consent", "name", "report_university", "specific_courses", "grades_raw",
                        "program_type", "report_question"]

# QUESTION_MAP keys whose answers ingest_form_csv.py splits on commas (_split_multi).
SPLIT_KEYS = ["needs", "target_countries", "location_prefs"]

# Unfilled template text in the consent notice (I12): [Your name], <email>, XXX, TBD.
PLACEHOLDER_RE = re.compile(r"\[[^\]]*\]|<[^>]*>|\bX{2,}\b|\bTBD\b", re.IGNORECASE)


def fetch(names, offline):
    """Fetch (or, offline, load) each named form. Returns {name: payload}."""
    if offline:
        out = {}
        for name in names:
            path = FORMS_DIR / f"{name}.json"
            if not path.exists():
                sys.exit(f"ERROR: {path.relative_to(REPO_ROOT)} does not exist — run without --offline first.")
            out[name] = json.loads(path.read_text(encoding="utf-8"))
        return out

    url, token = load_config()
    out = {}
    for name in names:
        form_id = os.getenv(FORMS[name], "").strip()
        if not form_id and name != "intake":
            sys.exit(f"ERROR: {FORMS[name]} is not set in .env (the ID from the form's edit address).")
        payload = call_endpoint(url, token, "questions", {"form": form_id} if form_id else None)
        if not isinstance(payload, dict) or "items" not in payload:
            sys.exit("ERROR: endpoint response has no 'items' — is the deployed Code.gs out of date?")
        FORMS_DIR.mkdir(exist_ok=True)
        path = FORMS_DIR / f"{name}.json"
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        answered = sum(1 for i in payload["items"] if i["type"] not in LAYOUT_TYPES)
        print(f"{name}: {answered} question(s) -> {path.relative_to(REPO_ROOT)}")
        out[name] = payload
    return out


def sheet_headers(items):
    """The response-sheet headers this form produces: one per question, and one
    'Title [Row]' per row of a grid (how Google Forms names grid columns)."""
    headers = []
    for item in items:
        if item["type"] in LAYOUT_TYPES:
            continue
        if item["type"] in ("GRID", "CHECKBOX_GRID"):
            headers.extend(f"{item['title']} [{row}]" for row in item.get("rows", []))
        else:
            headers.append(item["title"])
    return headers


def report(label, problems):
    """Print one check's result; return how many problems it found."""
    print(f"\n{label}: " + ("ok" if not problems else f"{len(problems)} problem(s)"))
    for p in problems:
        print(f"  - {p}")
    return len(problems)


def check_intake(form):
    """Check the intake form against ingest_form_csv.py. Returns the exit code."""
    items = form["items"]
    by_title = {i["title"]: i for i in items}
    headers = sheet_headers(items)
    col_index = build_col_index(headers)

    print(f"Intake form: {form.get('title')!r}\n")
    _check_headers(headers, col_index, _grid_columns(headers), _slider_columns(headers),
                   _subject_columns(headers), _subject_grid_columns(headers))

    def options(key):
        item = by_title.get(col_index.get(key))
        return item.get("options", []) if item else []

    report("Questions the program depends on",
           [f"no question matches {k!r} — every new student gets it blank" for k in REQUIRED_KEYS
            if k not in col_index])

    # Budget: show every option's ceiling, since a plausible-looking wrong number is the trap (I11).
    print("\nBudget options -> ceiling (MYR):")
    budget_problems = []
    for opt in options("total_budget"):
        ceiling, _label = _budget_band(opt)
        route = ""
        if ceiling is _UNMATCHED_BAND:
            ceiling, route = budget_ceiling(opt), "  (only via the legacy free-text fallback)"
            if ceiling is None:
                budget_problems.append(f"{opt!r} gives no number; every student who picks it gets a review flag")
        print(f"  {opt!r} -> {'no limit' if ceiling is None else f'{ceiling:,.0f}'}{route}")
    report("Budget options", budget_problems)

    report("Country options", [f"{o!r} is not in COUNTRY_NORMALIZE (dropped on ingest)"
                               for o in options("target_countries")
                               if o.strip().lower() not in COUNTRY_NORMALIZE])
    report("Course options", [f"{_course_title(o)!r} is not in COURSE_ACCREDITATION_MAP (no recognition targets)"
                              for o in options("specific_courses")
                              if _course_title(o) not in COURSE_ACCREDITATION_MAP])
    report("Other-preferences options", [f"{o!r} matches nothing in NEEDS_NORMALIZE (ignored on ingest)"
                                         for o in options("needs")
                                         if not any(t in o.lower() for t in NEEDS_NORMALIZE)])

    tick_problems = []
    for item in items:
        if TICK_MARKER in item["title"].lower():
            tick_problems += [f"column {c!r} is not in TICK_IMPORTANCE_NORMALIZE (that answer is skipped)"
                              for c in item.get("columns", []) if c.strip().lower() not in TICK_IMPORTANCE_NORMALIZE]
    report("Priority grid columns", tick_problems)

    # Google Forms joins ticked checkboxes with ", ", and _split_multi() splits on commas. Only
    # the fields that go through _split_multi() matter; courses and budget are read whole.
    split_titles = {col_index.get(k) for k in SPLIT_KEYS} - {None}
    report("Checkbox options with a comma", [
        f"{item['title'][:50]!r}: {o!r} gets split in two on ingest"
        for item in items if item["title"] in split_titles for o in item.get("options", []) if "," in o])

    return 1 if report("Consent question", consent_problems(items)) else 0


def consent_problems(items):
    """The consent rules (I12): the only checks that fail the run.

    A section header titled "consent" is fine (never a column), but the notice text often
    lives in its description, so placeholders are searched in those too.
    """
    consent_all = [i for i in items if "consent" in i["title"].lower()]
    consent_items = [i for i in consent_all if i["type"] not in LAYOUT_TYPES]
    problems = []
    if len(consent_items) != 1:
        problems.append(f"{len(consent_items)} question titles contain 'consent'; exactly 1 must "
                        "(the program finds the consent question by that word)")
    for item in consent_items:
        for o in item.get("options", []):
            if o.strip().lower().startswith("n"):
                problems.append(f"option {o!r} starts with N, which the program reads as 'No' "
                                "and skips the student")
        if not item.get("required"):
            problems.append(f"{item['title'][:50]!r} is not required")
    for item in consent_all:
        text = " ".join([item["title"], item.get("description") or ""] + item.get("options", []))
        for hit in PLACEHOLDER_RE.findall(text):
            problems.append(f"unfilled placeholder {hit!r} in the consent question")
    return problems


def check_report_form(form):
    """Check the report form against ingest_form_csv.py. Returns the exit code."""
    items = form["items"]
    col_index = build_col_index(sheet_headers(items))
    print(f"\nReport form: {form.get('title')!r}")
    report("Questions the program depends on",
           [f"no question matches {k!r} — every new buyer gets it blank" for k in REPORT_REQUIRED_KEYS
            if k not in col_index])

    problems = consent_problems(items)
    # A person may only agree to what the form collects: this form asks neither.
    for item in items:
        if "consent" not in item["title"].lower() or item["type"] in LAYOUT_TYPES:
            continue
        wording = " ".join(item.get("options", [])).lower()
        problems += [f"the consent wording names {word!r}, which this form never asks"
                     for word in ("race", "halal", "prayer") if word in wording]
    return 1 if report("Consent question", problems) else 0


def main():
    parser = argparse.ArgumentParser(description="Save live Google Form questions to forms/<name>.json.")
    parser.add_argument("--form", nargs="+", choices=sorted(FORMS), help="Which form(s); default: every configured one.")
    parser.add_argument("--check", action="store_true", help="Check the intake form against ingest_form_csv.py.")
    parser.add_argument("--offline", action="store_true", help="Use the saved forms/*.json instead of fetching.")
    args = parser.parse_args()

    if args.check:
        load_config()  # loads .env, so the report form's ID is visible below
        names = ["intake"]
        if os.getenv(FORMS["report_intake"], "").strip() or (args.offline and (FORMS_DIR / "report_intake.json").exists()):
            names.append("report_intake")
        else:
            print(f"Report form not checked: no {FORMS['report_intake']} in .env\n")
    elif args.form:
        names = args.form
    else:
        load_config()  # loads .env, so the configured-ness test below sees it
        names = [n for n in FORMS if n == "intake" or os.getenv(FORMS[n], "").strip()]
        skipped = [FORMS[n] for n in FORMS if n not in names]
        if skipped:
            print(f"Skipping forms with no ID in .env: {', '.join(skipped)}\n")

    forms = fetch(names, args.offline)
    if args.check:
        print()
        code = check_intake(forms["intake"])
        if "report_intake" in forms:
            code = max(code, check_report_form(forms["report_intake"]))
        return code
    return 0


if __name__ == "__main__":
    sys.exit(main())
