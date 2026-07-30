---
description: Build a per-region "how to apply" guide for a student (Stage 8 utility)
argument-hint: <student-slug> <region>
---

Run `workflows/08_application_prep.md` for student `$1`, region `$2`.

If `$2` is empty, list the regions that student actually has Shortlist/Finalist rows for and ask
which one. **One region per pass** — each is a lot of official verification.

Invoke the **`application-guide`** skill for voice before writing anything; it sets the
admissions-coach register and the rules that keep the guide readable for an 18-year-old.

Sequence: research the apply mechanics for each Shortlist/Finalist uni in the region from
**official** admissions + financial-aid pages → assemble `.tmp/$1/apply_prep_$2.json` → then:

```powershell
python tools/build_application_prep.py --student $1 --input .tmp/$1/apply_prep_$2.json
python tools/apply_prep_to_pdf.py --student $1 --region $2
```

Don't hand-write the intro, Contents, Key terms, jargon links, checkboxes or list spacing — the
renderer adds those.

**This stage is read-only against `master_list.csv`.** It never changes `List status` and never
flips a row. It's a checklist-and-deadlines deliverable, not a fit assessment — skip the "is this
uni right for me?" texture, that's the university report's job.

Rewrite `status.md` at the end.

This workflow IS the plan. Do not enter plan mode (CLAUDE.md).
