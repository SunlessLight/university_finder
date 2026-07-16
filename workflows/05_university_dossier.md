# Workflow: Stage 5a — University Dossier (deep research per finalist)

## Objective

For each **finalist** (the 3-5 strongest Shortlist rows), produce a deep, standardized **16-section
dossier** (Snapshot + 14 content sections + Sources) that answers three decision questions — **can I get
in? · will I belong & thrive? · what will it take to apply?** — so the student can *decide*, not just
compare. Lead with texture that determines whether they apply; keep the hard-fact sections as guardrails.
This is the most research-intensive stage — do it only for finalists, A-tier and best-fit first.

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

1. **Snapshot** *(auto-rendered from the JSON's top-level fields)* — uni · course · country/city · overall
   rank · subject rank · application system · admission likelihood.
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
    read `data/students/toru/student_life_research.md` first**: 30 rows of this was already researched at
    Stage 4 under the old schema and migrated there. Don't pay for it twice.
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
proceed to **Stage 5b** (`06_decide_and_apply.md`).
