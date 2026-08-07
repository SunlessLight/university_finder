"""
shortlist_schema.py — single source of truth for the university finder.

Defines the master_list.csv column order, the deterministic desirability scoring
rubric, the admission-likelihood (Reach/Match/Safety) and feasibility-gate logic,
rough currency normalization to MYR, and the slug/canonical-name helpers used for
deduplication. Imported by init_student.py, sync_shortlist.py, compare_universities.py,
build_report.py, and build_calendar.py so the layout and the math never drift apart.

Design rule baked in here: DESIRABILITY is kept separate from ADMISSIBILITY. Entry
fit is NOT one of the scoring weights — a university the student can't get into must
not rank highly on price alone. Admissibility lives in classify_admission() (Reach /
Match / Safety) and feasibility_flags(), which are surfaced alongside the score.
validate_weights() enforces that rule mechanically via FORBIDDEN_WEIGHT_KEYS.

Scoring weights are PER-STUDENT and live in data/students/<slug>/weights.json — never
in this file. This module is shared, so a weight hardcoded here is a weight two
concurrent sessions fight over. Derive them with the 'scoring-weights' skill.
"""

import argparse
import json
import re
import sys
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
    "Admission likelihood", # Reach / Match / Safety, optionally "Reach (very selective)" (see classify_admission)
    "Warnings",             # hard warnings, e.g. "Deadline passed; English short" (was "Feasibility flags")
    # Identity
    "University",
    "Course",
    "Course at a glance",   # ONE tight sentence: shape of the degree, e.g. "3-yr, broad first year then pick a DS major"
    "Country",
    "City",
    "Student life",         # ONE tight sentence: what living/studying there is like. Depth belongs in the report.
    # Quality
    "Subject rank",
    "Overall rank",
    # Fit
    "Entry requirements",
    "Student grades",
    "Grades vs entry bar",  # Well above / Above / Meets / Below / Well below — GRADES ONLY (was "Fits grades?")
    "English req",
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

# --------------------------------------------------------------------------- #
# Completeness policy — the master list is the PRODUCT, and a blank cell reads to
# the client as breakage (established 2026-07-29 after auditing all 8 student CSVs).
#
# Stage 3 now fills every column from official sources rather than leaving
# "Course at a glance", the scholarship block and "Key deadline" for Stage 4. That
# rewrite has one obvious failure mode — "fill every column" becoming "invent every
# column" — so completeness comes in two halves that must always ship together:
#
#   REQUIRED_COLUMNS  what must not be blank
#   SENTINEL_VALUES   the legal ways to say "there is no answer here", per column
#
# A sentinel is an honest non-answer ("Not ranked", "Rolling"), not a fabrication.
# Using one in a column that doesn't allow it is itself a finding: it means the
# agent dodged a fact that exists. Enforced by tools/check_master_list.py
# (completeness check) and, before the CSV, by tools/merge_candidates.py.
# --------------------------------------------------------------------------- #
# Everything except "Warnings", which is written as "None" when a row is clean and
# so is never actually blank either — see sync_shortlist.candidate_to_row().
REQUIRED_COLUMNS = [h for h in SHORTLIST_HEADERS if h != "Warnings"]

WARNINGS_NONE = "None"

SENTINEL_VALUES = {
    # A university with no fixed date genuinely has none; a guessed date is worse
    # than saying so (the old "don't invent a key_deadline" rule, now expressible).
    "Key deadline": ["Rolling", "Not published — check portal"],
    # US liberal-arts colleges genuinely carry no QS/THE rank — see the
    # liberal-arts-trap note in 03_discover_longlist.md's USA playbook.
    "Subject rank": ["Not ranked"],
    "Overall rank": ["Not ranked"],
    "Scholarship competitiveness": ["No statistics published"],
    # Already a real value of this column (see GRADE_FIT_LABELS) — listed here so
    # the completeness check knows it is an allowed non-answer, not a gap.
    "Grades vs entry bar": ["Not published"],
    "Warnings": [WARNINGS_NONE],
}

