# Fact audit: start here

*2026-10-28. Written for Evan. Read this page first; the nine reports beside it hold the detail.*

## What this is

Nine helpers each read one part of the project and listed every place where a **guess**, **advice**,
**chatty text** or an **unexplained judgment** can reach a student, plus every rule or script that lets
it through. Nothing was changed. This is a map for fixing, not a fix.

**The labels:**
- **G (Guess):** a fact from AI memory, or hedged ("likely", "usually", "~", "confirm").
- **A (Advice):** tells the student what to do ("you should", "check the portal", "avoid it").
- **Y (Yapping):** chatter or AI notes-to-self in a student's file ("Note: I couldn't…").
- **J (Unexplained judgment):** our own score or label (0–100, Reach/Match/Safety, "Well above")
  shown as if it were a fact.
- **L (Loophole):** a rule or script that *lets* the above through, or a check that misses it.

**Severity:** **High** reaches a student or the public · **Medium** could · **Low** internal only.

## The answer in four lines

1. **Yes, it's widespread, but it's mostly the same few causes repeated.** 282 findings, 139 High.
2. **The checks don't look for it.** No automatic check looks for hedge, advice or chatter
   words, in the spreadsheet or in reports. So nothing stops it.
3. **"Official page" doesn't mean what the sales copy says.** It's one stamp per row (35 facts),
   put on by the AI itself, not a human. 58% of "Official page" rows still hold a hedge word.
4. **Some advice is built into the templates**, so it appears in every student's file however
   careful the research was.

## The products, and how each one did

| Product | Who gets it | High findings | Main problem | Report |
|---|---|---|---|---|
| Student profile (from the form) | internal, but feeds everything | 4 | Budget choices start at RM 500,000; "Forecast Grades" not understood | [01](01_intake.md) |
| University list (spreadsheet) | student | 28 in the sample + ~1,300 hedged cells across real lists | Hedges and advice in fact cells; scores unexplained | [02](02_longlist_instructions.md) [03](03_scoring_and_checks.md) [04](04_spreadsheet_text.md) |
| Glossary tab | student | inside 04 | Definitions carry advice and undated facts from memory | [04](04_spreadsheet_text.md) |
| Comparison table (picking finalists) | Evan | 1 | Scores printed beside fees as if they were facts | [06](06_report_tools.md) |
| University report (PDF) | student | 26 | "Your fit" and "Why here" sections are verdicts; no date on the report | [05](05_report_instructions.md) [06](06_report_tools.md) |
| Recommendation + calendar | student | inside 07 | The calendar shows an estimated date as a plain date | [07](07_decide_and_apply.md) |
| How-to-apply guide (PDF) | student | 17 | Self-set deadlines look like real ones; "strategy" is coaching | [07](07_decide_and_apply.md) |
| Sample pack + demo website | the public | many | Same problems, shown to every prospect | [04](04_spreadsheet_text.md) [08](08_output_sweep.md) |
| Sales and pitch documents | prospects, investors | 11 | Promise checks that no program enforces | [09](09_promises_vs_reality.md) |

How much is in what students already got ([08](08_output_sweep.md), counts only, no student named):
- **43%** of all list rows (213 of 493) are "Not verified".
- **1,827** hedge words in 42 university reports.
- **193** advice phrases in those reports.
- The spreadsheet has almost no chatter: 11 cells out of about 17,000. Chatter is mainly a
  report problem.

## Top 10 problems

| # | Problem | Label | Where to read more | Backlog |
|---|---|---|---|---|
| 1 | No check catches hedge, advice or chatter words. `check_master_list.py` looks only for jargon, and `check_report.py` only for pronouns. | L | 03 #16, 06 #10–12 | new |
| 2 | "Official page" is one AI-stamped label per row. 162 of 280 such rows contain a hedge. Sales copy says "a human has confirmed". | L | 08 #24, 09 #4–5 | L5, R9 |
| 3 | The step that makes a row a Finalist never checks whether it's verified. The sales copy and the product reports say it can't happen. | L | 09 #2 | new |
| 4 | The budget question's lowest choice is RM 500,000. A family with RM 150,000 must pick 500,000, so "Over budget" never shows for them. | G | 01 #4 | new (close to I3) |
| 5 | The official "no date" deadline wording is itself advice: "Not published — check portal". The Warnings cell says "Recognition risk — check MQA". | A | 03 #1–2, 02 #1 | new |
| 6 | Desirability, Tier, Reach/Match/Safety and "Well above" are explained nowhere a student can see. "Safety" reads like a promise. | J | 03 #4–6, 04 #22 | new (R17 is part) |
| 7 | The glossary is written from memory: advice ("Avoid it if…"), undated dates ("Opens 1 October"), money ("Roughly AUD 650–800"). It's printed in every sheet, report and guide. | A, G | 04 #1–11, 06 #19–20 | new |
| 8 | Report sections ask for verdicts: "your fit", "Why here / why hesitate", "Honest read on your fit", "The verdict". The sample MIT report is full of coaching. | J, A | 05 #16–31, 06 #1–2 | new |
| 9 | The calendar keeps only the date from a cell, so "2027-01-15 (estimated)" shows as a plain 2027-01-15. Reports and guides print no "prepared on" date. | L | 07 #23–24, 06 #6 | new (close to R9) |
| 10 | The public sample shows all of it: guessed deadlines ("~Apr 2027"), "~" rankings, "MQA: verify", opinions ("China's most competitive"), 13 cells cut off mid-sentence. | G, Y, A | 04 #14–32, 08 #42–47 | SP1 (partly) |

