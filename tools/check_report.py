"""
check_report.py — lint a rendered Stage 4 university report for the things that make it
half-researched or unreadable.

The Stage 4 counterpart to check_master_list.py, and it exists for a measured reason: an
LSE report session verified its finished report by READING ALL 390 LINES back into the
orchestrating session's context. A resident token is re-billed on every subsequent turn
(see plan.md, "Context"), so that is the most expensive possible way to answer "is this
report actually finished" — and it is not a thing a long session should repeat per finalist.
This tool answers the mechanical half of that question in ~20 lines of output.

It is deliberately NOT a synthesis judge. build_report.py's validate() only checks that each
section is non-empty; this checks that a non-empty report is also *complete, sourced, and
written to the student*. Whether the writing is any GOOD is still why the stage is pinned to
Opus (workflows/00_overview.md).

It reads the RENDERED .md, not the research JSON: the .md is the durable artifact the student
gets, the JSON lives in .tmp and is deleted, and reading the render also catches a report
built by an older section spec.

Checks (use --check to run a subset while working through a fix):
  structure   16 sections, right headings, right order, for the detected mode
  snapshot    every Snapshot fact row present and filled (a missing row = a missing JSON field)
  notfound    "Not found — …" density, bare "Not found" with no reason, all-not-found sections
  sources     enough sources, each with a URL, an authority, and enough of them Official
  voice       written TO the student — second person, no student name, no third person
  tables      the sections the writing rules say must be a table/checklist actually are,
              and the ⚠️ glyph only ever appears inside a blockquote callout

Mode (course vs university) is DETECTED from the headings, not passed in — the whole point is
that a cold session can run this on a report it did not build.

Every threshold below was calibrated against the 20 reports on disk on 2026-08-08, not
guessed. The separation is wide, so a finding means something: the pre-writing-rules early
batch carries 16-77 third-person pronouns, every report written under the current rules
carries 0-1. Bold density was considered and REJECTED as a check — it runs 6.9%-32.2% with
good recent reports at both ends, so any threshold would be noise. Repetition ("say each key
fact once") is the other real writing rule with no deterministic check yet.

Usage:
    python tools/check_report.py --student <slug> --report <report-slug>
    python tools/check_report.py --student <slug> --all
    python tools/check_report.py --file data/students/<slug>/reports/<report-slug>.md
    python tools/check_report.py --student <slug> --all --check voice,tables
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_report import SECTIONS_BY_MODE  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    # sys.exit("ERROR: … — …") writes to stderr, and every error message here has an em-dash
    # in it. Without this the Windows console renders them as mojibake.
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

CHECKS = ["structure", "snapshot", "notfound", "sources", "voice", "tables"]

# --- Thresholds (calibrated 2026-08-08 against the 20 reports on disk) -----------------
# Observed max in a real report is 3. A few honest gaps are the convention working; fifteen
# is a half-researched report that slipped past the non-empty check.
MAX_NOT_FOUND = 8
# Observed 7-39. The two thin ones (7 and 9) are both from the pre-writing-rules batch.
MIN_SOURCES = 10
# Hard facts need official pages (guardrail 2). Can't map source->fact from the render, so
# this is a proxy: at least half the list must be Official. Observed 50%-100%.
MIN_OFFICIAL_SHARE = 0.5
# "you"/"your" per 1,000 chars. Observed 2.1-4.0 in reports written to the student, and
# 0.13-0.7 in the ones written about him. The gap is 3x wide, so 1.0 is not a close call.
MIN_YOU_PER_1K = 1.0
# Name parts shorter than this are not searched for: "Lee" would hit NTU's Lee Kong Chian
# School of Medicine, "Hui" hits ordinary words. The full name is always searched, and a
# report written in third person nearly always trips the pronoun rule anyway.
MIN_NAME_PART = 4
# Longest excerpt quoted back in a finding. Findings are a scanning surface too — the report
# is on disk, and the whole point of this tool is not re-reading it.
EXCERPT = 70

# Snapshot rows _fact_table() renders per mode, in order. It SKIPS empty values, so a row
# missing from the render means the field was missing from the research JSON — which is the
# only place that omission is ever visible.
SNAPSHOT_ROWS = {
    "course": [
        "University", "Course", "Country / City", "Overall rank", "Subject rank",
        "How to apply", "Admission likelihood", "Your priorities",
    ],
    "university": [
        "University", "Location", "Setting", "Type & size", "Overall rank",
        "How to apply", "Admission likelihood", "Est. net cost after aid (MYR)",
        "Your priorities",
    ],
}

# Sections the writing rules require to be STRUCTURED, keyed by section key per mode.
# "Tables and checklists beat prose for anything structured" is the rule; these are the
# places it is not a preference — a cost breakdown or a deadline list written as a
# paragraph is the specific failure the readability review found.
REQUIRED_TABLES = {
    "course": {
        "costs": "a line-item cost table (tuition / living / total in MYR)",
        "scholarships": "a table of schemes with value + eligibility",
        "admitted_profiles": "a stats table (admit rate, applications per place, test range)",
        "why_here": "a 2-column key-value table matching the Snapshot",
    },
    "university": {
        "costs_aid": "a line-item cost table (COA / aid model / your share in MYR)",
        "admissions_fit": "a stats table (admit rate, ED vs RD, intl, test range)",
        "why_here": "a 2-column key-value table matching the Snapshot",
    },
}
REQUIRED_CHECKLISTS = {
    "course": {
        "application_checklist": "`- [ ]` items, one per thing to gather",
        "key_dates": "`- [ ]` items with dates, not a paragraph",
    },
    "university": {
        "how_to_apply": "`- [ ]` items for the deadlines and the pieces to prepare",
    },
}

# Third person about the student. Word-bounded, and the Sources section is excluded before
# matching (a forum thread title is not the report's voice).
THIRD_PERSON = re.compile(r"\b(he|she|his|him|hers|himself|herself)\b", re.I)
SECOND_PERSON = re.compile(r"\byou(?:r|rs)?\b", re.I)
# "Not found" is the sanctioned way to record a gap; "Not found — <why>" is the whole
# convention. Bare, it is indistinguishable from not having looked.
NOT_FOUND = re.compile(r"\bnot found\b", re.I)
NOT_FOUND_BARE = re.compile(r"\bnot found\b(?!\s*[—–\-:])", re.I)
HEADING = re.compile(r"^## (\d+)\.\s*(.+?)\s*$")
# Bullet/quote/emphasis/checkbox noise a line can open with before its real first character.
# Used to ask "is this line TRYING to be a callout?" — see check_tables.
LEADING_NOISE = re.compile(r"^(?:[-*+>\s]|\[[ xX]\]|\d+\.)+")
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
YEAR = re.compile(r"\b(20\d{2})\b")


# --- Parsing ---------------------------------------------------------------------------

def parse_report(text):
    """(title, [(number, heading, [body lines])]) from a rendered report .md."""
    title, sections, current = "", [], None
    for line in text.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        match = HEADING.match(line)
        if match:
            current = (int(match.group(1)), match.group(2), [])
            sections.append(current)
        elif current is not None:
            current[2].append(line)
    return title, sections


def detect_mode(sections):
    """Which of build_report.py's two section specs this report was rendered against.

    Detected rather than passed in: the caller is usually a cold session linting a report it
    didn't build, and the headings already carry the answer unambiguously (every report on
    disk matches one spec 16/16 and the other far less).
    """
    headings = {h for _, h, _ in sections}
    scores = {
        mode: len(headings & ({"Snapshot", "Sources"} | {h for _, h in spec}))
        for mode, spec in SECTIONS_BY_MODE.items()
    }
    best = max(scores, key=scores.get)
    tied = [m for m, s in scores.items() if s == scores[best]]
    return best, (len(tied) > 1)


def expected_headings(mode):
    return ["Snapshot"] + [h for _, h in SECTIONS_BY_MODE[mode]] + ["Sources"]


def section_bodies(sections, mode):
    """{section key: body text}, keyed the way the research JSON is keyed.

    Lets a check name the section it cares about ("costs") instead of hard-coding a heading
    string that would drift the first time a heading is reworded.
    """
    by_heading = {h: key for key, h in SECTIONS_BY_MODE[mode]}
    return {
        by_heading[h]: "\n".join(body).strip()
        for _, h, body in sections
        if h in by_heading
    }


def find_section(sections, heading):
    for _, h, body in sections:
        if h == heading:
            return "\n".join(body).strip()
    return None


def strip_links(text):
    """Replace [title](url) with just the title — URLs are full of words that aren't prose."""
    return MD_LINK.sub(lambda m: m.group(1), text)


