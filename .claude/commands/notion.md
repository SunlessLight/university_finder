---
description: Sync the Notion client board with local student files (wraps workflows/notion_sync.md)
argument-hint: [student-slug]
---

Run `workflows/notion_sync.md`.

- `$1` empty → board check across every client: stage, last delivered, feedback outstanding.
- `$1` given → sync that one student. If it doesn't match a folder under `data/students/`, list the
  folders and ask which student — don't guess.

The non-negotiable parts of that workflow: **the local files win over Notion**, every query and
write is scoped to `Area = University Research Agent`, and **only name / stage / what was delivered
/ feedback gist ever goes into Notion** — never grades, finances or any profile field.

**Show me the planned changes and wait** before writing to Notion. Never mark feedback as received
unless I told you in this session.

This workflow IS the plan. Do not enter plan mode (CLAUDE.md).
