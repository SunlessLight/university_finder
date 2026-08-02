# Workflow: Stage 3 — Discover → Longlist (→ master_list.csv)

## Objective

Produce, for **ONE country per session**, 8-12 university+course rows in `master_list.csv` with **all 35
columns filled from official sources**. Every row is a **Longlist** row the student can cut on at a
glance; Stage 4 no longer re-verifies it, it only writes reports on the survivors.

> **The master list is the PRODUCT.** The client receives it as a spreadsheet, so a blank cell reads as
> breakage, not as work-in-progress (established 2026-07-29, after an audit of all 8 student CSVs found
> `Course at a glance` filled on 1 of 44 rows for one student and 24 of 24 for another — the workflow
> itself used to say "leave it for Stage 4"). Completeness is now enforced in code twice:
> `merge_candidates.py` before the CSV, `check_master_list.py` after it.
>
> **Completeness must never become invention.** The counterweight is `SENTINEL_VALUES` in
> `tools/shortlist_schema.py`: the honest ways to say there is no answer — `Rolling` /
> `Not published — check portal` for a deadline, `Not ranked` for a rank a university genuinely
> doesn't hold, `No statistics published` for scholarship odds, `Not published` for a grade bar,
> `None` for clean warnings. A sentinel is for *"there is no answer"*, never for *"I didn't find it"* —
> if the fact exists and you couldn't reach it, say so in `notes`.

> **The longlist is a SCANNING surface, not a report.** A row carries only what the student needs in
> order to **cut** — enough to say "keep looking at this one" or "drop it" at a glance in Google Sheets.
> Anything that needs a paragraph belongs somewhere else: the long-form research goes to
> `research_notes.md` now, and the real depth goes into the Stage-4 **university report**
> (`04_university_report.md`), which is the document the student actually reads to *decide*. Cell
> length budgets enforce this in code — see the readability rules below.

## Tools used (in order)

**One country per session.** Do not run two in one pass — that is what keeps this session's context
small enough to research 35 columns a row, and it's now a hard gate (`--country` on both tools).

```
0. Pick the country      — from the files, never ask. See "Pick the next country".
1. Roster sweep          — free WebSearch, 6-10 queries -> 8-12 rows of
                           university + course + city + course URL ONLY.
2. Country constants     — researched ONCE, reused by every row: visa money, work
                           rights, how to apply, intake, living benchmark, ranks.
                           -> .tmp/<slug>/country_<code>.json
3. Row fill              — PARALLEL row-filler subagents, one per university.
                           -> .tmp/<slug>/candidates/<uni-slug>.json
4. python tools/merge_candidates.py --student <slug> --country "<Country>"
                           merges the fragments; HARD-ERRORS naming every gap.
5. python tools/sync_shortlist.py --student <slug> --country "<Country>"
                           scores, dedupes, appends Longlist rows.
6. python tools/check_master_list.py --student <slug>
   python tools/build_glossary_sheet.py --student <slug>
7. Update status.md      — name the NEXT country explicitly.
```

**Search routing: free first, Firecrawl when free is blocked.** Claude's `WebSearch`/`WebFetch` is the
default for everything here, official course pages included. Escalate to `firecrawl_search.py` the
moment free search is *blocked* — meaning an error **or a response that doesn't contain the fact you
went there for** (a JS-rendered fee table coming back empty is the usual case, and it's a block even
though nothing errored). Then just run it; credits are there to be spent, no permission needed. The
full rule is **guardrail 6 in `00_overview.md`** — this is the only copy that stage-specific detail
belongs in.

## Pick the next country (don't ask the student)

`preferences.json → target_countries` is already in the student's stated preference order — that
order **is** the discovery sequence. Never open a session by asking "which country should we start
with" or "which country next" — work it out from the files, the same discipline `resume.md` uses
for the rest of the pipeline state:

1. **Read `target_countries`** from `data/students/<slug>/preferences.json` (e.g. `["Australia",
   "Singapore", "Malaysia", "China"]`) — this is the full ordered scope.
2. **Read `master_list.csv`'s `Country` column** (if the file exists yet) to see which of those
   countries already have rows. Zero rows ⇒ not yet discovered; any rows ⇒ at least started.
   `master_list.csv` is the source of truth here, not `status.md`'s prose — if they disagree, trust
   the CSV, same rule as `resume.md`'s "files win over the note."
