"""
ingest_form_csv.py — batch-scaffold student data banks from a Google Forms CSV export.

This is the deterministic half of Stage 1 intake (see workflows/01_intake.md) — the only on-ramp.
It reads a Google Forms "responses" CSV (one row per respondent), and for each row that gave
consent it creates data/students/<slug>/ with a filled profile.json + preferences.json, using
the SAME templates as init_student.py so the shape never drifts.

The mechanically-mappable fields (name, budget, countries, priorities, ...) are filled
here. Grades, ethnicity, the scholarship gate, and recognition_targets matched off the
"Choose your desired course" dropdown are all deterministic and need no agent review (the
dropdown is a closed set of 38 known titles — see COURSE_ACCREDITATION_MAP / google_form_notes.md).
The only judgment-heavy bit left is flagged in a top-level "_needs_review" list on profile.json:
  - recognition_targets matched from the optional free-text "specific field of studies"
    supplement (open text, not the closed dropdown -> best-effort keyword-guess, verify)
  - a respondent who gave no course and no field of study at all (nothing to search on)

Columns are matched by a distinctive SUBSTRING of each question title (case-insensitive).
QUESTION_MAP below is the single source of truth for the column<->field wiring; keep it in step
with the form spec in workflows/01_intake.md. A reworded question can still drop the match
silently — if a field comes back null for EVERY respondent, that means a broken QUESTION_MAP
substring, not blank answers. Grep the real export's headers against QUESTION_MAP before trusting
the mapping, especially after the form's questions change.

Usage:
    python tools/ingest_form_csv.py data/form/responses.csv
    python tools/ingest_form_csv.py data/form/responses.csv --dry-run
    python tools/ingest_form_csv.py data/form/responses.csv --force

data/form/ is gitignored (PII), same class as data/students/.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

# Allow running from any cwd: make the tools dir importable for shared helpers/templates.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from shortlist_schema import budget_ceiling, slugify  # noqa: E402
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
    ("nickname", "name"),  # current form: nickname permanently replaces full name (identity protection)
    ("race", "ethnicity"),  # PDPA-sensitive; used for scholarship-eligibility research only
    ("live and work after", "post_grad_location"),  # aspiration, NOT home_country (stays Malaysia)
    ("when do you graduate", "current_completion"),  # current form's wording
    ("when do you finish", "current_completion"),    # legacy fallback (older form)
    ("final exam results", "current_completion"),    # legacy: "when will you get your actual final exam results"
    ("final result", "current_completion"),          # current form: "When month does your final result comes out?"
    ("what year does your actual result", "current_completion_year"),  # current form: added 2026-09 as a
                                                                          # dedicated year column, fixing the
                                                                          # "January (Takes A2 in Oct/Nov)" no-year
                                                                          # ambiguity — map_row() concatenates this
                                                                          # with current_completion before parsing.
    ("list each subject", "grades_raw"),             # legacy paragraph-grades form; structured subjects handled separately
    ("actual results or predicted", "grade_status"),  # legacy wording
    ("forecast result or actual", "grade_status"),  # current form: "Are you applying with forecast result or actual?"
    ("what's the score", "english_score"),   # current form: "If English test taken, what's the score?..."
                                              # MUST precede "english test taken" below — that header
                                              # contains BOTH substrings, and build_col_index() takes
                                              # the first QUESTION_MAP match in list order, so the more
                                              # specific one has to win or the score is silently lost.
    ("which english test", "english_test"),  # legacy
    ("english test score", "english_score"), # legacy
    ("english score", "english_score"),      # legacy
    ("english test taken", "english_test"),  # current form: "English Test Taken" — must stay AFTER
                                              # "what's the score" above, see comment there
    ("will you take it", "english_date"),
    ("total budget", "total_budget"),
    ("whole degree", "total_budget"),  # this form's wording: "your budget (RM) for the whole degree"
    ("per-year budget", "budget_per_year"),
    ("scholarship a must", "scholarship_gate"),  # current form: Yes/No -> scholarship_required (clean gate)
    ("planning to apply", "scholarship_interests"),  # current form: which scholarships to research (a hint)
    ("how will you fund", "funding_plan"),  # merged funding-reality question (legacy)
    ("how will you pay", "funding_source"),  # legacy fallback (older form)
    ("win a scholarship", "scholarship_dependent"),  # legacy fallback (older form)
    # NOTE: "regulated profession" checkbox is gone from the live form. recognition_targets is now
    # auto-guessed from fields_of_interest/specific_courses via _guess_recognition_targets() instead
    # of a checkbox scan — see map_row(), after preferences are built.
    ("belonging", "needs"),        # legacy fallback ("support & belonging needs" wording)
    ("personal needs", "needs"),   # legacy fallback (older form)
    ("any other perferences", "needs"),  # current form: "Any other perferences?" — consolidated lifestyle
                                          # checklist (replaces "belonging"); matched on the live form's own
                                          # typo ("perferences") since that's what's actually deployed —
                                          # --check-headers will flag it if the typo is ever fixed.
    ("achievements", "achievements_text"),  # current form: "Achievements / activities you'd want to write about..."
    # preferences
    ("which countries", "target_countries"),  # legacy fallback (older form: "Which countries would you consider?")
    ("chose your countries", "target_countries"),  # current form: "Chose your countries" (sic — live form's own typo)
    ("country matters most", "primary_country"),  # current form: "Which country matters most ( If you picked several )? "
    ("broad area", "fields_of_interest"),   # legacy fallback — the "Broad Area of Study" selector + per-area
                                              # grid was removed from the live form 2026-09 (see "choose your
                                              # desired course" below); fields_of_interest is unpopulated on
                                              # the current form by design.
    ("field or subject", "fields_of_interest"),  # legacy fallback (older form)
    ("specific field of studies", "specific_courses_freetext"),  # current form — free-text SUPPLEMENT to
                                                                    # "choose your desired course" below;
                                                                    # map_row() merges both.
    ("already know the exact course", "decided"),  # legacy fallback (older form)
    ("name the course", "specific_courses"),  # legacy fallback (older form)
    ("choose your desired course", "specific_courses"),  # current form: single dropdown, the 38
                                                            # google_form_notes.md options flattened into
                                                            # one question (replaces the old per-area grid).
    ("already have in mind", "preferred_universities"),  # current form: "Universities you already have in mind"
    ("degree level", "degree_level"),
    ("want to start", "intake"),  # legacy — no current header matches this; intake resolves to
                                   # "Flexible" via _normalize_intake's blank-input default
    ("#1 priority", "priority_1"),
    ("#2 priority", "priority_2"),
    ("#3 priority", "priority_3"),
    ("how important is university ranking", "ranking_importance"),
    ("work abroad", "work_abroad"),
    ("deal-breaker", "deal_breakers"),  # legacy fallback (hyphenated wording)
    ("dealbreaker", "deal_breakers"),   # legacy fallback — dropped from the live form 2026-09, folded into
                                          # "Any other perferences?" (-> needs) instead; unpopulated on the
                                          # current form by design.
    ("location preference", "location_prefs"),
    ("specific information you want to know", "additional_requirements"),  # legacy fallback — dropped from
                                                                              # the live form 2026-09, folded
                                                                              # into "Any other perferences?"
                                                                              # (-> needs) instead; unpopulated
                                                                              # on the current form by design.
    # NOTE: the old interest-discovery questions (career goal / what you enjoy / work styles /
    # values / constraints) were removed from the form, and the career-backwards branch that
    # consumed them was dropped on 2026-07-25 along with workflows/02_aspirations_intake.md.
    # A student who names a broad area but no exact course is normal — Stage 3 discovers courses
    # inside that area. See workflows/01_intake.md, finalize step 5.
]

# The eight supported destinations (preferences.target_countries). Normalize the form's
# checkbox labels onto these exact tokens.
#
# Singapore and Malaysia were ONE fused "Singapore/Malaysia" token until 2026-07-29, even
# though the live form offers them as separate checkboxes — so a student who ticked only
# Malaysia got a longlist half-full of Singapore rows (Foo De Mi: 6 of them). They are two
# countries with different fee tiers, recognition ladders, entry systems and costs, and
# Stage 3 now researches one country per pass, so the fused token was wrong at both ends.
# The legacy fused labels still map — to Singapore — so an old export doesn't silently drop
# a destination; split such a student's preferences.json by hand (see 03_discover_longlist.md).
COUNTRY_NORMALIZE = {
    "uk": "UK",
    "united kingdom": "UK",
    "australia": "Australia",
    "usa": "USA",
    "united states": "USA",
    "us": "USA",
    "singapore": "Singapore",
    "malaysia": "Malaysia",
    "singapore-malaysia": "Singapore",  # legacy label from the pre-2026-07-29 form
    "singapore/malaysia": "Singapore",  # legacy label from the pre-2026-07-29 form
    "china": "China",
    "japan": "Japan",
    "hong kong": "Hong Kong",
}

# Rendered into the "we dropped this country" message so it never drifts from the map above.
SUPPORTED_DESTINATIONS = ["UK", "Australia", "USA", "Singapore", "Malaysia", "China", "Japan", "Hong Kong"]

# --------------------------------------------------------------------------- #
# Budget BANDS (the form's dropdown, 2026-07-29) -> a numeric ceiling in MYR.
#
# Budget used to be free text, and free text is what people actually type: "unsure yet",
# "~1 million? Idk", a sentence about living costs mattering more than tuition. That string
# went straight into total_budget / total_budget_ceiling, where downstream code expects a
# number — and budget_ceiling() pulled the digit 1 out of "~ 1 million? Idk" and returned
# 1.0, which would have flagged every row "Over budget". A four-option dropdown removes the
# whole class of problem at the source (budget_ceiling() rejects sub-1000 values as a second
# net, and the "Not sure" band is an honest null, not a zero).
#
# Matched by substring on the lowercased label, first match wins — so "under" is checked
# before the range, and the two null bands last.
BUDGET_BAND_NORMALIZE = [
    ("under", 500000),
    ("<", 500000),        # current form: "< 500,000" (symbol replaced the word "under")
    # "Above RM 1,000,000" states a FLOOR, not a ceiling — the student has at least that much.
    # Pinning the ceiling at 1,000,000 would flag a 1.2M programme "Over budget" for exactly the
    # students who can afford it, so the top band carries no ceiling, same as "Not sure".
    ("above", None),
    (">", None),           # defensive — no live sample of the top band's symbol wording yet, but if
                            # "above" ever becomes ">" the same way "under" became "<", the fallback
                            # budget_ceiling() would otherwise misparse it as a numeric CEILING instead
                            # of "no ceiling", silently flagging affluent students "Over budget".
    ("1,000,000", 1000000),   # "RM 500,000 - 1,000,000" only reaches here if the above all missed
    ("1000000", 1000000),
    ("not sure", None),
    ("no fixed", None),
]


# Sentinel distinguishing "the label matched a band whose ceiling is None" (an honest
# "not sure") from "no band matched at all" (a legacy free-text answer to fall back on).
_UNMATCHED_BAND = object()


def _budget_band(answer):
    """Map a budget-band label to (ceiling_or__UNMATCHED_BAND, verbatim_label).

    A blank answer and a "not sure" answer both mean "no ceiling — research everything",
    which is the intended default, not a gap to chase. An unrecognised label (a legacy
    free-text export) returns _UNMATCHED_BAND so the caller falls back to budget_ceiling(),
    which returns None unless the text parses to a plausible budget.
    """
    label = _clean(answer)
    if not label:
        return None, None
    low = label.lower()
    for substr, ceiling in BUDGET_BAND_NORMALIZE:
        if substr in low:
            return ceiling, label
    return _UNMATCHED_BAND, label


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
SLIDER_MARKER = "rank your priorities"  # legacy fallback: the 1-8 numeric-slider wording
TICK_MARKER = "tick the importance"  # current form: "Tick the importance of each topic below" — a 3-tier
                                       # categorical scale replacing the numeric slider (see
                                       # TICK_IMPORTANCE_NORMALIZE); same per-category bracket structure.
TICK_IMPORTANCE_NORMALIZE = {
    "must have": 3,
    "important": 2,
    "nice to have": 1,
}
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
    "english literature": "English Literature",
    "history": "History",
    "psychology": "Psychology",
    "law": "Law",
}


def _normalize_subject(name):
    """Map a subject dropdown label to its canonical name; pass through unknown labels verbatim."""
    cleaned = _clean(name)
    return SUBJECT_NORMALIZE.get(cleaned.lower(), cleaned)


# Fixed-subject grade grid (current form, 2026-08+) — replaces the old paired "list your Nth
# subject" + "grade" dropdowns with ONE column per subject: "Select the forecast grades for your
# subjects. ( Or grade ur confident in getting ) [Biology]", one per subject, and a student leaves
# blank the ones they don't take. Detected by the shared marker substring + a bracketed suffix.
SUBJECT_GRID_MARKER = "forecast grades for your subjects"


def _subject_grid_columns(fieldnames):
    """Return [(header, subject_name)] for the fixed-subject bracketed grade columns.

    Empty for the legacy paired-dropdown form (caller falls back to _subject_columns()).
    """
    cols = []
    for header in fieldnames or []:
        if SUBJECT_GRID_MARKER not in (header or "").lower():
            continue
        m = re.search(r"\[([^\]]+)\]\s*$", header or "")
        if m:
            cols.append((header, m.group(1).strip()))
    return cols


def _build_subjects_from_grid(row, subject_grid_cols):
    """Build subjects[] from the fixed-subject grid, skipping blank cells.

    Same contract as the legacy _build_subjects(): the caller stamps grade_status = "expected"
    whenever this returns anything non-empty (the grid is a self-prediction, whatever the exact
    header wording — "Or grade ur confident in getting").
    """
    subjects = []
    for header, subject_name in subject_grid_cols:
        grade = _clean(row.get(header))
        if grade:
            subjects.append({
                "subject": _normalize_subject(subject_name),
                "grade_or_predicted": grade,
            })
    return subjects


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
    "crime": "personal_safety",  # "Low crime rate" — current form's "Any other perferences?" wording
    "climate": "climate_weather",
    "weather": "climate_weather",
    "season": "climate_weather",  # "4 seasons" — current form's "Any other perferences?" wording
    "good food": "food_quality",  # added to the live form 2026-08
    "public transport": "good_public_transport",  # added to the live form 2026-09 ("Any other perferences?")
    "living cost": "affordable_cost_of_living",    # added to the live form 2026-09 ("Any other perferences?")
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

# Best-effort recognition targets per regulated-profession KEYWORD (MQA + the professional
# body / accord). Used ONLY for the free-text "specific field of studies" supplement — see
# _guess_recognition_targets() below and the note on COURSE_ACCREDITATION_MAP. Bodies verified
# 2026-09 (WebSearch): BEM/Washington Accord (engineering), MMC (medicine), LPQB (law), MIA+ACCA
# (accounting), Pharmacy Board Malaysia, MDC (dentistry), LAM (architects) + BQSM (quantity
# surveyors, Quantity Surveyors Act 1967 — a DIFFERENT board than architects), Nursing Board
# Malaysia under the Nurses Act 1950 (NOT the Allied Health Professions Act), and MAHPC under the
# Allied Health Professions Act 2016 (Act 774) for the allied-health titles it actually covers
# (dietitian, physiotherapist, radiographer, medical laboratory technologist, audiologist —
# confirmed NOT nursing, which has its own older Act). Deliberately excludes psychology and social
# work: both have a bill/framework in progress but neither is enacted/enforced as of 2026-09, so
# there is no real body to auto-fill yet — leave [] rather than assert one that doesn't exist.
PROFESSION_RECOGNITION = {
    "medicine": ["MQA", "MMC"],
    "engineering": ["MQA", "BEM", "Washington Accord"],
    "law": ["MQA", "LPQB"],
    "accounting": ["MQA", "MIA", "ACCA"],
    "pharmacy": ["MQA", "Pharmacy Board Malaysia"],
    "dentistry": ["MQA", "MDC"],
    "architecture": ["MQA", "LAM"],
    "quantity survey": ["MQA", "BQSM"],
    "nursing": ["MQA", "Nursing Board Malaysia"],
    "physiotherap": ["MQA", "MAHPC"],
    "dietit": ["MQA", "MAHPC"],
    "radiograph": ["MQA", "MAHPC"],
    "medical laboratory": ["MQA", "MAHPC"],
    "audiolog": ["MQA", "MAHPC"],
}

# Exact-title recognition targets for the "Choose your desired course" dropdown — the 38 fixed
# options in google_form_notes.md. Because this is a CLOSED, KNOWN set (not open text), a match
# here is deterministic and needs no agent review, unlike the free-text keyword scan above. Keyed
# on the option TITLE only (the text before " — "; see _course_title()) so the hook wording can be
# revised without breaking the map — only a title rename requires updating this dict.
#
# Two rows bundle more than one real profession because the option itself does (see
# google_form_notes.md hooks) — both bodies are included rather than guessing which one applies:
#   - "Architecture & Built Environment" (hook: "...urban planning, QS") -> LAM (architects) AND
#     BQSM (quantity surveyors) are two separate boards under two separate Acts.
#   - "Nursing & Allied Health" (hook: "nurse, physiotherapist, radiographer") -> Nursing Board
#     Malaysia (nurse) AND MAHPC (physiotherapist/radiographer) are two separate boards under two
#     separate Acts.
# A field with no Malaysian licensing body (most of the 38 — arts, business, pure CS, pure
# science, teaching, ...) maps to [], which is the correct fact, not a gap.
COURSE_ACCREDITATION_MAP = {
    "Fine Arts": [],
    "Design": [],
    "Performing Arts": [],
    "Languages & Literature": [],
    "History & Philosophy": [],
    "Media & Communication": [],
    "Psychology": [],  # AHPA 2016 covers the title but practice licensing isn't enforced yet (2026-09)
    "Sociology & Anthropology": [],  # Social Work Profession Bill not yet enacted (2026-09)
    "Political Science & International Relations": [],
    "Law": ["MQA", "LPQB"],
    "Business & Management": [],
    "Accounting & Finance": ["MQA", "MIA", "ACCA"],
    "Marketing & Advertising": [],
    "Economics": [],
    "Hospitality, Tourism & Events": [],
    "Computer Science / Software Engineering / IT": [],
    "Data Science & Artificial Intelligence": [],
    "Cybersecurity": [],
    "Mechanical Engineering": ["MQA", "BEM", "Washington Accord"],
    "Civil Engineering": ["MQA", "BEM", "Washington Accord"],
    "Electrical & Electronics Engineering": ["MQA", "BEM", "Washington Accord"],
    "Aerospace Engineering": ["MQA", "BEM", "Washington Accord"],
    "Chemical Engineering": ["MQA", "BEM", "Washington Accord"],
    "Biomedical Engineering": ["MQA", "BEM", "Washington Accord"],
    "Architecture & Built Environment": ["MQA", "LAM", "BQSM"],
    "Biological & Life Sciences": [],
    "Chemistry": [],
    "Physics": [],
    "Mathematics & Statistics": [],
    "Environmental & Agricultural Sciences": [],
    "Medicine & Surgery (MBBS)": ["MQA", "MMC"],
    "Nursing & Allied Health": ["MQA", "Nursing Board Malaysia", "MAHPC"],
    "Pharmacy": ["MQA", "Pharmacy Board Malaysia"],
    "Biomedical Science & Lab Technology": ["MQA", "MAHPC"],
    "Public Health & Nutrition": ["MQA", "MAHPC"],  # dietetics is the regulated sub-title; general
                                                      # "public health" alone is not
    "Special Needs & Inclusive Education": [],
    "Secondary Education": [],
    "Early Childhood & Primary Education": [],
}


def _course_title(course_answer):
    """Extract the option TITLE from a 'Title — hook' dropdown answer (the format rule in
    google_form_notes.md). Splits on the first ' — ' (em dash); returns the string unchanged if
    the separator isn't present (a legacy export, or a title with no hook)."""
    text = _clean(course_answer)
    if " — " in text:
        return text.split(" — ", 1)[0].strip()
    return text


