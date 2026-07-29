"""
sync_shortlist.py — score, dedupe, and append university candidates to the master list.

Reads .tmp/<student-slug>/uni_candidates.json (written by the agent after reviewing
Firecrawl results in Stage 3), computes a desirability score + A/B/C tier, an
admission likelihood (Reach/Match/Safety), and feasibility flags for each candidate,
drops any already present in the student's master_list.csv (by canonical
university+course key), sorts the rest by desirability, and appends them as new rows
with List status "Longlist".

The master list is a plain CSV (data/students/<slug>/master_list.csv) that opens in
Excel / Google Sheets / LibreOffice. It is created with a header row on first run.

This tool NEVER demotes or overwrites existing rows — promotion (Longlist -> Shortlist
-> Finalist) and rejection are agent edits, not a side-effect of syncing.

Scoring weights are per-student: data/students/<slug>/weights.json is REQUIRED and this
tool refuses to run without it (see the 'scoring-weights' skill). Because no student
state is shared, two students can be synced concurrently. Each scored candidate is
appended to data/students/<slug>/score_log.jsonl — the sub-scores, entry_margin, and
weights_id behind a row, none of which the CSV has room to keep.

The CSV is a SCANNING surface, so a candidate's long-form research does not go in it:
`notes` (short, budgeted) becomes the "Notes" cell, while `research_notes` (free length)
is appended to data/students/<slug>/research_notes.md. Cells over CELL_BUDGETS are
reported after a sync and never silently truncated.

--country is REQUIRED and every candidate must match it: Stage 3 runs one country per
pass (see check_one_country). The normal input is written by tools/merge_candidates.py,
which merges the per-university fragments and refuses to emit an incomplete row.

Usage:
    python tools/sync_shortlist.py --student aisyah-rahman --country Australia
    python tools/sync_shortlist.py --student aisyah-rahman --country Australia --dry-run

candidate JSON: a list of objects — see workflows/03_discover_longlist.md for the
full schema. Each carries a "scores" dict (0-5 sub-scores) and an "entry_margin".
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import (  # noqa: E402
    CELL_BUDGETS,
    DEFAULT_LIST_STATUS,
    INFO_SOURCE_UNVERIFIED,
    SHORTLIST_HEADERS,
    WARNINGS_NONE,
    candidate_total_myr,
    classify_admission,
    compute_score,
    course_key,
    feasibility_flags,
    grade_fit_label,
    load_weights,
    tier_for,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

UNI_COL = SHORTLIST_HEADERS.index("University")
COURSE_COL = SHORTLIST_HEADERS.index("Course")


def read_existing(csv_path):
    """Return existing data rows (list of lists), skipping the header. [] if no file."""
    if not csv_path.exists():
        return []
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[1:] if rows else []


def existing_keys(rows):
    """Build the dedupe key set (canonical university+course) from current rows."""
    keys = set()
    for row in rows:
        uni = row[UNI_COL] if len(row) > UNI_COL else ""
        course = row[COURSE_COL] if len(row) > COURSE_COL else ""
        keys.add(course_key(uni, course))
    return keys


def candidate_to_row(c, score, tier, admission, flags):
    """Build a CSV row in SHORTLIST_HEADERS order from a scored candidate.

    Several candidate fields deliberately have no column: `currency` and `total_cost_programme`
    feed "Approx total (MYR)" (see candidate_total_myr), `meets_english` feeds the
    "English short" warning, and `research_notes` goes to research_notes.md. They stay in
    the JSON; the CSV shows the result, not the input.

    "Grades vs entry bar" is derived from entry_margin alone (grade_fit_label) — there is no
    per-candidate override, and no caveat for self-predicted grades: feasibility_flags()
    already stamps "Grades unverified (self-predicted)" in Warnings for such a student, and
    repeating it in a second column just costs 45 chars a row.

    A clean row's "Warnings" is written as "None", not left blank: the master list is the
    client's deliverable and an empty cell reads as an unfinished one. "None" says a human
    looked and there was nothing to flag (see SENTINEL_VALUES in shortlist_schema.py).
    """
    myr = candidate_total_myr(c)
    values = {
        "List status": DEFAULT_LIST_STATUS,
        "Desirability": str(score),
        "Tier": tier,
        "Admission likelihood": admission,
        "Warnings": "; ".join(flags) if flags else WARNINGS_NONE,
        "University": c.get("university", ""),
        "Course": c.get("course", ""),
        "Course at a glance": c.get("course_at_a_glance", ""),
        "Country": c.get("country", ""),
        "City": c.get("city", ""),
        "Student life": c.get("student_life", ""),
        "Subject rank": c.get("subject_rank", ""),
        "Overall rank": c.get("overall_rank", ""),
        "Entry requirements": c.get("entry_requirements", ""),
        "Student grades": c.get("student_grades", ""),
        "Grades vs entry bar": grade_fit_label(c.get("entry_margin")),
        "English req": c.get("english_req", ""),
        "Annual tuition": c.get("annual_tuition", ""),
        "Total tuition": c.get("total_tuition", ""),
        "Est. living/yr": c.get("est_living_per_year", ""),
        "Duration (yrs)": c.get("duration_years", ""),
        "Approx total (MYR)": "" if myr is None else str(myr),
        # Scholarship detail (Toru's #1 priority). Fall back to a legacy single "scholarships" field.
        "Scholarship & portal": c.get("scholarship_portal", c.get("scholarships", "")),
        "Scholarship coverage": c.get("scholarship_coverage", ""),
        "Scholarship competitiveness": c.get("scholarship_competitiveness", ""),
        "How to get the scholarship": c.get("scholarship_how_to", ""),
        "Money to show (visa)": c.get("funds_proof", ""),
        "Work rights after graduating": c.get("post_study_work", ""),
        "Recognised in Malaysia?": c.get("recognised_back_home", ""),
        "How to apply": c.get("application_system", ""),
        "Key deadline": c.get("key_deadline", ""),
        "Intake": c.get("intake", ""),
        "Notes": c.get("notes", ""),
        "Course URL": c.get("course_url", ""),
        "Info source": c.get("source_authority", INFO_SOURCE_UNVERIFIED),
    }
    return [values.get(h, "") for h in SHORTLIST_HEADERS]


def check_one_country(candidates, country):
    """Hard-error unless every candidate's `country` is exactly `country`.

    Stage 3 runs ONE country per session — a rule that lived only as prose in
    workflows/03_discover_longlist.md and so was followed inconsistently (Foo De Mi
    ended up with six Singapore rows for a country she never picked). One country per
    pass is what keeps a session's context small enough to research 35 columns a row,
    and what makes "which country is next?" answerable from the CSV alone.

    Compared case-insensitively on stripped text so "australia" doesn't fail a run,
    but the candidate's own spelling is what lands in the CSV.
    """
    want = (country or "").strip().lower()
    offenders = []
    for c in candidates:
        got = str(c.get("country") or "").strip()
        if got.lower() != want:
            offenders.append(f"{c.get('university', '?')} — country {got or '(blank)'!r}")
    if offenders:
        sys.exit(
            f"ERROR: --country {country!r} but {len(offenders)} candidate(s) say otherwise:\n  "
            + "\n  ".join(offenders)
            + "\nStage 3 syncs ONE country per pass. Split the file and sync each country separately."
        )


def append_research_notes(notes_path, scored):
    """Append each candidate's long-form `research_notes` to research_notes.md.

    This is the other half of the cell budget (CELL_BUDGETS). The CSV's "Notes" column
    holds a <=200-char headline the student can scan; the verification stamps, source
    conflicts and cost traps that used to bloat that cell to 2900 chars live here, under
    a "## <University> - <Course>" heading. Nothing is truncated and nothing is lost —
    the two are separate candidate-JSON fields, so there is no splitting logic to get wrong.

    Skips a candidate whose heading is already present, so a re-sync doesn't duplicate it.
    Returns the number of sections written.
    """
    sections = [(c, str(c.get("research_notes") or "").strip()) for _, _, _, _, c in scored]
    sections = [(c, text) for c, text in sections if text]
    if not sections:
        return 0

    existing = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
    have = {course_key(*_heading_parts(line)) for line in existing.splitlines() if line.startswith("## ")}

    written = 0
    with notes_path.open("a", encoding="utf-8", newline="\n") as f:
        if not existing:
            f.write("# Research notes\n\nThe long-form research behind each master_list row — the "
                    "verification stamps, source conflicts and cost traps that are too long for a "
                    "spreadsheet cell. The CSV's `Notes` column carries the one-line headline.\n")
        for c, text in sections:
            uni, course = c.get("university", ""), c.get("course", "")
            if course_key(uni, course) in have:
                continue
            f.write(f"\n## {uni} - {course}\n\n{text}\n")
            have.add(course_key(uni, course))
            written += 1
    return written


def _heading_parts(line):
    """Split a '## University - Course' heading back into (university, course)."""
    body = line[3:].strip()
    uni, _, course = body.partition(" - ")
    return uni, course


def over_budget_cells(rows):
    """[(University, column, length, budget)] for cells exceeding CELL_BUDGETS.

    Reported, never trimmed: silently truncating a cell would delete verified research.
    check_master_list.py runs the same rule over the whole file.
    """
    uni_col = SHORTLIST_HEADERS.index("University")
    findings = []
    for row in rows:
        for column, budget in CELL_BUDGETS.items():
            value = row[SHORTLIST_HEADERS.index(column)]
            if len(value or "") > budget:
                findings.append((row[uni_col], column, len(value), budget))
    return findings


def append_score_log(log_path, weights_id, scored):
    """Append one JSON line per scored candidate: the audit trail the CSV can't hold.

    Recovers which weights produced a row, the sub-scores behind it, and the entry_margin
    (the only input to Admission likelihood, otherwise discarded). Append-only, so a
    re-sync leaves a history instead of overwriting one. Per-student file: parallel-safe.
    """
    ts = datetime.now().isoformat(timespec="seconds")
    with log_path.open("a", encoding="utf-8", newline="\n") as f:
        for score, tier, admission, flags, c in scored:
            uni, course = course_key(c.get("university"), c.get("course"))
            f.write(json.dumps({
                "ts": ts,
                "weights_id": weights_id,
                "course_key": f"{uni}|{course}",
                "scores": c.get("scores", {}),
                "entry_margin": c.get("entry_margin"),
                "desirability": score,
                "tier": tier,
                "admission": admission,
                "warnings": flags,
            }, ensure_ascii=False) + "\n")


def needs_leading_newline(csv_path):
    """True if the file exists, is non-empty, and its last byte isn't a newline.
    Appending to such a file would fuse the first new row onto the last row."""
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return False
    with csv_path.open("rb") as f:
        f.seek(-1, 2)
        return f.read(1) not in (b"\n", b"\r")


def reorder_to_header(rows, file_header):
    """Re-map rows (built in SHORTLIST_HEADERS order) to an existing file's column
    order. Guards against schema/header drift: an older master_list.csv may carry the
    same columns in a different order (e.g. "Approx total (MYR)" in a different slot).
    Appending schema-order rows to such a file would silently misalign every column.
    Same columns, different order -> remap. Different column set -> refuse (needs migration).
    """
    if file_header == SHORTLIST_HEADERS:
        return rows
    if set(file_header) == set(SHORTLIST_HEADERS):
        idx = [SHORTLIST_HEADERS.index(h) for h in file_header]
        return [[r[i] for i in idx] for r in rows]
    sys.exit(
        "ERROR: master_list.csv columns differ from the current schema "
        "(SHORTLIST_HEADERS). Migrate the file to the schema columns before syncing."
    )


def write_rows(csv_path, rows):
    """Append rows, creating the file with a header row if it doesn't exist yet.
    When appending to an existing file, rows are written in that file's header order,
    not blindly in SHORTLIST_HEADERS order (see reorder_to_header)."""
    is_new = not csv_path.exists()
    if not is_new:
        with csv_path.open(newline="", encoding="utf-8") as f:
            file_header = next(csv.reader(f), None)
        if file_header:
            rows = reorder_to_header(rows, file_header)
    add_newline = needs_leading_newline(csv_path)
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        if add_newline:
            f.write("\r\n")
        writer = csv.writer(f)
        if is_new:
            writer.writerow(SHORTLIST_HEADERS)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Sync scored university candidates into the master list.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument(
        "--country",
        required=True,
        help="The ONE country this pass covers. Every candidate must carry this exact "
        "'country' value; a mismatch is a hard error.",
    )
    parser.add_argument("--input", help="Path to uni_candidates.json (default .tmp/<slug>/uni_candidates.json).")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Score and dedupe but do not write; print what would be added.",
    )
    args = parser.parse_args()

    slug = args.student
    student_dir = STUDENTS_DIR / slug
    if not student_dir.exists():
        sys.exit(f"ERROR: {student_dir} not found. Run init_student.py first.")

    try:
        weights, wmeta = load_weights(slug)
    except FileNotFoundError:
        sys.exit(
            f"ERROR: {student_dir / 'weights.json'} not found.\n"
            f"Scoring weights are PER-STUDENT and must be derived from preferences.json before syncing.\n"
            f"Ask Claude to derive them (the 'scoring-weights' skill).\n"
            f"Never hand-edit weights in tools/shortlist_schema.py — that file is shared and "
            f"collides across concurrent sessions."
        )
    except ValueError as exc:
        sys.exit(f"ERROR: invalid {student_dir / 'weights.json'}: {exc}")
    if wmeta.get("student") not in (None, "", slug):
        sys.exit(f"ERROR: weights.json is for {wmeta['student']!r}, not {slug!r}. Wrong file copied?")
    weights_id = wmeta.get("weights_id", "(unset)")

    input_path = Path(args.input) if args.input else REPO_ROOT / ".tmp" / slug / "uni_candidates.json"
    if not input_path.is_absolute():
        input_path = REPO_ROOT / input_path
    if not input_path.exists():
        sys.exit(f"ERROR: {input_path} not found. Write candidates there first (Stage 3).")

    output_path = student_dir / "master_list.csv"

    # Load profile for feasibility checks (budget). Tolerate a not-yet-filled profile.
    profile = {}
    profile_path = student_dir / "profile.json"
    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            profile = {}

    candidates = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(candidates, list):
        sys.exit("ERROR: uni_candidates.json must be a JSON list of candidate objects.")

    check_one_country(candidates, args.country)

    seen = set(existing_keys(read_existing(output_path)))
    scored = []
    skipped = 0
    for c in candidates:
        key = course_key(c.get("university"), c.get("course"))
        if key in seen:
            skipped += 1
            continue
        seen.add(key)
        score = compute_score(c.get("scores", {}), weights)
        try:
            admission = classify_admission(
                c.get("entry_margin"), c.get("admission_likelihood"), c.get("admission_reason")
            )
        except ValueError as exc:
            sys.exit(f"ERROR: {c.get('university', '?')} — {c.get('course', '?')}: {exc}")
        flags = feasibility_flags(c, profile)
        scored.append((score, tier_for(score), admission, flags, c))

    scored.sort(key=lambda t: t[0], reverse=True)
    rows = [candidate_to_row(c, score, tier, admission, flags) for score, tier, admission, flags, c in scored]

    print(f"student: {slug} | weights: {weights_id}")
    print(f"{len(candidates)} candidates in file | {skipped} duplicates skipped | {len(rows)} new")
    for score, tier, admission, flags, c in scored:
        flag_str = f"  ⚑ {'; '.join(flags)}" if flags else ""
        print(f"  [{tier}] {score:>3}  {admission or '-':<7} {c.get('university','?')} — {c.get('course','?')}{flag_str}")

    over = over_budget_cells(rows)
    if over:
        print(f"\n{len(over)} cell(s) over the length budget — the master list is a scanning surface:")
        for uni, column, length, budget in over[:10]:
            print(f"  ! {uni} — {column}: {length} chars (budget {budget})")
        print("  Move the depth into the candidate's 'research_notes' field; run "
              "tools/check_master_list.py for the full report.")

    if args.dry_run:
        print("\n(dry run — nothing written)")
        return
    if not rows:
        print("\nNothing new to add.")
        return

    write_rows(output_path, rows)
    append_score_log(student_dir / "score_log.jsonl", weights_id, scored)
    written = append_research_notes(student_dir / "research_notes.md", scored)
    print(f"\nAppended {len(rows)} rows to {output_path} (as Longlist)")
    if written:
        print(f"Wrote {written} section(s) to {student_dir / 'research_notes.md'}")


if __name__ == "__main__":
    main()
