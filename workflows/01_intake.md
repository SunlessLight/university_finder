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
- **Nickname**; **Race/ethnicity**.
  - **Nickname permanently replaces "Full name" (2026-08+, identity protection).** `QUESTION_MAP`
    maps `"nickname"` straight onto the `name` logical key — same slug/personalization path as
    before, no special handling. Don't expect a real legal name in `profile.name`; a report should
    address the student by whatever nickname they gave (some are gamertag-style handles, e.g.
    `GwakGwak3000` — that's expected, not a data-quality problem).
  - **Age, Gender, Nationality, and "where you live in now" are gone (2026-08+), permanently.**
    None of them ever had a downstream read path — no tool, no agent prompt anywhere in the
    pipeline consumed them — so they were cut as pure friction. `profile_template()` no longer
    carries these keys at all; don't reintroduce them without wiring a real consumer first.
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
- **Qualification type is a permanent hardcoded default, not a question (2026-08+).** The form no
  longer asks "what are you studying now" or "which college" — this project targets A-Level students
  only, so `current_program.type` is hardcoded to `"A-Level"` in `profile_template()`, the same
  pattern as `home_country: "Malaysia"`. If a non-A-Level student ever comes through this form, fix
  `current_program.type` by hand at finalize — the tool will not catch it, since nothing asks the
  question any more. `current_program.institution` is gone from the schema entirely (no downstream
  use, never wired to anything).
- **When do you graduate** / get results — **two separate dropdowns now: month, then year** (added
  2026-09, e.g. "January" + "2027"). The old single month+year dropdown's option text carried no year
  at all ("January (Takes A2 in Oct/Nov)" — found 2026-08-23, see the edge case below); the dedicated
  year column fixes that at the source. `map_row()` concatenates the two raw answers before calling
  `_normalize_month_year` (`YYYY-MM`), so nothing downstream needs to change — an answer it can't read
  as a month+year is kept verbatim, never guessed.
- **Subjects & grades — a 12-column fixed-subject grid (2026-08+, replaces the old 4-slot free-choice
  dropdown pairs).** The form now asks one column per subject — *"Select the forecast grades for your
  subjects. ( Or grade ur confident in getting ) [`<Subject>`]"* — for exactly these 12: **Biology,
  Physic, Chemistry, Math, Further Math, English Literature, Economics, Accounting, Computer Science,
  Psychology, History, Law**. A student leaves blank the ones they don't take. `_subject_grid_columns()`
  detects these columns by the shared marker substring `"forecast grades for your subjects"` plus the
  bracketed subject name, and `_build_subjects_from_grid()` builds `profile.subjects[]` from every
  non-blank cell — this is now the **primary** path; the legacy paired-dropdown detector
  (`_subject_columns()`/`_build_subjects()`) only fires as a fallback for an old-format CSV. Same
  `grade_status = "expected"` stamp as before (self-prediction, provisional — see the edge case below).
  A separate question, **"Are you applying with forecast result or actual?"** (Forecast/Actual),
  overrides `grade_status` to `"actual"` when answered "Actual" — every respondent answers this now,
  not just an edge case.
- **English proficiency — two SEPARATE questions now, watch the substring collision.** **"English Test
  Taken"** (IELTS / TOEFL / MUET / PTE / Duolingo / **None** / Other) and, positioned much later on the
  form (near the optional/free-text cluster, not adjacent to the test question), **"If English test
  taken, what's the score? ( leave blank if haven't )"**. The second header's text literally *contains*
  the first header's matching substring (`"english test taken"`), so `QUESTION_MAP`'s entry for
  `english_score` (`"what's the score"`) **must be listed before** the entry for `english_test`
  (`"english test taken"`) — `build_col_index()` takes the first list match per header, so the wrong
  order silently steals the score question's match and drops the score entirely. Keep this cautionary
  note if either header is reworded again. *Do NOT ask "when will you take it"* — each university sets
  its own bar; that's a research-stage fact, not an intake one.