def _course_recognition_targets(course_answer):
    """Exact-match a 'Choose your desired course' dropdown answer against COURSE_ACCREDITATION_MAP.

    Deterministic: the 38 titles are a closed, known set, so a match needs no agent review (unlike
    _guess_recognition_targets(), which scans open free text). Returns [] for a non-regulated
    field, an unrecognised title (legacy export, or the dropdown options changed without updating
    this map), or a blank answer.
    """
    return list(COURSE_ACCREDITATION_MAP.get(_course_title(course_answer), []))


def _guess_recognition_targets(*texts):
    """Keyword-scan free text for a regulated-profession name; best-effort, not NLP.

    Used ONLY for the optional free-text "specific field of studies" supplement — open text can't
    be trusted the way the closed 38-option dropdown can (see _course_recognition_targets()), so a
    hit here still gets flagged for agent review in workflows/01_intake.md. Same false-negative
    risk as before (text that doesn't literally name the profession, e.g. "clinical sciences" for
    medicine, gets nothing) plus a small false-positive risk from short substrings (e.g. "law"
    inside an unrelated word).
    """
    haystack = " ".join(_clean(t) for t in texts if t).lower()
    targets, matched = [], []
    for pkey, vals in PROFESSION_RECOGNITION.items():
        if pkey in haystack:
            matched.append(pkey)
            targets.extend(v for v in vals if v not in targets)
    return targets, matched


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


