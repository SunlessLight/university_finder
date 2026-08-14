"""
apply_backfill.py — patch EXISTING master_list.csv rows from row-filler backfill fragments.

The sibling of merge_candidates.py, for the other direction. merge_candidates.py collects
fragments for universities that are NOT on the list yet and hands them to sync_shortlist.py,
which only ever APPENDS. Neither can top up a row that already exists: sync dedupes by
course_key and silently skips a repeat. So a longlist with holes — a legacy row predating the
"all 35 columns required" policy (2026-07-29), or a country pass that came back short — had no
tool at all, and got patched by hand.

Two real sessions did exactly that (2026-08-01 UK, 2026-08-02 USA, same student, one day apart)
and both paid the same avoidable cost, measured in token_cost_report.md: each of ~10 row-fillers
reported its values as prose in its REPLY, so the orchestrating session had to hold ten replies
in context and re-transcribe them by hand, then make ten sequential Edit calls against
research_notes.md. Fragments on disk + one read-modify-write pass is the fix (plan.md Change 8b/8c):
the values never enter the main session's context at all, and both files are written once.

What it does, in order:
  1. reads .tmp/<slug>/backfill/*.json  (one fragment per university, written by row-filler)
  2. matches each to an EXISTING row by course_key — refuses to create rows (that is sync's job)
  3. refuses any COMPUTED_COLUMNS write, any unknown column, any cell over CELL_BUDGETS,
     and any overwrite of an already-filled cell unless --overwrite
  4. writes master_list.csv once, and appends each fragment's research_notes under that
     university's existing "## University - Course" heading in research_notes.md

Nothing is written unless every fragment passes — a half-applied batch is worse than none,
because the second run can't tell which rows it already touched.

Fragment shape (row-filler backfill mode; see .claude/agents/row-filler.md):
    {
      "university": "University of Strathclyde",
      "course": "BSc (Hons) Chemistry",
      "cells": {"English req": "IELTS 6.5 overall, 5.5 each part", "Overall rank": "QS 2027 #230"},
      "research_notes": "Free-length prose: sources, caveats, why a sentinel was used.",
      "gaps": "none"
    }

Usage:
    python tools/apply_backfill.py --student <slug> --dry-run
    python tools/apply_backfill.py --student <slug>
    python tools/apply_backfill.py --student <slug> --country "United Kingdom"
    python tools/apply_backfill.py --student <slug> --fragments .tmp/x/backfill/uk
"""

