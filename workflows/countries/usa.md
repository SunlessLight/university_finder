# USA — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> a US row. Split out of `03_discover_longlist.md` on 2026-07-30 — see that file's "Per-destination
> query playbook" section for how this fits into Step 1 and Step 3.

**USA** → Common App + department + outcomes:
```
<course> Common App universities
<university> <department> admissions requirements international
US News best <field> programs
OPT STEM <field> post study work
```

## Known-good sources (locations, never values)

> Places to **fetch**, never facts to quote — a fee, deadline or cutoff comes off the page every
> time (guardrail 2). `free` = plain `WebFetch` works; `blocked` = the page exists but 403s a
> plain fetch, so skip the retries and go straight to `firecrawl_search.py`; `quirk` = reachable
> only at the exact address given. Confirmed 2026-08-08. If one 404s, go up to the site root
> rather than guessing a deeper path — then fix the row here. **Cross-country sources —
> rankings, Malaysian sponsors, MQA + the professional bodies, English tests — are in
> `workflows/sources.md`**, not repeated per country.

| Answers | URL | Fetch |
|---|---|---|
| Which universities take the Common App, their requirements and deadlines | `https://www.commonapp.org/apply/first-year-students` | free |
| CSS Profile — the aid form internationals usually **must** file at application | `https://cssprofile.collegeboard.org/` | free |
| Official cost, aid and graduate-earnings data per institution | `https://collegescorecard.ed.gov/` | free |
| Official admissions/enrolment stats (admit rate, test ranges) | `https://nces.ed.gov/collegenavigator/` | free |
| Is the engineering/computing programme ABET-accredited (feeds BEM/Washington Accord) | `https://amspub.abet.org/` | free |
| F-1 student visa | `https://travel.state.gov/content/travel/en/us-visas/study/student-visa.html` | **blocked** |
| SEVIS I-901 fee | `https://www.fmjfee.com/` | free |
| OPT + 24-month STEM OPT | `https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-opt-for-f-1-students` | free |

**The Common Data Set has no central host** — it is published per university, so search
`<university> common data set` and take the university's own PDF/page. That is the source behind the
admitted-profile stats in a Stage 4 report's *Who actually gets in*.

**Need-blind / meets-full-need status has no register either**, and that is deliberate — the cohort
drifts (see the trap below). It comes off each university's own international-aid page, every time.

> **For the USA, FUNDING is the real axis — not sticker price.** A 4-year US degree runs ~840k-1.8M MYR,
> so for most Malaysian budgets *every* US row busts the ceiling at sticker and the list is meaningless
> unless built around aid. Always add these queries:
> ```
> US universities that meet full financial need for international students undergraduate
> need-blind admissions for international students US universities list
> <university> international students financial aid CSS Profile
> ```
> **Need-BLIND vs need-AWARE for internationals is the distinction that matters** — at a need-aware
> school, *requesting aid actively lowers admission odds*, so it belongs in `entry_margin` and `Notes`,
> not just the scholarship columns. And a sub-5%-acceptance deal-breaker removes the most selective end.
>
> **The need-blind-for-international cohort membership drifts — always re-check against each university's
> OWN current page, not a remembered list or even a past "confirmed" note in this file (learned
> 2026-07-28; corrected again same day after a second session re-verified).** Bowdoin's July
> 2022 press release states *"Bowdoin joins Harvard University, Princeton University, Massachusetts
> Institute of Technology, Yale University, Dartmouth College, and Amherst College in including all
> students, regardless of citizenship, under its need-blind admissions policy"* — a clean, citable 7-school
> cohort **as of 2022**. Brown is widely reported to have joined later (~Class of 2029) — plausible but
> re-verify the year. **Washington & Lee and Notre Dame have since joined too — both are need-blind AND
> meet 100% of demonstrated need for international undergraduates, per their own pages, verified
> 2026-07-28:** Notre Dame's `admissions.nd.edu/apply/resources-for/international-applicants/international-faqs/`
> states "We offer need-based financial aid that meets the full demonstrated need of all undergraduate
> students, domestic and international"; W&L's `wlu.edu/admissions/financial-aid/types-of-aid/international-student-aid`
> states "W&L is need-blind in its admissions decisions" and "meets 100% of demonstrated financial need
> without loans for every admitted student." Both changes came from large 2024 gifts — Notre Dame's
> "Pathways to Notre Dame" initiative (announced 2024-09-13, effective Class of 2029) and W&L's $132M gift
> (announced 2024-10-24/25, effective Class of 2029) — **both postdating Bowdoin's 2022 anchor**, which is
> exactly why an earlier pass of this note (same session, same day) checked Notre Dame's general costs page
> instead of its international-applicants FAQ, found no international mention, and wrongly concluded
> need-aware/uncertain. **The actual lesson, twice-learned: "absent from an older confirmed list" is not the
> same as "excluded" — a school can join after the anchor source's date, so always check for a MORE RECENT
> institutional announcement before treating an exclusion as settled,** and prefer a page written for
> international applicants specifically (an FAQ, an "International Student Aid" page) over a general costs
> page that may simply not mention international status either way. Don't assume this correction is final
> either — this cohort keeps growing; re-verify against each university's own current page every time, and
> don't just trust this note's snapshot indefinitely.
>
> **Headline admit rates lie for aid-seeking internationals.** Duke publishes ~6% but funds only **20-25
> international students a year** university-wide, in a *separate* pool — the effective rate is far lower.
> Read the aid page, not the admissions brochure.
>
> **Expect the US list to be all Reach**, and say so rather than manufacturing a fake Safety: meets-full-need
> ∩ >5% admit ∩ good ranking is a tiny set with no safe end. The balanced-shortlist rule applies **across
> the whole list, not per country** — source the Safety from the UK/Australia/local instead.
>
> **The liberal-arts trap:** the most aid-generous schools (Amherst, Grinnell, Richmond, Bowdoin, W&L) have
> **no QS rank** and little Malaysian employer recognition, and often offer data science only as a *minor*.
> They score badly on ranking-led priorities despite being strongest on funding. Surface the trade-off and
> ask the student what "the name" means to them — QS rank or US reputation. Don't silently drop or inflate them.
>
> **Check the testing policy per school.** Test-optional is receding: Cornell, Dartmouth, Brown, Yale and
> Penn have all reinstated the SAT/ACT. If the student has no score, flag it — it's an action item with a
> deadline, not a disqualifier.
