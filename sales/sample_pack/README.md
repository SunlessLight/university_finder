# Sample pack — the demo you send

This is the **show-don't-tell** asset. When someone says *"Gemini's enough"* or *"I just want a
spreadsheet,"* you send one of these files and stop typing. The gap argues for you.
(Reasoning: [../positioning.md §3](../positioning.md). The tiers these map to: [../service-tiers.md](../service-tiers.md).)

## What's in here — one artifact per tier

| File | Tier it shows | What the prospect sees |
|---|---|---|
| `sample_master_list.csv` | **Tier 1 — The List** | 15 real universities × the full **34 columns** — Reach/Match/Safety separate from Desirability, total cost in ringgit, "Recognised in Malaysia?", verified-vs-not. Opens in Excel / Google Sheets. |
| `sample_dossier_MIT.pdf` | **Tier 2 — The Dossiers** | One full **16-section decision dossier** (6 pages) — who actually gets in, aid maths, and honest *reasons to hesitate*. |
| `sample_apply-guide_US.pdf` | **Tier 3 — The Apply Pack** | One **per-region apply guide** (15 pages) — grouped by application system, every deadline, the exact financial-aid mechanics. |

Send **one**, not all three, unless someone asks for the full thing — the dossier PDF is usually the
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

Redacted copies of the source student's `dossiers/mit-mechanical-engineering.md` and
`application_prep/us.md` were rendered with the existing tools (`dossier_to_pdf.py`,
`apply_prep_to_pdf.py`); the CSV is 15 selected rows of the master list with the same redaction applied
to every cell. The un-redacted source stays in the gitignored data bank and is never shared.
