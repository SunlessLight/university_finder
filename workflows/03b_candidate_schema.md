# Stage 3 — Candidate schema (row-filler reference)

> Split out of `03_discover_longlist.md` on 2026-07-30 to cut token spend: this schema is
> read in full by every `row-filler` subagent (once per university, per country pass), but
> the main session never needs it. Read `03_discover_longlist.md` for the stage's objective,
> tools, and step-by-step flow; this file is only the "what each row-filler writes" reference
> it points to from Step 3.

## The candidate schema (what each row-filler writes)

> **`specific_courses` from the Broad-Area grid is a sub-category, not a literal course title.**
> The grid's per-area cell (e.g. "Accounting & Finance (Includes Corporate Finance, Banking &
> FinTech)") is the student's course of interest *in their framing* — treat it as decided
> (`interest_discovery.decided = true` already reflects this), but search **broadly across the
> courses implied by that sub-category** (Accounting, Finance, Banking, FinTech, Corporate
> Finance, …), not for an exact title match against the label itself. A course named just
> "BSc Finance" or "BSc Banking & FinTech" both count as candidates for that student.

One fragment per university, at `.tmp/<slug>/candidates/<uni-slug>.json` — a **single** candidate
object, with honest **0-5 sub-scores** and an **`entry_margin`** judgement. **Every field below is
required and non-empty** (`REQUIRED_CANDIDATE_FIELDS` in `tools/shortlist_schema.py`, enforced by
`merge_candidates.py`); `total_cost_programme` is the one exception, where empty means *"compute it
from tuition + living × duration"*, which is the normal case.

```json
{
  "university": "University of Manchester",
  "course": "BSc Computer Science",
  "country": "UK",
  "city": "Manchester",
  "subject_rank": "QS CS #51-100",
  "overall_rank": "QS #34",
  "entry_requirements": "AAA incl. Maths",
  "student_grades": "AAA (predicted)",
  "english_req": "IELTS 6.5 (6.0)",
  "meets_english": true,
  "annual_tuition": "GBP 30000",
  "total_tuition": "GBP 90000",
  "est_living_per_year": "GBP 12000",
  "duration_years": 3,
  "currency": "GBP",
  "total_cost_programme": "",
  "scholarship_portal": "Global Futures Scholarship — apply via the university funding portal",
  "scholarship_coverage": "GBP 5,000/yr off tuition, renewable for all 3 years",
  "scholarship_competitiveness": "No statistics published",
  "scholarship_how_to": "Automatic on the UCAS application; no separate form. Decisions with the offer.",
  "funds_proof": "~GBP 12,000 living costs shown for the visa, plus first-year tuition",
  "post_study_work": "2 yrs work rights after graduating (Graduate Route)",
  "recognised_back_home": "MQA recognised; no professional body needed for pure CS",
  "application_system": "UCAS",
  "key_deadline": "2027-01-15",
  "intake": "2027 Sept",
  "course_url": "https://www.manchester.ac.uk/...",
  "source_authority": "Official page",
  "entry_margin": 0,
  "admission_likelihood": "",
  "admission_reason": "",
  "pathway_option": "INTO Manchester Foundation if below AAA",
  "course_at_a_glance": "3-yr BSc, broad first year then pick a specialism",
  "student_life": "Large city campus, strong industry-placement culture",
  "notes": "Fees confirmed on the course page for 2026/27 entry; 2027 rate not yet published.",
  "research_notes": "Fee page read 2026-07-29 ... (free length — the depth the cells can't hold)",
  "scores": {
    "course_match": 5,
    "subject_reputation": 4,
    "total_cost_fit": 2,
    "post_study_work_fit": 4,
    "scholarship_opportunity": 3,
    "experiential_fit": 3,
    "location_pref_fit": 4,
    "recognition_fit": 5
  }
}
```

