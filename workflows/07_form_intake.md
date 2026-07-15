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
- **Name**; **Your age**; **Gender**; **Nationality**; where you **live in now**; where you plan to **live and
  work after** graduating (a post-study *aspiration* → recorded in `notes` + `intent_to_migrate`;
  it does **not** become `home_country`, which stays "Malaysia").

**Section 2 - Your Studies**
- What are you **studying now** (A-Level / STPM / UEC / IB / Foundation / Matriculation / Diploma /
  Other); **which college**/school; **when do you finish** / get results.
- **List each subject** and your grade — paragraph (e.g. "Maths A*, Physics A, Chemistry B").
- Are those grades **actual results or predicted** — Actual / Predicted.
- **English proficiency — a capability snapshot only.** Ask just: **which English test** have you taken
  (IELTS / TOEFL / MUET / PTE / Duolingo / **Not yet** / Other) and your **English test score** (blank
  if none). *Do NOT ask "when will you take it".* Each university sets its own English bar; the required
  test + score per uni is filled during research (`English req` / `Meets English?`), and the definitive
  "tests you must sit" list is produced at the apply stage — not here.
- **Total budget** for the whole degree in MYR (blank = "research everything, I'll decide" — the
  intended default; a rough ceiling only powers the "Over budget" flag); **per-year budget** (optional).
- **How will you fund this degree?** — ONE question (replaces the old "how will you pay" + "only if
  scholarship" pair). Options, most- to least-dependent: *"I can only go on a full or near-full
  scholarship"* / *"I need a partial scholarship or financial aid to make it work"* / *"My family/I can
  cover it — scholarships optional"*. This one answer sets both `funding_source` and whether a
  scholarship is a hard **gate** (`scholarship_required` / `scholarship_dependent`).
- Are you aiming at a **regulated profession** — checkboxes (Medicine / Engineering / Law / Accounting
  / Pharmacy / Dentistry / Architecture / Nursing / None). *(Should match the intended career — see the
  Engineering-vs-CS edge case below.)*
- Any **support & belonging needs** (optional; PDPA-sensitive) — checkboxes, broad and faith/culture-
  neutral: **Halal food** / **Prayer facilities** / **Malaysian community nearby** / **Stay close to family** / **Personal safety** /
  **Climate / weather** — plus **Other**.

**Section 2 — What you want → `preferences.json`**
- **Which countries** would you consider — checkboxes (UK / Australia / USA / Singapore-Malaysia /
  China). Picking several is fine (research-first breadth). *(Optional follow-up: **which country
  matters most?** — the agent records it in `preferences.notes` so research goes deepest where it
  counts.)*
- What **field or subject**; do you **already know the exact course** (Yes → next section / No →
  interest-discovery, via Forms "Go to section based on answer"); if yes, **name the course**(s).
- **Degree level**; **when do you want to start** — pick a **year + season** (e.g. "Sept 2027") **or**
  *"Flexible / show me all intakes"*. Intake only selects the application *cycle* to research — it never
  filters or scores, so "Flexible" is a perfectly good answer (stored as `Flexible`).
- Your **#1 priority** / **#2 priority** / **#3 priority** — three dropdowns from: Cost / Scholarship /
  Ranking / Employability / Recognition back home / Location / Hands-on experience.
- **How much does the university's strength in *your subject* matter** — linear scale 1-5. *(Steers the
  `subject_reputation` sub-score — subject-specific standing + graduate outcomes, not overall vanity
  rank.)*
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

1. **Grades** → parse `_intake_raw.grades` into `subjects[]` as `{subject, grade_or_predicted}`.
   `grade_status` is already set from the form; sanity-check it. Then **delete `_intake_raw`**.
2. **Recognition** → the tool auto-fills `recognition_targets` from the regulated-profession answer
   (e.g. Engineering → `["MQA","BEM","Washington Accord"]`). **Verify** against the recognition
   guardrail in `00_overview.md` (MQA + the correct professional body) and correct if needed.
3. **Undecided student** → confirm `interest_discovery`, then run the Stage 2 **career-backwards**
   branch (`02_aspirations_intake.md`) to propose candidate fields *with the requester* before
   discovery. Don't silently pick a field. *(If the **field** is already clear and only the exact
   course/university is open — e.g. "Computer Science" — leave `decided=false` but skip the full
   career-backwards pass; Stage 3 can discover courses directly.)*
4. **Delete the `_needs_review` key** once done, so the finished `profile.json` matches the standard
   schema shape (no stray keys — compare against the current `profile_template()` in
   `tools/init_student.py`, the source of truth for the shape; note the `needs` block is the broad
   "support & belonging" set, so older students like `toru` carry a now-outdated `needs` shape).
5. Write the student's `status.md` (so `resume.md` works next session).

## Before Stage 3 — per-student scoring weights (important)

`SCORE_WEIGHTS` in `tools/shortlist_schema.py` is a **single global** weighting. When you longlist
several form students in a row, **re-tune `SCORE_WEIGHTS` from that student's `preferences.priorities`
before each `sync_shortlist.py` run**, and process **one student at a time**. (A per-student weights
file is a planned upgrade; until then, don't batch the *scoring* — only the intake is batched.)

## Edge cases & rules

- **No consent / no name** → row skipped (reported in the summary). This is the PDPA gate — respect it.
- **Duplicate names** → same slug; the second is skipped rather than clobbering the first. Disambiguate
  the name (or `--force` deliberately) if two real people share a name.
- **Messy multi-select** → Forms joins checkbox answers with commas and doesn't escape commas inside a
  label; a rare answer may split oddly. Spot-check `target_countries` / `location_prefs` after ingest.
- **Everything the form couldn't capture stays `null`/empty** — the tool never invents values. Fill
  gaps by contacting the requester, same honesty rule as `01`.
- **"Undecided" over-triggers.** The tool flags `undecided` whenever "know the exact course?" = No OR
  `specific_courses` is empty — but a student who clearly knows their **field** (e.g. "Computer
  Science") just doesn't know the exact *course/university*. That is normal and needs **no** Stage-2
  career-backwards pass; set `interest_discovery.decided=false` but note the field is known and go
  straight to Stage 3. Only run career-backwards when the *field itself* is genuinely open.
- **English "Other" / "Not yet".** If the respondent picks "Other" without naming the test, `test` is
  unusable — confirm which test + score before it counts. "Not yet" is fine (many longlist rows won't
  need a score until Stage 4). The specific tests-to-sit come from research, not the form.
- **Free-text dates are ambiguous** (`9/10/2027` = Sept 10 or Oct 9?). Normalize `intake` /
  `expected_completion` to `YYYY-MM` (or "YYYY Mon") during finalize and confirm with the student. The
  improved form asks intake as **year+season or "Flexible"**; the tool collapses blank / "flexible" /
  "not sure" to `intake = "Flexible"` (never a fake date). `expected_completion` is still free text —
  normalize it by hand.
- **Merged funding question.** The tool reads the single *"how will you fund this degree?"* answer and
  derives `funding_source` + `scholarship_required` + `scholarship_dependent` together (full/near-full →
  both flags true; partial/aid → required true, dependent false; family/self → both false). If the form
  still has the **legacy** two questions instead, the tool falls back to them automatically. If the
  answer is free-text "Other" and matches no keyword, funding stays blank → confirm at finalize.
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
