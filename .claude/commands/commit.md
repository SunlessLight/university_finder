---
description: Review the working tree and draft commits (dispatches the commit-drafter agent)
argument-hint: [optional: why you made these changes, or a scope hint]
---

Draft commits for the current working tree.

Dispatch the **`commit-drafter`** agent (one dispatch, not parallel — there is one working
tree). Its prompt is short by design: the agent file is its instructions, so pass only what
it cannot derive from the repo —

- `$ARGUMENTS` if I gave any. That is usually the *why* behind a change that isn't written
  down anywhere on disk, which is the one thing a cold agent genuinely cannot recover.
- Anything from this session it can't see: what we were actually doing, a decision we made
  and its reason, work that is deliberately half-finished.

**Don't run `git diff` yourself first.** Reading the diff into this session is the exact
cost the agent exists to absorb — it reads the volume, you read the plan.

When it returns, read `.tmp/commit_plan.md` and present it to me: one line per commit
(subject + files), then every `NEEDS FROM YOU` and every safety-sweep flag, loudest first.
Show me the full drafted message only for a commit I ask about.

Then **wait.** I approve the split before anything is staged. On approval, run each
commit's two commands as written (`git add …` then `git commit -F .tmp/commit_msgs/…`).
Stop at the first failure and show me the error rather than improvising a fix.

**Never push.** Ask, every time, even if I pushed last time.

If the agent flags PII, a secret, or a `data/students/` path in the tree, that outranks the
commit plan — surface it first and don't stage anything until it's resolved.

This is a launcher, not a planning exercise. Do not enter plan mode (CLAUDE.md).
