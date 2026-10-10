# Product review — University & Course Researching Service

*Written 2026-09-25. A business/marketing look at the whole project: what's working, what isn't, and
what to do about it. Based on the sales folder, the intake form, the real student feedback
(`data/feedback/`), and the live progress dashboard (`tools/progress_dashboard.py`).*

*Updated 2026-10-10: added the section "Does anyone actually want this?" (near the bottom) and
toned down the places where the first version overstated the evidence. Each changed spot is marked
"Updated 2026-10-10".*

---

## Read this first

**Nothing in this review says the product is useless.** The opposite, in fact:

- The core idea solves a real, expensive problem.
- The positioning is better than most startups manage.
- Real students rated it 4.1/5 and 4.2/5, and several gave specific, critical feedback, which shows
  they actually used it. *(Updated 2026-10-10: these students are friends who got it free, so the
  ratings show the product is usable. They don't yet show that strangers want it.)*

Every "con" below is about **delivery and consistency**: the marketing got ahead of what the pipeline
reliably delivers, and the sales story is still the early-days one. Those are normal problems for a
product that works and has real users.

*(Updated 2026-10-10)* Whether enough people **want** it is a separate question. It isn't answered
yet, in either direction, and it has its own section near the bottom.

**There's no deadline on any of this.** Take one item at a time. The "next moves" list at the bottom
is in order, so if you only ever do #1, you're still better off.

---

## ✅ Pros — what's working

### 1. It solves a real, expensive problem
Choosing a university is a RM200k–400k, 3–4-year decision. The fear of getting it wrong is real, and
parents feel it even more than students do. A product that reduces a big risk for a small price is an
easy sell. **Principle: sell painkillers, not vitamins.** This is a painkiller.

### 2. The positioning is excellent
[positioning.md](sales/positioning.md) is better than most startup positioning:
- **You sell the result, not the technology.** The "job to be done" (the real goal the customer hires
  a product for) is "don't waste RM400k, get my parents to agree, don't miss a deadline". It isn't
  "learn about universities", and every script is framed around that.
- **You compete with the real alternative.** For your buyers that's Gemini/ChatGPT, not other
  consultants, and you handle it without arguing: *"yeah honestly for a lot of stuff it can… this is
  mine tho."*
- **You tell the wrong customer not to buy** ("if you already know your 3 UK unis, just use
  Gemini"). This is a proven trust builder, and it creates referrals.

### 3. The differences are real and hard to copy with a prompt
Each of these is built into the tools, not just claimed:
- **"Is it a good uni" and "can you get in" are kept separate.** A famous uni you can't get into
  can't rank #1. That fixes the most common AI mistake.
- **Total cost of the whole degree in ringgit** makes a 3-year UK degree comparable with a 4-year US one.
- **Recognised in Malaysia**: whether the degree is accepted by MQA (Malaysian Qualifications Agency)
  and the professional bodies for medicine, engineering, law and accounting. For those careers,
  getting this wrong is a dealbreaker, and generic tools don't check it.
- **Local detail**: JPA/MARA/Yayasan scholarships, halal food and prayer facilities. This is a niche a
  global competitor won't serve well.

### 4. Low friction to start
The poster has one clear CTA (call to action, the single thing you want the reader to do): a free form
that takes 2 minutes. There's no payment, no call to book and no account to create. The effort needed
to start is about as low as it gets.

### 5. "Show, don't tell" is built into how you sell
The poster shows a real spreadsheet row and a real quote from a report ("drinking from a firehose"). A
sample pack exists. The "every report says why NOT to go" line is your most believable sentence,
because honesty about downsides is rare in education sales.

### 6. You now have real social proof
Social proof means evidence that other people used it and liked it. You have 13 spreadsheet ratings
averaging **4.1/5** and 6 report ratings averaging **4.2/5** on time saved, with genuine quotes. The
poster already uses them, which is correct.

*(Updated 2026-10-10)* A caveat: all of these students are friends, were asked in person, and got
it free. So this is proof that the product is usable and that people engage with it. It is not yet
proof of demand from people who don't know you.

### 7. The deliverables are files people keep
A spreadsheet and PDFs you can forward to parents beat a chat log that scrolls away. Parents trust
documents, so the product works as a pitch to the parents too.

### 8. Sensible go-to-market plan
Go-to-market is the plan for reaching customers. Yours relies on word of mouth, no paid ads, and
friends-of-friends first. At a low price with 18-year-olds who all talk to each other, that's the
right channel.

---

## ❌ Cons — what needs fixing (most serious first)

### 1. 🔴 The poster promises more than the lists actually contain
The poster says *"Every fee, requirement and deadline **checked on the actual university page**."* The
progress dashboard (2026-09-25) shows otherwise:
- one list has **52 of 56** rows unverified
- another has **41 of 44** unverified, another 33 of 36, another 17 of 18

Your whole brand rests on "I checked, Gemini guesses." If a parent opens the spreadsheet and sees
`Not verified` on most rows, that one moment undoes the pitch. **Principle: under-promise,
over-deliver.** Either verify before delivery, or change the wording to something like "the ones on
your shortlist are checked on the official page".

### 2. 🔴 Very few students reach the end
Of **29 students** (2026-09-25):

| Where they are | Count |
|---|---|
| Waiting for their list, or partway through it (Stage 3) | 13 |
| List done plus at least one deep report (Stage 4) | 14 |
| **Full package with recommendation + apply guide (Stage 5)** | **1** |

The poster and the tiers sell three products: List → Report → Apply Guide. Only 1 in 29 has received
the third. That's a funnel problem (the step-by-step drop-off from signing up to finishing). It also
means Tier 3 is being advertised on essentially one example.

*(Updated 2026-10-10)* Timing matters here: the A-level students are in exams right now, so part of
this drop-off is simply that nobody is thinking about applications yet.

### 3. 🔴 The numbers don't match across your materials
Consistency is a trust signal. At the time of writing:
- **Columns:** 34 ([service-tiers.md](sales/service-tiers.md) heading), 35 (sample pack, poster), 41
  ([scripts.md](sales/scripts.md) "Gemini" reply and cold opener)
- **Report size:** 15 sections, 16 sections (the sample report), "20-page report" (the feedback form)
- **Longlist size:** "20–40 unis" (tiers, scripts) vs "8–12 per country" (poster) vs **6–12**
  actually delivered to most students
- **Finalists:** "3–5 finalists" (tiers) vs "Pick 1 uni to go deep on" (poster)
- **Price:** RM50 everywhere in the sales docs, but no price on the poster at all

A sharp student who compares your WhatsApp message with your poster will notice.

### 4. 🟠 The sales story is out of date
Everything in [positioning.md](sales/positioning.md) and the scripts is built on *"I've done this for
exactly one person."* You're now at 29 sign-ups and 15 students with at least one delivered report.
The honest disarm ("I'm early, first 5 free") was the right move and it worked. It's now false in the
other direction, because you're undervaluing yourself. The plan was "free 5, then RM50", and you've
given away around 29. **When you're ready, it's time to start charging.**

*(Updated 2026-10-10)* A price is still the clearest way to tell real interest from politeness. But
don't run that test during exam season, when nobody would buy anything.

### 5. 🟠 Unit economics: every sale costs you real time
Unit economics means how much you earn vs. spend per customer. Each student needs you running Claude
Code sessions: about 70k tokens (units of AI usage) per university, 10+ universities per country,
plus your manual review steps. At RM50 your hourly rate is very low, and the service **can't grow
beyond your own hours**. Many students are still waiting at the list stage, which suggests capacity is
already the bottleneck. There's also no stated turnaround time, just "I'll message you once your list
is ready." Customers who wait without knowing how long get anxious and stop engaging.

### 6. 🟠 Too much information for the customer
"35 columns" impresses in a pitch. But look at what students actually said was most useful: **Course
at a glance, Entry requirements, Total cost**. Those are the simple ones. For the report, *every*
section was named "confusing or unnecessary" by at least one student, and "Why here / why hesitate"
was named twice. That's the same section two others found most interesting, so it's divisive rather
than bad. **Principle: fewer, clearer choices beat more information** (it's called "choice
overload"). A one-page "your top 5 at a glance" summary in front of the spreadsheet would probably
raise perceived value more than another column.

*(Updated 2026-10-10)* The same applies to the report, which runs about 20 pages. Only 6 of the
roughly 15 students who received one answered the feedback form, so it's unknown how many of the
others read it. The likely problem is the length, not the content, and a one-page summary at the
front fixes that without cutting anything.

### 7. 🟠 Missing famous names hurts credibility
Feedback mentioned missing UCL, KCL, Manchester, Warwick, NYU and Fudan. "Not just the famous names" is
a good line, but students judge a list by first checking that the names they already know are on it.
When a famous name is missing, they assume the list is incomplete, not tailored. Fix: always include
the well-known ones, marked "Reach" or with a reason they didn't fit. That also shows off your
Reach/Match/Safety feature.

### 8. 🟡 Your demo files are stale
The sample report uses the old 16-section format. The sample apply guide is flagged in
[its own README](sales/sample_pack/README.md) as containing **outdated facts** (Columbia's test policy,
US visa work rules). Your [go-to-market memo](sales/go-to-market.md) calls the sample "the priority,
above everything else," so your best sales asset should be your most current one.

### 9. 🟡 Unclear who the buyer is
Pricing is set for student pocket money (RM50, "below the ask-my-parents threshold"). But the person
who feels the RM400k risk and holds the budget is the parent. You have a parent-facing script but no
parent-facing asset, and no higher-priced tier. Consider keeping a cheap student entry (the List) and
a parent-priced full package (Reports + Apply Guide). The tier structure already supports this.

### 10. 🟡 Legal and privacy basics for a paid service
While this was internal testing, a casual form without formal consent was fine. Once you take money
and hold minors' grades, family finances and nationality, Malaysia's PDPA (Personal Data Protection
Act 2010) applies. You'll need a short consent line and a "this is research, not guaranteed advice;
fees change" disclaimer. That protects you if a fee turns out to be wrong.

### 11. 🟡 Generic name, no brand
"University & Course Researching Service" describes what it is but isn't memorable or searchable.
That's fine for friends-of-friends, but word of mouth works better when people can repeat a name.

---

## Does anyone actually want this? (added 2026-10-10)

After reading the review, the bigger worry turned out not to be any of the cons above. It was this:
*"Maybe A-level students don't need this at all. They can use Gemini, they already know which unis
they want, and they're too proud to accept help."*

This section records where that conversation got to.

### The short answer

**It's unknown, and now is the worst time to find out.** The students are in exams. Their silence
can't be read as "they don't want it", and the friendly sign-ups can't be read as "they do".

### Why it feels like nobody needs it

Three well-known thinking traps are involved. None of them is a personal flaw; everyone who builds
something runs into them.

- **Curse of knowledge.** Once you know something, it's very hard to remember not knowing it. You
  spent three months learning how university research works, so it now feels obvious, and you assume
  it's obvious to everyone.
- **False consensus effect.** Assuming other people behave the way you do. You'd research
  universities yourself with Gemini, so you assume every student would.
- **Experts underestimate themselves** (one half of the Dunning-Kruger effect). When something feels
  easy to you, you assume it's easy for others. This is the "if I can do it, they can too" thought.

### Why the sign-ups don't prove demand either

All 29 students are friends, were asked personally, and got it free. Saying yes in that situation is
often just kindness. The name for it is **courtesy bias**: people tell you what's kind instead of
what's true. So the number 29 is not evidence that people want the product.

### What is known, and what is a guess

| Statement | Known or guess? |
|---|---|
| Students who got a list engaged with it | **Known.** They gave specific complaints ("didn't see Warwick"), four ratings of 3 out of 5, and requests for extra columns. People being polite don't do that. |
| One student came back and asked for another report | **Known.** Nobody asked them to. This is the strongest single signal so far. |
| Students are busy with exams | **Known.** |
| "They're only being nice to me" | Guess. |
| "They're too proud to ask for help" | Guess. |
| "They already know which unis they want" | Guess. True for some (the sales notes already say those students don't need this), not shown for all. |
| Strangers would pay for it | **Unknown.** Never tested. |

Both the hopeful guesses and the fearful guesses are guesses. The fearful ones only feel more true.

### Four possible reasons for the silence

| Reason | How likely | Can anything be done now? |
|---|---|---|
| Exams | Very likely | No. Wait it out. |
| They think it's one report each | Plausible. The poster says **"Pick 1 uni to go deep on"**, so asking for a second may feel cheeky. | Yes. Tell them more is available, after exams. |
| The report is too long (about 20 pages) | Plausible | Yes. Add a one-page summary at the front. |
| They don't want it | Unknown | Can't tell until exams end. |

### How to find out, without guessing

The rule comes from a book called *The Mom Test* by Rob Fitzpatrick: **compliments cost nothing, so
they tell you nothing. Watch what people do when it costs them something** (time, money, or
recommending you to someone else).

Signals worth more than any sign-up:
- someone comes back on their own asking for more (this has happened once)
- someone forwards their list or report to a parent or friend
- someone mentions using it when they actually chose or applied
- someone pays, even a small amount

### Small steps, in order

**Now, during exam season** (nothing here needs anyone's opinion):
- [ ] Do the private fixes from the list below: moves 1, 2, 4 and 5.
- [ ] Change "Pick 1 uni to go deep on" on the poster if more than one report is on offer.

**After exams end:**
- [ ] Ask one friend who already has their list: *"What didn't you know before you saw it?"* This
  checks the curse of knowledge with a real answer.
- [ ] Ask one friend: *"Do you know anyone who's stressed about choosing a uni?"* Whoever they name
  owes you no politeness, so their reaction is the first honest signal.
- [ ] Then move 3 (price and turnaround time on the poster).

### On being humble

Humility is about how you treat people: not showing off, admitting what you don't know, telling
someone "you don't need me" when that's true. The sales scripts already do all of that.

Saying "I know more about this than most 18-year-olds because I spent three months on it" is a plain
fact about hours spent. Underestimating what you know isn't humble, it's inaccurate, and it costs the
students who would have been helped.

---

## Next moves (in order, one at a time)

- [ ] **1. Make the promise match the delivery.** Verify every row before delivering, or reword the
  poster's "every fee checked" claim.
- [ ] **2. Pick one set of numbers** (columns, sections, list size, number of finalists, price) and
  update the poster, scripts, tiers and feedback form to match.
- [ ] **3. Rewrite the "n=1" pitch** as "29 students have tried it" (true, and you can say they were
  free trials if asked). Publish a price and a turnaround time on the poster. *(Updated 2026-10-10:
  wait until exams are over for this one.)*
- [ ] **4. Add a one-page summary** at the top of the spreadsheet and the report, built around the 3
  columns students said they actually use.
- [ ] **5. Regenerate the sample pack** from a current student so your main sales asset is up to date.

Moves 1 and 2 are **private fixes**: no customer sees you making them, and nobody has to judge anything
new. They're a low-pressure place to start.

---

## Three ideas worth remembering

- **The problem changed as you grew.** At 1 student, the risk was that people couldn't *see* the
  product. At 29, the risk is that they *can*, so any gap between the poster and the actual
  spreadsheet gets noticed.
- **Depth sells, simplicity gets used.** Students valued the simplest columns most. Lead with a short
  summary; keep the depth one click away.
- **The tier ladder is also a pricing ladder.** List → Report → Apply Guide maps onto cheap student
  entry → parent-priced full package, which fixes the time-vs-money problem without raising the
  entry price.
