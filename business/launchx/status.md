# LaunchX status

*As of 2026-10-20. Rewritten whenever something changes. See [mentor.md](mentor.md) for how.*

## Dates

- **24 Oct 2026:** Bootcamp 2. 15 minutes with an investor panel. A feedback session, not a
  contest: the deck template is optional and Evan can bring whatever he wants feedback on.
- **10 to 13 Nov:** pilot test with real customers. First paid sales are meant to happen here.
- **2 Dec:** demo day and seed-funding consideration.

## Where things stand

The product works and has been used by 29 students, all friends, none paid. Desk research and the
cost sums are done. **20 Oct: the survey went out (promoted with the "HEY YOU!" carousel in
`launchx/HEY YOU!/`) and has 48 answers, not yet read or counted.** No parent chats yet. Evan is
in exams.

**New, 20 Oct:** iLabs check-in before Bootcamp 2. Due beforehand: a Prototype & Insight form
(A: link to the prototype; B: feedback consolidated from Bootcamp 1 peers) and first NABC answers
(Needs, Approach, Benefits, Competition). Not yet known: what peer feedback Evan got at
Bootcamp 1, and the check-in date. Plan: read the 48 answers via the Google Sheet linked to the
form (Drive connector) or a CSV saved in `data/form/` (git ignores it), counts only.

## Decided

- **Business first, backend frozen until 24 Oct.** No bug-fixing, no website, no new features.
  Known limits ("Sunway A-level only", "intake is a Google Form") and essay help go on a "what we
  build next" slide.
- **The deck ends on three questions for the panel**, not a funding request (slide 10).
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
| Not known | Whether a stranger or a parent would pay, and how much. Which worry comes first for students: scholarships, essays, cost, or choosing. |

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
- [ ] Send the form beyond classmates. Target 30 answers. Ask two or three people to help.
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