# Candidate-JSON keys a row needs before it can be synced. Includes the three inputs
# with NO column of their own (currency, total_cost_programme, meets_english): they
# feed "Approx total (MYR)" and the "English short" warning, and a blank currency
# silently blanks the MYR total *and* the "Over budget" flag with it.
#
# `total_cost_programme` is required as a KEY, not as a value: an empty string means
# "compute it from total_tuition + living x duration", which is the normal case.
# merge_candidates.py checks presence for it and non-emptiness for the rest.
REQUIRED_CANDIDATE_FIELDS = [
    "university",
    "course",
    "course_at_a_glance",
    "country",
    "city",
    "student_life",
    "subject_rank",
    "overall_rank",
    "entry_requirements",
    "student_grades",
    "entry_margin",
    "english_req",
    "meets_english",
    "annual_tuition",
    "total_tuition",
    "est_living_per_year",
    "duration_years",
    "currency",
    "total_cost_programme",
    "scholarship_portal",
    "scholarship_coverage",
    "scholarship_competitiveness",
    "scholarship_how_to",
    "funds_proof",
    "post_study_work",
    "recognised_back_home",
    "application_system",
    "key_deadline",
    "intake",
    "notes",
    "course_url",
    "source_authority",
    "scores",
]

# Fields that may legitimately be present-but-empty (see the note above).
OPTIONAL_VALUE_FIELDS = {"total_cost_programme"}

# --------------------------------------------------------------------------- #
# Cell length budgets — the master list is a SCANNING surface, not a report.
#
# It is read in Google Sheets, where a 500-word cell either truncates or blows the
# row height up and makes the whole list unscannable. Enforced by
# tools/check_master_list.py, never by silent truncation: a budget that quietly
# deletes verified research is worse than one that complains.
#
# The overflow has a home. Deep prose goes to data/students/<slug>/research_notes.md
# (the candidate JSON's `research_notes` field), which sync_shortlist.py writes
# alongside the short `notes` headline. Columns absent from this map are short by
# nature (ranks, amounts, dates) and are not budgeted.
# --------------------------------------------------------------------------- #
CELL_BUDGETS = {
    "Notes": 200,
    "Scholarship & portal": 200,
    "How to get the scholarship": 200,
    "Entry requirements": 160,
    "Recognised in Malaysia?": 160,
    "Work rights after graduating": 160,
    "Scholarship competitiveness": 160,
    # Course at a glance / Student life were 120 until 2026-08-06: Austin Lau Hong
    # Shen's UK pass (12 rows) measured post-trim content clustering at 91-92% of that
    # cap (avg 110.8/120 and 109.1/120) — real one-sentence content needed more room,
    # not tighter writing. Raised to 150, same "catch bloat, not shred facts" rationale
    # as the English req / Money to show pair below.
    "Course at a glance": 150,
    "Student life": 150,
    "Scholarship coverage": 120,
    "Warnings": 120,
    # These two were set to 100/80 and then raised once measured against the real data:
    # a visa figure ("AUD 29,710/yr living costs + first-year tuition + return airfare")
    # runs ~92 chars of pure fact, and the essential English statement ("TOEFL 105 /
    # IELTS 7.5 normally required, but waived for English-medium secondary instruction")
    # runs ~106. The tighter numbers were forcing mid-sentence cuts on cells that had
    # nothing to trim — a budget should catch bloat, not shred facts.
    "English req": 120,
    # Money to show (visa) raised 100 -> 115 alongside the pair above (2026-08-06,
    # same Austin pass): measured avg 81.8/100 (82%), less tight than the other two
    # but still worth a buffer against the same squeeze-and-recheck pattern.
    "Money to show (visa)": 115,
    "Admission likelihood": 40,
    "Grades vs entry bar": 40,
}

# status.md is a snapshot read at the start of every /catchup, /longlist, /report, /decide
# and /apply-prep session (see workflows/resume.md) — not a growing log. The resume.md
# template produces ~1,000 chars; 3,000 gives headroom without letting it run away.
STATUS_BUDGET = 3000

