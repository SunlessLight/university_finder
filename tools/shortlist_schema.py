"""
shortlist_schema.py — single source of truth for the university finder.

Defines the master_list.csv column order, the deterministic desirability scoring
rubric, the admission-likelihood (Reach/Match/Safety) and feasibility-gate logic,
rough currency normalization to MYR, and the slug/canonical-name helpers used for
deduplication. Imported by init_student.py, sync_shortlist.py, compare_universities.py,
build_dossier.py, and build_calendar.py so the layout and the math never drift apart.

Design rule baked in here: DESIRABILITY is kept separate from ADMISSIBILITY. Entry
fit is NOT one of the scoring weights — a university the student can't get into must
not rank highly on price alone. Admissibility lives in classify_admission() (Reach /
Match / Safety) and feasibility_flags(), which are surfaced alongside the score.
validate_weights() enforces that rule mechanically via FORBIDDEN_WEIGHT_KEYS.

Scoring weights are PER-STUDENT and live in data/students/<slug>/weights.json — never
in this file. This module is shared, so a weight hardcoded here is a weight two
concurrent sessions fight over. Derive them with the 'scoring-weights' skill.
"""

import json
import re
from datetime import date
from pathlib import Path

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
    "Backup entry route",   # foundation / INTO-Kaplan-Navitas / transfer if direct entry is a Reach (was "Pathway option")
    # Money
    "Annual tuition",
    "Total tuition",
    "Est. living/yr",
    "Duration (yrs)",
    "Approx total (MYR)",   # rough normalization for apples-to-apples comparison
    # Scholarships — the student's #1 priority; expanded from a single free-text column.
    # Write these as complete, plain-English sentences with real portal links + any statistics.
    "Scholarship & portal",         # which scholarship(s) + where to apply (link)
    "Scholarship coverage",         # how much it covers: full / tuition-only / % / fixed amount
    "Scholarship competitiveness",  # how hard to win + any published statistics (say so if unknown)
    "How to get the scholarship",   # eligibility + steps + separate deadline if any
    # Visa / recognition
    "Money to show (visa)",         # was "Funds proof"
    "Work rights after graduating", # was "Post-study work"
    "Recognised in Malaysia?",      # was "Recognised back home?"
    # Apply
    "How to apply",         # UCAS / Common App / Direct portal (was "Application system")
    "Key deadline",
    "Intake",
    "Notes",
    # Provenance
    "Course URL",
    "Info source",          # Not verified / Official page — hard facts must become "Official page" by Stage 4
]

# Allowed values for the "List status" column (first is the default for new rows).
LIST_STATUSES = ["Longlist", "Shortlist", "Finalist", "Rejected"]
DEFAULT_LIST_STATUS = LIST_STATUSES[0]

# Allowed values for "Info source". A row starts unverified and the Stage 4 pre-flight flips it once the
# fact has been confirmed on the university's own page (see workflows/04_university_dossier.md).
INFO_SOURCE_UNVERIFIED = "Not verified"
INFO_SOURCE_OFFICIAL = "Official page"

# --------------------------------------------------------------------------- #
# Desirability scoring. Each sub-score is 0-5; the weighted sum is normalized to
# 0-100. NOTE the deliberate absence of an "entry_fit" weight (see module docstring).
#
# The weights themselves are NOT here — they are per-student data, loaded from
# data/students/<slug>/weights.json by load_weights(). See the 'scoring-weights' skill.
# --------------------------------------------------------------------------- #
WEIGHT_KEYS = (
    "course_match",
    "subject_reputation",
    "total_cost_fit",
    "post_study_work_fit",
    "scholarship_opportunity",
    "experiential_fit",
    "location_pref_fit",
    "recognition_fit",
)

# Equal-weight template for the 'scoring-weights' skill to start from. NEVER a fallback:
# it is deliberately flat so that any accidental use yields obviously-uniform scores
# rather than plausible-looking wrong ones. compute_score() has no default for this reason.
DEFAULT_WEIGHTS = {k: 0.125 for k in WEIGHT_KEYS}

# Admissibility must never leak into the desirability score (see module docstring).
FORBIDDEN_WEIGHT_KEYS = ("entry_fit", "admission_fit", "admissibility", "entry_margin_fit")

MAX_SINGLE_WEIGHT = 0.5
_WEIGHT_SUM_TOLERANCE = 1e-6

# Priority tiers by normalized desirability score (same thresholds as the speaker tool).
TIER_A_MIN = 75  # A: >= 75
TIER_B_MIN = 55  # B: 55-74 ; C: < 55


