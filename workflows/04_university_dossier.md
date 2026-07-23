# Workflow: Stage 4 — Verify & Dossier (per finalist)

## Objective

For each **finalist** (the 3-5 universities the student picks from the Longlist), produce a deep,
standardized **16-section dossier** (Snapshot + 14 content sections + Sources) that answers three decision
questions — **can I get in? · will I belong & thrive? · what will it take to apply?** — so the student can
*decide*, not just compare. Lead with texture that determines whether they apply; keep the hard-fact
sections as guardrails. This is the most research-intensive stage — do it only for finalists, A-tier and
best-fit first.

> **This stage absorbs the old "verify → shortlist" step.** There is no longer a separate 8-12 Shortlist
> tier: the student picks their finalists straight off the Longlist, and you **verify each pick's hard
> facts before you deep-research it**. Do the pre-flight cut below *first* — it's cheap, and it stops you
> sinking a full dossier into a university that turns out to be over budget or past its deadline.

## Before you research: pick, verify, and cut (the pre-flight)

Longlist facts are *provisional* (snippet-level, often wrong or stale). Run this cheap cut on the
student's picks **before** any deep dossier research:

**1. Pick the finalists.** The student promotes their picks from the Longlist to
**`List status = Shortlist`** (an agent edit to `master_list.csv`) — aim for ~3-5 they genuinely want to
apply to. Render the trade-offs first so the choice is informed:
```powershell
python tools/compare_universities.py --student <slug> --status Longlist --dimensions summary,scholarship,fit
```
Use `--country <name>` to work one destination at a time on a large list. This is the narrowing surface —
the student may keep, drop, or re-add rows; that iteration *is* the cut working.

**2. Verify each pick's hard facts against OFFICIAL sources** — the university's own course page, UCAS, or
Common App, never an aggregator:
- **Tuition** (per year + full programme) + **living cost** → recompute the total; sanity-check `Approx total (MYR)`.
- **Entry requirements** (academic + English) → does the student actually meet them?
- **Key deadline** + **intake** → is the intake offered, and is the deadline still open?
- **Recognition back home** (MQA + the relevant professional body) for regulated professions — a gate, not a footnote.

Set **`Info source = Official page`** on each verified row (it starts `Not verified`). Where the official
page disagrees with a search result, **the official figure wins** — put the discrepancy in `Notes`.
Verifying may need a couple of Firecrawl scrapes of clean official pages — **ask the user before running**,
per `00_overview.md`.

**3. Re-judge admissibility & warnings on the verified facts.** Re-confirm **`Admission likelihood`**
(Reach/Match/Safety) and the hard **`Warnings`** (`Over budget`, `English short`, `Deadline passed`) —
these were computed at Stage 3 from provisional data and often move once real facts land. Predicted grades
keep borderline cases Reach until results come in. To update an existing row's facts, **edit
`master_list.csv` directly** — re-running `sync_shortlist.py` is only for *new* candidates.

**4. Check the set is balanced, and swap out any dud.** Across the picks, confirm a Reach/Match/Safety
spread — at least one **Safety** the student clears comfortably, not five long-shots. If verification kills
a pick (over budget even with scholarship, deadline passed, entry unreachable), demote it to
**`Rejected`** with a one-line reason in `Notes` and have the student pick a replacement from the
Longlist — *before* you sink dossier research into it. For a kept Reach where direct entry is a stretch,
record the **`Backup entry route`** (foundation year / INTO-Kaplan-Navitas / community-college transfer)
and its rough entry bar, so a grades-short student still has a route.

> **Too few survivors?** If the cut leaves fewer than ~3 workable picks, go back to **Stage 3**
> (`03_discover_longlist.md`) and widen discovery (more countries or safer options) rather than
> dossiering weak rows.

Only once a pick survives this cut do you build its dossier below. The dossier's own deep research (Costs,
Scholarships, Visa, Recognition sections) is where the *full* funding and fit detail gets written — you
don't also need to write paragraphs into the master-list scholarship cells; the make-or-break facts above
are enough to earn a dossier.

## Two dossier paths — course vs university (pick with `--mode`)

`build_dossier.py` renders **two** dossier shapes; choose per finalist:

