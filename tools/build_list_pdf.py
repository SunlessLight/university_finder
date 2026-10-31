"""
build_list_pdf.py — the student's university list as a portrait PDF.

2026-10-30 (plans/list_pdf_plan.md T6): new. The PDF replaces the spreadsheet download
(Decisions item 1). Five parts, in this order: student profile, summary table, key to the
judgment labels, one card per university, glossary. master_list.csv stays the working
file; this only reads it.

What it leaves out (Decisions items 2, 8, 9): rows with List status Rejected, and the
columns in HIDDEN_COLUMNS. Admission likelihood is internal only; Admit rate (a published
fact) is what the student sees.

Money: the cost breakdown on each card is computed here, not by the AI (Decisions item 6):
total tuition + living x years in the local currency, the FX_TO_MYR rate and FX_AS_OF,
then the RM total. The card's total line always prints the row's Approx total (MYR), so
card and summary never disagree.

2026-10-30 (E1, Evan): no notes to ourselves on the student's page. A money cell holding
more than "<CODE> <number>", or parts that don't add up to Approx total (MYR), is a
problem printed to the terminal, and the build stops (exit 1). --draft builds anyway for
review: the figure is read by its first number and the footer says "Draft, not for
sending". Fix the cell in master_list.csv (apply_backfill.py), never in the PDF.

Links: each card ends with "Useful links": the Course URL, the row's Apply link and
Scholarship link (columns planned in T3c; printed when present), and the official site
of every shared system the card mentions (apply_glossary.OFFICIAL_LINKS: Common App,
CSS Profile, IELTS...).

2026-10-31 (O8, Evan): the card's living line says "Estimated", because living costs are
estimates even on a row whose hard facts are checked on the official page.

Engine: WeasyPrint via apply_prep_to_pdf._load_weasyprint() (adds the GTK DLL dir on
Windows). Run with the project venv: .venv/Scripts/python.exe. Template + stylesheet:
tools/templates/list_pdf.html / list_pdf.css (string.Template, $placeholders).

Usage:
    .venv/Scripts/python.exe tools/build_list_pdf.py --student <slug>
        # reads data/students/<slug>/{profile,preferences}.json + master_list.csv,
        # writes data/students/<slug>/list.pdf (gitignored; never commit it)
    .venv/Scripts/python.exe tools/build_list_pdf.py \
        --file business/sales/sample_pack/sample_master_list.csv \
        --profile business/sales/sample_pack/sample_profile.json --out .tmp/sample_list.pdf
        # --profile: a profile.json; an optional "preferences" key stands in for preferences.json
    ... --draft    # build even with money problems (review copy, never sent)
"""

import argparse
import csv
import json
import re
import sys
from datetime import date
from html import escape, unescape
from pathlib import Path
from string import Template

