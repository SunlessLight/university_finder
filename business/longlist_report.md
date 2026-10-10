# The Longlist Stage: how a student's university list gets built

*Written 2026-10-10 for a reader with no technical background. Every special word is explained
where it first appears and again in the glossary at the end. Figures on current progress come from
the project's own progress report, run the same day.*

---

## The short version

A student tells us their grades, their budget, the course they want and the countries they would
consider. The longlist stage turns that into a spreadsheet of real options.

For each country, the spreadsheet holds **8 to 12 universities**. Each one has **35 facts** filled
in: what it costs, what grades it asks for, what scholarships exist, when to apply, whether the
degree is accepted back in Malaysia, and so on. Every fact is read from the university's own
website, not from a comparison site and not from the AI's memory. Each university is then marked
with two separate judgements: how well it suits this particular student, and how likely this
student is to get in.

It is called a **longlist** because it is deliberately the long version. Nobody applies to 30
universities. The student reads the list, crosses most of it off, and keeps a few. Those few go on
to the next stage, where each gets a full written report.

This is the stage where most of the work happens and most of the product's value is created. If
the list is wrong, everything built on top of it is wrong too.

---

## Where this stage sits

The whole service has four steps. Inside the project they are numbered 1, 3, 4 and 5. There is no
step 2, because two early steps were merged into one and the later ones kept their numbers.

| Step | What happens | What the student gets |
|---|---|---|
| 1. Intake | The student fills in a form about themselves | Nothing yet. We now know who they are |
| **3. Longlist (this report)** | **We find and research universities, one country at a time** | **The spreadsheet** |
| 4. University report | The student picks a few favourites and we research each in depth | A long written report per university |
| 5. Decide and apply | We recommend, and lay out the deadlines | A recommendation and a calendar |

The idea behind the order is simple: **do the cheap research on many universities first, and the
expensive research only on the ones that survive.** A deep report takes far more effort than a
spreadsheet row, so it would be wasteful to write one for a university the student was always
going to cross off.

---

## What comes out: the master list

The spreadsheet is called the **master list**. Three words are worth pinning down:

- A **row** is one line across the spreadsheet. Here, one row is one university plus one course,
  for example "University of Manchester, Computer Science".
- A **column** is one kind of fact that every row has, for example "Total tuition".
- A **cell** is a single box: one fact about one university.

There are 35 columns, in nine groups. Each group answers a question the student is really asking.

| Group | The question it answers | What is in it |
|---|---|---|
| At a glance (5) | "Should I keep looking at this one?" | Where it stands on the student's list, its suitability score, a grade band for that score, the chance of getting in, and any warnings |
| What it is (6) | "What am I actually looking at?" | University, course, one sentence on how the degree is structured, country, city, one sentence on what living there is like |
| Quality (2) | "Is it any good?" | Its ranking for this subject, and its overall ranking |
| Getting in (4) | "Do my grades fit?" | What the university asks for, what the student has, how the two compare, and the English test required |
| Money (5) | "Can we afford it?" | Yearly tuition, total tuition, yearly living cost, length of the degree, and the total for the whole degree in ringgit |
| Scholarships (4) | "Can I get help paying?" | Which scholarship and where to apply, how much it covers, how hard it is to win, and the steps to get it |
| Visa and recognition (3) | "Can I go, stay, and use the degree at home?" | The money a student must prove they have to get a visa, the right to work after graduating, and whether Malaysia recognises the degree |
| Applying (4) | "What do I do, and by when?" | How to apply, the key deadline, the start date, and a short note |
| Proof (2) | "Where did this come from?" | The link to the course page, and whether the facts were checked on the official page |

Three smaller files travel with the spreadsheet:

- **Research notes.** A spreadsheet cell should be readable at a glance, so the long explanations
  (where a number came from, where two sources disagreed, hidden cost traps) are kept in a separate
  document, one section per university. Nothing is thrown away to make a cell short.
- **A glossary page.** A second sheet that explains any special term this student's list uses.
- **A score record.** A log of exactly how each suitability score was calculated, so any score can
  be explained later.

### One row, as the student sees it