- **`--mode course` (default) — the course-specific dossier.** *"Should I do THIS course here?"* Every
  `master_list.csv` row is a `University + Course` pair, so it matches/flips the row by
  `course_key(university, course)`. Use it for **UK · Australia · Singapore · China** — anywhere you
  apply to a named degree. The 16-section spec below is this path.
- **`--mode university` — the whole-institution dossier. US-only.** *"Should I GO to this university?"*
  US undergrads apply to the **institution** and typically **declare a major in year 2**, so a
  course-anchored dossier asks the wrong question. This path swaps the course lens for institutional
  fit — character, the "type" of student it wants, curriculum shape, culture, aid, setting. It matches/
  flips by **university name only** (ignoring `Course`) and **hard-errors if a matched row's `Country`
  isn't `USA`**. Filename is slugged on the university alone (`stanford-university.md`), so it never
  collides with a course dossier for the same uni — both can coexist. See **"The US university path"** below.

Everything else — the free-search-vs-Firecrawl split, "capture social links, don't scrape", official
sources for hard facts, enforced non-empty sections, the PDF export — is **identical for both paths**.

## Tools used

1. *(agent research)* gather the facts for the 14 content sections. **Hard facts** (fees, requirements,
   visa, recognition, deadlines) come from **official sources** (course page, UCAS/Common App, the
   country's visa site, MQA). **Decision texture** (who gets in, student life, the city) comes from search
   + forums/video/social — capture their URLs + snippets without scraping them.
2. *(agent step)* assemble `.tmp/<slug>/dossier_<uni>.json`.
3. `build_dossier.py --student <slug> --input .tmp/<slug>/dossier_<uni>.json` — renders the dossier and
   flips that row to `List status = Finalist`. (There is no `Dossier status` column — the dossier file
   under `dossiers/` *is* the record that it was built.)

### Which scraper for which section (spend credits where they matter)

- **Claude WebSearch / WebFetch (free) — the default, and the *only* tool for the decision-texture
  sections** (`admitted_profiles`, `student_life_culture`, `city_and_belonging`). Their best sources are
  Reddit / The Student Room / YouTube / Instagram / Discord — which Firecrawl either can't scrape (IG / FB
  / TikTok / X are hard-skipped in `firecrawl_search.py`) or handles unreliably, so paid credits buy almost
  nothing here. Capture the URL + a snippet from the search result; don't try to scrape the page.
- **Firecrawl (paid credits) — reserve for hard-fact official pages that block Claude's plain fetch**: fee
  pages, fee PDFs, some scholarship/visa pages (the recurring "confirm — blocks automated fetch" gaps).
  There the info difference is real (an exact figure vs "confirm later"). Pre-authorised for these official
  pages during dossier research; don't spend credits on the culture/admit sections.
- Firecrawl doesn't offload the agent's reasoning — fetched content still lands in context; the win is
  reliability on protected pages + fewer failed-fetch retries.

## The 16 sections (the tool enforces all 14 content sections — empty = build fails)

Ordered decision-first. **Snapshot (1)** and **Sources (16)** are rendered by the tool; you fill 2–15.

1. **Snapshot** *(auto-rendered as a fact table from the JSON's top-level fields)* — uni · course ·
   country/city · overall rank · subject rank · application system · admission likelihood, plus the
   student's ranked **`priorities`** (set this field — it's where the priorities get stated once, up front).
2. **Entry requirements & this student's fit** — academic + English, the grade margin → Reach/Match/Safety,
   and the **pathway/foundation route** if direct entry is short.
3. **Who actually gets in** — real admitted-student texture: the **extracurriculars, awards, academic
   profile, and essay/interview angles** of people who got in. Sources: results/decision threads (Reddit,
   The Student Room offer-holder threads), "how I got into X" blogs/YouTube, the US **Common Data Set** /
   acceptance-rate, or the grades-based **IGP / cutoff** (NUS, China). **Fallback when thin:** admit-rate /
   cutoff stats **plus official *and* unofficial social channels** (subreddit, IG, Discord, student-society
   pages) as leads for the student to dig further. If genuinely nothing exists, write `Not found — <why>`.
4. **Course details & structure** — modules, duration, intake, placement/sandwich/co-op, flexibility to
   change major (a real UK vs US difference).