3. **Next country = the first entry in `target_countries` with no rows yet.** Run **exactly one**
   country per session — roster → constants → row fill → merge → sync. Not a preference: `--country`
   on `merge_candidates.py` and `sync_shortlist.py` refuses a mixed batch, because a 35-column
   country pass is the most context this session can hold and still research honestly.
4. **Every target country already has rows ⇒ Stage 3 discovery is done**, not "pick one to redo" —
   move on to Stage 4 (see "Done when").
5. **Singapore and Malaysia are separate entries** (split 2026-07-29 — `COUNTRY_NORMALIZE` used to
   fuse them into one `Singapore/Malaysia` token, which handed Foo De Mi six Singapore rows for a
   country she never picked). They are two countries, two passes, two syncs. The same goes for any
   grouped label you meet in an older `preferences.json` — split it before you start.

The one case actually worth surfacing to the student: `target_countries` is empty/missing, or names
a country with no file in `workflows/countries/` and no obvious query pattern to improvise from.
Everything else is inferable from the files.

**Update `status.md` after every country's pass, not just at the end of the whole stage.** Rewrite
the "Master list state → Destinations covered" line and the "Next action" line to name the specific
next country (e.g. "Next: run Singapore discovery"), so a fresh session — or you, next message —
never has to ask again.

## Per-destination query playbook

**This section has two readers, and each now reads a different pair of files.** You (main session)
use it for the **roster sweep** (step 1) — 6-10 queries to name the country's 8-12 candidate
universities and courses. Each **row-filler subagent** is told to read its country's file first,
because the dated traps in it (the Australian domestic-fee trap, Singapore's five-tier fee table,
the SMU name collision, XJTLU's Year-2 entry) are exactly what a cold researcher gets wrong. **They
live in `workflows/countries/<code>.md` and only there** — never copy them into the agent file, and
never copy them back into this core file.

Substitute `<field>`, `<course>`, `<level>`. Aggregators are fine for *finding* universities in the
roster sweep; they are never the source of a number that lands in a cell.

**Cross-country (discovery only — never the source of record for a hard fact):**
```
<course> bachelor StudyPortals
QS world university rankings <field>
Times Higher Education <field> subject ranking
best universities for <course> <country>
```

**Each country's block — query list, dated traps, and lore — now lives in its own file, not inline
here.** Read yours before the roster sweep (main session) or before researching your row (row-filler):
`workflows/countries/uk.md`, `usa.md`, `australia.md`, `singapore.md`, `malaysia.md`, `china.md`,
`hong-kong.md`, `japan.md`. Same invariant as before: a trap lives in exactly one place — this core
file keeps the pointer, the country file keeps the lore.

## Step 1 — Roster sweep (free WebSearch, main session)

Name the country's candidates and **nothing else**. 6-10 free `WebSearch` queries off the playbook
block above, and for each plausible hit record only four things:

| university | course | city | course URL |
|---|---|---|---|

**Stop there.** No fees, no entry bars, no scores — those are the row-fillers' job, and pulling them
now means paying for the same page twice and filling this session's context with 12 universities'
worth of detail. Aim for **8-12 rows**: enough to cut from, few enough that each can carry 35
researched columns. Aggregators (StudyPortals, QS, THE) are welcome *here* — this is the one step
where they're the right tool.

Sanity-check the roster before dispatching: drop anything that plainly fails a stated deal-breaker,
doesn't teach the field in English, or is a name collision (`smu.edu` is **Texas**, not Singapore).
Each bad row costs a full subagent.

## Step 2 — Country constants (once per country)

Research **once** what every row in this country would otherwise re-research 10 times, and write it to
`.tmp/<slug>/country_<code>.json`. Every row-filler is handed this path:

```json
{
  "country": "Australia",
  "as_of": "2026-07-29",
  "visa_funds_proof": "AUD 29,710/yr living costs + first-year tuition + return airfare (subclass 500)",
  "post_study_work": "485 graduate visa, 2-3 yrs; +1 yr in designated regional areas",
  "application_system": "Direct to each university (or an agent portal)",
  "intakes": "Semester 1 late Feb; Semester 2 late July. NO September intake.",
  "living_benchmark_per_year": "AUD 29,710 (official); Sydney/Melbourne ~20-40% above",
  "recognition_route": "Washington Accord via Engineers Australia; check MQA recognition per programme",
  "ranking_source": "QS 2026 subject + overall",
  "notes": "Domestic (Commonwealth Supported) fees appear beside international fees on the same page."
}
```

Fill only the keys that are genuinely country-wide. A row-filler is told to prefer a real per-university
exception over these when one exists — and to say so in `research_notes` when it does.

## Step 3 — Row fill (parallel `row-filler` subagents)

Dispatch **one `row-filler` subagent per university, in parallel** (`.claude/agents/row-filler.md`,
pinned to Sonnet). Each researches its one university+course and writes exactly one fragment to
`.tmp/<slug>/candidates/<uni-slug>.json`. Give each dispatch, explicitly:

- the **student slug**,
- the **one university + course** (and city + course URL from the roster),
- the **country**,
- the path to `.tmp/<slug>/country_<code>.json`.

Parallel is safe here and serial is not just slower but *worse*: each agent writes its own fragment
file and never touches `master_list.csv`, so there is nothing to race — unlike Stage 4's report-writer
dispatches, which rewrite the whole CSV and must run one at a time. Keeping the research out of this
session is the point: 12 universities' worth of fetched pages would otherwise all land in one context.

**Parallelised by ROW, not by column.** One agent per university (~2-3 fetches each) beats one agent
per column (~21 agents each re-fetching the same course page). It also matches how the tools work:
`sync_shortlist.py` dedupes by `course_key` and **skips** a repeat university rather than merging into
it, so a column-at-a-time sync is impossible today — and scoring needs all eight sub-scores at once
anyway. Fragments in, one merge, one sync.

When they're all back, read the "Gaps/flags" line of each reply — that's where sentinels and
unverifiable facts get declared — before merging.

> **Firecrawl's rate limit is tight and shared across search+scrape (~10-15 req/min, learned
> 2026-07-28, Francena).** This bites much less now that Firecrawl is a *fallback* rather than the
> primary discovery tool, but it still applies when several row-fillers escalate at once: some queries
> return 0 results, some scrapes silently come back `null`, and the tool still exits 0. **Check the
> `results` count and `markdown` per query before trusting a batch.** Retry a few seconds later (the
> error carries a `retry after Ns` hint), and always to a **different `--out` path** — the tool
> overwrites and has no append mode, so concurrent agents must not share one output file.

