"""
ingest_form_csv.py — batch-scaffold student data banks from a Google Forms CSV export.

This is the deterministic half of Stage 1 intake (see workflows/01_intake.md) — the only on-ramp.
It reads a Google Forms "responses" CSV (one row per respondent), and for each row that gave
consent it creates data/students/<slug>/ with a filled profile.json + preferences.json, using
the SAME templates as init_student.py so the shape never drifts.

The mechanically-mappable fields (name, age, budget, countries, priorities, ...) are filled
here. The judgment-heavy bits are left for the agent (Claude) to finalize in workflow 01 and
are flagged in a top-level "_needs_review" list on profile.json:
  - self-predicted grades -> confirm, or upgrade grade_status when real results arrive
  - the regulated-profession answer -> recognition_targets (best-effort auto-fill + verify)
  - a respondent who gave no field of study at all (nothing to search on)

Columns are matched by a distinctive SUBSTRING of each question title (case-insensitive), so
light rewording of the form questions won't break the mapping. QUESTION_MAP below is the single
source of truth for the column<->field wiring; keep it in step with the form spec in
workflows/01_intake.md.

Usage:
    python tools/ingest_form_csv.py data/form/responses.csv
    python tools/ingest_form_csv.py data/form/responses.csv --dry-run
    python tools/ingest_form_csv.py data/form/responses.csv --force

data/form/ is gitignored (PII), same class as data/students/.
"""

import argparse
import csv
import json
import sys
from pathlib import Path

# Allow running from any cwd: make the tools dir importable for shared helpers/templates.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import slugify  # noqa: E402
from init_student import profile_template, preferences_template  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# --------------------------------------------------------------------------- #
# Column -> logical-key mapping. Each entry is (distinctive substring, key).
# For every CSV header we scan these in order and take the FIRST substring the
# header contains, so put more-specific substrings before looser ones.
# --------------------------------------------------------------------------- #
QUESTION_MAP = [
    ("consent", "consent"),
    ("email", "email"),
    ("full name", "name"),
    ("your name", "name"),  # Forms often exports the name Q's header merged with the section title
    ("your age", "age"),
    ("gender", "gender"),
    ("nationality", "nationality"),
    ("race", "ethnicity"),  # PDPA-sensitive; used for scholarship-eligibility research only
    ("live in now", "country_of_residence"),
    ("live and work after", "post_grad_location"),  # aspiration, NOT home_country (stays Malaysia)
    ("studying now", "current_type"),
    ("which college", "current_institution"),
    ("when do you graduate", "current_completion"),  # current form's wording
    ("when do you finish", "current_completion"),    # legacy fallback (older form)
    ("list each subject", "grades_raw"),             # legacy paragraph-grades form; structured subjects handled separately
    ("actual results or predicted", "grade_status"),
    ("which english test", "english_test"),
    ("english test score", "english_score"),
    ("english score", "english_score"),  # current form: "write down english score"
    ("will you take it", "english_date"),
    ("total budget", "total_budget"),
    ("whole degree", "total_budget"),  # this form's wording: "your budget (RM) for the whole degree"
    ("per-year budget", "budget_per_year"),
    ("scholarship a must", "scholarship_gate"),  # current form: Yes/No -> scholarship_required (clean gate)
    ("planning to apply", "scholarship_interests"),  # current form: which scholarships to research (a hint)
    ("how will you fund", "funding_plan"),  # merged funding-reality question (legacy)
    ("how will you pay", "funding_source"),  # legacy fallback (older form)
    ("win a scholarship", "scholarship_dependent"),  # legacy fallback (older form)
    ("regulated profession", "regulated_profession"),
    ("belonging", "needs"),        # "support & belonging needs" (preferred wording)
    ("personal needs", "needs"),   # legacy fallback (older form)
    # preferences
    ("which countries", "target_countries"),
    ("broad area", "fields_of_interest"),   # current form: "Broad Area of Study" dropdown
    ("field or subject", "fields_of_interest"),  # legacy fallback (older form)
    ("already know the exact course", "decided"),
    ("name the course", "specific_courses"),
    ("degree level", "degree_level"),
    ("want to start", "intake"),
    ("#1 priority", "priority_1"),
    ("#2 priority", "priority_2"),
    ("#3 priority", "priority_3"),
    ("how important is university ranking", "ranking_importance"),
    ("work abroad", "work_abroad"),
    ("deal-breaker", "deal_breakers"),
    ("location preference", "location_prefs"),
    # NOTE: the old interest-discovery questions (career goal / what you enjoy / work styles /
    # values / constraints) were removed from the form, and the career-backwards branch that
    # consumed them was dropped on 2026-07-25 along with workflows/02_aspirations_intake.md.
    # A student who names a broad area but no exact course is normal — Stage 3 discovers courses
    # inside that area. See workflows/01_intake.md, finalize step 5.
]

