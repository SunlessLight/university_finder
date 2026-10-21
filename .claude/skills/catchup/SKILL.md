---
name: catchup
description: Use when a session starts cold in this project and Evan asks where things stand, says "catch me up", "where were we", "resume <name>", "pick up <name>", or types /catchup [student-slug].
argument-hint: "[optional: student slug]"
---

# Catch up

## Overview

New sessions start with no memory. The Now box at the top of `STATUS.md` (whole project) and each student's `status.md` are the fast hand-off notes, but notes drift. **The real files win over the note.** This skill rebuilds an accurate picture from the files, briefs Evan, and fixes the note.

This is a read, not research. **Never search the web to catch up.** Don't enter plan mode: these steps are the plan.

## Steps: whole project (no argument)

1. Read the Now box at the top of `STATUS.md`.
2. Read the newest entry in `plans/build-log.md`.
3. Check the note against the real files. For each claim, open the file that proves it:

   | If the note claims | Check |
   |---|---|
   | Where each student is | `python tools/progress_dashboard.py` |
   | LaunchX state, what's decided | `business/launchx/status.md`; if it disagrees with `deck_content.md` or `survey.md`, those win |
   | A backlog item (R-number) is fixed | its entry in `business/additionals.md`, then `git log -p` on the file it names |
   | A plan step is done | `git log -p -- <its target files>` (a plan's banner can lag the code) |

   Also check recent change history (`git log --oneline -10`) for work the note doesn't mention.
4. If the Now box says the project is **paused**, ask Evan first whether he's resuming. Don't treat old dates in it as deadlines.
5. Brief Evan, in this shape:
   - **Where it stands:** 2–4 plain-English lines.
   - **Next step:** one action, small enough to start now.
   - **Fixed in the note:** anything the files contradicted (or "nothing").
6. If the note was wrong or stale, rewrite the Now box to match the files. Replace lines; don't add history (that's the build log's job). Tell Evan what you changed.

## Steps: one student (slug given)

This runs `workflows/resume.md`; that workflow is the source of truth.

1. Match the argument to a folder under `data/students/`. If it's empty or matches nothing, list the folders and ask which student. Don't guess.
2. Read `data/students/<slug>/status.md`.
3. Check it against `profile.json`, `preferences.json` and `master_list.csv`, which win. Reconcile: `target_countries` vs the destinations actually in the CSV; the `List status` counts; stale `Notes` cells; any row still reading `Info source = Not verified`; and whether `profile.json` still carries `_needs_review` or `_intake_raw` (⇒ Stage 1 never finished: finish it before any discovery).
4. Brief and fix the note exactly as in steps 5–6 above, but for this student's `status.md`.

## Common mistakes

| Mistake | Fix |
|---|---|
| Repeating the note back as fact | Every claim gets checked against a file first |
| Searching the web or opening many files "to be safe" | Read only the note, the log entry, and the files that prove its claims |
| Pushing stale dates on a paused project | Ask whether Evan is resuming first |
| Adding a history paragraph to the Now box | The Now box is replaced, not appended. History goes in the build log |
| Listing five next steps | One next step. Evan will ask for more |
