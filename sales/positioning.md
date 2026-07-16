# Positioning — why this beats "I'll just use Gemini"

The reasoning behind the pitch. Scripts live in [scripts.md](scripts.md); this file is why they're
worded the way they are. Read it once so you can improvise when a conversation goes off-script.

---

## 1. The diagnosis: they're not talking about Gemini

At RM50, nobody is running a cost-benefit analysis. RM50 is two teh tariks and a roti. When someone
says *"Gemini is enough,"* they are almost never making a technical claim. They mean one of:

- **"I don't believe this is a real thing."** They picture a ChatGPT chat log in a Word doc.
- **"I'd feel stupid paying for AI I already have free."** This one is about *them*, not you.
- **"I'm not actually doing my uni research right now."** Timing. Not an objection at all.

None of those are answered by explaining what Gemini is bad at. Worse — arguing Gemini's limits tells
a person who is proud of using Gemini that they've been using it wrong. You will win the argument and
lose the sale.

**So don't answer the objection they said. Answer the one they meant: make it feel real.** That's a
demo problem, not an argument problem. See §3.

## 2. The reframe: you don't sell research, you sell a decision artifact

Gemini gives you a conversation. Conversations scroll away. You give a **file**.

The student's actual job-to-be-done is not "learn about universities." It's:

1. **Don't torch RM400k and 3-4 years** on the wrong choice.
2. **Get parents to agree.** Parents do not read chat logs. Parents read spreadsheets.
3. **Don't miss a deadline** they didn't know existed.

Every script frames around those three. Never frame around "my AI is better than your AI" — that's a
fight about tools, and the tool isn't the product. The *artifact* is the product: a CSV that opens in
Excel and PDFs that open on a phone, six months from now, when the chat is long gone.

## 3. Show, don't debate

**The single highest-converting move in this whole playbook:** paste the 41 column headers, or one
page of an apply guide. Then stop typing.

Do not say "Gemini can't do this." Say **"here's what mine looks like."** The gap argues for you, and
nobody gets defensive at a screenshot. If they come back with "oh — Gemini didn't give me any of
that," they sold themselves and you didn't spend a word.

Corollary: **get the demo asset ready before you pitch anyone.** A pitch without something to show is
just you making claims, which is exactly the thing they don't believe.

## 4. The four structural gaps — what prompting cannot fix

This is the spine of the long rebuttal, for the friend who genuinely wants to argue. Each of these is
enforced in the code, not a promise:

### 4.1 Gemini will rank a university you cannot get into as #1

This is the killer, so lead with it. LLMs conflate *prestigious* with *right for you* — ask for "best
unis for me" and you get a list bent toward famous names, because that's what the training data
rewards. Your scorer **refuses** to let entry fit touch the desirability score:
`FORBIDDEN_WEIGHT_KEYS` (`tools/shortlist_schema.py:113`) raises an error if you try. Admissibility is
a *separate* Reach/Match/Safety column, computed from the entry margin.

> **The killer question:** *"Did your list separate 'this is a great uni' from 'you can actually get
> in'?"*

It didn't. That's not a prompting skill gap they can close by writing a better prompt — it's
structural. A cheap uni you can't get into can never rank #1 on your list. That's the whole point.

### 4.2 It won't tell you when it's guessing

Every row stamps **`Info source`** — `Not verified` until a human has confirmed the fact on the
university's own page, `Official page` after. Gemini will state a 2022 tuition fee as current fact, with
total confidence, and never flag it.

That fee is the single most decision-relevant number in the entire exercise, and it's the one most
likely to be silently stale. Aggregators are discovery-only here — a row can't reach Shortlist on
aggregator facts. Everything hard gets re-checked against the official uni / UCAS / Common App page.

### 4.3 It forgets you

Application season is six months, not one chat window. Come back next week and Gemini starts cold —
you re-explain your grades, your budget, your dealbreakers, and it gives you a *different* answer,
because nothing was written down.

Your data bank persists. `resume.md` reconstructs where a student is from their actual files — and
notably **distrusts its own status note**, reconciling against the CSV, because a real session got
burned by a stale note and gave wrong advice.

