"""
apply_glossary.py — plain-English glossary of admissions jargon + the logic that
renders a "Key terms" section and auto-links jargon in an application-prep guide.

The apply-prep guides (build_application_prep.py) are dense with shorthand a
Malaysian 18-year-old hasn't met yet — RD, ED, SCEA, REA, need-blind, CSS Profile,
IDOC, ESAT, CSCA… This module is the single source of truth for what those mean and
how they get surfaced:

- build_glossary_section(text) → a "Key terms" markdown block listing ONLY the terms
  that actually appear in the guide (each with an explicit <a id> anchor to jump to).
- link_terms(text) → wraps the FIRST occurrence per section of each present term with
  a markdown link to its glossary anchor, so the student can tap any term to see what
  it means. First-occurrence-per-section (not every occurrence) keeps it from getting
  noisy, and it skips headings, code, URLs, and existing links so nothing breaks.

Reused by build_application_prep.py (and any future guide tool). Pure stdlib.
"""

import re

# --------------------------------------------------------------------------- #
# The glossary. canonical term -> definition + optional extra surface forms.
# `present_terms` filters this down to what a given guide actually uses, so extra
# entries here are free — they only render when the guide mentions them.
# Definitions are one plain-English line, written to the student ("you").
# --------------------------------------------------------------------------- #
GLOSSARY = {
    # --- Early-application types (the ones the student called out) ------------
    "ED": {
        "aliases": ["Early Decision"],
        "definition": "**Early Decision** — apply early and, if admitted, you are *bound* to enrol "
                      "and withdraw your other applications. Avoid it if you need to compare aid offers.",
    },
    "EA": {
        "aliases": ["Early Action"],
        "definition": "**Early Action** — apply early for an earlier decision; *non-binding*, so you "
                      "stay free to compare offers and decline.",
    },
    "RD": {
        "aliases": ["Regular Decision"],
        "definition": "**Regular Decision** — the standard round with the normal (later) deadline; "
                      "non-binding.",
    },
    "SCEA": {
        "aliases": ["Single-Choice Early Action"],
        "definition": "**Single-Choice Early Action** — a restrictive early option: non-binding, but "
                      "you may not apply early to most *other* private universities at the same time.",
    },
    "REA": {
        "aliases": ["Restrictive Early Action"],
        "definition": "**Restrictive Early Action** — like SCEA: non-binding early action that bars "
                      "you from applying early to other private schools.",
    },
    # --- Financial aid --------------------------------------------------------
    # NOTE: no "need" alias on demonstrated need / no "cost" alias on cost of attendance —
    # surface matching is case-insensitive and word-boundary only, so a bare common word
    # would link every innocent "you need to..." in the guide.
    "cost of attendance": {
        "aliases": ["COA"],
        "definition": "The university's official all-in yearly price — tuition **plus** housing, food, "
                      "fees, books and personal expenses. This is the number financial aid is measured "
                      "against, not the tuition figure alone.",
    },
    "demonstrated need": {
        "aliases": ["financial need"],
        "definition": "Your cost of attendance minus what the university calculates your family can "
                      "pay. \"Meets 100% of need\" means it covers that gap — it does not automatically "
                      "mean you pay nothing, so check what's left for you.",
    },
    "student contribution": {
        "aliases": ["summer work expectation"],
        "definition": "The amount a US aid package expects *you* (not your parents) to contribute each "
                      "year, usually from summer or term-time campus work. It is part of the package, "
                      "so it is not covered by the grant.",
    },
    "need-blind": {
        "aliases": [],
        "definition": "The university decides admission *without* looking at whether you asked for "
                      "financial aid — requesting aid can't hurt your chances.",
    },
    "need-aware": {
        "aliases": ["need-sensitive"],
        "definition": "Your ability to pay *can* factor into the admission decision — you still request "
                      "aid, but it is a consideration.",
    },
    "CSS Profile": {
        "aliases": ["CSS"],
        "definition": "The College Board's detailed financial-aid application most US universities use "
                      "to assess your need (separate from the FAFSA). Opens 1 October.",
    },
    "IDOC": {
        "aliases": [],
        "definition": "College Board's Institutional Documentation Service — where you upload your "
                      "parents' tax/income documents for financial aid.",
    },
    "PFAA": {
        "aliases": ["Princeton Financial Aid Application"],
        "definition": "**Princeton Financial Aid Application** — Princeton's own aid form, filed "
                      "alongside the CSS Profile.",
    },
    "ISAFA": {
        "aliases": ["International Student Financial Aid Application"],
        "definition": "**International Student Financial Aid Application** — Stanford's alternative aid "
                      "form if you can't pay the CSS Profile fee.",
    },
    "fee waiver": {
        "aliases": [],
        "definition": "A request to cancel the application fee on the grounds of financial need — so "
                      "you pay nothing to apply.",
    },
    # --- Application mechanics ------------------------------------------------
    "Common App": {
        "aliases": ["Common Application"],
        "definition": "The Common Application — one online form plus one main essay you reuse across "
                      "many US universities.",
    },
    "self-report": {
        "aliases": ["self-reported", "self-reporting"],
        "definition": "You type your own test scores into the application; you only pay to send "
                      "official scores once you enrol.",
    },
    "supplement": {
        "aliases": ["supplement essay", "supplements", "supplement essays"],
        "definition": "Extra, school-specific essay(s) on top of the shared Common App essay.",
    },
    "School Report": {
        "aliases": [],
        "definition": "A form (plus a letter) your school counsellor submits about you and your school.",
    },
    "mid-year report": {
        "aliases": [],
        "definition": "An update your school sends partway through the year with your latest grades.",
    },
    "I-20": {
        "aliases": [],
        "definition": "The US immigration form your university issues after you're admitted — you need "
                      "it to apply for a student visa.",
    },
    # --- Tests ----------------------------------------------------------------
    "SAT": {
        "aliases": [],
        "definition": "A standardised US university-entrance exam; many US universities require the "
                      "SAT or the ACT.",
    },
    "ACT": {
        "aliases": [],
        "definition": "A standardised US university-entrance exam; an accepted alternative to the SAT.",
    },
    "IELTS": {
        "aliases": [],
        "definition": "International English Language Testing System — an English-proficiency test. Your "
                      "English-medium A-Levels waive it at many universities, but not all.",
    },
    "TOEFL": {
        "aliases": [],
        "definition": "Test of English as a Foreign Language — an English-proficiency test; an "
                      "alternative to IELTS.",
    },
    "ESAT": {
        "aliases": [],
        "definition": "Engineering and Science Admissions Test — required by Oxford and Imperial "
                      "engineering; register and sit it in autumn.",
    },
    "CSCA": {
        "aliases": [],
        "definition": "China's common standardised admission assessment that international "
                      "undergraduates must sit *before* applying to Chinese universities.",
    },
    "HSK": {
        "aliases": [],
        "definition": "Hanyu Shuiping Kaoshi — the standard Chinese-language proficiency test; higher "
                      "levels (e.g. HSK 5) are needed for Chinese-taught degrees.",
    },
    # --- Scholarships / sponsors ---------------------------------------------
    "CSC": {
        "aliases": ["China Scholarship Council"],
        "definition": "China Scholarship Council scholarship — the main full-ride government "
                      "scholarship for international students in China.",
    },
    "MOE Tuition Grant": {
        "aliases": [],
        "definition": "Singapore's Ministry of Education subsidy that cuts tuition sharply in exchange "
                      "for a 3-year work bond after graduation.",
    },
    "JPA": {
        "aliases": ["JPA-MARA", "PKJM"],
        "definition": "Malaysian government overseas-study sponsorship (JPA / MARA, via the PKJM "
                      "programme) — a route to full funding for eligible students.",
    },
    "Yayasan Khazanah": {
        "aliases": [],
        "definition": "A Malaysian foundation offering competitive scholarships to study at top global "
                      "universities.",
    },
    "UAC": {
        "aliases": [],
        "definition": "Universities Admissions Centre — the shared applications hub for Australian "
                      "Year-12 students; international applicants usually apply to each university "
                      "directly instead.",
    },
    # --- Recognition, outcomes & academic structure (dossier terms) -----------
    # These surface mostly in the dossiers (build_dossier.py) rather than the apply
    # guides — recognition-back-home, post-study work, and department shorthand.
    "OPT": {
        "aliases": ["Optional Practical Training"],
        "definition": "**Optional Practical Training** — US work permission that lets you work in "
                      "your field for up to 12 months after graduating on a student visa.",
    },
    "STEM OPT": {
        "aliases": ["STEM-OPT", "STEM extension", "STEM OPT extension"],
        "definition": "**STEM OPT extension** — a 24-month extension of OPT for science/engineering "
                      "degrees, giving up to 36 months of US work authorisation after you graduate.",
    },
    "ABET": {
        "aliases": [],
        "definition": "The US accreditation board for engineering and technology degrees. An "
                      "ABET-accredited degree is recognised internationally and eases professional "
                      "registration back home.",
    },
    "Washington Accord": {
        "aliases": [],
        "definition": "An international agreement that mutually recognises engineering degrees "
                      "between member countries (the US, UK, Australia and Malaysia all belong), so "
                      "an accredited degree carries over.",
    },
    "BEM": {
        "aliases": ["Board of Engineers Malaysia"],
        "definition": "**Board of Engineers Malaysia** — the body you register with to practise as "
                      "an engineer in Malaysia; it recognises accredited degrees via the Washington "
                      "Accord.",
    },
    "MQA": {
        "aliases": ["Malaysian Qualifications Agency"],
        "definition": "**Malaysian Qualifications Agency** — the Malaysian body that recognises "
                      "foreign qualifications; check its register to confirm your degree counts back "
                      "home.",
    },
    "Common Data Set": {
        "aliases": ["CDS"],
        "definition": "A standardised set of admissions and enrolment statistics each US university "
                      "publishes — the reliable place to check real admit rates and what admitted "
                      "students look like.",
    },
    "land-grant": {
        "aliases": [],
        "definition": "A US university originally funded by federal land grants to teach practical "
                      "fields like agriculture and engineering alongside the liberal arts.",
    },
    "MAE": {
        "aliases": [],
        "definition": "Mechanical & Aerospace Engineering — a common name for the university "
                      "department or school that houses mechanical engineering degrees.",
    },
    "ECE": {
        "aliases": [],
        "definition": "Electrical & Computer Engineering — a common name for the university "
                      "department covering electrical engineering and computer hardware.",
    },
    # --- Naval architecture / marine engineering + UK routes (dossier terms) ---
    "RINA": {
        "aliases": ["Royal Institution of Naval Architects"],
        "definition": "**Royal Institution of Naval Architects** — the UK professional body for "
                      "naval architects; a RINA-accredited degree counts toward Chartered/Incorporated "
                      "Engineer status.",
    },
    "IMarEST": {
        "aliases": ["Institute of Marine Engineering, Science and Technology"],
        "definition": "**Institute of Marine Engineering, Science & Technology** — the UK professional "
                      "body for marine engineers; accredits degrees toward Chartered/Incorporated "
                      "Engineer status.",
    },
    "CEng": {
        "aliases": ["Chartered Engineer"],
        "definition": "**Chartered Engineer** — the UK's full professional-engineer status; it usually "
                      "needs an accredited MEng (or a BEng plus further learning) and maps to the "
                      "Washington Accord, so it's the route Malaysia's BEM recognises for Ir. registration.",
    },
    "IEng": {
        "aliases": ["Incorporated Engineer"],
        "definition": "**Incorporated Engineer** — a UK professional grade below Chartered. A BEng on "
                      "its own typically meets IEng, which maps to the Sydney Accord — a lower tier than "
                      "the Washington Accord chartered route.",
    },
    "Sydney Accord": {
        "aliases": [],
        "definition": "An international agreement recognising engineering-technologist / Incorporated-"
                      "Engineer qualifications between member countries — a separate, lower tier than the "
                      "Washington Accord for chartered engineers.",
    },
    "EAC": {
        "aliases": ["Engineering Accreditation Council"],
        "definition": "**Engineering Accreditation Council** — the Malaysian body that accredits "
                      "engineering degrees for the Washington Accord and for BEM Professional Engineer "
                      "(Ir.) registration.",
    },
    "UCAS": {
        "aliases": [],
        "definition": "The UK's central undergraduate application service — one form to apply to up to "
                      "five UK universities, with a mid-January equal-consideration deadline.",
    },
    "Graduate Route": {
        "aliases": [],
        "definition": "The UK's post-study work visa — lets graduates stay and work after their degree "
                      "(18 months for bachelor's/master's applying from 1 January 2027).",
    },
    "NAOME": {
        "aliases": [],
        "definition": "Naval Architecture, Ocean & Marine Engineering — the name of Strathclyde's "
                      "department for these degrees.",
    },
}


