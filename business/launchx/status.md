# LaunchX status

*As of 2026-10-24. Rewritten whenever something changes. See [mentor.md](mentor.md) for how.*

## Dates

- **24 Oct (done):** Bootcamp 2 panel. Their message: ChatGPT can do the research too.
- **25 Oct:** nudge silent leads, count the 29.
- **2 Nov:** paid lists delivered.
- **10 to 13 Nov:** pilot with real customers.
- **2 Dec:** demo day. Check: 1 consultancy on a paid pilot **and** 10 paying families?
- **10 Dec:** if short of the bar, the pause ends: continue, pivot or stop.

## Where things stand

The product works: 29 students used it, all friends, none paid. Survey (out 12 Oct): 79 responses
by 23 Oct (12 strangers, 25 "a little", 42 friends), CSV in `data/form/` (gitignored, holds contact
details). 35 left a number at RM50, 6 misread the question, so **29 real leads, all messaged by
23 Oct** (want: list 19, report 7, both 6). After the panel the main track moved to B2B (see
Decided). Evan is in exams.

## Survey highlights (20 Oct, 54 rows; the only copy of these figures)

- **0 parents** answered. 44 pre-university, 7 at university.
- **Nobody pays for help today:** 49 of 54 paid no one; 2 paid RM100–500; 3 used a paid consultant.
- Top worry: scholarships 19, essays 11, entry requirements 7, choosing a university only 5.
- Students decide (33 mostly me, 19 together, 2 parents); parents pay (33).
- 25 already know their universities; most "no" reasons are "already applied". Sell before applications.
- Used: uni websites 46, ChatGPT/Gemini 38, rankings 33, seniors 31, fairs 25, school 25, social 24,
  agents 14, paid consultant 3.
- Looked up: fees 37, entry reqs 35, scholarships 35, jobs 26, living costs 25, post-study work 16,
  recognition 14, safety 13, visa funds 10. The "extras" are the least researched.

## Decided

- **Focus shift (24 Oct):** main track = B2B test using the current workflow, sold to small
  family-paid consultancies (guess D). Side track = families: light advertising plus referrals.
  Order: consultancy messages first, then cost cuts measured on the 2 Nov lists, then only fixes a
  customer or consultant would see. Stale-wording and internal fixes in additionals.md stay parked.
- **Continue-bar (24 Oct): 1 consultancy on a paid pilot and 10 paying families by 2 Dec.** On a
  miss: pause, work out what went wrong, decide continue / pivot / stop by 10 Dec.
- **Prices (23 Oct):** list (20–30 universities) RM50, single report RM30. Count the 25 Oct replies
  at the old price, then announce RM30 in the nudge.
- **Pre-sale cap: 15 list spots (22 Oct)**, set by Evan's time. Pre-sell before fixing (21 Oct).
- **After payment** the customer gets the existing Google Form (feeds the intake tools), not WhatsApp.
- **Referral reward:** a free one-university report per friend who pays; only for people who have
  paid and received their list.
- **Firecrawl is costed at its paid price** (about RM77 a month), not zero.
- No legal or tax setup until someone pays; SSM registration comes with the first B2B payment.

## Known, and not known

| | |
|---|---|
| Known | Usable: 13 list ratings average 4.1 of 5, 6 report ratings 4.2. One student asked for a second report unprompted. |
| Known (testers) | Spreadsheet and reports too wordy; score, Match / Safety / Reach and labels not understood. |
| Known (iLabs, 21 Oct) | Prototype nice; needs a better look, less text, email instead of WhatsApp. Asked: why not ChatGPT? and one-time buyers only? |
| Known (Evan) | Most listed universities are over the student's budget (US, UK most). The tool ranks; it does not remove. |
| Known | Under 1 hour hands-on per student. Tools about RM158 a month. |
| Known (estimate) | At RM50 the reachable family market is about RM775,000 a year. Price is the lever. |
| Known | Free competitors are paid by universities. Paid help starts around RM2,000. |
| Not known | Whether any of the 29 leads pay. Whether parents or consultancies would pay. |

