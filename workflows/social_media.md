# Workflow: Social Media Posting — draft a confidentiality-checked Twitter/X post

## Objective

Turn a finished piece of repo work — a commit, an incident writeup (`token_cost_report.md`-style),
an architecture decision — into a draft social post or thread, in this repo's own voice, that has
already been checked for leaked confidential material before a human ever sees it.

This workflow **does not post anything**. There is no X/Twitter API integration here — posting
stays manual copy-paste, the same shape as the worked example at `.tmp/social/twitter_thread.md`
(read it once to see what a finished draft looks like: numbered blocks, per-block screenshot
instructions, a "before you post" checklist). This is a **utility, not a pipeline stage** — it sits
outside the four-stage student pipeline, alongside `resume.md` and `08_application_prep.md`, and
touches none of a student's data.

## Tools used

- `git log` / `git diff` (read-only) — or a pointed-to file instead of a commit range: a
  `token_cost_report.md`-style writeup, a `plan.md` decision, a specific commit. Whichever the topic
  names, read it directly rather than re-deriving it from scratch.
- `tools/check_social_post.py` — **mandatory gate**. Every draft runs through it before it can be
  called ready. (Built by a sibling task in this same plan; referenced here by path only.)
- `.claude/skills/social-post-voice/SKILL.md` — the voice skill. Invoke it when drafting so the post
  reads in this repo's voice instead of generic marketing copy. (Also built by a sibling task;
  referenced here by path only.)

## How to start

1. The user runs `/social [topic]`.
2. Dispatch the **`social-post-drafter`** agent (`.claude/agents/social-post-drafter.md`) **once —
   not in parallel.** This is judgment work, one draft, not a volume fan-out — but the agent still
   absorbs read-once `git log`/`git diff` volume itself, the same way `commit-drafter` absorbs a
   full `git diff` so the main session's transcript doesn't have to carry it.
3. The agent drafts the post, runs `tools/check_social_post.py` on it itself, and iterates until the
   gate comes back clean — then writes the result to `.tmp/social/<topic-slug>.md`.
4. The main session presents the draft **as-is** — the actual post text from
   `.tmp/social/<topic-slug>.md`, unmodified, so the user has what they need to approve or edit it
   — and waits. Approve, edit, or decline. The session never auto-posts, ever.

## Edge cases & rules

- **Pull only.** This workflow runs when the user runs `/social` and wants a draft — never
  proactively, and never riding along on `/commit` or any other command. Finishing a piece of work
  is not itself a trigger to draft a post about it.
- **Never draft from `data/students/`, `data/form/`, or `.tmp/<student-slug>/` content directly.**
  Those paths are PDPA-sensitive and out of scope for this workflow, full stop — unless the user has
  explicitly handed over text they've already sanitized themselves, in which case that text is the
  input, not the folder.
- **`check_social_post.py` must come back clean before a draft is presented as ready** — this
  mirrors `check_master_list.py` in this repo's existing pattern ("must come back clean before a
  list goes to a student"). A draft with a flagged slug or path is not ready, no exceptions by
  default — the same override-by-hand escape hatch other gates in this repo have still applies if
  the user chooses to use it, but that's their call, not the agent's.
- **Known limitation: the checker only scans the working tree, not git history.** If a draft's topic
  touches something that was once leaked and has since been scrubbed (a commit that briefly
  contained a real name or a token before being fixed), a clean scan will not catch it — say this
  explicitly to the user rather than letting a clean gate read as a guarantee it isn't.

## Done when

The draft + its "before you post" checklist sits in `.tmp/social/<topic-slug>.md`, `check_social_post.py`
has passed on it, and the user has reviewed it and either approved it, edited it, or declined it.
