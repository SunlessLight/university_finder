# Singapore — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> a Singapore row. Split out of `03_discover_longlist.md` on 2026-07-30 — see that file's
> "Per-destination query playbook" section for how this fits into Step 1 and Step 3.

**Singapore** → the public five + a private/foreign campus for the Safety end:
```
NUS OR NTU OR SMU <course> admissions
SUTD OR SIT <course> undergraduate international admissions
Singapore MOE tuition grant ASEAN undergraduate tuition fees
ASEAN Undergraduate Scholarship NUS NTU
JCU OR Curtin OR SIM Singapore <course> bachelor international fees
Singapore Employment Pass minimum salary graduate
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
| MOE Tuition Grant — the subsidy **and the 3-year bond** that decide the real fee | `https://www.moe.gov.sg/financial-matters/tuition-grant-scheme` | free |
| Student's Pass (ICA) | `https://www.ica.gov.sg/reside/STP/apply` | free |

The five-tier fee table itself is per-university (NUS/NTU/SMU/SUTD/SIT each publish their own) — the
MOE page tells you which tier the student lands in and what it costs them in bond years, which is the
part aggregators always drop.

> **Singapore and Malaysia were one block until 2026-07-29** — `COUNTRY_NORMALIZE` fused them into a
> single `Singapore/Malaysia` token, so a student who ticked only Malaysia got Singapore rows. They are
> two countries with almost nothing in common operationally (fee tiers, recognition ladder, entry
> system, cost), and now two separate passes.

> **SINGAPORE — for an ASEAN student, the funded public unis are a genuine mid-band, not a Reach wall
> (learned 2026-07-16, Ong).** The playbook that worked: 10 queries covering NUS / NTU / SMU / SUTD / SIT
> (public) **plus** a private/foreign campus (JCU / Curtin / SIM) for the Safety end, **plus** three
> structural queries — the MOE Tuition Grant bond, the with-grant-vs-without fee split, and the ASEAN
> Undergraduate Scholarship. Add a post-study-work query too (see below). Traps, in order of how badly
> each bites:
>
> **The fee table has FIVE tiers, not two — and the one you want is buried in the middle.** NUS/NTU/SMU
> pages (and NUS's official fee PDF) show, left to right: **Singapore Citizen · Singapore PR · International
> WITH Tuition Grant (ASEAN) · International WITH Tuition Grant (all other) · International WITHOUT Grant.**
> For a **Malaysian (ASEAN) student the correct column is the third**, and it is roughly *half* the
> no-grant column. NUS Computing/Science AY2026/27: ASEAN-with-grant **S$18,050** vs no-grant **S$36,650-39,700**.
> The citizen rate (~S$8,300) is the Australian-domestic-fee trap all over again — **if a Singapore fee
> looks like ~S$8-10k it is the citizen rate; do not use it.** Pick the tier deliberately and say which in
> `notes`. MOE sets the subsidised tiers, so NUS and NTU's ASEAN-with-grant figures match to the dollar —
> a useful cross-check when one page's column labels are ambiguous (NTU's fee page returned *different*
> labels on two fetches; the S$18,050 held because it matched NUS's PDF).
>
> **The Tuition Grant is the row's real story, and its "cost" is a feature for a migration-minded student.**
> ~50% fee cut in exchange for a **3-year bond working for a Singapore-registered company** after
> graduating. For `intent_to_migrate: true`, that bond is close to a guaranteed graduate pathway — it
> should *lift* `post_study_work_fit`, not lower it. The **ASEAN Undergraduate Scholarship** stacks on top:
> **automatic consideration on the admission application (no separate form)**, 100% of post-grant tuition +
> living/accommodation allowances, interview-selected. That auto-consideration structure is worth more than
> a bigger award you must separately win — score it well. Private/foreign campuses (JCU etc.) get **neither**
> the Grant nor the scholarship — their listed fee is the full fee.
>
> **Admissibility is the mirror of Australia — measured, and often a Reach.** NUS/NTU publish an
> **Indicative Grade Profile (IGP)**, but note two things: (1) it is for **Singapore-Cambridge** A-Levels,
> not international A-Levels, and international places are capped — so treat it as *indicative*, not the
> arithmetic Australia gives you; (2) the direct-admit data courses are so oversubscribed the profile is
> **AAA/A at BOTH the 10th and 90th percentile** (no spread) — a single B (Ong's Physics) pushes a student
> into Reach. **The escape hatch is the entry door:** at NUS, applying to the **Faculty of Science** and
> declaring the Data Science major *after* admission has a far softer published profile (ABB/C → AAA/A) than
> the direct-admit courses. Finding the soft door can turn a Reach into a Match at the same university —
> protect it. Don't invent an acceptance rate to test a sub-5% deal-breaker against; NUS/NTU don't publish
> one, and the IGP is not a rate. NTU's IGP is a **PDF that Firecrawl/WebFetch won't render** — if you can't
> get the real bar, say the entry margin is inferred and flag it for Stage 4, don't fake precision.
>
> **Singapore's intake is August — it maps cleanly to a "Sept" preference** (unlike Australia, which has no
> September intake). One intake a year. Public degrees are **4 years** (direct honours). A private
> trimester campus can run a bachelor's in **2 years** (JCU Singapore) — the inverse of the Australian
> honours trap, and usually the cheapest row on the list; but a 2-year BSc raises **two real Stage-4
> checks: MQA recognition, and whether it qualifies for Employment Pass COMPASS points.**
>
> **There is NO post-study work visa.** The Student's Pass lapses at graduation (~30-day grace); staying
> needs an **Employment Pass** — a job offer at **S$6,000/month (non-financial) or S$6,600 (financial)
> from 1 Jan 2027**, plus COMPASS points. Put this in `post_study_work` honestly: the *bond* guarantees
> three years of work, but a *long-term* stay still runs through the EP salary bar.
>
> **The SMU name-collision trap (cost a scrape this session):** `datascience.smu.edu` and `smu.edu` are
> **Southern Methodist University in Dallas, Texas** — not Singapore Management University (`smu.edu.sg`).
> A scrape of the Texas site returned US fees. Any `smu.edu`-without-`.sg` result is the wrong SMU. Also:
> SMU offers data science as a **second major on an Economics/Computing degree**, not a standalone DS
> degree — score `course_match` for what it actually is.
