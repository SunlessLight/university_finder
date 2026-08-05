#1 — The @workflows/03_discover_longlist.md mention, turn one: ~16,000 tokens in a single shot
When your first message tagged @workflows/resume.md @workflows/03_discover_longlist.md, the harness pre-expanded both files into the context before I did anything:

Attachment	Size
03_discover_longlist.md (868 lines — full UK/USA/Australia/Singapore/Malaysia/China/HK/Japan playbooks)	63,918 chars ≈ 16,000 tokens
resume.md (109 lines)	6,454 chars ≈ 1,600 tokens
Skill listing (~40 skills + descriptions)	13,423 chars ≈ 3,350 tokens
Agent-type listing	4,404 chars ≈ 1,100 tokens
SessionStart hook (using-superpowers skill dump)	3,511 chars ≈ 880 tokens
Hook success log	3,908 chars ≈ 980 tokens
Deferred-tools listing	2,274 chars ≈ 570 tokens
Total first API call: cache_creation_input_tokens = 46,726, on top of a 26,403-token baseline already in cache (system prompt + tool defs) — so the session was at 73,129 tokens before I'd read a single file or run a single command. 03_discover_longlist.md alone is ~65% of that turn-one injection. It's a big file by design (every per-country trap ever learned across every student), but only the Australia/Singapore/Malaysia/China sections were relevant to Foo De Mi — the UK/USA/Japan/HK playbooks (roughly half the file) rode along for free.

#2 — Writing the 12 plan files: the most individual turns, ~29,000 tokens of output
Each plan file was its own thinking → tool_use(Write) round-trip. The Write tool itself is cheap on the result side (it just confirms "file created," ~230 chars each) — the cost was in what I had to generate: full, self-contained plan content, 12 times. Summed output across those turns: ~29,100 tokens — close to double the size of the entire status.md file. This phase (turns ~38–66) also accounts for the most distinct messages in the session — one Write call per file, 12 in a row.

#3 — Redundant tool calls (smaller, but avoidable)
status.md alone cost 19,527 chars (~4,880 tokens) to read once — it's a genuinely large per-student file.
I ran check_master_list.py three times during the gap analysis (once truncated with head -200, once via a redirect that didn't work, once finally with --limit 200) before landing on the right flag. That's avoidable duplication — same ~2,400-token output paid for twice extra.
#4 — This very question
Diagnosing this pulled the raw .jsonl transcript, wrote and ran several analysis scripts, and read back their output (~12K chars for one intermediate file alone) — a few thousand more tokens spent explaining the problem.

Bottom line
By the end of this session (last recorded turn): cache_read + cache_creation ≈ 185,338 tokens — matching your "200k+ fast" observation almost exactly. Of the ~159K tokens added during this session, the single @-mention in your first message accounts for ~29% of it, before any real work started. The 12-file plan-writing pass is the second-largest chunk and the busiest in terms of message count.

Actionable takeaway: 03_discover_longlist.md is the recurring cost here — it'll do this every time it's @-mentioned or auto-read for Stage 3 work. Worth considering whether it should be split (a short per-country index + separate per-country trap files), so a single-country session only pulls in what's relevant instead of all eight countries' worth of playbook every time.

---

## Addendum — 2026-08-01/02 session: resume + 10-agent backfill fan-out (Francena Dominic Francis)

Different session, different shape of waste. This one ran `/catchup francena-dominic-francis`,
found the Stage 3 completeness gate blocked, and executed the student's own split backfill plan
(`data/students/francena-dominic-francis/plans/01-06`): dispatched 9 parallel `row-filler` agents
in a one-off "backfill" mode (report values as reply-text, don't write a candidate JSON, don't
touch the CSV), applied the results, then closed the gate. No raw `.jsonl` pull was done for this
session (unlike the analysis above), so the numbers below are what's directly visible in the
transcript — subagent-reported `<usage>` tokens and tool-call counts — not a full trace.

**Measured: subagent fan-out cost.** The 10 dispatches that completed (9 UK backfills + 1
same-agent retry after a session-limit failure, + 1 later spot-check agent) reported
`subagent_tokens` summing to **≈334,750 tokens**, ~33.5k average per dispatch, for ~8-10 cell
values each. This is each agent's *own*, isolated context — it does not get re-billed on the main
session's subsequent turns the way resident context does, so in the report's own "resident-token-
turns" framing (see plan.md) it is a one-time cost, not a multiplier. It is also mostly
irreducible: it's real multi-page research under a "never invent a fact" rule (several WebSearch/
WebFetch/Firecrawl calls per fact) — not padding.

**The three things that *were* avoidable, all in the main session (each one gets the resident-
turn multiplier because the main session kept running afterward):**

1. **Dispatch prompts re-pasted shared context instead of pointing at the plan file.** The
   student's own `plans/02_uk_row_fill.md` already had the full shared context written once
   (student profile, cell budgets, sentinels, the backfill override). Each of the 9 dispatch
   prompts re-stated it in full (~250-350 words × 9) instead of "read
   `plans/02_uk_row_fill.md`, you are dispatch #N ($UNIVERSITY)." Same fix as Change 1/2 below:
   point an agent at a file, don't paste the file into the prompt.
2. **The orchestrating session re-transcribed all 9 replies into a scratch Python dict**
   (`check_budgets.py`) to check cell budgets before applying — content that had already arrived
   once via the task-notification relay. A structural fix exists: the backfill override could
   have each agent write a small JSON fragment to disk (mirroring row-filler's normal
   `.tmp/<slug>/candidates/<uni-slug>.json` behaviour) instead of reply-text prose, so applying
   is a script reading N files, never a manual re-type.
