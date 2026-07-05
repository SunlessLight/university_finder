"""
shortlist_schema.py — single source of truth for the university finder.

Defines the master_list.csv column order, the deterministic desirability scoring
rubric, the admission-likelihood (Reach/Match/Safety) and feasibility-gate logic,
rough currency normalization to MYR, and the slug/canonical-name helpers used for
deduplication. Imported by init_student.py, sync_shortlist.py, compare_universities.py,
build_dossier.py, and build_calendar.py so the layout and the math never drift apart.

Design rule baked in here: DESIRABILITY is kept separate from ADMISSIBILITY. Entry
fit is NOT one of the SCORE_WEIGHTS — a university the student can't get into must
not rank highly on price alone. Admissibility lives in classify_admission() (Reach /
Match / Safety) and feasibility_flags(), which are surfaced alongside the score.
"""

import re
from datetime import date

# --------------------------------------------------------------------------- #
# Master list columns (row 1 headers). Grouped by purpose; order is the CSV order.
# --------------------------------------------------------------------------- #
SHORTLIST_HEADERS = [
    # Triage
    "List status",          # Longlist / Shortlist / Finalist / Rejected
    "Desirability",         # 0-100 weighted score (computed)
    "Tier",                 # A / B / C (computed)
    "Admission likelihood", # Reach / Match / Safety (computed from entry_margin)
    "Warnings",             # hard warnings, e.g. "Deadline passed; English short" (was "Feasibility flags")
    # Identity
    "University",
    "Course",
    "Country",
    "City",
    # Quality
    "Subject rank",
    "Overall rank",
    # Fit
    "Entry requirements",
    "Student grades",
    "Fits grades?",
    "English req",
    "Meets English?",
    "Backup entry route",   # foundation / INTO-Kaplan-Navitas / transfer if direct entry is a Reach (was "Pathway option")
    # Money
    "Annual tuition",
    "Total tuition",
    "Est. living/yr",
    "Duration (yrs)",
    "Total cost (programme)",
    "Currency",
    "Approx total (MYR)",   # rough normalization for apples-to-apples comparison
    # Scholarships — the student's #1 priority; expanded from a single free-text column.
    # Write these as complete, plain-English sentences with real portal links + any statistics.
    "Scholarship & portal",         # which scholarship(s) + where to apply (link)
    "Scholarship coverage",         # how much it covers: full / tuition-only / % / fixed amount
    "Scholarship competitiveness",  # how hard to win + any published statistics (say so if unknown)
    "How to get the scholarship",   # eligibility + steps + separate deadline if any
    # People & student life (readable research the student asked for)
    "Student community links",      # student society / Discord / Reddit / Facebook group links
    "Student life",                 # brief plain-English run-through + YouTube / Instagram links
    # Visa / recognition
    "Money to show (visa)",         # was "Funds proof"
    "Work rights after graduating", # was "Post-study work"
    "Recognised in Malaysia?",      # was "Recognised back home?"
    # Apply
    "How to apply",         # UCAS / Common App / Direct portal (was "Application system")
    "Key deadline",
    "Intake",
    # Provenance
    "Course URL",
    "Info source",          # Official / Aggregator — hard facts must become Official by Stage 4 (was "Source authority")
    "Data as-of",           # cycle year the facts were valid for
    "Dossier status",       # internal: whether the full deep-profile has been built (Not started / Done)
    "Notes",
]

# Allowed values for the "List status" column (first is the default for new rows).
LIST_STATUSES = ["Longlist", "Shortlist", "Finalist", "Rejected"]
DEFAULT_LIST_STATUS = LIST_STATUSES[0]
DEFAULT_DOSSIER_STATUS = "Not started"

# --------------------------------------------------------------------------- #
# Desirability scoring. Each sub-score is 0-5; the weighted sum is normalized to
# 0-100. NOTE the deliberate absence of an "entry_fit" weight (see module docstring).
# --------------------------------------------------------------------------- #
# Weights follow Toru's stated priority order (2026-07-05): scholarship > hands-on experience >
# ranking > location > employability > recognition. Cost is deliberately near-zero this round because
# the student set no budget limit and asked for cost NOT to be a screening factor. Re-tune per student.
SCORE_WEIGHTS = {
    "scholarship_opportunity": 0.22, # #1: realistic funding available to this student
    "experiential_fit": 0.18,        # #2: hands-on projects/research/community involvement, not just exams
    "course_match": 0.15,            # baseline: how well the course matches the field/goal (robotics)
    "subject_reputation": 0.15,      # #3 ranking: subject-specific rank + graduate outcomes
    "location_pref_fit": 0.10,       # #4: matches stated location/lifestyle preferences
    "post_study_work_fit": 0.10,     # #5 employability: visa / post-study work vs migration intent
    "recognition_fit": 0.06,         # #6: recognised back home (MQA + professional body) where it matters
    "total_cost_fit": 0.04,          # cost is NOT a screening factor this round (near-neutralised)
}

# Priority tiers by normalized desirability score (same thresholds as the speaker tool).
TIER_A_MIN = 75  # A: >= 75
TIER_B_MIN = 55  # B: 55-74 ; C: < 55


def compute_score(scores):
    """Return a 0-100 normalized weighted desirability score from a sub-score dict."""
    total = 0.0
    for field, weight in SCORE_WEIGHTS.items():
        raw = scores.get(field, 0) if isinstance(scores, dict) else 0
        try:
            raw = float(raw)
        except (TypeError, ValueError):
            raw = 0.0
        raw = max(0.0, min(5.0, raw))  # clamp to 0-5
        total += (raw / 5.0) * weight
    return round(total * 100)