def tables_in(body):
    """[[row, …], …] — each contiguous run of pipe-rows in `body`, delimiter row dropped."""
    out, current = [], []
    for line in body.splitlines():
        if line.lstrip().startswith("|"):
            current.append(line.strip())
        elif current:
            out.append(current)
            current = []
    if current:
        out.append(current)
    return [t for t in out if len(t) >= 3]  # header + delimiter + at least one data row


def table_columns(table):
    return len([c for c in table[0].strip("|").split("|")])


def excerpt(line):
    line = " ".join(line.split())
    return line[:EXCERPT] + ("…" if len(line) > EXCERPT else "")


# --- Checks ----------------------------------------------------------------------------

def check_structure(sections, mode, ambiguous):
    """All 16 sections, the right headings, in the right order, numbered 1..16.

    build_report.py renders this itself, so a failure here means the file was NOT rendered by
    the current tool — an older section spec, or a hand-edited report. Either way the rest of
    the checks are reading a shape they don't know, so this one is the gate on the others.
    """
    out = []
    if ambiguous:
        out.append("cannot tell course mode from university mode — the headings match neither spec")
    expected = expected_headings(mode)
    actual = [h for _, h, _ in sections]
    if actual == expected:
        pass
    elif set(actual) == set(expected):
        out.append(f"all {len(expected)} sections present but in a DIFFERENT ORDER "
                   f"(first difference: {next(a for a, e in zip(actual, expected) if a != e)!r})")
    else:
        missing = [h for h in expected if h not in actual]
        extra = [h for h in actual if h not in expected]
        if missing:
            out.append(f"missing section(s) for --mode {mode}: {missing}")
        if extra:
            out.append(f"unexpected section(s): {extra} — not in the {mode} spec")
    numbers = [n for n, _, _ in sections]
    if numbers != list(range(1, len(sections) + 1)):
        out.append(f"section numbering is {numbers} — build_report.py numbers 1..n in order")
    return out


