# Workflow: Application Prep — per-region "how to apply" guide (grouped by application system)

## Objective

Turn a student's **Shortlist/Finalist** into an **action-only apply guide** for one region at a time:
*exactly what to prepare and do to get every application in*, with the shared work grouped so it's done
once. It answers one question — **"what do I need to apply?"** — and deliberately skips the "is this uni
right for me?" texture (that's the dossier's job, `04_university_dossier.md`).

Use it when a student has decided to **apply and compare offers first, research fit later** — i.e. they
don't want more dossiers, they want a checklist + deadlines + financial-aid mechanics they can act on.
Produce it **one region at a time** (US, then UK, Australia, Singapore, China) — each region is a lot of
official verification.

This is a decision-support / how-to-apply deliverable, a sibling of Stage 5's `05_decide_and_apply.md`
application-strategy section, pulled out and made repeatable per region. Like `build_calendar.py`, it is
**read-only against `master_list.csv`** — it never changes `List status` or flips rows.

## Tools used

1. *(agent research)* verify the apply mechanics for each Shortlist/Finalist uni in the region from
   **official** admissions + financial-aid pages (see rules below).
2. *(agent step)* assemble `.tmp/<slug>/apply_prep_<region>.json` (shape below / in the tool header).
3. `build_application_prep.py --student <slug> --input .tmp/<slug>/apply_prep_<region>.json` — renders
   `data/students/<slug>/application_prep/<region>.md`, grouped by application system. **No CSV writes.**
4. `apply_prep_to_pdf.py --student <slug> --region <region>` — exports a clean student-facing PDF
   beside the `.md` (WeasyPrint; on Windows needs MSYS2 GTK — see the tool header). Also **read-only**.

### Voice — use the `application-guide` skill
Invoke the **`application-guide`** skill when authoring/regenerating a guide. It sets the admissions-
guide persona and the writing rules (checklists over prose runs, use-jargon-freely-the-glossary-defines-it,
warm second person, honesty about Reach odds). The persona is the wrapper; the readability comes from
these rules + the renderer's auto-formatting below.

### What the renderer auto-adds (do NOT hand-write these)
`build_application_prep.py` post-processes every guide so you only write the substance:
- a constant **"How to use this guide"** intro, an auto-generated **Contents** list, and a **Key terms**
  glossary listing only the jargon the guide actually uses (from `tools/apply_glossary.py`);
- **jargon auto-links** — the first mention per section of each glossary term links to its definition;
- **numbered scaffolding** — universities are numbered **1, 2, 3… continuously across the whole region**
  (not restarted per application system), and each university's subsections are lettered **a, b, c…**
  (`a. Deadlines`, `b. Tests`, `c. Essays`, `d. Application fee`, `e. Financial aid`, `f. What to
  gather / do`) as bold sub-headings, with the content indented beneath each;
- **checklists** — the `shared_checklist`, per-university `application_checklist`, and
  `consolidated_checklist` render as tickable `- [ ]` items; long ones (≥7 items — the "Filed once" and
  region-wide "Gather once" lists) auto-flow into **two columns** in the PDF.

