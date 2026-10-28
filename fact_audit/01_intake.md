# 01. Intake (Stage 1: Google Form → student profile)

*Fact audit, 2026-10-28. Written for Evan (no technical background). Labels: G guess, A advice,
Y yapping, J unlabelled judgment, L loophole. Severity: High reaches a student, Medium could,
Low internal.*

## What this part makes

A student fills in the Google Form. A script (`ingest_form_csv.py`, the "form reader") turns
each answer row into two small data files per student: `profile.json` (who they are: grades,
English, budget, which professional bodies their degree must be recognised by) and
`preferences.json` (what they want: countries, course, how much each priority matters). A second
script (`derive_weights.py`) turns the priority ticks into `weights.json`, the recipe for the
0–100 score every university later gets. Think of it as the intake desk at a clinic: the form is
the patient's questionnaire, the profile is the file the doctors read from then on. Anything the
desk writes down wrongly or fills in by itself, every later stage treats as true. The script
flags doubtful items in a `_needs_review` list (a "check this by hand" sticky note) that Evan
clears before Stage 3.

## Who sees it

- **Students and the public:** the form itself (`forms/intake.json`: intro text, questions,
  consent, disclaimer).
- **Students, indirectly:** nothing from this stage is sent as a file, but its values become
  master-list warnings ("Grades self-predicted", "Over budget", recognition risk), the 0–100 score,
  and report text about campus life, scholarships and English waivers.
- **Evan and helpers only:** `profile.json`, `preferences.json`, `weights.json`, the
  `_needs_review` lines, `workflows/01_intake.md`.

## Findings