def validate_weights(weights, source="weights"):
    """Raise ValueError unless `weights` is a usable weight set.

    Rejects — never normalizes. Silently rescaling a set that doesn't sum to 1.0 would
    hide a derivation mistake behind scores that still look plausible.
    """
    if not isinstance(weights, dict):
        raise ValueError(f"{source}: expected an object mapping weight keys to numbers.")

    forbidden = [k for k in weights if k in FORBIDDEN_WEIGHT_KEYS]
    if forbidden:
        raise ValueError(
            f"{source}: {', '.join(sorted(forbidden))} is not allowed as a weight. "
            "Desirability is kept separate from admissibility: entry fit belongs in "
            "'Admission likelihood' (Reach/Match/Safety) and 'Warnings', never in the score."
        )

    missing = sorted(set(WEIGHT_KEYS) - set(weights))
    extra = sorted(set(weights) - set(WEIGHT_KEYS))
    if missing:
        raise ValueError(f"{source}: missing weight key(s): {', '.join(missing)}.")
    if extra:
        raise ValueError(
            f"{source}: unknown weight key(s): {', '.join(extra)}. "
            f"Valid keys: {', '.join(WEIGHT_KEYS)}."
        )

    clean = {}
    for key in WEIGHT_KEYS:
        value = weights[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{source}: {key} must be a number, got {value!r}.")
        value = float(value)
        if value < 0:
            raise ValueError(f"{source}: {key} is negative ({value}).")
        if value > MAX_SINGLE_WEIGHT:
            raise ValueError(
                f"{source}: {key} is {value}, above the {MAX_SINGLE_WEIGHT} cap — "
                "no single factor may dominate the score."
            )
        clean[key] = value

    total = sum(clean.values())
    if abs(total - 1.0) > _WEIGHT_SUM_TOLERANCE:
        raise ValueError(
            f"{source}: weights sum to {total:.6f}, not 1.0 (off by {total - 1.0:+.6f}). "
            "Fix the derivation — do not fudge a key to make the sum work."
        )
    return clean


def load_weights(slug, students_dir=None):
    """Load and validate data/students/<slug>/weights.json.

    Returns (weights, meta) where meta is the full file (weights_id, student, rationale...).
    Raises FileNotFoundError if absent and ValueError if invalid — there is deliberately
    no fallback: scoring under weights nobody chose is the bug this file structure prevents.
    """
    base = Path(students_dir) if students_dir else (Path(__file__).resolve().parent.parent / "data" / "students")
    path = base / slug / "weights.json"
    if not path.exists():
        raise FileNotFoundError(str(path))
    try:
        meta = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: not valid JSON ({exc}).") from exc
    if not isinstance(meta, dict) or "weights" not in meta:
        raise ValueError(f"{path}: missing the top-level 'weights' object.")
    if not str(meta.get("rationale") or "").strip():
        raise ValueError(
            f"{path}: 'rationale' is required — it is the only thing that makes a weight set reviewable."
        )
    weights = validate_weights(meta["weights"], source=str(path))
    return weights, meta


def compute_score(scores, weights):
    """Return a 0-100 normalized weighted desirability score from a sub-score dict.

    `weights` is a REQUIRED positional argument. It has no default on purpose: a
    `weights=None -> DEFAULT_WEIGHTS` fallback would let a future call site silently
    score a student under weights nobody derived for them.
    """
    total = 0.0
    for field, weight in weights.items():
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
    # budget_ceiling handles a range ('400000-800000' -> 800000); a bare float() here
    # threw on any range and the swallowed error left this check silently dead.
    ceiling = budget_ceiling(budget)
    if myr is not None and ceiling:
        if float(myr) > ceiling:
            flags.append("Over budget")

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
    "JPY": 0.031,  # ~100 JPY -> 3.1 MYR
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


def budget_ceiling(value):
    """Return the upper bound of a stated budget, or None.

    Accepts a number, a single amount ('500000', 'MYR 500,000'), or a range
    ('400000-800000') — for a range the ceiling is the TOP, which is what an
    'Over budget' test must compare against. parse_amount() can't do this: it
    strips the separator and fuses '400000-800000' into 400000800000.
    """
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    amounts = [float(m) for m in re.findall(r"\d+(?:\.\d+)?", str(value).replace(",", ""))]
    return max(amounts) if amounts else None


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

    `currency` and `total_cost_programme` are candidate-JSON fields with no CSV column of
    their own — "Approx total (MYR)" is what the student sees. Still REQUIRED in the JSON:
    to_myr() returns None on an unknown/blank currency, which blanks the MYR total and, via
    feasibility_flags(), silently drops the "Over budget" warning with it.
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