# The six supported destination sets (preferences.target_countries). Normalize
# the form's checkbox labels onto these exact tokens.
COUNTRY_NORMALIZE = {
    "uk": "UK",
    "united kingdom": "UK",
    "australia": "Australia",
    "usa": "USA",
    "united states": "USA",
    "us": "USA",
    "singapore-malaysia": "Singapore/Malaysia",
    "singapore/malaysia": "Singapore/Malaysia",
    "singapore": "Singapore/Malaysia",
    "malaysia": "Singapore/Malaysia",
    "china": "China",
    "japan": "Japan",
}

# Priority dropdown labels -> short tokens used in preferences.priorities.
PRIORITY_NORMALIZE = {
    "cost": "cost",
    "scholarship": "scholarship",
    "ranking": "ranking",
    "employability": "employability",
    "recognition back home": "recognition",
    "recognition": "recognition",
    "location": "location",
    "hands-on experience": "hands-on experience",
}

# Per-category priority SLIDERS (the current form). Instead of three #1/#2/#3 dropdowns, the form asks
# "Rank Your Priorities (1 = least important, 7 = Most important) ... [<Category>]" as eight linear-scale
# columns. We detect them by the shared "rank your priorities" marker in the header + the bracketed
# category, map each category to a priority token, then order tokens by their numeric value (descending)
# to produce the same ordered `priorities` list the dropdown form produced. CANONICAL_SLIDER_ORDER breaks
# ties deterministically (form column order) so equal slider values yield a stable ranking.
SLIDER_MARKER = "rank your priorities"
SLIDER_CATEGORY_MAP = {
    "cost": "cost",
    "scholarship": "scholarship",
    "university ranking": "ranking",
    "course ranking": "course_quality",  # course-level standing -> course_match (scoring-weights skill)
    "employability": "employability",
    "recognition": "recognition",
    "location": "location",
    "hands-on": "hands-on experience",
}
CANONICAL_SLIDER_ORDER = [
    "cost", "scholarship", "ranking", "course_quality",
    "employability", "recognition", "location", "hands-on experience",
]

# NOTE: priority sliders are now a 1-8 linear scale (were 1-7). The ordering below is scale-agnostic
# (it sorts by value), so nothing breaks; but `ranking_importance` now carries a 1-8 value — the
# scoring-weights skill should read it on that scale.

# Subject dropdown labels -> canonical subject names. The form's subject dropdowns use short/quirky
# labels (e.g. "Physic", "Math"); normalise them to clean names for profile.subjects[]. Keyed by the
# lowercased dropdown label; an unlisted label passes through verbatim (extend this map with any new
# dropdown option). "None" is handled upstream (a skipped subject), so it isn't listed here.
SUBJECT_NORMALIZE = {
    "physic": "Physics",
    "physics": "Physics",
    "math": "Mathematics",
    "maths": "Mathematics",
    "mathematics": "Mathematics",
    "further math": "Further Mathematics",
    "further maths": "Further Mathematics",
    "further mathematics": "Further Mathematics",
    "add math": "Additional Mathematics",
    "add maths": "Additional Mathematics",
    "additional math": "Additional Mathematics",
    "additional mathematics": "Additional Mathematics",
    "chemistry": "Chemistry",
    "biology": "Biology",
    "econs": "Economics",
    "economic": "Economics",
    "economics": "Economics",
    "account": "Accounting",
    "accounting": "Accounting",
    "computing": "Computer Science",
    "computer science": "Computer Science",
    "business": "Business",
    "business studies": "Business",
}


