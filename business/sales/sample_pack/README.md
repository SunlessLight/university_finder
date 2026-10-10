# Sample pack — the demo you send

This is the **show-don't-tell** asset. When someone says *"Gemini's enough"* or *"I just want a
spreadsheet,"* you send one of these files and stop typing. The gap argues for you.
(Reasoning: [../positioning.md §3](../positioning.md). The tiers these map to: [../service-tiers.md](../service-tiers.md).)

## What's in here — one artifact per tier

| File | Tier it shows | What the prospect sees |
|---|---|---|
| `sample_master_list.csv` | **Tier 1 — The List** | 15 real universities × the full **35 columns** — Reach/Match/Safety separate from Desirability *and* from whether your grades clear the bar, total cost in ringgit, "Recognised in Malaysia?", verified-vs-not. Opens in Excel / Google Sheets. |
| `sample_glossary.csv` | **Tier 1 — The Glossary tab** | Plain-English definitions of every acronym the list actually uses, generated from the list itself. Import as a second sheet. |
| `sample_university-report_MIT.pdf` | **Tier 2 — The University Reports** | One full **16-section decision report** (19 pages, built under the pre-2026-09-06 schema — new reports are 15-section) — who actually gets in, aid maths, and honest *reasons to hesitate*. |
| `sample_apply-guide_US.pdf` | **Tier 3 — The Apply Pack** | One **per-region apply guide** (15 pages) — grouped by application system, every deadline, the exact financial-aid mechanics. |

Send **one**, not all three, unless someone asks for the full thing — the university-report PDF is usually the
one that lands, because it's the part they've never seen and can't picture.

## This is anonymized real work — not fiction

Every file is the genuine end-to-end output for **one real student, with their identity removed**:
- name changed to a stand-in (**"Arif"**),
- school name and exact family finances generalized (e.g. "a lower-income band" instead of a figure),
- university facts, fees, deadlines and aid numbers left intact — that's the part that's real and public.

Each file carries a **"Sample — anonymized demo"** banner at the top so nobody mistakes it for a real
person's private file, and so it's obvious you protect your clients' data.

## Before you share these — one check

These were scrubbed and scanned (zero hits for the name / school / income figures in the CSV and both
PDFs). But **open all three yourself once** before the first send — you're the last gate. If you ever
regenerate them from a different student, re-run the same scan and re-read them.

## How they were built (to regenerate)

`sample_master_list.csv`, `sample_glossary.csv` and `sample_university-report_MIT.pdf` are built by
`build_sample_pack.py` — run `python sales/sample_pack/build_sample_pack.py`. It pulls the same 15
universities from the source student's current `master_list.csv`, redacts each cell, regenerates the
glossary from that redacted list (`build_glossary_sheet.py`), and redacts + renders the MIT report
(`md_to_pdf.py`, same engine as `report_to_pdf.py`) with the "Sample — anonymized demo" banner inserted
after the title. It ends by re-running the same leak scan by hand ("zero hits") described below, so a
regeneration re-proves the guarantee instead of assuming it still holds.

Re-run it whenever the source student's list or reports change materially — a report rebuild, a
corrected fact, a re-scored row — so the sample stops drifting from what the pipeline produces today.
`check_master_list.py --file sample_master_list.csv` and `check_report.py --file <redacted .md>` should
both still come back at 0 findings after a regeneration; if they don't, the source data has an issue
worth fixing before it goes in a sample, not redaction to work around.

`sample_apply-guide_US.pdf` is **not** covered by the script and was left untouched in the 2026-08-22
refresh — the source student's `application_prep/us.md` (built 2026-07-26) predates a Stage 5a report
rebuild (2026-08-20) that corrected real facts (Columbia's test-optional status, a new DHS visa-rule
fact affecting OPT/STEM-OPT). Regenerate `us.md` via Stage 8 first, then build its sample the same way
(`md_to_pdf.py --type apply`), before trusting this file as current.

The un-redacted source stays in the gitignored data bank and is never shared.
