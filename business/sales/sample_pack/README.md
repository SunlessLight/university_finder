# Sample pack — the demo you send

This is the **show-don't-tell** asset. When someone says *"Gemini's enough"* or *"I just want a
spreadsheet,"* you send one of these files and stop typing. The gap argues for you.
(Reasoning: [../positioning.md §3](../positioning.md). The tiers these map to: [../service-tiers.md](../service-tiers.md).)

## What's in here — one artifact per tier

| File | Tier it shows | What the prospect sees |
|---|---|---|
| `sample_list.pdf` | **Tier 1 — The List** | 14 real universities in a portrait PDF (22 pages): student profile, summary table, a key to our labels, one card per university with its cost breakdown in ringgit and useful links, glossary at the back. Each card says when its facts were checked on the official page. |
| `sample_university-report_MIT.pdf` | **Tier 2 — The University Reports** | One full **15-section decision report** (25 pages) — who actually gets in, aid maths, and honest *reasons to hesitate*. |
| `sample_apply-guide_US.pdf` | **Tier 3 — The Apply Pack** | One **per-region apply guide** (28 pages, 9 universities) — grouped by application system, every deadline, the exact financial-aid mechanics. |

Send **one**, not all three, unless someone asks for the full thing — the university-report PDF is usually the
one that lands, because it's the part they've never seen and can't picture.

**Working files: don't send these.** They are inputs, kept because the build needs them:

| File | Why it stays |
|---|---|
| `sample_master_list.csv` | The redacted list: 15 rows × 40 columns, including one Rejected row and columns the PDF hides. `build_list_pdf.py` and the demo website's `prototype/_build/gen.py` read it. |
| `sample_glossary.csv` | The glossary as a file. The PDF prints its own, so this is only a by-product. |
| `sample_profile.json` | The stand-in student behind the PDF's profile page. |

## This is anonymized real work — not fiction

Every file is the genuine end-to-end output for **one real student, with their identity removed**:
- name changed to a stand-in (**"Arif"**),
- school name and exact family finances generalized (e.g. "a lower-income band" instead of a figure),
- university facts, fees, deadlines and aid numbers left intact — that's the part that's real and public.

Each PDF says it is a sample at the top ("Sample — anonymized demo" on the report and guide, "Sample
student" on the list) so nobody mistakes it for a real person's private file, and so it's obvious you
protect your clients' data.

## Before you share these — two checks

1. These were scrubbed and scanned (zero hits for the name / school / income figures in both CSVs and
   all three PDFs). But **open all three PDFs yourself once** before the first send — you're the last
   gate. If you ever regenerate them from a different student, re-run the same scan and re-read them.
2. **One small thing is still open:** R31 in `plans/additionals.md` (Monash's course title).

## How they were built (to regenerate)

All the files are built by `build_sample_pack.py` — run `.venv/Scripts/python.exe business/sales/sample_pack/build_sample_pack.py` (the venv has `pypdf` for the privacy scan and WeasyPrint for the PDFs). It pulls the same 15
universities from the source student's current `master_list.csv`, redacts each cell, regenerates the
glossary from that redacted list (`build_glossary_sheet.py`), builds the list PDF from it
(`build_list_pdf.py`, never `--draft`; the Rejected row drops out, which is why the PDF has 14), redacts + renders the MIT report
(`md_to_pdf.py`, same engine as `report_to_pdf.py`) with the "Sample — anonymized demo" banner inserted
after the title, and does the same for the US apply guide (`md_to_pdf.py --type apply`). It ends by re-running the same leak scan by hand ("zero hits") described below, so a
regeneration re-proves the guarantee instead of assuming it still holds.

**Last rebuilt: 2026-10-30**, at the exchange rates stamped `FX_AS_OF 2026-09-05` in
`tools/shortlist_schema.py` (USD 4.04). Every ringgit figure in the list, the MIT report and the apply guide is at
those rates. If `FX_AS_OF` moves, the source student's list and report need re-converting first, then
this rebuild — the script copies the source's ringgit figures, it does not recompute them.

Re-run it whenever the source student's list or reports change materially — a report rebuild, a
corrected fact, a re-scored row — so the sample stops drifting from what the pipeline produces today.
`check_master_list.py --file sample_master_list.csv` and `check_report.py --file <redacted .md>` should
both still come back at 0 findings after a regeneration; if they don't, the source data has an issue
worth fixing before it goes in a sample, not redaction to work around.

The un-redacted source stays in the gitignored data bank and is never shared.