- **Total budget** for the whole degree — a **four-option dropdown**, not free text. As of 2026-08 the
  live labels use **symbols**: **`< 500,000`** / **`500,000 - 1,000,000`** / a top "no ceiling" band
  (word or symbol — `"above"`/`">"` both map) / **`Not Sure`**. `BUDGET_BAND_NORMALIZE` maps them to a
  numeric ceiling (500000 / 1000000 / **null** / null — the top band states a *floor*, so it carries no
  ceiling, exactly like "Not sure"); the **verbatim label** goes to `financial.notes` and the **number**
  to `financial.total_budget` + `preferences.total_budget_ceiling`. A label string must never reach
  `total_budget_ceiling` — downstream cost checks expect a number or null. **Ask for the total, never
  per-year** — Stage 4 compares whole-programme cost, and a 3-year UK degree against a 4-year US one is
  not comparable per year. There is no per-year question, so `financial.budget_per_year` /
  `preferences.budget_ceiling_per_year` stay null.
- **Is scholarship a must?** — Yes/No. A clean gate: Yes sets both `preferences.scholarship_required` and
  `financial.scholarship_dependent` true. *(Legacy forms with a "how will you pay" / merged "how will
  you fund" question still work — the tool falls back automatically when the "is scholarship a must?"
  column is absent.)* **"What scholarships are you planning to apply for?" is gone from the form
  (2026-08+), permanently** — `preferences.scholarship_interests` stays null by design now. This isn't a
  gap: Stage 3/4 already researches every available scholarship (university + government/external +
  Malaysian sponsors — JPA/MARA/Yayasan/PTPTN) for every finalist regardless of this field, per
  `04_university_report.md` §6, so a research-hint question was pure friction.
- **The "regulated profession" checkbox is gone from the form (2026-08+), permanently.**
  `recognition_targets` is no longer checkbox-driven — `_guess_recognition_targets()` keyword-scans
  `preferences.fields_of_interest` + `preferences.specific_courses` against the same
  `PROFESSION_RECOGNITION` map instead (a course/field that literally names "Engineering", "Medicine",
  etc. still gets recognition targets auto-filled). See the finalize step below for the verification
  duty this creates.
