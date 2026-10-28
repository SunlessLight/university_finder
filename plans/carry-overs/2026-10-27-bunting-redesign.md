# Carry-over: bunting redesign + demo top-5 edit (2026-10-27)

> **Finished 2026-10-28.** Demo edit committed on branch `bunting-demo` (`d123f53`); bunting submitted as [SHORTLISTED_v3.png](../../business/launchx/Bunting_design/SHORTLISTED_v3.png). What's left lives in `STATUS.md`. History only below.

**Goal:** a bunting for the 10–13 Nov booth that a passer-by gets in 3 seconds ("it's for me, it does this"), using a screenshot of the demo website's list.
**Where it stands:** layout agreed in chat; the demo edit is planned but not started. Waiting on Evan's "go" (last question asked). Bunting and pilot plan were both due 27 Oct.

## Done this session
- Reviewed Evan's first draft → [business/launchx/Bunting_design/1.png](../../business/launchx/Bunting_design/1.png) against the Notion task "Make the bunting and booth materials, include the good text" · checked by: viewing the image. Must-fix found: empty Canva image box bottom right, "Don't Know" (capital K), QR label "Scan for more info" (brief says "Scan to book your spot").
- Found the intake form's grade grid takes A-level grades only (A*–E) → [forms/intake.json](../../forms/intake.json) "Select the grades…" · checked by: reading the file.
- Found the demo website's source → [prototype/](../../prototype/), list fed from [business/sales/sample_pack/sample_master_list.csv](../../business/sales/sample_pack/sample_master_list.csv) via [prototype/_build/gen.py](../../prototype/_build/gen.py) (never hand-edit `data.js`). Live site = separate repo `SunlessLight/Uni-finder-demo`, not on this laptop. Rows show in CSV order, not by score.
- Build log, decision log, Now box updated.

## Decisions (don't re-ask)
- Bunting picture = the demo website's list, cropped to 3–4 rows, in a Canva device frame, with 2–3 gold labels (total cost in RM, entry requirements, scholarships; not Reach/Match/Safety, testers don't understand it). Because customers get that website plus a spreadsheet download. Evan.
- Tick list dropped; "20–30 universities" folded into the fix line; proof line "Facts from each university's official page" kept, small. Claude suggested, Evan agreed.
- Layout top to bottom: pain headline → "We'll find 20–30 universities for you" → programme badges → website in device frame → QR "Scan to book your spot" → proof line → name and logos. Claude suggested; Evan didn't object.
- Demo top 5 rows: MIT, NUS, Monash, Cambridge, Tsinghua. Evan.
- Reach/Match/Safety labels are not changed to force a spread. With Cambridge = Reach: 3 Reach, 1 Match (NUS), 1 Safety (Monash). Claude, Evan didn't object.
- Cambridge row: reuse Toru's Cambridge Engineering MEng row (university facts only, all "Official page"), not research from scratch. Evan suggested the source; Claude recommended reuse plus a fee spot-check.

## Not done yet
- **Waiting on Evan:** "go" for this default plan: branch `bunting-demo` in its own worktree, local only, no push.
- **Waiting on Evan:** all pre-U students vs A-level only. Default: all pre-U, plus one intake question "Not doing A-levels? Type your programme and result" (Evan can add it in Google Forms). Unknown: who walks past the booth 10–13 Nov (ask iLabs).
- Two `business/launchx/status.md` drafts not written (need Evan's yes): designer feedback + A-level-only form + booth-audience unknown; customers get a website with a spreadsheet download.
- `Bunting_design/` and `demo_website_link.md` are untracked; not committed.
- Pilot plan (its pass line) still due 27 Oct.

## Next steps
1. Ask Evan for "go". On yes: make the worktree + branch `bunting-demo`.
2. Spot-check Cambridge's 2027/28 overseas fee on the official fees page (Toru's row has 2026/27: GBP 44,214; the sample intake is Oct 2027).
3. Copy Cambridge's university facts from `data/students/toru/master_list.csv` into the sample CSV. Strip "Toru falls under the 18-month rule". Redo Student grades, Grades vs entry bar, Admission likelihood (expect "Reach (test + interview)", like Oxford) and Desirability for the sample student (check `business/sales/sample_pack/` for its grades and weights).
4. Reorder so the first 5 rows are MIT, NUS, Monash, Cambridge, Tsinghua. Re-run `python prototype/_build/gen.py . prototype/_build/data.template.js` (check usage line first). Open `prototype/index.html` and show Evan.
5. Screenshot 3–4 rows at 200% browser zoom for the bunting.

## Read first
- [prototype/BUILD_PLAN.md](../../prototype/BUILD_PLAN.md): rules (sample student only, `window.DATA`, no `data/students/` in the demo).
- The Notion bunting task (above): wording, colours, tests, A4 sign.
- [decisions/log.md](../../decisions/log.md), last two bunting entries.

## Gotchas
- Never put Toru's name, grades or label into the sample; copy university facts only.
- The sample CSV is also the sales sample pack; its other files won't match after the edit.
- Fetching the live demo URL shows only the header (the list is drawn by script). Use the local `prototype/`.