def check_snapshot(sections, mode):
    """Every Snapshot fact row present and filled.

    _fact_table() silently SKIPS a field whose value is empty, so a missing row is the only
    trace an omitted research-JSON field leaves. 'Your priorities' matters most: the writing
    rules hang on stating the ranked priorities once, up front, and every later "your
    top-ranked priority" reference is meaningless without that row visible.
    """
    body = find_section(sections, "Snapshot")
    if body is None:
        return ["no Snapshot section"]
    rows = {m.group(1): m.group(2).strip()
            for m in re.finditer(r"^\|\s*\*\*(.+?)\*\*\s*\|(.*?)\|\s*$", body, re.M)}
    if not rows:
        return ["Snapshot is not a fact table — re-render with the current build_report.py"]
    out = []
    for label in SNAPSHOT_ROWS[mode]:
        if label not in rows:
            out.append(f"Snapshot has no {label!r} row — the research JSON left that field empty")
        elif not rows[label]:
            out.append(f"Snapshot {label!r} is blank")
    return out


def check_notfound(sections, mode):
    """Honest-gap density, gaps with no reason, and sections that are nothing but a gap.

    "Not found — <why>" is the sanctioned way to record something that genuinely isn't
    published, and a couple per report is the convention working. Without the reason it is
    indistinguishable from not having looked; fifteen of them is a report that passed the
    non-empty check while being half-researched; and a section whose ENTIRE body is one is
    the exact hole build_report.py's validate() was built to catch and can't.
    """
    out = []
    full = "\n".join("\n".join(b) for _, _, b in sections)
    total = len(NOT_FOUND.findall(full))
    if total > MAX_NOT_FOUND:
        out.append(f"{total} 'Not found' gaps (threshold {MAX_NOT_FOUND}) — this reads as "
                   f"half-researched, not as honest reporting")
    for _, heading, body in sections:
        text = "\n".join(body)
        for line in body:
            if NOT_FOUND_BARE.search(line):
                out.append(f"{heading}: 'Not found' with no reason — {excerpt(line)}")
        stripped = re.sub(r"[*_>#\s]+", " ", text).strip()
        if NOT_FOUND.search(text) and len(stripped) < 200:
            out.append(f"{heading}: the whole section is one 'Not found' — research it or say "
                       f"what IS known ({len(stripped)} chars)")
    return out


