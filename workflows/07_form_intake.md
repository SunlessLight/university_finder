# Workflow: Form Intake — Google Form CSV → student data banks (alternate Stage 1/2 on-ramp)

## Objective

Let **other people** request a university search without you driving a live conversation. They fill a
**Google Form**; you export the responses as CSV; this workflow batch-builds one
`data/students/<slug>/` per respondent (filled `profile.json` + `preferences.json`), then you finalize
a few judgment-heavy fields and hand each student off to **Stage 3** (discover longlist).

This replaces the *conversational* Stage 1 (`01_student_intake.md`) and Stage 2
(`02_aspirations_intake.md`) with a *form-driven* intake. The downstream pipeline (Stage 3-5) is
unchanged.

## The Google Form (build once)

Create **one form**, turn **"Collect email addresses" ON** (Settings → Responses), and add the
questions below. Question **wording** maps to CSV column headers; the tool matches columns by a
distinctive **substring** (see `QUESTION_MAP` in `tools/ingest_form_csv.py`), so light rewording is
fine — but keep the substring in bold intact.

**Section 0 — Consent & identity (required)**
- **"Collect email addresses" turned ON.** 
- **I consent** 'Cool for me to store your answers and use them to research unis for you 👍?'. — required checkbox. *(A row that explicitly answers **No** is always skipped.
  A **blank/absent** consent is also skipped **unless** you pass `--assume-consent` — see below.)*

**Section 1 — About you → `profile.json`**
- **Name**; **Your age**; **Gender**; **Nationality**; **Race/ethnicity**; where you **live in now**;
  where you plan to **live and work after** graduating (a post-study *aspiration* → recorded in `notes`
  + `intent_to_migrate`; it does **not** become `home_country`, which stays "Malaysia").
  - **Race/ethnicity → `profile.ethnicity`** (PDPA-sensitive). Captured because it drives
    **scholarship eligibility** in Malaysia (e.g. Bumiputra-only vs open funds) — the agent uses it as a
    research signal in Stage 3/4. It is **never** a desirability-score input.

**Section 2 - Your Studies**
- What are you **studying now** (A-Level / STPM / UEC / IB / Foundation / Matriculation / Diploma /
  Other); **which college**/school; **when do you graduate** / get results.
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
- **Total budget** for the whole degree in MYR (blank = "research everything, I'll decide" — the
  intended default; a rough ceiling only powers the "Over budget" flag).
- **Is scholarship a must?** — Yes/No. A clean gate: Yes sets both `preferences.scholarship_required` and
  `financial.scholarship_dependent` true. **What scholarships are you planning to apply for?** — free text
  → `preferences.scholarship_interests`, a *research hint* (which scholarships to dig into; "don't know /
  all options" is a fine answer meaning research broadly). It never filters or scores. *(Legacy forms with
  a "how will you pay" / merged "how will you fund" question still work — the tool falls back automatically
  when the "is scholarship a must?" column is absent.)*
- Are you aiming at a **regulated profession** — checkboxes (Medicine / Engineering / Law / Accounting
  / Pharmacy / Dentistry / Architecture / Nursing / None). *(Should match the intended career — see the
  Engineering-vs-CS edge case below.)*
- Any **support & belonging needs** (optional; PDPA-sensitive) — checkboxes, broad and faith/culture-
  neutral: **Halal food** / **Prayer facilities** / **Malaysian community nearby** / **Stay close to family** / **Personal safety** /
  **Climate / weather** — plus **Other**.

**Section 2 — What you want → `preferences.json`**
- **Which countries** would you consider — checkboxes (UK / Australia / USA / Singapore-Malaysia /
  China / Japan). Picking several is fine (research-first breadth). *(Optional follow-up: **which country
  matters most?** — the agent records it in `preferences.notes` so research goes deepest where it
  counts.)*
