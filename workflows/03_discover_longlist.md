# Workflow: Stage 3 — Discover → Longlist (→ master_list.csv)

## Objective

Cast a **wide, cheap** net: find 20-40 plausible university+course candidates across the student's target
countries, score them at snippet level, and land them in `master_list.csv` as **Longlist**. Facts here are
*provisional* — they get verified against official sources in Stage 4. Don't deep-research yet.

## Tools used (in order)

1. `firecrawl_search.py --student <slug>` — discovery: runs search queries, saves results to
   `.tmp/<slug>/search_results.json`. **Costs credits — ask the user before running.**
2. *(agent step)* review results, extract candidates → write `.tmp/<slug>/uni_candidates.json`.
3. `sync_shortlist.py --student <slug>` — scores, dedupes, appends Longlist rows to `master_list.csv`.

## Per-destination query playbook

Generate ~8-15 queries spanning aggregators (for breadth) **and** official course pages (for the real
data). Substitute `<field>`, `<course>`, `<level>`.

**Cross-country (discovery only — never the source of record for a hard fact):**
```
<course> bachelor StudyPortals
QS world university rankings <field>
Times Higher Education <field> subject ranking
best universities for <course> <country>
```

**UK** → UCAS + official entry-requirement pages:
```
<course> UCAS course search
site:ac.uk <course> entry requirements
<course> BSc UK tuition fees international students
UK Graduate Route post study work
```

**USA** → Common App + department + outcomes:
```
<course> Common App universities
<university> <department> admissions requirements international
US News best <field> programs
OPT STEM <field> post study work
```

**Australia** → course catalogs + visa:
```
<course> bachelor Australia university course
QS Australia <field>
Australia 485 graduate visa <field>
<university> international tuition <course>
```

**Singapore/Malaysia (local)** → NUS/NTU/SMU + MQA:
```
NUS OR NTU OR SMU <course> admissions
<course> Malaysia university intake <intake>
MQA recognised programme <course>
```

**China** → English-taught + CSC:
```
<course> English-taught bachelor China university
CSC scholarship <field> bachelor
<university> international admissions <course>
```

## Run discovery

