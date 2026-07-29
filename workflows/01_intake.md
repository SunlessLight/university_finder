# Workflow: Stage 1 — Intake (Google Form CSV → student data banks)

## Objective

Capture, in one pass, **who the student is** (grades, English, budget, recognition needs) and **what
they want** (destinations, field/course, priorities) — so later stages can judge fit, cost, and
admissibility accurately. Output is `data/students/<slug>/profile.json` + `preferences.json`.

**Every student comes in through the Google Form.** They fill it, you export the responses as CSV,
this workflow batch-builds one `data/students/<slug>/` per respondent, then you finalize a few
judgment-heavy fields and hand each student off to **Stage 3** (discover longlist). There is no
conversational intake path — a student you meet in person still fills the form (or you fill it for
them) so the data bank is built the same way every time.

> **Stage 1 and Stage 2 were merged on 2026-07-25.** The form asks who-you-are and what-you-want in
> one sitting, so the old `01_student_intake.md` / `02_aspirations_intake.md` conversational SOPs were
> deleted. Stages 3-5 keep their file numbers — **there is no Stage 2**.

## The Google Form (build once)

Create **one form**, turn **"Collect email addresses" ON** (Settings → Responses), and add the
questions below. Question **wording** maps to CSV column headers; the tool matches columns by a
distinctive **substring** (see `QUESTION_MAP` in `tools/ingest_form_csv.py`), so light rewording is
fine — but keep the substring in bold intact.

**Section 0 — Consent & identity (required)**
- **"Collect email addresses" turned ON.** 
- **I consent** 'Cool for me to store your answers and use them to research unis for you 👍?'. — required checkbox.
  *(**What the gate actually does**, checked against a real export: a Forms checkbox exports its own
  label text, so a ticked box lands a non-empty cell like `Cool for me to store your answers…` —
  `_yes()` can't read that as yes or no and returns `None`, and the row passes on the cell simply
  being **non-empty**. So a ticked checkbox needs **no** `--assume-consent`. What still skips a row:
  an **empty** consent cell (box not ticked) unless you pass `--assume-consent`, and an answer whose
  text starts with "n" — the explicit-No case, which no flag overrides.)*

**Section 1 — About you → `profile.json`**
- **Name**; **Your age**; **Gender**; **Nationality**; **Race/ethnicity**; where you **live in now**.
  - **Race/ethnicity → `profile.ethnicity`** (PDPA-sensitive). Captured because it drives
    **scholarship eligibility** in Malaysia (e.g. Bumiputra-only vs open funds) — the agent uses it as a
    research signal in Stage 3/4. It is **never** a desirability-score input.
  - **The respondent's email is stored**, not just used to dedupe: the tool writes it into
    `profile.notes` as `Contact: <email>` (PDPA-sensitive, same class as the rest of the data bank —
    it stays under gitignored `data/students/`).
  - **`home_country` always stays "Malaysia".** The tool never overwrites it. *(A legacy form asked
    "where do you want to **live and work after** graduating"; the current form dropped it, and
    `intent_to_migrate` comes from the "work abroad" question in Section 2 instead. If you ever
    re-add it, it is a post-study **aspiration** → `notes` + `intent_to_migrate`, never `home_country`.)*

**Section 2 — Your studies, money & recognition → `profile.json`**
- What are you **studying now** (A-Level / STPM / UEC / IB / Foundation / Matriculation / Diploma /
  Other); **which college**/school; **when do you graduate** / get results — a **month + year
  dropdown** (e.g. "September 2027"), not free text. The tool normalises it to `YYYY-MM`
  (`_normalize_month_year`), which is what retired the by-hand date-normalisation finalize step and
  the `9/1/2027` ambiguity. An answer it can't read as a month+year is kept verbatim, never guessed.
- **Subjects & grades — four structured dropdown pairs.** The form asks each subject as *"List your Nth
  subject"* + *"Select the grade you are **confident of getting**"* (subjects 1-3 required, subject 4
  optional → *"Select None if only 3 subjects"*). The tool builds `profile.subjects[]` **deterministically**
  from these pairs (no free-text parsing) and, because the grade question asks what the student is
  *confident of getting*, stamps **`grade_status = "expected"`** — a self-prediction, weaker than official
  predicted grades and than actual results. See the provisional-grades edge case below.