import argparse
import csv
import difflib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import (  # noqa: E402
    CELL_BUDGETS,
    SHORTLIST_HEADERS,
    course_key,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# Columns a backfill may NOT write, because nothing hand-typed belongs in them: each is
# derived by sync_shortlist.py from the candidate JSON's scores/entry_margin, and a
# hand-written value is precisely the bug the 2026-07-25 rebuild fixed (an agent typing
# "Reach" into Admission likelihood to mean "grades fall short" printed "doesn't fit the
# grades" for a student with A*A*A*A at Duke). "List status" is here for a different
# reason: promotion/rejection is a deliberate edit the student agreed to, never a
# side-effect of filling in cells.
COMPUTED_COLUMNS = {
    "List status",
    "Desirability",
    "Tier",
    "Admission likelihood",
    "Warnings",
    "Grades vs entry bar",
    "Approx total (MYR)",
}

# Patching one of these leaves a COMPUTED column stale, and this tool deliberately does not
# recompute (it has no candidate JSON, no weights, no sub-scores — only cells). Reported as a
# notice so the staleness is visible rather than silent; re-derive by hand or re-run the row
# through the normal fragment -> merge -> sync path.
STALE_TRIGGERS = {
    "Key deadline": 'Warnings ("Deadline passed")',
    "Annual tuition": 'Approx total (MYR), Warnings ("Over budget")',
    "Total tuition": 'Approx total (MYR), Warnings ("Over budget")',
    "Est. living/yr": 'Approx total (MYR), Warnings ("Over budget")',
    "Duration (yrs)": 'Approx total (MYR), Warnings ("Over budget")',
    "Entry requirements": 'Grades vs entry bar, Admission likelihood',
}

NOTES_HEADER = (
    "# Research notes\n\nThe long-form research behind each master_list row — the "
    "verification stamps, source conflicts and cost traps that are too long for a "
    "spreadsheet cell. The CSV's `Notes` column carries the one-line headline.\n"
)


def load_fragments(frag_dir):
    """Read every *.json in frag_dir as (path, fragment). Exits on unreadable JSON."""
    paths = sorted(p for p in frag_dir.glob("*.json"))
    if not paths:
        sys.exit(
            f"ERROR: no backfill fragments in {frag_dir}.\n"
            f"Each row-filler in backfill mode writes one {frag_dir.name}/<uni-slug>.json — "
            f"dispatch them first (.claude/agents/row-filler.md, 'Backfill mode')."
        )
    out = []
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            sys.exit(f"ERROR: {path} is not valid JSON ({exc}).")
        if not isinstance(data, dict):
            sys.exit(f"ERROR: {path} must hold one backfill object (see the tool docstring).")
        out.append((path, data))
    return out


def load_csv(csv_path):
    """(header, rows) from the master list. Exits if the column SET differs from the schema."""
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        sys.exit(f"ERROR: {csv_path} is empty.")
    header = rows[0]
    if set(header) != set(SHORTLIST_HEADERS):
        sys.exit(
            f"ERROR: {csv_path} columns differ from the current schema (SHORTLIST_HEADERS). "
            f"Migrate the file before backfilling it."
        )
    return header, rows[1:]


def index_rows(header, rows):
    """course_key -> row index, for matching a fragment to the row it patches."""
    uni_col, course_col = header.index("University"), header.index("Course")
    index = {}
    for i, row in enumerate(rows):
        uni = row[uni_col] if len(row) > uni_col else ""
        course = row[course_col] if len(row) > course_col else ""
        index.setdefault(course_key(uni, course), i)
    return index


def _norm(text):
    """Whitespace-insensitive form, for asking 'is this prose already in the file?'."""
    return " ".join(str(text or "").split())


def validate(fragments, header, rows, index, country, overwrite, notes_text=""):
    """Return (problems, plan, noop). `plan` is [(row_index, label, {column: value}, notes)].

    Every rule that could corrupt the deliverable fires here, before a single byte is
    written. A partially-applied batch is unrecoverable in practice: the second run has
    no way to tell an already-patched cell from one a human filled in.
    """
    problems, plan, noop = [], [], []
    country_col = header.index("Country")
    have_notes = _norm(notes_text)

    for path, frag in fragments:
        uni = str(frag.get("university") or "").strip()
        course = str(frag.get("course") or "").strip()
        label = f"{uni or path.stem} — {course or '?'}"
        if not uni or not course:
            problems.append(f"{path.name}: needs both 'university' and 'course' to match a row")
            continue

        row_i = index.get(course_key(uni, course))
        if row_i is None:
            problems.append(
                f"{label}: no such row in the master list. Backfill PATCHES existing rows; "
                f"a new university goes through merge_candidates.py + sync_shortlist.py instead"
            )
            continue

        row = rows[row_i]
        if country and str(row[country_col] or "").strip().lower() != country.strip().lower():
            problems.append(
                f"{label}: row's Country is {row[country_col]!r}, not {country!r} "
                f"(--country guards a split batch from patching the wrong half)"
            )
            continue

        cells = frag.get("cells")
        if not isinstance(cells, dict) or not cells:
            problems.append(f"{label}: 'cells' must be a non-empty object of column -> value")
            continue

        clean = {}
        for column, value in cells.items():
            if column not in SHORTLIST_HEADERS:
                near = difflib.get_close_matches(column, SHORTLIST_HEADERS, n=2, cutoff=0.5)
                hint = f" — closest: {', '.join(repr(n) for n in near)}" if near else ""
                problems.append(f"{label}: {column!r} is not a master-list column{hint}")
                continue
            if column in COMPUTED_COLUMNS:
                problems.append(
                    f"{label}: {column!r} is computed by sync_shortlist.py from the candidate "
                    f"JSON — a backfill must never hand-write it"
                )
                continue

            value = "" if value is None else str(value).strip()
            if not value:
                problems.append(f"{label}: {column!r} has no value (a blank patch is a no-op)")
                continue

            budget = CELL_BUDGETS.get(column)
            if budget and len(value) > budget:
                problems.append(
                    f"{label}: {column!r} is {len(value)} chars (budget {budget}) — say it "
                    f"shorter and move the detail to research_notes; nothing is truncated here"
                )
                continue

            existing = (row[header.index(column)] or "").strip()
            if existing and existing != value and not overwrite:
                problems.append(
                    f"{label}: {column!r} is already filled ({existing[:40]!r}...) — pass "
                    f"--overwrite if this is a deliberate correction"
                )
                continue
            if existing == value:
                continue  # already applied; a re-run is a no-op, not an error
            clean[column] = value

        # Already-present prose is dropped, not appended again: this tool is re-run after a
        # partial batch is fixed, and research_notes.md has no key to dedupe on the way the
        # CSV has course_key. Caught by testing a re-run, which duplicated both sections.
        notes = str(frag.get("research_notes") or "").strip()
        if notes and _norm(notes) in have_notes:
            notes = ""

        if clean or notes:
            plan.append((row_i, label, clean, notes))
        else:
            noop.append(label)

    return problems, plan, noop


def _heading_parts(line):
    """Split a '## University - Course' heading back into (university, course)."""
    body = line[3:].strip()
    uni, _, course = body.partition(" - ")
    return uni, course


def apply_notes(notes_path, entries):
    """Append each (university, course, text) under its existing '## Uni - Course' section.

    One read-modify-write pass over the whole file — deliberately, instead of N Edit calls.
    Ten sequential Edits against this file (2026-08-02) each needed a ~200-word `old_string`
    purely to disambiguate the match: pure token overhead carrying no new information, and
    every one of them resident in the session's context for the rest of its life.

    A missing heading is appended rather than treated as an error: a row can legitimately
    predate research_notes.md, which only came in with the 2026-07-25 schema change.

    Callers pass only prose that isn't already in the file — validate() drops the rest.
    """
    if not entries:
        return 0
    text = notes_path.read_text(encoding="utf-8") if notes_path.exists() else NOTES_HEADER
    lines = text.splitlines()

    def headings():
        return [(i, course_key(*_heading_parts(l))) for i, l in enumerate(lines) if l.startswith("## ")]

    for uni, course, body in entries:
        key = course_key(uni, course)
        heads = headings()
        pos = next((i for i, k in heads if k == key), None)
        if pos is None:
            lines.extend(["", f"## {uni} - {course}", "", body])
            continue
        end = next((i for i, _ in heads if i > pos), len(lines))
        while end > pos + 1 and not lines[end - 1].strip():
            end -= 1
        lines[end:end] = ["", body]

    notes_path.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")
    return len(entries)


def main():
    parser = argparse.ArgumentParser(
        description="Patch existing master_list.csv rows from row-filler backfill fragments."
    )
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument(
        "--country",
        help="Optional guard: every patched row's Country must match this. Use it when a "
        "backfill is split into per-country batches so one can't patch the other's rows.",
    )
    parser.add_argument("--fragments", help="Fragment directory (default .tmp/<slug>/backfill/).")
    parser.add_argument("--csv", help="Master list path (default data/students/<slug>/master_list.csv).")
    parser.add_argument("--notes", help="Research notes path (default data/students/<slug>/research_notes.md).")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow patching cells that are already filled. Off by default: a backfill fills "
        "blanks, and silently replacing a verified fact is the destructive case.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and report; write nothing.")
    args = parser.parse_args()

    slug = args.student
    student_dir = STUDENTS_DIR / slug

    def resolve(value, default):
        if not value:
            return default
        p = Path(value)
        return p if p.is_absolute() else REPO_ROOT / p

    frag_dir = resolve(args.fragments, REPO_ROOT / ".tmp" / slug / "backfill")
    csv_path = resolve(args.csv, student_dir / "master_list.csv")
    notes_path = resolve(args.notes, student_dir / "research_notes.md")

    if not frag_dir.exists():
        sys.exit(f"ERROR: {frag_dir} not found. Row-fillers in backfill mode write their fragments there.")
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found — there is nothing to backfill into.")

    fragments = load_fragments(frag_dir)
    header, rows = load_csv(csv_path)
    index = index_rows(header, rows)
    print(f"student: {slug} | {len(fragments)} fragment(s) in {frag_dir} | {len(rows)} row(s) in the list")

    notes_text = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
    problems, plan, noop = validate(
        fragments, header, rows, index, args.country, args.overwrite, notes_text
    )

    if problems:
        print(f"\nFAIL — {len(problems)} problem(s); NOTHING written:")
        for line in problems:
            print(f"  ! {line}")
        print(
            "\nFix the fragment(s) or re-dispatch the row-filler(s) named above. A fact that "
            "genuinely does not exist takes a sentinel\n(python tools/shortlist_schema.py "
            "--contract), never a guess."
        )
        sys.exit(1)

    total_cells = sum(len(cells) for _, _, cells, _ in plan)
    stale = {}
    for _, label, cells, _ in plan:
        for column in cells:
            if column in STALE_TRIGGERS:
                stale.setdefault(STALE_TRIGGERS[column], set()).add(label)
    for _, label, cells, notes in plan:
        bits = f"{len(cells)} cell(s)" if cells else "no cells"
        if notes:
            bits += " + research notes"
        print(f"  ok   {label}: {bits}")
    for label in noop:
        print(f"  --   {label}: already applied, nothing to change")

    if not plan:
        print("\nNothing to apply — every fragment's values are already in the list.")
        return

    if stale:
        print("\nNOTICE — computed columns this tool does NOT recompute (it has no scores or weights):")
        for column, unis in sorted(stale.items()):
            print(f"  ~ {column} may now be stale for: {', '.join(sorted(unis))}")
        print("  Re-derive those by hand, or re-run the row through merge_candidates.py + sync_shortlist.py.")

    if args.dry_run:
        print(f"\n(dry run — {total_cells} cell(s) across {len(plan)} row(s) would be written to {csv_path})")
        return

    for row_i, _, cells, _ in plan:
        row = rows[row_i]
        row.extend([""] * (len(header) - len(row)))
        for column, value in cells.items():
            row[header.index(column)] = value

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"\nPatched {total_cells} cell(s) across {len(plan)} row(s) in {csv_path}")

    note_entries = [
        (label.split(" — ")[0], label.split(" — ")[1], notes)
        for _, label, _, notes in plan
        if notes
    ]
    written = apply_notes(notes_path, note_entries)
    if written:
        print(f"Wrote {written} research-notes section(s) to {notes_path}")

    print(
        f"\nNext: python tools/check_master_list.py --student {slug}\n"
        f"      Run it WITHOUT --check — a narrow filter answers only the question you already "
        f"know to ask, and\n      has hidden an unrelated failure before (a bare acronym sitting "
        f"in ten cells the whole time)."
    )


if __name__ == "__main__":
    main()
