# Cutting token cost in the university_finder WAT pipeline

> **Status:** Session A (Changes 1+2) done 2026-07-30 — see "Session A" note below. Change 3
> (the `STATUS_BUDGET` gate) is also confirmed live as of 2026-08-02 — `resume.md` already
> carries its "history moves to research_notes.md" line and `check_master_list.py --check
> status` actively enforces it. **This banner was stale for days about that** — a plan file
> drifting out of sync with the code it describes is the same failure mode `resume.md` warns
> about for `status.md`; don't trust this note either, verify against the files. Changes 4-7
> status unverified. **Change 8 (row-filler backfill-dispatch hygiene) was executed
> 2026-08-02** — 8a/8b/8c all landed in the files, plus a new `tools/apply_backfill.py` and
> `check_master_list.py --blanks`. See the "Session D" note below for what shipped and what
> is still owed (a live end-to-end run). **Change 9 landed with it** (both bullets are in
> `check_master_list.py`'s docstring), so session E is done too.
> **How to pick this up:** open a fresh session in this repo and say
> *"execute Change N from plan.md"*. See "Execution order" at the bottom — some changes
> can run in parallel sessions, two must not.

## Context

`token_cost_report.md` diagnosed a session that hit ~185k tokens and blamed a turn-one
`@workflows/03_discover_longlist.md` mention (~16k tokens) for ~29% of the growth. That
diagnosis is directionally right but mis-prioritised, because it measured **one turn's
injection** rather than **cost over the session's life**. Two corrections change what to
fix first:

**1. The real unit is resident-token-turns, not tokens.** Every token in context is
re-billed at the cache-read rate on *every subsequent turn*. On Opus 5 with a 1-hour cache
TTL: cache write `$10/MTok`, cache read `$0.50/MTok`, output `$25/MTok`. So one resident
token in an 80-turn session costs `$10 + 80 x $0.50 = $50/MTok` — **10x the $5 sticker
input price.** A 16k file loaded at turn 1 isn't a 16k cost; it's 16k x 80.

**2. The `@`-mention was not the avoidable part.** `/longlist` would have read
[03_discover_longlist.md](workflows/03_discover_longlist.md) anyway. What was genuinely
wasted: `resume.md` (wrong workflow for that session), seven countries' playbooks, and the
222-line candidate schema — which the *main session never uses*, only the row-fillers do.
The fix is splitting the file, not changing how it's referenced.

**3. The subagent fan-out is where the multiplier lives.** Each of 8–12 `row-filler`
agents is told to read the whole 62,703-char file. That's the same waste x12, and
`.claude/agents/row-filler.md` additionally points them three times into
`tools/shortlist_schema.py` (28,481 chars ≈ 7.1k tokens).

Goal: cut per-pass token spend roughly in half and keep the main session far enough from the
200k ceiling that compaction (the most expensive single event in a session) stops happening.

---

## Change 1 — Split `03_discover_longlist.md` three ways *(largest win)*

Current: 867 lines / 62,703 chars ≈ **16k tokens**, read in full by the main session *and*
by every row-filler.

Structure it into three tiers, because the two readers need different halves:

| New file | Content (current lines) | Size | Read by |
|---|---|---|---|
| `workflows/03_discover_longlist.md` (core) | 1–111, 460–533, 756–867 | ~20,700 chars ≈ 5.2k tok | main session only |
| `workflows/countries/<code>.md` x8 | 112–459, one block each | 804–5,714 chars each | main session (1) + row-fillers (1) |
| `workflows/03b_candidate_schema.md` | 534–755 | 16,108 chars ≈ 4k tok | row-fillers only |

Country files: `uk.md`, `usa.md`, `australia.md`, `singapore.md`, `malaysia.md`,
`china.md`, `hong-kong.md`, `japan.md`. Move each block **verbatim** — the dated field-lore
blockquotes (Australian domestic-fee trap, Singapore's five-tier fee table, the SMU name
collision, XJTLU Year-2 entry, need-blind cohort drift) are the whole point of the file and
must not be summarised. Keep the shared "Cross-country (discovery only)" query block
(lines 104–111) in the core file.

**Result per country pass:**
- main session: 16k → ~6.2k tokens (**-61%**)
- each row-filler: 16k → ~5.0k tokens (**-69%**)

Preserve the existing invariant that traps live in exactly one place — core keeps the
pointer, the country file keeps the lore. Update the three files that reference the layout:
[03_discover_longlist.md:95-99](workflows/03_discover_longlist.md#L95-L99) (the "two
readers" preamble), [row-filler.md:20-27](.claude/agents/row-filler.md#L20-L27) (step 1 must
name `workflows/countries/<code>.md`, step 2 the schema file), and
[00_overview.md](workflows/00_overview.md) (stage table + tool reference).

---

## Change 2 — Stop sending row-fillers into `shortlist_schema.py`

[row-filler.md:65-80](.claude/agents/row-filler.md#L65-L80) points at
`tools/shortlist_schema.py` three times (`SENTINEL_VALUES`, `REQUIRED_CANDIDATE_FIELDS`,
`CELL_BUDGETS`). Any agent that follows the pointer reads **7.1k tokens** of Python to
retrieve about 40 lines of constants — potentially x12 per pass.

Add a `--contract` flag to [shortlist_schema.py](tools/shortlist_schema.py) that prints
those three structures (plus `SHORTLIST_HEADERS`) as JSON, ~500 tokens. Reuse the existing
`if __name__ == "__main__"` convention from the other tools; do not add a new file. Then
change the agent's wording from "see X in `tools/shortlist_schema.py`" to
`python tools/shortlist_schema.py --contract`, and add it to the existing
`Bash(python tools/...)` allow entries in [.claude/settings.json](.claude/settings.json)
(already glob-covered by `:*`, so verify rather than add).

**This is the general rule to apply everywhere:** a workflow must never point an agent at
Python source. Point it at `--help` or a purpose-built flag.

---

## Change 3 — Put a size budget on `status.md`

Measured across the 8 students: 7,275–19,065 chars, mean 12,228. The template in
[resume.md:66-89](workflows/resume.md#L66-L89) produces roughly **1,000 chars**, and
[resume.md:97](workflows/resume.md#L97) already states the rule — *"One snapshot, not a log."*
So `status.md` is running ~12x over its own design target, and it is read at the start of
**every** `/catchup`, `/longlist`, `/report`, `/decide` and `/apply-prep` session.

Convention alone failed here, exactly as the
[check_master_list.py](tools/check_master_list.py) docstring says it did for the CSV
("conventions are exactly what failed"). So enforce it in code, matching that precedent:

- Add `STATUS_BUDGET = 3000` (chars) to `CELL_BUDGETS`' neighbourhood in
  `shortlist_schema.py`.
- Add a `status` check to `check_master_list.py`'s existing `--check` set that fails when
  `data/students/<slug>/status.md` exceeds it.
- Add one line to `resume.md`'s "Updating status.md" section: history beyond the last two
  sessions moves to `research_notes.md`, which is already the free-length surface.

Then trim the 8 existing files to budget as part of this change.

---

## Change 4 — `resume.md` trim *(answers "is it simplifiable?" — barely)*

Direct answer: **`resume.md` is not your problem.** At 108 lines / 5,958 chars ≈ 1.5k tokens
it is the smallest workflow in the repo and one-tenth of `03`. Halving it saves ~$0.03 a
session. The file it *manages* — `status.md` at up to 4.8k tokens — costs 3x more, which is
Change 3.

Worth doing only as cleanup while the file is open, target ~70 lines:
- Compress the Toru war-story blockquote ([resume.md:43-46](workflows/resume.md#L43-L46)) to
  a single sentence — the lesson survives, the anecdote doesn't need four lines.
- Drop the two "Edge cases" bullets that restate step 3 verbatim.
- **Keep the status.md template intact.** It is the highest-value part of the file: it is
  what makes the output consistent, and it is the enforcement surface for Change 3.

Also note the duplication between [catchup.md](.claude/commands/catchup.md) and
`resume.md` step 3 — the command restates the cross-check list nearly word for word. That
duplication is *deliberate and correct* (the command primes a cold session before the Read
lands); leave it.

---

## Change 5 — Skills and tools hygiene *(answers "do python skills need descriptions?")*

**No — and the premise conflates two things.** Skills are `.claude/skills/<name>/SKILL.md`
with YAML frontmatter; the Python files in `tools/` are WAT *tools*, not skills, and need no
frontmatter. The distinction matters for cost:

- **Only a skill's `description` is always resident.** The body loads on invocation. So
  description length is what you optimise; body length barely matters.
- **A tool's docstring costs nothing until the file is Read** — and when it is read, a good
  docstring is what stops the agent reading the other 640 lines. Your existing docstrings
  earn their keep. Keep them; the fix is Change 2 (don't send agents there at all).

Concrete edits:
- [scoring-weights/SKILL.md](.claude/skills/scoring-weights/SKILL.md) — description is 599
  chars. Trim the trailing *"Covers the priorities->weight-key mapping, the modifiers, and
  validation."* That is a content summary, not a triggering condition, and per the
  `superpowers:writing-skills` guidance a description that summarises the skill's contents
  invites agents to act on the description instead of reading the skill. The "ALSO use if
  you are tempted to edit `tools/shortlist_schema.py`" clause is excellent — that *is* a
  trigger; keep it.
- [application-guide/SKILL.md](.claude/skills/application-guide/SKILL.md) — 378 chars,
  well-formed. No change.

---

## Change 6 — Harness settings

**Effort → `high`, project-scoped.** Add `"effortLevel": "high"` to
[.claude/settings.json](.claude/settings.json), leaving global `xhigh` untouched. Thinking
tokens bill at output rates ($25/MTok on Opus 5), and Anthropic's Opus 5 guidance makes
`high` the recommended default with `xhigh` reserved for the hardest coding work — this
pipeline mostly orchestrates deterministic tools and dispatches subagents. Use the
`update-config` skill to make the edit, and **verify the key is honoured at project scope**;
if it is user-scope-only, report that rather than silently leaving it unset.

**Plugins → keep four.** Set `enabledPlugins` in `~/.claude/settings.json` to
`superpowers`, `code-review`, `skill-creator`, `claude-md-management`; disable
`frontend-design`, `github`, `supabase`, `telegram`. This also removes the unauthenticated
`supabase` MCP server whose tool definitions render at position 0 of the cache prefix.
Expected: ~1,700 tokens off the always-resident skill listing, every turn of every session.
Again via `update-config`.

---

## Change 7 — Working habit: split plans in a *fresh* session, never after `/compact`

Direct answer to the question: **new session, and the choice between the two isn't the real
fix.**

The report's finding #2 (12 plan files, ~29,100 output tokens) understates the cost. The
output was ~$0.73 — unavoidable if you want 12 files. But those 12 Write turns happened in a
session already carrying ~150k tokens, so each turn re-read that window: `12 x 150k x
$0.50/MTok ≈ $0.90` in pure re-reads, on top of the output. In a fresh session at ~30k
resident, the same 12 writes cost ~$0.18.

`/compact` is worse than a new session on both axes: it pays a full read of the window, the
summary as output tokens, *and* a complete cache re-write (because summarising changes the
prefix, invalidating everything) — roughly $0.40 — and it loses fidelity. A new session
starts near the ~26k baseline with the plan read cleanly from disk.

So the rule to adopt: **write the big plan to a file in the session that produced it, then
open a fresh session to split it.** Bulk generation is cheap; bulk generation *late in a
long session* is not.

Add this to [CLAUDE.md](CLAUDE.md) as a short operating note under "How to Operate", next to
the existing subagent rule — it is the same principle (keep volume out of the judgement
session).

---

## Change 8 — Fix the ad hoc backfill-dispatch pattern (from `token_cost_report.md`'s addendum)

*(source: 2026-08-01/02 Francena Dominic Francis resume + backfill session — `token_cost_report.md`
addendum has the measured detail)*

That session invented a one-off "backfill mode" for `row-filler` (report values as reply-text
instead of writing a candidate JSON, since it's patching an existing longlist row, not
discovering a new one) inside a per-student plan file
(`data/students/<slug>/plans/02_uk_row_fill.md`). It worked, but the pattern isn't written down
anywhere shared, so it'll be reinvented — probably slightly differently, and with the same waste
— the next time a student's master list needs a completeness backfill. Two fixes, both cheap:

**8a — Dispatch by reference, not by paste.** When a plan file already contains the full shared
context for a batch of parallel dispatches (student profile, cell budgets, sentinels, per-row
blanks), the dispatch prompts should point at that file — *"read `plans/02_uk_row_fill.md`, you
are dispatch #N ($UNIVERSITY)"* — not re-paste the shared context into all N prompts. This
session re-pasted ~300 words of identical context into 9 separate prompts. Add this as an
explicit rule in `workflows/00_overview.md`'s "Subagents — concurrency and write fences" section
(next to the existing per-agent write-fence table around line 61-72) — it's the same "point at a
file, don't paste the file" principle as Change 2, just applied to dispatch prompts instead of
tool docs.

**8b — Backfill dispatches should write fragment files, not reply-text.** Give `row-filler` a
documented backfill mode (in `.claude/agents/row-filler.md` itself, not reinvented per-student):
when patching an existing row rather than discovering a new one, write a small JSON fragment to
`.tmp/<slug>/backfill/<uni-slug>.json` (column → value, same shape as the reply-text list used
this session) instead of reporting the values in the reply. This lets the "apply results" step
(`04_apply_*_results.md`-style) be a script that reads N fragment files and writes directly into
`master_list.csv` — the orchestrating session never has to hold and re-transcribe N full replies
into a scratch data structure the way this session's `check_budgets.py` did. Keep the existing
constraint that the fragment must not touch `master_list.csv` or run
`merge_candidates.py`/`sync_shortlist.py` (those tools treat existing rows as dupes and would
skip them) — the fragment is read by a small purpose-built apply script instead, same spirit as
`merge_candidates.py` but for patches, not new rows.

**8c — Multi-section text-file edits via script, not N `Edit` calls.** When updating many
near-identical sections of one file (e.g. appending a note to each of 9 `## University X`
sections in a student's `research_notes.md`), do it with one read-modify-write Python pass — as
this session correctly did for `master_list.csv` — instead of N sequential `Edit` tool calls each
needing a large `old_string` purely to disambiguate the match. Add this as a line under CLAUDE.md's
existing "Bulk file generation belongs in a fresh session" rule (How to Operate, item 6) — it's
the same instinct (keep repetitive volume off the turn-by-turn diff mechanism), just within a
single session rather than across sessions.

None of this touches `shortlist_schema.py`, `check_master_list.py`, or any currently-shared
workflow file besides `00_overview.md` and `row-filler.md` — low collision risk with A/B/C below.

> **Session D (Change 8 + Change 9) — done 2026-08-02.** Shipped more than the plan specified,
> because 8b's "small purpose-built apply script" turned out to be the natural home for 8c as well:
>
> - **`tools/apply_backfill.py` (new).** Reads `.tmp/<slug>/backfill/*.json`, matches each to an
>   **existing** row by `course_key`, and writes `master_list.csv` **and** `research_notes.md` in
>   one pass each. Validates everything before writing anything (all-or-nothing). Refuses: a
>   university not on the list, an unknown column (with a close-match hint), a cell over
>   `CELL_BUDGETS`, any `COMPUTED_COLUMNS` write (`Desirability`/`Tier`/`Admission
>   likelihood`/`Grades vs entry bar`/`Warnings`/`Approx total (MYR)`/`List status` — hand-typing
>   one is the 2026-07-25 bug), and any overwrite of a filled cell without `--overwrite`.
>   `--country` guards a split batch. Prints which computed columns went **stale** (it has cells,
>   not scores — it deliberately does not rescore). Idempotent: a re-run is a clean no-op.
> - **`check_master_list.py --blanks`.** Report mode (always exits 0): each row's blank required
>   columns grouped by university — the brief a backfill plan is written from. Both Change 9
>   bullets went into the same docstring.
> - **8a** → `00_overview.md`, new "Dispatch by reference, not by paste" subsection under Subagents,
>   with the two corollaries (agents report a path, not research; a tool call beats a hand-written
>   summary). **8b** → `row-filler.md` gained a two-mode table, a `## What you produce — backfill
>   mode` section, and a hardened reply cap. **8c** → `CLAUDE.md` How-to-Operate item 6.
> - Also: a `## Backfilling an existing longlist` SOP in `03_discover_longlist.md` (the missing
>   piece — the pattern had no shared home at all, which is *why* it was reinvented twice), the
>   backfill write-fence row in `00_overview.md`'s agent table, the append-vs-patch note in its
>   tool reference, a README note, and `.claude/settings.json` allow entries (Bash + PowerShell).
>
> **Verified:** both tools exercised against a scratchpad fixture — dry-run, real apply,
> idempotent re-run, and every rejection path (computed column, unknown column, over-budget cell,
> no-such-row, country mismatch, overwrite protection). Testing caught one real bug: the first
> version re-appended `research_notes` prose on a re-run, since that file has no `course_key` to
> dedupe on; the duplicate check now lives in `validate()` so `--dry-run` reports it accurately.
> **Not yet done:** a live end-to-end backfill on a real student — the next one that needs it is
> the proof. Francena is fully backfilled (`--blanks` returns zero), so it won't be her.

**Was confirmed unexecuted before this session (2026-08-02):** `grep backfill
.claude/agents/row-filler.md` was zero matches, and `00_overview.md`'s "Subagents" table had no
dispatch-by-reference rule. The 2026-08-02 Francena USA-backfill session (`token_cost_report.md`
Addendum 2) reproduced 8a and 8c exactly, one day after Addendum 1 first measured them on the same
student's UK half — direct evidence the fix needed to land in the files, not stay documented in a
plan. That is what this session fixed.

---

## Change 9 — Verification-loop discipline on budgeted files (from `token_cost_report.md`'s Addendum 2)

*(source: 2026-08-02 Francena Dominic Francis USA-backfill session)*

Two new patterns, distinct from Change 8, both about how a session interacts with
`check_master_list.py` rather than about the subagent dispatch itself:

**9a — Compute the length locally before a budgeted edit, don't discover it via a failed gate
run.** Updating `status.md` took three separate write → `check_master_list.py --check status`
→ fail → rewrite round trips (4199 chars, then 3254, both over the 3000 budget) before landing
under budget. Each round trip re-pays the file read, the edit, and the check output. A `python
-c "print(len(open(path, encoding='utf-8').read()))"` (or equivalent) run *before* writing tells
you the target immediately — cheaper than a gate call, and doesn't need the file rewritten to
find out it's still too long. Applies to any `CELL_BUDGETS`/`STATUS_BUDGET`-governed file:
draft to the known limit, don't iterate against the checker.

**9b — Run the full check, not a narrow `--check` filter, once you're fixing anything.** The
`--check status` flag answers only "is status.md's length OK" — it stayed green while an
unrelated `jargon` failure (bare "I-20" in 10 `Money to show (visa)` cells, flagged by
`apply_glossary.PLAIN_ALTERNATIVES`) sat undetected in the same file the whole time. Discovering
it took a second, separate full run. `--check <name>` exists for narrowing a *known* question
(e.g. "did my status.md trim work") — once a file is being actively edited for any reason, run
the full `check_master_list.py --student <slug>` with no filter, so every category gets checked
in the same pass instead of one flag at a time.

Add both as a short bullet under [check_master_list.py](tools/check_master_list.py)'s existing
`--check` docstring section (it already documents the flag; this is guidance on *when* to use
the narrow form vs. the full one) — no code change, workflow-discipline only. Low collision risk:
touches only that docstring.

---

## Execution order (session split)

The same rule that produced this plan applies to executing it: bulk file generation belongs
in a fresh session, not at the tail of a long one. Change 1 alone rewrites a 62,703-char file
into ten.

| Session | Changes | Why grouped |
|---|---|---|
| A | **1 + 2** | Both edit `.claude/agents/row-filler.md`. Splitting them across concurrent sessions would race the same file — the same write-fence rule `00_overview.md` applies to report-writers. Largest session; start it fresh. **Done 2026-07-30.** |
| B | **3 + 4** | Both touch `workflows/resume.md`, and 4 is cleanup done while the file is open. 3 also edits `shortlist_schema.py` + `check_master_list.py`. **Change 3 confirmed live 2026-08-02** (see status banner); Change 4 unverified. |
| C | **5 + 6 + 7** | Disjoint small edits: one SKILL.md description, two settings.json files, one CLAUDE.md note. Status unverified. |
| D | **8** | **Done 2026-08-02** — see the Session D note above. Touched `row-filler.md`, `00_overview.md`, `03_discover_longlist.md`, `CLAUDE.md`, `README.md`, `settings.json`; added `tools/apply_backfill.py` and `check_master_list.py --blanks`. |
| E | **9** | **Done 2026-08-02, folded into D** — both bullets are in `check_master_list.py`'s module docstring, added alongside `--blanks`. |

**A and B both edit `tools/shortlist_schema.py`** (A adds `--contract`, B adds
`STATUS_BUDGET`) — A is done and B's `STATUS_BUDGET` addition is confirmed merged in cleanly.
C is independent of both and can run any time. **D and E are done** (2026-08-02). Note for
whoever runs C: D added a "How to Operate" item-6 addition to `CLAUDE.md`, which is where C's
Change 7 note also goes — read item 6 first and append to it rather than assuming it's absent.
**C is now the only outstanding session** (5 + 6 + 7), plus Change 4's unverified `resume.md`
trim from B.

> **Session A (Changes 1+2) — done 2026-07-30, uncommitted.** `03_discover_longlist.md` split
> into the core file + `03b_candidate_schema.md` + `workflows/countries/{uk,usa,australia,
> singapore,malaysia,china,hong-kong,japan}.md`; byte-diffed lossless against the original
> (only the 8 country-file headers, the schema-file header, and three now-dangling
> cross-references — "the US block above" etc. — fixed, since a country file no longer has a
> USA block "above" it). `row-filler.md` step 1 now names its country file + the schema file;
> `00_overview.md` got a note under the Stage-4-subagent blockquote. `shortlist_schema.py`
> gained `--contract` (tested: valid JSON, `SENTINEL_VALUES`/`REQUIRED_CANDIDATE_FIELDS`/
> `CELL_BUDGETS`/`SHORTLIST_HEADERS`, ~630 tokens vs the ~7.1k-token file); `row-filler.md`'s
> three source-pointers now say `python tools/shortlist_schema.py --contract` instead. **One
> deviation from the plan:** `.claude/settings.json` had no `Bash(python tools/*.py:*)`
> wildcard to fall back on — every tool is listed individually — so `shortlist_schema.py` had
> **no allow entry at all** and needed one added (Bash + PowerShell), not just verified. Not
> yet done: the live end-to-end `/longlist` pass (verification step 6) and a before/after
> token-cost measurement (step 2) — both need a real student session to observe, not just a
> file diff. Worked directly in the shared working directory (no worktree) at the user's
> choice, since Changes 1+2 don't overlap 3-7's files except `shortlist_schema.py`, which
> merged cleanly with Session B's `STATUS_BUDGET` addition already landed concurrently.

## Verification

1. **Measure before changing.** `python tools/check_master_list.py --student <slug>` must be
   clean first, so nothing below is confounded by pre-existing drift.
2. **Baseline a country pass.** Note the context size reported at the end of a
   `/longlist <slug> <country>` run *before* the split.
3. **Unit-check the split is lossless:** `wc -c workflows/03_discover_longlist.md
   workflows/03b_candidate_schema.md workflows/countries/*.md` must sum to within a few
   hundred chars of the current 62,703 (headers/pointers only). No country blockquote may be
   shortened — diff each block against `git show HEAD:workflows/03_discover_longlist.md`.
4. **Contract flag:** `python tools/shortlist_schema.py --contract` returns valid JSON
   containing `SENTINEL_VALUES`, `REQUIRED_CANDIDATE_FIELDS`, `CELL_BUDGETS` and
   `SHORTLIST_HEADERS`; round-trip parses with `json.loads`.
5. **Status budget:** `python tools/check_master_list.py --student <slug> --check status`
   fails on an over-budget file and passes after trimming; run across all 8 students.
6. **End-to-end:** run one real `/longlist <slug> <country>` pass on a student with a country
   still to cover. Confirm (a) the main session read only the core + that one country file,
   (b) row-fillers cited the country file and the schema file, not `03` or
   `shortlist_schema.py`, (c) `check_master_list.py` comes back clean, (d) end-of-session
   context is materially below the baseline from step 2.
7. **Effort change:** compare the step-6 run against the step-2 baseline for output quality,
   not just tokens — if row quality drops, revert to `xhigh` for this project and keep every
   other change.

## Out of scope

- Rewriting `01_intake.md` (347 lines) or `04_university_report.md` (420 lines). Both are
  large but single-reader and single-stage — no fan-out multiplier, so the return is a
  fraction of Change 1. Revisit after measuring.
- Trimming `research_notes.md` (up to 102k chars for toru). It is the designated free-length
  surface and is read on demand, not on session start. Leave it — Change 3 sends *more* to
  it, deliberately.
- Touching `master_list.csv` layout. The 35-column schema and its budgets are settled work;
  this plan does not reopen them.
