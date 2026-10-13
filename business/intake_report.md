# Intake report — how a student gets into the system

*Written 2026-10-10. This explains the first stage of the service, called "intake", for a reader with
no technical background. It is based on the written procedure for the stage, the four small programs
that carry it out, the question list of the live form, and counts taken from the 29 student records
on file today.*

---

## The short version

Before we can research a single university for a student, we need to know two things: **who they
are** (their grades, their budget, their English level) and **what they want** (which countries,
which course, what matters most to them).

Intake is the stage that collects those two things. The student fills in one free online form with
about twenty questions. A small program then turns their answers into a tidy, private record. A
human checks the handful of answers the program was not sure about. After that, the student is
ready for research.

It is the least glamorous stage and the most important one. Every later step (finding
universities, scoring them, warning about cost, judging the chance of getting in) reads from the
record that intake creates. If intake gets something wrong, everything after it is wrong too, and
it will not look wrong.

---

## Some context first: what the whole service does

The service takes a Malaysian student who is finishing A-Levels (the two-year pre-university course
many Malaysian students take before a degree) and helps them choose where to study. It works in
four stages, and each stage narrows the options:

| Stage | Plain name | What comes out |
|---|---|---|
| 1 | **Intake** (this report) | A private record of who the student is and what they want |
| 3 | The long list | A spreadsheet of candidate universities, scored and with warnings |
| 4 | The deep reports | A detailed written report on each university the student shortlists |
| 5 | The decision | A recommendation, an application plan and a calendar of deadlines |

There is no Stage 2. Stages 1 and 2 used to be two separate interviews, one about the student and
one about their wishes. They were merged into a single form in July 2026, and the other stages kept
their old numbers.

A good way to picture intake: it is the form you fill in at a new clinic before you see the doctor.
The doctor cannot prescribe anything safely without knowing your allergies and your history. We
cannot recommend a university without knowing a student's grades and budget.

---

## What the student sees: one form

The student opens a Google Form (a free online questionnaire tool from Google) on their phone.
The poster advertises it as taking two minutes. There is no payment, no account to create and no
call to book.

Here is what it asks, and why each question earns its place.

