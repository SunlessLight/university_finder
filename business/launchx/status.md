# LaunchX status

*As of 2026-10-22. Rewritten whenever something changes. See [mentor.md](mentor.md) for how.*

## Dates

- **24 Oct 2026:** Bootcamp 2. 15 minutes with an investor panel. A feedback session, not a
  contest: the deck template is optional and Evan can bring whatever he wants feedback on.
- **10 to 13 Nov:** pilot test with real customers. First paid sales are meant to happen here.
- **2 Dec:** demo day and seed-funding consideration.

## Where things stand

The product works and has been used by 29 students, all friends, none paid. Desk research and the
cost sums are done. The survey went out 12 Oct (promoted with the "HEY YOU!" carousel in
`launchx/HEY YOU!/`). Responses CSV moved to `data/form/survey_responses_2026-10-20.csv`
(gitignored; it holds emails and phone numbers). No parent chats yet. Evan is in exams.

## Survey results (20 Oct, 54 rows, 53 unique emails, a few joke answers)

- **Who:** 26 friends, 18 "a little", 10 strangers. 44 pre-university, 7 at university, **0 parents**.
- **Left a WhatsApp number at RM50: 24 people** (25 rows, 1 repeat): 9 friends, 10 "a little",
  6 strangers. Prefer: list 11, report 6, both 5. A number left is a sign of interest, not payment.
- **Nobody pays for help today:** 49 of 54 families paid no one. 2 paid RM100–500. 3 used a paid consultant.
- **Top worry:** scholarships 19, essays 11, entry requirements 7, **choosing a university only 5**.
  Strangers: scholarships 5 of 10. Guess B supported; guess C partly (essays 2nd).
- **Decides vs pays:** students decide (33 mostly me, 19 together, 2 parents); parents pay (33).
  Guess A still untested: the survey reached no parents.
- **Already decided:** 25 say "I know exactly which universities". Most "no" reasons are
  "already chose / already applied (UCAS)". Timing matters: sell before applications, not after.
- **Used:** uni websites 46, ChatGPT/Gemini 38, rankings 33, seniors 31, fairs 25, school 25,
  social media 24, agents 14, paid consultant 3.
- **Looked up:** fees 37, entry reqs 35, scholarships 35, jobs 26, living costs 25, post-study work
  16, recognition 14, safety 13, visa bank funds 10. The "extras" are the least researched.

**New, 20 Oct:** iLabs check-in before Bootcamp 2. Due beforehand: a Prototype & Insight form
(A: link to the prototype; B: feedback consolidated from Bootcamp 1 peers) and first NABC answers
(Needs, Approach, Benefits, Competition). No peer feedback exists (Evan left Bootcamp 1 early).
**Check-in done (by 21 Oct):** Parts A and B both shown to the accelerator staff. Their feedback:
the prototype is nice but needs a better look, less text, email instead of WhatsApp (already in
the backlog). Two open questions they raised: (1) what separates this from ChatGPT/Gemini, when
anyone can ask it for a document; (2) one-time buyers, no repeat customers: keep selling to
families, or rent the workflow to businesses (guess D). Mentor: the workflow itself is no moat;
the edge is official-page facts, total cost in ringgit, fit kept apart from quality, recognition
checks. Unknown whether a ChatGPT user pays RM50 for that: the pre-sale answers it. Don't pick the
business model before either side has paid. Pilot capacity (24 people in 4 days) is still the
real readiness gap.

## Decided

- **Business first, backend frozen until 24 Oct.** No bug-fixing, no website, no new features.
  Known limits ("Sunway A-level only", "intake is a Google Form") and essay help go on a "what we
  build next" slide.
- **The deck ends on three questions for the panel**, not a funding request (slide 10).
- **Pre-sell before fixing (21 Oct).** Ask the 24 leads for a yes/no on RM50 first; after 24 Oct
  fix only what a paying customer would see.
- **Firecrawl is costed at its paid price** (about RM77 a month) on the slide, not at zero.

## Known, and not known

| | |
|---|---|
| Known | Product is usable: 13 list ratings average 4.1 of 5, 6 report ratings average 4.2. One student asked for a second report unprompted. |
| Known (testers, count not recorded) | Many found the spreadsheet and reports too wordy, and did not understand the score, Match / Safety / Reach, or why a university got its label. |
| Known (Evan, from delivered lists) | Most listed universities cost more than the student's budget, US and UK most of all. The tool ranks; it does not remove over-budget options. Students still ask for famous names. |
| Known | Under 1 hour hands-on per student. Tools about RM158 a month; four students at RM50 cover it. |
| Known (estimate) | At RM50 the reachable market is about RM775,000 a year. Price is the lever. |
| Known | Every free competitor checked is paid by universities. Paid help starts around RM2,000. |
| Not known | Whether any of the 24 who left a number will actually pay. Whether parents would pay (no parent answered). |

## Four guesses under test (all untested)

