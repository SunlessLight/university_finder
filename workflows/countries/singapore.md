# Singapore — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> a Singapore row. Split out of `03_discover_longlist.md` on 2026-07-30 — see that file's
> "Per-destination query playbook" section for how this fits into Step 1 and Step 3.

> **No private/foreign campus offers engineering (checked 2026-09-10, har-ley's Mechanical
> Engineering pass).** JCU Singapore's programmes are Business/IT/Psychology/Education/
> Accounting/Arts/Aquaculture/Environmental Science/Games Design/Tourism; Curtin Singapore is
> Health/Computing/Commerce/Communications with engineering only "planned," not live. For an
> Engineering-field student, widen the Safety end within the public five instead (NTU's
> Renaissance Engineering Programme and SIT's two ME routes — its own degree plus the SIT-Glasgow
> joint honours — worked well as substitutes). Re-check this if researching a non-Engineering
> field, where JCU/Curtin remain valid.

**Singapore** → the public five + a private/foreign campus for the Safety end (Engineering fields: see the note above first):
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
> **The "no separate form" claim above is NUS's process, not universal (learned 2026-08-23,
> GwakGwak3000's Mechanical Engineering pass).** NTU's own ASEAN Undergraduate Scholarship page requires
> a separate application with an essay and referee report — check each university's own scholarship page
> rather than assuming NUS's auto-consideration model carries over.
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
> **Update 2026-09-23 (zhiqi's NUS pass) — the soft door above is now the ONLY door, and the major was
> renamed.** NUS's Faculty of Science route was **Data Science and Analytics (DSA)** for cohorts
> AY2019/20–AY2025/26 and is superseded by **Data Science and Applied AI (DSAAI)** from AY2026/27 onward.
> DSAAI has **no direct-admit course** — you apply for admission to the Faculty of Science and read the
> major after. So don't go looking for a DSA course page to compare against; for anyone entering AY2026/27
> or later the Faculty route *is* the route, and it is still the softer-profile backup worth putting in a
> Reach row's report. Separately, **NUS School of Computing now admits Computer Science and Artificial
> Intelligence in ONE common pool** (AY2025/26 onward, `comp.nus.edu.sg/programmes/ug/ai/`): applicants
> don't choose between the two at application and pick the degree after years 1–2. That is a real hedge
> built into the admission — say so in `Course at a glance` and in the report's entry-route section. The
> official degree name as written is "Bachelor of Computing in Artificial Intelligence (with Honours)".
>
> **`nus.edu.sg/oam/*` is JS-rendered and returns an EMPTY BODY to a plain WebFetch — HTTP 200, no error,
> no content (confirmed 2026-09-23, cost two fetches).** This is the textbook case of guardrail 6's "a
> response that doesn't contain the fact you went there for" counting as *blocked*. Go **straight to
> `firecrawl_search.py`** for every OAM page — fees, living costs, scholarships, important dates, the
> international-qualifications requirements. The same pass also found the official fee PDF
> (`nus.edu.sg/registrar/docs/default-source/administrative-policies-procedures/ugtuitioncurrent.pdf`)
> comes back **garbled** on a plain fetch but clean via Firecrawl — it carries the real five-tier table
> (AY2026/27 Computing: Citizen 8,300 / PR 11,600 / **Intl-with-grant ASEAN 18,050** / Intl-with-grant
> non-ASEAN 21,400 / Intl-without-grant 39,700, SGD/yr).
>
> **NUS asks EVERY applicant for more than grades — and it is an ADMISSION risk, not a scholarship
> footnote (confirmed 2026-09-23 against NUS's own Aptitude-Based Admissions page).** Every applicant to
> every degree must list **up to four** achievements / co-curricular / non-academic activities *and*
> answer short-response questions in the same section. NUS's official page and its sample PDF confirm the
> section is mandatory and the four-achievement cap, but **do not state how many questions** — applicants
> on r/nus report five, most capped around 500 characters. Attribute it that way; don't assert five as
> official. Two consequences: (1) a straight-A student with nothing on file is **not** a safe applicant
> here, and (2) since the ASEAN Undergraduate Scholarship is interview-selected *from admitted
> applicants*, the same four achievements gate both admission and funding. Our Google Form does not
> collect any of this — expect `profile.achievements` to be null and raise it at the Stage 4 checkpoint.
>
> **A standardised test (SAT / ACT-with-Writing / AP) is required from applicants who finish their final
> exam AFTER the closing date** (official international A-Level page, 2026-09-23). A Malaysian sitting
> A2 in Oct/Nov with January results lands in the "completed" column before a mid-February close — but it
> is tight, and the consequence of being on the wrong side is a whole extra test. Tell the student to
> confirm the sequencing with NUS in writing rather than assuming it.
>
> **Two NUS scholarship traps:** the **AI Talent Scholarship is Singapore Citizens only** — don't put it
> in an international student's row. And the ASEAN Undergraduate Scholarship's official page (reachable
> via Firecrawl) carries figures the aggregators miss: 100% of post-grant tuition + **S$5,800/yr living +
> S$3,000/yr accommodation** + S$1,750 one-time computer allowance, GPA 3.50 to renew, interviews Jan–Jul,
> outcomes mid-July, 75%-of-units-in-Singapore cap, no stacking without approval. Third-party pages
> routinely drop the accommodation allowance entirely.
>
> **NUS's official undergraduate living-cost figure** (`nus.edu.sg/oam/financial-aid/living-costs`, via
> Firecrawl): **S$6,000/yr EXCLUDING accommodation** (meals 2,600 + personal 2,200 + transport 800 +
> books 400), plus on-campus hostel **S$4,000–10,290/yr**. All-in ≈ S$10,000–16,300/yr; S$14,000 is a
> defensible working mid-point. This supersedes the "S$12,000–18,000, not an official number" estimate
> used before 2026-09-23 — that guess is no longer necessary.
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
