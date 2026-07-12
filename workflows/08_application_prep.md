# Workflow: Application Prep — per-region "how to apply" guide (grouped by application system)

## Objective

Turn a student's **Shortlist/Finalist** into an **action-only apply guide** for one region at a time:
*exactly what to prepare and do to get every application in*, with the shared work grouped so it's done
once. It answers one question — **"what do I need to apply?"** — and deliberately skips the "is this uni
right for me?" texture (that's the dossier's job, `05_university_dossier.md`).

Use it when a student has decided to **apply and compare offers first, research fit later** — i.e. they
don't want more dossiers, they want a checklist + deadlines + financial-aid mechanics they can act on.
Produce it **one region at a time** (US, then UK, Australia, Singapore, China) — each region is a lot of
official verification.

This is a decision-support / how-to-apply deliverable, a sibling of Stage-5b's `06_decide_and_apply.md`
application-strategy section, pulled out and made repeatable per region. Like `build_calendar.py`, it is
**read-only against `master_list.csv`** — it never changes `List status` or flips rows.

## Tools used

1. *(agent research)* verify the apply mechanics for each Shortlist/Finalist uni in the region from
   **official** admissions + financial-aid pages (see rules below).
2. *(agent step)* assemble `.tmp/<slug>/apply_prep_<region>.json` (shape below / in the tool header).
3. `build_application_prep.py --student <slug> --input .tmp/<slug>/apply_prep_<region>.json` — renders
   `data/students/<slug>/application_prep/<region>.md`, grouped by application system. **No CSV writes.**

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
- **Financial aid** — the need model (need-blind vs need-aware for internationals), what it covers, the
  **forms** (CSS Profile / IDOC / school-specific like PFAA / ISAFA / the with-application rule), the
  **documents** (parent income/tax, translated), and the **dates**. This is the load-bearing part for a
  scholarship-required student — get it exact and official.
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
     "shared_checklist": "markdown — filed once across these schools"},
    {"system": "MIT application (own portal, NOT Common App)", "universities": ["...(MIT)"],
     "shared_checklist": "markdown"}
  ],
  "universities": [
    {"name": "Princeton University", "system": "Common App", "admission_likelihood": "Reach",
     "deadlines": {"application": "...", "aid": "..."},
     "tests": "md", "essays": "md", "fees": "md",
     "financial_aid": "md — model, forms, docs, dates",
     "application_checklist": "md", "portal": "https://..."}
  ],
  "consolidated_checklist": "markdown — gather once across the region",
  "dated_items": [{"date": "2027-01-01", "label": "...", "action": "..."}],
  "sources": [{"title": "...", "url": "...", "authority": "Official", "as_of": "2027"}]
}
```

**Validation (fails the build):** `region`, non-empty `overview`, ≥1 `systems`, and every university with
non-empty `deadlines` + `application_checklist` + `financial_aid`, plus ≥1 `sources`. A name in a
system's `universities` list is matched to the full entry in `universities` by exact `name`.

## Render

```powershell
python tools/build_application_prep.py --student toru --input .tmp/toru/apply_prep_us.json
```
Output: `data/students/<slug>/application_prep/<region>.md`. Repeat per region.

## Edge cases & rules

- **Official sources for hard facts** — deadlines, fees, aid forms/dates, test policy come from official
  admissions/financial-aid pages, not aggregators. Stamp every source with authority + as-of cycle year.
- **Does NOT change `List status`.** This is a how-to-apply deliverable, not a pipeline cut. It reads the
  Shortlist/Finalist rows; it never promotes, demotes, or flips them (unlike `build_dossier.py`).
- **Cycle-timing caveat.** For a Fall-20XX intake you're often researching the *previous* year's cycle
  before the new one opens (e.g. Common App supplement prompts publish ~1 Aug). State the figure with a
  "confirm when the 20XX-YY cycle opens" flag rather than guessing.
- **Overlap with `06_decide_and_apply.md`.** Stage 5b's `recommendation.md` also groups an apply strategy
  by system; this workflow is the standalone, per-region, dossier-free version. Use 5b when the student
  wants a ranked *decision*; use this when they've decided to apply broadly and just need the mechanics.
- **Credits gated / PDPA** — free search by default (ask before Firecrawl); output lives in the
  gitignored `data/students/<slug>/`, never committed.

## Done when

Every Shortlist/Finalist uni in the region appears in `application_prep/<region>.md`, correctly grouped by
application system, each with deadlines + tests + essays + fees + financial-aid forms/docs/dates +
checklist + portal; the overview carries the cross-cutting strategy; the gather-once list and the
chronological deadline calendar render; every hard fact has an official source stamped with its cycle
year; and `master_list.csv` is unchanged. Update `status.md` with the region done and the next region to
run. Repeat for the remaining regions.
