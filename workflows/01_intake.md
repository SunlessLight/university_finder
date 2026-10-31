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

**Two forms since 2026-10-30.** The **list form** (RM 50, `forms/intake.json`, most of this file) and
the **report form** (RM 30, one university, `forms/report_intake.json`): a cut-down copy read by the
same tool. See "The report form" below. Each buyer gets the form for what they bought; a buyer of
both gets both links.

> **Stage 1 and Stage 2 were merged on 2026-07-25.** The form asks who-you-are and what-you-want in
> one sitting, so the old `01_student_intake.md` / `02_aspirations_intake.md` conversational SOPs were
> deleted. Stages 3-5 keep their file numbers — **there is no Stage 2**.

## The Google Form (build once)

Turn **"Collect email addresses" ON** (Settings → Responses) on both forms, and keep the questions
below. Question **wording** maps to CSV column headers; the tool matches columns by a
distinctive **substring** (see `QUESTION_MAP` in `tools/ingest_form_csv.py`), so light rewording is
fine — but keep the substring in bold intact.

**Section 0 — Consent & identity (required)**
- **"Collect email addresses" turned ON.** 
- **Consent** (formal PDPA notice, live 2026-10-26, on its own last page): title *"Consent to use your
  information / Persetujuan penggunaan maklumat anda (PDPA)"*, one required option *"I agree to
  Shortlisted collecting and using my answers as described above, including my race and any halal or
  prayer preferences. / Saya bersetuju …"*. The bilingual notice in the description names Evan, his
  contact email, and **3-month** retention after the last contact (full text: `forms/intake.json`).
  Keep "consent" in the title (how the program finds it) and out of every other title; the option must
  not start with "N" (read as an explicit No). `fetch_form_questions.py --check` tests all three.
  *(**What the gate actually does**, checked against a real export: a Forms checkbox exports its own
  label text, so a ticked box lands a non-empty cell like `I agree to Shortlisted collecting…` —
  `_yes()` can't read that as yes or no and returns `None`, and the row passes on the cell simply
  being **non-empty**. So a ticked checkbox needs **no** `--assume-consent`. What still skips a row:
  an **empty** consent cell (box not ticked) unless you pass `--assume-consent`, and an answer whose
  text starts with "n" — the explicit-No case, which no flag overrides.)*

**Section 1 — About you → `profile.json`**
- **Full Name (As in IC)**; **Race/ethnicity**.
  - **The name question.** "Nickname" replaced "Full name" in 2026-08 (identity protection), and the
    live title went back to *"Full Name (As in IC)"* on 2026-10-30. `QUESTION_MAP` maps both onto the
    `name` logical key, so the slug path is the same. Older profiles hold nicknames, some
    gamertag-style (`GwakGwak3000`); that's expected. Since 2026-10-30 both consent notices say full
    name too.
  - **Age, Gender, Nationality, and "where you live in now" are gone (2026-08+), permanently.**
    None of them ever had a downstream read path — no tool, no agent prompt anywhere in the
    pipeline consumed them — so they were cut as pure friction. `profile_template()` no longer
    carries these keys at all; don't reintroduce them without wiring a real consumer first.
  - **Race/ethnicity → `profile.ethnicity`** (PDPA-sensitive). Captured because it drives
    **scholarship eligibility** in Malaysia (e.g. Bumiputra-only vs open funds) — the agent uses it as a
    research signal in Stage 3/4. It is **never** a desirability-score input. **"Prefer not to say"**
    (added 2026-10-30) means unknown: don't assume eligibility either way.
  - **The respondent's email is the identity key.** The tool writes it to
    **`profile.contact_email`** (structured, added 2026-09-23) *and* keeps the legacy
    `Contact: <email>` line in `profile.notes`. The structured field is what the re-submission guard
    in step 2 matches on; the notes line is the fallback for profiles ingested before that date.
    PDPA-sensitive, same class as the rest of the data bank — it stays under gitignored
    `data/students/`.
  - **`home_country` always stays "Malaysia".** The tool never overwrites it. *(A legacy form asked
    "where do you want to **live and work after** graduating"; the current form dropped it, and
    `intent_to_migrate` comes from the "work abroad" question in Section 2 instead. If you ever
    re-add it, it is a post-study **aspiration** → `notes` + `intent_to_migrate`, never `home_country`.)*