## The candidate schema

The full candidate schema — every required field, the field notes on `currency`/`total_cost_programme`/
`meets_english`, the `entry_margin` vs `admission_likelihood` distinction, the cell-budget readability
rules, the 0-5 scoring guide, and the `recognition_fit`/branch-campus/home-country scoring notes — now
lives in **`workflows/03b_candidate_schema.md`**. Row-fillers read it in full before writing their
fragment; the main session doesn't need it and shouldn't load it.

## Steps 4-6 — Merge, sync, check

```powershell
python tools/merge_candidates.py  --student <slug> --country "<Country>"   # gaps stop here
python tools/sync_shortlist.py    --student <slug> --country "<Country>"   # --dry-run to preview
python tools/check_master_list.py --student <slug>                          # the gate
python tools/build_glossary_sheet.py --student <slug>                       # refresh Glossary tab
```

`merge_candidates.py` collects `.tmp/<slug>/candidates/*.json` into `.tmp/<slug>/uni_candidates.json`
and **exits 1 naming every `(university, missing field)` pair** — so you re-dispatch only the two
row-fillers that came back short, not the country. It also rejects a fragment whose `country` isn't
this pass's, and two fragments claiming the same university+course. Fixing gaps *before* the CSV is
the whole point: sync only ever appends and dedupes by `course_key`, so a university synced with holes
is silently **skipped** on a re-run rather than topped up.

`sync_shortlist.py` computes desirability + A/B/C tier, Reach/Match/Safety, feasibility flags, dedupes
by canonical university+course, and appends new rows as **Longlist**. It also writes each candidate's
`research_notes` to `research_notes.md`. The CSV is created on first run. **`--country` is required**
and every candidate must match it — one country per pass, enforced.

