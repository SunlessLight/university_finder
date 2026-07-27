"""
init_student.py — scaffold a private data bank for one student.

Creates data/students/<slug>/ with a reports/ subfolder and writes template
profile.json + preferences.json pre-filled with the schema keys set to null/empty.

The normal way in is the Google Form (workflows/01_intake.md -> ingest_form_csv.py,
which imports the two templates below). This CLI is the manual fallback for
scaffolding one student's folder by hand; you then fill the JSON yourself.
Refuses to clobber an existing student folder unless --force.

profile_template() / preferences_template() are the SINGLE SOURCE OF TRUTH for the
data-bank shape — a finalized profile.json should match this key set exactly.

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
        "ethnicity": None,           # PDPA-sensitive; informs scholarship-eligibility research (e.g. Bumiputra vs non-Bumiputra funds), never a desirability input
        "country_of_residence": None,
        "home_country": "Malaysia",
        "recognition_targets": [],  # e.g. ["MQA","MMC"] — only for regulated professions
        "education_history": [],     # [{institution, qualification, years}]
        "current_program": {"type": None, "institution": None, "expected_completion": None},
        "subjects": [],              # [{subject, grade_or_predicted}]
        "grade_status": None,        # "actual" | "predicted" | "expected" (self-predicted / "confident of getting" — provisional)
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
            # "Support & belonging" — broad, faith/culture-neutral. All PDPA-sensitive → only set
            # from what the student volunteers; unmentioned stays null (not False).
            "diet_halal": None,
            "diet_vegetarian_vegan": None,
            "diet_other": None,
            "worship_facilities": None,       # any faith
            "diaspora_community": None,       # a home-country community nearby (Malaysian or other)
            "proximity_to_family": None,
            "disability_accessibility": None,
            "wellbeing_support": None,        # mental-health / counselling
            "lgbtq_friendly": None,
            "personal_safety": None,
            "climate_weather": None,
        },
        "notes": None,
    }


def preferences_template():
    """Stage-2 preferences.json template."""
    return {
        "target_countries": [],  # subset of UK / Australia / USA / Singapore/Malaysia / China / Japan
        "fields_of_interest": [],
        "specific_courses": [],  # may stay empty -> triggers interest-discovery mode
        "degree_level": None,    # undergrad | foundation | ...
        "intake": None,          # e.g. "2027 Sept"
        "budget_ceiling_per_year": None,
        "total_budget_ceiling": None,
        "currency": "MYR",
        "scholarship_required": None,
        "scholarship_interests": None,  # free-text: scholarships the student wants researched (a Stage 3/4 hint, not a filter)
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
    reports_dir = student_dir / "reports"

    if student_dir.exists() and not args.force:
        sys.exit(
            f"ERROR: {student_dir} already exists. Use --force to overwrite "
            f"(this will reset profile.json / preferences.json)."
        )

    reports_dir.mkdir(parents=True, exist_ok=True)

    profile_path = student_dir / "profile.json"
    prefs_path = student_dir / "preferences.json"
    profile_path.write_text(
        json.dumps(profile_template(slug, args.name), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    prefs_path.write_text(
        json.dumps(preferences_template(), indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"Created student data bank: {student_dir}")
    print(f"  - {profile_path.name}     (Stage 1: who the student is — fill by hand)")
    print(f"  - {prefs_path.name} (Stage 1: what they want — fill by hand)")
    print(f"  - reports/          (Stage 4: per-finalist deep reports land here)")
    print("\nNote: the normal intake path is the Google Form — see workflows/01_intake.md.")
    print("Filled both files by hand? Next: derive weights.json, then Stage 3 (discover longlist).")


if __name__ == "__main__":
    main()