def parse_sources(sections):
    """[(title, url, authority, as_of)] from the Sources section.

    render_sources() de-noises the list: when authority and cycle year are uniform it states
    them once in a lead note and drops the per-line suffix, tagging only the exceptions. So
    the default comes from the lead note and the tags override it — and older reports that
    tag every line still parse, because a tag always wins.
    """
    body = find_section(sections, "Sources")
    if body is None:
        return None
    lead = next((ln for ln in body.splitlines() if ln.startswith("_Sources")), "")
    default_auth = "Official" if "official" in lead.lower() else (
        "Aggregator" if "aggregator" in lead.lower() else "")
    lead_year = YEAR.search(lead)
    default_year = lead_year.group(1) if lead_year else ""

    out = []
    for line in body.splitlines():
        if not line.startswith("- "):
            continue
        entry = line[2:].strip()
        link = MD_LINK.search(entry)
        title = link.group(1) if link else entry
        url = link.group(2) if link else ""
        tail = entry[link.end():] if link else ""
        auth = default_auth
        if re.search(r"\bofficial\b", tail, re.I):
            auth = "Official"
        elif re.search(r"\baggregator\b", tail, re.I):
            auth = "Aggregator"
        year = YEAR.search(tail)
        out.append((title, url, auth, year.group(1) if year else default_year))
    return out


def check_sources(sections):
    """Enough sources, each with a URL and an authority, and enough of them Official.

    Guardrail 2 is that hard facts come from official pages, and the rendered report can't
    say which source backed which fact — so this is a proxy on the list as a whole: an
    all-aggregator source list cannot be backing a fee table or a deadline, whatever the
    prose claims. The as-of year matters for the same reason a cached fee does: a source with
    no cycle year can't be checked for staleness next year.
    """
    sources = parse_sources(sections)
    if sources is None:
        return ["no Sources section"]
    if not sources:
        return ["Sources section has no entries — every hard fact needs a citation"]

    out = []
    if len(sources) < MIN_SOURCES:
        out.append(f"{len(sources)} source(s) (minimum {MIN_SOURCES}) — too thin for 14 "
                   f"researched sections")
    for title, url, auth, year in sources:
        if not url:
            out.append(f"source has no URL: {excerpt(title)}")
        if not auth:
            out.append(f"source has no authority (Official/Aggregator): {excerpt(title)}")
        if not year:
            out.append(f"source has no as-of cycle year: {excerpt(title)}")

    official = sum(1 for _, _, auth, _ in sources if auth == "Official")
    share = official / len(sources)
    if share < MIN_OFFICIAL_SHARE:
        out.append(f"only {official}/{len(sources)} sources are Official ({share:.0%}, "
                   f"minimum {MIN_OFFICIAL_SHARE:.0%}) — hard facts can't rest on aggregators")
    return out


def check_voice(sections, student_name):
    """Written TO the student, in second person, with no name and no third person.

    "It's their guide, not an internal report" is the rule, and it is the one the pre-2026-07
    batch breaks wholesale — those reports read as a case file about the student instead of a guide written to
    them. The two halves catch different failures: the pronoun rule catches prose written ABOUT the student,
    the "you" rate catches prose written about nobody (a brochure). Sources are excluded from
    both — a forum thread title is not the report's voice.

    The known false positive is a pronoun belonging to a NAMED third party ("Feynman taught
    here — his lectures…"). It is a spot-check, not a parser; the excerpt makes the call
    obvious in a second, and the rewrite it prompts ("the Feynman Lectures") is usually
    tighter anyway. Worth keeping: on the pre-rules batch this rule fires 41 times on one
    report, and every one of those is real.
    """
    out = []
    prose = "\n".join(
        strip_links("\n".join(body)) for _, h, body in sections if h != "Sources"
    )
    for line in prose.splitlines():
        for match in THIRD_PERSON.finditer(line):
            out.append(f"third person {match.group(0)!r} — write to the student: {excerpt(line)}")
            break  # one finding per line; the fix is the sentence, not the word

    if student_name:
        for needle in name_needles(student_name):
            pattern = re.compile(rf"\b{re.escape(needle)}\b", re.I)
            for line in prose.splitlines():
                if pattern.search(line):
                    out.append(f"student's name {needle!r} appears — say 'you': {excerpt(line)}")
                    break

    rate = 1000 * len(SECOND_PERSON.findall(prose)) / max(len(prose), 1)
    if rate < MIN_YOU_PER_1K:
        out.append(f"only {rate:.1f} 'you'/'your' per 1,000 chars (minimum {MIN_YOU_PER_1K}) — "
                   f"this is written about the student, or about nobody")
    return out