from apply_glossary import GLOSSARY, JUDGMENT_LABELS, OFFICIAL_LINKS, present_terms
from apply_prep_to_pdf import _load_weasyprint
from shortlist_schema import (
    FX_AS_OF, FX_TO_MYR, INFO_SOURCE_OFFICIAL, RANKING_EDITION, SHORTLIST_HEADERS,
    WARNINGS_NONE, parse_amount, upgrade_header,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
STUDENTS_DIR = ROOT / "data" / "students"
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"

# Never printed (Decisions items 2 and 9). Student grades appear once, in the profile.
HIDDEN_COLUMNS = ("List status", "Tier", "Admission likelihood", "Student grades", "Notes",
                  "Student life", "Money to show (visa)")

# Link columns, printed under "Useful links" in this order when the row has them. Apply link
# and Scholarship link are planned columns (T3c); until then row.get() finds nothing.
LINK_COLUMNS = (("Course URL", "Course page"), ("Apply link", "Apply"),
                ("Scholarship link", "Scholarship"))

# Columns the card prints outside the groups: in its heading, warning box, cost table,
# links or source line.
CARD_FIXED_COLUMNS = ("University", "Course", "Country", "City", "Warnings", "Annual tuition",
                      "Total tuition", "Est. living/yr", "Duration (yrs)", "Approx total (MYR)",
                      "Info source", "Checked on") + tuple(c for c, _ in LINK_COLUMNS)

# The website's grouping (prototype/data.js columnGroups), minus the hidden columns. "What it
# costs" is the computed cost table. A column named nowhere lands in "Good to know".
CARD_GROUPS = [
    ("The course", ["Course at a glance", "Intake"]),
    ("Getting in", ["Entry requirements", "Grades vs entry bar", "English req",
                    "Application requirements", "Admit rate", "How to apply", "Key deadline"]),
    ("What it costs", None),
    ("Scholarships", ["Scholarship & portal", "Scholarship coverage",
                      "Scholarship competitiveness", "How to get the scholarship"]),
    ("After you graduate", ["Work rights after graduating", "Recognised in Malaysia?"]),
    ("How it ranks", ["Subject rank", "Overall rank", "Desirability"]),
]
_PLACED = set(HIDDEN_COLUMNS) | set(CARD_FIXED_COLUMNS) | {
    c for _, cols in CARD_GROUPS if cols for c in cols}
CARD_GROUPS.append(("Good to know", [h for h in SHORTLIST_HEADERS if h not in _PLACED]))

GRADE_STATUS_TEXT = {
    "predicted": "Predicted by your school",
    "actual": "Actual results",
    "expected": "Your own estimate",
}

_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_CURRENCY = re.compile(r"\b(" + "|".join(sorted(FX_TO_MYR, key=len, reverse=True)) + r")\b")
_CLEAN_MONEY = re.compile(r"[A-Z]{3} \d[\d,]*")


# --------------------------------------------------------------------------- #
# Small formatters
# --------------------------------------------------------------------------- #
def fmt_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {d:%b %Y}"


def fmt_rm(amount):
    return f"RM {amount:,.0f}"


def fmt_money(code, amount):
    return f"{code} {amount:,.0f}"


def label_for(column):
    if column in RANKING_EDITION:
        return f"{column} ({RANKING_EDITION[column]})"
    return column


def cell_text(row, column):
    value = row.get(column, "").strip()
    if column == "Desirability" and value:
        return f"{value} / 100"
    return value


def has_warning(row):
    text = row.get("Warnings", "").strip()
    return bool(text) and text != WARNINGS_NONE


def place(row):
    """City and country, once when they match (Singapore)."""
    city, country = row.get("City", "").strip(), row.get("Country", "").strip()
    return country if city == country or not city else f"{city}, {country}"


def short_deadline(cell):
    """The summary table's deadline: the first date, Rolling, or Not published."""
    text = cell.strip()
    if text.lower().startswith("rolling"):
        return "Rolling"
    if text.startswith("Not published"):
        return "Not published"
    m = _ISO_DATE.search(text)
    if not m:
        return text
    approx = text[m.start() - 1:m.start()] == "~" or re.match(r"\s*\(approx", text[m.end():], re.I)
    return fmt_date(m.group(0)) + (" (approx.)" if approx else "")


# --------------------------------------------------------------------------- #
# Money
# --------------------------------------------------------------------------- #
def read_money(cell):
    """(code, amount, clean) for a money cell; clean = it is just "<CODE> <number>".

    Old lists carry caveats after the figure ("GBP 241088 (187,488 university tuition...)");
    parse_amount() takes the first number, and clean=False marks the card for re-checking.
    """
    text = (cell or "").strip()
    if not text:
        return None, None, True
    m = _CURRENCY.search(text)
    code = m.group(1) if m else None
    if code == "RMB":
        code = "CNY"
    return code, parse_amount(text), bool(_CLEAN_MONEY.fullmatch(text)) and code is not None


def cost_breakdown(row):
    """(html, problems) for the card's "What it costs" group; problems go to the terminal."""
    notes, unclean = [], []
    parts = {}
    for column in ("Annual tuition", "Total tuition", "Est. living/yr"):
        code, amount, clean = read_money(row.get(column, ""))
        parts[column] = (code, amount)
        if not clean:
            unclean.append(column)
    codes = {c for c, a in parts.values() if a is not None and c}
    code = next(iter(codes)) if len(codes) == 1 else None
    if len(codes) > 1:
        notes.append("the money cells use different currencies")

    tuition = parts["Total tuition"][1]
    living = parts["Est. living/yr"][1]
    years = parse_amount(row.get("Duration (yrs)", ""))
    listed = parse_amount(row.get("Approx total (MYR)", ""))
    rate = FX_TO_MYR.get(code) if code else None

    lines = []
    annual = parts["Annual tuition"][1]
    if annual is not None and code:
        lines.append(("Tuition per year", fmt_money(code, annual), "rate"))
    if tuition is not None and code:
        lines.append(("Tuition, whole degree", fmt_money(code, tuition), ""))
    total_local = tuition
    if tuition is not None and living is not None and years is not None and code:
        years_txt = f"{years:g} year" + ("" if years == 1 else "s")
        lines.append((f"Estimated living, {fmt_money(code, living)} a year × {years_txt}",
                      fmt_money(code, living * years), ""))
        total_local = tuition + living * years
        lines.append((f"Whole degree in {code}", fmt_money(code, total_local), ""))
    computed = None
    if total_local is not None and rate is not None:
        lines.append((f"Exchange rate on {fmt_date(FX_AS_OF)}", f"1 {code} = RM {rate:g}", "rate"))
        computed = round(total_local * rate)
    if listed is not None:
        lines.append(("Approx total", fmt_rm(listed), "total"))

    for column in unclean:
        notes.append(f"{column} {row.get(column, '').strip()!r} is not '<CODE> <number>'")
    if computed is None:
        notes.append("the parts can't be added up from this row")
    elif listed is not None and computed != round(listed):
        notes.append(f"the parts add up to {fmt_rm(computed)}, not the {fmt_rm(listed)} "
                     "in Approx total (MYR)")

    body = "".join(
        f'<tr class="{cls}"><td>{escape(label)}</td><td class="amt">{escape(amount)}</td></tr>'
        for label, amount, cls in lines)
    return f'<table class="cost">{body}</table>', notes


# --------------------------------------------------------------------------- #
# The five parts
# --------------------------------------------------------------------------- #
def student_items(profile, rows=()):
    """(label, value) facts about the student. build_report.py prints the same ones. rows is the
    list's own rows, for the grades fallback."""
    prefs = profile.get("preferences") or {}
    items = []

    program = (profile.get("current_program") or {}).get("type")
    if program:
        items.append(("Qualification", program))
    subjects = [
        f"{s.get('subject')} {s.get('grade_or_predicted') or ''}".strip()
        for s in profile.get("subjects") or [] if s.get("subject")]
    if subjects:
        items.append(("Subjects", ", ".join(subjects)))
    else:
        # No subjects on the profile: fall back to the grades the rows repeat.
        grades = []
        for r in rows:
            g = r.get("Student grades", "").strip()
            if g and g not in grades:
                grades.append(g)
        if grades:
            items.append(("Grades", "; ".join(grades)))
    status = GRADE_STATUS_TEXT.get(profile.get("grade_status"))
    if status:
        items.append(("Grades are", status))
    english = profile.get("english_proficiency") or {}
    if english.get("test"):
        items.append(("English test", f"{english['test']} {english.get('score') or ''}".strip()))

    courses = prefs.get("specific_courses") or prefs.get("fields_of_interest") or []
    if courses:
        items.append(("Course", ", ".join(courses)))
    countries = prefs.get("target_countries") or []
    if countries:
        items.append(("Countries", ", ".join(countries)))
    budget = prefs.get("total_budget_ceiling") or (profile.get("financial") or {}).get("total_budget")
    if budget:
        items.append(("Budget, whole degree",
                      fmt_rm(budget) if isinstance(budget, (int, float)) else str(budget)))
    if prefs.get("scholarship_required") is not None:
        items.append(("Scholarship needed", "Yes" if prefs["scholarship_required"] else "No"))
    return items


def profile_rows(profile, rows, prepared_on):
    prefs = profile.get("preferences") or {}
    items = student_items(profile, rows)
    priorities = prefs.get("priorities") or []
    if priorities:
        items.append(("What matters most, in order",
                      ", ".join(str(p).replace("_", " ").capitalize() if p == str(p).lower() else str(p)
                                for p in priorities)))
    items.append(("Universities on this list", str(len(rows))))
    items.append(("List prepared on", fmt_date(prepared_on)))
    return "\n".join(f"<dt>{escape(k)}</dt><dd>{escape(v)}</dd>" for k, v in items)


def summary_rows(rows):
    out = []
    for n, r in enumerate(rows, start=1):
        warn = '<span class="warn-mark">!</span>' if has_warning(r) else ""
        total = parse_amount(r.get("Approx total (MYR)", ""))
        out.append(
            "<tr>"
            f'<td class="n">{n}</td>'
            f'<td class="uni">{escape(r.get("University", ""))}{warn}</td>'
            f'<td class="course">{escape(r.get("Course", ""))}</td>'
            f"<td>{escape(place(r))}</td>"
            f'<td class="num">{escape(r.get("Desirability", ""))}</td>'
            f'<td>{escape(r.get("Admit rate", "").strip() or "—")}</td>'
            f'<td>{escape(r.get("Grades vs entry bar", ""))}</td>'
            f'<td class="num">{escape(f"{total:,.0f}" if total is not None else "")}</td>'
            f'<td>{escape(short_deadline(r.get("Key deadline", "")))}</td>'
            "</tr>")
    return "\n".join(out)


def key_rows(rows):
    items = [(term, meta["definition"]) for term, meta in JUDGMENT_LABELS.items()]
    items.append(("Approx total (RM)", "Tuition plus living costs for the whole degree, in "
                  "ringgit, before scholarships."))
    if any(not r.get("Admit rate", "").strip() for r in rows):
        items.append(("—", "Not checked yet."))
    out = [f"<dt>{escape(k)}</dt><dd>{escape(v)}</dd>" for k, v in items]
    if any(has_warning(r) for r in rows):
        out.append('<dt><span class="warn-mark">!</span></dt>'
                   "<dd>This university has a warning. Read it at the top of its card.</dd>")
    return "\n".join(out)


def source_line(row):
    if row.get("Info source", "").strip() == INFO_SOURCE_OFFICIAL:
        checked = row.get("Checked on", "").strip()
        when = f", checked on {fmt_date(checked)}" if _ISO_DATE.fullmatch(checked) else ""
        status = f'<span class="checked">Official page{escape(when)}</span>'
    else:
        status = '<span class="unverified">Not verified</span>'
    return f'<div class="source">{status}</div>'


def useful_links(row, card_text):
    """The row's own links, then the official site of each shared system the card names."""
    links = [(label, row.get(column, "").strip()) for column, label in LINK_COLUMNS]
    links += [(term, OFFICIAL_LINKS[term]) for term in present_terms(card_text)
              if term in OFFICIAL_LINKS and not only_negated(term, card_text)]
    seen, dl = set(), []
    for label, url in links:
        if url and url not in seen:
            seen.add(url)
            dl.append(f'<dt>{escape(label)}</dt><dd><a href="{escape(url)}">{escape(url)}</a></dd>')
    return f'<div class="group"><h4>Useful links</h4><dl>{"".join(dl)}</dl></div>' if dl else ""


def only_negated(term, text):
    """True when every mention reads "not <term>" / "no <term>" ("MIT application (not Common
    App)"), so the card doesn't link a system the university doesn't use."""
    mentions = list(re.finditer(rf"(?<![\w-]){re.escape(term)}(?![\w-])", text))
    return bool(mentions) and all(
        re.search(r"\b(?:not|no)\s+(?:via\s+|through\s+|the\s+)?$", text[:m.start()], re.I)
        for m in mentions)


def card(n, row):
    """(html, problems): problems are for the terminal, never printed on the card."""
    groups, problems = [], []
    for title, columns in CARD_GROUPS:
        if columns is None:
            table, problems = cost_breakdown(row)
            groups.append(f'<div class="group"><h4>{title}</h4>{table}</div>')
            continue
        fields = [(c, cell_text(row, c)) for c in columns if cell_text(row, c)]
        if not fields:
            continue
        dl = "".join(f"<dt>{escape(label_for(c))}</dt><dd>{escape(v)}</dd>" for c, v in fields)
        groups.append(f'<div class="group"><h4>{title}</h4><dl>{dl}</dl></div>')

    warn = (f'<p class="card-warn"><strong>Warning.</strong> {escape(row["Warnings"].strip())}</p>'
            if has_warning(row) else "")
    body = "".join(groups)
    links = useful_links(row, unescape(re.sub(r"<[^>]+>", " ", body)))
    html = (
        '<article class="card">'
        f'<div class="card-head"><h3><span class="num-badge">{n}</span>'
        f'{escape(row.get("University", ""))}</h3>'
        f'<p class="sub">{escape(row.get("Course", ""))} · {escape(place(row))}</p></div>'
        f"{warn}{body}{links}{source_line(row)}"
        "</article>")
    return html, problems


def glossary_rows(visible_html):
    """GLOSSARY entries for the terms the printed list actually uses (link targets skipped)."""
    text = re.sub(r"<a\b[^>]*>.*?</a>", " ", visible_html, flags=re.S)
    text = unescape(re.sub(r"<[^>]+>", " ", text))
    terms = present_terms(text)
    if not terms:
        return '<dd class="muted">No shorthand in this list.</dd>'
    return "\n".join(f"<dt>{escape(t)}</dt><dd>{inline_markdown(GLOSSARY[t]['definition'])}</dd>"
                     for t in terms)


def inline_markdown(text):
    """GLOSSARY definitions use **bold** and *italic*; turn them into HTML."""
    html = escape(text)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    return re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", html)


# --------------------------------------------------------------------------- #
# Loading + rendering
# --------------------------------------------------------------------------- #
def load_rows(csv_path):
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        raw = [r for r in reader if any(cell.strip() for cell in r)]
    header, raw = upgrade_header(header, raw)
    rows = [dict(zip(header, r + [""] * (len(header) - len(r)))) for r in raw]
    return [r for r in rows if r.get("List status", "").strip() != "Rejected"]


def load_profile(profile_path, preferences_path=None):
    profile = json.loads(Path(profile_path).read_text(encoding="utf-8"))
    if preferences_path and Path(preferences_path).exists():
        profile.setdefault("preferences", json.loads(Path(preferences_path).read_text(encoding="utf-8")))
    return profile


def build_html(rows, profile, prepared_on, draft=False):
    """(html, problems): problems = [(university, problem), ...] for the terminal."""
    name = profile.get("name") or "you"
    built = [card(n, r) for n, r in enumerate(rows, start=1)]
    cards_html = "\n".join(html for html, _ in built)
    problems = [(r.get("University", ""), p) for r, (_, ps) in zip(rows, built) for p in ps]
    footer = f"University list for {name} · prepared {fmt_date(prepared_on)}"
    fields = {
        "title": f"University list for {name}",
        "heading": f"{name}'s universities",
        "prepared": f"{len(rows)} universities, prepared on {fmt_date(prepared_on)}",
        "sample_note": (f'<p class="sample-note">{escape(profile["_sample_note"])}</p>'
                        if profile.get("_sample_note") else ""),
        "profile_rows": profile_rows(profile, rows, prepared_on),
        "summary_heading": "Your universities at a glance",
        "summary_rows": summary_rows(rows),
        "key_rows": key_rows(rows),
        "cards": cards_html,
        "footer": escape(f"Draft, not for sending · {footer}" if draft else footer),
    }
    visible = " ".join(fields[k] for k in ("profile_rows", "summary_rows", "key_rows", "cards"))
    fields["glossary_rows"] = glossary_rows(visible)
    template = Template((TEMPLATE_DIR / "list_pdf.html").read_text(encoding="utf-8"))
    html = template.substitute({k: (escape(v) if k in ("title", "heading", "prepared") else v)
                                for k, v in fields.items()})
    return html, problems


def main():
    parser = argparse.ArgumentParser(description="Build the student's university list PDF.")
    parser.add_argument("--student", help="Student slug: reads and writes data/students/<slug>/.")
    parser.add_argument("--file", help="master_list.csv to read (default with --student: theirs).")
    parser.add_argument("--profile", help="profile.json to read (default with --student: theirs).")
    parser.add_argument("--out", help="Output PDF (default with --student: their list.pdf).")
    parser.add_argument("--draft", action="store_true",
                        help="Build even with money problems; footer says 'Draft, not for sending'.")
    args = parser.parse_args()

    preferences = None
    if args.student:
        folder = STUDENTS_DIR / args.student
        if not folder.is_dir():
            sys.exit(f"ERROR: no student folder {folder}")
        args.file = args.file or folder / "master_list.csv"
        args.profile = args.profile or folder / "profile.json"
        args.out = args.out or folder / "list.pdf"
        preferences = folder / "preferences.json"
    if not (args.file and args.profile and args.out):
        sys.exit("ERROR: give --student <slug>, or all of --file, --profile and --out")
    for p in (args.file, args.profile):
        if not Path(p).exists():
            sys.exit(f"ERROR: not found: {p}")

    rows = load_rows(args.file)
    if not rows:
        sys.exit(f"ERROR: no rows to print in {args.file} (all Rejected or empty)")
    profile = load_profile(args.profile, preferences)
    html, problems = build_html(rows, profile, date.today().isoformat(), draft=args.draft)
    if problems:
        print(f"{len(problems)} money problem(s); fix them in master_list.csv (apply_backfill.py):")
        for university, problem in problems:
            print(f"  - {university}: {problem}")
        if not args.draft:
            sys.exit("Not built. Fix the cells above, or pass --draft for a review copy.")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    weasyprint = _load_weasyprint()
    weasyprint.HTML(string=html, base_url=str(TEMPLATE_DIR)).write_pdf(str(out))
    print(f"Wrote {'DRAFT ' if args.draft else ''}PDF: {out} ({len(rows)} universities)")


if __name__ == "__main__":
    main()