This is a cut-down row from our sample pack, showing 11 of the 35 cells:

| Column | What the cell says |
|---|---|
| University | Massachusetts Institute of Technology (MIT) |
| Course at a glance | Core mechanical engineering plus a required thesis; robotics through a named module or a flexible track |
| Suitability score | 89 out of 100 (band A) |
| Grades vs entry bar | Well above |
| Admission likelihood | Reach (very selective) |
| Scholarship coverage | Admits international students without looking at ability to pay, then covers their full financial need |
| Work rights after graduating | Up to 3 years of work after the degree |
| Recognised in Malaysia? | Accredited engineering degree in a country whose engineering degrees Malaysia's engineering board accepts; confirm the exact entry with the Malaysian Qualifications Agency |
| How to apply | MIT's own application, not the shared US one |
| Key deadline | 1 January 2027 |
| Info source | Official page |

Look at the fourth and fifth lines together. This student's grades are *well above* what MIT asks
for, and MIT is still a long shot, because MIT turns away most applicants who have the grades. The
spreadsheet says both things, in two separate boxes. That separation is one of the most important
ideas in the product, and there is more on it below.

---

## How one country's list gets built

Think of a small research desk: **one editor, about ten researchers, and two inspectors.**

- The **editor** is the main AI session, steered by the founder. It decides what to research and
  in what order.
- The **researchers** are separate copies of the AI. Each is handed exactly one university and a
  rulebook. Each starts with a blank memory and cannot see the others.
- The **inspectors** are ordinary computer programs, with no AI in them at all. They do arithmetic
  and check rules, and they give the same answer every time.

That last point is a deliberate design choice. AI is good at reading a messy university website
and understanding it. It is not reliable at arithmetic or at following a rule the same way every
time. So the reading is given to AI, and the counting and checking are given to plain programs.

The desk works through one country at a time, in seven steps.

**1. Pick the country.** The student already ranked their countries on the intake form. The system
looks at which countries are on the spreadsheet so far and takes the next one. It never asks the
student "which country shall we do next?", because the answer is already on file.

**2. Name the candidates.** The editor runs 6 to 10 web searches to find 8 to 12 universities that
teach this course in this country. At this point it writes down only four things per university:
its name, the course, the city and the link. No fees or grades yet. Comparison websites are allowed
here, because the only job is to find names.

**3. Research the country once.** Some facts are the same for every university in a country: the
visa rules, how much money a student must show, work rights after graduating, how applications
work, when the academic year starts. These are looked up once and saved, so ten researchers do not
each look up the same visa page.

**4. Send out the researchers, all at once.** Each researcher gets one university. Before starting,
it reads four things: the notebook of known traps for that country (see "Lessons kept" below), the
rules for filling a row, the country facts from step 3, and the student's own profile. Then it
reads the university's official pages and writes up its one row in its own separate file.

The researchers work at the same time, which is faster. They are also not allowed to touch the
spreadsheet itself. Ten people typing into one spreadsheet at once will overwrite each other, so
each writes its own file and a program combines them afterwards.

**5. First inspection.** A program collects the researchers' files and refuses to continue if
anything is missing. It checks that every required fact is present, that every score is a number
from 0 to 5, that no university was researched twice, and that nothing from a different country
slipped in. When it fails, it names the exact university and the exact missing fact, so only that
one researcher is sent back out.

**6. Scoring and adding to the spreadsheet.** A second program calculates the suitability score,
works out the chance of getting in, converts the total cost to ringgit, attaches any warnings,
skips any university already on the list, and adds the new rows. It only ever adds. It never
changes or removes a row that is already there.

**7. Final inspection.** A third program reads the finished spreadsheet and checks it the way a
strict editor would. This check must pass before any list is sent to a student. It looks for:

- empty cells
- cells that are too long to read at a glance, or that were cut off mid-sentence
- a total cost that is obviously impossible (under RM 20,000 or over RM 3,000,000 for a whole degree)
- jargon that has a plainer equivalent
- values that are not allowed in a column
- two cells that contradict each other

Then the glossary page is rebuilt and a short handover note is written, naming the next country.

