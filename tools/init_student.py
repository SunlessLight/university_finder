"""
init_student.py — scaffold a private data bank for one student.

Creates data/students/<slug>/ with a dossiers/ subfolder and writes template
profile.json + preferences.json pre-filled with the schema keys set to null/empty,
so the agent fills them in conversation during Stage 1 (intake) and Stage 2
(aspirations). Refuses to clobber an existing student folder unless --force.

Usage:
    python tools/init_student.py "Aisyah Rahman"
    python tools/init_student.py "Aisyah Rahman" --force

The student's PII lives only under data/students/ (gitignored). Defaults assume a
Malaysian student (home_country = "Malaysia", currency = "MYR").
"""

import argparse
import json
import sys
from pathlib import Path

# Allow running from any cwd: make the tools dir importable for the shared schema.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import slugify  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"


def profile_template(slug, name):
    """Stage-1 profile.json — any unknown field stays null/empty for the agent to fill."""
    return {
        "student_slug": slug,
        "name": name,
        "age": None,
        "gender": None,
        "nationality": None,
        "country_of_residence": None,
        "home_country": "Malaysia",
        "recognition_targets": [],  # e.g. ["MQA","MMC"] — only for regulated professions
        "education_history": [],     # [{institution, qualification, years}]
        "current_program": {"type": None, "institution": None, "expected_completion": None},
        "subjects": [],              # [{subject, grade_or_predicted}]
        "grade_status": None,        # "actual" | "predicted"
        "english_proficiency": {"test": None, "score": None, "test_date_or_planned": None},
        "financial": {
            "budget_per_year": None,
            "total_budget": None,
            "currency": "MYR",
            "funding_source": None,  # self | loan | scholarship-dependent | sponsor
            "scholarship_dependent": None,
            "notes": None,
        },
        "interest_discovery": {
            "decided": None,
            "career_goal": None,
            "subjects_enjoyed": [],
            "work_styles": [],
            "values": [],
            "constraints": [],
        },
        "needs": {
            "halal_food": None,
            "prayer_facilities": None,
            "malaysian_community": None,
            "proximity_to_family": None,
        },
        "notes": None,
    }


def preferences_template():
    """Stage-2 preferences.json template."""
    return {
        "target_countries": [],  # subset of UK / Australia / USA / Singapore/Malaysia / China
        "fields_of_interest": [],
        "specific_courses": [],  # may stay empty -> triggers interest-discovery mode
        "degree_level": None,    # undergrad | foundation | ...
        "intake": None,          # e.g. "2027 Sept"
        "budget_ceiling_per_year": None,
        "total_budget_ceiling": None,
        "currency": "MYR",
        "scholarship_required": None,
        "priorities": [],        # ordered, e.g. ["cost","employability","recognition","ranking","location"]
        "ranking_importance": None,
        "min_subject_rank_pref": None,
        "post_study_work_importance": None,
        "intent_to_migrate": None,
        "deal_breakers": [],
        "location_prefs": [],
        "notes": None,
    }


def main():
    parser = argparse.ArgumentParser(description="Scaffold a student data bank folder.")
    parser.add_argument("name", help="Student's full name (used for the folder slug).")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing student folder.")
    args = parser.parse_args()

    slug = slugify(args.name)
    student_dir = STUDENTS_DIR / slug
    dossiers_dir = student_dir / "dossiers"

    if student_dir.exists() and not args.force:
        sys.exit(
            f"ERROR: {student_dir} already exists. Use --force to overwrite "
            f"(this will reset profile.json / preferences.json)."
        )

    dossiers_dir.mkdir(parents=True, exist_ok=True)

    profile_path = student_dir / "profile.json"
    prefs_path = student_dir / "preferences.json"
    profile_path.write_text(
        json.dumps(profile_template(slug, args.name), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    prefs_path.write_text(
        json.dumps(preferences_template(), indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"Created student data bank: {student_dir}")
    print(f"  - {profile_path.name}     (Stage 1: run student intake to fill)")
    print(f"  - {prefs_path.name} (Stage 2: run aspirations intake to fill)")
    print(f"  - dossiers/         (Stage 5: per-finalist deep dossiers land here)")
    print(f"\nNext: tell Claude \"run student intake for {args.name}\".")


if __name__ == "__main__":
    main()
