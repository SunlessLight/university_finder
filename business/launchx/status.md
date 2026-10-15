# LaunchX status

*As of 2026-10-15. Rewritten whenever something changes. See [mentor.md](mentor.md) for how.*

## Dates

- **24 Oct 2026:** Bootcamp 2. 15 minutes with an investor panel. A feedback session, not a
  contest: the deck template is optional and Evan can bring whatever he wants feedback on.
- **10 to 13 Nov:** pilot test with real customers. First paid sales are meant to happen here.
- **2 Dec:** demo day and seed-funding consideration.

## Where things stand

The product works and has been used by 29 students. All of them are friends and none paid.
Desk research and the cost sums are done. The Google Form is built and now offers both the list
and the single-university report; not known whether it has been sent. No survey answers or parent chats exist yet, so whether strangers or parents want it
is still unknown. Evan is in exams.

## Decided

- **Business first, backend frozen until 24 Oct.** No bug-fixing, no website. Known limits
  ("Sunway A-level only", "intake is a Google Form") go on a "what we build next" slide.
- **No new features before the pitch.** Essay help goes on that same slide.
- **The deck ends on three questions for the panel**, not a funding request (slide 10).
- **Firecrawl is costed at its paid price** (about RM77 a month) on the slide, not at zero.

## Known, and not known

| | |
|---|---|
| Known | Product is usable: 13 list ratings average 4.1 of 5, 6 report ratings average 4.2. One student asked for a second report unprompted. |
| Known (testers, count not recorded) | Many said the spreadsheet and reports are too much text and hard to read. They did not understand the score, what Match / Safety / Reach mean, or why a university got its label. |
| Known (Evan, from delivered lists) | Most universities on a list cost more than the student's stated budget, US and UK most of all. The tool ranks and labels; it does not remove over-budget options. Students still ask for famous names "to try applying". |
| Known | Hands-on time is under 1 hour a student. Tools cost about RM158 a month. Four students at RM50 cover that. |
| Known (estimate) | At RM50 the reachable market is small: about RM775,000 a year for everyone who starts a degree abroad. Price is the lever. |
| Known | Every free competitor checked is paid by universities. Paid help starts around RM2,000. |
| Not known | Whether a stranger would pay. Whether a parent would pay, and how much. |
| Not known | Which worry comes first for students: scholarships, essays, cost, or choosing. |

## Three guesses under test (all untested)

- **A:** parents feel the problem and would pay; students do not.
- **B:** scholarships are what students want help with first.
- **C:** essays and the application are a bigger fear than choosing a university.
- **D (new, 15 Oct):** education businesses would pay more for this than families. Idea came
  from a friend who sells automations to businesses. Mentor view: don't switch yet, test it.
  Better fit is paid consultants (paid by families, e.g. Inquota) and college counselling
  offices, not agents (paid by universities, would want partner universities ranked first).
  The product today is Evan running sessions himself, so a first B2B offer is a done-for-you
  service, not software. Cheapest test: the counsellor chat already planned, plus 2 consultancy
  chats, plus one of the three panel questions on 24 Oct.

## Open: Evan

- [ ] Before sending the survey, watch "How to Pitch Your Startup"
      (https://startupschool.org/videos/77) and read "How to Talk to Users"
      (https://ericmigi.com/blog/startup-school-how-to-talk-to-users).
- [ ] Decide the wording of the form's last question. The live form says "20 to 30 universities
      matched to your grades, budget, desired country", and "matched to your budget" is not true
      of what gets delivered. Mentor's suggested wording is in the 12 Oct chat. Once chosen, copy
      it into survey.md, which still has the old "8 to 12" text.
- [ ] Decide (mentor recommended yes): add one tick-all question, "which of these have you
      actually looked up?" (visa funds, work rights, recognition, jobs, safety), to measure the
      gap behind "why not just ask Gemini". If added, copy it into survey.md.
- [ ] Decide (mentor recommended yes): add one sorting question, "how far along are you in
      choosing?" (not started / know the country / a few universities in mind / know exactly
      which one). Evan's worry: people who already picked a university want the single-university
      report, not the list, and the form only offers the list. This measures how big that group
      is before a second offer is built for it. If added, copy it into survey.md.
- [ ] Copy the report offer into survey.md. Evan added the single-university report to the live
      form next to the RM50 list on 12 Oct (mentor had advised one offer only; his call). The
      price and wording he used are not in any file yet. Add a row for it to survey.md's "what to
      count" table.
- [ ] Decide: show the sample list and sample report on the form. Mentor recommended yes, as one
      screenshot of the clearest part placed inside the offer question only (never earlier), with
      the full links as an optional extra and a one-line "sample, layout may change" label, not
      a paragraph. Reason: most people fill forms on a phone and will not open a link, and a
      wide spreadsheet on a phone shows the known "too much text" problem at its worst. The
      sample must be of a made-up student, shared view-only.
- [ ] Send the form beyond classmates. Target 30 answers.
- [ ] Three to five parent chats. The most valuable hour in the plan.
- [ ] One chat with a Sunway College counsellor or the placement office.
- [ ] Two or three chats with students who already have a list.
- [ ] Ask two or three people to help collect form answers.
- [ ] Ask iLabs: when is the deck due, and do the 15 minutes include questions?
- [ ] Read deck_content.md and correct anything untrue. Fill in the slide 2 story, the slide 9
      line about himself, and a working name.
- [ ] Open The Sun link in market_sizing.md once to confirm the 54,440 figure.
- [ ] Confirm the 29 testers were all Sunway A-level students.
- [ ] Rehearse twice with qa_drill.md on 23 Oct.

## Open: mentor session

- [ ] About 21 Oct: put survey counts into the `[SURVEY]` blanks in deck_content.md and
      qa_drill.md.
- [ ] After the counsellor chat: replace the guessed counsellor column in competitors.md and the
      cohort figures in market_sizing.md.
- [ ] Build the slides, only after Evan has corrected deck_content.md. Add the readability
      complaint to the "what we build next" slide.
- [ ] Optional and last: put a price into the demo and rebuild its sample figures.

## After 24 Oct (backend, frozen until then)

- **Readability of the list and reports.** Evan wants the workflow to explain the score and the
  Match / Safety / Reach labels, and why each university got its label. This is part of the wider
  "too much text" complaint, so the fix is likely fewer words plus a short key, not more
  explanation. A Glossary tab already exists and students still did not understand: find out
  whether they saw it before building anything.

## Things Evan has said that matter

- The switching between studies and running the service has taken a toll. Suggested on 12 Oct:
  one fixed slot a day. Not yet known whether he tried it.
- He fears RM50 is too much, and says that may be because RM50 is a lot where he comes from
  (12 Oct). One person's feeling, so a guess: questions 5 and 9 of the form are what test it.
  Mentor advice: do not lower the price before the counts are in.
- His five observations of A-level students (scholarships first, they don't know what to ask,
  money worries push them to familiar names, they fear essays, they won't pay and feel awkward
  taking help from a classmate) are from his own circle, so each is a guess to test.
- He sees the difference from Gemini as the "extra" facts students don't think to ask about
  (visa, jobs after, politics). Most of those sit in the reports and apply pack, not the RM50
  list. Mentor advice: keep the form's offer as the list only, show the other two packages as a
  price ladder on the pricing slide, test selling the second in the November pilot. His call.