- **A:** parents feel the problem and would pay; students do not.
- **B:** scholarships are what students want help with first.
- **C:** essays and the application are a bigger fear than choosing a university.
- **D (15 Oct):** education businesses would pay more than families. Mentor view: don't switch,
  test it. Desk research done: [b2b_research/report.pdf](../b2b_research/report.pdf) (18 pages
  plus sources). It ranks **international-school counsellors** and **small family-paid
  consultancies** first. Agents and private universities are paid by universities, so talk to them
  to learn, not to sell. Inquota is *not* a clean family-paid example: it may also earn commission
  (unconfirmed). First calls: the Sunway placement-office chat (already planned), Alice Smith or
  KTJ, PrepWorks, Inquota, Sunway's American-degree transfer office. A first offer is a
  done-for-you pilot of about 10 students. Software prices schools already pay (about RM19–137 per
  student) don't support a much higher price for the list alone. Before any pitch, decide whether
  to refuse a partner-only list. Script and commitment ladder: report section 9.
  16 Oct paperwork check: talking needs none. First B2B payment needs an SSM sole-proprietor
  registration (about RM30/yr own name, RM60 trade name, from guides, not SSM itself; minimum
  age not confirmed) and a plain PDF invoice. E-invoicing is exempt below RM1M turnover (Known,
  from 1 Jan 2026). No Sdn Bhd needed. Real legal item: the PDPA processor agreement a school
  may send. Big groups (Sunway procurement, MARA) are out of reach for a sole trader anyway.

## Open: Evan

- [ ] Before sending the survey, watch "How to Pitch Your Startup"
      (https://startupschool.org/videos/77) and read "How to Talk to Users"
      (https://ericmigi.com/blog/startup-school-how-to-talk-to-users).
- [ ] Choose the form's last-question wording ("matched to your budget" isn't true of what is
      delivered; mentor's wording is in the 12 Oct chat), then copy it into survey.md (still says "8 to 12").
- [ ] Decide (mentor: yes) on two added questions, then copy any you add into survey.md: "which of these have you
      actually looked up?" (visa funds, work rights, recognition, jobs, safety) and "how far along are
      you in choosing?" (sizes the group who'd want the single report, not the list).
- [ ] Copy the single-university report offer (added to the form 12 Oct, his call) into survey.md,
      with its price, wording and a row in the "what to count" table.
- [ ] Decide on showing a sample on the form. Mentor: yes, one screenshot inside the offer question
      only, full links optional, labelled "sample, layout may change"; made-up student, view-only.
- [x] Send the form beyond classmates. 54 answers, 10 from strangers.
- [ ] Draft the RM50 pre-sale message to the 24 who left a number (real slots, a date, a deposit);
      send after 24 Oct and count replies and deposits.
- [ ] Three to five parent chats. The most valuable hour in the plan.
- [ ] One chat with a Sunway College counsellor or the placement office (also the first B2B call,
      guess D: use report section 9's pre-U questions).
- [ ] Two or three chats with students who already have a list.
- [ ] Ask iLabs: when is the deck due, and do the 15 minutes include questions?
- [ ] Read deck_content.md and correct anything untrue. Fill in the slide 2 story, the slide 9
      line about himself, and a working name.
- [ ] Open The Sun link in market_sizing.md once to confirm the 54,440 figure.
- [ ] Confirm the 29 testers were all Sunway A-level students.
- [ ] Rehearse twice with qa_drill.md on 23 Oct.

## Open: mentor session

- [ ] About 21 Oct: put survey counts into the `[SURVEY]` blanks in deck_content.md and qa_drill.md.
- [ ] After the counsellor chat: replace the guessed counsellor column in competitors.md (stream 3
      found some colleges may also earn commission) and the cohort figures in market_sizing.md.
- [ ] Build the slides only after Evan has corrected deck_content.md. Add the readability
      complaint to the "what we build next" slide.
- [ ] Optional and last: put a price into the demo and rebuild its sample figures.

## After 24 Oct (backend, frozen until then)

- **Readability of the list and reports:** explain the score and the labels, likely with fewer
  words plus a short key. A Glossary tab already exists: first find out whether students saw it.

## Things Evan has said that matter

- **21–22 Oct:** worried his edge over ChatGPT disappears if people learn to make documents with
  it, and that the product is "just a wrapper". Also afraid asking for a commitment up front
  lowers how many pay.

- **16 Oct: he wants a side hustle, not a big company.** Worried B2B is more than he can chew.
  Mentor: big-company sales, yes; one 10-student pilot with a small client, no. Asked him what
  "worth it" by December looks like; answer not yet given.

- Switching between studies and the service has taken a toll. Suggested 12 Oct: one fixed slot a
  day. Not known whether he tried it.
- He fears RM50 is too much, perhaps because RM50 is a lot where he comes from (12 Oct). Questions
  5 and 9 of the form test it. Mentor: don't lower the price before the counts are in.
- His five observations of A-level students (scholarships first, don't know what to ask, money
  pushes them to familiar names, fear of essays, won't pay a classmate) are from his own circle:
  guesses to test.
- He sees the difference from Gemini as the "extra" facts (visa, jobs after, politics). Most sit in
  the reports and apply pack, not the RM50 list. Mentor: keep the form's offer as the list only,
  show the others as a price ladder, test selling the second in the pilot. His call.
