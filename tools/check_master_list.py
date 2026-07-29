"""
check_master_list.py — lint a master list for the things that make it unreadable or untrue.

The master list is a SCANNING surface read in Google Sheets, and its two recurring
failures were never caught by anything: prose cells grew to 2,900 characters, and jargon
got expanded in one row and left bare in twenty others. Both had been written down as
conventions in the workflow — conventions are exactly what failed. This tool is the
deterministic half of the WAT split: the rule lives in code, so a drifting list fails
loudly instead of quietly.

Checks (use --check to run a subset while working through a fix):
  schema       header matches SHORTLIST_HEADERS exactly (catches column drift/misalignment)
  completeness every REQUIRED_COLUMNS cell filled; sentinels only where they're allowed
  budget       cells over their CELL_BUDGETS length
  jargon       bare acronyms that apply_glossary can explain, outside the allow-list
  values       List status / Info source / Grades vs entry bar outside their allowed sets
  contradiction  "Grades vs entry bar" vs "Admission likelihood" telling different stories

The contradiction check is the original bug turned into a rule. Duke read "Fits grades? =
No" for a student with A*A*A*A because the column was derived from admission likelihood;
grades and selectivity are different questions. So: below the bar cannot be a Safety, and
a Reach whose grades clear the bar must SAY why it is still a Reach — "Reach (very
selective)" — because that is the student's actual unanswered question.

Usage:
    python tools/check_master_list.py --student ong-kyan
    python tools/check_master_list.py --file csvs/master_list3.csv
    python tools/check_master_list.py --student toru --check budget,jargon
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_glossary import _COMPILED, PLAIN_ALTERNATIVES  # noqa: E402
from shortlist_schema import (  # noqa: E402
    ADMISSION_REASON_MAX,
    CELL_BUDGETS,
    GRADE_FIT_LABELS,
    INFO_SOURCE_OFFICIAL,
    INFO_SOURCE_UNVERIFIED,
    LIST_STATUSES,
    REQUIRED_COLUMNS,
    SENTINEL_VALUES,
    SHORTLIST_HEADERS,
    admission_base,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# Free-text columns the jargon rule applies to. Deliberately excludes the computed
# short columns and the identity/amount ones, where a course title or a currency code
# is not jargon to fix.
PROSE_COLUMNS = [
    "Course at a glance",
    "Student life",
    "Entry requirements",
    "English req",
    "Scholarship & portal",
    "Scholarship coverage",
    "Scholarship competitiveness",
    "How to get the scholarship",
    "Money to show (visa)",
    "Work rights after graduating",
    "Recognised in Malaysia?",
    "Notes",
]

# What counts as fixable jargon is defined in ONE place — apply_glossary.PLAIN_ALTERNATIVES.
# A term is flagged only if a shorter plain-English phrase says the same thing, so every
# finding arrives with its own fix. Proper nouns the student must search for on an official
# page (UCAS, MQA, BEM, Washington Accord, CSS Profile) are deliberately NOT flagged — the
# glossary sheet explains those instead. See the rule in apply_glossary.py.

CHECKS = ["schema", "completeness", "budget", "jargon", "values", "contradiction"]

# Every sentinel string, whatever column it belongs to — used to catch one being used
# in a column that doesn't allow it (see check_completeness).
_ALL_SENTINELS = {s for values in SENTINEL_VALUES.values() for s in values}


def load(csv_path):
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        sys.exit(f"ERROR: {csv_path} is empty.")
    return rows[0], rows[1:]


def check_schema(header):
    """Header must match the schema exactly — same columns, same order."""
    if header == SHORTLIST_HEADERS:
        return []
    missing = [h for h in SHORTLIST_HEADERS if h not in header]
    extra = [h for h in header if h not in SHORTLIST_HEADERS]
    if missing or extra:
        detail = []
        if missing:
            detail.append(f"missing {missing}")
        if extra:
            detail.append(f"unexpected {extra}")
        return [f"header column set differs from the schema: {'; '.join(detail)} — migrate the file"]
    return ["header has the schema's columns in a DIFFERENT ORDER — rewrite it keyed by column name"]


def check_completeness(rows_as_dicts):
    """Blank required cells, and sentinels used where they aren't allowed.

    The master list is the client's deliverable — a spreadsheet handed over as the
    product — so a blank cell reads as breakage, not as "we're still working on it".
    Stage 3 fills all 35 columns from official sources (it used to leave "Course at a
    glance", the scholarship block and "Key deadline" to Stage 4, and sessions honoured
    that unevenly: 1/44 rows filled for one student, 24/24 for another).

    The other half of the rule matters just as much. "Fill every column" invites
    invention, so SENTINEL_VALUES defines the honest ways to say there is no answer —
    per column. "Not ranked" is true of a US liberal-arts college and meaningless in
    "Key deadline"; a sentinel in the wrong column is an agent dodging a fact that
    exists, which is why that is reported rather than accepted as non-blank.

    Second net only: tools/merge_candidates.py catches the same gaps before they reach
    the CSV. This one catches hand-edits and rows synced before the policy existed.
    """
    out = []
    for n, row in rows_as_dicts:
        uni = row.get("University", "?")[:32]
        for column in REQUIRED_COLUMNS:
            value = (row.get(column) or "").strip()
            if not value:
                allowed = SENTINEL_VALUES.get(column)
                hint = f" — or say why not: {allowed}" if allowed else ""
                out.append(f"row {n} {uni} — {column} is blank{hint}")
            elif value in _ALL_SENTINELS and value not in SENTINEL_VALUES.get(column, []):
                out.append(
                    f"row {n} {uni} — {column}: {value!r} is a sentinel for another column; "
                    f"this one needs the real answer"
                )
    return out


def check_budget(rows_as_dicts):
    """Cells over budget, and cells that were cut mid-thought to get under it.

    A cell ending in an ellipsis is inside its budget but still unreadable — it stops
    mid-sentence. Getting under the budget by truncating is not the goal; saying the
    thing shorter is, with the detail in research_notes.md.
    """
    out = []
    for n, row in rows_as_dicts:
        for column, budget in CELL_BUDGETS.items():
            value = row.get(column) or ""
            if len(value) > budget:
                out.append(f"row {n} {row.get('University', '?')[:32]} — {column}: "
                           f"{len(value)} chars (budget {budget})")
            elif value.rstrip().endswith(("…", "...")):
                out.append(f"row {n} {row.get('University', '?')[:32]} — {column}: "
                           f"cut mid-sentence — rewrite it shorter instead of truncating")
    return out


def bare_terms(text):
    """Replaceable jargon appearing in `text`, as [(term, plain alternative)].

    Detection runs on a hyphen-normalised copy as well as the original: apply_glossary's
    matcher deliberately refuses to match across a hyphen (so "STEM-OPT" never partially
    hits "STEM"), but "ETAC-accredited" is exactly how these appear in a cell.
    """
    if not text:
        return []
    probe = text.replace("-", " ") + " " + text
    found = []
    seen = set()
    for surface, canonical, pattern in _COMPILED:
        if canonical in seen or canonical not in PLAIN_ALTERNATIVES:
            continue
        # Some terms list their own plain form as an alias ("out-of-state" is both an alias
        # of OOS and the phrase we rewrite OOS into). Matching on that surface would flag
        # the fix as the problem and make the finding impossible to clear.
        if surface.lower() == PLAIN_ALTERNATIVES[canonical].lower():
            continue
        if pattern.search(probe):
            seen.add(canonical)
            found.append((canonical, PLAIN_ALTERNATIVES[canonical]))
    return found


def check_jargon(rows_as_dicts):
    out = []
    for n, row in rows_as_dicts:
        for column in PROSE_COLUMNS:
            terms = bare_terms(row.get(column) or "")
            if terms:
                fixes = "; ".join(f"{t} -> {plain}" for t, plain in terms)
                out.append(f"row {n} {row.get('University', '?')[:32]} — {column}: {fixes}")
    return out


def check_values(rows_as_dicts):
    allowed_fit = set(GRADE_FIT_LABELS)
    allowed_source = {INFO_SOURCE_UNVERIFIED, INFO_SOURCE_OFFICIAL}
    out = []
    for n, row in rows_as_dicts:
        uni = row.get("University", "?")[:32]
        status = (row.get("List status") or "").strip()
        if status not in LIST_STATUSES:
            out.append(f"row {n} {uni} — List status {status!r} is not one of {LIST_STATUSES}")

        source = (row.get("Info source") or "").strip()
        if source not in allowed_source:
            out.append(f"row {n} {uni} — Info source {source!r} is not one of {sorted(allowed_source)}")

        # Blankness is the completeness check's job now (it owns every required column);
        # this one only judges whether a filled-in value is a legal one.
        fit = (row.get("Grades vs entry bar") or "").strip()
        if fit and fit not in allowed_fit:
            out.append(f"row {n} {uni} — Grades vs entry bar {fit!r} is not one of {list(GRADE_FIT_LABELS)}")

        admission = (row.get("Admission likelihood") or "").strip()
        if "(" in admission:
            reason = admission[admission.index("(") + 1:].rstrip(")").strip()
            if len(reason) > ADMISSION_REASON_MAX:
                out.append(f"row {n} {uni} — Admission likelihood reason is {len(reason)} chars "
                           f"(max {ADMISSION_REASON_MAX})")
    return out


def check_contradiction(rows_as_dicts):
    out = []
    for n, row in rows_as_dicts:
        uni = row.get("University", "?")[:32]
        fit = (row.get("Grades vs entry bar") or "").strip()
        admission = (row.get("Admission likelihood") or "").strip()
        level = admission_base(admission)

        if fit in ("Below", "Well below") and level == "Safety":
            out.append(f"row {n} {uni} — grades are {fit!r} the bar but this is marked a Safety")
        if fit in ("Well above", "Above") and level == "Reach" and "(" not in admission:
            out.append(f"row {n} {uni} — grades are {fit!r} the bar yet this is a Reach with no reason "
                       f"given; say why (e.g. 'Reach (very selective)')")
    return out


def run(header, rows, wanted):
    rows_as_dicts = [(i, dict(zip(header, r))) for i, r in enumerate(rows, start=2)]
    results = {}
    if "schema" in wanted:
        results["schema"] = check_schema(header)
    # The other checks read by column name, so a file with the wrong column SET can't be
    # meaningfully linted past the schema check.
    if set(header) != set(SHORTLIST_HEADERS):
        return results
    if "completeness" in wanted:
        results["completeness"] = check_completeness(rows_as_dicts)
    if "budget" in wanted:
        results["budget"] = check_budget(rows_as_dicts)
    if "jargon" in wanted:
        results["jargon"] = check_jargon(rows_as_dicts)
    if "values" in wanted:
        results["values"] = check_values(rows_as_dicts)
    if "contradiction" in wanted:
        results["contradiction"] = check_contradiction(rows_as_dicts)
    return results


def main():
    parser = argparse.ArgumentParser(description="Lint a master_list.csv for readability and honesty.")
    parser.add_argument("--student", help="Student slug (folder under data/students/).")
    parser.add_argument("--file", help="Path to a master list CSV, instead of --student.")
    parser.add_argument("--check", help=f"Comma list of checks to run (default all): {', '.join(CHECKS)}")
    parser.add_argument("--limit", type=int, default=15, help="Max findings shown per check (default 15).")
    args = parser.parse_args()

    if bool(args.student) == bool(args.file):
        sys.exit("ERROR: pass exactly one of --student or --file.")

    if args.student:
        csv_path = STUDENTS_DIR / args.student / "master_list.csv"
    else:
        csv_path = Path(args.file)
        if not csv_path.is_absolute():
            csv_path = REPO_ROOT / csv_path
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found.")

    wanted = CHECKS
    if args.check:
        wanted = [c.strip().lower() for c in args.check.split(",") if c.strip()]
        unknown = [c for c in wanted if c not in CHECKS]
        if unknown:
            sys.exit(f"ERROR: unknown check(s) {unknown}. Valid: {', '.join(CHECKS)}")

    header, rows = load(csv_path)
    results = run(header, rows, wanted)

    total = sum(len(v) for v in results.values())
    print(f"{csv_path.relative_to(REPO_ROOT) if csv_path.is_relative_to(REPO_ROOT) else csv_path} "
          f"— {len(rows)} rows, {total} finding(s)")
    for name in CHECKS:
        findings = results.get(name)
        if findings is None:
            continue
        if not findings:
            print(f"  ok   {name}")
            continue
        print(f"  FAIL {name} ({len(findings)})")
        for line in findings[:args.limit]:
            print(f"       {line}")
        if len(findings) > args.limit:
            print(f"       ... and {len(findings) - args.limit} more")

    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