**Section 2 — Your studies, money & recognition → `profile.json`**
- **Which pre-university programme are you doing?** (added 2026-10-30): A-levels / STPM / UEC / IB /
  foundation / Matriculation / Diploma. → `current_program.type`, spelling unified by
  `PROGRAM_NORMALIZE` (an "Other" answer stays verbatim). A blank keeps the `"A-Level"` default, so
  rows from before this question are unchanged. `build_list_pdf.py` prints it; `check_grades.py`
  picks its scale from it; row-fillers compare against the bar published for it.
- **What month does your actual result come out?** January to December, and **What year does your
  actual results come out?** 2026 / 2027 / 2028 (both forms; the year came back 2026-10-30).
  `map_row()` concatenates the two before `_normalize_month_year` (`YYYY-MM`). A month with no year
  is kept verbatim and raises a `_needs_review` line. An answer it can't read is kept verbatim, never guessed. On the old rows, the year sits
  in the column now headed "What month…" of the old spreadsheet (see "Edge cases" below).
- **Subjects & grades: one free-text box (2026-10-30; replaces the grade grid for everyone).** *"Type
  you subject and grades (eg. physic A, Chemistry B, etc)"* (sic; `QUESTION_MAP` also matches the
  tidied wording) → `_intake_raw.grades`. AI tidies it at finalize and `check_grades.py` checks the
  tidy-up (step 1 of "Finalize"). The report form's box is worded *"List down the subject and grades
  (eg Physic A, Chemistry B, etc)"*. An export that still has the old grid columns goes through
  `_subject_grid_columns()` / `_build_subjects_from_grid()` as before; the student's own
  `grade_status` question then sets the status.
- **what are you applying with?** (Forecast Grades / Actual Grades) → `grade_status` `predicted` /
  `actual`. *(Older wording: "Are you applying with forecast result or actual?")*
- **English proficiency — two SEPARATE questions now, watch the substring collision.** **"English Test
  Taken"** (IELTS / TOEFL / Cambridge English Test / **None** / Other) and **"If English test
  taken, what's the score? ( leave blank if haven't )"**. The second header's text literally *contains*
  the first header's matching substring (`"english test taken"`), so `QUESTION_MAP`'s entry for
  `english_score` (`"what's the score"`) **must be listed before** the entry for `english_test`
  (`"english test taken"`) — `build_col_index()` takes the first list match per header, so the wrong
  order silently steals the score question's match and drops the score entirely. Keep this cautionary
  note if either header is reworded again. *Do NOT ask "when will you take it"* — each university sets
  its own bar; that's a research-stage fact, not an intake one.
- **Total budget** for the whole degree — a **dropdown of limits**, not free text (reworded
  2026-10-27, backlog I11): *"What's your limit (RM) for the whole degree. (include tuition, living
  cost, etc)"* → **`100,000`** / **`200,000`** / **`500,000`** / **`1,000,000`** / **`1,500,000`**. No
  "Not sure" option. `BUDGET_LIMIT_EXACT` matches them exactly (commas/spaces ignored) **before** the
  substring list, because `500,000` is inside `1,500,000`. Keep labels plain numbers: any label with
  "under" reads as RM 500,000. All are real ceilings, so a student who could
  pay more than RM 1.5M gets "Over budget" on rows above it (Evan accepted: budget is secondary). The
  title must keep "whole degree" or "total budget". Older exports' bands (`< 500000` / `500000-1000000`
  / `>1000000` = null floor / legacy "Not sure" = null) still go through `BUDGET_BAND_NORMALIZE`. The
  **verbatim label** goes to `financial.notes` and the **number**
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
  lifestyle checklist: **Low crime rate** (→ `needs.personal_safety`) / **Malaysian Community nearby**
  (→ `needs.diaspora_community`) / **4 seasons** (→ `needs.climate_weather`) / **Good public transport**
  (→ `needs.good_public_transport`, new) / **Affordable living cost** (→
  `needs.affordable_cost_of_living`, new) / **Good food** (→ `needs.food_quality`). **Confirmed present
  on the live form 2026-09-09** (two real respondents both ticked it, correctly landing on
  `diaspora_community` via the `NEEDS_NORMALIZE` "community"/"malaysian" match) — this corrects an
  earlier note in this file that claimed it had been dropped; that was stale, not the code. **Halal
  food and Prayer facilities were added as ticks 2026-10-25** (→ `needs.diet_halal` /
  `needs.worship_facilities` via the existing `NEEDS_NORMALIZE` "halal"/"prayer" keys; no code
  change). Responses before that date were never asked, so their `null` means "not asked", not "no
  need". **Since 2026-10-30:** the live tick is one option, "Muslim Facilities/Halal Food", and it sets
  both flags (`NEEDS_NORMALIZE` "muslim"). A report mentions halal or prayer only when one is set
  (`04_university_report.md`), so a miss here hides it. The exact ticks are kept in
  `preferences.other_preferences`, because `needs` merges them. **The live ticks (2026-10-30, both
  forms):** Stay close to family / Low crime rate / Malaysian Community nearby / Cold Weather / Summer
  Weather / 4 seasons / Good public transport / Affordable living cost / Muslim Facilities/Halal Food,
  plus Other. "Good food" is no longer an option. **Still not on the form:**
  disability/accessibility, mental-health/wellbeing support, LGBT-friendly — their `needs` keys stay
  `null` = "not asked".