| What we ask | Why we need it |
|---|---|
| **Email address** | It is how we recognise a returning student. More on this below. |
| **A nickname** (not a legal name) | So the reports can address them. We chose not to hold real names. |
| **Race** | Some Malaysian government scholarships are open only to certain groups. We use this to avoid recommending funding a student cannot apply for. It is never used to score a university. |
| **Expected grade in each subject** (a grid of 12 A-Level subjects; they skip the ones they don't take) | To judge which universities they can realistically get into. |
| **The month and year their real results come out**, and whether they are applying with forecast or actual results | To know how firm the grades are. |
| **English test taken, and the score** | Most overseas universities require one. |
| **Their desired course** (one pick from a list of 38) | To know what to search for. |
| **Which countries they would consider**, and which one matters most | To know where to search, and where to start. |
| **How important each of eight things is**: cost, scholarships, university ranking, course ranking, job prospects, recognition back home, location, hands-on experience. Each gets "Must have", "Important" or "Nice to have". | To score universities according to *this* student's taste and not a generic league table. |
| **Total budget for the whole degree** (three bands: under RM 500,000 / RM 500,000 to 1,000,000 / above RM 1,000,000) | To warn when a university costs more than the family can pay. |
| **Is a scholarship a must?** (Yes / No) | If yes, a university with no scholarship route is not a real option. |
| **Do they want to work abroad afterwards?** | It changes which countries make sense. |
| **Location and lifestyle preferences** (for example low crime, a Malaysian community nearby, good public transport) | To describe daily life accurately in the reports. |
| **Optional:** other fields they are curious about, universities already in mind, achievements and activities | To compare their activities against what admitted students typically have. |
| **Consent** | Permission to store and use their answers. Without it we keep nothing. |

### What we chose not to ask

The form used to be longer. We removed age, gender, nationality, home town, the name of their
college, when they want to start, and which scholarships they plan to apply for.

The rule we applied was simple: **if nothing later in the process uses an answer, the question is
only a nuisance.** Every extra question makes it more likely a busy 18-year-old gives up halfway.
Some of the removed questions also asked for sensitive personal details we had no use for, and not
holding data you don't need is the cheapest form of privacy protection.

Two details are worth pointing out because they show the thinking:

- **We ask for the total budget, never the yearly one.** A British degree takes three years and an
  American one takes four. Comparing them by yearly cost makes the American one look cheaper than
  it is.
- **We don't ask when they want to start.** The student should pick a start date after seeing the
  research, not before.

---

## What happens after they press Submit

Four steps, always in the same order. Three are done by small programs. One is done by a person.

A quick word on who "runs" these. The founder works with an AI assistant (Claude, made by
Anthropic). The assistant reads a written procedure and runs the programs in the right order. The
programs themselves contain no AI at all. A **program**, or **script**, is a fixed list of
instructions that a computer follows exactly the same way every time.

That division is deliberate, and it is the core design idea of the whole project: **AI does the
thinking, plain programs do the repetitive work.** An AI is good at judgement but can make a
slightly different choice each time. If you chain five steps that are each 90% reliable, the whole
chain is right only about 59% of the time. A plain program copying an answer from a form into a
record is right every time, so we never spend AI judgement on it.

### Step 1 — Collect the new answers

Google stores every form answer as a row in a spreadsheet. The first program fetches only the rows
we have not processed yet.

It knows which ones are new because the spreadsheet has an extra column called "Ingested at"
("ingested" means "taken in and processed"). A blank cell means "not done yet". The record of
who has been processed therefore lives in the spreadsheet itself, so it survives even if the
founder's computer is lost.

### Step 2 — Convert each answer into a clean record

The second program reads each new answer and creates a private folder for that student containing
two files:

- a **"who you are" file**: grades, English level, budget, and which official bodies need to
  recognise the degree;
- a **"what you want" file**: countries, course, priorities and lifestyle preferences.

Most of the work here is translation. People type things in a human way, and the later stages need
them in one standard form. The worked example in the next section shows this in detail.

Both of these first two steps can be run in **preview mode** (the technical name is a "dry run"),
which shows exactly what would happen without saving anything.

### Step 3 — A person reviews what the program was unsure about

The program is written to know the limits of its own certainty. When an answer cannot be converted
with confidence, it does not guess. It leaves the item blank and adds it to a "needs review" list
for that student. The founder then goes through that list with the AI assistant, and sometimes
messages the student, before any university is scored.

Today the program raises a flag in only a few situations:

- the student typed an extra field of interest in their own words, and it seems to mention a
  licensed profession (for example the word "law" appears). A person checks whether that is what
  the student meant;
- the student picked a country we don't yet cover, such as Canada;
- the student somehow gave no course at all, so there is nothing to search for.

Everything else, including grades, budget, scholarship need and the main course choice, comes from
fixed-choice questions, so the program can convert it with no doubt.

### Step 4 — Tick them off

Only after the records are written and reviewed does the last program go back to Google's
spreadsheet and stamp those rows as done.

The order matters. If something crashes halfway, the rows are still marked "not done", and the next
run simply picks them up again. If we stamped them first and then crashed, those students would
vanish from the queue and nobody would notice.

---

## A worked example

Meet Mei. **She is invented for this report and is not a real student.** Here is what she types,
what the system stores, and why.

| What Mei answers | What gets stored | Why |
|---|---|---|
| Nickname: "Mei" | A folder named `mei` | A simple, consistent label for her record |
| Math A\*, "Physic" A, Chemistry A; the other nine subjects left blank | Mathematics A\*, Physics A, Chemistry A, labelled **"self-predicted"** | Subject names are tidied. The label means every list she later receives carries a warning that her grades are not confirmed yet |
| Results: "January" and "2027" | `2027-01` | One standard way of writing dates, so nothing is misread |
| English test: "None" | Left blank | Blank means "not known yet", which is different from "failed" |
| Course: "Mechanical Engineering — machines, engines, vehicles, ships" | The course, plus a checklist: **MQA, BEM, Washington Accord** | Engineering is a licensed profession in Malaysia. Explained just below |
| Countries: UK, Australia, Canada | UK and Australia kept. Canada is **flagged for a person** | We don't cover Canada yet. We tell her so; we don't quietly drop it |
| Matters most: UK | "Research the UK first" | Her top choice is done first |
| Budget: "500,000 – 1,000,000" | A ceiling of RM 1,000,000, with her original wording kept in a note | Later stages need a number to compare costs against |
| Scholarship a must: No | No scholarship requirement | |
| Other preferences: "Low crime rate", "Good food" | Safety: yes. Food: yes. Everything else: **not known** | Not ticking a box does not mean "I don't need this". We record "not known", never "no" |

### The checklist on the course, explained

This is one of the most valuable things intake does, so it deserves a plain explanation.

In Malaysia, some careers are **regulated professions**: you cannot legally practise without a
licence, and the licensing body only accepts degrees it recognises. A student can spend four years
and RM 400,000 on an engineering degree abroad, come home, and find it does not count.

So the moment a student picks one of these courses, the program attaches the list of bodies whose
approval must be checked for every university we later suggest:

- **MQA** (Malaysian Qualifications Agency) — the government body that recognises qualifications
  in general.
- **BEM** (Board of Engineers Malaysia) and the **Washington Accord** (an international agreement
  under which member countries accept each other's accredited engineering degrees) — for
  engineering.
- **MMC** (Malaysian Medical Council) — for medicine.
- **LPQB** (Legal Profession Qualifying Board) — for law.
- **MIA** (Malaysian Institute of Accountants) and **ACCA** (a global accountancy body) — for
  accounting.
- Similar bodies for pharmacy, architecture, nursing and other health professions.

Of the 38 courses on the form, 14 carry a checklist like this. The other 24, such as business,
computer science and design, carry none, because no licence is needed and inventing a requirement
would be misleading.

**18 of the 29 students on file are aiming at a course where one of these bodies matters.** For
roughly six in ten of our students, "will this degree count back home?" is a question that can
ruin the whole investment, and general-purpose AI chat tools do not check it.

---

## Turning "what matters to me" into numbers

One more thing happens before research starts. The eight importance answers become a personal
scoring formula for that student.

The program puts the eight topics in order from most to least important. The top one counts for
20% of a university's score and the bottom one for 5%, with the rest evenly spaced between, so the
eight add up to 100%. Two universities can therefore rank in a different order for two different
students, which is the point.

Two rules override the student's own ticks:

- If a scholarship is a must, scholarship availability goes straight to the top. A student may say
  scholarships are only "nice to have" as a matter of taste while being unable to attend anywhere
  without one.
- "Is this even the right course?" can never fall to the very bottom of the formula.

There is also one thing the formula is forbidden from containing: **the student's chance of
getting in.** How attractive a university is and whether the student can be admitted are kept as
two separate answers. Otherwise a famous university the student has no hope of entering would sit
at the top of their list. This separation is the single biggest difference between our lists and
what a chat tool produces.

---

## The safety nets

Intake handles young people's personal information and feeds every later stage, so it is built to
fail safely. In plain terms:

- **No consent, no record.** If the consent box is not ticked, the program skips that person. An
  explicit "no" cannot be overridden by anyone.
- **It never invents an answer.** A blank stays blank. A blank is an open question; a made-up grade
  or budget is a wrong answer that looks right.
- **It never overwrites an existing student** unless told to in so many words. A student's folder
  later holds weeks of research, and student records are deliberately kept out of the project's
  saved history for privacy, so there is no undo button.
- **It recognises returning students by email**, even if they type a different nickname the second
  time. It skips the repeat and says which existing student it matches.
- **It refuses damaged data.** If a row from the spreadsheet has the wrong number of cells, it
  stops; it does not save a record with every answer shifted into the wrong slot.
- **The link to the spreadsheet is protected by a secret key** (a long password that only our
  program holds).
- **It can check the form against itself.** If someone rewords a question, a diagnostic lists any
  question the program no longer recognises.

---

## Lessons already built in

Nearly every rule above exists because something went wrong once with a real student. Four
examples:

1. **The RM 1 budget.** Budget used to be a blank box to type into. One student typed
   *"~ 1 million? Idk"*. The program found the digit 1 and concluded the budget was RM 1, which
   would have marked every university on earth as over budget. The fix was to replace the blank
   box with fixed bands, so that kind of mistake cannot be typed.
2. **The August student filed under May.** A date option read "August 2027 (Takes A2 in
   May/June)". The program spotted "May" first and recorded the wrong month. It now takes the
   first month written, and the form asks for the year separately.
3. **The student who appeared twice.** A returning student re-filled the form with a shorter
   nickname and silently got a second, empty record. The program now matches on email.
4. **Singapore and Malaysia glued together.** The two were once stored as a single option. A
   student who ticked only Malaysia received a list half full of Singaporean universities. They
   are now two separate countries with separate fees and entry rules.

The pattern in all four is the same: find the mistake, fix the program, then write the lesson into
the procedure so it cannot quietly return. The system gets more reliable with each student it
handles.

---

## Where things stand today (2026-10-10)

- **29 students** have a record on file.
- **All 29** have been fully reviewed; none has an unresolved "needs review" item.
- **28 of 29** have their personal scoring formula.
- **Grades:** 22 are the student's own prediction, 5 are official school predictions, and 2 are
  real results. This is expected, because students come to us before their exams, and it is why
  the warning label matters.
- **The service covers 10 destinations:** the UK, Australia, the USA, Singapore, Malaysia, China,
  Japan, Hong Kong, Taiwan and Germany. The last two were added in September 2026 because a
  student asked for them.

---

## What is still rough

An honest list, most important first.

1. **The form assumes one kind of student.** It takes for granted that the student is Malaysian,
   is doing A-Levels and wants a first degree. A student who does not fit must be corrected by
   hand, and the program will not notice.
2. **Three levels across eight topics means lots of ties.** If a student marks five things "Must
   have", the program still has to put them in an order, and it uses a fixed order (cost first,
   hands-on experience last). Within a tie, that order was not chosen by the student.