def _normalize_subject(name):
    """Map a subject dropdown label to its canonical name; pass through unknown labels verbatim."""
    cleaned = _clean(name)
    return SUBJECT_NORMALIZE.get(cleaned.lower(), cleaned)


# "Broad Area of Study" grid — the form renders eight per-area columns; only the column matching the
# chosen broad area holds the specific course (e.g. "Engineering & Built Environment" = "Mechanical
# Engineering"). We detect these columns by a distinctive substring of each area label, then collect
# any non-empty cell across them as preferences.specific_courses.
GRID_CATEGORY_SUBSTRINGS = [
    "arts, humanities",
    "media, communication",
    "business, finance",
    "computer science",
    "engineering & built",
    "pure & applied",
    "health & medical",
    "education & teaching",
]

# "Support & belonging" checkbox labels -> needs.* boolean keys. Matched by substring, so
# reworded labels still land as long as the keyword survives. Order matters only where one
# substring could shadow another (none do here).
NEEDS_NORMALIZE = {
    "halal": "diet_halal",
    "vegetarian": "diet_vegetarian_vegan",
    "vegan": "diet_vegetarian_vegan",
    "other diet": "diet_other",
    "dietary": "diet_other",
    "worship": "worship_facilities",
    "prayer": "worship_facilities",
    "faith": "worship_facilities",
    "religio": "worship_facilities",
    "community": "diaspora_community",
    "diaspora": "diaspora_community",
    "malaysian": "diaspora_community",
    "family": "proximity_to_family",
    "disab": "disability_accessibility",
    "accessib": "disability_accessibility",
    "wheelchair": "disability_accessibility",
    "mental": "wellbeing_support",
    "wellbeing": "wellbeing_support",
    "well-being": "wellbeing_support",
    "counsel": "wellbeing_support",
    "lgbt": "lgbtq_friendly",
    "queer": "lgbtq_friendly",
    "safety": "personal_safety",
    "safe": "personal_safety",
    "climate": "climate_weather",
    "weather": "climate_weather",
}

# Merged "how will you fund this degree?" answer -> (funding_source label, scholarship_required,
# scholarship_dependent). Scanned in order; first matching substring wins, so the most-dependent
# ("only ... full scholarship") is checked before the looser "family/self" phrasing.
FUNDING_NORMALIZE = [
    ("only", ("Scholarship-dependent (full/near-full)", True, True)),
    ("near-full", ("Scholarship-dependent (full/near-full)", True, True)),
    ("full scholarship", ("Scholarship-dependent (full/near-full)", True, True)),
    ("partial", ("Needs partial scholarship/aid", True, False)),
    ("aid", ("Needs partial scholarship/aid", True, False)),
    ("family", ("Family/self-funded", False, False)),
    ("self", ("Family/self-funded", False, False)),
    ("cover", ("Family/self-funded", False, False)),
]


def _funding_from_plan(answer):
    """Map the merged funding answer to (funding_source, scholarship_required, scholarship_dependent),
    or None if the answer is blank/unrecognized (caller falls back to the legacy two questions)."""
    low = _clean(answer).lower()
    if not low:
        return None
    for substr, result in FUNDING_NORMALIZE:
        if substr in low:
            return result
    return None