```powershell
python tools/firecrawl_search.py "query one" "query two" --limit 6 --scrape-top 2
```
Or put queries in a JSON list and pass `--queries-file .tmp/<slug>/queries.json`. Use `--scrape-top N` to
pull full markdown for the most promising official course/prospectus pages (those scrape cleanly;
social/forum URLs return "Website Not Supported" — capture the URL + snippet, don't waste a scrape slot).
Results land in `.tmp/<slug>/search_results.json`. **`--student` (or `--out`) is required** — there is no
shared default path, so parallel sessions can't overwrite each other's results.

## Extract candidates (agent judgement)

Read `.tmp/<slug>/search_results.json`. For each plausible university+course, build a candidate object with honest
**0-5 sub-scores** and an **`entry_margin`** judgement, and write the list to
`.tmp/<slug>/uni_candidates.json`:

```json
[
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
    "scholarship_coverage": "",
    "scholarship_competitiveness": "",
    "scholarship_how_to": "",
    "community_links": "",
    "student_life": "",
    "funds_proof": "~GBP 12000 shown for visa",
    "post_study_work": "Graduate Route 2 yrs",
    "recognised_back_home": "MQA recognised; n/a professional body",
    "application_system": "UCAS",
    "key_deadline": "2027-01-15",
    "intake": "2027 Sept",
    "course_url": "https://www.manchester.ac.uk/...",
    "source_authority": "Aggregator",
    "data_as_of": "2026",
    "entry_margin": 0,
    "pathway_option": "INTO Manchester Foundation if below AAA",
    "fits_grades": "",
    "notes": "",
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
]
```

**Field notes:**
- Leave `total_cost_programme` empty to let the tool compute it from `total_tuition` + `est_living_per_year`
  × `duration_years` (in `currency`) and convert to approximate MYR. Put a date in `key_deadline` as
  `YYYY-MM-DD` so it parses (extra text after the date is fine).
- `meets_english`: `true`/`false` (drives the "English short" feasibility flag); `null`/omit if unknown.
- `entry_margin` is your honest read of the student's grades vs the requirement: **+2** well above … **0**
  borderline/meets … **−2** well below. This maps to Reach/Match/Safety. Don't fold it into the sub-scores.
- `source_authority` stays `"Aggregator"` at this stage — Stage 4 flips verified rows to `"Official"`.

**Scoring guide (each 0-5 — these are DESIRABILITY only, never admissibility):**
- `course_match` — how well the course matches the field/goal.
- `subject_reputation` — subject-specific rank + graduate outcomes (not overall vanity rank).
- `total_cost_fit` — full-programme total (MYR) vs the student's budget (lower cost = higher).
- `post_study_work_fit` — visa/post-study-work rights vs `intent_to_migrate`.
- `scholarship_opportunity` — realistic funding this student could actually get.
- `experiential_fit` — hands-on opportunities: projects, research, community involvement, not just exams.
- `location_pref_fit` — matches stated location/lifestyle preferences.
- `recognition_fit` — recognised back home (MQA + professional body) where it matters.

> **Weights are per-student and live in `data/students/<slug>/weights.json`** — never in
> `tools/shortlist_schema.py`, which is shared source that concurrent sessions would fight over.
> Derive them from the student's `preferences.priorities` with the **`scoring-weights` skill** before
> syncing; `sync_shortlist.py` refuses to run without a valid file. Because no student state is shared,
> two students can be discovered and synced **in parallel**. The rich scholarship/community/student-life
> detail columns are usually left blank at discovery and filled during Stage 4.

## Sync to the master list

```powershell
python tools/sync_shortlist.py --student <slug>          # add --dry-run to preview first
```
This computes desirability + A/B/C tier, Reach/Match/Safety, feasibility flags, dedupes by canonical
university+course, and appends new rows as **Longlist**. The CSV is created on first run.

## Edge cases & rules

- **Aim wide** — a Longlist of 20-40 across countries is healthy. Include some safe options, not only
  aspirational ones.
- **Don't over-scrape** — tune `--limit` / `--scrape-top` to control credit use; scraping costs more than
  searching. Only scrape the most promising official pages.
- **Provisional facts** — snippet-level fees/requirements are often wrong or out of date. That's fine here;
  Stage 4 verifies. Keep `source_authority = Aggregator` until then.
- **CSV append needs a trailing newline** — `sync_shortlist.py` appends rows. If the existing
  `master_list.csv` doesn't end in a newline (e.g. it was hand-edited, or renamed from another file), the
  first appended row used to fuse onto the last existing row, corrupting it into one physical line. The tool
  now auto-inserts a separator (`write_rows`/`needs_leading_newline`), but if you hand-edit the CSV, leave a
  trailing newline. Sanity-check after a sync: row count should rise by the "N new" the tool reports.
- **Header / schema column-order drift** — an older `master_list.csv` may carry the same columns
  in a *different order* than the current `SHORTLIST_HEADERS` (e.g. Toru's file had `Approx total (MYR)`
  at index 8, right after Country). `sync_shortlist.py` builds rows in schema order, so appending to a
  drifted file used to misalign every column of the new rows (data intact, but under the wrong headers).
  The tool now reorders appended rows to the *existing file's* header (`reorder_to_header`) and refuses
  if the column *set* differs (a real schema change → migrate first). If you find a drifted file, rewrite
  it once into `SHORTLIST_HEADERS` order (keyed by column name) so it matches the schema and the sibling
  students. Sanity-check after a sync that a spot-checked row's `Approx total (MYR)`/`City`/`Currency`
  line up under their headers.
- **Stale `.tmp/<slug>/uni_candidates.json`** — this file is disposable and may carry leftovers from an
  earlier round (different unis, old scoring). Overwrite it fresh each discovery run rather than appending —
  `sync_shortlist.py` syncs whatever is in it.

## Done when

`master_list.csv` holds a broad Longlist with sensible scores and flags. Then proceed to **Stage 4**
(`04_verify_shortlist.md`) — the first real narrowing cut.