- **Broad Area of Study + a course grid.** One **Broad Area of Study** dropdown (Arts, Humanities &
  Design / Media, Communication & Social Sciences / Business, Finance & Management / Computer Science, IT
  & Data / Engineering & Built Environment / Pure & Applied Sciences / Health & Medical Sciences /
  Education & Teaching) → `preferences.fields_of_interest`. A **grid** of those same eight areas as columns
  captures the exact course under the chosen area (e.g. Engineering & Built Environment = "Mechanical
  Engineering") → `preferences.specific_courses` (the tool collects the one non-empty grid cell).
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
  value (1-7).
- Do you want to **work abroad** after graduating — Yes / No / Unsure.
- Any **deal-breaker**s (optional); **location preference**s (optional checkboxes); **prefered universities** (optional).

**Section 3 — Only if undecided → `profile.interest_discovery`**
- What **career or life** do you want; what activities you **genuinely enjoy**; how you **like to
  work**; what **matters to you**; any **constraints**.

## How to run

1. Export the form responses (Responses → ⋮ → *Download responses (.csv)*) and drop the file in
   **`data/form/`** (gitignored — it's PII). Default name: `data/form/responses.csv`.
2. Preview first, then run for real:
   ```powershell
   python tools/ingest_form_csv.py data/form/responses.csv --dry-run
   python tools/ingest_form_csv.py data/form/responses.csv
   ```
   The tool creates `data/students/<slug>/{profile.json,preferences.json,dossiers/}` per consenting
   respondent, copies budget/scholarship into **both** files, and prints a per-student
   **"Needs agent review"** list. Add `--force` only to intentionally overwrite an existing folder.
   - `--assume-consent` — **internal-only escape hatch.** If the form has no consent question (e.g. a
     friends-only test intake where the formal checkbox was dropped as too heavy), this treats a
     blank/absent consent as consent given so the row isn't skipped. It does **not** relax an explicit
     **No**, and it never writes a fabricated consent value into the CSV. When you use it, say so in the
     student's `profile.notes` (implied vs explicit consent). For anything beyond internal testing, put
     the consent checkbox back on the form instead.
   - **`home_country` is NOT the post-grad answer.** The *"where do you want to live and work after
     graduating"* question is a migration *aspiration* — the tool records it in `profile.notes` +
     `preferences.intent_to_migrate` and leaves `home_country` at the "Malaysia" default. (Earlier the
     tool wrongly overwrote `home_country` with it, mislabelling a Malaysian who wants to work abroad.)

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
   (e.g. Engineering → `["MQA","BEM","Washington Accord"]`). **Verify** against the recognition
   guardrail in `00_overview.md` (MQA + the correct professional body) and correct if needed.
5. **Undecided student** → confirm `interest_discovery`, then run the Stage 2 **career-backwards**
   branch (`02_aspirations_intake.md`) to propose candidate fields *with the requester* before
   discovery. Don't silently pick a field. *(If the **field** is already clear and only the exact
   course/university is open — e.g. "Computer Science" — leave `decided=false` but skip the full
   career-backwards pass; Stage 3 can discover courses directly.)*
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
- **Unsupported target countries are reported, not dropped.** A picked country outside the 6 sets
  (UK / Australia / USA / Singapore-Malaysia / China / Japan) — e.g. **Canada** or **Germany** — is left
  out of `target_countries` but recorded in a `_needs_review` line **and** `preferences.notes`, so
  nothing is lost silently. Decide with the student whether to research it out-of-band.
- **Budget unit ambiguity.** A bare number like **`500`** for a whole degree is almost certainly *in
  thousands* (RM 500,000), not RM 500. The tool captures the raw cell verbatim; **you** interpret the unit
  at finalize and note the assumption — confirm the real ceiling with the student.
- **`degree_level` is an absent column.** The form has no "degree level" question, so it stays null →
  **you** set it at finalize (an A-Level / STPM / Foundation student heading to a bachelor's →
  `undergraduate`). `grade_status` is set from the subject dropdowns → `expected` (see the provisional
  grades note above); a legacy "actual vs predicted" column, if present, overrides it.
- **No consent / no name** → row skipped (reported in the summary). This is the PDPA gate — respect it.
- **Duplicate names** → same slug; the second is skipped rather than clobbering the first. Disambiguate
  the name (or `--force` deliberately) if two real people share a name.
- **Messy multi-select** → Forms joins checkbox answers with commas and doesn't escape commas inside a
  label; a rare answer may split oddly. Spot-check `target_countries` / `location_prefs` after ingest.
- **Everything the form couldn't capture stays `null`/empty** — the tool never invents values. Fill
  gaps by contacting the requester, same honesty rule as `01`.
- **"Undecided" over-triggers.** The tool flags `undecided` whenever `specific_courses` is empty (on the
  current form: the student picked a Broad Area but left the course grid blank) — but a student who
  clearly knows their **field** (e.g. "Computer Science") just doesn't know the exact *course/university*.
  That is normal and needs **no** Stage-2 career-backwards pass; set `interest_discovery.decided=false`
  but note the field is known and go straight to Stage 3. Only run career-backwards when the *field
  itself* is genuinely open. *(When the grid course is filled, the tool marks `decided=true` — no flag.)*
- **English "Other" / "Not yet".** If the respondent picks "Other" without naming the test, `test` is
  unusable — confirm which test + score before it counts. "Not yet" is fine (many longlist rows won't
  need a score until Stage 4). The specific tests-to-sit come from research, not the form.
- **Free-text dates are ambiguous** (`9/10/2027` = Sept 10 or Oct 9?). Normalize `intake` /
  `expected_completion` to `YYYY-MM` (or "YYYY Mon") during finalize and confirm with the student. The
  improved form asks intake as **year+season or "Flexible"**; the tool collapses blank / "flexible" /
  "not sure" to `intake = "Flexible"` (never a fake date). `expected_completion` is still free text —
  normalize it by hand.
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