- **English proficiency — a capability snapshot only.** Ask just: **which English test** have you taken
  (IELTS / TOEFL / MUET / PTE / Duolingo / **None** / Other) and your **English score** (blank if none).
  *Do NOT ask "when will you take it".* Each university sets its own English bar; the required test +
  score per uni is filled during research (the `English req` column, plus the `meets_english` candidate
  field behind the `English short` warning), and the definitive "tests you must sit" list is produced at
  the apply stage — not here.
- **Total budget** for the whole degree — a **four-option dropdown**, not free text:
  **`Under RM 500,000`** / **`RM 500,000 - 1,000,000`** / **`Above RM 1,000,000`** /
  **`Not sure - no fixed budget`**. `BUDGET_BAND_NORMALIZE` maps them to a numeric ceiling
  (500000 / 1000000 / **null** / null — "Above RM 1,000,000" states a *floor*, so it carries no
  ceiling, exactly like "Not sure"); the **verbatim label** goes to `financial.notes` and the
  **number** to `financial.total_budget` + `preferences.total_budget_ceiling`. A label string must
  never reach `total_budget_ceiling` — downstream cost checks expect a number or null. "Not sure" is
  a real answer meaning "research everything, I'll decide", and only powers the absence of the
  "Over budget" flag. **Ask for the total, never per-year** — Stage 4 compares whole-programme cost,
  and a 3-year UK degree against a 4-year US one is not comparable per year. There is no per-year
  question, so `financial.budget_per_year` / `preferences.budget_ceiling_per_year` stay null.
- **Is scholarship a must?** — Yes/No. A clean gate: Yes sets both `preferences.scholarship_required` and
  `financial.scholarship_dependent` true. **What scholarships are you planning to apply for?** — free text
  → `preferences.scholarship_interests`, a *research hint* (which scholarships to dig into; "don't know /
  all options" is a fine answer meaning research broadly). It never filters or scores. *(Legacy forms with
  a "how will you pay" / merged "how will you fund" question still work — the tool falls back automatically
  when the "is scholarship a must?" column is absent.)*
- Are you aiming at a **regulated profession** — checkboxes (Medicine / Engineering / Law / Accounting
  / Pharmacy / Dentistry / Architecture / Nursing / None). *(Should match the intended career — see the
  Engineering-vs-CS edge case below.)*