# Best-effort recognition targets per regulated profession (MQA + the professional
# body / accord). The agent VERIFIES these in workflows/01_intake.md — see the guardrail on
# recognition in 00_overview.md. "None" -> [].
PROFESSION_RECOGNITION = {
    "medicine": ["MQA", "MMC"],
    "engineering": ["MQA", "BEM", "Washington Accord"],
    "law": ["MQA", "LPQB"],
    "accounting": ["MQA", "MIA"],
    "pharmacy": ["MQA", "Pharmacy Board Malaysia"],
    "dentistry": ["MQA", "MDC"],
    "architecture": ["MQA", "LAM"],
    "nursing": ["MQA", "Nursing Board Malaysia"],
}


# --------------------------------------------------------------------------- #
# Small parsing helpers.
# --------------------------------------------------------------------------- #
def _clean(value):
    """Strip a cell to a clean string, or '' for empty/None."""
    return (value or "").strip()


def _split_multi(value):
    """Split a Google Forms multi-select cell (comma-separated) into a clean list.

    Forms joins checkbox answers with ', '. Labels themselves can contain commas,
    which Forms does not escape — this is a best-effort split; the agent can fix
    the rare mangled case in review.
    """
    return [part.strip() for part in _clean(value).split(",") if part.strip()]


def _yes(value):
    """Map a Yes/No answer to a bool, or None if blank/unclear."""
    v = _clean(value).lower()
    if v.startswith("y"):
        return True
    if v.startswith("n"):
        return False
    return None


def _as_list(value):
    """A single free-text answer -> a one-element list (or [] if blank)."""
    v = _clean(value)
    return [v] if v else []


def build_col_index(fieldnames):
    """Map each CSV header to its logical key via QUESTION_MAP substring match.

    Returns {logical_key: header}. If two headers match the same key, the first
    one wins (later duplicates are ignored) so the mapping stays deterministic.
    """
    index = {}
    for header in fieldnames or []:
        low = (header or "").lower()
        for substr, key in QUESTION_MAP:
            if substr in low and key not in index:
                index[key] = header
                break
    return index


def get(row, col_index, key):
    """Fetch the cleaned cell for a logical key, or '' if the column is absent."""
    header = col_index.get(key)
    return _clean(row.get(header)) if header else ""


