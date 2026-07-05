# Workflow: Stage 5a — University Dossier (deep research per finalist)

## Objective

For each **finalist** (the 3-5 strongest Shortlist rows), produce a deep, standardized **14-section
dossier** so the student can compare like-for-like and make a confident decision. This is the most
research-intensive stage — do it only for finalists, A-tier and best-fit first.

## Tools used

1. *(agent research)* gather the facts for the 14 sections from **official sources** (course page, UCAS/
   Common App, the country's visa site, MQA), capturing social/forum URLs without scraping them.
2. *(agent step)* assemble `.tmp/<slug>/dossier_<uni>.json`.
3. `build_dossier.py --student <slug> --input .tmp/<slug>/dossier_<uni>.json` — renders the dossier and
   flips that row to `List status = Finalist`, `Dossier status = Done`.

## The 14 sections (the tool enforces all 12 content sections — empty = build fails)

1. **Snapshot** *(auto-rendered from the JSON's top-level fields)* — uni · course · country/city · overall
   rank · subject rank · application system · admission likelihood.
2. **Course details & structure** — modules, duration, intake, placement/sandwich/co-op, flexibility to
   change major (a real UK vs US difference).
3. **Entry requirements & this student's fit** — academic + English, the grade margin → Reach/Match/Safety,
   and the **pathway/foundation route** if direct entry is short.
4. **Costs (full)** — tuition (per year + full programme), living, application fees, deposit, and the
   **total cost of attendance in MYR**.
5. **Scholarships & financial aid** — university + government/external + **Malaysian sponsors (JPA, MARA,
   Yayasan, PTPTN)**, each with eligibility.
6. **Visa & immigration** — financial-proof requirement, visa + health-surcharge cost, work-during-study
   hours, and **post-study work rights** (UK Graduate Route / AUS 485 / US OPT–STEM OPT).
7. **Recognition back home** — **MQA recognition + the relevant Malaysian professional body**; can the
   student practise in Malaysia? (Material only for regulated professions — say "n/a" otherwise.)
8. **Cost of living & accommodation** — monthly estimate, on/off campus.
9. **Employability & outcomes** — graduate employment rate / salary data, internships, alumni network.
10. **Environment, community & student life** — incl. Malaysian/Muslim community, halal, prayer facilities
    *if the student flagged these in `needs`*.
11. **Student sentiment** — Reddit / The Student Room / forums / YouTube; capture snippets + links
    (don't scrape social domains).
12. **How to apply — step by step** — country-specific (UCAS / Common App / direct portal).
13. **Key dates & deadlines** — application, scholarship, admissions-test dates.
14. **Sources** — each with **authority (Official/Aggregator) + as-of cycle year**.

## Assemble the dossier JSON

Write `.tmp/<slug>/dossier_<uni>.json` (see `build_dossier.py`'s header for the exact shape). Each of the
12 content sections is a Markdown string under `"sections"`. Two optional-but-recommended extras:

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

## Edge cases & rules

- **Official sources for hard facts** — fees, requirements, visa rules, and recognition come from official
  sites, not aggregators. Stamp every source with its cycle year.
- **Don't scrape social/forums** — Firecrawl returns "Website Not Supported"; capture the URL + snippet for
  section 11 instead.
- **Recognition is a gate, not a footnote** — for regulated professions, if the degree isn't recognised by
  MQA / the professional body, say so prominently; it may demote the finalist.

## Done when

Every finalist has a complete dossier and the master list shows them as Finalist / Dossier Done. Then
proceed to **Stage 5b** (`06_decide_and_apply.md`).