---

## The five rules that make the list trustworthy

Anyone can ask a chatbot for "ten universities for computer science in the UK" and get a tidy
table. The table will look finished. Some of it will be wrong, and nothing in it will tell you
which part. These five rules are what separate this list from that table. All five are enforced by
the inspector programs, not left to good intentions.

### 1. Hard facts come from the official page

A **hard fact** is one that costs money or closes a door if it is wrong: a fee, a grade
requirement, a deadline, a start date. These must be read from the university's own website, or
from the official application or visa website.

Comparison websites (sites that gather information about many universities) are used only to
*find* universities. They are never the source of a number, because they are often out of date or
quote the wrong figure. Each row carries a label saying whether its facts were checked on the
official page. A row without that label cannot be promoted to a finalist.

### 2. No empty cells, and no invented ones

The spreadsheet is the product. An empty cell looks like something broke. So every cell must be
filled.

That rule on its own would be dangerous, because the easy way to fill a cell is to make something
up. So it comes with a second rule: when a fact truly does not exist, the cell must say so, using
one of a short list of approved **honest non-answers**. For example:

- a university with no fixed deadline is marked "Rolling" (it accepts applications continuously)
- a university that publishes no scholarship odds is marked "No statistics published"
- a small college that is not in the world rankings is marked "Not ranked"

There is a difference between "there is no answer" and "I could not find the answer". The honest
non-answers are only for the first. If the fact exists and the researcher could not reach it, the
row has to say that plainly in its note. The inspector even catches a non-answer used in the wrong
column, since that is a sign of a researcher dodging a fact.

### 3. "Is it a good fit?" and "can I get in?" are never mixed

This is the rule the product is proudest of.

- The **suitability score** (0 to 100) says how good this university is *for this student*.
- The **admission likelihood** says how likely this student is to be accepted. It uses three
  words borrowed from admissions advisers: **Reach** (a long shot), **Match** (realistic) and
  **Safety** (very likely).

The chance of getting in is deliberately kept *out of* the score. Otherwise a famous university the
student has no hope of entering could sit at the top of their list, and a list like that is a
recipe for a wasted application year. The scoring program refuses to run if anyone tries to add
"chance of entry" into the score.

There is a second split inside "can I get in?":

- **Do my grades meet what they ask for?** This is a measurement against a published number.
- **Will they actually take me?** Some universities turn away most applicants who have the grades.

An early version of the system mixed these two up. A student with four top A-Level grades saw a row
for a highly selective US university saying their grades did not fit. Their grades fit easily. The
university was simply very hard to get into. Today those are two separate columns, and a row can
read "grades well above the bar" next to "Reach (very selective)". The final inspection fails any
list where those two columns tell conflicting stories without an explanation.

### 4. The whole degree, in ringgit

A degree in the UK usually takes 3 years. In the US it takes 4. Comparing yearly fees would make
the US look cheaper than it is. So every row shows the cost of the **whole degree**: all the
tuition plus living costs for every year, converted into ringgit.

The conversion uses a table of exchange rates (how many ringgit one pound, one US dollar and so on
are worth). The table carries the date it was last updated, and the system warns when it is more
than 90 days old. The total is an estimate for comparing options, not a quote.

### 5. Written to be read by an 18-year-old

Each kind of cell has a length limit, most between 120 and 200 characters. That is roughly one or
two sentences. A cell that goes over is flagged. It is never silently chopped, because chopping
could delete a real fact. The researcher has to say it more briefly and move the detail to the
research notes.

Jargon is replaced with plain words wherever a plain version exists: "post-study work visa"
instead of the visa's official code number. The few official names a student will have to search
for themselves are kept, and explained on the glossary page.

---

## How the suitability score works

Each researcher gives its university eight marks from 0 to 5, one for each thing a student might
care about:

1. how well the course matches what the student wants to study
2. the university's reputation in that subject
3. how the total cost compares with the family's budget
4. the right to work after graduating
5. realistic scholarship chances
6. hands-on learning (projects, placements, research)
7. location and lifestyle
8. recognition of the degree back in Malaysia