**Field notes:**
- **Some JSON fields have no CSV column of their own — they are inputs, not display.** Filling them is
  still mandatory; the master list shows what they *produce*:
  - **`currency`** ⇒ `Approx total (MYR)`. **This one is a silent-failure trap:** `to_myr()` returns
    `None` on a blank or unrecognised currency, which empties the MYR total *and* takes the
    `Over budget` warning down with it — an unaffordable row then looks clean. Always set it, and use a
    code from `FX_TO_MYR` (MYR/GBP/USD/AUD/SGD/CNY/EUR/JPY/HKD).
  - **`total_cost_programme`** ⇒ also `Approx total (MYR)`. Leave it empty to let the tool compute
    `total_tuition` + `est_living_per_year` × `duration_years`; set it explicitly only when that model
    can't express the cost (e.g. a mixed-currency 2+2 — see the branch-campus note below).
  - **`meets_english`** ⇒ the `English short` warning. `true`/`false` only — and it is now **required**,
    so decide it: compare the student's test/score in `profile.english_proficiency` against the
    university's stated bar. It is a strict identity check, so the string `"No"` does **not** trigger
    the flag. The requirement itself goes in `english_req`, which *is* a column.
- Put a date in `key_deadline` as `YYYY-MM-DD` so it parses (extra text after the date is fine). Where
  the university publishes none, write the sentinel — `Rolling` or `Not published — check portal`.
- **`source_authority` is `"Official page"` at Stage 3 now**, because Stage 3 is where hard facts get
  verified (the pre-flight moved here on 2026-07-29 — Stage 4 is report-only). Leave `"Not verified"`
  **only** on a row whose facts you genuinely could not confirm on an official page, and say which fact
  in `notes` — that row can't become a Finalist until someone does. These are the only two values the
  `Info source` column takes.
- **Sentinels, not blanks, not guesses.** Every field is required, so a fact that genuinely doesn't
  exist takes its column's sentinel from `SENTINEL_VALUES` (`Not ranked`, `Rolling`,
  `Not published — check portal`, `No statistics published`, `not_published` as an `entry_margin`).
  A fact that *does* exist but you couldn't reach is not a sentinel case — name the gap in `notes`.

> **`entry_margin` means ONE thing: grades vs the published academic bar.** **+2** well above …
> **0** borderline/meets … **−2** well below. It produces the **`Grades vs entry bar`** column
> (`Well above`/`Above`/`Meets`/`Below`/`Well below`/`Not published`) and, by default,
> `Admission likelihood`. Don't fold it into the sub-scores.
>
> **Do NOT push a holistic Reach through `entry_margin` — that was a real bug (fixed 2026-07-25).**
> Agents were setting `entry_margin: -2` on selective US schools to express "unlikely to get in",
> so the grade column printed "No" for a student with A\*A\*A\*A at Duke, Vanderbilt and Georgia
> Tech — while the same student's other file read "Exceeds academic bar" at MIT. Same grades,
> contradictory answers, and a quiet breach of the desirability-vs-admissibility guardrail.
> Anything that is **not** the grade bar — holistic selection, a capped international quota,
> need-aware admission, an interview or admissions test — goes in the override instead:
> ```json
> "entry_margin": 2, "admission_likelihood": "Reach", "admission_reason": "very selective"
> ```
> which renders **`Reach (very selective)`** and answers the student's real question: *why is a
> university I qualify for still a long shot?* Keep `admission_reason` under 24 characters.
> Where a university publishes **no** academic bar at all (holistic US admission, or a profile
> you genuinely could not retrieve), set `Grades vs entry bar` to **`Not published`** — saying so
> beats inventing a comparison. There is no `fits_grades` field any more; the column is derived.