- **"Any personal needs?"** (optional; PDPA-sensitive) — the "support & belonging" checkbox set, broad
  and faith/culture-neutral: **Halal food** / **Prayer facilities** / **Malaysian community nearby** /
  **Stay close to family** / **Personal safety** / **Climate / weather** — plus **Other**. *(The live
  form's current header is still the plain "Any personal needs?" — "support & belonging" is an optional
  future rewording, not what's live today; `QUESTION_MAP`'s `"personal needs"` substring matches the
  current wording, `"belonging"` is there ready for if it's reworded later.)*

**Section 3 — What you want → `preferences.json`**
- **Which countries** would you consider — checkboxes (UK / Australia / USA / **Singapore** /
  **Malaysia** / China / Japan / Hong Kong — **8** supported destinations; `COUNTRY_NORMALIZE` in
  `tools/ingest_form_csv.py` is the source of truth for the exact tokens). **Singapore and Malaysia
  are separate** as of 2026-07-29 — they were fused into one `Singapore/Malaysia` token, which gave a
  student who ticked only Malaysia a longlist half-full of Singapore rows. Picking several is fine
  (research-first breadth). *(**Not currently on the live form**: an optional "which country matters
  most?" follow-up was proposed but never added — if it's added later, it needs a new `QUESTION_MAP`
  entry so the agent can record it in `preferences.notes` and research goes deepest where it counts.)*
- **Broad Area of Study + a course grid.** One **Broad Area of Study** dropdown (Arts, Humanities &
  Design / Media, Communication & Social Sciences / Business, Finance & Management / Computer Science, IT
  & Data / Engineering & Built Environment / Pure & Applied Sciences / Health & Medical Sciences /
  Education & Teaching) → `preferences.fields_of_interest`. A **grid** of those same eight areas as columns
  captures a **sub-category within the chosen area** — not a literal course title — e.g. Business,
  Finance & Management = *"Accounting & Finance (Includes Corporate Finance, Banking & FinTech)"* →
  `preferences.specific_courses` (the tool collects the one non-empty grid cell). This sub-category
  **is** the course the student wants, in their framing, so it still sets
  `interest_discovery.decided = true` — but Stage 3 discovery must search broadly across the courses
  implied by that sub-category rather than literal-matching the label (see
  `workflows/03_discover_longlist.md`, "Extract candidates").
- **When do you want to start** — a **year + season** (e.g. "Sept 2027") **or** *"Flexible / show me all
  intakes"*. Intake only selects the application *cycle* to research — it never filters or scores, so
  "Flexible" is a perfectly good answer (stored as `Flexible`). *(No separate "degree level" question →
  the agent sets `degree_level` at finalize.)*
- **Rank your priorities** — **eight per-category sliders**, now a **1-8 scale** (1 = least important,
  8 = most), one each for: **Cost / Scholarship / University Ranking / Course Ranking / Employability /
  Recognition back home / Location / Hands-On Experience**. The tool detects them by the shared *"rank
  your priorities"* marker + the bracketed category, then orders the categories by slider value (highest
  first, ties broken by the form's column order) into `preferences.priorities`. This gives a full 8-way
  ranking including **Course Ranking** (`course_quality` → `course_match`). The ordering logic is
  scale-agnostic, so the 1-7→1-8 change is transparent — but `ranking_importance` now carries a **1-8**
  value; the `scoring-weights` skill should read it on that scale. *(Legacy forms with **#1/#2/#3
  priority** dropdowns still work — the tool falls back automatically when no sliders are present.)*
- **`ranking_importance`** steers the `subject_reputation` sub-score (subject-specific standing +
  graduate outcomes, not overall vanity rank). If the form has a dedicated *"how much does your subject's
  strength matter"* 1-5 question the tool uses it; otherwise it reads the **[University Ranking]** slider
  value (**1-8** — the current slider scale; make sure the `scoring-weights` skill reads it on that scale).
- Do you want to **work abroad** after graduating — Yes / No / Unsure. → `intent_to_migrate` (and the
  raw answer into `post_study_work_importance`).
- Any **deal-breaker**s (optional); **location preference**s (optional checkboxes).
- **Preferred universities** — ⚠️ **not currently on the live form.** This question was proposed but
  never added to the actual Google Form (confirmed against a real export — no such column exists), so
  there is no `QUESTION_MAP` entry either. If it's added later, wire up a `QUESTION_MAP` entry (e.g.
  `("preferred universit", "preferred_universities")`) and land the answer in `preferences.notes` — a
  student naming unis they already care about should never be silently ignored. Until then, there's
  nothing to read out of the CSV.

## How to run

1. Export the form responses (Responses → ⋮ → *Download responses (.csv)*) and drop the file in
   **`data/form/`** (gitignored — it's PII). Google names the export after the form itself (e.g.
   `Form Response.csv`), not `responses.csv` — the tool takes whatever path you pass, so either rename
   it to `data/form/responses.csv` to match the commands below verbatim, or just point the commands at
   your actual filename.