def name_needles(name):
    """The name strings worth searching for: the whole name, plus parts long enough to be safe.

    Short parts are dropped on purpose — "Lee" would hit NTU's Lee Kong Chian School of
    Medicine on every Singapore report, and a lint that cries wolf gets run with --check.
    """
    parts = [p for p in re.split(r"[\s,]+", name.strip()) if len(p) >= MIN_NAME_PART]
    whole = " ".join(name.split())
    return list(dict.fromkeys(([whole] if len(whole) >= MIN_NAME_PART else []) + parts))


def check_tables(sections, mode):
    """The structured sections are actually structured, and ⚠️ stays inside a callout.

    Both halves come from the readability review in workflows/04: the reports were
    well-researched but fought the reader, with cost breakdowns buried in prose and the one
    make-or-break warning sitting mid-paragraph. report_to_pdf.py renders a blockquote as an
    unmissable red callout and a plain paragraph as a plain paragraph, so a ⚠️ outside a
    blockquote is a warning the student will scroll straight past.

    Scoped for precision, because a gate that cries wolf gets run with --check: only a line
    that OPENS with the glyph is a warning that failed to become a callout. Mid-line uses are
    a cross-reference ("see the ⚠️ above") or a verdict marker in a comparison table, and
    both are fine — except in why_here, where the writing rules ban the glyph outright.
    """
    out = []
    bodies = section_bodies(sections, mode)

    for key, want in REQUIRED_TABLES[mode].items():
        body = bodies.get(key)
        if body is None:
            continue  # structure check owns a missing section
        tables = tables_in(body)
        if not tables:
            out.append(f"{key}: no table — the writing rules want {want}")
        elif key == "why_here" and table_columns(tables[0]) != 2:
            out.append(f"why_here: table has {table_columns(tables[0])} columns — it should be "
                       f"2 (topic | honest read), with each hesitation folded into its verdict")

    for key, want in REQUIRED_CHECKLISTS[mode].items():
        body = bodies.get(key)
        if body is None:
            continue
        if not re.search(r"^\s*- \[ \]", body, re.M):
            out.append(f"{key}: no `- [ ]` checklist items — the writing rules want {want}")

    for _, heading, body in sections:
        in_why_here = heading == dict(SECTIONS_BY_MODE[mode]).get("why_here", "")
        for line in body:
            if "⚠" not in line:
                continue
            stripped = line.lstrip()
            if stripped.startswith(">"):
                continue
            if stripped.startswith("|"):
                if in_why_here:
                    out.append(f"why_here: ⚠️ in a table cell — that glyph is reserved for the "
                               f"red callouts: {excerpt(line)}")
                continue
            if LEADING_NOISE.sub("", stripped).startswith("⚠"):
                out.append(f"{heading}: ⚠️ opens a plain line — make it a `>` blockquote or it "
                           f"renders as ordinary text, not a red callout: {excerpt(line)}")
    return out


# --- Driver ----------------------------------------------------------------------------

def run(text, wanted, student_name=None):
    """(mode, {check: [findings]}) for one report's Markdown."""
    _, sections = parse_report(text)
    if not sections:
        return None, {"structure": ["no '## N. Heading' sections — this is not a rendered report"]}
    mode, ambiguous = detect_mode(sections)

    results = {}
    if "structure" in wanted:
        results["structure"] = check_structure(sections, mode, ambiguous)
    # The rest read by section key, so a report whose section SET is wrong can't be
    # meaningfully linted past the structure check (same rule as check_master_list.py).
    if set(h for _, h, _ in sections) != set(expected_headings(mode)):
        return mode, results
    if "snapshot" in wanted:
        results["snapshot"] = check_snapshot(sections, mode)
    if "notfound" in wanted:
        results["notfound"] = check_notfound(sections, mode)
    if "sources" in wanted:
        results["sources"] = check_sources(sections)
    if "voice" in wanted:
        results["voice"] = check_voice(sections, student_name)
    if "tables" in wanted:
        results["tables"] = check_tables(sections, mode)
    return mode, results