`check_master_list.py` is the gate — it must come back clean before you hand a list to a student. It
checks the header against the schema, **completeness** (every required column filled; a sentinel only
in a column that allows one), the length budgets, bare jargon that has a plain equivalent, the allowed
values per column, and contradictions between `Grades vs entry bar` and `Admission likelihood` (grades
below the bar can't be a Safety; grades above it that are still a Reach must say why).

## Step 7 — Update `status.md`

Rewrite "Master list state → Destinations covered" and "Next action" to name the **specific** next
country. Record the pass's cost (rough token spend + wall-clock) while you still know it — the
per-country budget is a measurement nobody has taken yet.

## Backfilling an existing longlist (rows that are already there, with holes)

Not a country pass. This is the repair path for a list that already has its rows but fails the
completeness gate — a legacy student predating the "all 35 columns required" policy (2026-07-29),
or a pass that came back short. **`sync_shortlist.py` cannot do this**: it only appends and dedupes
by `course_key`, so it silently *skips* a university already on the list rather than topping it up.

```
1. python tools/check_master_list.py --student <slug> --blanks
                           the brief: each row's blank columns, grouped by university.
2. Write the shared context ONCE            -> data/students/<slug>/plans/<n>_<country>_backfill.md
                           student profile, cell budgets, sentinels, any paste-don't-research
                           constants (e.g. the visa figure), and the per-university column lists.
3. Dispatch row-filler in BACKFILL mode     -> .tmp/<slug>/backfill/<uni-slug>.json
                           parallel, one per university. Each prompt = the plan file's path,
                           the dispatch number, the university. Nothing else. See 00_overview.md
                           -> "Dispatch by reference, not by paste".
4. python tools/apply_backfill.py --student <slug> [--country "<Country>"] --dry-run
   python tools/apply_backfill.py --student <slug> [--country "<Country>"]
5. python tools/check_master_list.py --student <slug>        # full run, no --check filter
   python tools/build_glossary_sheet.py --student <slug>
6. Update status.md.
```

`apply_backfill.py` patches the cells **and** appends each fragment's `research_notes` under that
university's existing heading in `research_notes.md` — both files written once, from disk. It
validates everything first and writes nothing if any fragment fails, so a batch is all-or-nothing.
It refuses: a university not already on the list, an unknown column, a cell over `CELL_BUDGETS`, a
computed column (`Desirability`, `Tier`, `Admission likelihood`, `Grades vs entry bar`, `Warnings`,
`Approx total (MYR)`, `List status`), and — without `--overwrite` — any cell that is already filled.

> **It does not rescore.** It has cells, not sub-scores or weights, so patching `Key deadline` or a
> cost column leaves `Warnings` / `Approx total (MYR)` stale. The tool prints which computed columns
> went stale; re-derive those by hand, or put the row through the normal fragment → merge → sync
> path instead. `--country` is the guard for a split batch (UK half and USA half in two sessions):
> it refuses to patch a row whose `Country` doesn't match.

## Edge cases & rules

- **8-12 rows per country, not 20-40 in one go.** The old "aim wide" number came from snippet-level
  rows that cost almost nothing; a 35-column officially-sourced row is a different unit of work. Wide
  still matters — get the spread *across* countries and include genuinely safe options, not only
  aspirational ones — but a country pass that returns 25 rows means each got researched a third as well.
- **Don't over-scrape — for signal, not for spend.** Every scraped page lands in context and dilutes it,
  so a wide `--scrape-top` makes the extraction step *worse*, not just pricier. Tune `--limit` /
  `--scrape-top` to the most promising official pages.
- **Facts are official-sourced now, not provisional.** Stage 3 owns verification (the pre-flight moved
  here on 2026-07-29); Stage 4 writes reports and does not re-check the row. So a number in a cell has
  to have come off the university's own page — `source_authority = "Official page"`. A row left
  `Not verified` is an admission of a gap, and it must name the unverified fact in `notes`.
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
  students. Sanity-check after a sync that a spot-checked row's `Approx total (MYR)`/`City`/`Intake`
  line up under their headers.
- **The schema went 34 → 35 columns on 2026-07-25** (the readability fix). `Fits grades?` was renamed
  **`Grades vs entry bar`** and is now derived from `entry_margin` alone; `Backup entry route` was
  dropped from the CSV (it is a Stage-4 report section now — see `04_university_report.md`); and
  **`Course at a glance`** + **`Student life`** were added, one sentence each. All five student CSVs were
  migrated in one disposable pass. Two new per-student files came with it: `research_notes.md` (the
  long-form research the cells no longer hold) and `glossary.csv` (the Google Sheets Glossary tab).
- **The schema was slimmed 41 → 34 columns on 2026-07-16** — the master list is read in Google Sheets, and
  seven columns were blank, duplicated another column, or were internal bookkeeping: `Meets English?`,
  `Total cost (programme)`, `Currency`, `Student community links`, `Student life`, `Data as-of`,
  `Report status`. All five student CSVs were migrated in one pass (a disposable script, not a `tools/`
  entry — same rationale as the budget backfill below). **The columns went, the candidate-JSON fields
  stayed**: `currency`, `total_cost_programme` and `meets_english` are still required inputs (see Field
  notes above). If you are reading an old report or `.bak` that references the dropped columns, that's
  why. Toru's Stage-4 student-life research was rescued to
  `data/students/toru/student_life_research.md` — fold it into a report rather than re-researching it.
- **A missing `Over budget` flag on an OLD row proves nothing** (the free-text-budget era, closed
  2026-07-29). Budget used to be a free-text form question passed straight through, so a student who typed
  `400000-800000` landed a *range string* in `profile.financial.total_budget`; `feasibility_flags()` did
  `float(budget)` inside a swallowing `except: pass`, the parse threw, and the check silently never ran —
  over-budget rows looked clean. Two fixes closed it: `budget_ceiling()` parses a range to its **upper
  bound** (2026-07-16) and now also **rejects implausible values** (anything under 1000 → `None`, so
  `"~ 1 million? Idk"` no longer yields a ceiling of `1.0`); and the form's budget question became a
  **four-band dropdown** (2026-07-29), so nothing but a number or null reaches `total_budget_ceiling` any
  more — see the band table in `01_intake.md`.
  **Sync only ever appends, so rows synced before those fixes were never retro-flagged.** Don't read the
  absence of `Over budget` on a pre-2026-07-29 row as affordable; re-check it against the ceiling. Ong's UK
  rows were backfilled on 2026-07-16 (UCL 893,850 / Manchester 885,000 / Warwick 841,281) and are now
  clean — worth knowing that the first status note of this named only two of the three, so **re-derive
  which rows are over from the CSV, don't trust a prose list of them.** Backfill is a small one-off script
  reusing `budget_ceiling()`: only the affected students matter, so it doesn't belong in `tools/`.
- **Stale `.tmp/<slug>/candidates/`** — fragments are disposable and a stale one from an earlier round
  (different course, old scoring) merges just as happily as a fresh one. **Clear the directory before
  each country's pass**, and remember `merge_candidates.py` reads *every* `*.json` in it. Same for
  `uni_candidates.json`, which is overwritten, and which `sync_shortlist.py` syncs verbatim.
- **The 35 columns are all required now (2026-07-29)** — `REQUIRED_COLUMNS` in `shortlist_schema.py`,
  everything but `Warnings`, which is written `None` when a row is clean rather than left empty. The
  eight existing student CSVs were **not** backfilled: they predate the policy and will fail the
  completeness check until someone re-researches them. That's expected, not a regression — the policy
  applies to new students and new country passes.

## Done when

For **this country**: 8-12 rows in `master_list.csv`, every one of the 35 columns populated,
`merge_candidates.py` and `check_master_list.py` both clean, and `status.md` naming the next country.

For **Stage 3 overall**: every entry in `preferences.json → target_countries` has rows (see "Pick the
next country" — that's what makes this checkable without asking), with a Reach/Match/Safety spread
*across* the whole list rather than per country.

What carries forward is a **verified** list, not a provisional one. Stage 4 no longer re-checks these
facts — it takes the student's finalists and writes reports. Proceed to **Stage 4**
(`04_university_report.md`).