3. **Grades are taken on trust.** We have no way to verify them at this stage. We label them
   instead.
4. **Some needs are not asked about.** The record has room for halal food, prayer facilities,
   disability access, mental health support and LGBT-friendliness, but the current form does not
   ask about any of them. Our sales material names halal food and prayer facilities as a strength,
   so this gap should be closed or the claim softened.
5. **"Universities already in mind" is collected but not yet used.** The answer is stored, and
   nothing in the research procedure reads it. Eight of the 29 students filled it in. Students
   have told us they judge a list by whether
   the famous names they expected are on it, so this is worth wiring up.
6. **12 of 29 students have no spending limit on record.** Seven gave an answer that carries no
   limit ("not sure", "budget is not a problem" or "above RM 1,000,000"); the first two options
   have since been removed from the form. The other five are older records with no saved answer.
   For all twelve the "over budget" warning can never appear.
7. **The consent wording is casual.** That was fine while testing with friends. Before charging
   money we need a proper consent sentence and a disclaimer, to comply with Malaysia's PDPA
   (Personal Data Protection Act 2010).
8. **Rewording a form question can silently lose its answer.** The program finds each answer by
   looking for a key phrase in the question. The diagnostic catches this, but only if someone
   remembers to run it.
9. **The spreadsheet must never be sorted by hand.** The program identifies each student by their
   row position between collecting and ticking off. Sorting the sheet in that window would tick
   off the wrong people.