### 4.4 "Who actually gets in" — and doing shared work once

Two things a normal user won't get at any prompt quality, because they don't know to ask:

- **The admitted-student texture.** Reddit / The Student Room offer threads, the Common Data Set, NUS
  IGP cutoffs. Real people, real grades, real essay angles. A normal user doesn't know these sources
  exist. This is the genuinely irreplaceable section.
- **Grouping by application system.** 19 universities grouped so Common App work gets filed *once*
  instead of six times, with MIT's own portal broken out separately. That's product design, not
  research. No prompt produces it.

## 5. Pricing: RM50, and why

**The buyer is the A-Level student, not the parent.** Student pocket money sets the ceiling. That
sounds like a constraint; it's actually an advantage worth naming:

> **RM50 is below the ask-my-parents threshold.** An 18-year-old can just decide. A RM250 product
> needs a parent conversation — a pitch you're not in the room for, and a week of delay. RM50 closes
> today.

Why RM50 and not RM20: **cheapness is a signal, and RM20 signals "this took no effort,"** which is
precisely what invites the Gemini comparison. RM50 reads as a real product with a person behind it.
Keep the gap.

But cheapness still has to be **explained**, or it reads as a tell — see §6.

### The first five are free

Independent of price level. This is about your **n = 1 problem**: exactly one student has been through
the pipeline end-to-end. You cannot sell a track record you don't have.

Give the first ~5 away as an **explicit trade**: a testimonial, plus permission to use an anonymized
case study. RM250 of forgone revenue is nothing against what 5 finished, screenshot-able case studies
unlock at RM50 × 50 later. **Buy the proof first, then charge everyone.**

## 6. The honest disarm

Volunteer the weakness. It does three jobs at once:

> *"I've done this properly end-to-end for exactly one person so far. I'm doing it free because I want
> 5 case studies, not because it's worth nothing. If it's rubbish, tell me and pay nothing — I just
> want to use it as an example. RM50 after that."*

1. **Explains the suspicious price** before they have to wonder about it.
2. **Makes them an insider, not a customer.** People help friends build things. Nobody wants to be
   customer #1 of an unproven service.
3. **Drops their risk to zero**, which removes the last reason to think about it and get back to you.

The instinct is to hide n=1. Don't. Somebody *will* ask "how many people have you done this for," and
"one" lands very differently as a confession than as a boast you made first.

## 7. Who should NOT buy — say this out loud

**If a student knows their course, knows their country, and has already picked 3 UK unis — Gemini is
genuinely enough. Tell them so.**

Your product earns its keep when at least one of these is true:

- **Multiple countries are live.** Comparing a 3-year UK degree against a 4-year US one honestly, in
  MYR, total — not annual tuition — is the genuinely hard part, and the part everyone gets wrong.
- **The course is undecided.** The career-backwards interest discovery is a real service in itself.
- **Budget is tight enough that total cost decides it.** Then `Approx total (MYR)` *is* the answer.
- **A regulated profession is involved.** Medicine/MMC, engineering/BEM, law/LPQB, accounting/MIA.
  Getting recognition wrong doesn't mean a worse degree — it means **can't practise in Malaysia**.
  That's a dealbreaker, not a footnote, and it's the highest-stakes thing you check.

Disqualifying the wrong buyer costs you nothing and makes the right buyer's yes real. It's also just
true, which matters more — these are your friends, and you'll see them next semester.

## 8. Voice notes

- **Never** say "AI-powered," "leverage," "comprehensive solution." You're a guy with a spreadsheet
  who did the work. That's more credible than any adjective.
- **Never** oversell the research. "I checked the official pages" beats "extensively researched."
- **Show numbers, not claims.** "41 columns" > "very detailed." "16 sections, 6 pages" > "in-depth."
- **The dossiers include reasons to hesitate.** Say that. A list that only says nice things about
  every uni is a list nobody trusts. This is the single most credibility-building fact you have:
  *"inform conviction, don't sell"* is literally the rule the workflow runs on.