# --------------------------------------------------------------------------- #
# Surface forms + matching
# --------------------------------------------------------------------------- #
def slug(term):
    """Stable glossary anchor id for a canonical term, e.g. 'CSS Profile' -> 'term-css-profile'."""
    s = re.sub(r"[^a-z0-9]+", "-", term.strip().lower()).strip("-")
    return f"term-{s or 'x'}"


def _is_acronym(surface):
    """Acronyms (all-caps letters/digits/hyphens) match case-sensitively; phrases don't."""
    return re.fullmatch(r"[A-Z0-9][A-Z0-9\-]*", surface) is not None


def _surface_forms():
    """All (surface, canonical) pairs, longest surface first so 'CSS Profile' beats 'CSS'."""
    pairs = []
    for term, meta in GLOSSARY.items():
        for surface in [term, *meta.get("aliases", [])]:
            pairs.append((surface, term))
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


def _pattern_for(surface):
    """Word-boundary regex for a surface form; case-sensitive only for acronyms."""
    flags = 0 if _is_acronym(surface) else re.IGNORECASE
    return re.compile(rf"(?<![\w-]){re.escape(surface)}(?![\w-])", flags)


# Precompute once.
_SURFACES = _surface_forms()
_COMPILED = [(surface, canonical, _pattern_for(surface)) for surface, canonical in _SURFACES]


