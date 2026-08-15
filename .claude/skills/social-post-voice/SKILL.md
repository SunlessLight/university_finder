---
name: social-post-voice
description: >
  Use when drafting or editing social copy (a Twitter/X thread or post) about this
  repo's work — i.e. running workflows/social_media.md, the social-post-drafter
  agent, or the /social command. Sets the voice: measured numbers over hype, a real
  before/after diff, exact screenshot callouts, and the "Before you post" checklist
  every thread closes with.
---

# Social post voice — measured, not marketing

You are drafting a post about real engineering work in this repo — a token-cost
fix, an architecture change, an incident writeup — for an audience that can tell
the difference between a claim and a measurement. Write like the engineer who did
the work, not like the account promoting it.

**Honest scope:** the worked excerpt below is quoted directly from a real,
validated thread this repo drafted about its own token-cost fix. It's inlined
here — not referenced — so this skill is usable on its own: `.tmp/` is
gitignored and disposable, so nothing here depends on any file still existing
under `.tmp/social/`. When in doubt about shape or tone, match this excerpt
rather than inventing a new structure.

## Worked excerpt — measured numbers + a screenshot callout

Two blocks from that thread, kept verbatim to show the shape:

```
## 2/  [no image]

The leak: I fan out ~10 subagents to research universities in parallel.

Every prompt was ~317 words. 195 of them byte-identical across all 10.

Those prompts are tool-call inputs. They sit in the transcript and get re-read
on every remaining turn of the session.

> Note: the 195/317 figures are measured from session transcripts but are NOT
> yet in the repo — `token_cost_report.md` still says "~1,300-1,500 words".
> Fix the report first if you want them sourced.
```

```
## 3/  [IMAGE — must have]

The unit that matters isn't tokens. It's resident-token-turns.

Every token in context is re-billed at cache-read rate, every turn.

Opus 5: $10/MTok to write, $0.50 to read.
One token in an 80-turn session = $10 + 80×$0.50 = $50/MTok.

10x the sticker price.

> **Screenshot:** `plan.md`, lines 26-30. The paragraph starting
> "**1. The real unit is resident-token-turns, not tokens.**"
```

Block 2/ shows the measured-number rule in action — "195 of 317 words" beats
"reduced duplication," and the note under it is honest about what's sourced and
what isn't rather than asserting an unverified figure as fact. Block 3/ shows a
correctly-formed screenshot callout: exact file, exact line range, and a search
anchor (the heading text) in case the line numbers drift.

## Voice rules

- **Concrete measured numbers over hype.** "195 of 317 words identical" beats
  "reduced duplication." "34 words, down from 317" beats "much more concise." If a
  number isn't sourced from a real file in the repo (a report, a transcript, a line
  count), don't state it as fact — either go find it or say plainly that it's not
  yet measured (Worked excerpt 2/ above does this: it flags the 195/317 figures as
  measured-but-not-yet-in-the-repo, rather than asserting them as settled).
- **No marketing language.** No "game-changing," "supercharge," "unlock," "seamless,"
  no exclamation-point energy, no rhetorical questions used as hooks. If a sentence
  would work equally well selling a SaaS product, cut it.