| # | Where (file:line) | Quote (≤20 words) | Label | Severity | Why it matters | Suggested fix (one line) | Already in backlog? |
|---|---|---|---|---|---|---|---|
| 1 | tools/ingest_form_csv.py:1108; workflows/01_intake.md:450 | "deterministic but arbitrary among ties" | L | High | The form only has 3–4 tiers for 8 priorities, so ties are normal. Tied priorities are put in form-column order (Cost first, Hands-On last), and `derive_weights.py` turns that order into weights from 0.20 down to 0.05. A student who ticks all 8 "Must have" gets Cost weighted 4× Hands-On, which they never said. This shapes every 0–100 score they see. The workflow says "sanity-check the ordering", but no `_needs_review` line is raised. | Give tied priorities equal weight (score by tier, not by position), or at least raise a `_needs_review` line when ties exist. | new |
| 2 | tools/ingest_form_csv.py:323-324; tools/derive_weights.py:18-19 | "\"doesn't matter\": 0, ... must still rank (last), because derive_weights.py refuses a priorities list missing any" | L | Medium | A category the student ticked "Doesn't matter" still gets a weight of 0.05–0.09 in the score, so something they said they don't care about still moves the score. | Give "Doesn't matter" a weight of 0 and spread the remainder over the others. | new |
| 3 | tools/derive_weights.py:65,25-26; forms/intake.json:222-223 | "\"ranking\": \"subject_reputation\"" … "\"is this even the right course\"" | J | Medium | The student ticks "University Ranking" and "Course Ranking". The first actually weights *subject* reputation, the second weights "is this the right course" (course match). So the score claims to reflect priorities the student answered about something else. | Reword the form rows to name what is really scored ("Subject ranking", "How close the course is to what I want"), or remap. | new |
| 4 | forms/intake.json:261-269; tools/ingest_form_csv.py:218-221 | "What's your limit (RM) for the whole degree" — options "500,000" / "1,000,000" / "1,500,000" | G | High | The lowest option is RM 500,000. A family whose real limit is RM 150,000 must pick 500,000, which is saved as their ceiling. Rows costing up to RM 500k then show **no** "Over budget" warning, so the list tells them a course is affordable when it isn't. Most Malaysian private-uni degrees sit far below this floor. | Add lower options (e.g. 100k / 250k) or a "less than 500,000" choice that raises a `_needs_review` line asking for the figure. | new |
| 5 | tools/ingest_form_csv.py:789-793; forms/intake.json:56-63; tools/shortlist_schema.py:519 | "if grade_status.startswith(\"actual\") … elif grade_status.startswith(\"predict\")" — form option "Forecast Grades" | G | High | The live form's choice is "Forecast Grades" (usually school-issued), but the reader only knows "actual" and "predict…", so every forecast student stays `expected` (self-guessed). Every row on their list then carries the warning "Grades self-predicted", which states something about the student that they didn't say. | Map "forecast" to `predicted`, or reword the warning to "Grades not final yet". | new |
| 6 | forms/intake.json:68-70; tools/ingest_form_csv.py:415-420 | "\"type\": \"CHECKBOX_GRID\"", "\"required\": false" | L | Medium | The grade grid lets a student tick several grades for one subject and lets them skip it entirely. The reader saves a multi-grade cell as-is and raises no flag; an empty grid gives no grades and no flag. Later stages then judge "Well above / below" entry bars from an unclear or missing grade. | Make it a one-choice-per-row grid, and raise a `_needs_review` line for an empty grid or a cell with two grades. | new |
| 7 | tools/init_student.py:53; workflows/01_intake.md:68-73 | "type is a permanent default (no question asks it)" … "the tool will not catch it" | G | Medium | Every student is recorded as doing A-Levels without being asked. A Foundation, STPM or IB student gets checked against A-Level entry requirements, and nothing flags it. | Ask the pre-university qualification on the form, or raise a `_needs_review` line until someone confirms it. | new |
| 8 | workflows/01_intake.md:579-581; tools/ingest_form_csv.py:578-582 | "treat it as settled fact, same as any other dropdown answer" / "\"Public Health & Nutrition\": [\"MQA\", \"MAHPC\"]" | G | Medium | The course-to-professional-body list was checked once (2026-09), stores no source link, and is never re-checked for each student. Combined options get bodies the student may not need: Public Health gets the allied-health board, though the code's own comment says "general public health alone is not" regulated; Architecture gets both architect and quantity-surveyor boards. These turn into "recognition risk" warnings on the student's list. | Store the source link and date for each body; for combined options, raise a `_needs_review` line asking which profession the student means. | new (related: I9) |
| 9 | tools/ingest_form_csv.py:604-608; tools/fetch_form_questions.py:186-188,227 | "Returns [] for a non-regulated field, an unrecognised title … or a blank answer" | L | Medium | If a course title on the form is renamed (it has happened twice), a regulated course like Medicine quietly gets an empty list, which reads exactly like "no licence needed", and the recognition gate disappears. `--check` lists it, but only if someone runs it, and it still exits as "ok". The form reader itself raises nothing. | In the form reader, a course title missing from the list should add a `_needs_review` line; make `--check` fail on it. | new |
| 10 | tools/ingest_form_csv.py:468-470; forms/intake.json:304-306 | "\"weather\": \"climate_weather\", \"season\": \"climate_weather\"" — options "Cold Weather", "Summer Weather", "4 seasons" | G | Medium | Three opposite answers all become the same `climate_weather: true`. Whoever writes the campus-life section has to guess whether the student wants cold or hot. `--check` passes it because each option matches some keyword. | Save the ticked labels word for word (or use separate keys) so the writer reads what the student chose. | new |
| 11 | tools/ingest_form_csv.py:443,448-451; forms/intake.json:309; workflows/01_intake.md:142-145 | "Halal food and Prayer facilities were added as ticks 2026-10-25" — live option "Muslim Facilities/Halal Food" | L | Low | The live form has one combined tick. It sets halal food only. "Muslim Facilities" (prayer space) matches no keyword, so it is lost, and the workflow wrongly says there are two ticks. This is missing information rather than a guess. | Add "muslim" to the prayer keywords and correct the workflow note. | new |
| 12 | forms/intake.json:285,298 | "Location preferences" … "\"required\": true"; "Any other perferences?" … "\"required\": true" | G | Medium | Both checkbox questions are compulsory and have no "No preference" choice, so a student with no preference has to tick something. That forced tick is saved as a real need and feeds the location score and the campus-life text. | Make both optional or add a "No preference" option. | new |
| 13 | workflows/01_intake.md:365-366; forms/intake.json:18-25 | "a non-Bumiputra student can't claim Bumiputra-only scholarships" — options Chinese / Malay / Indian / Other | G | Medium | The form asks race, not Bumiputera status, so the helper must work out eligibility for itself. A Sabah or Sarawak native who picks "Other" could be wrongly ruled out of Bumiputera-only funds, or a student wrongly ruled in. | Ask "Are you Bumiputera?" (Yes / No / Not sure) directly, or tell helpers to state the fund's rule and not decide eligibility. | new |
| 14 | workflows/01_intake.md:156-157 | "a waiver needing N years is \"likely\" only when the floor ≥ N" | L | Medium | Tells the helper to describe an English-test waiver as "likely", a hedged guess word, in student text. A floor of years can only say "meets the stated rule" or "can't tell". | Replace "likely" with "meets the stated N-year rule"; otherwise state the rule and let the student count. | related: R21 |
| 15 | workflows/01_intake.md:494-495 | "Judge subject standing from `ranking_importance` instead." | L | Low | Tells the helper to work out a subject-ranking preference from the *University* Ranking tick, which the same file says (line 228-233) nothing should read. That invites a made-up preference. | Delete the sentence; leave `min_subject_rank_pref` null. | new |
| 16 | tools/ingest_form_csv.py:1039-1040; workflows/01_intake.md:211-212 | "always resolves to the literal string **\"Flexible\"** (never `null`)" | G | Low | The student is never asked when they want to start, but the profile records "Flexible" as if it were their answer. Today it only picks which application round to research. | Store `null` with a note "not asked", and treat null as "research all intakes". | new |
| 17 | workflows/01_intake.md:473; tools/ingest_form_csv.py:838 | "*(blank)* \| `null` \| Ask the student for a figure at finalize" | L | Low | The workflow promises a blank budget gets chased, but the reader only flags a budget that is filled in and can't be read. A blank (old or hand-entered rows) quietly becomes "no limit", so the student sees no "Over budget" warnings at all. | Add a `_needs_review` line when the budget answer is blank. | related: I3 |
| 18 | forms/intake.json:4,7 | "Hihi! … your data is safe with me, i will be using them to research universities suitable to your preference.🤩🥰" | Y | High | First thing every student and parent reads. It is chatty, promises "suitable" (a fit promise the copy rules ban), and "safe with me" clashes with the consent text, which says data goes to AI tools and overseas servers. The page title "Fill up these quick questions and ur done!" is chatty too (2 instances). | One plain line: what the form is for, roughly how long it takes, and "how we use your data: see the last page". | new |