- **"Any other perferences?"** (optional; PDPA-sensitive; live header keeps the site's own typo,
  "perferences" not "preferences" — `QUESTION_MAP` matches on the typo, `--check-headers` will flag it
  if it's ever fixed). **Replaced the old "Any personal needs?" checkbox 2026-09** — a consolidated
  lifestyle checklist: **Low crime rate** (→ `needs.personal_safety`) / **4 seasons** (→
  `needs.climate_weather`) / **Good public transport** (→ `needs.good_public_transport`, new) /
  **Affordable living cost** (→ `needs.affordable_cost_of_living`, new) / **Good food** (→
  `needs.food_quality`). **The old sensitive items — Halal food, Prayer facilities, Malaysian community
  nearby, Stay close to family, disability/accessibility, mental-health/wellbeing support, LGBT-friendly
  — do not appear anywhere on the current 42-column form.** Confirm with Evan whether that's a
  deliberate drop or something to add back before treating a student's silence on those as "no need"
  rather than "not asked" — `profile_template()`'s `needs` keys for them are unchanged, they'll just
  never get populated by this form as it stands.
- **"Achievements / activities you'd want to write about in your application?"** (optional, new
  2026-08) → `profile.achievements`, free text. This exists specifically so Stage 4's "Who actually
  gets in" section and the application-prep guide can compare the student's real activities against
  what admitted applicants are shown to have, instead of only generic "here's what unis look for" text
  — the concrete need that prompted this: a student explicitly asked "what traits are universities
  looking for in my application, and do I match?"

**Section 3 — What you want → `preferences.json`**
- **Which countries** would you consider — checkboxes (UK / Australia / USA / **Singapore** /
  **Malaysia** / China / Japan / Hong Kong — **8** supported destinations; `COUNTRY_NORMALIZE` in
  `tools/ingest_form_csv.py` is the source of truth for the exact tokens). **Singapore and Malaysia
  are separate** as of 2026-07-29 — they were fused into one `Singapore/Malaysia` token, which gave a
  student who ticked only Malaysia a longlist half-full of Singapore rows. Picking several is fine
  (research-first breadth). **Live header as of 2026-09 is "Chose your countries"** (sic — the form's
  own typo for "Choose"); `QUESTION_MAP` matches on the typo directly rather than relying on the old
  "which countries" substring, which this header no longer contains.
- **"Which country matters most ( if you picked several )?"** — live on the form as of 2026-08 →
  `preferences.primary_country`. When set, `workflows/03_discover_longlist.md`'s "Pick the next
  country" step researches it first, overriding pure `target_countries` list order — so this is no
  longer a captured-but-inert field, it actually steers Stage 3 discovery order.
- **"Choose your desired course"** — ONE dropdown, 38 options, PLUS a free-text supplement.
  **Replaced the old "Broad Area of Study" selector + eight-column per-area grid entirely, 2026-09.**
  There is no broad-area routing step any more — every student sees the same flat list of all 38
  options and picks one directly (e.g. *"Electrical & Electronics Engineering — circuits, power,
  robotics"*) → `preferences.specific_courses` (the primary source now — `QUESTION_MAP`'s
  `"choose your desired course"` entry). **`preferences.fields_of_interest` is unpopulated on the
  current form by design** — there's no structured broad-area capture left to derive it from; that was
  a deliberate simplification Evan made, not a bug (confirmed 2026-09-03).

  The 38 option titles are unchanged from the **2026-09-01 rewording** (source of truth:
  `google_form_notes.md`) — that revision work wasn't wasted, it just now serves one flat dropdown
  instead of eight per-area grids. Reworded for A-Level Malaysian students who don't know course
  names/descriptions going in (a relatable hook instead of an academic catalog phrase, e.g. "Design —
  graphic, fashion, product, interior"); merged only where fields truly overlap (Computing) or an
  option was too niche to stand alone (Naval → Mechanical); every option follows `Title — 3-4 concrete
  nouns`, no semicolons, no cross-references between options (a student picking from one flat list can
  still only see the option's own wording, so disambiguation must be self-contained). Keep the format
  rule if the option list is ever revised again.

  **`_split_multi()` (comma-splitting) is deliberately NOT used on this answer** — a single-select
  dropdown whose own option text contains commas (the format rule's hook style) would get shredded
  into fake fragments (found + fixed 2026-09-03, spot-checking the real first ingest). The answer is
  taken as one item. **"Any SPECIFIC FIELD OF STUDIES interested in? Can write more than 1."** — a
  separate free-text question (numbered-list or `/`-separated) — is still merged in alongside it as a
  genuine supplement (`_split_free_list()`), so a student can name interests beyond their chosen course.

  This selection still sets `interest_discovery.decided = true`, same as before.
- **"When do you want to start" is gone from the form (2026-08+), permanently.** The reasoning: the
  student should decide their intake based on the university research, not the other way around.
  `preferences.intake` therefore always resolves to the literal string **`"Flexible"`** (never `null`)
  via `_normalize_intake()`'s blank-input default — this is intentional, not a gap. *(No separate
  "degree level" question → the tool defaults `degree_level` to `"undergraduate"` automatically, 2026-08-29+;
  see item 6 below.)*
- **"Tick the importance of each topic below"** — **eight per-category questions, a 3-tier scale now
  (replaced the 1-8 numeric sliders 2026-09)**: **Must have** / **Important** / **Nice to have**, one
  each for: **Affordable Cost / Scholarship availability / University Ranking / Course Ranking /
  Employability / Recognition back home / Location / Hands-On Experience** (category wording also
  lightly reworded — e.g. "Cost"→"Affordable Cost" — but the substrings `QUESTION_MAP` matches on
  still hit). The tool detects them by the shared *"tick the importance"* marker (the legacy *"rank
  your priorities"* marker still works too, so an older export still parses) + the bracketed category,
  normalises the tier to a number via `TICK_IMPORTANCE_NORMALIZE` (3/2/1), then orders the categories
  by that value (highest first, ties broken by the form's column order) into `preferences.priorities` —
  same ordering logic as the old numeric sliders, just fed a 3-tier value instead of a 1-8 one. This
  still gives a full 8-way ranking including **Course Ranking** (`course_quality` → `course_match`).
  *(Legacy forms with **#1/#2/#3 priority** dropdowns still work — the tool falls back automatically
  when neither marker is present.)*
- **`ranking_importance`** steers the `subject_reputation` sub-score (subject-specific standing +
  graduate outcomes, not overall vanity rank). If the form has a dedicated *"how much does your subject's
  strength matter"* question the tool uses it; otherwise it reads the **[University Ranking]** tick
  answer verbatim — a **3-tier label** now ("Must have" / "Important" / "Nice to have"), not the old
  **1-8** numeric slider value. **Check the `scoring-weights` skill reads this on the new scale** before
  deriving a `weights.json` for a student ingested through the current form — it hasn't been re-checked
  against the 2026-09 rework as of this writing.
- Do you want to **work abroad** after graduating — Yes / No / Unsure. → `intent_to_migrate` (and the
  raw answer into `post_study_work_importance`).
- **Dealbreakers is gone from the live form (2026-09), permanently.** It used to be its own optional
  question (`preferences.deal_breakers`); it's now folded into "Any other perferences?" above (→
  `needs`), so `deal_breakers` stays an empty list on the current form by design, not a gap.
  **Location preferences** (optional checkboxes, e.g. "Rural / Campus-based", "Close to public
  transport") is still its own separate question → `preferences.location_prefs`.
- **Preferred universities** — ✅ **wired (2026-08+).** *"Universities you already have in mind ( if
  any )? Can write more than 1."* → `preferences.preferred_universities`, free text (answers use
  "and" between names, not commas — don't split it into a list). A student naming unis they already
  care about is no longer silently ignored.
- **Additional requirements is gone from the live form (2026-09), permanently.** The old *"Is there any
  specific information you want to know about universities..."* free-text question — the one that
  originally prompted this whole redesign, feeding Stage 4 §3 ("Who actually gets in") and §13
  (application-prep checklist) — has been folded into "Any other perferences?" above (→ `needs`), same
  as dealbreakers. `preferences.additional_requirements` stays null on the current form by design.
  Confirm with Evan whether the Stage 4 §3/§13 use case still has a source now that its dedicated
  question is gone, or whether it needs pulling from `needs`/`achievements` instead.

## How to run

Four commands, in this order. Steps 1-3 are safe to repeat; step 4 is the one that changes the sheet.

1. **Fetch what's pending** — pulls only responses that haven't been ingested yet, straight from the
   responses spreadsheet, into `data/form/responses.csv` (gitignored — it's PII):
   ```powershell
   python tools/fetch_form_responses.py --dry-run   # who's pending, writes nothing
   python tools/fetch_form_responses.py             # writes data/form/responses.csv
   ```
   "Already ingested" is recorded **in the sheet**, in a column called `Ingested at` (blank = pending),
   so it survives a wiped `data/` folder or a different machine. The fetched CSV carries one extra
   trailing column, `_row`, holding each response's sheet row number — that's what step 4 stamps.
   Both `_row` and `Ingested at` are inert to `ingest_form_csv.py` (they match nothing in
   `QUESTION_MAP`), which is why the ingest tool needs no special handling.

   *Fallback if the endpoint is broken or not set up:* export by hand (Responses → ⋮ → *Download
   responses (.csv)*) and drop the file in **`data/form/`**. Google names the export after the form
   itself (e.g. `Form responses - Sheet1.csv`), not `responses.csv` — the ingest tool takes whatever
   path you pass. A manual export has no `_row` column, so step 4 can't run against it; stamp the
   `Ingested at` cells by hand instead, or the same people come back next fetch.

2. Preview first, then run for real:
   ```powershell
   python tools/ingest_form_csv.py "data/form/responses.csv" --dry-run
   python tools/ingest_form_csv.py "data/form/responses.csv"
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

3. **Finalize each student's `_needs_review` items** — the next section. This is the judgment step and
   it happens *before* step 4.

4. **Confirm — last, and only once the ingest actually succeeded:**
   ```powershell
   python tools/fetch_form_responses.py --confirm
   ```
   This stamps `Ingested at` for every row in `data/form/responses.csv`, so those respondents are never
   handed back again. Running it last is the whole safety property: **a crashed or abandoned ingest
   leaves the rows pending**, and re-running step 1 simply hands them back. Confirming early and then
   failing to ingest loses the respondents silently.

### Edge cases

- **Never sort the responses sheet by hand.** Row identity is the sheet row number, which only holds
  because Forms *appends* responses and never reorders them. A `Data → Sort range` would make `_row`
  in an already-fetched CSV point at the wrong respondent, and `--confirm` would stamp the wrong rows.
  Filter views are fine (they don't move the underlying rows). If it does get sorted, delete
  `data/form/responses.csv` unconfirmed and re-fetch.
- **`--confirm` reports skipped rows** when the CSV and the sheet disagree (a `_row` beyond the end of
  the sheet). It exits non-zero and names them — usually it means the sheet was sorted or rows deleted.
- **Deleting rows from the sheet shifts every row below them up.** Same hazard as sorting: only ever do
  it when there is no unconfirmed `responses.csv` sitting on disk.
- **`--confirm` against a manual export** fails with a clear error — there's no `_row` column to stamp.

## Finalize each student (the judgment layer — this is your job, not the tool's)

**As of 2026-09, most of this stage is deterministic and needs no per-student review.** Grades,
ethnicity, the scholarship gate, degree level, and recognition_targets matched off the "Choose your
desired course" dropdown are all filled straight from clean form answers or an exact lookup against
a closed, known set — none of them raise a `_needs_review` line any more. The only thing left to
check per student is whatever the tool actually flagged in `profile.json`'s **`_needs_review`**
(normally just a free-text recognition match, or the rare no-course-no-field case):

1. **Grades** — nothing to check. `subjects[]` is built **deterministically** from the 12-column
   subject grid (see Section 2 above); `grade_status` starts at `"expected"` (self-predicted /
   "confident of getting") and is overridden to `"actual"`/`"predicted"` by the separate "forecast or
   actual" question when answered. `sync_shortlist.py` already surfaces `expected` as a "Grades
   unverified (self-predicted)" warning automatically once the student reaches the master list, so it
   doesn't need flagging again at intake. Subject names are normalised via `SUBJECT_NORMALIZE` in
   `tools/ingest_form_csv.py` (grid label → canonical, e.g. "Physic"→"Physics") — **if the form gains a
   new subject grid column, add it to that map** so it doesn't pass through raw. *(Legacy
   paragraph-grades forms still stage the free text under `_intake_raw.grades`; parse + delete it as
   before — that path is the one remaining manual case.)*
2. **Ethnicity** — nothing to check, just a fact to carry forward. `profile.ethnicity` is a clean
   pass-through of one dropdown answer, captured for **scholarship-eligibility** research. When you
   research scholarships in Stage 3/4, use it to include/exclude ethnicity-gated funds (e.g. a
   non-Bumiputra student can't claim Bumiputra-only scholarships). Never let it touch the desirability
   score.
3. **Scholarship** — nothing to check. `scholarship_required` comes straight from the clean "Is
   scholarship a must?" Yes/No gate. `scholarship_interests` stays null by design (its question was
   dropped from the form) — Stage 3/4 already researches every available scholarship for every
   finalist regardless (per `04_university_report.md` §6), so treat `scholarship_required = true` alone
   as "research broadly."
4. **Recognition** — two independent sources, only one of which is ever flagged:
   - **The "Choose your desired course" dropdown** is a **closed, known set of 38 titles**
     (`google_form_notes.md`). `_course_recognition_targets()` exact-matches the answer's title
     against `COURSE_ACCREDITATION_MAP` in `tools/ingest_form_csv.py` — deterministic, **never
     flagged**. The map was built from the same 38 titles and verified against the actual Malaysian
     regulator for each (BEM, MMC, LPQB, MIA+ACCA, Pharmacy Board, MDC, LAM, BQSM, Nursing Board
     Malaysia, MAHPC — sourced 2026-09), so it needs no per-student check. It only needs a one-time
     update if **you** change a course title in the live form — a renamed title stops matching and
     silently falls back to `[]` (see `_check_headers`-style drift risk, same principle as
     `QUESTION_MAP`). Two of the 38 options bundle more than one real profession (the option itself
     does — see the comment above `COURSE_ACCREDITATION_MAP`): "Architecture & Built Environment"
     carries both LAM (architects) and BQSM (quantity surveyors); "Nursing & Allied Health" carries
     both Nursing Board Malaysia (nurse) and MAHPC (physiotherapist/radiographer). A non-regulated
     field (pure CS, business, design, pure science, teaching…) gets an **empty** `recognition_targets`
     — don't pad it with MQA for its own sake. See guardrail 5 in `00_overview.md` for why this is a
     gate and not a footnote.
   - **The optional free-text "Any SPECIFIC FIELD OF STUDIES..." supplement** is open text, so it still
     goes through the old best-effort scanner (`_guess_recognition_targets()` against
     `PROFESSION_RECOGNITION`) and **only this path** raises a `_needs_review` line, naming the matched
     keyword(s). **Verify every hit, in both directions** — this is the one manual check left in this
     whole stage:
     - **False negative** — text that never literally names the profession (e.g. "Biomedical
       Sciences" for a med-adjacent field) gets nothing.
     - **False positive** — a short substring can fire inside an unrelated word or a passing mention
       that isn't the student's real direction. Read the matched keyword(s) in the `_needs_review` line
       against what the student actually typed, not just whether the word appears somewhere in it.
5. **Course is always present now, so this is a true edge case, not the normal state.** The "Choose
   your desired course" dropdown is a required single-select among the 38 `google_form_notes.md`
   options, so `specific_courses` should always be non-empty. If `_needs_review` ever names "no course
   and no field of study at all," that means the dropdown answer genuinely came back blank (a form
   bug, or a manually-entered legacy row) — contact the student, since there's nothing to search on.
   *(The form no longer asks the old career/values/work-style questions, so `interest_discovery`'s
   free-text fields are always null. The career-backwards branch that used to consume them was dropped
   on 2026-07-25 along with `02_aspirations_intake.md`.)*
6. **Degree level** — nothing to check. No form question sets it; the tool defaults `degree_level` to
   `"undergraduate"` itself at ingest time (every respondent is a pre-university student heading to a
   bachelor's). Only touch it by hand for a genuine exception (e.g. a postgrad-conversion case).
7. **Delete the `_needs_review` key** once any remaining lines are resolved, so the finished
   `profile.json` matches the standard schema shape (no stray keys — compare against the current
   `profile_template()` in `tools/init_student.py`, the source of truth for the shape; note the `needs`
   block is the broad "support & belonging" set, so students from before this shape existed carry a
   now-outdated `needs` shape).
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
- **"Choose your desired course" is a single answer, not a checkbox set.** `specific_courses` comes
  primarily from that one dropdown answer (kept intact, never comma-split — see Section 3 above), plus
  whatever the free-text "specific field of studies" supplement adds. Legacy exports (the old per-area
  grid) still work via the same field — `grid_cols` is just empty on the current form, so the fallback
  never fires.
- **Priority ticks — ties & scale.** The current form is a **3-tier** scale (Must have / Important /
  Nice to have — replaced the 1-8 numeric sliders 2026-09) and ties are *more* likely now, not less
  (only 3 distinct values across 8 categories). The tool orders equal values by the form's column order
  (Cost → Scholarship → University Ranking → Course Ranking → Employability → Recognition → Location →
  Hands-On), deterministic but arbitrary among ties — **sanity-check the ordering** against any
  free-text notes before deriving `weights.json`, since the top band drives the weights, and a 3-tier
  scale means the top band is now much more crowded than it used to be under 1-8. `ranking_importance`
  carries the **raw 3-tier label** ("Must have" / "Important" / "Nice to have") on the current form, not
  a 1-8 number — check the `scoring-weights` skill actually reads it that way before trusting a
  derived `weights.json` for a student ingested through the current form.
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
  - **`degree_level`** — no question, but not a gap: the tool defaults it to `"undergraduate"` at
    ingest (2026-08-29+). Only touch it by hand for a genuine exception the default gets wrong.
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
- **Empty `specific_courses` should no longer happen on the current form** — "Choose your desired
  course" is a required single-select among the 38 `google_form_notes.md` options, so every respondent
  should have at least one entry. If `interest_discovery.decided` still comes back `false` with a
  `_needs_review` line naming this, treat it as a genuine anomaly (a form bug, or a legacy/manual row),
  not the normal path: there's no broad-area fallback to discover within any more (`fields_of_interest`
  is always empty, see Section 3), so Stage 3 would have to discover from scratch off `achievements`/free
  text alone — contact the student instead, since there's genuinely nothing to search on.
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
  - **RESOLVED 2026-09.** The live "final result" dropdown's month-only option text carried NO year at
    all (found 2026-08-23 — 3 respondents all came back with the identical raw string `"January ( Takes
    A2 in Oct/Nov )"`, not a substring-match failure or coincidental blank answers, just a label with no
    year in it). The form now asks a **separate year dropdown** alongside the month one; `map_row()`
    concatenates both raw answers before calling `_normalize_month_year()`. Confirmed working on the
    first real ingest through the new form (2026-09-03): `expected_completion` resolved cleanly to
    `"2027-01"` with no by-hand finalize step needed. A **legacy export with only the month column**
    still hits the old verbatim-passthrough behaviour — check for that shape before assuming every
    student needs the year added by hand.
  - **A dropdown label can name more than one month, and only the first one is the answer.** An older
    live version of this question's options carried a gloss with the year present —
    `August 2027 ( Takes A2 in May/June )` — the case this next behaviour was built for.
    `_normalize_month_year`
    now takes the **earliest** month in the string; it used to scan `_MONTHS` in dict order, reach
    `may` before `aug`, and silently return `2027-05` for an August student (found 2026-08-03, when
    every one of six profiles also had a **null** `expected_completion` — `QUESTION_MAP` had no
    substring matching the live header *"When month does your final result comes out?"*). Two lessons
    that generalise: **an all-null field across every respondent means a broken `QUESTION_MAP` entry,
    not six blank answers** — check the header before you patch profiles by hand; and when the form
    gains a reworded question, grep the real export's headers against `QUESTION_MAP` rather than
    trusting that "light rewording is fine".
- **Scholarship gate.** The current form asks *"Is scholarship a must?"* (Yes/No) → the tool sets
  `scholarship_required` + `scholarship_dependent` directly (`funding_source` stays null here). The old
  *"What scholarships are you planning to apply for?"* free-text question is gone from the form
  (2026-08+), permanently — `scholarship_interests` stays null by design, not a gap (see the finalize
  note above). If the gate column is absent the tool falls back, in order, to the merged *"how will
  you fund this degree?"* question and then the legacy *"how will you pay" + "only if you win a
  scholarship"* pair. A blank/unrecognized fallback answer leaves the gate null → confirm at finalize.
- **`needs` set, and what the current form actually feeds it.** The schema still carries the full
  faith/culture-neutral set (`diet_halal`, `worship_facilities`, `diaspora_community`,
  `disability_accessibility`, `wellbeing_support`, `lgbtq_friendly`, `personal_safety`,
  `climate_weather`, `food_quality`, plus `good_public_transport` / `affordable_cost_of_living`, added
  2026-09), but **the current live form's "Any other perferences?" question only offers 5 of those
  options** (crime→safety, seasons→climate, transport, cost, food) — the sensitive ones (halal, prayer,
  disability, mental-health, LGBT-friendly) don't appear on the form at all right now. Only ticked
  options become `true`; everything else stays `null` (not `false`) — these are PDPA-sensitive, so
  absence ≠ "no need," and on the current form it may just mean "not asked." Spot-check the multi-select
  split, same as countries.
- **Recognition has two tiers now — course-exact-match (trusted) vs free-text keyword-guess
  (flagged).** The dropdown-matched `recognition_targets` come from `COURSE_ACCREDITATION_MAP` — an
  exact lookup against one of the 38 known titles, so there's no "matched a secondary mention"
  ambiguity to second-guess; treat it as settled fact, same as any other dropdown answer. Only targets
  added from the free-text "specific field of studies" supplement carry the old keyword-guess risk
  (matched a passing mention that conflicts with the student's actual chosen course, e.g. "engineering"
  inside an unrelated aside) — those, and only those, get a `_needs_review` line. See finalize step 4
  above for the full false-positive/false-negative rundown on that free-text path.

## Done when

Each requested student has a finalized `profile.json` + `preferences.json` (no `_needs_review` /
`_intake_raw` left), a `status.md`, and is ready for **Stage 3** (`03_discover_longlist.md`).