**Write checklist fields as JSON arrays (one action per item).** Legacy `·`-joined strings are still
split automatically, but arrays are the convention. **Write the info fields (`tests`, `essays`, `fees`)
as short Markdown sub-bullets, not paragraphs** — one point per `- ` line; the renderer indents them
under the lettered section title. **Write `financial_aid` as an object** with the fixed keys `model`,
`cost`, `covers`, `your_share`, `forms`, `documents`, `dates` (any you can't fill are skipped) — the
renderer lays them out as labelled sub-rows so aid reads consistently across universities. Any aid key
may itself be written as `- ` sub-bullets; they nest under the label. A legacy `financial_aid` string
still renders (as prose) for back-compat.

> **The rule that earned `cost` + `your_share` (2026-07-16).** The R2 fixed-label object made the US
> guide *tidier and thinner*: every university said "meets 100% of need" and not one said what the
> 100% was **of**. **A fixed label must never license a terser answer.** `cost` states the sticker
> cost of attendance (USD **+ approximate MYR** + line items) so "100%" has a denominator;
> `your_share` states the residual aid does *not* pay. Both are load-bearing for a scholarship-required
> student — the research turned up that Stanford expects ~USD 5,000/yr from the student while Princeton
> abolished its contribution entirely, a difference "100% of need" completely hides. **If you use a term not in the glossary, add it to `GLOSSARY` in
`tools/apply_glossary.py`** (term → one-line definition + aliases) so it gets defined and linked everywhere.

### Which scraper (spend credits where they matter)
- **Claude WebSearch / WebFetch (free) — the default.** Deadlines, test policy, aid forms/dates, fees and
  supplement counts live on official admissions/financial-aid pages that fetch cleanly. All of the US
  research used free search/fetch only.
- **Firecrawl (paid, gated) — only if an official page hard-blocks a clean fetch** (a fee PDF, a
  login-walled aid page). **Ask before spending credits** (guardrail #6 in `00_overview.md`).

## What to capture per university (the apply mechanics)

For each Shortlist/Finalist uni in the region, from official sources:
- **Application system** — Common App / UCAS / the uni's own portal / direct — so the tool can group it.
- **Deadlines** — application (incl. early type: EA / ED / SCEA / REA / RD) **and** the financial-aid
  deadline (they often differ).
- **Tests** — SAT/ACT (required / optional?) + the sit-by date; English test (IELTS/TOEFL) **or the
  waiver** (English-medium A-Levels waive it for the US + 3 UK unis, but NOT Singapore / China /
  Australia).
- **Essays** — the shared essay (Common App / UCAS personal statement) + this uni's supplements/count.
- **Fees** — application fee + international **fee-waiver** eligibility.
- **Financial aid** — capture it into the object's fixed keys: **`model`** (need-blind vs need-aware for
  internationals), **`cost`** (the official **cost of attendance** — not tuition alone — in USD **and
  approximate MYR**, with the line-item split; this is the denominator "100% of need" is measured
  against), **`covers`** (what the aid pays for *against that number*, for this student's income band),
  **`your_share`** (the residual aid does **not** pay: the **student contribution** / summer-work or
  term-time-work expectation, flights, visa + SEVIS, health insurance, personal spending),
  **`forms`** (CSS Profile / IDOC / school-specific like PFAA / ISAFA / the with-application rule),
  **`documents`** (parent income/tax, translated), and **`dates`**. This is the load-bearing part for a
  scholarship-required student — get it exact and official. **Never write a bare "100%"**: if you can't
  state the cost it's 100% of, you haven't finished the research.
- **Portal** URLs (application + aid).

Then write the region-level **overview** (the cross-cutting strategy): early-application constraints,
the test lead-time gate, aid-model tiers, the fee budget, and an aid-forms cheat-sheet. And a
**consolidated "gather once"** list + **dated_items** for the deadline calendar.

## Assemble the JSON

Write `.tmp/<slug>/apply_prep_<region>.json` (exact shape in `build_application_prep.py`'s header):

```json
{
  "student_slug": "toru", "region": "us", "region_title": "United States",
  "overview": "markdown — the cross-cutting apply strategy",
  "systems": [
    {"system": "Common App", "universities": ["Princeton University", "..."],
     "shared_checklist": ["one action per item", "filed once across these schools"]},
    {"system": "MIT application (own portal, NOT Common App)", "universities": ["...(MIT)"],
     "shared_checklist": ["..."]}
  ],
  "universities": [
    {"name": "Princeton University", "system": "Common App", "admission_likelihood": "Reach",
     "deadlines": {"application": "...", "aid": "..."},
     "tests": "- sub-bullet\n- sub-bullet", "essays": "- sub-bullet\n- sub-bullet", "fees": "- sub-bullet",
     "financial_aid": {"model": "need-blind — asking can't hurt you",
       "cost": "USD 94,624/yr all-in (~RM 386,000/yr) — tuition 68,140 · housing 13,010 · food 9,110",
       "covers": "all of it for your band — zero family contribution, grants, no loans",
       "your_share": "- nothing from you — the student contribution was abolished in 2022\n- Still yours: visa + SEVIS fees",
       "forms": "PFAA + CSS Profile", "documents": "parent income/tax docs", "dates": "file with the app"},
     "application_checklist": ["Common App + Princeton supplement", "counselor + 2 teacher recs",
       "PFAA + CSS Profile + parent tax docs"], "portal": "https://..."}
  ],
  "consolidated_checklist": ["gather-once action per item", "across the region"],
  "dated_items": [{"date": "2027-01-01", "label": "...", "action": "..."}],
  "sources": [{"title": "...", "url": "...", "authority": "Official", "as_of": "2027"}]
}
```

**Validation (fails the build):** `region`, non-empty `overview`, ≥1 `systems`, and every university with
non-empty `deadlines` + `application_checklist` + `financial_aid` (the aid object needs ≥1 non-empty key),
plus ≥1 `sources`. A name in a system's `universities` list is matched to the full entry in `universities`
by exact `name`.

## Render

```powershell
python tools/build_application_prep.py --student toru --input .tmp/toru/apply_prep_us.json
python tools/apply_prep_to_pdf.py --student toru --region us
```
Output: `data/students/<slug>/application_prep/<region>.md` (+ `.pdf`). Repeat per region. The `.md` is
regenerable from the `.tmp/<slug>/apply_prep_<region>.json` — keep that JSON so a re-render costs no
research. `checklist` fields as arrays are back-compatible: old string guides re-render into checklists.

## Edge cases & rules

- **Official sources for hard facts** — deadlines, fees, aid forms/dates, test policy come from official
  admissions/financial-aid pages, not aggregators. Stamp every source with authority + as-of cycle year.
- **Does NOT change `List status`.** This is a how-to-apply deliverable, not a pipeline cut. It reads the
  Shortlist/Finalist rows; it never promotes, demotes, or flips them (unlike `build_dossier.py`).
- **Cycle-timing caveat.** For a Fall-20XX intake you're often researching the *previous* year's cycle
  before the new one opens (e.g. Common App supplement prompts publish ~1 Aug). State the figure with a
  "confirm when the 20XX-YY cycle opens" flag rather than guessing.
- **Overlap with `05_decide_and_apply.md`.** Stage 5's `recommendation.md` also groups an apply strategy
  by system; this workflow is the standalone, per-region, dossier-free version. Use 5b when the student
  wants a ranked *decision*; use this when they've decided to apply broadly and just need the mechanics.
- **Credits gated / PDPA** — free search by default (ask before Firecrawl); output lives in the
  gitignored `data/students/<slug>/`, never committed.

## Done when

Every Shortlist/Finalist uni in the region appears in `application_prep/<region>.md`, correctly grouped by
application system, each with deadlines + tests + essays + fees + financial-aid forms/docs/dates +
checklist + portal; the overview carries the cross-cutting strategy; the gather-once list and the
chronological deadline calendar render; the guide has the auto-added intro + Contents + Key terms +
linked jargon + tickable checklists; the **PDF** exports cleanly (clickable Contents/glossary jumps);
every hard fact has an official source stamped with its cycle year; and `master_list.csv` is unchanged.
Update `status.md` with the region done and the next region to run. Repeat for the remaining regions.