def _split_free_list(value):
    """Split a free-text 'name a few things' answer into a clean list.

    Handles the two shapes seen on the live "specific field of studies" question: a
    newline-numbered list ("1. artificial intelligence \n2. Mechanical engineering") and a
    single line with '/'-separated items (the field's own placeholder example: "Mechatronics &
    Nanotech engineering / Criminal Law & Accounting Law"). Falls back to a comma split, then to
    the whole string as one item. Best-effort, same spirit as _split_multi().
    """
    text = _clean(value)
    if not text:
        return []
    items = []
    for line in (ln.strip() for ln in text.splitlines() if ln.strip()):
        line = re.sub(r"^\s*\d+[\.\)]\s*", "", line)  # strip "1." / "2)" numbering
        if "/" in line:
            items.extend(p.strip() for p in line.split("/") if p.strip())
        else:
            items.append(line)
    if len(items) <= 1 and "," in text:
        items = [p.strip() for p in text.split(",") if p.strip()]
    return [i for i in items if i]


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
def map_row(row, col_index, slider_cols=None, subject_cols=None, grid_cols=None,
            subject_grid_cols=None, assume_consent=False):
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
    subject_grid_cols = subject_grid_cols or []

    email = get(row, col_index, "email")

    # --- profile: identity -------------------------------------------------- #
    profile["ethnicity"] = get(row, col_index, "ethnicity") or None  # scholarship-eligibility research only
    # NOTE: home_country stays the template default ("Malaysia"). The "where do you want to live
    # and work after graduating" answer is a post-study *aspiration* (captured in notes below +
    # preferences.intent_to_migrate), NOT the student's home country — don't overwrite it here.
    post_grad_location = get(row, col_index, "post_grad_location")

    # --- profile: current program ------------------------------------------ #
    # expected_completion -> "YYYY-MM". Current form: month and year are separate columns (year added
    # 2026-09, fixing the "January (Takes A2 in Oct/Nov)" no-year ambiguity found 2026-08-23) — combine
    # them before parsing. Legacy forms carried both in the one month+year dropdown cell already.
    # type/institution are no longer asked — type stays the template default ("A-Level").
    completion_raw = get(row, col_index, "current_completion")
    completion_year_raw = get(row, col_index, "current_completion_year")
    completion_combined = f"{completion_raw} {completion_year_raw}".strip() if completion_year_raw else completion_raw
    profile["current_program"]["expected_completion"] = (
        _normalize_month_year(completion_combined) or completion_combined or None
    )

    # --- profile: grades ---------------------------------------------------- #
    # Current form: structured dropdown pairs -> build subjects[] deterministically here. The grade
    # question asks what the student is "confident of getting" (a self-prediction), so grade_status
    # is "expected" — provisional, surfaced as a warning in the longlist until real/official grades.
    subjects = _build_subjects_from_grid(row, subject_grid_cols) or _build_subjects(row, subject_cols)
    if subjects:
        profile["subjects"] = subjects
        # The dropdown path IS the self-prediction path, whatever the exact question wording, so
        # stamp "expected" unconditionally. (This used to require the literal word "confident" in
        # the grade header, while _subject_columns also accepted "select the grade" — a reworded
        # form then built subjects[], left grade_status None, and still emitted the review line
        # below asserting grade_status=expected.) A legacy/current explicit column still overrides, below.
        profile["grade_status"] = "expected"
    # Explicit "actual vs predicted" column ("Are you applying with forecast result or actual?") still
    # wins if present — resolve it BEFORE deciding whether to flag, so a student who answered "Actual"
    # (e.g. real AS/mock results already in hand ahead of a later final exam) doesn't get a review note
    # that contradicts the grade_status the profile actually ends up with.
    grade_status = get(row, col_index, "grade_status").lower()
    if grade_status.startswith("actual"):
        profile["grade_status"] = "actual"
    elif grade_status.startswith("predict"):
        profile["grade_status"] = "predicted"
    # NOTE: no needs_review flag for grade_status="expected" (self-predicted) — that's the
    # NORMAL case for this form, not something to check per-student. sync_shortlist.py already
    # surfaces it automatically as a "Grades unverified (self-predicted)" warning on every row of
    # the master list once the student reaches Stage 3, so flagging it again here was pure
    # duplication. Just leave it; upgrade grade_status by hand only if real/official results arrive.
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
    profile["achievements"] = get(row, col_index, "achievements_text") or None

    # --- profile + preferences: money (asked once, copied to both) ---------- #
    # The form asks budget as a four-option BAND, so what lands in total_budget /
    # total_budget_ceiling is always a number or null — never the label, never prose.
    # The verbatim label is kept in financial.notes, where the nuance belongs.
    band_ceiling, budget_label = _budget_band(get(row, col_index, "total_budget"))
    if band_ceiling is _UNMATCHED_BAND:
        # Legacy free-text export: parse it, and accept only a plausible budget.
        band_ceiling = budget_ceiling(budget_label)
        if band_ceiling is None and budget_label:
            needs_review.append(
                f"budget answer {budget_label!r} didn't match a band and isn't a usable number — "
                f"treated as no ceiling; confirm with the student"
            )
    total_budget = band_ceiling
    budget_note = f"Budget answer: {budget_label}" if budget_label else None
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
        "notes": budget_note,
    }
    prefs["total_budget_ceiling"] = total_budget
    prefs["budget_ceiling_per_year"] = budget_per_year
    prefs["scholarship_required"] = scholarship_required
    prefs["scholarship_interests"] = get(row, col_index, "scholarship_interests") or None

    # NOTE: recognition_targets is filled further down, after fields_of_interest/specific_courses
    # are built — see _guess_recognition_targets(). The old checkbox-driven block used to live
    # here; it's gone along with the "regulated profession" question.

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
    prefs["primary_country"] = get(row, col_index, "primary_country") or None
    prefs["fields_of_interest"] = _as_list(get(row, col_index, "fields_of_interest"))
    # specific_courses: current form is a single "Choose your desired course" dropdown (the 38
    # google_form_notes.md options), PLUS a separate free-text "specific field of studies" supplement —
    # merge both, dropdown first, no duplicates. Legacy forms encoded the course in a per-area grid
    # instead (only the column matching the chosen broad area was filled) — grid_cols is empty on the
    # current form, so this falls through to the dropdown/free-text path automatically.
    # NOT _split_multi(desired_course): "Choose your desired course" is a single-select dropdown whose
    # own option text contains commas (the google_form_notes.md "Title — 3-4 concrete nouns" hook
    # format), so comma-splitting it would shred one course title into several fake ones.
    desired_course = get(row, col_index, "specific_courses")
    grid_courses = [c for c in (_clean(row.get(h)) for h in grid_cols) if c]
    primary_courses = [desired_course] if desired_course else grid_courses
    freetext_raw = get(row, col_index, "specific_courses_freetext")
    freetext_courses = _split_free_list(freetext_raw)
    prefs["specific_courses"] = primary_courses + [c for c in freetext_courses if c not in primary_courses]
    prefs["preferred_universities"] = get(row, col_index, "preferred_universities") or None
    # No "degree level" question on the current form -- every respondent is a pre-university student
    # (A-Level/STPM/Foundation) heading to a bachelor's, so default to "undergraduate" rather than
    # leaving this null and flagging it for manual finalize every single intake. An explicit answer
    # (legacy forms, or a future postgrad-conversion question) still wins over the default.
    prefs["degree_level"] = get(row, col_index, "degree_level").lower() or "undergraduate"
    prefs["intake"] = _normalize_intake(get(row, col_index, "intake"))
    prefs["additional_requirements"] = get(row, col_index, "additional_requirements") or None

    # --- profile: recognition ----------------------------------------------- #
    # Exact-match the dropdown course against the closed 38-title set -> deterministic, no review.
    course_targets = _course_recognition_targets(desired_course)
    # The free-text supplement is open text -> still a best-effort keyword guess, still flagged.
    freetext_targets, freetext_matched = (
        _guess_recognition_targets(freetext_raw) if freetext_raw else ([], [])
    )
    rec_targets = course_targets + [t for t in freetext_targets if t not in course_targets]
    if rec_targets:
        profile["recognition_targets"] = rec_targets
    if freetext_matched:
        needs_review.append(
            f"verify recognition_targets matched from the free-text 'specific field of studies' "
            f"answer (keyword match: {', '.join(freetext_matched)}) — the dropdown-course match "
            f"is already trusted, this only covers the extra free text"
        )

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
        supported = " / ".join(SUPPORTED_DESTINATIONS)
        prefs["notes"] = (
            f"Requested target countries not in the {len(SUPPORTED_DESTINATIONS)} supported destinations "
            f"({supported}), so NOT in target_countries: {joined}. "
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


# Month name/abbreviation -> number, for _normalize_month_year(). Covers the spellings a
# month+year dropdown produces ("September 2027", "Sept 2027", "Sep 2027").
_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}