# --------------------------------------------------------------------------- #
# Row -> (profile, preferences) mapping.
# --------------------------------------------------------------------------- #
def map_row(row, col_index, slider_cols=None, subject_cols=None, grid_cols=None, assume_consent=False):
    """Turn one CSV row into (slug, profile_dict, preferences_dict, needs_review).

    Returns (None, ...) with a reason if the row should be skipped.

    Consent (PDPA gate): an explicit "No" always skips. A blank/absent consent
    answer skips too UNLESS assume_consent is set (the --assume-consent escape
    hatch, for internal runs on a form that has no consent question). We never
    invent a consent value in the data; assume_consent only relaxes the gate.
    """
    name = get(row, col_index, "name")
    if not name:
        return None, None, None, None, "no name"

    consent = get(row, col_index, "consent")
    if _yes(consent) is False:
        return None, None, None, None, "consent declined"
    if not consent and not assume_consent:
        return None, None, None, None, "no consent (use --assume-consent for a form without a consent question)"

    slug = slugify(name)
    profile = profile_template(slug, name)
    prefs = preferences_template()
    needs_review = []
    intake_raw = {}
    slider_cols = slider_cols or {}
    subject_cols = subject_cols or []
    grid_cols = grid_cols or []

    email = get(row, col_index, "email")

    # --- profile: identity -------------------------------------------------- #
    profile["age"] = get(row, col_index, "age") or None
    profile["gender"] = get(row, col_index, "gender") or None
    profile["nationality"] = get(row, col_index, "nationality") or None
    profile["ethnicity"] = get(row, col_index, "ethnicity") or None  # scholarship-eligibility research only
    profile["country_of_residence"] = get(row, col_index, "country_of_residence") or None
    # NOTE: home_country stays the template default ("Malaysia"). The "where do you want to live
    # and work after graduating" answer is a post-study *aspiration* (captured in notes below +
    # preferences.intent_to_migrate), NOT the student's home country — don't overwrite it here.
    post_grad_location = get(row, col_index, "post_grad_location")

    # --- profile: current program ------------------------------------------ #
    profile["current_program"] = {
        "type": get(row, col_index, "current_type") or None,
        "institution": get(row, col_index, "current_institution") or None,
        "expected_completion": get(row, col_index, "current_completion") or None,
    }

    # --- profile: grades ---------------------------------------------------- #
    # Current form: structured dropdown pairs -> build subjects[] deterministically here. The grade
    # question asks what the student is "confident of getting" (a self-prediction), so grade_status
    # is "expected" — provisional, surfaced as a warning in the longlist until real/official grades.
    subjects = _build_subjects(row, subject_cols)
    if subjects:
        profile["subjects"] = subjects
        # The dropdown path IS the self-prediction path, whatever the exact question wording, so
        # stamp "expected" unconditionally. (This used to require the literal word "confident" in
        # the grade header, while _subject_columns also accepted "select the grade" — a reworded
        # form then built subjects[], left grade_status None, and still emitted the review line
        # below asserting grade_status=expected.) A legacy explicit column still overrides, below.
        profile["grade_status"] = "expected"
        needs_review.append(
            "grades are self-predicted (grade_status=expected) — provisional until actual/official predicted results"
        )
    # Explicit "actual vs predicted" column (legacy) still wins if present.
    grade_status = get(row, col_index, "grade_status").lower()
    if grade_status.startswith("actual"):
        profile["grade_status"] = "actual"
    elif grade_status.startswith("predict"):
        profile["grade_status"] = "predicted"
    # Legacy paragraph-grades form (no structured columns) — stage the free-text for the agent.
    if not subjects:
        if profile["grade_status"] is None:
            grades_header = (col_index.get("grades_raw") or "").lower()
            if "predict" in grades_header:
                profile["grade_status"] = "predicted"
            elif "actual" in grades_header:
                profile["grade_status"] = "actual"
        grades_raw = get(row, col_index, "grades_raw")
        if grades_raw:
            intake_raw["grades"] = grades_raw
            needs_review.append("parse '_intake_raw.grades' into subjects[] (grade_status already set)")

    # --- profile: english -------------------------------------------------- #
    english_test = get(row, col_index, "english_test")
    profile["english_proficiency"] = {
        "test": None if english_test.lower().startswith("none") or not english_test else english_test,
        "score": get(row, col_index, "english_score") or None,
        "test_date_or_planned": get(row, col_index, "english_date") or None,
    }

    # --- profile + preferences: money (asked once, copied to both) ---------- #
    total_budget = get(row, col_index, "total_budget") or None
    budget_per_year = get(row, col_index, "budget_per_year") or None

    # Scholarship gate: prefer the dedicated "Is scholarship a must?" Yes/No (current form) — a clean
    # gate. Else fall back to the merged "how will you fund" question, then the legacy pay/win pair.
    gate = _yes(get(row, col_index, "scholarship_gate"))
    if gate is not None:
        funding_source = None
        scholarship_required = gate
        scholarship_dep = gate
    else:
        funding = _funding_from_plan(get(row, col_index, "funding_plan"))
        if funding:
            funding_source, scholarship_required, scholarship_dep = funding
        else:
            funding_source = get(row, col_index, "funding_source") or None
            scholarship_dep = _yes(get(row, col_index, "scholarship_dependent"))
            scholarship_required = scholarship_dep

    profile["financial"] = {
        "budget_per_year": budget_per_year,
        "total_budget": total_budget,
        "currency": "MYR",
        "funding_source": funding_source,
        "scholarship_dependent": scholarship_dep,
        "notes": None,
    }
    prefs["total_budget_ceiling"] = total_budget
    prefs["budget_ceiling_per_year"] = budget_per_year
    prefs["scholarship_required"] = scholarship_required
    prefs["scholarship_interests"] = get(row, col_index, "scholarship_interests") or None

    # --- profile: recognition (best-effort; agent verifies) ---------------- #
    professions = _split_multi(get(row, col_index, "regulated_profession"))
    targets = []
    for prof in professions:
        key = prof.strip().lower()
        if key in ("none", "none of these", ""):
            continue
        for pkey, vals in PROFESSION_RECOGNITION.items():
            if pkey in key:
                for v in vals:
                    if v not in targets:
                        targets.append(v)
    if targets:
        profile["recognition_targets"] = targets
        needs_review.append(
            f"verify recognition_targets (auto-filled from: {', '.join(professions)})"
        )

    # --- profile: personal needs ------------------------------------------- #
    needs_selected = _split_multi(get(row, col_index, "needs"))
    for label in needs_selected:
        low = label.lower()
        for token, key in NEEDS_NORMALIZE.items():
            if token in low:
                profile["needs"][key] = True

    # --- preferences: what they want --------------------------------------- #
    kept_countries, dropped_countries = _normalize_countries(get(row, col_index, "target_countries"))
    prefs["target_countries"] = kept_countries
    prefs["fields_of_interest"] = _as_list(get(row, col_index, "fields_of_interest"))
    # specific_courses: current form encodes the exact course in the "Broad Area of Study" grid (only the
    # column matching the chosen area is filled). Collect non-empty grid cells; else legacy free-text.
    grid_courses = [c for c in (_clean(row.get(h)) for h in grid_cols) if c]
    prefs["specific_courses"] = grid_courses or _split_multi(get(row, col_index, "specific_courses"))
    prefs["degree_level"] = get(row, col_index, "degree_level").lower() or None
    prefs["intake"] = _normalize_intake(get(row, col_index, "intake"))

    # Priorities: prefer the per-category sliders (current form); fall back to #1/#2/#3 dropdowns.
    prefs["priorities"] = _build_priorities_from_sliders(row, slider_cols) or _build_priorities(row, col_index)

    ranking_importance = get(row, col_index, "ranking_importance") or None
    if not ranking_importance and "ranking" in slider_cols:
        # No dedicated 1-5 ranking-importance question — read the [University Ranking] slider value.
        ranking_importance = _clean(row.get(slider_cols["ranking"])) or None
    prefs["ranking_importance"] = ranking_importance
    prefs["deal_breakers"] = _as_list(get(row, col_index, "deal_breakers"))
    prefs["location_prefs"] = _split_multi(get(row, col_index, "location_prefs"))

    work_abroad = get(row, col_index, "work_abroad")
    prefs["intent_to_migrate"] = _yes(work_abroad)
    prefs["post_study_work_importance"] = work_abroad or None

    # --- decided / undecided on course ------------------------------------- #
    # An empty specific_courses is the NORMAL case: the student picked a Broad Area and left the
    # course grid blank, and Stage 3 discovers courses inside that area. Only flag for review when
    # there is no field of study either — then there is genuinely nothing to search on.
    decided = _yes(get(row, col_index, "decided"))
    if decided is False or not prefs["specific_courses"]:
        profile["interest_discovery"]["decided"] = False
        if not prefs["fields_of_interest"]:
            needs_review.append(
                "no field of study and no course given — contact the student before Stage 3"
            )
    else:
        profile["interest_discovery"]["decided"] = True

    # --- dropped target countries (don't lose them silently) --------------- #
    if dropped_countries:
        joined = ", ".join(dropped_countries)
        prefs["notes"] = (
            f"Requested target countries not in the 6 supported destination sets (UK / Australia / USA / "
            f"Singapore-Malaysia / China / Japan), so NOT in target_countries: {joined}. "
            f"Decide with the student whether to research them out-of-band."
        )
        needs_review.append(f"target_countries dropped unsupported destination(s): {joined}")

    # --- provenance + staging ---------------------------------------------- #
    note_bits = ["Ingested from Google Form."]
    if email:
        note_bits.append(f"Contact: {email}")
    if post_grad_location:
        note_bits.append(f"Wants to live/work after graduating in: {post_grad_location}.")
    profile["notes"] = " ".join(note_bits)
    if intake_raw:
        profile["_intake_raw"] = intake_raw
    if needs_review:
        profile["_needs_review"] = needs_review

    return slug, profile, prefs, needs_review, None


