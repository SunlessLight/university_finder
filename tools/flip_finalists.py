"""
flip_finalists.py — fold Stage 4 finalist markers into master_list.csv in ONE pass.

The Stage 4 counterpart to merge_candidates.py. Each report-writer dispatch renders its
report with build_report.py, which writes a marker fragment to
.tmp/<slug>/finalists/<report-slug>.json instead of touching the CSV. This tool reads every
fragment, reads master_list.csv ONCE, applies them all, writes ONCE, and deletes only the
fragments it successfully applied.

Why it exists: build_report.py used to do the flip itself, reading and rewriting the whole
CSV per report. That is a shared write set, so report-writer dispatches had to run one at a
time — 3-5 sequential Opus deep-research passes — purely to stop two of them racing on one
file. The reports themselves share nothing. Moving the write here makes the dispatches
parallel, exactly as row-filler fragments do for Stage 3.

Per-fragment outcomes (SOFT-fail, unlike merge_candidates.py's all-or-nothing):

  flipped         matched, was not Finalist, no corrections     row changed, fragment deleted
  corrected       matched, flipped and/or corrections applied   row changed, fragment deleted
  already_final   matched, already Finalist; corrections still  maybe changed, fragment deleted
  already_rejected  a matched row currently reads Rejected      NOT changed, fragment KEPT
  no_match        no CSV row matched university(+course)        not changed, fragment kept
  guard_failed    --mode university marker hit a non-USA row    not changed, fragment kept
  bad_correction  a correction is not a writable column / too long   not changed, fragment kept

All-or-nothing would be wrong here in a way it isn't for merge_candidates.py: a Stage 3
fragment that fails means re-dispatching a cheap Sonnet row-filler, but a Stage 4 fragment
that fails has an expensive, already-written report behind it. One typo'd university name
must not withhold four good flips. Whatever fails stays on disk, named, for a re-run — and a
re-run is idempotent, because re-applying an applied fragment lands on already_final.

THE already_rejected CHECK IS THE POINT. The old build_report.py set "Finalist"
unconditionally, ignoring the row's current status. That was already a latent bug; batching
widens the window, because the student can demote a row to Rejected in the main session
between the report being written and this tool running. A naive flip would silently
resurrect a row the student just dropped — the exact class of quiet wrongness this project's
guardrails exist to stop. So: read the status first, refuse, keep the fragment, say so loudly.

Marker shape (written by build_report.py; see its header):
    {
      "university": "London School of Economics",
      "course": "BSc Economics",          # null in --mode university
      "mode": "course",                   # "course" | "university"
      "corrections": {"Student life": "One tight corrected sentence."}
    }

Usage:
    python tools/flip_finalists.py --student <slug> --dry-run
    python tools/flip_finalists.py --student <slug>
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
    canonical_uni,
    course_key,
)

# Imported, not re-listed: the set of columns nothing hand-written may touch is one rule
# with one rationale, and a second copy here would drift the first time a column is added.
# apply_backfill.py has no import-time side effects beyond constants and defs.
from apply_backfill import COMPUTED_COLUMNS  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# Country values that count as US for the university-mode guard (the CSV uses "USA").
US_COUNTRY_VALUES = {"usa", "us", "united states", "united states of america"}

# Outcomes whose fragment has done its job and can be cleaned up. Everything else stays on
# disk so a re-run picks it up after the human fixes whatever it named.
APPLIED_OUTCOMES = {"flipped", "corrected", "already_final"}


def load_markers(frag_dir):
    """Read every *.json in frag_dir as (path, marker). Exits on unreadable JSON.

    A malformed marker is fatal rather than soft-failed: it means build_report.py did not
    write this file, so the assumption that a report exists behind it no longer holds.
    """
    out = []
    for path in sorted(frag_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            sys.exit(f"ERROR: {path} is not valid JSON ({exc}).")
        if not isinstance(data, dict):
            sys.exit(f"ERROR: {path} must hold one finalist marker object (see the tool docstring).")
        out.append((path, data))
    return out


def load_csv(csv_path):
    """(header, rows) from the master list. Exits if the column SET differs from the schema."""
    # utf-8-sig, not utf-8: master_list.csv is often written with a BOM (Excel, and
    # ingest_form_csv/fetch_form_responses both read that way). Reading it as plain
    # utf-8 leaves "﻿List status" as the first header, so the schema check below
    # fails with "columns differ" on a file whose columns are actually identical.
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    if not rows:
        sys.exit(f"ERROR: {csv_path} is empty.")
    header = rows[0]
    if set(header) != set(SHORTLIST_HEADERS):
        sys.exit(
            f"ERROR: {csv_path} columns differ from the current schema (SHORTLIST_HEADERS). "
            f"Migrate the file before flipping finalists into it."
        )
    return header, rows[1:]


def _cell(row, col):
    return (row[col] if len(row) > col else "") or ""


def match_rows(marker, header, rows):
    """Row indices this marker claims.

    Course mode matches one row by course_key(university, course). University mode (US-only)
    matches by UNIVERSITY NAME alone — a US general report certifies the whole institution
    and the student applies undeclared — so it can legitimately claim several course rows.
    """
    uni_col, course_col = header.index("University"), header.index("Course")
    uni = str(marker.get("university") or "").strip()
    if (marker.get("mode") or "course") == "university":
        target = canonical_uni(uni)
        return [i for i, row in enumerate(rows) if canonical_uni(_cell(row, uni_col)) == target]
    target = course_key(uni, marker.get("course"))
    return [
        i for i, row in enumerate(rows)
        if course_key(_cell(row, uni_col), _cell(row, course_col)) == target
    ]


def validate_corrections(marker, header, label, mode, match_count):
    """(clean, problems, warnings) for a marker's optional cell corrections.

    Same rules as apply_backfill.py: a real column, never a COMPUTED one, within its
    CELL_BUDGETS length. Deliberately NOT apply_backfill's "already filled" rule — a
    correction is by definition an overwrite of a filled cell, which is the one thing
    report-writer is allowed to do to a row it researched more deeply than Stage 3 did.
    """
    corrections = marker.get("corrections") or {}
    if not isinstance(corrections, dict):
        return {}, [f"{label}: 'corrections' must be an object of column -> value"], []

    clean, problems, warnings = {}, [], []
    for column, value in corrections.items():
        if column not in SHORTLIST_HEADERS:
            near = difflib.get_close_matches(column, SHORTLIST_HEADERS, n=2, cutoff=0.5)
            hint = f" — closest: {', '.join(repr(n) for n in near)}" if near else ""
            problems.append(f"{label}: {column!r} is not a master-list column{hint}")
            continue
        if column in COMPUTED_COLUMNS:
            problems.append(
                f"{label}: {column!r} is computed by sync_shortlist.py from the candidate "
                f"JSON's scores — a report must never hand-write it (guardrail 1)"
            )
            continue

        value = "" if value is None else str(value).strip()
        if not value:
            problems.append(f"{label}: {column!r} has no value — never blank a cell to 'correct' it")
            continue

        budget = CELL_BUDGETS.get(column)
        if budget and len(value) > budget:
            problems.append(
                f"{label}: {column!r} is {len(value)} chars (budget {budget}) — say it shorter; "
                f"the depth belongs in the report, and nothing is truncated here"
            )
            continue

        # A course sentence is per-course by construction, but a university-mode marker
        # matches by name and can claim several course rows at once — writing one course
        # sentence into all of them is wrong for every row but one. Warn, don't block:
        # a single-row university is the legitimate case.
        if mode == "university" and column == "Course at a glance":
            severity = "WRONG for" if match_count > 1 else "questionable on"
            warnings.append(
                f"{label}: 'Course at a glance' from a --mode university report is {severity} "
                f"{match_count} matched row(s) — that cell is per-course, the report is not"
            )
        clean[column] = value
    return clean, problems, warnings


def plan_marker(path, marker, header, rows):
    """(outcome, label, detail, row_indices, clean_corrections, warnings) — decide, write nothing."""
    uni = str(marker.get("university") or "").strip()
    course = str(marker.get("course") or "").strip()
    mode = marker.get("mode") or "course"
    label = f"{uni or path.stem}{f' — {course}' if course else ''}"

    if not uni:
        return "bad_correction", label, "marker has no 'university' to match on", [], {}, []

    matches = match_rows(marker, header, rows)
    if not matches:
        what = f"{uni} — {course}" if mode == "course" else f"{uni} (any course)"
        return "no_match", label, f"no master_list row matches {what}", [], {}, []

    status_col, country_col = header.index("List status"), header.index("Country")
    course_col = header.index("Course")

    if mode == "university":
        non_us = sorted({
            _cell(rows[i], country_col).strip() or "(blank)"
            for i in matches
            if _cell(rows[i], country_col).strip().lower() not in US_COUNTRY_VALUES
        })
        if non_us:
            return (
                "guard_failed", label,
                f"--mode university is US-only, but matched rows have Country = "
                f"{', '.join(non_us)}. Rebuild as a course report for a non-US university",
                [], {}, [],
            )

    rejected = [i for i in matches if _cell(rows[i], status_col).strip().lower() == "rejected"]
    if rejected:
        dropped = ", ".join(_cell(rows[i], course_col) or "(no course)" for i in rejected)
        return (
            "already_rejected", label,
            f"the student demoted this to Rejected ({dropped}) — NOT resurrecting it. "
            f"Re-promote the row by hand if the rejection was a mistake, then re-run",
            [], {}, [],
        )

    clean, problems, warnings = validate_corrections(marker, header, label, mode, len(matches))
    if problems:
        return "bad_correction", label, "; ".join(p.split(": ", 1)[-1] for p in problems), [], {}, warnings

    to_flip = [i for i in matches if _cell(rows[i], status_col).strip() != "Finalist"]
    courses = ", ".join(_cell(rows[i], course_col) or "(no course)" for i in matches)
    bits = []
    if to_flip:
        bits.append(f"{len(to_flip)} row(s) -> Finalist")
    if clean:
        bits.append(f"{len(clean)} correction(s) x {len(matches)} row(s): {', '.join(clean)}")
    if not to_flip:
        bits.append("already Finalist")
    detail = f"{'; '.join(bits)} [{courses}]"

    if not to_flip:
        outcome = "already_final"
    elif clean:
        outcome = "corrected"
    else:
        outcome = "flipped"
    return outcome, label, detail, matches, clean, warnings


def main():
    parser = argparse.ArgumentParser(
        description="Apply Stage 4 finalist marker fragments to master_list.csv in one pass."
    )
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--fragments", help="Fragment directory (default .tmp/<slug>/finalists/).")
    parser.add_argument("--csv", help="Master list path (default data/students/<slug>/master_list.csv).")
    parser.add_argument("--dry-run", action="store_true", help="Decide and report; write and delete nothing.")
    args = parser.parse_args()

    slug = args.student
    student_dir = STUDENTS_DIR / slug

    def resolve(value, default):
        if not value:
            return default
        p = Path(value)
        return p if p.is_absolute() else REPO_ROOT / p

    frag_dir = resolve(args.fragments, REPO_ROOT / ".tmp" / slug / "finalists")
    csv_path = resolve(args.csv, student_dir / "master_list.csv")

    # A missing student folder is a typo'd slug — fatal. A missing/empty fragment dir under a
    # real student is the NORMAL end state (every marker already applied, or no report built
    # yet), so it exits 0. Splitting those two apart is what keeps "nothing to do" from
    # looking identical to "you spelled the slug wrong".
    if not student_dir.exists():
        sys.exit(f"ERROR: {student_dir} not found — check the student slug.")
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found — there is nothing to flip finalists into.")

    markers = load_markers(frag_dir) if frag_dir.exists() else []
    if not markers:
        print(f"No finalist markers in {frag_dir} — nothing to flip. (This is a normal end state.)")
        return

    header, rows = load_csv(csv_path)
    print(f"student: {slug} | {len(markers)} marker(s) in {frag_dir} | {len(rows)} row(s) in the list")

    results, all_warnings = [], []
    for path, marker in markers:
        outcome, label, detail, matches, clean, warnings = plan_marker(path, marker, header, rows)
        results.append((path, outcome, label, detail, matches, clean))
        all_warnings.extend(warnings)
        mark = "ok  " if outcome in APPLIED_OUTCOMES else "FAIL"
        print(f"  {mark} [{outcome}] {label}: {detail}")

    for line in all_warnings:
        print(f"  ~ WARNING {line}")

    applied = [r for r in results if r[1] in APPLIED_OUTCOMES]
    failed = [r for r in results if r[1] not in APPLIED_OUTCOMES]
    changing = [r for r in applied if r[4] and (r[1] != "already_final" or r[5])]

    if args.dry_run:
        print(
            f"\n(dry run — {len(changing)} marker(s) would change {csv_path.name}, "
            f"{len(applied)} fragment(s) would be deleted, {len(failed)} kept for a re-run)"
        )
        return

    if applied:
        status_col = header.index("List status")
        for _, outcome, _, _, matches, clean in applied:
            for i in matches:
                row = rows[i]
                row.extend([""] * (len(header) - len(row)))
                if row[status_col].strip() != "Finalist":
                    row[status_col] = "Finalist"
                for column, value in clean.items():
                    row[header.index(column)] = value

        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"\nWrote {csv_path} — {len(changing)} marker(s) applied")

        # Only after the CSV is safely on disk: a fragment deleted before the write would
        # take an unrepeatable flip with it if the write then failed.
        for path, *_ in applied:
            path.unlink()
        print(f"Deleted {len(applied)} applied fragment(s) from {frag_dir}")

    if failed:
        print(f"\n{len(failed)} fragment(s) NOT applied and left in {frag_dir}:")
        for path, outcome, label, detail, _, _ in failed:
            print(f"  ! [{outcome}] {label} ({path.name}): {detail}")
        print("  Fix the row or the marker, then re-run — re-applying an applied marker is a no-op.")

    print(
        f"\nNext: python tools/check_master_list.py --student {slug}\n"
        f"      Run it WITHOUT --check — a narrow filter answers only the question you already "
        f"know to ask."
    )
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
