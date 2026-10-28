# Carry-over: backlog trim and the two before-10-Nov steps (2026-10-28)

**Goal:** keep `business/additionals.md` (the backlog) short and current, and clear the two
backlog steps a customer would notice before the 10 Nov paid lists and booth pilot.
**Where it stands:** backlog rewritten to open entries only (8 numbered steps), committed as
`0d7a86f`. Steps 1 and 2 not started; step 1 waits on Evan's yes on R22.

## Done this session
- I10 (form-questions tool) ticked: proven live 27 Oct → [business/additionals.md](../../business/additionals.md) · checked by: `git log -- forms/` (`9822ac6`) and build log "live `--check` exit 0"
- Backlog trimmed from 1,782 to ~270 lines: open entries only, one step list split before / after 10 Nov, a "Closed on 2026-10-28 without a fix" list → [business/additionals.md](../../business/additionals.md) · old full version: `git show 10b847c:business/additionals.md`
- New entries R22 and SP1 written (see Not done yet) · checked by: grep of `row-filler.md` and `workflows/` for "waive"; a Python read of `business/sales/sample_pack/sample_master_list.csv`
- Four decisions → [decisions/log.md](../../decisions/log.md); README line → [business/README.md](../../business/README.md); Now box → [STATUS.md](../../STATUS.md); build log → [plans/build-log.md](../build-log.md); Notion "Shortlisted — Now" page got a Backlog section

## Decisions (don't re-ask)
- L2: repair the 22 Shortlist / Finalist "Not verified" rows first, not all 212. Evan.
- D2 and P2 closed: no Stage 5 runs and no corrected reports for free testers. Fix the system first; send testers something only when Evan wants them to try it. Evan.
- D5 closed: the source student (the finished one, behind the sample pack) is done. Their own fixes dropped: R2, R14, R15, and their share of R16, R17, R18, R21. Evan.
- Exception: their list is still fixed where the sample pack / demo website shows it (SP1). Claude's default, flagged to Evan, not yet confirmed or refused.
- Finished backlog entries are deleted, not ticked; entry IDs stay stable because old plan files cite them. Claude suggested, Evan asked for the trim.
- R16 apply + R17 + R21 run as one session per student (backlog step 6), because all three rewrite the same list. Claude.

## Not done yet
- **Evan's yes or no on R22** (asked, no answer yet): add "never write 'likely waived' for A-Levels / English-medium schooling" to `.claude/agents/row-filler.md` and `workflows/03_discover_longlist.md`.
- **SP1:** seven wrong cells in the sample pack and `prototype/data.js`: "Well above" on MIT, Princeton, Stanford, Harvard and Carnegie Mellon; English-waiver claims on Imperial and Oxford.
- **R18:** the UK living-cost rule (visa office monthly figure × 12) was never written into `workflows/countries/uk.md`.
- Honest-opinion point raised, no answer: the old testers' list repairs (L2, R16, R21, I9) only pay off if a list is re-sent. They could wait longer than 10 Nov.

## Next steps
1. Ask Evan for his yes on R22. On yes, run backlog step 1 (R22, then R18): type "Execute step 1 of `business/additionals.md`".
2. Backlog step 2 (SP1), before 10 Nov. **First check that the `bunting-demo` branch is merged** (see Gotchas).
3. After 10 Nov: backlog steps 3 onward, in order.

## Read first
- [business/additionals.md](../../business/additionals.md) → "Start here": the steps, the rules for every step session, and what was closed.
- The R22, R18 and SP1 entries in the same file: their "Suggested fix" is the plan.

## Gotchas
- **SP1 and the bunting demo edit touch the same files.** Another session made the demo edit on the local branch `bunting-demo` (`d123f53`, worktree `.claude/worktrees/bunting-demo`), not merged. Merge it before SP1 rebuilds `prototype/data.js`, or one overwrites the other.
- Sessions can't read `.env.example` (a deny rule), so I10's missing form-ID keys there stay unfixed.
- The sample pack's "Well above" check must skip non-US rows. Oxford, Imperial and Tsinghua have real grade bars, so their "Well above" is fine.
- Stamp the Notion Now page from the Now box only. The Now box's Next-step line was written by the bunting session, which owns syncing it.
