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

**Honest scope:** the validated example this skill crystallizes is
`.tmp/social/twitter_thread.md` (plus the `before.md`/`after.md` diff pair it
screenshots). When in doubt about shape or tone, read that thread again rather
than inventing a new one — it's the template, not just an example.

## Voice rules

- **Concrete measured numbers over hype.** "195 of 317 words identical" beats
  "reduced duplication." "34 words, down from 317" beats "much more concise." If a
  number isn't sourced from a real file in the repo (a report, a transcript, a line
  count), don't state it as fact — either go find it or say plainly that it's not
  yet measured (`twitter_thread.md` 2/ does this: it flags the 195/317 figures as
  measured-but-not-yet-in-the-repo, rather than asserting them as settled).
- **No marketing language.** No "game-changing," "supercharge," "unlock," "seamless,"
  no exclamation-point energy, no rhetorical questions used as hooks. If a sentence
  would work equally well selling a SaaS product, cut it.
- **Show the mistake, not just the fix.** The strongest tweets in the example admit
  something went wrong first ("Writing the fix down changed nothing," "Here's the
  part that stung," "grep backfill .claude/agents/row-filler.md → 0 matches, a day
  later"). A post that only shows the improvement reads as marketing; a post that
  shows the failure first earns the improvement.
- **Say what you're deliberately not optimising.** The example's 7/ names the real
  cost that stayed high (334k and 304k tokens of genuine research) and says so
  explicitly, rather than presenting the whole pipeline as now cheap. Knowing which
  number not to chase is part of the story — say it, don't hide it.
- **Short lines, one idea per line.** Look at how every numbered block in
  `twitter_thread.md` breaks after a single clause, not at a sentence-length
  convention. Dense paragraphs don't survive as tweets.

## Real before/after diffs, not paraphrase

When the post's point is "here's what changed," build an actual before/after pair
the way `.tmp/social/before.md` / `.tmp/social/after.md` do it:

- **`before.md`** — the real artifact (a prompt, a config block, a snippet) exactly
  as it existed, with the student slug/name swapped for a placeholder. Redaction is
  a pass you have to actually finish, not a property the file gets for free: the
  example's own `before.md` still has real predicted grades in it
  (`Maths A*/Chem A*/Econs A`, line 13) even though the slug is already
  `[redacted]` — which is exactly why its thread's closing checklist carries an
  explicit, unchecked "`before.md` re-read once for student details — name,
  college, grades all gone" item. Don't mark a draft ready until that re-read has
  actually happened; don't assume a prior redaction pass caught everything. Ends
  with a one-line measured tally, e.g.
  `# ↑ 317 words. 195 of them byte-identical in all 10 prompts.`
- **`after.md`** — the same artifact post-fix, same redaction rules, same closing
  tally line for comparison, e.g. `# ↑ 34 words. The other 195 live in one file...`

The tallies at the bottom of each file are what make the diff a measurement instead
of an assertion — don't drop them even though they're not part of the "real" file
content.

## Screenshot callouts: exact file + line, never paraphrased

Every image-worthy tweet gets a callout block, formatted as a `>` blockquote right
under the tweet text, that names:

1. The **exact file** (`token_cost_report.md`, `plan.md` — not "the report").
2. The **exact line or heading** to navigate to (`Ctrl+G → line 78`, `lines 26-30`),
   or a search anchor if the line number will drift (`the paragraph starting
   "**1. The real unit is..."`).
3. What the frame should contain, stated concretely enough that someone who has
   never seen the file could still capture the right thing.

Mark each tweet's image requirement inline in its heading — `[IMAGE — must have]`,
`[image — optional]`, or `[no image]` — so the drafter (and the human reviewing it)
can tell at a glance which screenshots are load-bearing and which can be skipped
under time pressure.

## Screenshot settings (copy exactly — don't re-derive)

Every thread that includes screenshots reuses this block verbatim, the same one
`twitter_thread.md` lists under its own "Screenshot settings" heading:

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
  teaser question — the example's 1/ states the actual dates and token figure
  before the thread even starts.
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