## Guesses under test

- **A:** parents feel the problem and would pay; students do not. (No parent reached yet.)
- **B:** scholarships are what students want help with first. (Survey supports.)
- **C:** essays and the application are a bigger fear than choosing. (Partly: essays 2nd.)
- **D, now the main track:** consultancies would pay more than families.
  [b2b_research/report.pdf](../b2b_research/report.pdf) ranks international-school counsellors and
  small family-paid consultancies first; agents and private universities are paid by universities
  (talk to learn, not to sell). Inquota may also earn commission (unconfirmed). First offer: a
  done-for-you pilot of about 10 students. Script and commitment ladder: report section 9.
  Paperwork: talking needs none; first payment needs an SSM sole-proprietor registration (about
  RM30–60 a year, from guides) and a PDF invoice; e-invoicing exempt below RM1M. Watch for a PDPA
  processor agreement from a school.

## Open: Evan

- [ ] Write the panel's feedback down word for word.
- [ ] 25 Oct: nudge silent leads, then count paid / yes-not-paid / no / silent. Only "paid" is
      demand. Ask one "no" why. If the first message set no payment date, the nudge does.
- [ ] After the count: message 3 consultancies (PrepWorks, Inquota, one more) for a 15-minute chat
      on how they research universities. Learn, don't pitch. Before any pitch, decide whether to
      refuse a partner-only list.
- [ ] Sunway counsellor or placement-office chat (also a B2B call: report section 9 questions).
- [ ] Three to five parent chats.
- [ ] Two chats with "too expensive" leads; two or three with students who already have a list.
- [ ] Park "big problem" ideas in a phone list until 2 Dec.
- [ ] Low priority: copy the form's final wording, added questions and RM30 offer into survey.md;
      confirm the 29 testers were all Sunway A-level; check The Sun link in market_sizing.md.

## Open: mentor session

- [ ] After the consultancy or counsellor chats: replace the guessed counsellor column in
      competitors.md and the cohort figures in market_sizing.md.
- [ ] Before demo day: check deck_content.md and qa_drill.md for unfilled `[SURVEY]` blanks.

## Backend (open, within the focus-shift limits)

- **Cost:** time each step and note tokens on the 2 Nov paid lists (backlog N1), then cut the top
  one or two before the pilot. No big rewrite before 2 Nov. Keep one human review per student.
- **Readability:** explain the score and labels with fewer words plus a short key. A Glossary tab
  exists: first find out whether students saw it.
- **Over-budget universities** crowding the lists.

## Things Evan has said that matter

- **24 Oct:** after the panel, wanted to pivot to a "big problem"; feels his ideas (credit card
  tracker, SnapIt, this) are small ChatGPT wrappers; thinks free ChatGPT is good enough for
  families; prefers B2B. Mentor: the problem is big, the price is small; the pattern to break is
  never reaching a count; "automations" is a method, not a problem; change the customer, not the
  product. Evan chose the focus shift and new bar.
- **23 Oct:** worried it's a luxury; running out of people he knows; wants full automation with no
  human check; FOMO from social media. Tutors at RM100–120/hr, about 3 hours every 2 days.
  Mentor: B2B doesn't escape outreach; keep one human review (the edge over ChatGPT); tutoring
  pays more per hour now, this is a bet on income not tied to his hours.
- **21–22 Oct:** fears the edge disappears as people learn ChatGPT. Mentor: the workflow is no
  moat; the edge is official-page facts, total cost in ringgit, fit kept apart from quality,
  recognition checks.
- **16 Oct:** wants a side hustle, not a big company.
- Switching between studies and the service takes a toll. One fixed daily slot suggested 12 Oct;
  not known whether he tried it.
- Fears RM50 is a lot (12 Oct). Mentor: don't lower prices before the counts are in.
- His five observations of A-level students come from his own circle: guesses to test.
