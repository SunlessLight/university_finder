# Carry-over: form access for Claude (2026-10-26)

**Goal:** Claude can read the questions AND answers of all four Google Forms (intake, report feedback, spreadsheet feedback, survey) without Evan describing them.
**Where it stands:** The questions tool is built, committed and deployed, but Google's Forms permission isn't granted. Claude proposed adding an `answers` action to the same script first. Evan hasn't said "go" yet.

## Done this session
- Form-questions tool (backlog I10) → [tools/fetch_form_questions.py](../../tools/fetch_form_questions.py), `questions` action + `authorizeForms` in [tools/appsscript/Code.gs](../../tools/appsscript/Code.gs), README → Setup step 5, [workflows/01_intake.md](../../workflows/01_intake.md) step 0 · checked by: `--check` on a made-up form in the session scratchpad (caught every planted problem). The live run failed on permission (see Not done yet).
- Evan pasted the new `Code.gs`, deployed it as **New version**, and added `FORM_ID_REPORT_FEEDBACK`, `FORM_ID_SPREADSHEET_FEEDBACK`, `FORM_ID_SURVEY` to `.env` · checked by: the live call reached the new action (no `unknown_action`, no `unauthorized`).
- Notion mirror → new page "Shortlisted — Now" (`40525bdf03ad8167895cf78073e5a1ac`), end-of-session rule in [CLAUDE.md](../../CLAUDE.md) → Status, phone ticks pulled back in [.claude/skills/catchup/SKILL.md](../../.claude/skills/catchup/SKILL.md) · checked by: page created and edited.
- Backlog R20 (Claude as project manager / advisor / marketing director) → [business/additionals.md](../../business/additionals.md), at the bottom and in the rounds table.
- Payer replies, the done nudge, and the 27 Oct bunting deadline → [business/launchx/status.md](../../business/launchx/status.md).
- Commits: `e69b19c`, `6a39485`. Later edits (CLAUDE.md Drive line, STATUS.md, build log, this note) are not committed.

## Decisions (don't re-ask)
- Notion is a one-way copy of the files, except task ticks, which `/catchup` copies back. Summary on one page; tasks stay in the Tasks database. Claude suggested, Evan agreed ("I'll follow whatever suits").
- Same token for every form. Form IDs are addresses, not secrets. The intake form needs no ID. Evan agreed.
- R20 waits until after the paid lists go out on 10 Nov (default, not objected to).

## Not done yet
- **Waiting on Evan's "go"** for the `answers` action. Default: go.
- Forms permission not granted. Live error: "You do not have permission to call FormApp.openById". Evan should do the permission click only after `answers` is pasted in, so he clicks once.
- Survey answers have no tool. Only a manual CSV from 25 Oct sits in `data/form/`.
- Both feedback sheets are shared "Anyone with the link can view" (they hold testers' names). Make them private after `answers` works.
- One Notion task still says "27 testers" (the auto-mode check blocked the rename): "Plan how to get more people…". Evan may add allow rules in `.claude/settings.local.json`; the steps were given in chat.
- `.env.example` lacks the FORM_ID keys (it's blocked by the deny rule `Read(./.env.*)`).
- Sample spreadsheet shows "$" on the MYR column. Evan to fix (Format → Number → Custom `"RM"#,##0`).

## Next steps
1. ✅ Done 2026-10-27 (Evan said go): `answers` in `Code.gs` (matches the responses tab by form ID; never creates `Ingested at`), new `tools/fetch_form_answers.py` (intake → `data/form/intake_answers.csv`, not `responses.csv`), README step 5 + CLAUDE.md Drive line. Checked: `node --check` clean; live call reaches the old deployment (`unknown_action: answers`), as expected before the paste. Original plan: add action `answers&form=<id>` to `Code.gs`: `FormApp.openById(id).getDestinationId()` → `SpreadsheetApp.openById` → first sheet → `{headers, rows}`, same token gate. With no ID, use the bound sheet. Add a command (extend `fetch_form_questions.py` or a sibling) that writes intake → `data/form/`, feedback and survey → `data/feedback/` (both gitignored).
2. Give Evan one set of Google clicks: paste `Code.gs` → Deploy → Manage deployments → ✏️ → New version → run `authorizeForms` → Allow (covers Forms + Sheets). If no popup appears: tick "show appsscript.json" in Project Settings and add `oauthScopes` with BOTH `.../auth/forms` and `.../auth/spreadsheets` (an explicit list turns off Google's auto-detection). Same wording now in README step 5.
3. ✅ Done 2026-10-27: all 4 forms' questions + answers fetched (intake 10, report fb 12, sheet fb 15, survey 84 = manual export). `FORM_ID_INTAKE` was wrong (Evan fixed it). `--check` found the live intake form drifted from `ingest_form_csv.py`: grades grid renamed ("Select the grades for your subjects…" no longer hits `SUBJECT_GRID_MARKER`), 3 new unmapped questions, course + budget now CHECKBOX (code assumes single-select), "Doesn't matter" grid column unmapped, consent shows "[12 months]". The 36 comma warnings are false alarms (courses/budget aren't comma-split). Awaiting Evan's picks; `forms/*.json` not yet committed.
4. Evan sets both feedback sheets to Restricted. Switch `fetch_feedback.py` to the script.
5. Then I12 and I11 (backlog group 2 step 11).

## Read first
- [business/additionals.md](../../business/additionals.md) → I10, I11, I12 — the plan for step 11.
- [tools/appsscript/Code.gs](../../tools/appsscript/Code.gs) header — why everything is GET, and the token gate.

## Gotchas
- Deploying a new version never asks for new permissions. Only running a function in the editor does.
- The Drive connector returns sample rows only, cuts long cells, and can't see Forms. Don't use it as an answer source.
- Google's "collect email addresses" is a form setting, not an item, so the question list has no email column. The check doesn't require one.
- Evan has no technical background. Explain the whole picture before handing him steps; piecemeal steps confused him this session.
