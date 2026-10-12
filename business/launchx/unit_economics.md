# Cost to serve one student

*For slide 8 (Revenue Model & Financial Projection). Finished 2026-10-12 from your answers.*

"Unit economics" means what you earn and spend on one customer. The panel will ask: *"How does
this grow?"* This page is the honest answer.

## The short version

- **Hands-on time:** under 30 minutes for a list, under 30 minutes for a report. So **under one
  hour per student** for a list plus one report. (Your figures, 12 October.)
- **Tools:** about **RM158 a month in total**, however many students you serve.
- **At RM50, four students a month pay for the tools.** Everything after that pays you.
- **The real limit is not hours. It is interruptions.** Each student needs you at your laptop at
  three or four separate moments (start, approve, check, send). So a job with under an hour of
  work in it takes most of a day to finish, and it pulls you out of your studies each time.

That last point is the one to say to the panel. It is true, it is specific, and it has a fix.

## What the tools cost

| Tool | What you pay now | What I used for the slide | Why |
|---|---|---|---|
| Claude (the AI that runs the research) | USD 20 a month, shared with your other work | **RM81 a month** | USD 20 at RM4.04, the rate the tools use (stamped 2026-09-23). The full amount is an upper limit, because you use it for other things too. |
| Firecrawl (the paid web-scraping service, used only when free search is blocked) | RM0, on the free plan of 1,000 credits a month | **RM77 a month** | The cheapest paid plan: USD 19 a month for 5,000 credits. Source: [firecrawl.dev/pricing](https://www.firecrawl.dev/pricing), opened 12 October. |
| **Total** | about RM81 | **about RM158 a month** | |

**Why I priced Firecrawl as paid when you pay nothing.** Today you use the free plan with
several keys. That is fine for testing. But a cost of "zero, because I switch between free
accounts" is not a number an investor will accept, and Firecrawl's terms let it close an account
for any reason. A paid business should not depend on that. At RM77 a month it is small, so cost
it honestly and move on.

**You do not need to build a key-switching script.** `tools/firecrawl_search.py` already does
it: when one key runs out of credits it moves to the next one by itself.

**If you ever paid per use instead of a flat plan:** the one measured run (10 US universities,
in `token_cost_report.md`) came to roughly USD 2 to 3 for the research step. That is an estimate
for one country, and reports were never measured.

## One year, three ways

Each row is "students a month × RM50, minus RM158 for tools". I used one hour of hands-on time
per student, which is the top of your range.

| Students a month | Money in | Tools | Left over each month | Your hands-on hours | Left over per hour | Left over in a year |
|---|---|---|---|---|---|---|
| 10 | RM500 | RM158 | RM342 | 10 | about RM34 | about RM4,100 |
| 20 | RM1,000 | RM158 | RM842 | 20 | about RM42 | about RM10,100 |
| 30 | RM1,500 | RM158 | RM1,342 | 30 | about RM45 | about RM16,100 |

**What these assume, so you can say so if asked:**

- Every student pays RM50. Nobody has paid yet, so this is untested.
- The same number of students every month. Real demand will bunch up around application season.
- 10 a month is about your pace so far (29 students since you started), so it is the realistic
  row. It is also about a quarter of one Sunway A-level cohort (477) in a year.
- 30 a month would mean most of a cohort. That is a ceiling, not a plan.
- The flat Claude plan has a usage limit. At some number of students you would need a bigger
  plan. I cannot measure where that is from here.

## What this says

Two things, and they match what [market_sizing.md](market_sizing.md) found.

**1. The business is cheap to run.** Four students a month cover the tools. You do not need
money to keep going. That matters for slide 10: your ask is introductions and a mentor, not
funding. If you do ask for the fund, a full year of tools is about RM1,900.

**2. At RM50 it stays small.** Even the best row is about RM16,000 a year. The price is the
lever. The same 10 students a month at RM150 would leave about RM1,340 a month instead of RM342.
That is an illustration, not a price I am proposing. What a parent would pay is what the parent
chats test.

## The answer to "how does this grow?"

> "Each student takes me under an hour of hands-on work, and the tools cost about RM158 a month
> in total. What slows me down is not the work. It is that each student needs me at my laptop at
> three or four separate moments. So growing means cutting those moments: do them in one sitting
> a day now, then automate the checking and sending. I want to prove people will pay first, and
> automate second."

## One thing you could try now, with nothing to build

You said the switching between studies and this has taken a toll, and that there is no reminder.
That is worth fixing for your own sake, not only for the pitch.

**One fixed slot a day.** Pick a time when the laptop is already open, for example the evening.
In that slot: send whatever finished yesterday, check it, then start today's runs and close the
laptop. Nothing during the day.

It trades speed for calm: a student waits until the next slot instead of a few hours. For a
decision that takes months, a one-day turnaround is fast. It also gives you a promise you can put
on the poster: "your list within 2 days".
