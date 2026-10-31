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
| O5 | Is RM 50 for 20-30 universities too cheap? | Don't change the price before the pilot. Measure the real cost and hours on the first paid lists, then decide | 2026-10-29 |
| O6 | Turn it into an app at USD 5 for 8-12 universities? | Not now. See 2026-10-29 below | 2026-10-29 |
| O7 | Store researched universities and reuse them for the next student | Good idea, after the pilot. See 2026-10-29 below | 2026-10-29 |
| O8 | The demo says "15 of 15 rows are checked", but three facts aren't confirmed yet (the MQA register was read 30 Oct; rows not updated yet) | Update the rows, reword the sentence so hard facts are checked and living costs are estimates, and Evan reads Northeastern's requirements page. See 2026-10-30 below | 2026-10-30 |
| O9 | The sample's dates go out of date during the pilot | Keep Cambridge in the top 5 but show its "Deadline passed" warning on Results; move MIT to the regular round (three lines in `prototype/data.js`, not one). See 2026-10-30 below | 2026-10-30 |
| O12 | The list form no longer asks for achievements | Fine to leave off: the list doesn't use them. Stage 4 and the apply guide do, so ask at that point if a list buyer goes on to a report | 2026-10-30 |
| O13 | How does each buyer's list get its MQA check? | A small script that looks each university up live, plus a short file of matched register names. No full database. Build after 10 Nov: professional accreditation is what matters most for regulated courses. See 2026-10-30 below | 2026-10-30 |

## 2026-10-30

**MQA register without a browser (O8, O13)**
- **Found:** eSISRAF (MQA's foreign-degree register) can be read by a script. The page gets its data from
  `get_negara.cfm`, `get_institusi_json.cfm` and `get_result.cfm`. The old note saying it needs a browser
  was wrong. Read this way, MIT gave the same 4 rows as the 17 Oct browser check.
- **Size:** 27 lists hold 493 rows but only 207 different universities, 101 of them used more than once.
  One lookup is about 3 requests, so a full client takes minutes. Nothing needs storing in advance.
- **The catch:** matching names. Loose search words hit the wrong place: "MASSACHUSETTS" returns Amherst
  first, "MELBOURNE" also returns RMIT, Monash has 5 entries, and NTU only finds an old "Nanyang Univ."
  entry with no rows. So the one thing worth keeping is a short file of matched register names.
- **Results for the 14 sample universities (read 30 Oct):**
  - Named mechanical or mechatronics rows: Monash Clayton (Mechanical, Mechatronics), UNSW (Mechanical,
    Mechatronics), Melbourne (Mechanical and Manufacturing only).
  - Broad Bachelor of Science row only: MIT, Princeton, Stanford, Harvard, Rose-Hulman, Northeastern.
  - University listed, but no engineering row: NUS, Cambridge, Imperial.
  - Chinese-language studies rows only: Tsinghua.
  - Not listed: NTU.
- **How to read that:** it's the public-service register, listed by broad field. "No row" doesn't mean a
  degree isn't recognised, and a listing doesn't prove the engineering route. Accreditation and the
  professional body stay the real gate, so the wording on the list matters more than the lookup.
- **Can the professional bodies' sites be reached? (plain script, front pages only, 30 Oct)** Refused:
  BEM and EAC (406), MIA (403). Loaded: MMC, LAM, MBOT, Engineers Australia, Engineering Council, ABET
  (a tiny page) and Pharmacy Board (a tiny page). Malaysian engineering programmes can't be confirmed from
  EAC's own PDFs, so helpers use the university's page and MQR. The ABET lookup in R16 hasn't been run.

**Two forms, and how many grades Evan still checks**
- Split the intake into a list form and a report form (`plans/intake_forms_plan.md`). The report
  includes "your fit", grades are one text box for every programme, and budget stays a dropdown.
- **20-clean-forms tally: 0 of 20.** AI tidies the grades and a script checks them. Evan looks at raw
  vs tidied for 30 seconds until 20 forms in a row need no correction, then the look stops (R41).
  +1 for a clean form, back to 0 for a correction.
- The real forms differ from the plan in places. Three of those are open questions: O10, O11, O12.

**Sample pack rebuild (T8) raised two questions**
- **"15 of 15 rows are checked" (O8).** The website and every PDF card say the row was checked on the
  official page. T7 left four things not confirmed there: the MQA register on all rows, Northeastern's
  application requirements, Tsinghua's living cost, NUS's living cost. The first one matters most,
  because recognition in Malaysia is a hard gate for an engineering student.
- **Dates that pass (O9).** Cambridge's deadline (15 Oct) has passed, so its PDF card says "Deadline
  passed", but the website's Results screen still shows it in "5 to look at first" with no warning.
  The Decide screen tells the student to aim for MIT's early round on 1 Nov, which will be over
  before the booth opens on 10 Nov.

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
- **Settled later the same day** (were open questions O1-O4):
  - List status: hidden from students now (the PDF leaves it out); removed inside the system after 10 Nov.
  - Each university's page in the PDF gets a cost breakdown table: tuition + living x years, the
    exchange rate and its date, then the RM total. Script-made, no AI text.
  - "Money to show (visa)" leaves the list and moves to the how-to-apply guide. It's the bank balance
    a visa needs, not a cost.
  - New "Application requirements" field, as a fixed list of words a script can check, e.g.
    "Essay · 2 recommendation letters · Interview · Test: ESAT".

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
