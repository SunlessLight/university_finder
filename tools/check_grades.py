"""
check_grades.py — check a student's tidied grades against their programme's grade scale.

Added 2026-10-30 (plans/intake_forms_plan.md T3). The form takes grades as one free-text box, and
AI tidies that text into profile.subjects[] at Stage 1 finalize. This is the check on that step: it
fails any grade impossible for current_program.type, and any tidied list with fewer subjects than the
raw text appears to name, so a dropped subject is caught. It then prints raw and tidied side by side
for Evan's 30-second look, which stays until 20 forms in a row need no correction (tally:
R41 in plans/additionals.md).

Scales: A-Level A*-E. STPM A, A-, B+, B, B-, C+, C, C-, D+, D, F. UEC A1, A2, B3-B6, C7, C8, F9.
IB 1-7 per subject, and a subject named "Total" up to 45. Foundation / Matriculation / Diploma CGPA
0-4.0. Any other programme has no scale, so it never fails on a grade and always raises a review line.

The subject count is a word-splitting guess, so read a count failure against the raw text: a subject
with "and" in its name counts as two.

Usage:
    python tools/check_grades.py --student <slug>

Exit code 1 when anything fails; a review line alone exits 0.
"""

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

LETTER_SCALES = {
    "A-Level": {"A*", "A", "B", "C", "D", "E"},
    "STPM": {"A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"},
    "UEC": {"A1", "A2", "B3", "B4", "B5", "B6", "C7", "C8", "F9"},
}
CGPA_PROGRAMMES = {"Foundation", "Matriculation", "Diploma"}
IB_TOTAL_MAX = 45
CGPA_RE = re.compile(r"^(?:cgpa\s*[:=]?\s*)?(\d+(?:\.\d+)?)$", re.IGNORECASE)
# What separates one subject from the next in free text. The full stop needs a space or the end of
# the text after it, so the "." in "CGPA 3.6" doesn't split.
RAW_SPLIT_RE = re.compile(r"[,;\n]|\band\b|\.(?=\s|$)", re.IGNORECASE)


def grade_problem(program, subject, grade):
    """Why this grade can't exist on this programme's scale, or None if it can."""
    text = str(grade or "").strip()
    if not text:
        return f"{subject}: no grade"
    if program in LETTER_SCALES:
        if text.replace(" ", "").upper() not in LETTER_SCALES[program]:
            return f"{subject}: {text!r} is not a {program} grade"
    elif program == "IB":
        if not text.isdigit():
            return f"{subject}: {text!r} is not an IB grade"
        limit = (0, IB_TOTAL_MAX) if "total" in subject.lower() else (1, 7)
        if not limit[0] <= int(text) <= limit[1]:
            return f"{subject}: {text!r} is outside the IB range {limit[0]}-{limit[1]}"
    elif program in CGPA_PROGRAMMES:
        match = CGPA_RE.match(text)
        if not match or float(match.group(1)) > 4.0:
            return f"{subject}: {text!r} is not a CGPA from 0 to 4.0"
    return None


def raw_subject_count(raw):
    """How many subjects the free text appears to name: the pieces that hold a letter."""
    return sum(1 for piece in RAW_SPLIT_RE.split(raw or "") if re.search(r"[A-Za-z]", piece))


def check(profile):
    """Return (failures, reviews) for one profile. Failures are impossible; reviews want a look."""
    program = (profile.get("current_program") or {}).get("type") or "A-Level"
    subjects = profile.get("subjects") or []
    raw = (profile.get("_intake_raw") or {}).get("grades")

    failures, reviews = [], []
    if not subjects:
        failures.append("no tidied grades in subjects[]")
    known = program in LETTER_SCALES or program == "IB" or program in CGPA_PROGRAMMES
    if known:
        for item in subjects:
            problem = grade_problem(program, item.get("subject") or "(no subject)", item.get("grade_or_predicted"))
            if problem:
                failures.append(problem)
    else:
        reviews.append(f"programme {program!r} has no grade scale here: read the grades by hand")
    named = raw_subject_count(raw)
    if subjects and named > len(subjects):
        failures.append(f"raw text appears to name {named} subjects but the tidied list has {len(subjects)}")
    return failures, reviews


def print_side_by_side(profile):
    raw = (profile.get("_intake_raw") or {}).get("grades") or "(no free text on this profile)"
    print("Raw:")
    for line in raw.splitlines():
        print(f"  {line}")
    print("Tidied:")
    for item in profile.get("subjects") or []:
        print(f"  {item.get('subject')}: {item.get('grade_or_predicted')}")


def main():
    parser = argparse.ArgumentParser(description="Check a student's tidied grades against their programme.")
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    args = parser.parse_args()

    path = STUDENTS_DIR / args.student / "profile.json"
    if not path.exists():
        sys.exit(f"ERROR: {path} not found.")
    profile = json.loads(path.read_text(encoding="utf-8"))

    failures, reviews = check(profile)
    print(f"{args.student}: programme {(profile.get('current_program') or {}).get('type')}\n")
    print_side_by_side(profile)
    print()
    for line in failures:
        print(f"FAIL: {line}")
    for line in reviews:
        print(f"REVIEW: {line}")
    if not failures and not reviews:
        print("OK: every grade fits the programme, and no subject looks dropped.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