Students do not care about these equally. So on the intake form, each student ranks the eight from
most to least important. Their top priority counts for 20% of the score, their bottom one for 5%,
and the rest are spaced evenly in between. Those percentages are called **weights**: a weight is
how much one factor counts.

**The same university therefore gets a different score for different students.** Take one
university with these marks: course match 5, subject reputation 4, cost 2, work rights 4,
scholarships 3, hands-on 3, location 4, recognition 5.

- For a student who ranks **cost** first, it scores **72**.
- For a student who ranks **course match** first and cost last, it scores **82**.

Nothing about the university changed. What changed is who is asking. Scores of 75 and above are
band A, 55 to 74 are band B, and below 55 are band C.

Two fixed rules protect students from their own rankings:

- If a student says they cannot attend without a scholarship, scholarships are moved to the top
  automatically, wherever the student ranked them.
- "Is this the right course?" can never fall to the very bottom weight.

The weights are worked out by a formula from the student's form answers, and stored separately for
each student. The AI does not choose them.

### Warnings sit beside the score, never inside it

Some problems are too serious to be averaged away inside a number. The scoring program attaches
them as plain warnings next to the score:

- **Deadline passed**
- **English short** (the student's English test result is below what the university asks)
- **Over budget** (the whole-degree cost is above the family's stated limit)
- **Grades self-predicted** (the student has not sat the exams yet, so every admission judgement is provisional)
- **Recognition risk** (for careers such as engineering or medicine, the degree may not let the student practise in Malaysia)

A row with no problems says "None". That way the student knows it was checked.

---

## Lessons kept: the country notebooks

University websites are full of traps, and each country has its own. Every time a researcher falls
into one, the lesson is written into a notebook for that country, with the date. Every future
researcher must read that notebook before starting. There are notebooks for ten destinations: the
UK, the US, Australia, Singapore, Malaysia, China, Hong Kong, Japan, Taiwan and Germany.

Three real entries:

- **Australia: two fees on one page.** Australian course pages show the fee for local students
  right next to the fee for international students. On one page we recorded, the local figure for
  the full degree was about A$27,000 and the international figure was A$189,000. Comparison
  websites pick up the wrong one all the time. The notebook's rule: if an Australian yearly fee
  looks under about A$25,000, it is the local fee, and must not be used.
- **Singapore: five prices for the same degree.** Singapore's public universities list five fee
  levels depending on who the student is. A Malaysian student belongs in the third one, which is
  roughly half the price of the last one. Picking the wrong column either halves or doubles the
  cost on the spreadsheet.
- **Two universities, one abbreviation.** "SMU" is a university in Singapore and also a
  university in Texas. One researcher read the Texas website and came back with American fees.

This is why the service improves with each student. A chatbot answering the same question starts
from zero every time. Each list built here leaves the next one a little harder to get wrong.

The same habit applies to the system's own mistakes. The exchange-rate table once went two months
without an update and overstated UK totals by about 8% and US totals by about 16%. A student
noticed before we did. That is why the table now carries a date and a 90-day warning, and why the
final inspection now rejects impossible totals.

---

## Where things stand today

From the project's progress report on 2026-10-10:

- **29 students** have signed up. **28** have a master list. The 29th has not been started.
- Together those lists hold **503 rows**.
- **16** students have at least one in-depth report written on top of their list.
- **12** students are still partway through their countries.

Two honest gaps:

**About 228 of the 503 rows are still labelled as not checked on the official page.** These are not
spread evenly. 224 of them sit in eight older lists, all started before the "official
page only, every cell filled" rules came in on 29 July 2026. In the other 20 lists, 4 rows out of
213 are unchecked. So the method now in use produces verified lists, and the older lists have not
yet been brought up to that standard. A repair process exists for exactly this job (it re-researches
only the missing or unchecked cells of an existing row), but it has not yet been run across all of
the older lists.

**Most students do not yet have every country they asked for.** One country is researched per
sitting, so a student who picked four countries needs four sittings. Three lists also hold only 6
universities for their country, slightly under the 8 to 12 target.

---

## What limits this stage

- **It needs a person to start each run.** Each country, for each student, is started and
  supervised by the founder. The stage does not run on its own yet, so the number of lists
  delivered is tied to one person's hours.
- **Each university has a real cost.** Researching one university uses roughly 70,000 tokens (a
  token is the unit of AI usage we pay for), according to the earlier product review. The exact
  cost of a full country has not been measured yet. Measuring it is an open task.
- **One country per sitting is a hard limit, on purpose.** Researching 35 facts each for a dozen
  universities is about as much as one session can hold while still doing the work carefully. The
  programs refuse to mix two countries in one run.
- **Exchange rates are updated by hand.** Updating the table does not change rows already on a
  spreadsheet; those need a separate recalculation.
- **Some pages will not load the simple way.** A fee table that only appears inside a real web
  browser comes back empty to the free reading method. The system then switches to a paid
  web-reading service, which costs a small amount per page.

For the business view of these same limits (pricing, capacity, what to fix first), see the
[product review](product_review_2026-09-25.md).

---

## Glossary

| Word | What it means here |
|---|---|
| **Longlist** | The first, wide list of universities for a student. Meant to be cut down |
| **Shortlist** | The universities the student is still seriously considering after reading the longlist |
| **Finalist** | A university the student has picked for a full written report |
| **Master list** | The spreadsheet that holds all of a student's universities, whatever their status |
| **Row, column, cell** | A row is one university and course. A column is one kind of fact. A cell is one box |
| **Official page** | The university's own website, or the official application or visa website |
| **Comparison website** | A site that gathers information about many universities. Useful for finding names, not trusted for numbers |
| **Hard fact** | A fact that costs money or closes a door if wrong: fees, grade requirements, deadlines, start dates |
| **Honest non-answer** | An approved phrase for "this fact does not exist", such as "Rolling" or "Not ranked" |
| **Suitability score** | A 0 to 100 score for how well a university fits this student. Called "Desirability" on the spreadsheet |
| **Weight** | How much one factor counts toward the score, set by the student's own ranking |
| **Band A / B / C** | A quick label for the score: 75 and up, 55 to 74, below 55. Called "Tier" on the spreadsheet |
| **Reach / Match / Safety** | A long shot / a realistic option / a very likely option |
| **Entry bar** | The grades a university publishes as its requirement |
| **Tuition** | The fee paid to the university for teaching. Does not include living costs |
| **Intake** | The month and year a course starts |
| **Visa** | Official permission to enter and stay in a country, here as a student |
| **Post-study work rights** | Permission to stay and work in the country after graduating, and for how long |
| **Recognised in Malaysia** | Whether Malaysia accepts the degree, through the Malaysian Qualifications Agency and, for careers like engineering or medicine, the body that licenses that profession |
| **Exchange rate** | How many ringgit one unit of a foreign currency is worth |
| **AI researcher** | A separate copy of the AI given one university and a rulebook. It starts with no memory of anything else |
| **Program (no AI)** | Ordinary software that follows fixed rules and gives the same answer every time. Used here for arithmetic and checking |
| **Token** | The unit of AI usage that we are billed for. More reading and writing means more tokens |

---

## For the technically curious: where each step lives

Not needed to understand the above. This maps the plain names used here to the files in the project.

| In this report | In the project |
|---|---|
| The step-by-step method | `workflows/03_discover_longlist.md` |
| The rules for filling a row | `workflows/03b_candidate_schema.md` |
| The country notebooks | `workflows/countries/` |
| The researcher's rulebook | `.claude/agents/row-filler.md` |
| The 35 columns, the scoring maths, the honest non-answers, the exchange rates | `tools/shortlist_schema.py` |
| Turning a student's ranking into weights | `tools/derive_weights.py` |
| First inspection | `tools/merge_candidates.py` |
| Scoring and adding rows | `tools/sync_shortlist.py` |
| Final inspection | `tools/check_master_list.py` |
| The glossary page | `tools/build_glossary_sheet.py` |
| The repair process for older rows | `tools/apply_backfill.py` |
| The paid web-reading fallback | `tools/firecrawl_search.py` |
| The progress report | `tools/progress_dashboard.py` |