2. Preview first, then run for real (swap in your actual filename):
   ```powershell
   python tools/ingest_form_csv.py data/form/responses.csv --dry-run
   python tools/ingest_form_csv.py data/form/responses.csv
   ```
   The tool creates `data/students/<slug>/{profile.json,preferences.json,reports/}` per consenting
   respondent, copies budget/scholarship into **both** files, and prints a per-student
   **"Needs agent review"** list. Add `--force` only to intentionally overwrite an existing folder.
   - `--assume-consent` — **internal-only escape hatch.** If the form has no consent question (e.g. a
     friends-only test intake where the formal checkbox was dropped as too heavy), this treats a
     blank/absent consent as consent given so the row isn't skipped. It does **not** relax an explicit
     **No**, and it never writes a fabricated consent value into the CSV. When you use it, say so in the
     student's `profile.notes` (implied vs explicit consent). For anything beyond internal testing, put
     the consent checkbox back on the form instead.
   - **`home_country` is never taken from a post-grad answer.** It stays at the "Malaysia" default.
     Wanting to work abroad is a migration *aspiration* → `preferences.intent_to_migrate`, not a
     different home country. (The tool used to overwrite `home_country` from the old "live and work
     after graduating" question, mislabelling a Malaysian who simply wants to work overseas.)

## Finalize each student (the judgment layer — this is your job, not the tool's)

For every student the tool flagged in `profile.json`'s **`_needs_review`**:

1. **Grades** → `subjects[]` is now built **deterministically** from the four dropdown pairs and
   `grade_status = "expected"` (self-predicted / "confident of getting"). Subject names are normalised via
   `SUBJECT_NORMALIZE` in `tools/ingest_form_csv.py` (dropdown label → canonical, e.g. "Physic"→"Physics",
   "Math"→"Mathematics") — **if the form gains a new subject dropdown option, add it to that map** so it
   doesn't pass through raw. Just sanity-check the result; leave `grade_status = "expected"` unless the
   student volunteers these are actual/official-predicted grades (then set `actual`/`predicted`). The
   longlist treats `expected` as **provisional** automatically (see the provisional-grades note below).
   *(Legacy paragraph-grades forms still stage the free text under `_intake_raw.grades`; parse + delete
   it as before.)*
2. **Ethnicity** → `profile.ethnicity` is captured for **scholarship-eligibility** research. When you
   research scholarships in Stage 3/4, use it to include/exclude ethnicity-gated funds (e.g. a
   non-Bumiputra student can't claim Bumiputra-only scholarships). Never let it touch the desirability score.
3. **Scholarship** → `scholarship_required` comes straight from the "Is scholarship a must?" gate (Yes →
   a hard gate). `scholarship_interests` holds the free-text list of scholarships to research — feed it
   into the Stage 3/4 scholarship columns ("all options" = research broadly).
4. **Recognition** → the tool auto-fills `recognition_targets` from the regulated-profession answer
   via `PROFESSION_RECOGNITION` in `tools/ingest_form_csv.py`. **Verify it** — `MQA` is always the
   floor, plus the correct Malaysian professional body:

   | Profession | Targets beyond MQA |
   |---|---|
   | Medicine | MMC (Malaysian Medical Council) |
   | Engineering | BEM + Washington Accord |
   | Law | LPQB |
   | Accounting | MIA — **and usually ACCA**; the tool only auto-fills MIA, add ACCA yourself |
   | Pharmacy | Pharmacy Board Malaysia |
   | Dentistry | MDC (Malaysian Dental Council) |
   | Architecture | LAM |
   | Nursing | Nursing Board Malaysia |

   A non-regulated field (pure CS, business, design…) gets an **empty** `recognition_targets` — don't
   pad it with MQA for its own sake. See guardrail 5 in `00_overview.md` for why this is a gate and
   not a footnote.
5. **No specific course** → this is the **normal** state, not a problem. The student picked a Broad
   Area and left the course grid blank, so `specific_courses` is empty and
   `interest_discovery.decided` is `false`. Stage 3 discovers courses **within that broad area** —
   just go. Only stop and contact the student when `fields_of_interest` is **also** empty, i.e. they
   gave no direction at all; the tool flags exactly that case in `_needs_review`.
   *(The form no longer asks the old career/values/work-style questions, so `interest_discovery`'s
   free-text fields are always null. The career-backwards branch that used to consume them was
   dropped on 2026-07-25 along with `02_aspirations_intake.md`.)*
6. **Degree level** → no form question sets it; the agent sets `degree_level` at finalize
   (an A-Level / STPM / Foundation student heading to a bachelor's → `undergraduate`).
7. **Delete the `_needs_review` key** once done, so the finished `profile.json` matches the standard
   schema shape (no stray keys — compare against the current `profile_template()` in
   `tools/init_student.py`, the source of truth for the shape; note the `needs` block is the broad
   "support & belonging" set, so older students like `toru` carry a now-outdated `needs` shape).
8. Write the student's `status.md` (so `resume.md` works next session).

## Before Stage 3 — per-student scoring weights (important)

Each student needs their own **`data/students/<slug>/weights.json`**, derived from their
`preferences.priorities` with the **`scoring-weights` skill**. `sync_shortlist.py` hard-errors without
one — it will not guess.

**Scoring is now safe to parallelise.** Weights are per-student data, not shared source, so longlisting
several form students concurrently is fine: no student's scoring can overwrite another's. Never hand-edit
weights into `tools/shortlist_schema.py` — that shared file is exactly what made batching unsafe before.

## Edge cases & rules

- **Provisional (self-predicted) grades.** The form asks for grades the student is *"confident of
  getting"* → `grade_status = "expected"`. This is weaker than official predicted grades and than actual
  results, so the longlist surfaces it automatically: `sync_shortlist.py` adds a **"Grades unverified
  (self-predicted)"** warning to every row. Admission likelihood is still computed (the list stays
  actionable) — just never reads as settled. When real results / official predicted grades arrive, set
  `grade_status` to `actual`/`predicted` and re-sync to drop the caveat.
  (It used to *also* suffix the grade column with "(provisional — self-predicted, confirm at results)".
  Dropped on 2026-07-25: it repeated the warning already sitting on the same row, and cost 45 characters
  in a column that now has a 40-character budget.)
- **Ethnicity is capture-only for scholarships.** `profile.ethnicity` (PDPA-sensitive) exists to make
  scholarship research eligibility-aware (Bumiputra-only vs open funds), nothing else. Never feed it into
  the desirability score or any filter.
- **Broad-Area grid split.** `specific_courses` comes from the one non-empty cell of the eight-column
  "Broad Area of Study" grid. If a student somehow filled more than one area's cell, the tool keeps all
  non-empty cells — spot-check that `specific_courses` matches the chosen `fields_of_interest`.
- **Priority sliders — ties & scale.** The sliders are a **1-8** scale (they used to be 1-7) and can tie
  (a student may rate several categories the same). The tool orders equal values by the form's column
  order (Cost → Scholarship → University Ranking → Course Ranking → Employability → Recognition →
  Location → Hands-On), deterministic but arbitrary among ties — **sanity-check the ordering** against any
  free-text notes before deriving `weights.json`, since the top band drives the weights. `ranking_importance`
  now carries a 1-8 value; make sure the `scoring-weights` skill reads it on that scale.
- **Unsupported target countries are reported, not dropped.** A picked country outside the **8**
  supported destinations (UK / Australia / USA / Singapore / Malaysia / China / Japan / Hong Kong) —
  e.g. **Canada** or **Germany** — is left out of `target_countries` but recorded in a `_needs_review`
  line **and** `preferences.notes`, so nothing is lost silently. Decide with the student whether to
  research it out-of-band. (`SUPPORTED_DESTINATIONS` in `tools/ingest_form_csv.py` renders that message,
  so the count never drifts from `COUNTRY_NORMALIZE`.)
- **Budget bands, and what each one means downstream.** The form's four-option dropdown removed the
  whole class of budget-parsing problems (see the two retired edge cases in the note below). What lands
  where:

  | Form answer | `total_budget` + `total_budget_ceiling` | Meaning |
  |---|---|---|
  | `Under RM 500,000` | `500000` | Real ceiling — cost checks apply |
  | `RM 500,000 - 1,000,000` | `1000000` | Real ceiling — top of the band |
  | `Above RM 1,000,000` | `null` | A **floor**, not a ceiling: no "Over budget" flag |
  | `Not sure - no fixed budget` | `null` | "Research everything, I'll decide" |
  | *(blank)* | `null` | Same as "Not sure" |

  The **verbatim label** always goes to `profile.financial.notes` as `Budget answer: <label>`, so the
  nuance survives even though the number is a band edge. A `null` ceiling is a legitimate answer, not a
  gap to chase — don't invent a number for it, and never let a label string reach `total_budget_ceiling`
  (downstream cost checks expect a number or null).
  - *Legacy free-text exports* still ingest: an answer matching no band falls back to `budget_ceiling()`,
    which returns a number only if the text parses to a **plausible** degree budget (it rejects anything
    under 1000, so `"~ 1 million? Idk"` yields `None`, not `1.0`). If that fallback yields nothing, the
    tool raises a `_needs_review` line naming the answer — confirm the real ceiling with the student.
    The old *"budget unit ambiguity"* (`500` meaning RM 500,000) and *"hedging prose"* edge cases both
    belong to that legacy path only.
- **Fields the form never fills.** The schema (`profile_template()` / `preferences_template()` in
  `tools/init_student.py`) is wider than the form, so some keys are *always* null after ingest. Know
  which, so you don't mistake an absent question for a missing answer:
  - **`degree_level`** — no question. **You** set it at finalize (an A-Level / STPM / Foundation
    student heading to a bachelor's → `undergraduate`). This is the one you must not skip.
  - **`budget_ceiling_per_year`** / **`financial.budget_per_year`** — no per-year question by design
    (total cost is what Stage 4 compares).
  - **`english_proficiency.test_date_or_planned`** — the form deliberately doesn't ask "when will you
    take it"; the tests a student must sit come out of research at Stage 4 / apply stage.
  - **`min_subject_rank_pref`** — no question, and the tool never touches it. Judge subject standing
    from `ranking_importance` instead.
  - **`education_history`** — no question; fill by hand only if a student volunteers something that
    matters. (**`financial.notes`** is *not* in this list any more — the budget dropdown's verbatim
    label lands there automatically as `Budget answer: <label>`. Append to it, don't overwrite it.)
  - **`preferences.notes`** — only written when the tool dropped an unsupported country. Anything else
    you want recorded there (e.g. which country matters most, preferred universities) you add at finalize.

  `grade_status` is set from the subject dropdowns → `expected` (see the provisional grades note above);
  a legacy "actual vs predicted" column, if present, overrides it.
- **No consent / no name** → row skipped (reported in the summary). This is the PDPA gate — respect it.
- **Duplicate names** → same slug; the second is skipped rather than clobbering the first. Disambiguate
  the name (or `--force` deliberately) if two real people share a name.
- **Messy multi-select** → Forms joins checkbox answers with commas and doesn't escape commas inside a
  label; a rare answer may split oddly. Spot-check `target_countries` / `location_prefs` after ingest.
- **Everything the form couldn't capture stays `null`/empty** — the tool never invents values, and
  neither do you. A `null` is more useful than a fabricated grade or budget: it's an open question, not
  a wrong answer. Fill gaps by contacting the requester, and note what's still open in `profile.notes`.
- **Empty `specific_courses` is not a blocker.** `interest_discovery.decided` goes `false` whenever the
  course grid is blank, but a student who knows their **field** ("Computer Science") and not the exact
  course is the common case — Stage 3 discovers courses inside the chosen Broad Area. The tool only
  raises `_needs_review` when `fields_of_interest` is empty **too**; that one means contact the student,
  because there is genuinely nothing to search on. *(It used to flag every blank grid cell, which was
  pure noise — narrowed 2026-07-25 when career-backwards was dropped.)*
- **English "Other" / "Not yet".** If the respondent picks "Other" without naming the test, `test` is
  unusable — confirm which test + score before it counts. "Not yet" is fine (many longlist rows won't
  need a score until Stage 4). The specific tests-to-sit come from research, not the form.
- **Dates are dropdowns now — normalising them is no longer your job.** Both `intake` and
  `current_program.expected_completion` come from a **month + year dropdown**, and
  `_normalize_month_year()` turns "September 2027" / "Sept 2027" / "Sep 2027" into **`2027-09`** at
  ingest. That retired the by-hand date step *and* the ambiguity free text always carried (`9/10/2027`
  = Sept 10 or Oct 9?). Two behaviours to know:
  - **`intake` also accepts "Flexible".** Blank / "flexible" / "not sure" / "any" all collapse to
    `intake = "Flexible"` — never a fake date. Intake only picks the application *cycle* to research;
    it never filters or scores, so "Flexible" is a good answer, not a gap.
  - **An unreadable answer is kept verbatim, never guessed.** If a legacy export or an "Other" answer
    doesn't parse as month+year, the raw string passes through unchanged. Spot-check for that shape at
    finalize and fix it to `YYYY-MM` by hand — but don't invent a month the student didn't give.
- **Scholarship gate + interests.** The current form asks *"Is scholarship a must?"* (Yes/No) → the tool
  sets `scholarship_required` + `scholarship_dependent` directly, and *"What scholarships are you planning
  to apply for?"* (free text) → `scholarship_interests` (a research hint, never a filter; `funding_source`
  stays null here). If the gate column is absent the tool falls back, in order, to the merged *"how will
  you fund this degree?"* question and then the legacy *"how will you pay" + "only if you win a
  scholarship"* pair. A blank/unrecognized fallback answer leaves the gate null → confirm at finalize.
- **Broad `needs` set.** `needs` is now the faith/culture-neutral "support & belonging" block
  (`diet_halal`, `worship_facilities`, `diaspora_community`, `disability_accessibility`,
  `wellbeing_support`, `lgbtq_friendly`, `personal_safety`, `climate_weather`, …). Only ticked options
  become `true`; everything else stays `null` (not `false`) — these are PDPA-sensitive, so absence ≠ "no
  need". Spot-check the multi-select split, same as countries.
- **Regulated-profession vs field mismatch.** Auto-filled `recognition_targets` follow the *ticked
  profession*; if that conflicts with the stated field (e.g. "Engineering" ticked but the field is
  pure Computer Science — CS is not BEM/Washington-Accord accredited), keep MQA but caveat the
  professional-body targets and verify against the actual course type.

## Done when

Each requested student has a finalized `profile.json` + `preferences.json` (no `_needs_review` /
`_intake_raw` left), a `status.md`, and is ready for **Stage 3** (`03_discover_longlist.md`).
