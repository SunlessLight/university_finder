---
description: Stage 4 — pre-flight the finalists, then build one university report each
argument-hint: <student-slug> [finalist; finalist; ...]
---

Run `workflows/04_university_report.md` for student `$1`.

Read `data/students/$1/status.md` first and cross-check it against `master_list.csv` (files win
over the note).

**The pre-flight stays in this session — it is the Stage 4 checkpoint with me, not research:**

**1. Get to a Shortlist.** Two ways in, depending on whether finalists were named after the slug:

- **Named directly** — e.g. `/report $1 UCL: mechanical engineering; Imperial; Manchester: aerospace`
  (`;` between finalists, an optional `: Course` after a university only when it has more than one
  course on the list). Resolve each name — don't match it yourself, that's exactly the guessing this
  step exists to avoid:
  ```powershell
  python tools/match_finalists.py --student $1 --query "University|Course" --query "University2"
  ```
  One `--query` per named finalist (course after `|`, omitted where I didn't give one). Read the JSON
  result per query:
  - `resolved` — promote it (edit `master_list.csv`, that row's `List status` → `Shortlist`).
  - `ambiguous_course` — tell me the `options` for that university and ask which one I meant.
  - `ambiguous_university` / `not_found` — tell me what didn't match. **Don't guess** — fall back to
    the render below for that one rather than picking the closest-looking row yourself; this is the
    same "stop rather than guess" rule `report-writer` follows for its own dispatch inputs.

  Once every named finalist resolves, render just those picks so I can confirm the set before you go
  further — I already named these, so this is a quick confirmation, not a cold render:
  ```powershell
  python tools/compare_universities.py --student $1 --rows "University|Course, University|Course" --dimensions summary,scholarship,fit
  ```

- **Not named** — render the full Longlist and **wait**:
  ```powershell
  python tools/compare_universities.py --student $1 --status Longlist --dimensions summary,scholarship,fit
  ```
  **I pick the finalists. Do not self-select** (CLAUDE.md). Use `--country <name>` to work one
  destination at a time on a long list.

Either way, from here on it's the same set of Shortlist rows — steps 2-4 apply regardless of how they
got there.

2. Spot-check the picks for **currency, not correctness** — `Key deadline` + intake still open, any
   pick still reading `Info source = Not verified` gets the full official-source check, recognition
   recorded for regulated professions, and what the application itself makes the student submit.
3. Re-judge `Admission likelihood` and `Warnings` if a fact moved. Edit `master_list.csv` directly
   for existing rows — `sync_shortlist.py` is only for new candidates.
4. Confirm the set is a Reach/Match/Safety spread and swap out any dud **before** sinking research
   into it. Demoting or rejecting a row is my call — bring it to me with the one-line reason.

Then, and only for picks that survived: **dispatch the `report-writer` subagent once per finalist,
all in parallel.** Each dispatch writes only its own report and its own marker fragment — nothing
writes `master_list.csv`, so there is nothing to race. Give each dispatch the slug, the finalist,
and the mode (`--mode course` default; `--mode university` for US whole-institution fit).

When every dispatch is back, **once**, in this session:
```powershell
python tools/flip_finalists.py    --student $1   # folds the markers into the CSV in one pass
python tools/check_master_list.py --student $1   # the gate — must come back clean
```
`flip_finalists.py` soft-fails per fragment and leaves anything it refused on disk. Bring me its
failure lines rather than working around them — `already_rejected` in particular means it declined
to resurrect a row I dropped, and re-promoting that row is my call.

Report back each agent's gaps (`"Not found — <why>"`) so I can see what's missing. Rewrite
`status.md` at the end.

This workflow IS the plan. Do not enter plan mode (CLAUDE.md).