# Allowed values for "Info source". Since 2026-07-29 Stage 3's row-filler agents build every row from
# official pages, so a fresh row is stamped "Official page" at sync time and "Not verified" means either
# a legacy row or a research failure — not "not yet". (See workflows/03_discover_longlist.md; Stage 4
# only spot-checks currency.)
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
#
# entry_margin means ONE thing: the student's grades vs the course's published
# academic bar. +2 well above ... 0 borderline/meets ... -2 well below.
#
# It used to mean two things at once, and that was a real bug (fixed 2026-07-25).
# Agents set entry_margin = -2 on US holistic Reaches to express "unlikely to get
# in", not "grades fall short" — so "Fits grades?" rendered "No" for a student with
# A*A*A*A at Duke, Vanderbilt and Georgia Tech, while the same student's other file
# read "Exceeds academic bar" at MIT and Princeton. Same grades, contradictory
# answers, and a quiet violation of the desirability-vs-admissibility guardrail.
#
# The two questions now have two inputs:
#   entry_margin          -> "Grades vs entry bar"    (measured against the bar)
#   admission_likelihood  -> "Admission likelihood"   (optional override; holistic
#                            selectivity, capped international quotas, aid-aware
#                            admission — anything that is not the grade bar)
# --------------------------------------------------------------------------- #
ADMISSION_LEVELS = ("Reach", "Match", "Safety")

# Rendered values of "Grades vs entry bar", from strongest to weakest.
#
# "Not published" is a real answer, not a missing one: a holistic US university sets no
# academic cutoff, and NTU's grade profile is a PDF that won't render. Saying so beats
# manufacturing a comparison against a bar that does not exist — which is the same class
# of mistake as the bug this column was rebuilt to fix. An EMPTY cell is different: it
# means nobody judged the row yet, and check_master_list.py flags it.
GRADE_FIT_LABELS = ("Well above", "Above", "Meets", "Below", "Well below", "Not published")

# Cap on the parenthetical reason so the cell stays inside its 40-char budget.
ADMISSION_REASON_MAX = 24


def _margin(entry_margin):
    """entry_margin as a float, or None if absent/unparseable."""
    if entry_margin is None or entry_margin == "":
        return None
    try:
        return float(entry_margin)
    except (TypeError, ValueError):
        return None


def grade_fit_label(entry_margin):
    """Render entry_margin as the "Grades vs entry bar" cell. Unknown -> ''.

    Thresholds (not equality) so a fractional margin still lands somewhere sensible.
    This is the ONLY producer of that column — there is deliberately no free-text
    override, because a hand-typed value is exactly how two of this student's files
    ended up giving contradictory answers for the same grades.

    entry_margin also accepts the sentinel "not_published" (any case/spacing) for a
    university that sets no academic bar at all — see GRADE_FIT_LABELS's "Not
    published" note above. Without this branch the label was unreachable: it was
    declared valid here and checked for by check_master_list.py, but nothing ever
    produced it, so every holistic-admission US row came back "blank" (found
    2026-07-28 building Teoh Yu Shan's USA longlist — a Longlist of Ivies/elite LACs
    with no published grade bar has no other way to pass the gate).
    """
    if isinstance(entry_margin, str) and entry_margin.strip().lower().replace(" ", "_") == "not_published":
        return "Not published"
    m = _margin(entry_margin)
    if m is None:
        return ""
    if m >= 1.5:
        return "Well above"
    if m >= 0.5:
        return "Above"
    if m > -0.5:
        return "Meets"
    if m > -1.5:
        return "Below"
    return "Well below"


def classify_admission(entry_margin, override=None, reason=None):
    """Map an entry_margin (-2..+2) to Reach / Match / Safety. Unknown -> ''.

    `override` lets the agent state an admission likelihood the grade bar cannot
    express — a school that is a Reach on holistic selectivity or a capped
    international quota even though the grades clear the bar. `reason` is a short
    phrase rendered in brackets ("Reach (very selective)") so the student can see
    WHY a row they qualify for is still a long shot. Use admission_base() to read
    the bare level back out.
    """
    if override:
        level = str(override).strip().capitalize()
        if level not in ADMISSION_LEVELS:
            raise ValueError(
                f"admission_likelihood override must be one of {', '.join(ADMISSION_LEVELS)}, got {override!r}."
            )
    else:
        m = _margin(entry_margin)
        if m is None:
            return ""
        level = "Safety" if m >= 1 else ("Reach" if m <= -1 else "Match")

    note = str(reason or "").strip()
    if not note:
        return level
    if len(note) > ADMISSION_REASON_MAX:
        raise ValueError(
            f"admission_reason {note!r} is {len(note)} chars, over the {ADMISSION_REASON_MAX} cap — "
            "keep it to a short phrase like 'very selective'; the detail belongs in research_notes."
        )
    return f"{level} ({note})"


