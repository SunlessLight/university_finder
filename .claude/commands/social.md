---
description: Draft social media posts for a topic (dispatches the social-post-drafter agent)
argument-hint: [topic or title for the posts]
---

Run `workflows/social_media.md`. Draft social media posts for a given topic.

Dispatch the **`social-post-drafter`** agent (one dispatch, not parallel — one draft per call). Its prompt is short by design: the agent file is its instructions, so pass only what it cannot derive from the repo —

- `$ARGUMENTS` if I gave any. That is usually the topic or title you want posts about, which is the one thing a cold agent genuinely cannot recover.
- Anything from this session it can't see: context, a decision we made and its reason, work that is deliberately half-finished.

**Don't draft posts yourself first.** The agent reads the logic, you read the draft.

When it returns, **check its `Gate:` line before anything else.** If it reports the
confidentiality check failed or unresolved, that outranks the draft — surface it first and
do not present the draft as ready (mirror how `commit.md` treats a flagged safety-sweep
finding: it outranks the plan, and nothing is presented as done until it's resolved). Only
once the gate reports passed, read `.tmp/social/<topic-slug>.md` and present it to me.

Then **wait.** I approve the draft before anything is posted.

**This feature does not post to any social media platform.** The drafted posts are for your review and external sharing only — there is no posting integration. You must copy the posts manually to the platform of your choice.

This is a launcher, not a planning exercise. Do not enter plan mode (CLAUDE.md).