def _normalize_month_year(value):
    """'September 2027' -> '2027-09'. Returns None if there's no month+year to read.

    The form asks intake and results-date as a month+year dropdown (2026-07-29), which
    kills the ambiguity free text always carried: '9/1/2027' is September 1st to a
    Malaysian and January 9th to an American, and normalising it was a by-hand finalize
    step that got skipped. Anything that isn't a clean month+year returns None so the
    caller can keep the raw text rather than invent a date.
    """
    text = _clean(value)
    if not text:
        return None
    low = text.lower()
    year = re.search(r"(20\d{2})", low)
    if not year:
        return None
    # Take the EARLIEST month in the string, not the first one in _MONTHS order. The live
    # dropdown labels carry a trailing gloss that names other months — "August 2027 ( Takes
    # A2 in May/June )" — and a dict-order scan reached "may" before "aug" and returned
    # 2027-05 for an August student (caught on the 2026-08-03 intake). The answer's own
    # month always leads; the decoys sit in the parenthetical after it.
    hits = [
        (match.start(), number)
        for name, number in _MONTHS.items()
        if (match := re.search(rf"\b{name}", low))
    ]
    if hits:
        return f"{year.group(1)}-{min(hits)[1]:02d}"
    # Already normalised ("2027-09"), or a numeric month+year we can read unambiguously.
    iso = re.search(r"(20\d{2})[-/](\d{1,2})\b", low)
    if iso and 1 <= int(iso.group(2)) <= 12:
        return f"{iso.group(1)}-{int(iso.group(2)):02d}"
    return None


