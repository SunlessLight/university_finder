"""
build_application_prep.py — render an action-only application-prep guide for one
region, grouped by application system.

Reads a research JSON the agent assembles from official admissions/financial-aid
pages and renders a single Markdown guide that answers one question — *what do I
need to do to apply?* — for every Shortlist/Finalist university in a region. It
groups universities by their application system (e.g. Common App vs a school's own
portal) so the student files shared items once, and it foregrounds the hard apply
mechanics: deadlines, tests, essays, fees, and the financial-aid forms/documents/
dates. Writes it to data/students/<slug>/application_prep/<region>.md.

This is a decision-support / how-to-apply deliverable (sibling of build_calendar.py):
read-only against master_list.csv — it does NOT change List status or flip rows.
It complements the per-university report (build_report.py); it does not replace it.

Every university must carry non-empty deadlines + application_checklist + financial_aid,
or the build fails loudly — a half-researched apply guide shouldn't pass.

Usage:
    python tools/build_application_prep.py --student <slug> --input .tmp/<slug>/apply_prep_us.json

Input JSON shape (see workflows/08_application_prep.md for the full spec):
    {
      "student_slug": "<slug>",
      "region": "us",
      "region_title": "United States",
      # Optional. 3-6 imperative next actions, rendered as an ordered list right
      # after the Contents so the guide opens on something to DO.
      "start_here": ["Register for the SAT — sit it by 3 Oct 2026", "..."],
      # Optional. Makes every "~RM" figure in the guide checkable.
      "fx": {"rate": "USD 1 = RM 4.10", "as_of": "2026-07-25"},
      # Optional. One line on which cycle the cost figures are from, and when the
      # entry-year figures publish — rendered as a callout above the universities.
      "cost_cycle_note": "These are the published 2026-27 figures ...",
      "overview": "markdown — the cross-cutting apply strategy for this region",
      "systems": [
        {"system": "Common App",
         "universities": ["Princeton", "Stanford", "UPenn", "Harvard", "Yale"],
         "shared_checklist": "markdown — items filed once across these schools"},
        {"system": "MIT application (own portal, NOT Common App)",
         "universities": ["MIT"], "shared_checklist": "markdown"}
      ],
      "universities": [
        {"name": "Princeton University", "system": "Common App",
         "admission_likelihood": "Reach",
         "deadlines": {"application": "2027-01-01 (RD; SCEA 2026-11-01)", "aid": "..."},
         "tests": "markdown", "essays": "markdown", "fees": "markdown",
         "financial_aid": {"model": "need-blind — asking can't hurt you",
                           "cost": "USD 90k/yr all-in (~RM 425k) — tuition 62k · housing+food 22k",
                           "covers": "100% of that 90k for your band — you pay 0",
                           "your_share": "~USD 3.5k/yr summer-work contribution + flights + visa",
                           "forms": "CSS Profile + IDOC", "documents": "parents' tax/income docs",
                           "dates": "file with the application"},
         "application_checklist": ["one action per item"], "portal": "https://..."}
      ],
      "consolidated_checklist": "markdown — the gather-once list across the region",
      "dated_items": [
        {"date": "2027-01-01", "label": "Regular Decision deadline", "action": "Submit"}
      ],
      "sources": [
        {"title": "...", "url": "...", "authority": "Official"|"Aggregator", "as_of": "2027"}
      ]
    }
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_glossary  # noqa: E402
from shortlist_schema import _parse_iso_date, slugify  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = REPO_ROOT / "data" / "students"

# Per-university subsection order. deadlines/application_checklist/financial_aid are
# required (enforced in validate); the rest are optional-but-recommended. Deadlines is
# rendered first as its own lettered section (see render_systems), so it isn't listed here.
UNI_FIELDS = [
    ("tests", "Tests"),
    ("essays", "Essays"),
    ("fees", "Application fee"),
    ("financial_aid", "Financial aid — cost, what's covered, forms, dates"),
    ("application_checklist", "What to gather / do"),
]
REQUIRED_UNI_FIELDS = ("application_checklist", "financial_aid")

# Financial aid renders as fixed sub-labels (in this order) when authored as an object,
# so the densest field is scannable and consistent across universities. A legacy string
# is passed through unchanged. See render_financial_aid.
#
# `cost` precedes `covers` on purpose: "meets 100% of need" is meaningless until the
# student has seen the number it is 100% *of*. `your_share` follows it so the residual
# the aid does NOT pay (student contribution, flights, visa) can't be skipped either.
FINANCIAL_AID_FIELDS = [
    ("model", "Model"),
    ("cost", "Cost"),
    ("covers", "Covers"),
    ("your_share", "Your share"),
    ("forms", "Forms"),
    ("documents", "Documents"),
    ("dates", "Dates"),
]

# Region-agnostic preamble, prepended to every guide so the student knows what they're
# looking at (and how the jump-links work) without an agent hand-writing it each time.
INTRO = """> **How to use this guide.** This is your **action list** for applying to these universities —
> the deadlines, tests, essays, fees, and financial-aid forms, with the shared work grouped so you do it
> once. It is *not* a "which university is best for me?" guide (that's your university reports). Work top to bottom:
> begin with **Start here**, read the strategy, then work each checklist. **Don't know a term? Tap it —
> every piece of jargon links to its plain-English meaning in [Key terms](#sec-key-terms) at the back.**
> Use the Contents to jump around."""

# Checklist-style fields get rendered as tickable `- [ ]` items instead of prose runs.
_BULLET_RE = re.compile(r"^(\s*)[-*]\s+(.*)$")

# A top-level list item, and "a line that is already part of a list" (indented
# continuation or another item). Used by ensure_list_spacing.
#
# The marker must be followed by whitespace in both: a line opening with `**Bold
# lead:**` starts with `*` but is a paragraph, not a bullet. Without the `\s` the
# normaliser mistook it for an open list and skipped the blank line it needed —
# which is exactly the "**To confirm:**" heading over the calendar's undated items.
_LIST_START = re.compile(r"^([-*+]|\d+\.)\s")
_LIST_CONT = re.compile(r"^(\s|([-*+]|\d+\.)\s)")


def ensure_list_spacing(md):
    """
    Insert a blank line before a top-level list that directly follows a paragraph.

    python-markdown's `sane_lists` (which the PDF path enables) refuses to open a
    list without a preceding blank line, so an authored "lead sentence:" butted
    against its bullets silently collapses into one prose blob — it looks correct
    in the .md source but renders as a wall of text with literal `-` markers in the
    PDF. This bit the US guide three times, worst of all the region-wide "Gather
    once" checklist (1,122 characters as a single paragraph), and it also defeated
    the two-column layout: with no <ul> to lay out, `.cols2` had nothing to act on.

    Normalising here means an author never has to remember the blank line, and every
    existing region JSON is repaired with no re-authoring.
    """
    out, in_fence = [], False
    for line in md.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and _LIST_START.match(line) and out:
            prev = out[-1]
            # Only when the previous line is prose: non-blank, not already part of a
            # list, and not a heading (a list right after a heading parses fine).
            if prev.strip() and not _LIST_CONT.match(prev) and not prev.lstrip().startswith("#"):
                out.append("")
        out.append(line)
    return "\n".join(out)


def as_checklist(value):
    """
    Render a checklist field as tickable `- [ ]` items.

    Accepts either a list (preferred, new convention — one action per item) or a
    legacy markdown string. For strings: existing top-level `-`/`*` bullets become
    `- [ ]` (lead paragraphs and indented continuations are left as-is), and a plain
    ` · `-separated line is split into one checkbox per item. Returns markdown.
    """
    if isinstance(value, list):
        items = [str(v).strip() for v in value if str(v).strip()]
        return "\n".join(f"- [ ] {it}" for it in items)

    text = (value or "").strip()
    if not text:
        return ""

    lines = text.splitlines()
    has_bullets = any(_BULLET_RE.match(ln) for ln in lines)
    if has_bullets:
        out = []
        for ln in lines:
            m = _BULLET_RE.match(ln)
            if m and not m.group(1):          # top-level bullet only
                out.append(f"- [ ] {m.group(2)}")
            elif ln.startswith((" ", "\t")) and out and out[-1].startswith("- [ ] "):
                # A wrapped continuation of the item above — fold it back in. Left on
                # its own line, a continuation that happens to *begin* with "+" or "-"
                # (e.g. "1 maths/science\n  + 1 other") parses as a bullet in its own
                # right and splits one action into two.
                out[-1] = f"{out[-1].rstrip()} {ln.strip()}"
            else:
                out.append(ln)                 # lead sentence / other prose
        return "\n".join(out)

    # Plain prose. A ` · `-separated line is really a jammed-together checklist.
    if " · " in text:
        items = [it.strip().rstrip(".") for it in text.split(" · ") if it.strip()]
        return "\n".join(f"- [ ] {it}" for it in items)
    return text


def checklist_block(value, twocol_min=7):
    """
    Render a checklist and, when it's long, wrap it in a `.cols2` div so the PDF lays it
    out in two columns (used for the "Filed once" and region-wide "Gather once" lists).
    Short lists stay single-column rows. Returns '' for an empty checklist.
    """
    md = as_checklist(value)
    if not md.strip():
        return ""
    items = sum(1 for ln in md.splitlines() if ln.lstrip().startswith("- [ ]"))
    if items >= twocol_min:
        return f'<div class="cols2" markdown="1">\n{md}\n</div>'
    return md


def render_financial_aid(value):
    """
    Financial aid as fixed, scannable sub-labels (Model / Cost / Covers / Your share /
    Forms / Documents / Dates) when authored as an object; a legacy markdown string is
    passed through as-is.

    A value may be a single line ("- **Label** — text") or its own list of `- ` bullets,
    which nest *under* the label instead of flattening to sibling level — the denser aid
    fields (`your_share`, `covers`) need the breakdown room.
    """
    if not isinstance(value, dict):
        return (value or "").strip()

    lines = []
    for key, label in FINANCIAL_AID_FIELDS:
        text = str(value.get(key) or "").strip()
        if not text:
            continue
        if text.startswith("- "):
            # Authored as sub-bullets: label on its own row, bullets indented beneath it.
            # 4 spaces, not 2 — python-markdown (the PDF path, with `sane_lists`) only
            # nests at 4; at 2 the sub-points silently flatten to sibling level in the
            # PDF while still looking correct in the .md.
            lines.append(f"- **{label}**")
            lines.extend(f"    {ln.strip()}" for ln in text.splitlines() if ln.strip())
        else:
            lines.append(f"- **{label}** — {text}")
    return "\n".join(lines)


def anchorize_and_toc(body):
    """
    Inject an explicit `<a id>` anchor into every ## / ### / #### heading and build
    a nested Contents list linking to them. Returns (toc_markdown, body_with_anchors).

    Explicit HTML anchors (rather than relying on auto-slugging) make the jump-links
    resolve identically in GitHub/VS Code *and* in the PDF renderer.

    The anchor goes *inside* the heading line, not on its own line above it: a bare
    `<a id="..."></a>` on its own line is parsed as a paragraph, so every heading in
    the guide used to be preceded by an empty <p> carrying a 7pt margin — 20 of them
    in the US guide — which added dead space and an extra page-break opportunity
    immediately before each heading.
    """
    out_lines, toc, used = [], [], set()
    in_fence = False
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        m = None if in_fence else re.match(r"(#{2,4})\s+(.*)$", stripped)
        if not m:
            out_lines.append(line)
            continue
        level = len(m.group(1))
        display = re.sub(r"[*_`]", "", m.group(2)).strip()
        anchor = "sec-" + (slugify(display) or "x")
        n, base = 2, anchor
        while anchor in used:
            anchor, n = f"{base}-{n}", n + 1
        used.add(anchor)
        toc.append(f"{'  ' * (level - 2)}- [{display}](#{anchor})")
        out_lines.append(f'{m.group(1)} <a id="{anchor}"></a>{m.group(2)}')
    # Wrapped in a .toc div so the stylesheet can tighten it. (A `h2#toc + ul` rule
    # can't work: no `toc` markdown extension is enabled, so headings carry no ids.)
    toc_md = ('## Contents\n\n<div class="toc" markdown="1">\n\n'
              + "\n".join(toc) + "\n\n</div>") if toc else ""
    return toc_md, "\n".join(out_lines)


def _is_empty(val):
    """True if a field carries no content — handles list, dict (aid object), or string."""
    if isinstance(val, list):
        return not [x for x in val if str(x).strip()]
    if isinstance(val, dict):
        return not [x for x in val.values() if str(x).strip()]
    return not (val or "").strip()


def validate(data):
    """Fail loudly if required top-level fields or per-university fields are missing/empty."""
    if not (data.get("region") or "").strip():
        sys.exit("ERROR: apply-prep JSON is missing required field 'region'.")
    if not (data.get("overview") or "").strip():
        sys.exit("ERROR: apply-prep JSON has an empty 'overview' — write the region apply strategy.")
    if not data.get("systems"):
        sys.exit("ERROR: apply-prep JSON has no 'systems' — group the universities by application system.")
    unis = data.get("universities") or []
    if not unis:
        sys.exit("ERROR: apply-prep JSON lists no 'universities'.")

    problems = []
    for i, u in enumerate(unis):
        name = (u.get("name") or "").strip() or f"university[{i}]"
        if not name.strip() or name == f"university[{i}]":
            problems.append(f"{name}: missing 'name'")
        if not (u.get("deadlines") or {}):
            problems.append(f"{name}: missing 'deadlines'")
        for key in REQUIRED_UNI_FIELDS:
            if _is_empty(u.get(key)):
                problems.append(f"{name}: empty '{key}'")
    if problems:
        sys.exit(
            "ERROR: apply-prep guide is incomplete —\n  - "
            + "\n  - ".join(problems)
            + "\nEvery university needs deadlines + application_checklist + financial_aid "
            "(research them, or write 'Not found — <why>')."
        )
    if not data.get("sources"):
        sys.exit("ERROR: apply-prep guide has no sources. Every hard fact needs a citation.")


def render_deadlines(deadlines):
    labels = {"application": "Application deadline", "aid": "Financial-aid deadline"}
    lines = []
    for key, value in deadlines.items():
        if not value:
            continue
        lines.append(f"- **{labels.get(key, key.replace('_', ' ').title())}:** {value}")
    return "\n".join(lines) if lines else "- _To confirm._"


def render_snapshot(data, unis):
    systems = data.get("systems") or []
    rows = [
        ("Region", data.get("region_title") or data.get("region")),
        ("Universities", str(len(unis))),
    ]
    lines = [f"- **{label}:** {value or '—'}" for label, value in rows]
    for s in systems:
        members = ", ".join(s.get("universities") or []) or "—"
        lines.append(f"- **{s.get('system', 'System')}:** {members}")
    # Every "~RM" figure in a guide is a derived conversion. Stating the rate and the
    # date it was taken is what makes those numbers checkable rather than assertions.
    fx = data.get("fx") or {}
    if isinstance(fx, dict) and (fx.get("rate") or "").strip():
        stamp = f" (as of {fx['as_of']})" if (fx.get("as_of") or "").strip() else ""
        lines.append(f"- **MYR conversions use:** {fx['rate'].strip()}{stamp}")
    return "\n".join(lines)


def render_start_here(items):
    """
    The 'do these first' opener — a short ordered list of the next concrete actions,
    rendered directly after the Contents.

    The guide is ~15 pages; without this the student's first page of content was 27
    glossary definitions. Ordered (not tickable) on purpose: this is a sequence, and
    the tickable checklists live further down where the detail is.
    """
    if isinstance(items, str):
        items = [ln.strip().lstrip("-*").strip() for ln in items.splitlines() if ln.strip()]
    actions = [str(i).strip() for i in (items or []) if str(i).strip()]
    if not actions:
        return ""
    return "\n".join(f"{n}. {a}" for n, a in enumerate(actions, 1))


def _render_field(key, value):
    """Render one per-university field to markdown. Checklist and financial-aid fields
    get their structured treatment; everything else is prose (authored as sub-bullets)."""
    if key == "application_checklist":
        return as_checklist(value)
    if key == "financial_aid":
        return render_financial_aid(value)
    return (value or "").strip()


def render_systems(data, unis_by_name):
    parts = []
    uni_no = 0  # continuous 1..N across every system group (see 08_application_prep.md)
    for s in data.get("systems") or []:
        system = s.get("system", "Application system")
        parts.append(f"### {system}")
        members = s.get("universities") or []
        if members:
            parts.append(f"_Universities: {', '.join(members)}._")
            parts.append("")
        shared = checklist_block(s.get("shared_checklist"))
        if shared:
            parts.append("**Filed once across these schools:**")
            parts.append("")
            parts.append(shared)
            parts.append("")
        # Per-university subsections, in the order the system lists them.
        ordered = [unis_by_name[m] for m in members if m in unis_by_name]
        # Any universities tagged with this system but not named in `universities` list.
        ordered += [u for u in data.get("universities", [])
                    if u.get("system") == system and u not in ordered]
        for u in ordered:
            uni_no += 1
            heading = f"{uni_no}. {u.get('name', 'University')}"
            likelihood = (u.get("admission_likelihood") or "").strip()
            if likelihood:
                heading += f" — {likelihood}"
            parts.append(f"#### {heading}")

            # Gather the sections that actually have content, then letter them a, b, c…
            # (contiguously) and render each as a bold sub-heading + an indented body.
            sections = [("Deadlines", render_deadlines(u.get("deadlines") or {}))]
            sections += [(label, _render_field(key, u.get(key))) for key, label in UNI_FIELDS]
            letter = ord("a")
            for label, value in sections:
                if not value.strip():
                    continue
                parts.append(f"##### {chr(letter)}. {label}")
                parts.append("")
                parts.append('<div class="apply-body" markdown="1">')
                parts.append("")
                parts.append(value)
                parts.append("")
                parts.append("</div>")
                parts.append("")
                letter += 1
            portal = (u.get("portal") or "").strip()
            if portal:
                parts.append(f"**Portal:** {portal}")
                parts.append("")
    return "\n".join(parts).rstrip()


def render_calendar(dated_items):
    dated = sorted(
        [(it, _parse_iso_date(it.get("date"))) for it in dated_items],
        key=lambda pair: (pair[1] is None, pair[1] or ""),
    )
    known = [(it, d) for it, d in dated if d]
    unknown = [it for it, d in dated if not d]
    lines = []
    if known:
        lines.append("| Date | What | Action |")
        lines.append("| --- | --- | --- |")
        for it, d in known:
            lines.append(f"| {d.isoformat()} | {it.get('label', '')} | {it.get('action', '')} |")
    if unknown:
        lines.append("")
        lines.append("**To confirm:**")
        for it in unknown:
            raw = f" (\"{it.get('date')}\")" if it.get("date") else ""
            lines.append(f"- {it.get('label', 'Date')} — {it.get('action', '')}{raw}")
    return "\n".join(lines) if lines else "_No dated items yet._"


def render_sources(sources):
    lines = []
    for s in sources:
        title = s.get("title") or s.get("url") or "source"
        url = s.get("url") or ""
        suffix = " — ".join(
            x for x in [s.get("authority") or "", f"as of {s['as_of']}" if s.get("as_of") else ""] if x
        )
        link = f"[{title}]({url})" if url else title
        lines.append(f"- {link}{(' — ' + suffix) if suffix else ''}")
    return "\n".join(lines)


def render_guide(data):
    unis = data.get("universities") or []
    unis_by_name = {u.get("name"): u for u in unis if u.get("name")}
    region_title = data.get("region_title") or data.get("region")

    # --- The "middle": the substantive content (Start here → Deadline calendar). ---
    middle = []
    start_here = render_start_here(data.get("start_here"))
    if start_here:
        n = len([ln for ln in start_here.splitlines() if ln.strip()])
        middle += [f"## Start here — your next {n} actions", "", start_here, ""]
    middle += ["## Snapshot", render_snapshot(data, unis), "",
               f"## {region_title} application strategy", data["overview"].strip(), "",
               "## Grouped by application system"]
    # Cost figures are almost always the *current* cycle's published numbers while the
    # student is applying for the next one. Say so once, next to the money.
    cycle_note = (data.get("cost_cycle_note") or "").strip()
    if cycle_note:
        middle += ["", f"> **On the cost figures.** {cycle_note}", ""]
    middle += [render_systems(data, unis_by_name), ""]
    gather = checklist_block(data.get("consolidated_checklist"))
    if gather:
        middle += ["## Gather once (across the whole region)", "", gather, ""]
    middle += ["## Deadline calendar", render_calendar(data.get("dated_items") or []), ""]
    middle_md = "\n".join(middle)

    # Glossary is built from the raw middle (so it lists terms actually used); the
    # middle then gets its jargon auto-linked to those anchors.
    glossary_md = apply_glossary.build_glossary_section(middle_md, title="Key terms")
    linked_middle = apply_glossary.link_terms(middle_md)

    sources_md = "## Sources\n" + render_sources(data.get("sources") or [])

    # Body = linked middle + Key terms + Sources, then anchors + a Contents list.
    # Key terms sits at the BACK: it is a reference appendix the jump-links reach on
    # demand, and leading with ~27 definitions meant the student's first page of
    # content was a dictionary rather than an action.
    body_sections = [s for s in (linked_middle, glossary_md, sources_md) if s.strip()]
    toc_md, body_with_anchors = anchorize_and_toc("\n\n".join(body_sections))

    doc = [f"# Application prep — {region_title}: {len(unis)} universities", "",
           INTRO, ""]
    if toc_md:
        doc += [toc_md, ""]
    doc += [body_with_anchors, ""]
    # Normalise list spacing last, so it also catches lists inside authored prose
    # fields (overview, tests, essays, aid) and the assembled scaffolding alike.
    return ensure_list_spacing("\n".join(doc))


def main():
    parser = argparse.ArgumentParser(
        description="Render an action-only, per-region application-prep guide grouped by application system."
    )
    parser.add_argument("--student", required=True, help="Student slug (folder under data/students/).")
    parser.add_argument("--input", required=True, help="Path to the apply-prep research JSON.")
    args = parser.parse_args()

    student_dir = STUDENTS_DIR / args.student
    if not student_dir.exists():
        sys.exit(f"ERROR: {student_dir} not found. Run init_student.py first.")

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = REPO_ROOT / input_path
    if not input_path.exists():
        sys.exit(f"ERROR: {input_path} not found.")

    data = json.loads(input_path.read_text(encoding="utf-8"))
    validate(data)

    region_slug = slugify(data.get("region"))
    out_dir = student_dir / "application_prep"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{region_slug}.md"
    out_path.write_text(render_guide(data), encoding="utf-8")
    print(f"Wrote application-prep guide: {out_path}  ({len(data.get('universities') or [])} universities)")


if __name__ == "__main__":
    main()