def admission_base(value):
    """The bare Reach/Match/Safety out of an 'Admission likelihood' cell.

    'Reach (very selective)' -> 'Reach'. Use this for the balanced-shortlist check
    and any filtering, so the explanatory bracket never breaks an equality test.
    """
    return str(value or "").split("(")[0].strip()


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

    # Provisional grades: when the student's grades are self-predicted ("confident of getting"),
    # every admission judgement is provisional — flag it so the longlist never reads as settled.
    if isinstance(profile, dict) and profile.get("grade_status") == "expected":
        flags.append("Grades unverified (self-predicted)")

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
    "HKD": 0.60,  # ~7.8 HKD per USD, USD 4.7 MYR -> ~0.60
}


def parse_amount(value):
    """Extract a numeric amount from a string like 'GBP 90,000' -> 90000.0. None if absent.

    Takes the FIRST number token only. Row-filler tuition/living cells routinely carry a
    caveat after the figure ('GBP 107,100 (3 yrs at 2026/27 rate as proxy)') — stripping to
    digits-only and concatenating everything used to fuse the caveat's digits onto the real
    number (107100 + 3 + 2026 + 27 -> 1071003202627). Matching just the leading number avoids
    that, and matches how a human reads these strings.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"\d[\d,]*(?:\.\d+)?", str(value))
    if not match:
        return None
    digits = match.group(0).replace(",", "")
    try:
        return float(digits)
    except ValueError:
        return None


# Below this, a "budget" is not a degree budget — it's a stray number the parser
# picked out of prose. A whole-degree budget under RM 1,000 does not exist.
MIN_PLAUSIBLE_BUDGET = 1000


def budget_ceiling(value):
    """Return the upper bound of a stated budget, or None.

    Accepts a number, a single amount ('500000', 'MYR 500,000'), or a range
    ('400000-800000') — for a range the ceiling is the TOP, which is what an
    'Over budget' test must compare against. parse_amount() can't do this: it
    strips the separator and fuses '400000-800000' into 400000800000.

    Anything that doesn't parse to a PLAUSIBLE degree budget returns None (= no
    ceiling), not a number. Hedging prose reaches this function in practice —
    '~ 1 million? Idk' pulls out the digit 1 and used to return 1.0, which would
    have flagged literally every row 'Over budget' and made the warning column
    worthless. A missing ceiling is an open question; a ceiling of RM 1 is a lie.
    The form's budget bands (BUDGET_BAND_NORMALIZE in ingest_form_csv.py) mean
    prose should no longer arrive here at all — this is the second net.
    """
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        ceiling = float(value)
    else:
        amounts = [float(m) for m in re.findall(r"\d+(?:\.\d+)?", str(value).replace(",", ""))]
        if not amounts:
            return None
        ceiling = max(amounts)
    return ceiling if ceiling >= MIN_PLAUSIBLE_BUDGET else None


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


def main():
    """CLI: --contract prints the row-filler-facing constants as JSON.

    A row-filler subagent used to be pointed straight at this file to look up
    SENTINEL_VALUES / REQUIRED_CANDIDATE_FIELDS / CELL_BUDGETS — reading all ~7.1k
    tokens of this module for ~40 lines of constants, once per dispatch. --contract
    gives the same facts as ~500 tokens of JSON. See workflows/03b_candidate_schema.md
    and .claude/agents/row-filler.md.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--contract",
        action="store_true",
        help="Print SENTINEL_VALUES, REQUIRED_CANDIDATE_FIELDS, CELL_BUDGETS and SHORTLIST_HEADERS as JSON.",
    )
    args = parser.parse_args()

    if args.contract:
        print(json.dumps(
            {
                "SENTINEL_VALUES": SENTINEL_VALUES,
                "REQUIRED_CANDIDATE_FIELDS": REQUIRED_CANDIDATE_FIELDS,
                "CELL_BUDGETS": CELL_BUDGETS,
                "SHORTLIST_HEADERS": SHORTLIST_HEADERS,
            },
            indent=2,
            ensure_ascii=False,
        ))
        return

    parser.print_help()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