> **Write cells for a scanning student, not for a report (the 2026-07-25 readability fix).**
> The master list is read in Google Sheets, where a 500-word cell truncates or blows the row
> height up. Three rules, all enforced by **`python tools/check_master_list.py --student <slug>`**
> — run it after every sync:
> 1. **Length budgets per column** (`CELL_BUDGETS` in `shortlist_schema.py`; `Notes` 200 chars,
>    most prose 120-200). Nothing is ever silently truncated — you say it shorter.
> 2. **`notes` vs `research_notes` — two fields, two destinations.** `notes` is the ≤200-char
>    headline that lands in the CSV; **`research_notes`** is free-length and is appended to
>    `data/students/<slug>/research_notes.md` under a `## University - Course` heading. Put the
>    verification stamps, source conflicts and cost traps there. This is what makes the budget
>    survivable — depth is preserved, just not in a spreadsheet cell.
> 3. **Plain English first.** Prefer the plain phrase over the acronym outright — it is *shorter
>    and* clearer (`3 yrs post-study work` beats `OPT + 24mo STEM OPT`). The replaceable terms
>    live in `apply_glossary.PLAIN_ALTERNATIVES`, and the linter flags them with their fix.
>    **Keep** the proper nouns the student must search for on an official page — UCAS, MQA, BEM,
>    Washington Accord, CSS Profile, IELTS; `tools/build_glossary_sheet.py` generates a per-student
>    `glossary.csv` explaining exactly the terms that student's list uses, to import as a second tab.
> - `course_at_a_glance` and `student_life` are **one tight sentence each** — the shape of the
>   degree, and what living there is like. **Research them and fill them here** (they used to be
>   left for Stage 4, which is exactly how they ended up blank on 43 of one student's 44 rows).
>   One real sentence from the course page and the university's own student-life/accommodation
>   pages is enough; an invented sentence about campus culture is a fabricated fact like any other,
>   so if you truly have nothing, say what you *do* know about the degree's shape rather than
>   inventing atmosphere.

**Scoring guide (each 0-5 — these are DESIRABILITY only, never admissibility):**
- `course_match` — how well the course matches the field/goal.
- `subject_reputation` — subject-specific rank + graduate outcomes (not overall vanity rank).
- `total_cost_fit` — full-programme total (MYR) vs the student's budget (lower cost = higher).
- `post_study_work_fit` — visa/post-study-work rights vs `intent_to_migrate`.
- `scholarship_opportunity` — realistic funding this student could actually get.
- `experiential_fit` — hands-on opportunities: projects, research, community involvement, not just exams.
- `location_pref_fit` — matches stated location/lifestyle preferences.
- `recognition_fit` — recognised back home (MQA + professional body) where it matters.

> **Scoring `recognition_fit` for HOME-COUNTRY (Malaysian) rows — MQA is a floor, not a distinction.**
> Every Malaysian programme is MQA-registered, so scoring MQA as recognition makes *every* domestic row
> max out and Malaysia sweeps the list for a reason that means nothing. Score the **professional ladder**
> the degree actually sits on, **per programme, not per university**:
>
> | Degree title says | Accreditor | Register | Accord |
> |---|---|---|---|
> | "Bachelor of **Engineering**" | **EAC** | **BEM** Professional Engineer (**Ir.**) | **Washington** |
> | "Bachelor of Engineering **Technology**" | **ETAC** | **MBOT** Professional Technologist (**Ts.**) | **Sydney** |
> | "Bachelor of Applied **Science**" | — | none | — |
>
> The two ladders are **not interchangeable**, and for a regulated profession this is a gate, not a
> preference. Check `profile.recognition_targets`: if it names **BEM / Washington Accord**, an ETAC row
> **fails the student's own gate even when the course title matches perfectly** — that's a real negative
> finding worth keeping on the list, not a row to quietly score well.
>
> **Tell-tales when the page doesn't name the accreditor** (common — programme pages often omit it):
> - The **degree title** is the strongest signal: "Engineering **Technology**" ⇒ ETAC.
> - The **PLO wording** gives it away: Washington Accord programmes say "**complex** engineering problems"
>   (WK1-WK7); Sydney/ETAC ones say "**broadly-defined** Engineering Technology problems" (SK1-SK4).
> - Registers to check: `eac.org.my` and `etac.org.my` (accredited-programme lists), `bem.org.my`, MQR.
> - If you can only **infer** the ladder, say so in `notes` and flag it for Stage 4 — never let an inferred
>   accreditation reach Shortlist unverified.
>
> **The EAC register is Cloudflare-protected — plan around it (learned 2026-07-16).** The *index* page
> (`eac.org.my/v2/list-of-accredited-engineering-programme-malaysia/`) scrapes fine with Firecrawl and gives
> you the list of accredited **institutions**, each linking to a per-university PDF of its accredited
> **programmes**. Those **PDFs 403 to both WebFetch and curl** (Cloudflare "Just a moment..." — a browser UA
> and Referer do not help), so you cannot confirm a *specific programme* from the register for free. Work
> around it in this order, which is free and was sufficient for all 6 Malaysian rows:
> 1. **The university's own programme page** — often names the accreditor outright ("Professional or
>    Statutory Body of Accreditation: ... Engineering Accreditation Council") and, better, exposes the
>    **PLO wording** tell-tale above. UTM's page did both.
> 2. **The university's FAQ / accreditation page** — UM's states "Board of Engineers Malaysia" + "Washington
>    Accord" explicitly.
> 3. **MQR** (`www2.mqa.gov.my/mqr`) — gives the professional body **and the accreditation window**; check the
>    end date, it may be expired on its face (UniMAP's read 2019-2024) and needs a renewal check at Stage 4.
> Note the institution list is **necessary but not sufficient**: a university on it has *some* accredited
> programme, not necessarily the one you want. Absence, though, is strong evidence — University of Cyberjaya
> is missing from it, matching its ETAC/Sydney-Accord status.

> **A "local" branch-campus row may be a 2+2 in disguise — check before costing it (learned 2026-07-16).**
> Monash Malaysia's Bachelor of Biomedical Engineering is *"a four-year degree where you'll study your first
> two years in Malaysia and your final years at our Clayton campus in Melbourne"* — the transfer is
> **mandatory**. That inverts three things at once, so catch it at discovery, not Stage 4:
> - **Cost** is mixed-currency and roughly 4x the local rate. The `total_tuition` + `living` × `duration`
>   model cannot express it — compute the total yourself and set **`total_cost_programme` explicitly** (in
>   MYR, with `currency: "MYR"`); the tool prefers an explicit value over the computed one.
> - **`post_study_work_fit` flips from floor to high** — the student graduates *in* the destination country
>   and gets its post-study visa (485), so a "Malaysia" row can carry a full migration pathway.
> - **The comparison changes**: score it against the parent university's home row, not the domestic rows.
> Also check **scholarship eligibility by qualification** — Monash Malaysia's RM8,000/yr waiver is UEC-only,
> so an A-Level student gets nothing from it.
> Conversely, don't trust an aggregator that a branch campus offers the field at all: Nottingham Malaysia has
> only Biomedical **Sciences** (BSc), and MMU Cyberjaya has no biomedical programme despite aggregator claims.

> **Home-country rows: price them at the LOCAL rate, not the international one.** Aggregators quote the
> international fee by default (eduadvisor listed UM Biomedical at RM111,400). A domestic student pays the
> subsidised local rate — often 4-10x less at a public university — which is usually what decides whether the
> row clears the budget. The local route also has its **own English requirement**: Malaysian publics take
> **MUET** (via UPU), not IELTS, so a student with no formal test still has an action item, just a different one.
>
> Watch the mirror-image trap too: an **RINA / IMarEST / MARDEP** stamp is genuine and worth noting, but it
> is *not* a substitute for the BEM route if that's what the student asked for.

> **Weights are per-student and live in `data/students/<slug>/weights.json`** — never in
> `tools/shortlist_schema.py`, which is shared source that concurrent sessions would fight over.
> Derive them from the student's `preferences.priorities` with the **`scoring-weights` skill** before
> syncing; `sync_shortlist.py` refuses to run without a valid file. Because no student state is shared,
> two students can be discovered and synced **in parallel**. **The four scholarship columns are filled
> here, not at Stage 4** — they were the single biggest source of blank cells, and for a
> `scholarship_required` student they are the reason the list exists.
