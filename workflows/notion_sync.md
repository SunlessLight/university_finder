# Workflow: Notion sync — keep the client board honest (↔ Notion "Clients" project)

## Objective

Evan tracks who he has done what for, and whether they gave feedback, on a Notion board. This
workflow keeps that board matching the real state in `data/students/<slug>/`, so he can open Notion
on his phone and trust it. **The local files are the source of truth; Notion is a mirror.** Nothing
in this repo ever reads Notion to decide pipeline work.

This is a **utility** workflow, not a pipeline stage. It never changes `master_list.csv`,
`List status`, `status.md` or any other student file.

## When to run

- `/notion` — board check: every client, which stage, what was delivered, feedback or not.
- `/notion <slug>` — sync one student after a stage finishes or something is sent to them.
- Offer it (don't auto-run) at the end of a session that delivered something to a student, right
  after `status.md` is rewritten.
- Evan says a student replied / gave feedback → log it with `/notion <slug>`.

## Where things live in Notion (verified 2026-10-13)

Everything sits in two shared databases under the "🗓️ Everything" page. Other areas of Evan's life
(A-Levels, Personal, University Application) share these databases — **every query and every write
is scoped to `Area = University Research Agent`.** Never touch a row from another Area.

| What | Address |
|---|---|
| Tasks database | `collection://7d1af2d7-87c3-4eb8-a2d5-085093eaafae` |
| Projects database | `collection://6f27534c-773d-4659-81f7-d426d9a101c3` |
| Project "Clients" | `3bf25bdf03ad80df91e0e37d3282a821` |
| Project "URP Marketing" | `3bf25bdf03ad8082ab61f4bf95f9f9ba` — Evan's own marketing to-dos; read-only for this workflow |
| Stage card "Stage 1 Intake" | `3b425bdf03ad8039aca2f4c113b81743` |
| Stage card "Stage 2 Longlist" | `3b425bdf03ad806baff0f886e6f4ac89` |
| Stage card "Stage 3 Report" | `3b425bdf03ad800e84e3c092c5664004` |
| Stage card "Stage 4 Application Guide" | `3b425bdf03ad8066851ae749d21b9013` |

Tasks columns used here: `Task name` (title), `Area`, `Project`, `Parent-task`, `Sub-tasks`,
`Status` (`Not Started` / `Today` / `This Week` / `This Month` / `Daily` / `Done`), `Due`.

**How the board works.** Each client is one card (a row in Tasks) named after the student, linked
to the "Clients" project, and filed as a sub-task of exactly one stage card. Moving a client to a
new stage = changing which stage card its `Parent-task` points at.

**Notion's stage numbers are not this repo's stage numbers.** Notion counts 1-4 for Evan; the repo
skips 2 and has utilities. Map by the furthest stage where work has started:

| Local state | Notion stage card |
|---|---|
| Folder exists, `profile.json` still has `_needs_review` / `_intake_raw`, or no `master_list.csv` yet | Stage 1 Intake |
| `master_list.csv` exists, no file in `reports/` | Stage 2 Longlist |
| At least one report in `reports/` (Stage 4), with or without `recommendation.md` (Stage 5) | Stage 3 Report |
| An application-prep guide has been built (`08_application_prep.md`) | Stage 4 Application Guide |

## The client card body

The stage says where a client is; the card body says what they actually received and what came
back. Keep exactly these two headings, newest line first, one line each:

```markdown
## Delivered
- YYYY-MM-DD — <what was sent, e.g. "UK longlist spreadsheet" or "reports: Imperial, Heriot-Watt">

## Feedback
- YYYY-MM-DD — <asked, waiting | received: one-line gist>
```

A delivery with no feedback line dated on or after it = **feedback outstanding**. That is the thing
Evan most wants to see.

## Privacy fence (PDPA — same rule as the rest of the repo)

Notion is an external service. A card may hold **only**: the student's name, their stage, what was
delivered and when, and a one-line gist of their feedback. **Never** write grades, budget or
finances, nationality, scholarship status, phone/email, or any `profile.json` / `preferences.json`
field. University names in a "Delivered" line are fine; the student's scores against them are not.

## Steps

1. **Load the Notion tools.** They are deferred — one `ToolSearch` call:
   `select:mcp__notion__notion-fetch,mcp__notion__notion-query-data-sources,mcp__notion__notion-update-page,mcp__notion__notion-create-pages`.
   Follow the parameter shapes those schemas return; don't guess them.
2. **Read the board in one query** (never search Notion blind):
   `SELECT url, "Task name", "Status", "Parent-task" FROM "collection://7d1af2d7-87c3-4eb8-a2d5-085093eaafae" WHERE "Area" = 'University Research Agent'`.
   Client cards are the rows whose `Parent-task` is one of the four stage cards.
3. **Read local state** for the student(s) in scope: `status.md`, then confirm against the files
   using the mapping table above (status notes drift — the files win, as in `resume.md`).
4. **Match card ↔ folder by name.** Cards use short names ("Demi", "Zheng Yi"); folders use slugs
   (`foo-de-mi`, `lai-zheng-yi`). If a match isn't obvious, ask — never create a second card for
   someone who may already have one. No card and Evan confirms they're a real client → create one:
   `Task name` = the name Evan uses, `Area` = University Research Agent, `Project` = Clients,
   `Parent-task` = the right stage card.
5. **Work out the diff, then show it before writing anything.** Per student: stage move (from →
   to), new "Delivered" lines, new "Feedback" lines. Take delivered dates from `status.md` "Recent
   actions" or the output file's date — don't invent one; if unknown, ask.
6. **Wait for Evan's yes**, then write: `Parent-task` for a stage move, card body for the log.
   Append to the body — never overwrite lines already there (Evan edits these by hand too).
7. **Re-query and confirm** each changed card now shows the intended `Parent-task`.

For the no-argument board check, steps 2-5 across every client card and every folder in
`data/students/`, then report as one table: name · Notion stage · local stage · last delivered ·
feedback (received / outstanding / never asked). Fetch a card's body only if it's a client card.
List folders with no card and cards with no folder separately — don't auto-create either.

## Edge cases & rules

- **Feedback is something only Evan knows.** It arrives over WhatsApp, not in any file. Never mark
  feedback as received unless he says so in this session.
- **Setting a relation can replace or merge.** After changing `Parent-task`, a card must sit under
  exactly one stage card — step 7 is not optional. (Seen during the 2026-08 workspace migration:
  the first relation write after a change sometimes merged with the old value instead of replacing it.)
- **Don't add columns or options to the databases.** They're shared with Evan's other areas; a
  schema change there is a decision for him, not a sync side-effect.
- **Leave `Status` and `Due` alone** unless Evan asks — those are his own planning fields.
- **If an address above fails**, re-find it with one keyword search, fix this table, and re-date the
  "verified" heading.
- **Never search to sync.** No `WebSearch`, no `firecrawl_search.py` — this is a read of local files
  and a read/write of Notion, nothing else.

## Done when

Every card in scope sits under the stage its files say, its "Delivered" log matches what was
actually sent, feedback lines reflect what Evan told you, and he's seen the list of clients with
feedback outstanding.