## What touches the 10 Nov paid lists

The paid lists use the intake form and the spreadsheet only. These are worth fixing before then.
All are small, and all are allowed under the freeze, because a customer would see them:
- **#4 Budget choices** (form). Default: add lower choices, or make it a number box.
- **#5 Fixed wording**: "check portal" → "Not published"; "Recognition risk — check" → a plain fact.
- **#1 A hedge-word check** in `check_master_list.py`, so nothing hedged goes out. This is the one
  change that protects every list after it.
- **#7 The glossary's advice lines** (about 6 entries), because every sheet carries the Glossary tab.
- The form's opening text, "Hihi! … your data is safe with me 🤩🥰" (01 #18): chatty, and it clashes
  with the consent text.

Everything about reports, guides and the calendar waits until after 10 Nov.

**Note:** another session fixed the sample pack and demo website (SP1) while this audit ran, so a
few sample-pack findings are already fixed. Backlog entry R31 lists what was still there afterwards.

**In the backlog:** these became entries **R26–R37** in `business/additionals.md`, steps 2b and
2c (before 10 Nov) and steps 7, 9 and 10 (after). R26 (the form) and R37 (the sales lines) are
your own edits.

## Decisions for you (each has a default)

1. **The judgment columns** (score, Tier, Reach/Match/Safety). *Default:* keep them, but explain
   each in the Glossary tab as "our label, made by this rule". They're part of what families pay
   for.
2. **The "fit", "verdict" and "Why here" parts of the report**, and the Stage 5 recommendation.
   *Default:* move all opinion into one box headed "Our assessment (a judgment, not a fact)". Every
   other section becomes facts with sources.
3. **What's allowed when a fact isn't found.** *Default:* one fixed wording, "Not published on
   <page>, checked <date>". No "~", no "confirm", no "likely".
4. **The sales lines** "a human has confirmed" and "can't reach Shortlist on aggregator facts".
   *Default:* reword them now to match what's true. That's a 10-minute edit to
   `business/sales/positioning.md`, and it's your wording.

## What's already solid (so it isn't lost)

- Every row carries a verification label. None is blank.
- "Not published" is already used instead of a made-up number in 133 cells.
- The rule "hard facts from the official page" is written down clearly everywhere. The gap is
  enforcement, not intent.
- Chatter in the spreadsheet is close to zero.

## Counts per report (recounted from the files)

| Report | G | A | Y | J | L | Total | High |
|---|---|---|---|---|---|---|---|
| 01 Intake | 8 | 0 | 1 | 1 | 8 | 18 | 4 |
| 02 Longlist instructions | 15 | 3 | 1 | 1 | 17 | 37 | 1 |
| 03 Scoring and checks | 1 | 2 | 1 | 6 | 17 | 27 | 9 |
| 04 Spreadsheet text | 14 | 5 | 4 | 5 | 6 | 34 | 28 |
| 05 Report instructions | 1 | 5 | 3 | 7 | 15 | 31 | 16 |
| 06 Report tools | 1 | 2 | 0 | 3 | 21 | 27 | 10 |
| 07 Decide and apply | 11 | 6 | 2 | 3 | 10 | 32 | 17 |
| 08 Output sweep | 32 | 8 | 5 | 0 | 2 | 47 | 43 |
| 09 Promises vs reality | 8 | 3 | 1 | 2 | 15 | 29 | 11 |
| **Total** | **91** | **34** | **18** | **28** | **111** | **282** | **139** |

The same problem often shows up in two reports: a rule in one, its result in another. So 282 is
the number of rows, not the number of separate problems. Most findings trace back to the top 10.
