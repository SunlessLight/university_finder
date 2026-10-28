# Carry-over: fact audit → fixes (2026-10-28)

**Goal:** everything a student receives is factual: information, not advice. No guesses, no
chatter, and judgments labelled as judgments.
**Where it stands:** the audit is done and committed (`b62db20`). Its findings are backlog entries
R26–R37. No fix has started yet. Evan is reading the summary and doing his two edits (R26, R37).

## Done this session
- Nine read-only helpers audited one part each → [fact_audit/](../../fact_audit/) (nine reports +
  [00_START_HERE.md](../../fact_audit/00_START_HERE.md), the two-page summary). 282 findings, 139 High.
  · Checked by: every report's count recounted with `grep`; all reports grepped for every student
  folder name (zero hits); three findings spot-checked in the code (budget options start at RM 500,000
  in `forms/intake.json`; `flip_finalists.py` never reads `Info source`; the
  `"Not published — check portal"` sentinel at `shortlist_schema.py:109`).
- Backlog → [business/additionals.md](../../business/additionals.md): R26–R37, new steps 2b, 2c, 9, 10;
  R36 added to step 7; R26 and R37 under "Not a session". Plan →
  [plans/fact_audit_plan.md](../fact_audit_plan.md) (banner: done).
- Build log entry "2026-10-28 (5)", Now box backlog line, Notion "Shortlisted — Now" page updated.

## Decisions (don't re-ask)
- `research_notes.md` is internal and never sent to students. So its AI notes-to-self are fine, and
  R28's new check skips it. (Evan)
- Every top-10 problem became a backlog entry, grouped by cause (12 entries, not 282). (Claude
  suggested, Evan agreed by saying "continue")
- Step order: 2b (fix the tools) before 2c (rebuild the demo rows), so the rebuilt sample carries the
  new wording and passes the new check. (Claude)

## Not done yet
- **Evan's four decisions** in `00_START_HERE.md` → "Decisions for you": judgment columns (R32),
  report opinion box (R34), "not found" wording, sales lines. Each has a default; R32 needs an
  answer before step 2b writes its glossary rows.
- **R26 (Evan):** change the form's budget question (lowest choice is RM 500,000) and the chatty
  opening text. After his edit: `python tools/fetch_form_questions.py --check`, then update the budget
  reader in `tools/ingest_form_csv.py`.
- **R37 (Evan):** reword `business/sales/positioning.md:71` and `:76-77` before the 10 Nov booth.

## Next steps
1. Ask Evan whether he has read `00_START_HERE.md` and gone with the defaults (if he says "defaults",
   that settles all four decisions). Log them in `decisions/log.md`.
2. If he has done R26, run the form check and update `ingest_form_csv.py`'s budget reader.
3. "Execute step 2b of `business/additionals.md`": R27, R28, R29, R30 part a, R32. All before 10 Nov.
4. Then step 2c (R23, R25, R31): fix the source list, rebuild the sample pack and demo.
5. Step 9 (R33, R34) before the first paid report goes out.

## Read first
- `business/additionals.md` → "Start here" and the entries your step names. The "Suggested fix" is
  the plan.
- The `fact_audit/<NN>` report and finding numbers each entry cites (e.g. "03 #16") give exact lines.
- `fact_audit/08_output_sweep.md` → regex table: the word lists for R28's new check.

## Gotchas
- R29 changes an allowed cell value. Keep the old `"Not published — check portal"` accepted, or
  every old list fails the check.
- R28's check will fail old lists. That's intended (they aren't being re-sent); don't loosen it to
  make them pass.
- Sample pack facts are fixed in the source student's list and rebuilt, never typed into
  `sample_master_list.csv`. Build it with `.venv/Scripts/python.exe` (has `pypdf`).
- The student-name privacy grep gives false positives: one short folder name matches inside an
  ordinary word in old build-log text. Check whether a hit is in new text before acting.