def present_terms(text):
    """Canonical terms that actually occur in `text`, in GLOSSARY (definition) order."""
    found = set()
    for surface, canonical, pat in _COMPILED:
        if canonical in found:
            continue
        if pat.search(text):
            found.add(canonical)
    return [t for t in GLOSSARY if t in found]


def build_glossary_section(text, title="Key terms"):
    """Markdown 'Key terms' block for only the terms present in `text`. '' if none."""
    terms = present_terms(text)
    if not terms:
        return ""
    lines = [f"## {title}", "",
             "_New to these? Here's what the shorthand in this guide means — "
             "tap a linked term anywhere below to jump back here._", ""]
    for term in terms:
        anchor = slug(term)
        lines.append(f'- <a id="{anchor}"></a>**{term}** — {GLOSSARY[term]["definition"]}')
    return "\n".join(lines)


# Spans we must never rewrite inside: existing markdown links, inline code, bare
# URLs, and raw HTML tags. Everything outside these is "free" text we can link in.
_PROTECTED = re.compile(
    r"(\[[^\]]*\]\([^)]*\)"      # [text](url) markdown links
    r"|`[^`]*`"                  # `inline code`
    r"|https?://\S+"             # bare URLs
    r"|<[^>]+>)"                 # raw HTML tags / anchors
)


