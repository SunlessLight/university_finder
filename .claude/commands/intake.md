---
description: Stage 1 — ingest the Google Form CSV and finalize each student's profile
argument-hint: [csv-path]
---

Run `workflows/01_intake.md`.

**Start by fetching** — don't go hunting for a file:

```powershell
python tools/fetch_form_responses.py --dry-run
python tools/fetch_form_responses.py
```

This pulls only respondents not yet ingested into `data/form/responses.csv`. "Nothing new" means
there's nothing to do — say so and stop. If the fetch fails (endpoint not set up, bad token, no
network), fall back to whatever CSV is already in `data/form/` (Google names the export after the
form, e.g. `Form responses - Sheet1.csv`); if there's more than one file, ask which. Say which path
you took — a fallback CSV can't be `--confirm`ed.

If `$1` is given, use that CSV directly and skip the fetch.

Preview before writing:

```powershell
python tools/ingest_form_csv.py "<csv>" --dry-run
python tools/ingest_form_csv.py "<csv>"
```

Then do the part the tool can't: **finalize every `_needs_review` item per student** (that
workflow's "Finalize each student" section) — grades sanity-check, ethnicity for scholarship
eligibility only, degree level, and the profession → regulator mapping (MMC / BEM+Washington
Accord / LPQB / MIA+ACCA / LAM). Delete `_needs_review` and `_intake_raw` when each student is
genuinely settled; a student parked mid-finalize looks complete otherwise.

**Checkpoint:** settle the `_needs_review` items *with me* before anything gets scored (CLAUDE.md).
Bring me the flagged list per student rather than resolving judgment calls silently.

`--force` overwrites an existing student folder and `data/students/` is gitignored with no undo —
confirm with me first.

Write each student's first `status.md` when their intake is done.

**Then, last of all** — once every student's folder and `status.md` are actually written:

```powershell
python tools/fetch_form_responses.py --confirm
```

That stamps those respondents as ingested in the sheet so they're never handed back again. It runs
*after* everything else on purpose: an intake that crashed or that you abandoned mid-finalize leaves
the rows pending, and the next `/intake` just picks them up. Skip it if you used a fallback CSV.

This workflow IS the plan. Do not enter plan mode (CLAUDE.md).
