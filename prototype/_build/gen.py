"""Generator for prototype/data.js (and, on a first run only, the 14 screen stubs).

usage: python gen.py <repo_root> <data_template>

data.js is always rewritten from the template: edit data.template.js and re-run, never hand-edit
data.js. A screen file that already exists is never touched (the real screens replaced the stubs
on 2026-10-10; an unguarded re-run that day overwrote all 14 and they had to come back from git).
"""
import csv
import json
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
template = Path(sys.argv[2]).read_text(encoding="utf-8")
proto = repo / "prototype"

COLUMNS = [
    ("List status", "listStatus"), ("Desirability", "desirability"), ("Tier", "tier"),
    ("Admission likelihood", "admissionLikelihood"), ("Warnings", "warnings"),
    ("University", "university"), ("Course", "course"), ("Course at a glance", "courseAtAGlance"),
    ("Country", "country"), ("City", "city"), ("Student life", "studentLife"),
    ("Subject rank", "subjectRank"), ("Overall rank", "overallRank"),
    ("Entry requirements", "entryRequirements"), ("Student grades", "studentGrades"),
    ("Grades vs entry bar", "gradesVsEntryBar"), ("English req", "englishReq"),
    ("Annual tuition", "annualTuition"), ("Total tuition", "totalTuition"),
    ("Est. living/yr", "estLivingPerYear"), ("Duration (yrs)", "durationYears"),
    ("Approx total (MYR)", "approxTotalMyr"), ("Scholarship & portal", "scholarshipAndPortal"),
    ("Scholarship coverage", "scholarshipCoverage"),
    ("Scholarship competitiveness", "scholarshipCompetitiveness"),
    ("How to get the scholarship", "howToGetScholarship"),
    ("Money to show (visa)", "moneyToShowVisa"),
    ("Work rights after graduating", "workRightsAfterGraduating"),
    ("Recognised in Malaysia?", "recognisedInMalaysia"), ("How to apply", "howToApply"),
    ("Key deadline", "keyDeadline"), ("Intake", "intake"), ("Notes", "notes"),
    ("Course URL", "courseUrl"), ("Info source", "infoSource"),
]
IDS = {
    "Massachusetts Institute of Technology": ("mit", "MIT"),
    "University of Oxford": ("oxford", "Oxford"),
    "National University of Singapore": ("nus", "NUS"),
    "Princeton University": ("princeton", "Princeton"),
    "Tsinghua University": ("tsinghua", "Tsinghua"),
    "Stanford University": ("stanford", "Stanford"),
    "UNSW Sydney": ("unsw", "UNSW"),
    "Harvard University": ("harvard", "Harvard"),
    "Imperial College London": ("imperial", "Imperial"),
    "Monash University": ("monash", "Monash"),
    "Nanyang Technological University": ("ntu", "NTU"),
    "Rose-Hulman Institute of Technology": ("rose-hulman", "Rose-Hulman"),
    "Northeastern University": ("northeastern", "Northeastern"),
    "University of Melbourne": ("melbourne", "Melbourne"),
    "Carnegie Mellon University": ("cmu", "Carnegie Mellon"),
}
NUMERIC = {"desirability", "durationYears", "approxTotalMyr"}

# --- universities ---
src = repo / "business/sales/sample_pack/sample_master_list.csv"
with src.open(encoding="utf-8-sig", newline="") as fh:
    reader = csv.DictReader(fh)
    assert reader.fieldnames == [c for c, _ in COLUMNS], reader.fieldnames
    raw = list(reader)

rows = []
for r in raw:
    uid, short = IDS[r["University"]]
    row = {"id": uid, "shortName": short}
    for label, key in COLUMNS:
        value = r[label].strip()
        if key in NUMERIC:
            number = float(value.replace(",", ""))
            assert number == int(number), (uid, key, value)
            value = int(number)
        row[key] = value
    rows.append(row)
assert len(rows) == 15 and len({r["id"] for r in rows}) == 15
# Corrections to the sample CSV, which is older than the sample MIT report (Evan, 2026-10-10:
# "follow the report, the spreadsheet is outdated"). (id, key): (text in the CSV, text shown).
OVERRIDES = {
    ("mit", "entryRequirements"): (
        "Holistic; no fixed grades. SAT/ACT optional-ish; top academics expected",
        "Holistic; no fixed grades. SAT or ACT required; top academics expected"),
}
for (uid, key), (old, new) in OVERRIDES.items():
    row = next(r for r in rows if r["id"] == uid)
    assert row[key] == old, (uid, key, row[key])  # the CSV changed: re-check the override
    row[key] = new