def _normalize_intake(value):
    """Intake never filters/scores — it only picks the application cycle. A blank answer or an
    explicit 'flexible / not sure' collapses to 'Flexible' (research all intakes); a month+year
    becomes 'YYYY-MM'; anything else is kept verbatim. Never invents a date."""
    v = _clean(value)
    low = v.lower()
    if not v or "flex" in low or "not sure" in low or "unsure" in low or "any" in low:
        return "Flexible"
    return _normalize_month_year(v) or v


def _normalize_countries(value):
    """Map the checkbox labels onto the 8 supported destinations.

    Returns (kept_tokens, dropped_labels): dropped_labels are answers we couldn't map (e.g. "Canada",
    which isn't supported) so the caller can report them instead of losing them silently.
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
    """Return {priority_token: header} for the per-category priority questions present in this form.

    A header contains either marker — the legacy numeric-slider wording ("rank your priorities") or
    the current tick-scale wording ("tick the importance") — plus a bracketed category ("... [Cost]").
    Matched by substring so light rewording survives. Empty if the form uses the legacy #1/#2/#3
    dropdowns instead.
    """
    cols = {}
    for header in fieldnames or []:
        low = (header or "").lower()
        if SLIDER_MARKER not in low and TICK_MARKER not in low:
            continue
        for cat_substr, token in SLIDER_CATEGORY_MAP.items():
            if cat_substr in low and token not in cols:
                cols[token] = header
                break
    return cols


def _build_priorities_from_sliders(row, slider_cols):
    """Order the priority tokens by importance (desc), tie-broken by CANONICAL_SLIDER_ORDER.

    Handles both the legacy 1-8 numeric slider and the current form's 3-tier tick scale (Must have /
    Important / Nice to have, via TICK_IMPORTANCE_NORMALIZE) through the same numeric comparison.
    Blank or unrecognised cells are skipped. Returns [] if no usable values (caller falls back to the
    legacy dropdown builder).
    """
    scored = []
    for token, header in slider_cols.items():
        raw = _clean(row.get(header))
        try:
            value = float(raw)
        except (TypeError, ValueError):
            value = TICK_IMPORTANCE_NORMALIZE.get(raw.lower())
            if value is None:
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
    """Return the headers of the "Broad Area of Study" grid (the eight per-area course columns).

    Excludes the subject-forecast-grid columns (SUBJECT_GRID_MARKER): one of the 12 A-Level
    subjects is literally "Computer Science", so its bracketed grade header also contains the
    "computer science" category substring and would otherwise be mistaken for the "Computer
    Science, IT & Data" broad-area column — leaking a grade like "A*" into specific_courses for
    any student who takes that subject (found 2026-08-23 via a real-CSV verification pass).
    """
    cols = []
    for header in fieldnames or []:
        low = (header or "").lower()
        if SUBJECT_GRID_MARKER in low:
            continue
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
# Header-coverage diagnostic.
# --------------------------------------------------------------------------- #
# Headers that are inert by design (see build_col_index / Code.gs docstrings) — never real answers,
# so they should never show up as "unmapped" noise.
_INERT_HEADER_SUBSTRINGS = ("timestamp",)


def _check_headers(fieldnames, col_index, grid_cols, slider_cols, subject_cols, subject_grid_cols):
    """Report which live-form headers QUESTION_MAP (and the grid/slider/subject-grid finders) don't
    recognise, and which QUESTION_MAP keys found no header on this CSV.

    This is the standing version of the by-hand header diff that's needed every time the live Google
    Form changes — a header that matches nothing used to fail silently (a quietly-blank field) rather
    than surface here. The unmapped-key list is NOT all bad news: legacy fallback entries (older-form
    wordings) are expected to go unmatched on a current export.
    """
    matched_headers = set(col_index.values()) | set(grid_cols) | set(slider_cols.values())
    matched_headers |= {header for header, _subject_name in subject_grid_cols}
    for subject_header, grade_header in subject_cols:
        matched_headers.add(subject_header)
        matched_headers.add(grade_header)

    unmapped_headers = [
        h for h in (fieldnames or [])
        if h and h != "_row" and h not in matched_headers  # "_row": fetch_form_responses.py's bookkeeping column
        and not any(s in h.lower() for s in _INERT_HEADER_SUBSTRINGS)
    ]
    unmapped_keys = sorted({key for _, key in QUESTION_MAP} - set(col_index.keys()))

    print(f"Checked {len(fieldnames or [])} header(s).")
    print(f"\nHeaders with NO mapping ({len(unmapped_headers)}) — a new/renamed question, or a typo drifted:")
    for h in unmapped_headers:
        print(f"  - {h!r}")
    if not unmapped_headers:
        print("  (none)")
    print(f"\nQUESTION_MAP keys with no matching header on this CSV ({len(unmapped_keys)}) — expected for "
          f"legacy fallback entries, worth a second look for anything that should be live:")
    for k in unmapped_keys:
        print(f"  - {k}")
    if not unmapped_keys:
        print("  (none)")


# --------------------------------------------------------------------------- #
# Main.
# --------------------------------------------------------------------------- #
def main():
    parser = argparse.ArgumentParser(description="Batch-scaffold student folders from a Google Forms CSV.")
    parser.add_argument("csv_path", help="Path to the Google Forms responses CSV export.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing student folders.")
    parser.add_argument("--dry-run", action="store_true", help="Report what would happen; write nothing.")
    parser.add_argument(
        "--check-headers",
        action="store_true",
        help="Report which CSV headers QUESTION_MAP doesn't recognise, and which QUESTION_MAP keys "
        "found no header on this CSV. Diagnostic only — writes nothing and doesn't ingest.",
    )
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
        subject_grid_cols = _subject_grid_columns(reader.fieldnames)
        grid_cols = _grid_columns(reader.fieldnames)
        rows = list(reader)

    if args.check_headers:
        _check_headers(reader.fieldnames, col_index, grid_cols, slider_cols, subject_cols, subject_grid_cols)
        return 0

    if "name" not in col_index:
        sys.exit(
            "ERROR: could not find a 'full name' column. Check the CSV headers against "
            "QUESTION_MAP / the form spec in workflows/01_intake.md."
        )

    created, skipped, review_flags = [], [], {}
    seen_slugs = set()

    for i, row in enumerate(rows, start=1):
        slug, profile, prefs, needs_review, skip_reason = map_row(
            row, col_index,
            slider_cols=slider_cols, subject_cols=subject_cols, grid_cols=grid_cols,
            subject_grid_cols=subject_grid_cols, assume_consent=args.assume_consent,
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
