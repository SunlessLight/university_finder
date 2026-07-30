# Cutting token cost in the university_finder WAT pipeline

> **Status:** Session A (Changes 1+2) done 2026-07-30 — see "Session A" note below. Changes
> 3-7 not yet executed as of this note.
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

## Execution order (session split)

The same rule that produced this plan applies to executing it: bulk file generation belongs
in a fresh session, not at the tail of a long one. Change 1 alone rewrites a 62,703-char file
into ten.

| Session | Changes | Why grouped |
|---|---|---|
| A | **1 + 2** | Both edit `.claude/agents/row-filler.md`. Splitting them across concurrent sessions would race the same file — the same write-fence rule `00_overview.md` applies to report-writers. Largest session; start it fresh. |
| B | **3 + 4** | Both touch `workflows/resume.md`, and 4 is cleanup done while the file is open. 3 also edits `shortlist_schema.py` + `check_master_list.py`. |
| C | **5 + 6 + 7** | Disjoint small edits: one SKILL.md description, two settings.json files, one CLAUDE.md note. |

**A and B both edit `tools/shortlist_schema.py`** (A adds `--contract`, B adds
`STATUS_BUDGET`) — run A to completion first, or accept a merge. C is independent of both
and can run any time.

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