# --- report sections ---
sections = []
for line in (repo / "business/university_report.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^\|\s*(\d+)\s*\|(.+)\|\s*$", line)
    if not m:
        continue
    cells = [c.strip().replace("**", "") for c in m.group(2).split("|")]
    if len(cells) != 3:  # the 4-step overview table also has numbered rows
        continue
    title, tells, question = cells
    sections.append({"n": int(m.group(1)), "title": title, "tells": tells, "question": question})
assert [s["n"] for s in sections] == list(range(1, 16)), [s["n"] for s in sections]


def js(value):
    return json.dumps(value, indent=2, ensure_ascii=False).replace("\n", "\n  ")


out = (template
       .replace("/*@COLUMNS@*/", js([{"key": k, "label": l} for l, k in COLUMNS]))
       .replace("/*@UNIVERSITIES@*/", js(rows))
       .replace("/*@REPORT_SECTIONS@*/", js(sections)))
assert "/*@" not in out
(proto / "data.js").write_text(out, encoding="utf-8", newline="\n")

# --- screen stubs ---
# (id, owner, heading, what goes here, button label, next screen)
SCREENS = [
    ("landing", "A", "Landing",
     "The one-line pitch, the three deliverables (List, Report, Apply Guide) and early-tester feedback will go here.",
     "Start, 2 minutes", "onboarding"),
    ("onboarding", "A", "Onboarding",
     "Three short steps (about you, what you want, money), pre-filled from the sample student, will go here.",
     "Finish sign-up", "waiting"),
    ("waiting", "A", "We're building your list",
     "The progress steps, the WhatsApp note and a preview of what is coming will go here.",
     None, "results"),
    ("results", "B", "Your results",
     "The welcome-back page will go here: five top picks as cards, what we found, and the spreadsheet download.",
     "See the full list", "list"),
    ("list", "B", "Your full list",
     "The table of every university, with tick boxes to choose which ones get a deep report, will go here.",
     "Get my report", "report"),
    ("report", "C", "University report",
     "The MIT report will go here: a one-page summary, the section list, and why here / why hesitate.",
     "Decide and apply", "decide"),
    ("decide", "C", "Decide and apply",
     "The recommended university, the deadline calendar and the apply steps will go here.",
     "Back to the start", "landing"),
]
(proto / "screens").mkdir(exist_ok=True)
written = 0
for n, (sid, owner, heading, line, label, nxt) in enumerate(SCREENS, 1):
    if sid == "waiting":
        action = ("      '<button type=\"button\" class=\"btn btn-ghost stub-skip\" data-skip>Skip ahead (demo)</button>' +\n")
        wiring = (
            "\n    // Demo control: pretend the list has been built, then show it.\n"
            "    root.querySelector('[data-skip]').addEventListener('click', function () {\n"
            "      App.setState({ ready: true });\n"
            "      App.go('results');\n"
            "    });\n")
    else:
        kind = "btn-ghost" if sid == "decide" else "btn-primary"
        action = f"      '<button type=\"button\" class=\"btn {kind}\" data-go=\"{nxt}\">{label}</button>' +\n"
        wiring = ""
    js_text = (
        f"/* Screen {n} of 7: {sid}. Owner: Session {owner}.\n"
        f"   Stub from Session 1 — replace the body of render(). */\n"
        f"App.register('{sid}', {{\n"
        f"  render: function (root, state, data) {{\n"
        f"    root.innerHTML =\n"
        f"      '<div class=\"stub card\">' +\n"
        f"      '<p class=\"section-title\">Screen {n} of 7</p>' +\n"
        f"      '<h1>{heading.replace(chr(39), chr(92) + chr(39))}</h1>' +\n"
        f"      '<p class=\"muted\">{line.replace(chr(39), chr(92) + chr(39))}</p>' +\n"
        f"{action}"
        f"      '</div>';\n"
        f"{wiring}"
        f"  }}\n"
        f"}});\n")
    css_text = (
        f"/* Screen {n} of 7: {sid}. Owner: Session {owner}.\n"
        f"   Every selector in this file must start with .screen-{sid} so nothing leaks into\n"
        f"   another screen. Use the shared classes and tokens in ../styles.css first. */\n")
    for ext, text in (("js", js_text), ("css", css_text)):
        target = proto / "screens" / f"{sid}.{ext}"
        if target.exists():  # a real screen lives here now: never overwrite it
            continue
        target.write_text(text, encoding="utf-8", newline="\n")
        written += 1

print(f"data.js: {len(rows)} rows x {len(COLUMNS)} columns, {len(sections)} report sections")
print(f"stubs: {written} written, {len(SCREENS) * 2 - written} existing screen files left alone")