def tier_for(score):
    """Map a 0-100 desirability score to an A/B/C priority tier."""
    if score >= TIER_A_MIN:
        return "A"
    if score >= TIER_B_MIN:
        return "B"
    return "C"


# --------------------------------------------------------------------------- #
# Admissibility — kept separate from desirability on purpose.
# entry_margin is the agent's honest judgement of the student's grades vs the
# course's requirement: +2 well above ... 0 borderline/meets ... -2 well below.
# --------------------------------------------------------------------------- #
def classify_admission(entry_margin):
    """Map an entry_margin (-2..+2) to Reach / Match / Safety. Unknown -> ''."""
    if entry_margin is None or entry_margin == "":
        return ""
    try:
        m = float(entry_margin)
    except (TypeError, ValueError):
        return ""
    if m >= 1:
        return "Safety"
    if m <= -1:
        return "Reach"
    return "Match"


def _parse_iso_date(text):
    """Pull the first YYYY-MM-DD date out of a free-text string, or None."""
    if not text:
        return None
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", str(text))
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def feasibility_flags(candidate, profile=None, today=None):
    """Return a list of hard-gate warnings. These are surfaced next to (and never
    folded into) the desirability score, so an unreachable/ineligible option stays
    visibly flagged rather than silently scoring well."""
    flags = []
    today = today or date.today()

    deadline = _parse_iso_date(candidate.get("key_deadline"))
    if deadline and deadline < today:
        flags.append("Deadline passed")

    if candidate.get("meets_english") is False:
        flags.append("English short")

    myr = candidate_total_myr(candidate)
    budget = None
    if isinstance(profile, dict):
        budget = (profile.get("financial") or {}).get("total_budget")
    if myr is not None and budget:
        try:
            if float(myr) > float(budget):
                flags.append("Over budget")
        except (TypeError, ValueError):
            pass

    return flags


# --------------------------------------------------------------------------- #
# Rough currency normalization to MYR. This is an OFFLINE static table — update the
# rates periodically; it exists only to make 3-yr-UK vs 4-yr-US totals roughly
# comparable, not for financial precision.
# --------------------------------------------------------------------------- #
FX_TO_MYR = {
    "MYR": 1.0,
    "GBP": 5.9,
    "USD": 4.7,
    "AUD": 3.1,
    "SGD": 3.5,
    "CNY": 0.65,
    "EUR": 5.1,
    "RMB": 0.65,  # alias for CNY
}


def parse_amount(value):
    """Extract a numeric amount from a string like 'GBP 90,000' -> 90000.0. None if absent."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    digits = re.sub(r"[^0-9.]", "", str(value).replace(",", ""))
    if not digits or digits == ".":
        return None
    try:
        return float(digits)
    except ValueError:
        return None


def to_myr(amount, currency):
    """Convert an amount in `currency` to approximate MYR using FX_TO_MYR. None if unknown."""
    amt = parse_amount(amount)
    if amt is None:
        return None
    rate = FX_TO_MYR.get((currency or "").strip().upper())
    if rate is None:
        return None
    return round(amt * rate)


def candidate_total_myr(candidate):
    """Best-effort total programme cost in MYR for a candidate dict.

    Prefers an explicit total_cost_programme; otherwise total_tuition + living*years.
    Returns an int (MYR) or None if there isn't enough to compute.
    """
    currency = candidate.get("currency")
    explicit = candidate.get("total_cost_programme")
    if explicit not in (None, ""):
        return to_myr(explicit, currency)

    tuition = parse_amount(candidate.get("total_tuition"))
    living = parse_amount(candidate.get("est_living_per_year"))
    years = parse_amount(candidate.get("duration_years"))
    if tuition is None:
        return None
    total = tuition
    if living is not None and years is not None:
        total += living * years
    return to_myr(total, currency)


# --------------------------------------------------------------------------- #
# Slug + canonical-name helpers (used for folders, filenames, and dedupe keys).
# --------------------------------------------------------------------------- #
def slugify(text):
    """Lowercase, hyphenate, strip to a filesystem/URL-safe slug."""
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").strip().lower())
    return s.strip("-") or "unnamed"


# Common university aliases -> canonical form, so dedupe doesn't fragment the list.
_UNI_ALIASES = {
    "ucl": "university college london",
    "lse": "london school of economics",
    "imperial": "imperial college london",
    "nus": "national university of singapore",
    "ntu": "nanyang technological university",
    "smu": "singapore management university",
    "mit": "massachusetts institute of technology",
    "ucla": "university of california los angeles",
    "uom": "university of manchester",
}

# Course-title noise stripped before keying (BSc Computer Science == Computer Science BSc (Hons)).
_COURSE_NOISE = (
    "(hons)", "(honours)", "hons", "honours",
    "bsc", "ba", "beng", "meng", "llb", "mbbs", "bachelor of", "bachelor",
    "degree", "with placement", "(with placement)",
)


def canonical_uni(name):
    """Normalize a university name to a canonical comparison key."""
    base = re.sub(r"[^a-z0-9 ]+", " ", (name or "").strip().lower())
    base = re.sub(r"\s+", " ", base).strip()
    return _UNI_ALIASES.get(base, base)


def _canonical_course(course):
    base = (course or "").strip().lower()
    for noise in _COURSE_NOISE:
        base = base.replace(noise, " ")
    base = re.sub(r"[^a-z0-9 ]+", " ", base)
    return re.sub(r"\s+", " ", base).strip()


def course_key(university, course):
    """Dedupe key for a (university, course) pair, resistant to alias/title noise."""
    return (canonical_uni(university), _canonical_course(course))