## What is already solid

- **No made-up numbers for budget or dates.** A budget that can't be read becomes `null` with a
  `_needs_review` line (`ingest_form_csv.py:835-842`), never a guessed figure, and a date that
  isn't a clean month and year is kept word for word (`_normalize_month_year`).
- **Needs stay `null`, not "no".** Unticked or never-asked needs stay `null`
  (`init_student.py:77-78`), so "not asked" is never stored as "doesn't need it".
- **Free-text course matching is flagged.** Professional bodies guessed from the student's own
  typed field of study always raise a `_needs_review` line (`ingest_form_csv.py:926-931`).
  Unsupported countries are recorded and flagged, not dropped silently (`:965-973`).
- **Lesson language is a cautious floor.** "DLP" and "Not sure" give `null` ("can't tell"),
  never an assumed waiver (`ingest_form_csv.py:274-281`). An "Other" answer gets a review line.
- **`derive_weights.py` refuses to guess.** It stops with an error on an incomplete priority list
  (`:93-98`) and writes a plain rationale of every rule it applied into `weights.json`. The
  scholarship override and course-match floor are named in that rationale.
- **The form is honest about itself.** The race question says why it is asked, the priority grid
  says "Will be used to score each university for you", and the closing disclaimer says reports
  are "research … not a guarantee" and to confirm fees and deadlines on the official site (the
  one piece of advice on the form, and the right one to keep).

## Counts

G: 8 · A: 0 · Y: 1 · J: 1 · L: 8 · Total: 18 (High 4, Medium 10, Low 4)