def _normalize_intake(value):
    """Intake never filters/scores — it only picks the application cycle. A blank answer or an
    explicit 'flexible / not sure' collapses to 'Flexible' (research all intakes); anything else
    (e.g. 'Sept 2027') is kept verbatim. Never invents a date."""
    v = _clean(value)
    low = v.lower()
    if not v or "flex" in low or "not sure" in low or "unsure" in low or "any" in low:
        return "Flexible"
    return v


def _normalize_countries(value):
    """Map the checkbox labels onto the 6 supported destination sets.

    Returns (kept_tokens, dropped_labels): dropped_labels are answers we couldn't map (e.g. "Canada",
    which isn't one of the 6 sets) so the caller can report them instead of losing them silently.
    """
    out, dropped = [], []
    for label in _split_multi(value):
        token = COUNTRY_NORMALIZE.get(label.strip().lower())
        if token:
            if token not in out:
                out.append(token)
        elif label not in dropped:
            dropped.append(label)
    return out, dropped


def _build_priorities(row, col_index):
    out = []
    for key in ("priority_1", "priority_2", "priority_3"):
        label = get(row, col_index, key).strip().lower()
        token = PRIORITY_NORMALIZE.get(label, label) if label else None
        if token and token not in out:
            out.append(token)
    return out