5. **Costs (full)** — tuition (per year + full programme), living, application fees, deposit, and the
   **total cost of attendance in MYR**.
6. **Scholarships & financial aid** — university + government/external + **Malaysian sponsors (JPA, MARA,
   Yayasan, PTPTN)**, each with eligibility.
7. **Cost of living & accommodation** — monthly estimate, on/off campus.
8. **Visa & immigration** — financial-proof requirement, visa + health-surcharge cost, work-during-study
   hours, and **post-study work rights** (UK Graduate Route / AUS 485 / US OPT–STEM OPT).
9. **Recognition back home** — **MQA recognition + the relevant Malaysian professional body**; can the
   student practise in Malaysia? (Material only for regulated professions — say "n/a" otherwise.)
10. **Employability & outcomes** — graduate employment rate / salary data, internships, alumni network.
11. **Student life & culture** — the texture that answers *"will I belong?"*: **study life** (workload,
    teaching style, intensity), **life outside study** (clubs, sport, weekends, nightlife), the **student
    personality archetype** (collaborative vs competitive, hands-on vs theoretical), **what a newcomer
    needs to blend in**, **first-year / orientation activities** (freshers, signature first-year projects),
    and **real student voices** (Reddit / The Student Room / YouTube — links + snippets, not scraped).
    This is the **only** home for student-life research since the master-list columns were removed on
    2026-07-16 — it needs paragraphs, which is exactly what a spreadsheet cell can't hold. **For Toru,
    read `data/students/toru/student_life_research.md` first**: 30 rows of this was already researched
    under the old verify-shortlist step and migrated there. Don't pay for it twice.
12. **The city, the area & belonging** — the **city/area feel, safety, transport, and things to do /
    sightseeing**, plus the **Malaysian / halal / prayer / religious-community** angle. Surface
    `needs`-flagged items prominently; otherwise treat as reassuring background, not a decision driver.
13. **Application prep checklist** — *not a step-by-step guide.* A **readiness checklist** of everything to
    gather beforehand so the application is done in one sitting: documents (transcripts, predicted grades),
    tests (English test + status, admissions tests e.g. ESAT/SAT), essays/personal statement, references/
    recommenders, portfolio/interview prep, application + deposit fees, and portal/account setup. Note the
    system (UCAS / Common App / direct portal) but keep the emphasis on *what to prepare*.