3. **9 sequential `Edit` calls against `research_notes.md`**, each needing a large `old_string`
   purely to disambiguate the match — no new information, pure token overhead. The same session
   updated `master_list.csv` correctly (one Python read-modify-write pass, one tool call) but
   didn't extend that pattern to the second file being updated in the same way.

**Actionable takeaway:** the fan-out research cost (≈335k tokens) is the expensive part in
absolute terms but is roughly fixed — 9-12 universities' worth of honest research doesn't compress
much further without weakening the "never invent a fact" rule. The **orchestrating session's own
duplication** (re-pasting shared context 9x, re-transcribing 9 replies, N-Edit-calls-instead-of-
one-script) is smaller in absolute tokens but 100% avoidable and, unlike the subagent cost, rides
on every subsequent turn of an already-long session. See plan.md Change 8 for the concrete fix.

---

## Addendum 2 — 2026-08-02 session: USA row-fill dispatch (same student, other half of the split)

This session ran `execute plan 03` — the USA half of the same Francena backfill (`plans/03_usa_row_fill.md` + `05_apply_usa_results.md`), while a parallel session did the UK half analyzed in Addendum 1 above. Same shape of work, and — worth stating plainly — **the same avoidable waste recurred, unchanged, less than 24 hours after Addendum 1 documented it and plan.md's Change 8 proposed the fix.** Change 8 was written down; it was not executed in `.claude/agents/row-filler.md` or `workflows/00_overview.md` before this session started, so there was nothing in the actual files to stop the pattern repeating. (Verified just now: `grep backfill .claude/agents/row-filler.md` — zero matches. The documented "backfill mode" only ever existed as prose in `plan.md` and inside the student's own `plans/*.md` files.)

**Measured: subagent fan-out.** The 10 completed USA dispatches reported `subagent_tokens` summing to **304,665** (avg 30,467/dispatch) via their own `<usage>` tags — directly comparable to Addendum 1's ≈334,750 for the 9-10 UK dispatches. Same conclusion: this is real per-fact research (official pages, `WebFetch`/Firecrawl fallback), mostly irreducible, and isolated to each agent's own context rather than the multiplier that resident main-session tokens carry.

**Repeated exactly, in the main session (each one gets the resident-token-turn multiplier, per plan.md's framing):**

1. **8a recurred — dispatch prompts re-pasted shared context 10x.** Every one of the 10 `Agent` calls re-stated the same ~130-150 words (student profile, cell budgets, sentinels, the "derive Money to show as Annual tuition + Est. living/yr" formula) instead of "read `plans/03_usa_row_fill.md`, you're dispatch #N ($UNIVERSITY)." That's ~1,300-1,500 words of pure duplication sitting in the tool-call inputs, which — same as the Write-heavy turns in Finding #2 of Addendum 1 — become resident transcript content re-billed on every later turn of this same session.
2. **8c recurred — 10 sequential `Edit` calls against `research_notes.md`**, each needing a large `old_string` (a full existing paragraph, ~150-250 words) purely to disambiguate the match, immediately after this same session had *correctly* done the CSV update as one Python read-modify-write pass (`apply_usa_backfill.py`). The two files were updated with two different disciplines in the same session, and the worse one was picked for the second file.
3. **New pattern, not previously documented — verification-loop churn on a size-budgeted file.** Updating `status.md` took 2 initial `Edit` calls, then `check_master_list.py --check status` failed (4199 chars, budget 3000), then 2 more trims and a second failure (3254 chars), before it passed on the third check. Three separate write→check→fail round trips, when a one-line local length check (`python -c "print(len(open('status.md').read()))"`) before each edit would have told me the target ahead of time instead of discovering it via a failed gate run.
4. **New pattern — narrow `--check` calls hid an unrelated failure.** After finally getting `status.md` under budget, a full (unfiltered) `check_master_list.py` run surfaced a *second*, unrelated failure (`jargon`: "I-20" in all 10 USA `Money to show (visa)` cells) that the narrower `--check status` calls never would have caught. Running the full check from the start — rather than the flag that answers only the immediate question — would have surfaced both problems in one pass instead of two.
5. **Confirms Addendum 1's 8b diagnosis directly.** All 10 agent replies (each ~150-300 words of research prose plus a two-line summary) arrived as reply-text inside task-notifications and now sit in this session's transcript permanently. Had backfill dispatches written small JSON fragments to disk instead (the fix Change 8b already specifies), the apply step would have been a script reading 10 files, and this session's resident transcript would be ~10 x 200 words lighter for the rest of its life.

**Meta-finding:** `plan.md`'s own status banner ("Changes 3-8 not yet executed as of this note", dated 2026-07-30) is stale — Change 3 (`STATUS_BUDGET` + the `check_master_list.py --check status` gate) is demonstrably live and was what caught finding #3 above. Plan-file drift is the same failure mode `resume.md` already warns about for `status.md` ("status notes drift — the files are the source of truth"); a plan file needs the same discipline.

**Actionable takeaway:** Change 8 (8a/8b/8c) is no longer a hypothetical — it has now cost roughly the same avoidable overhead twice, on two sessions, one day apart, on the same student. It should be executed before the next fan-out backfill on any student, not queued behind Changes 5-7. See plan.md Change 8's updated priority note and new Change 9 (verification-loop discipline) for the concrete fixes.