def _slider_columns(fieldnames):
    """Return {priority_token: header} for the per-category priority sliders present in this form.

    A slider header contains the shared marker ("rank your priorities") plus a bracketed category
    ("... [Cost]"). Matched by substring so light rewording survives. Empty if the form uses the
    legacy #1/#2/#3 dropdowns instead.
    """
    cols = {}
    for header in fieldnames or []:
        low = (header or "").lower()
        if SLIDER_MARKER not in low:
            continue
        for cat_substr, token in SLIDER_CATEGORY_MAP.items():
            if cat_substr in low and token not in cols:
                cols[token] = header
                break
    return cols


def _build_priorities_from_sliders(row, slider_cols):
    """Order the slider tokens by their numeric value (desc), tie-broken by CANONICAL_SLIDER_ORDER.

    Blank or non-numeric slider cells are skipped. Returns [] if no usable values (caller falls back
    to the legacy dropdown builder).
    """
    scored = []
    for token, header in slider_cols.items():
        raw = _clean(row.get(header))
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        tie = CANONICAL_SLIDER_ORDER.index(token) if token in CANONICAL_SLIDER_ORDER else len(CANONICAL_SLIDER_ORDER)
        scored.append((-value, tie, token))
    scored.sort()
    return [token for _, _, token in scored]


def _subject_columns(fieldnames):
    """Return ordered (subject_header, grade_header) pairs for the structured subject dropdowns.

    The current form asks each subject as a pair of adjacent columns: "N. List your ... subject" and
    "N. Select the grade you are confident of getting ...". We collect the subject-name headers and
    grade headers separately (in CSV column order, which alternates subject, grade, subject, grade)
    and zip them. Empty for the legacy paragraph-grades form (caller falls back to grades_raw).
    """
    subject_headers, grade_headers = [], []
    for header in fieldnames or []:
        low = (header or "").lower()
        if "grade" in low and ("confident" in low or "select the grade" in low):
            grade_headers.append(header)
        elif "list your" in low and "subject" in low:
            subject_headers.append(header)
    return list(zip(subject_headers, grade_headers))