def link_terms(text):
    """
    Link the first occurrence *per section* of each glossary term to its anchor.

    "Section" resets at each `##` (level-2) heading only — so within one major
    section (e.g. the whole "Grouped by application system" block with its per-
    university sub-headings) a term links just once, not once per university.
    Never links inside any heading, fenced code block, or protected span
    (links/code/URLs/HTML). A term already inside a link won't be re-linked.
    """
    out = []
    seen = set()          # canonical terms already linked in the current section
    in_fence = False
    for line in text.splitlines():
        stripped = line.lstrip()
        # Fenced code blocks: pass through untouched.
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        # Any heading: never link inside it. A level-1/2 heading also starts a
        # fresh section (deeper ### / #### headings do not reset, to avoid
        # re-linking the same term in every university block).
        heading = re.match(r"(#{1,6})\s", stripped)
        if heading:
            if len(heading.group(1)) <= 2:
                seen = set()
            out.append(line)
            continue
        out.append(_link_line(line, seen))
    return "\n".join(out)


def _link_line(line, seen):
    """Link eligible terms in one line, mutating `seen`. Protects links/code/URLs."""
    parts = _PROTECTED.split(line)
    # split() with one capturing group yields [free, protected, free, protected, ...]
    for i in range(0, len(parts), 2):
        parts[i] = _link_free_segment(parts[i], seen)
    return "".join(parts)


def _link_free_segment(segment, seen):
    if not segment.strip():
        return segment
    for surface, canonical, pat in _COMPILED:
        if canonical in seen:
            continue
        m = pat.search(segment)
        if not m:
            continue
        anchor = slug(canonical)
        start, end = m.span()
        segment = f"{segment[:start]}[{segment[start:end]}](#{anchor}){segment[end:]}"
        seen.add(canonical)
    return segment
