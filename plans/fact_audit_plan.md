# Plan: the "facts, not guesses" audit

> **Status (2026-10-28): done.** T0–T10 and T12 done; results in `fact_audit/`. T11 (Evan's pick)
> went with the defaults: every top-10 problem became a backlog entry (R26–R37,
> `business/additionals.md`). Evan's four decisions (`fact_audit/00_START_HERE.md`) are still open,
> inside R32 and R34.

## Context (why)

Evan wants everything a student receives to be **factual: information, not advice**. Right now
some files carry AI guesses ("likely waived…"), AI notes-to-self, and chatty text. Before fixing
anything, we need a map: which product has the problem, where it comes from, and how bad it is.
This plan makes that map as a folder of plain-English reports, written by helpers working side by
side.

This plan **only reads and reports**. It changes no workflow, tool or student file. Fixes come
later, one by one, after Evan has read the reports.

## Quick answers to Evan's questions

**Is there already a backlog task for "all information verified"?** Partly. In
`business/additionals.md`:
- **L5**: show every fact with its source, or "Not found on official page". The closest match. Not
  planned yet.
- **R9**: record *when* a fact was checked, not just that it was.
- **L2**: 212 rows on older lists still say "Not verified".
- **R16, R17, R21**: clean-ups of three specific kinds of old guesses (degree recognition,
  "Well above" grade bars, English-test waivers).
- **Nothing covers the other half:** advice wording, chatty text and AI notes-to-self in what a
  student reads. And nobody has scanned the whole system. This audit is new.

**What products this project makes** (to be confirmed by the audit):

| # | Product | Who gets it | Made by |
|---|---|---|---|
| 1 | Student profile (from the Google Form) | internal | Stage 1, `ingest_form_csv.py` |
| 2 | University list (spreadsheet + research notes + glossary tab) | student | Stage 3, row-filler helpers + `sync_shortlist.py` |
| 3 | Comparison table for picking finalists | Evan | `compare_universities.py` |
| 4 | University report (PDF, one per finalist) | student | Stage 4, report-writer + `build_report.py` |
| 5 | Quick university report (no form needed) | student | `quick_university_report.md` |
| 6 | Recommendation + application strategy + one deadline calendar | student | Stage 5, `build_calendar.py` |
| 7 | "How to apply" guide per region (PDF) | student | Stage 8, `build_application_prep.py` |
| 8 | Sample pack + demo website | the public | `business/sales/sample_pack/`, `prototype/` |

Not in scope (business tools, not student products): social posts, mentor, Notion sync, catchup.

**Honest opinion, before we start:** not everything can be "information, not advice". The 0–100
score, Reach/Match/Safety and the Stage 5 recommendation are *judgments by design*. Those are the
product. The right rule for them isn't "delete them" but "label them as judgments and show the
rule behind them". The audit tags them separately (label **J**, below) so Evan can decide product
by product.

## The labels every report uses

- **G (Guess):** a fact written from AI memory or with "likely / usually / probably", or a value
  filled in without a source.
- **A (Advice):** tells the student what to do ("you should", "we recommend", "consider").
- **Y (Yapping):** chatty text or AI notes-to-self *in a file a student reads* ("Note: I couldn't
  find…", "let me check"). Terse instructions written for helpers are fine and are not flagged.
- **J (Unlabelled judgment):** a rule-made score or label shown as if it were a fact.
- **L (Loophole):** an instruction or tool that *lets* G/A/Y through ("if not found, estimate"),
  or a check that should catch it and doesn't.

Severity: **High** = reaches a student as a fact. **Medium** = could reach one. **Low** = internal only.

## Output folder: `fact_audit/` (in the project)

```
fact_audit/
  00_START_HERE.md        the summary Evan reads first (≤2 pages, top 10 problems)
  _brief.md               shared rules for the helpers (labels, template, privacy)
  01_intake.md            02_longlist_instructions.md   03_scoring_and_checks.md
  04_spreadsheet_text.md  05_report_instructions.md     06_report_tools.md
  07_decide_and_apply.md  08_output_sweep.md            09_promises_vs_reality.md
```

Each report has the same shape: what this part makes (one plain paragraph) → who sees it →
findings table (`# | Where (file:line) | Quote ≤20 words | Label | Severity | Why it matters |
Suggested fix, one line | Already in backlog?`) → what is already solid → counts per label.

## Tasks

| ID | Goal | Who | Needs | Touches | Size |
|---|---|---|---|---|---|
| T0 | Copy this plan to `plans/fact_audit_plan.md`; write `fact_audit/_brief.md` (labels, severity, template, privacy, read-only rules from this plan) | Claude | none | those 2 files | S |
| T1 | Intake: `workflows/01_intake.md`, `tools/ingest_form_csv.py`, `fetch_form_*.py`, `init_student.py`, `derive_weights.py`, `tools/appsscript/`, `forms/*.json`, `/intake` command → `01_intake.md` | helper | T0 | its report | M |
| T2 | Longlist instructions: `03_discover_longlist.md`, `03b_candidate_schema.md`, `sources.md`, `workflows/countries/*.md`, `.claude/agents/row-filler.md`, `/longlist` → `02_…` | helper | T0 | its report | M |
| T3 | Scoring and checks: `shortlist_schema.py`, `sync_shortlist.py`, `check_master_list.py`, `apply_backfill.py`, `merge_candidates.py`, `firecrawl_search.py`, `scoring-weights` skill → `03_…` | helper | T0 | its report | M |
| T4 | Text the student reads in the spreadsheet: `apply_glossary.py`, `build_glossary_sheet.py`, `business/sales/sample_pack/sample_master_list.csv` + `sample_glossary.csv` → `04_…` | helper | T0 | its report | M |
| T5 | Report instructions: `04_university_report.md`, `quick_university_report.md`, `report-writer.md`, `/report`, `/quick-report`, sample MIT report PDF (pages 1–10) → `05_…` | helper | T0 | its report | L |
| T6 | Report tools: `build_report.py`, `check_report.py`, `apply_report_fx.py`, `report_to_pdf.py`, `compare_universities.py`, `match_finalists.py`, `flip_finalists.py` → `06_…` | helper | T0 | its report | M |
| T7 | Decide + apply: `05_decide_and_apply.md`, `build_calendar.py`, `08_application_prep.md`, `build_application_prep.py`, `apply_prep_to_pdf.py`, `application-guide` skill, `/decide`, `/apply-prep`, sample US guide PDF → `07_…` | helper | T0 | its report | M |
| T8 | Output sweep: a count-only script (in `.tmp/fact_audit/`) over every student's generated files (`master_list.csv` Notes/Warnings, `research_notes.md`, `reports/`, `application_prep/`, recommendation, calendar), plus the sample pack and `prototype/data.js`. Counts per phrase type per file type. **No quotes from student files**; quotes only from the sample pack and demo → `08_…` | helper | T0 | its report, `.tmp/fact_audit/` | M |
| T9 | Promises vs reality: what `business/product_report/*.md`, `business/sales/positioning.md`, `sample_pack/README.md` promise ("every fact from the university's own website") vs what `workflows/00_overview.md` and the tools actually guarantee → `09_…` | helper | T0 | its report | M |
| T10 | Summary: read the 9 reports, recount findings with `grep`, write `00_START_HERE.md`: product list (corrected), top 10 problems by severity, which ones touch the 10 Nov paid lists, which are already in the backlog, decisions for Evan (each with a default) | Claude | T1–T9 | `00_START_HERE.md` | M |
| T11 | Read `00_START_HERE.md`; say which findings become backlog entries (R23+) and the rule for J items | **Evan** | T10 | none | — |
| T12 | Add the agreed findings to `business/additionals.md` (R23+, each in a step), build-log entry, Now box, Notion mirror, commit | Claude | T11 | `additionals.md`, `plans/build-log.md`, `STATUS.md` | S |

**Helper prompt (T1–T9, same shape, filled per task):**
> You are auditing one part of the Shortlisted project for guesses, advice and chatty text.
> Read `<repo>/fact_audit/_brief.md` first and follow it exactly. Your part: **<name>**. Read
> these files: <list>. Read-only: do not edit any file except your report. No web searches.
> Never quote a student's name, grades, income, school or nationality. Write your report to
> `<repo>/fact_audit/<NN_name>.md` using the template in the brief. Write the file early and
> update it as you go. Reply with ONLY the path and the number of findings.

## Run order

```
STAGE 1            → T0                      (this session)
STAGE 2 (parallel) → T1 T2 T3 T4 T5 T6 T7 T8 T9   (9 helpers launched in one message from this session)
STAGE 3            → T10                     (this session; needs all 9)
STAGE 4            → T11                     (Evan, when he has time)
STAGE 5            → T12                     (a new short session)
```

- No clashes: each helper writes only its own report; none uses Chrome, Notion or the web.
- Budget: each helper reads 20–60k tokens. The main session only sees 9 one-line replies, then
  reads the 9 reports (~45k). Whole run in this session ≈ 80k. Safe.
- Hand-off: the reports *are* the hand-off. If T10 doesn't finish, the next session reads
  `fact_audit/` and starts at T10.

## Timing and the freeze

The backend is frozen until the 10 Nov lists, except fixes a customer would see. The audit only
reads, so it can run now. **Default:** run it now, so any High finding in the *spreadsheet* (the
product going out on 10 Nov) can be fixed before then. Everything else waits until after 10 Nov.

## Verification

- `ls fact_audit/` shows all 11 files.
- `grep -c "^| [0-9]" fact_audit/0*.md` matches each helper's reported count (recount, don't trust).
- Privacy: grep `fact_audit/` for every student folder name under `data/students/`: zero hits.
- `git status` shows no changed file outside `fact_audit/`, `plans/fact_audit_plan.md` and `.tmp/`.
- Spot-check 3 findings: open the cited `file:line` and confirm the quote is there.