- **Show the mistake, not just the fix.** The strongest tweets in the source thread
  admit something went wrong first ("Writing the fix down changed nothing," "Here's
  the part that stung," "grep backfill .claude/agents/row-filler.md → 0 matches, a
  day later"). A post that only shows the improvement reads as marketing; a post
  that shows the failure first earns the improvement.
- **Say what you're deliberately not optimising.** The source thread's 7/ names the
  real cost that stayed high (334k and 304k tokens of genuine research) and says so
  explicitly, rather than presenting the whole pipeline as now cheap. Knowing which
  number not to chase is part of the story — say it, don't hide it.
- **Short lines, one idea per line.** Look at how the Worked excerpt above breaks
  after a single clause, not at a sentence-length convention. Dense paragraphs
  don't survive as tweets.

## Real before/after diffs, not paraphrase

When the post's point is "here's what changed," build an actual before/after
pair: the real artifact (a prompt, a config block, a snippet) exactly as it
existed, with any personal detail swapped for a placeholder, followed by the
same artifact post-fix. Close **each half** with a one-line measured tally —
that tally is what turns the diff into a measurement instead of an assertion,
so don't drop it even though it's not part of the "real" file content.

Redaction is a pass you have to actually finish, not a property a file gets for
free just because a slug already reads `[redacted]`. Before calling a before/after
pair ready, re-read it once specifically hunting for anything that identifies a
real person — name, college, grades, nationality, finances — and confirm none of
it survived. Don't assume a prior redaction pass caught everything; that's exactly
the kind of check a gate script can't do for you, which is why it belongs on the
"Before you post" checklist below, not just in your head.

A fictional stand-in, invented end to end (no real student's details), showing
the shape:

```
BEFORE (one of N near-identical dispatch prompts):
  Student slug: <student-slug>. Shared context: [intake term, cell budgets,
  sentinel values, ~150 more words repeated verbatim in every dispatch].
  University: <Name> — <Course>. Blanks to research: [column list].
  # ↑ 214 words. 150 of them byte-identical across every dispatch.

AFTER (same dispatch, under the new rule):
  Read <shared-plan-file> — it has the profile, budgets, and sentinels.
  You are dispatch #3: <Name>, <Course>. Fill the columns listed for it.
  # ↑ 26 words. The other 150 now live in one file, read once.
```

## Screenshot callouts: exact file + line, never paraphrased

Every image-worthy tweet gets a callout block, formatted as a `>` blockquote right
under the tweet text, that names:

1. The **exact file** (`token_cost_report.md`, `plan.md` — not "the report").
2. The **exact line or heading** to navigate to (`Ctrl+G → line 78`, `lines 26-30`),
   or a search anchor if the line number will drift (`the paragraph starting
   "**1. The real unit is..."`).
3. What the frame should contain, stated concretely enough that someone who has
   never seen the file could still capture the right thing.

See Worked excerpt 3/ above for a callout that does this correctly — exact file
(`plan.md`), exact line range (26-30), and a search anchor for when the lines drift.

Mark each tweet's image requirement inline in its heading — `[IMAGE — must have]`,
`[image — optional]`, or `[no image]` — so the drafter (and the human reviewing it)
can tell at a glance which screenshots are load-bearing and which can be skipped
under time pressure.

## Screenshot settings (copy exactly — don't re-derive)

Every thread that includes screenshots reuses this block verbatim — the same one
the source thread above was drafted under:

```
- Ctrl+B — hide sidebar
- Ctrl+= ×3 — zoom in (mobile readers need ~16px minimum)
- Alt+Z — word wrap on, so markdown lines don't run off screen
- Minimap off: View → Appearance → uncheck Minimap
- Crop tight to the paragraph. X shows a 16:9 slice on mobile.
```

## Structure every thread follows

- **Numbered blocks** (`1/`, `2/`, ...), one per tweet, each a `##` heading with the
  image requirement tag in brackets.
- **A hook on 1/** that states the concrete before/after or the failure, not a
  teaser question — the source thread's 1/ opens with the actual dates and token
  figure before the thread even starts.
- **A closing "Before you post" checklist**, always, as the last section of the
  file — the manual, human-only verification pass that a gate script cannot do:
  placeholders that need real values (a repo link), redactions that need a second
  read, any number in the draft that isn't yet sourced. This is not optional even
  for a short thread; write at minimum one line if there's truly nothing else to
  check.

## Done when

The draft has numbered blocks with per-block image tags, every screenshot callout
names an exact file + line, every stated number traces to a real file in the repo
(or is flagged as unsourced rather than asserted), no line reads as marketing copy,
and the file ends with a non-empty "Before you post" checklist. Then — and only
then — it's ready for `tools/check_social_post.py`, which checks for leaked
confidential material, not voice; this skill is what makes it sound right.
