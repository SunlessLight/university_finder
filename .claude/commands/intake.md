---
description: Stage 1 — ingest the Google Form CSV and finalize each student's profile
argument-hint: [csv-path]
---

Run `workflows/01_intake.md` for the responses CSV at `$1`.

If `$1` is empty, look in `data/form/` and use what's there (Google names the export after the
form, e.g. `Form responses - Sheet1.csv` — not `responses.csv`). If there's more than one file, ask
which.

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

This workflow IS the plan. Do not enter plan mode (CLAUDE.md).