def student_name_for(md_path, slug=None):
    """The student's name from profile.json, or None if it can't be located.

    Derived from the report's own path when --file is used, so a one-off lint still gets the
    name half of the voice check. Returns None quietly rather than failing: the pronoun and
    "you"-rate halves are the load-bearing ones.
    """
    if slug:
        profile = STUDENTS_DIR / slug / "profile.json"
    else:
        profile = md_path.parent.parent / "profile.json"
    if not profile.exists():
        return None
    try:
        return (json.loads(profile.read_text(encoding="utf-8")).get("name") or "").strip() or None
    except (json.JSONDecodeError, OSError):
        return None


def check_one(md_path, wanted, slug, limit):
    """Lint one report, print its block, return the finding count."""
    text = md_path.read_text(encoding="utf-8")
    name = student_name_for(md_path, slug)
    mode, results = run(text, wanted, student_name=name)

    total = sum(len(v) for v in results.values())
    label = md_path.relative_to(REPO_ROOT) if md_path.is_relative_to(REPO_ROOT) else md_path
    note = "" if name else "  (no profile.json — name check skipped)"
    print(f"{label} — mode {mode or '?'}, {len(text)} chars, {total} finding(s){note}")
    for check in CHECKS:
        findings = results.get(check)
        if findings is None:
            continue
        if not findings:
            print(f"  ok   {check}")
            continue
        print(f"  FAIL {check} ({len(findings)})")
        for line in findings[:limit]:
            print(f"       {line}")
        if len(findings) > limit:
            print(f"       ... and {len(findings) - limit} more")
    return total


def main():
    parser = argparse.ArgumentParser(
        description="Lint a rendered Stage 4 university report for completeness and readability."
    )
    parser.add_argument("--student", help="Student slug (folder under data/students/).")
    parser.add_argument("--report", help="Report slug, with or without .md (needs --student).")
    parser.add_argument("--all", action="store_true", help="Every report for --student.")
    parser.add_argument("--file", help="Path to one report .md, instead of --student/--report.")
    parser.add_argument("--check", help=f"Comma list of checks to run (default all): {', '.join(CHECKS)}")
    parser.add_argument("--limit", type=int, default=10, help="Max findings shown per check (default 10).")
    args = parser.parse_args()

    if bool(args.file) == bool(args.student):
        sys.exit("ERROR: pass exactly one of --student or --file.")
    if args.student and bool(args.report) == bool(args.all):
        sys.exit("ERROR: with --student, pass exactly one of --report or --all.")

    wanted = CHECKS
    if args.check:
        wanted = [c.strip().lower() for c in args.check.split(",") if c.strip()]
        unknown = [c for c in wanted if c not in CHECKS]
        if unknown:
            sys.exit(f"ERROR: unknown check(s) {unknown}. Valid: {', '.join(CHECKS)}")

    if args.file:
        path = Path(args.file)
        if not path.is_absolute():
            path = REPO_ROOT / path
        if not path.exists():
            sys.exit(f"ERROR: {path} not found.")
        paths = [path]
    else:
        reports_dir = STUDENTS_DIR / args.student / "reports"
        if not reports_dir.exists():
            sys.exit(f"ERROR: {reports_dir} not found — no reports built for this student yet.")
        if args.all:
            paths = sorted(reports_dir.glob("*.md"))
            if not paths:
                sys.exit(f"ERROR: no reports in {reports_dir}.")
        else:
            path = reports_dir / (args.report if args.report.endswith(".md") else f"{args.report}.md")
            if not path.exists():
                sys.exit(f"ERROR: {path} not found. Built reports: "
                         f"{sorted(p.stem for p in reports_dir.glob('*.md')) or 'none'}")
            paths = [path]

    total = 0
    for i, path in enumerate(paths):
        if i:
            print()
        total += check_one(path, wanted, args.student, args.limit)

    if len(paths) > 1:
        print(f"\n{len(paths)} report(s), {total} finding(s) total")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
