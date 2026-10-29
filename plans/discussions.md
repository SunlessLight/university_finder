# Discussions: ideas and open questions

*One running file, so nothing gets lost between sessions. Written for Evan.*

**How this file works**
- **Open** (top): questions still being talked about. Each has Claude's default answer.
- **By date** (below): what came up in each session. Newest first.
- Once something is decided, it also goes into `decisions/log.md`. Once it's a job to do, it goes into
  `business/additionals.md` or a plan. This file keeps the thinking; those keep the outcome.
- No student names here (this file is in git).

## Open

| # | Question | Claude's default | Raised |
|---|---|---|---|
| O1 | Remove "List status" from the whole system before 10 Nov, or just hide it from students? | Hide it now (the PDF leaves it out); remove it inside the system after 10 Nov | 2026-10-29 |
| O2 | Cost breakdown table on each university's page in the PDF? | Yes: tuition + living x years, exchange rate and its date, then the RM total. Script-made, no AI text | 2026-10-29 |
| O3 | "Money to show (visa)": keep it? | Drop it from the list. It's the bank balance a visa needs, not a cost, and today's cells say nothing useful. It belongs in the how-to-apply guide | 2026-10-29 |
| O4 | New "Application requirements" field (essay, recommendation letters, interview, test) | Yes, as a fixed list of words a script can check, e.g. "Essay · 2 recommendation letters · Interview" | 2026-10-29 |
| O5 | Is RM 50 for 20-30 universities too cheap? | Don't change the price before the pilot. Measure the real cost and hours on the first paid lists, then decide | 2026-10-29 |
| O6 | Turn it into an app at USD 5 for 8-12 universities? | Not now. See 2026-10-29 below | 2026-10-29 |
| O7 | Store researched universities and reuse them for the next student | Good idea, after the pilot. See 2026-10-29 below | 2026-10-29 |

## 2026-10-29

**Decided** (also in `decisions/log.md`)
- **Missing deadline:** the cell says just "Not published". The row's "Info source" says
  "Official page, checked on <date>". This replaces both the backlog's R29 wording and decision 3's.
- **The student gets a portrait PDF, not a spreadsheet.** A spreadsheet (CSV, a plain text file with
  commas between cells) has no formatting and only one sheet, so it looked packed and the glossary had
  to be a separate file. PDF layout:
  1. **Student profile** at the top: the details that used to repeat in every row (grades, course,
     countries, budget, English score), plus the date the list was prepared.
  2. **Summary table** of the important columns only (about 8).
  3. **Key** under the table explaining the judgment labels (score, Reach/Match/Safety, Grades vs entry bar).
  4. **One card per university**, grouped like the website's list screen (course, getting in, cost,
     scholarships, after you graduate).
  5. **Glossary** at the back.
- **Columns** (35 now → about 26):
  - Drop: List status (from what students see), Tier (it's just the score cut at 75 and 55),
    Student grades (moves to the profile), Notes (a catch-all where chatter slips in).
  - Merge: City + Country; four scholarship columns into two ("Scholarship", "How to get it").
  - Move to the university report: Student life.
  - Numbers only: both ranks (ranking name and year go in the header), Annual tuition, Total tuition,
    Living per year. Calculations go to the research notes; a check rejects any extra text.
- **The website stays a demo.** The PDF is the product. Building the website into the real product is
  a decision for after the pilot.
- **Budget question:** Evan added RM 200,000 as the lowest choice; the form reader now reads it.

**Before 10 Nov, if the new list goes out then** (Claude's view, not yet a plan)
1. Step 2b fixes already in the backlog (R27, R28, R29 with the new wording, R30a, R32).
2. New column list + the research helper's instructions (numbers only, application requirements).
3. A new script that builds the PDF.
4. Rebuild the sample pack and website demo on the new columns (step 2c).
5. Update the workflow files, README and CLAUDE.md.
6. After 10 Nov: remove "List status" inside the system (27 files mention it, mostly the report,
   decide and apply-guide stages, which paid lists don't use).

**Pricing and cost** (evidence from `token_cost_report.md`, one measured run only)
- Known: one US pass of 10 universities used about 700,000 tokens in its helpers. That's about
  USD 2-3 at pay-per-use API prices. Evan pays a flat Claude subscription, not per token.
  The main session's share was never measured.
- Guess: a full client (3 countries, about 30 universities, plus checking and fixing) is roughly
  USD 8-15 at API prices. That's about the same as RM 50, so on pay-per-use there'd be almost no margin.
- Unknown: how many clients one subscription can handle per week before hitting usage limits; how
  many hours of Evan's time each client takes; whether families would pay more.
- The real limit today is capacity (usage limits + Evan's hours), not a token bill.
- **Next step (5 minutes per run):** on the first paid lists, type `/cost` after each country pass and
  note the time spent. Add the numbers to `token_cost_report.md`.

**App at USD 5 for 8-12 universities** (Claude's honest opinion: not now)
- Per university it's about the same price (RM 50 / 25 ≈ RM 2 each; USD 5 / 10 ≈ RM 2 each), so it
  doesn't fix the "too cheap" worry. It just splits the sale.
- An app needs a server, logins, payments and PDPA-safe storage of grades and finances: months of work.
- App users expect instant answers, but a pass takes minutes and needs Evan's checks.
- Revisit after the pilot, with real cost and willingness-to-pay numbers.

**Reusing research (the "database" idea)**
- Sound: many students pick the same universities (Monash, UCL, NUS…), and those facts get researched
  again each time. 27 existing lists already hold about 490 rows.
- Catches: fees and deadlines change every year, so a stored fact needs its "checked on" date and a
  re-check; and the same university with a different course is a different row.
- A smaller first version: before researching a university+course, look for an existing row less
  than X months old and only re-check it. After the pilot.