def _grid_columns(fieldnames):
    """Return the headers of the "Broad Area of Study" grid (the eight per-area course columns)."""
    cols = []
    for header in fieldnames or []:
        low = (header or "").lower()
        if any(sub in low for sub in GRID_CATEGORY_SUBSTRINGS):
            cols.append(header)
    return cols


def _build_subjects(row, subject_cols):
    """Build subjects[] from the structured dropdown pairs, skipping empty / 'None' subject cells.

    The caller stamps grade_status = "expected" whenever this returns anything: the dropdowns ask
    what the student is confident of getting, i.e. a self-prediction.
    """
    subjects = []
    for subject_header, grade_header in subject_cols:
        name = _clean(row.get(subject_header))
        if not name or name.lower() == "none":
            continue
        subjects.append({
            "subject": _normalize_subject(name),
            "grade_or_predicted": _clean(row.get(grade_header)) or None,
        })
    return subjects


# --------------------------------------------------------------------------- #
# Main.
# --------------------------------------------------------------------------- #
def main():
    parser = argparse.ArgumentParser(description="Batch-scaffold student folders from a Google Forms CSV.")
    parser.add_argument("csv_path", help="Path to the Google Forms responses CSV export.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing student folders.")
    parser.add_argument("--dry-run", action="store_true", help="Report what would happen; write nothing.")
    parser.add_argument(
        "--assume-consent",
        action="store_true",
        help="Treat a blank/absent consent answer as consent given (internal runs on a form "
        "with no consent question). An explicit 'No' is still always skipped.",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found.")

    with csv_path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        col_index = build_col_index(reader.fieldnames)
        slider_cols = _slider_columns(reader.fieldnames)
        subject_cols = _subject_columns(reader.fieldnames)
        grid_cols = _grid_columns(reader.fieldnames)
        rows = list(reader)

    if "name" not in col_index:
        sys.exit(
            "ERROR: could not find a 'full name' column. Check the CSV headers against "
            "QUESTION_MAP / the form spec in workflows/01_intake.md."
        )

    created, skipped, review_flags = [], [], {}
    seen_slugs = set()

    for i, row in enumerate(rows, start=1):
        slug, profile, prefs, needs_review, skip_reason = map_row(
            row, col_index, slider_cols, subject_cols, grid_cols, args.assume_consent
        )
        if skip_reason:
            skipped.append((i, get(row, col_index, "name") or "(no name)", skip_reason))
            continue

        student_dir = STUDENTS_DIR / slug
        if slug in seen_slugs:
            skipped.append((i, profile["name"], f"duplicate slug '{slug}' in this CSV"))
            continue
        if student_dir.exists() and not args.force:
            skipped.append((i, profile["name"], f"folder '{slug}' exists (use --force)"))
            continue
        seen_slugs.add(slug)

        if not args.dry_run:
            (student_dir / "reports").mkdir(parents=True, exist_ok=True)
            (student_dir / "profile.json").write_text(
                json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            (student_dir / "preferences.json").write_text(
                json.dumps(prefs, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        created.append(slug)
        if needs_review:
            review_flags[slug] = needs_review

    # --- summary ------------------------------------------------------------ #
    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}Read {len(rows)} row(s) from {csv_path.name}.")
    print(f"{prefix}Created {len(created)} student folder(s): {', '.join(created) or '(none)'}")
    if review_flags:
        print(f"\n{prefix}Needs agent review (finalize in workflows/01_intake.md):")
        for slug, items in review_flags.items():
            print(f"  - {slug}:")
            for item in items:
                print(f"      * {item}")
    if skipped:
        print(f"\n{prefix}Skipped {len(skipped)} row(s):")
        for i, name, reason in skipped:
            print(f"  - row {i} ({name}): {reason}")
    if not args.dry_run and created:
        print(f"\nNext: finalize the flagged fields per student, then run Stage 3 (discover longlist).")


if __name__ == "__main__":
    main()