- **Lesson-language question (added to the live form 2026-10-25, backlog S9):** "What language were
  most of your lessons (maths, science, etc.) taught in? Not your English class." Six options, from
  "English, all through secondary school and pre-university" to "Not sure", plus Other (labels:
  `forms/intake.json`). → **`english_proficiency.lesson_language`**, verbatim (mapped 2026-10-27), and
  **`english_proficiency.years_in_english_min`**, the floor of years taught in English
  (`LESSON_LANGUAGE_YEARS` in `ingest_form_csv.py`, 2026-10-27): all through = 5, pre-university
  only = 1, Mostly Malay / Chinese = 0, DLP / Not sure = `null` (can't tell; never assume a waiver).
  An "Other" answer is `null` plus a `_needs_review` line: at finalize, set a whole number only if the
  answer clearly supports it, else leave `null`. It is a floor, so a waiver needing N years is
  "likely" only when the floor ≥ N; below N or `null`, state the rule and let the student count.
- **"What did you take for ur secondary school?"** (IGCSE / SPM / UEC / O-Level) → **`secondary_qualification`**,
  verbatim (mapped 2026-10-27). Nothing reads it automatically yet; it is context for the English-waiver
  call and for entry requirements that name SPM or IGCSE.
- **"Achievements / activities you'd want to write about in your application?"** (optional, new
  2026-08; report form only since 2026-10-30, see O12 in `plans/additionals.md`) →
  `profile.achievements`, free text. This exists specifically so Stage 4's "Who actually
  gets in" section and the application-prep guide can compare the student's real activities against
  what admitted applicants are shown to have, instead of only generic "here's what unis look for" text
  — the concrete need that prompted this: a student explicitly asked "what traits are universities
  looking for in my application, and do I match?"

**Section 3 — What you want → `preferences.json`**
- **Which countries** would you consider — checkboxes (UK / Australia / USA / **Singapore** /
  **Malaysia** / China / Japan / Hong Kong / Taiwan / Germany — **10** supported destinations;
  `COUNTRY_NORMALIZE` in
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
- **"When do you want to start" is gone from the list form (2026-08+), permanently** (the report form
  asks "Which year do you want to start?"). The reasoning: the
  student should decide their intake based on the university research, not the other way around.
  `preferences.intake` therefore always resolves to the literal string **`"Flexible"`** (never `null`)
  via `_normalize_intake()`'s blank-input default — this is intentional, not a gap. *(No separate
  "degree level" question → the tool defaults `degree_level` to `"undergraduate"` automatically, 2026-08-29+;
  see item 6 below.)*
- **"Tick the importance of each topic below"** (both forms) — **eight per-category questions, a
  4-level scale now (replaced the 1-8 numeric sliders 2026-09)**: **Must have** / **Important** /
  **Nice to have** / **Doesn't matter**, one
  each for: **Affordable Cost / Scholarship availability / University Ranking / Course Ranking /
  Employability / Recognition back home / Location / Hands-On Experience** (category wording also
  lightly reworded — e.g. "Cost"→"Affordable Cost" — but the substrings `QUESTION_MAP` matches on
  still hit). The tool detects them by the shared *"tick the importance"* marker (the legacy *"rank
  your priorities"* marker still works too, so an older export still parses) + the bracketed category,
  normalises the tier to a number via `TICK_IMPORTANCE_NORMALIZE` (3/2/1/0), keeps it in
  `preferences.priority_levels`, then orders the categories
  by that value (highest first, ties broken by the form's column order) into `preferences.priorities`.
  This still gives a full 8-way ranking including **Course Ranking** (`course_quality` → `course_match`).
  **It must stay a Multiple choice grid** (one tick per row, since 2026-10-30). A checkbox grid
  lets a student tick two levels on one row ("Must have, Important"); the higher one then counts, with
  a `_needs_review` line, because a missing token stops `derive_weights.py`. `--check` flags that.
  *(Legacy forms with **#1/#2/#3 priority** dropdowns still work — the tool falls back automatically
  when neither marker is present.)*
- **`ranking_importance`** is kept for reference only. It holds the **[University Ranking]** tick
  answer verbatim — a **3-tier label** on the current form ("Must have" / "Important" / "Nice to
  have"), a **1-8** number on older records — or the answer to a dedicated *"how much does your
  subject's strength matter"* question if the form has one. Nothing in scoring reads it:
  `tools/derive_weights.py` builds `weights.json` from `preferences.priority_levels`, or from the
  `preferences.priorities` order on profiles from before the tick points.
- Do you want to **work abroad** after graduating — Yes / No / Unsure. → `intent_to_migrate` (and the
  raw answer into `post_study_work_importance`).
- **Dealbreakers is gone from the live form (2026-09), permanently.** It used to be its own optional
  question (`preferences.deal_breakers`); it's now folded into "Any other perferences?" above (→
  `needs`), so `deal_breakers` stays an empty list on the current form by design, not a gap.
  **Location preferences** (required dropdown: "Urban / City" / "Rural / Campus-based") is still its
  own separate question → `preferences.location_prefs`. A "No preference" answer, if that option is
  added, becomes an empty list so it doesn't steer the location score.
- **Preferred universities** — ✅ **wired (2026-08+).** *"Universities you already have in mind ( if
  any )? Can write more than 1."* → `preferences.preferred_universities`, free text (answers use
  "and" between names, not commas — don't split it into a list). A student naming unis they already
  care about is no longer silently ignored: since 2026-10-13 Stage 3's roster sweep reads this field
  and puts each named university in the country being researched on the roster
  (`03_discover_longlist.md` → Step 1). Before that date it was saved here and read by nothing.
- **Additional requirements is gone from the live form (2026-09), permanently.** The old *"Is there any
  specific information you want to know about universities..."* free-text question — the one that
  originally prompted this whole redesign, feeding Stage 4 §3 ("Who actually gets in") and §13
  (application-prep checklist) — has been folded into "Any other perferences?" above (→ `needs`), same
  as dealbreakers. `preferences.additional_requirements` stays null on the current form by design.
  Confirm with Evan whether the Stage 4 §3/§13 use case still has a source now that its dedicated
  question is gone, or whether it needs pulling from `needs`/`achievements` instead.

## How to run

Four commands, in this order. Steps 1-3 are safe to repeat; step 4 is the one that changes the sheet.

0. **After any form edit, check the live questions first** (read-only):
   ```powershell
   python tools/fetch_form_questions.py --check   # saves forms/intake.json, checks it against this tool's maps
   ```
   Prints every unmapped title or option (budget ceilings shown per option) and exits 1 on a broken
   consent question. `git diff forms/` shows what changed on the form. Fix `ingest_form_csv.py` or the
   form *before* the first student answers the new version.

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
   - **A re-submission by an existing email is skipped, and the skip names the existing slug** —
     e.g. `email already belongs to student 'ng-kai-wang' (already on disk) — likely a re-submission`.
     The slug comes from the **nickname**, so a returning student who retypes it ("Ng Kai Wang" →
     "NgKW") used to sail past both slug checks and silently earn a second folder (hit for real
     2026-09-23). Matching is on `profile.contact_email`, case-insensitive, falling back to the
     `Contact:` line in `notes` for older profiles; students with no email recorded never match,
     which is correct. It **skips, never overwrites** — the existing folder holds the research.
     `--force` overrides the on-disk match, but it also disables the folder-exists guard for the
     whole run, so prefer fixing the row. The guard separately catches two rows sharing an email
     **inside one CSV**; `--force` does *not* override that one (same as the duplicate-slug check —
     the second row would clobber a folder the same run just wrote).
   - **Testing the form with your own email can trip this.** A list row and a report row from one
     address count as one buyer. Use a plus-address (`you+test3@gmail.com`) for test rows — Gmail
     delivers it to the same inbox but it is a distinct identity to the guard.
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

- **Old answers (2026-10-31).** The list form now writes to "List Intake Form (Responses)", which
  started empty. That file also holds the Apps Script since 31 Oct, so never delete it. The old sheet,
  "List Intake (Responses)", is gone. Only its tab `Form Responses 2` is saved, in `data/form/`, with
  no `Ingested at` stamps. Anyone whose old answers are needed fills the form again. If they already
  have a folder, that row is skipped and the folder stays as it is, so change a kept profile by
  hand. The tools find a form's sheet through `FORM_ID_LIST_INTAKE`, so
  re-linking a form moves nothing. That value is the form's ID: anything else gives `Invalid ID` or
  `No item with the given ID`.
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

## The report form (one report, no list)

A report buyer answers the shorter form (`forms/report_intake.json`) and gets a small student folder,
because their grades are personal data and `data/quick_reports/` is not for that: two buyers of one
university would also overwrite each other there. There is no sheet-stamping step for this form.

```powershell
python tools/fetch_form_answers.py --form report_intake                 # data/form/report_answers.csv
python tools/ingest_form_csv.py "data/form/report_answers.csv" --dry-run
python tools/ingest_form_csv.py "data/form/report_answers.csv"
```

- A row that answers *"Which University do you want a report of?"* adds one entry to
  `profile.report_orders` (university, course, start year, the student's `question`, submitted).
- **A buyer who already has a folder keeps it untouched, apart from the new order**, even with
  `--force`. The folder is found by email, then by name if the email agrees. A same-name folder with a
  different email is skipped and named in the summary; settle it by hand. Re-reading the same answers
  adds nothing, so the whole CSV is safe to re-run.
- The form also asks budget, race, preferences and the importance grid (2026-10-30, so the report can
  compare cost with their limit, say which funds they can apply for, and write to their ticks and
  priorities). Unlike the list form it has no countries and no "Is scholarship a must?".
- New folders have blank countries by design. Finalize the grades as step 1
  below; the other steps mostly have nothing to do. Then dispatch `report-writer` with the slug (the
  "Report order" section of `.claude/agents/report-writer.md`), one per order.
- **A buyer of both who fills the report form first:** the list row is skipped, because `--force`
  would wipe the order. Copy the list answers in by hand: run that row alone through a temporary
  folder, then copy its `preferences.json` fields and missing profile fields across, keeping
  `report_orders` and any tidied `subjects[]`. List form first needs nothing special.
- `progress_dashboard.py` shows these students as **Report order**, not stuck at Stage 1.

## Finalize each student (the judgment layer — this is your job, not the tool's)

**Most of this stage is deterministic and needs no per-student review.** Ethnicity, the scholarship
gate, degree level, and recognition_targets matched off the "Choose your desired course" dropdown are
all filled straight from clean form answers or an exact lookup against a closed, known set. What's left
per student is whatever the tool flagged in `profile.json`'s **`_needs_review`** (normally the
free-text grades, the result year, sometimes a free-text recognition match):

1. **Grades** — the one manual step on every form.
   1. Tidy `_intake_raw.grades` into `subjects[]`, one `{"subject", "grade_or_predicted"}` per subject,
      keeping the student's grades exactly. Subject names follow `SUBJECT_NORMALIZE`. Don't delete
      `_intake_raw` yet.
   2. Run `python tools/check_grades.py --student <slug>`. It fails a grade impossible for
      `current_program.type`, or a tidied list shorter than the raw text appears to name (read that
      one against the raw text: a subject with "and" in its name counts as two). Fix the tidy-up, not
      the check. "Other" has no scale, so read those by hand.
   3. Show Evan raw vs tidied (the tool prints both), a 30-second look.
   4. Update the tally in R41 of `plans/additionals.md`: +1 if nothing needed correcting, back to 0 if
      something did. At 20 in a row the look can stop (backlog R41).
   5. Delete `_intake_raw`.

   `grade_status` comes from the "what are you applying with" question. If it's blank (the report form
   allows "Not sure"), ask the student. `sync_shortlist.py` surfaces `expected` as a "Grades unverified
   (self-predicted)" warning once the student reaches the master list.
2. **Ethnicity** — nothing to check, just a fact to carry forward. `profile.ethnicity` is a clean
   pass-through of one dropdown answer, captured for **scholarship-eligibility** research. When you
   research scholarships in Stage 3/4, use it to include/exclude ethnicity-gated funds (e.g. a
   non-Bumiputra student can't claim Bumiputra-only scholarships). Never let it touch the desirability
   score.
3. **Scholarship** — nothing to check. `scholarship_required` comes straight from the clean "Is
   scholarship a must?" Yes/No gate. `scholarship_interests` stays null by design (its question was
   dropped from the form) — Stage 3/4 already researches every available scholarship for every
   finalist regardless (per `04_university_report.md` §11), so treat `scholarship_required = true` alone
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
  results, so the longlist surfaces it automatically: `sync_shortlist.py` adds a **"Grades
  self-predicted"** warning to every row. Admission likelihood is still computed (the list stays
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
  scale means the top band is now much more crowded than it used to be under 1-8. (`ranking_importance`
  is not part of this — it is kept for reference only and weight derivation does not read it.)
- **Unsupported target countries are reported, not dropped.** A picked country outside the **10**
  supported destinations (UK / Australia / USA / Singapore / Malaysia / China / Japan / Hong Kong /
  **Taiwan** / **Germany**, both added 2026-09-23) — e.g. **Canada** — is left out of `target_countries` but recorded in a `_needs_review`
  line **and** `preferences.notes`, so nothing is lost silently. Decide with the student whether to
  research it out-of-band. (`SUPPORTED_DESTINATIONS` in `tools/ingest_form_csv.py` renders that message,
  so the count never drifts from `COUNTRY_NORMALIZE`.)
- **Budget bands, and what each one means downstream.** The form's dropdown removed the
  whole class of budget-parsing problems (see the two retired edge cases in the note below). What lands
  where (live labels from 2026-10-27; older exports below them):

  | Form answer | `total_budget` + `total_budget_ceiling` | Meaning |
  |---|---|---|
  | `100,000` | `100000` | Real ceiling — cost checks apply |
  | `200,000` | `200000` | Real ceiling |
  | `500,000` | `500000` | Real ceiling |
  | `1,000,000` | `1000000` | Real ceiling |
  | `1,500,000` | `1500000` | Real ceiling, even for a family that could pay more |
  | `< 500000` (pre-2026-10-27) | `500000` | Real ceiling |
  | `500000-1000000` (pre-2026-10-27) | `1000000` | Real ceiling — top of the band |
  | `>1000000` (pre-2026-10-27) | `null` | A **floor**, not a ceiling: no "Over budget" flag |
  | `Not sure - no fixed budget` (legacy exports only) | `null` | "Research everything, I'll decide" |
  | *(blank)* | `null` | Ask the student for a figure at finalize |

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

  `grade_status` is set from the "what are you applying with" question; older grid rows start at
  `expected` (see the provisional grades note above).
- **A question replaced on the form keeps its old sheet column.** The new one is added further right,
  so one logical key can have two columns (old + new consent, month, applying-with).
  `merge_duplicate_columns()` counts an answer in either. Without it, `build_col_index()` reads only the
  first column, and every new respondent looks blank there: a blank consent skips them. Found
  2026-10-30, before any new student was lost.
- **No consent / no name** → row skipped (reported in the summary). This is the PDPA gate — respect it.
- **Duplicate names** → same slug; the second is skipped rather than clobbering the first. Disambiguate
  the name (or `--force` deliberately) if two real people share a name.
- **Same person, different nickname** → caught by the email guard (step 2), not by the slug checks.
  The row is skipped and the message names the existing slug, so there is no longer any need to grep
  the roster for the email by hand before finalizing. Deciding what a re-submission's *updated* facts
  (new grades, a changed budget) should do to the existing student is still a conversation — the tool
  only stops the silent second folder, it never merges.
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
  2026-09), but **the current live form's "Any other perferences?" question offers 8 of those
  options** (crime→safety, community→diaspora, seasons→climate, transport, cost, food — confirmed
  2026-09-09 against two real respondents — plus halal→`diet_halal` and prayer→`worship_facilities`,
  added 2026-10-25). The remaining sensitive ones (family, disability, mental-health, LGBT-friendly)
  don't appear on the form at all right now. Only ticked options become `true`;
  everything else stays `null` (not `false`) — these are PDPA-sensitive, so absence ≠ "no need," and on
  the current form it may just mean "not asked." Spot-check the multi-select split, same as countries.
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