None of these makes the stage unusable. Items 1 to 6 affect the quality of what the student
receives; items 7 to 9 are operating risks.

---

## Why this stage matters to the business

- **It is the front door, and it is free.** The only thing a new customer has to do is fill in one
  form. That is about as low a barrier as a service can have.
- **It costs almost nothing to run.** The collecting, converting and ticking off are plain
  programs, so they use no paid AI time. Human effort is limited to the few flagged items. The
  expensive, slow part of the service is the research that comes afterwards, so intake is not what
  limits how many students we can serve.
- **It decides the quality of everything else.** A wrong budget makes the cost warnings wrong. A
  wrong course makes the whole list irrelevant. Careful intake is what lets us stand behind the
  later work.
- **It is where privacy is won or lost.** We collect less than we used to, use nicknames in place
  of legal names, and refuse to create a record without consent. Those habits will matter more
  once the service is paid.

---

## Word list

| Word | Meaning |
|---|---|
| **A-Levels** | A two-year pre-university qualification, graded A\* to E, widely accepted by universities abroad |
| **Intake** | The first stage: collecting who the student is and what they want |
| **Google Form** | A free online questionnaire tool. Answers land in a spreadsheet automatically |
| **Program / script** | A fixed list of instructions a computer follows the same way every time. No AI involved |
| **AI assistant** | Software that can read instructions and make judgement calls. Here it acts as the operator who runs the programs |
| **Ingest** | To take data in and process it |
| **Preview mode ("dry run")** | Running a program so it shows what it would do without saving anything |
| **Record** | The private folder of files we hold for one student |
| **Flag** | A note the program leaves for a human saying "please check this" |
| **Self-predicted grade** | A grade the student expects to get, as opposed to one their school has officially predicted or one they have actually received |
| **Budget ceiling** | The most a family can spend on the whole degree |
| **Regulated profession** | A career you need a licence for, such as doctor, engineer, lawyer or accountant |
| **Recognition** | Whether Malaysian authorities accept a foreign degree as valid |
| **MQA** | Malaysian Qualifications Agency |
| **PDPA** | Personal Data Protection Act 2010, Malaysia's privacy law |
| **Consent** | The student's permission for us to store and use their answers |
| **Scoring formula ("weights")** | The percentages that say how much each of the eight topics counts for one particular student |

---

## For the technically curious: plain names and real names

| In this report | In the project |
|---|---|
| The written procedure | `workflows/01_intake.md` |
| Step 1 and Step 4 (collect, tick off) | `tools/fetch_form_responses.py`, talking to `tools/appsscript/Code.gs` inside the Google spreadsheet |
| Step 2 (convert) | `tools/ingest_form_csv.py` |
| The blank template every record starts from | `tools/init_student.py` |
| The "who you are" file | `data/students/<student>/profile.json` |
| The "what you want" file | `data/students/<student>/preferences.json` |
| The scoring formula | `data/students/<student>/weights.json`, made by `tools/derive_weights.py` |
| The list of 38 courses | `google_form_notes.md` |