14. **Key dates & deadlines** — application, scholarship, admissions-test dates.
15. **Why here / why hesitate** — a short honest synthesis tied to this student's `priorities` / `needs`:
    **2–4 reasons to choose** (the standout hook — signature labs, flagship projects, societies, notable
    alumni *in the student's field*) **and** an explicit **"reasons to hesitate"**. Inform conviction —
    don't sell.
16. **Sources** — each with **authority (Official/Aggregator) + as-of cycle year**.

## The US university path (`--mode university`)

For US finalists, build the whole-institution dossier instead of (or alongside) a course one. It answers
*"is this the right **place** for me?"* — the question US admissions actually turns on.

### What US fit-qualities to look for (the lens)

US universities differ far more in **character** than in course catalogue. Research each through these,
and frame every one as a **"does THIS student fit?"** check — not a brochure:

- **Institutional archetype / "who it's for."** Every top US school has a recognisable type it recruits
  and shapes: **Stanford → founders/builders**, **MIT → makers/hands-on problem-solvers**, **Princeton →
  scholars/researchers** (undergrad research, the senior thesis), **Harvard → future leaders/humanities +
  breadth**, **Caltech → pure scientists**, an LAC → discussion-driven generalists. Name it, then say
  honestly whether the student *is* that person.
- **Curriculum shape.** **Open curriculum** (Brown — almost no requirements) vs **core** (Columbia,
  Chicago — a fixed great-books/science core) vs **distribution** (most — breadth across areas). **When
  you declare a major** (usually end of year 2), how easy it is to switch, and whether **double
  majors / minors / self-designed majors** are normal. This is the single biggest US-vs-elsewhere
  difference — lead with it.
- **Size & setting.** Large research university vs small liberal-arts college; **urban / college-town /
  rural**. Affects class size, teaching (professors vs TAs), and daily life.
- **Culture.** Collaborative vs competitive (P/F first semester? no first-year grades?), intellectual vs
  pre-professional, **Greek life** presence, **sports** (D1 spectacle vs D3), traditions, and how
  **undergrad-focused** it is vs graduate/research-heavy.
- **Aid model — the money reality for an international.** **Need-blind vs need-aware for internationals**,
  **meets-full-need** or not, and **merit** scholarships. (For Malaysian students this is often the gate —
  keep it honest and in MYR.)
- **Support & advising** for internationals, and **outcomes/network** (OPT → STEM-OPT, alumni pull in the
  student's field).

Same scraper split as the course path: **decision-texture** (archetype, culture, student life, city,
food, sentiment) → **free WebSearch + social/forum/video** (Reddit / YouTube / student-society pages —
links + snippets, don't scrape); **hard facts** (aid policy, cost of attendance, deadlines, test
requirements) → **official pages** (Firecrawl gated — ask before spending). If a student already has
`student_life_research.md`, read it first; don't pay for it twice.

### The 14 university sections (the tool enforces all 14 — empty = build fails)

Ordered institution-first. **Snapshot** and **Sources** are rendered by the tool; you fill 1–14.

1. **Identity & mission** — the aim, values, what the place stands for.
2. **Who it's for — the archetype & this student's fit** — the signature "type" (founders/makers/
   scholars/…) + an honest fit check against the student's `profile` / `preferences`.
3. **Getting in — admissions & this student's fit** — holistic profile, admit rate, tests (SAT/ACT +
   whether required this cycle), the grade margin → Reach/Match/Safety, what admits actually look like.
4. **Academic structure & the four years** — open/core/distribution curriculum, gen-ed, **when you
   declare a major**, how years 1–4 split, room to explore before committing. *(Scope: the shape of
   the degree and the timeline. Don't re-explain major-affiliation mechanics in 5 as well — cover
   it once here.)*
5. **Majors, minors & flexibility** — fields it's known for, double-major/minor/self-design, ease of
   switching, and its strength in the student's area of interest. *(Scope: the menu of fields and how
   freely you move between them — not the year-by-year timeline, that's 4.)*
6. **Signature academic experiences** — undergrad research (e.g. MIT's UROP), co-op, study abroad,
   makerspaces/labs, first-year signature projects — the hands-on texture. *(Scope: named programmes
   and hands-on opportunities — not curriculum structure, that's 4/5.)*
7. **Culture & vibe** — collaborative vs competitive, intellectual tone, Greek life, sports (D1/D3),
   traditions, the student personality.
8. **Student life & food** — housing (residential-college system?), clubs, weekends, social scene,
   dining/meal plans, and **halal/dietary options**.
9. **The city, the area & belonging** — setting, safety, transport, weather, things to do, plus the
   **Malaysian / halal / prayer / Muslim-community** angle. Surface `needs`-flagged items prominently.
10. **Costs & financial aid** — cost of attendance, **need-blind vs need-aware for internationals**,
    meets-full-need, merit awards + Malaysian sponsors (JPA/MARA/Yayasan), and the realistic **your-share
    in MYR** (not the sticker — the residual after aid).
11. **How to apply** — Common App / Coalition / own app, **EA / ED / REA / RD** and which single early
    shot to spend, essays/supplements, recommenders, application + deposit fees / waivers.
12. **Outcomes & network** — graduate outcomes, **OPT + 24-month STEM-OPT**, alumni network, careers.
13. **Unique facts & quirks** — traditions, notable alumni *in the student's field*, fun/quirky facts —
    the colour that makes it real.
14. **Why here / why hesitate** — an honest synthesis tied to the student's `priorities` / `needs`:
    2–4 reasons to choose **and** an explicit "reasons to hesitate". Inform conviction — don't sell.

### The university-mode JSON shape

Write `.tmp/<slug>/uni_<uni-slug>.json` (see `build_dossier.py`'s header for the exact shape). No
`course`; the snapshot uses institution fields, and `sections` are the 14 keys above:

```json
{
  "university": "Massachusetts Institute of Technology",
  "country": "USA", "city": "Cambridge, Massachusetts",
  "setting": "urban (Boston metro)",
  "type": "private research university",
  "size": "~4,500 undergraduates",
  "overall_rank": "QS #1 / US News ~#2",
  "application_system": "MIT's own portal (not Common App)",
  "admission_likelihood": "Reach",
  "net_cost": "~RM 0-40k/yr after aid (income-band dependent; approx)",
  "priorities": "1. Funding · 2. Hands-on · 3. Safe/nature setting",
  "sections": {
    "identity_mission": "markdown...", "who_its_for": "markdown...",
    "admissions_fit": "markdown...", "academic_structure": "markdown...",
    "majors_minors": "markdown...", "signature_experiences": "markdown...",
    "culture_vibe": "markdown...", "student_life_food": "markdown...",
    "city_belonging": "markdown...", "costs_aid": "markdown...",
    "how_to_apply": "markdown...", "outcomes_network": "markdown...",
    "unique_facts": "markdown...", "why_here": "markdown..."
  },
  "sources": [ {"title": "...", "url": "...", "authority": "Official", "as_of": "2026"} ]
}
```

Render it:
```powershell
python tools/build_dossier.py --student <slug> --input .tmp/<slug>/uni_mit.json --mode university
```
Output: `data/students/<slug>/dossiers/<uni-slug>.md`; every `master_list.csv` row for that university
flips to `Finalist` (the tool prints which, and refuses if any matched row isn't a US row). Export to PDF
exactly as below — `dossier_to_pdf.py` reads either dossier unchanged.

## Writing rules — make it skimmable (non-negotiable, both modes)

A readability review (`tools/report.md`) found the old dossiers were well-researched but **fought
the reader**: walls of bold prose, the same facts repeated 3-4×, the one make-or-break warning
buried mid-paragraph, and unexplained acronyms. The student opens a dossier to answer three
questions — *can I get in? · can I afford it? · what do I actually do?* — and must be able to
**skim** to each answer. Write to that:

- **Second person.** Write *to* the student ("**you**"), never *about* them — no student name, no
  third-person "his/her/their". It's their guide, not an internal report.
- **State the ranked priorities once, up front.** Fill the Snapshot's `priorities` field (e.g.
  `"1. Funding · 2. Hands-on · 3. Safe/nature setting"`). After that, refer to a priority by name —
  don't re-rank it every section, and never write "#1 priority" without the list being visible.
- **Say each key fact once.** Pick the section that owns a fact (funding → Costs; test-not-yet-sat →
  Application checklist / Getting in) and state it there. `why_here` is **net-new synthesis**
  (the standout hook + honest hesitations), *not* a re-read of the whole dossier — keep it short.
- **Bold budget.** Bold only genuinely key figures and actions. If half a paragraph is bold, nothing
  stands out — prefer a short lead phrase or a table over bolding every clause.
- **Tables and checklists beat prose** for anything structured. Write these sections **as Markdown**
  (the renderer styles them):
  - **Costs** — a small table (row per line item: tuition / COA / net-cost-in-MYR / aid structure).
  - **Getting in / admitted profile** — a stats table (admit rate, RD vs ED, intl, test range).
  - **Application checklist & key dates** — a checklist (`- [ ] …`) with deadlines, not a paragraph.
  - **Halal / dining** — a table (location · what's served · hours) when there are 3+ options.
  - **`why_here`** — a **key-value table matching the Snapshot**: column 1 = the topic/priority,
    column 2 = the honest read for it. One row per theme, and **fold each hesitation into its
    topic's verdict** (lead with the strength, then name the caveat with "But…/trade-off") rather
    than a separate pros/cons column — keeps the format consistent with the Snapshot/cost tables and
    lets long verdicts wrap cleanly. Still cover the real strengths *and* explicit hesitations;
    inform, don't sell. Don't use ⚠️ in cells — that glyph is reserved for the red callouts below.
- **Critical warnings are a callout, not a sentence in a wall.** For a make-or-break rule (e.g. "an
  international who doesn't request aid at application is barred from applying later"), write a
  **blockquote** so it renders as an unmissable red callout:
  ```markdown
  > ⚠️ **Must request aid at application.** If you don't file the CSS Profile with the Common App,
  > you are permanently barred from applying for aid later. This is irreversible.
  ```
  Reserve blockquotes for these — don't use them for ordinary notes. For a softer neutral aside use
  `<div class="callout-note" markdown="1"> … </div>`.
- **Collect every "confirm this yourself" task into the Application checklist** — one place, as
  checklist items — instead of scattering "confirm the 4-year English record" across five sections.
- **Acronyms are auto-glossaried — don't hand-expand every one.** `dossier_to_pdf.py` builds a
  "Key terms" block from the acronyms you actually use (via `apply_glossary.py`) and links each
  term's first use to it. So write `MAE`, `OPT`, `CSS Profile`, `MQA`, `ABET`, `BEM` normally — the
  PDF explains them. **If you use an acronym the glossary doesn't know, add it to
  `tools/apply_glossary.py`** (one plain-English line) rather than expanding it inline every time.
- **No nested parentheticals; keep numbers tight.** Never `(college town (rural Finger Lakes, NY))` —
  the Snapshot has separate `city` and `setting` fields, use them. Give one figure or a tight range
  with MYR shown (not a 2.5× spread), and don't flip between USD and MYR without a conversion.

## Assemble the dossier JSON

Write `.tmp/<slug>/dossier_<uni>.json` (see `build_dossier.py`'s header for the exact shape). Each of the
14 content sections is a Markdown string under `"sections"`. Two optional-but-recommended extras:

- **`dated_items`** — structured dates the calendar will pick up:
  ```json
  "dated_items": [
    {"date": "2027-01-15", "label": "UCAS deadline", "action": "Submit application"},
    {"date": "2026-11-01", "label": "Scholarship X deadline", "action": "Apply separately"}
  ]
  ```
- **`sources`** — required; every hard fact needs a citation with authority + `as_of`.

If a fact genuinely can't be found, write `"Not found — <why>"` in that section rather than leaving it
empty (empty sections fail the build on purpose — a half-researched dossier shouldn't pass).

## Render

```powershell
python tools/build_dossier.py --student <slug> --input .tmp/<slug>/dossier_manchester-cs.json
```
Output: `data/students/<slug>/dossiers/<uni-course-slug>.md`, and the matching `master_list.csv` row flips
to Finalist / Dossier Done. Repeat per finalist.

## Export to PDF (optional, on request)

When a student asks for their dossier(s) to read outside the tool, convert the rendered Markdown to a
clean PDF (written alongside the `.md`):
```powershell
python tools/dossier_to_pdf.py --student <slug> --dossier manchester-cs   # one dossier
python tools/dossier_to_pdf.py --student <slug> --all                     # every dossier
```
This is a delivery step, not a pipeline stage — it only reads the existing `.md` (no research, no CSV
changes). Output: `data/students/<slug>/dossiers/<uni-course-slug>.pdf` (gitignored, like the rest of
the student's data bank).

The PDF renders with **WeasyPrint** and adds three things at render time (nothing to do in the `.md`):
a **"Key terms"** glossary built from the acronyms the dossier uses, with each term's first use
**tap-linked** to it; **red callouts** for blockquote warnings; and **tickable checkboxes** for
`- [ ]` items. So follow the *Writing rules* above and the presentation comes for free.

## Edge cases & rules

- **Official sources for hard facts** — fees, requirements, visa rules, and recognition come from official
  sites, not aggregators. Stamp every source with its cycle year.
- **Capture social/forum/video links, don't scrape them** — this is load-bearing for the decision-texture
  sections (`admitted_profiles`, `student_life_culture`, `city_and_belonging`). `firecrawl_search.py`
  hard-skips IG / FB / TikTok / X (they return "Website Not Supported"); Reddit / The Student Room / YouTube
  aren't skipped but are JS-heavy and unreliable to scrape — get what you need from **search snippets** and
  record the URL + snippet as a lead for the student to follow, rather than scraping the page.
- **Recognition is a gate, not a footnote** — for regulated professions, if the degree isn't recognised by
  MQA / the professional body, say so prominently; it may demote the finalist.

## Done when

Every finalist has a complete dossier and the master list shows them as Finalist / Dossier Done. Then
proceed to **Stage 5** (`05_decide_and_apply.md`).
