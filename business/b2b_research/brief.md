# B2B buyer research — shared agent brief

Read this whole file before researching. Your dispatch prompt names your stream number; everything
else you need is here.

## Why this exists

The founder (one student, building a university-shortlist service for Malaysian students) is
considering selling that research **to education businesses** instead of to families at RM50.
The product: for each student, an honest longlist of universities that keeps "good university"
separate from "can you get in" (Reach/Match/Safety), shows **total cost of the degree in MYR**,
covers any university (not just partners), and gives reasons *not* to go somewhere. Output is a
spreadsheet plus PDF reports. Context: `business/launchx/competitors.md` (read it — it shows the
B2C competitor picture and the "who pays them" conflict test).

The pack tells the founder **who to talk to and what to ask**. It does not decide whether anyone
would pay. Don't write a verdict; write evidence.

## Scope

- **Malaysia only.** Global players only for their Malaysia operations. Global software only where
  Malaysian organisations use it (or plausibly could — say which).
- **Education only.** No general "automation agency" angle.

## Streams

| # | Fragment file | Covers |
|---|---|---|
| 1 | `fragments/01_agents_portals.md` | Education agents and free portals (IDP, MABECS, AECC, SI-UK, Uni Enrol, EasyUni, EduAdvisor, plus others you find): services, customers, commission model and rates, size, staff roles, revenue where public (e.g. IDP annual report) |
| 2 | `fragments/02_paid_consultants.md` | Paid admissions consultants (Crimson, Inquota, plus others found): packages, prices, staff, how they build lists, size |
| 3 | `fragments/03_schools_colleges_scholarships.md` | Pre-university college counselling/placement offices (Sunway, Taylor's, HELP, INTI…), international-school counsellors, scholarship bodies (MARA, JPA, Yayasan…): who pays, caseload, budgets |
| 4 | `fragments/04_institutions_recruitment.md` | Private universities and branch campuses: recruitment and international offices, what they spend to get students, whether they are a buyer, and the conflict this creates |
| 5 | `fragments/05_existing_b2b_tools.md` | Software sold to the groups above (Cialfo, BridgeU, Unifrog, ApplyBoard, Adventus, others): what it does and doesn't do (total cost in MYR? honest fit?), pricing, which Malaysian organisations use it |
| 6 | `fragments/06_selling_and_rules.md` | How buying works per type, events and associations, PDPA as a data processor, agent codes, B2B pricing models, pain-point evidence from job ads (JobStreet), reviews and forums |

Paths are relative to `business/b2b_research/`. Write **only your own fragment file**. Do not edit
anything else in the repo.

## Research rules

1. **Search order.** `WebSearch` / `WebFetch` first, for everything. If a page is blocked, errors,
   or comes back without the fact you went for (JS-rendered pages often return empty), run
   `python tools/firecrawl_search.py "<query>" --out .tmp/b2b_research/<stream>_<n>.json --scrape-top 2`
   and read the JSON. Don't ask permission; just run it.
2. **Every number carries a source or the word "estimate".** No market sizes, commission rates,
   salaries or prices from memory.
3. **Tag every substantive claim** `[Known]` (a source you opened says it), `[Guess]` (your
   reasoning, say from what), or `[Unknown]` (looked, couldn't find — say where you looked).
   "Unknown" is a useful answer; a confident invention is not.
4. **Opened vs not.** In the sources table, say whether you actually opened the page or only saw a
   search snippet. Prefer opened.
5. **Plain English.** The reader is new to business. Gloss any term on first use in brackets, e.g.
   "commission (a fee the university pays the agent per enrolled student)".
6. **No PII.** No student names, no private individuals' personal details. Named organisations and
   publicly listed business roles/titles are fine (e.g. "Head of Counselling, X College"); don't
   harvest personal emails or phone numbers. Don't cite a person's own LinkedIn profile (`linkedin.com/in/...`)
   either. Cite the company page, the job ad or the organisation's own site, or describe it as
   "LinkedIn search snippet" without the link.
7. **Be concrete.** Named organisations, real prices, real job-ad wording beat generalities.
8. Keep the fragment to roughly 1,500–3,000 words. Depth over padding.

## Fragment template (all 10 sections, in this order, these headings)

```markdown
# <Stream title>

*Stream N. Researched <YYYY-MM-DD>.*

## 1. Summary in 5 lines
   (then, directly under it, a quoted box "Gaps in this research", a table with the columns
   Gap | Why it matters | How to close it, listing everything you looked for and couldn't verify.
   The founder reads this box to know how far to trust the fragment, and report.md's
   "Open unknowns" section is assembled from these boxes.)
## 2. Who they are
   (types/sub-types, named players, size: offices, staff, students placed — sourced)
## 3. Customers
   (who they serve, who pays them — these can differ)
## 4. How they make money
   (fee/commission model, rates, revenue where public)
## 5. Pain points
   (evidence-backed: job ads, reviews, annual reports, interviews, forum posts. Required.)
## 6. How they shortlist today
   (who builds the university list for a student, how long it takes, what tools)
## 7. Fit with an honest, family-first list
   (does an honest, any-university, total-cost list help or hurt their income? where's the conflict?)
## 8. Named organisations to contact
   (table: organisation | type | why them | public contact route e.g. website form / LinkedIn company page / event)
## 9. Questions to ask them
   (Mom Test style: about past behaviour and current spend, never "would you buy?")
## 10. Sources
| Claim | Source | Did I open the page? |
|---|---|---|
```

A fragment with no opened sources will be sent back.

## When done

Reply to the main session with **only**: the fragment path, a one-line summary, and a flag line
listing anything you couldn't verify that matters (e.g. "commission rate range is from one
source only"). Don't paste the research into the reply.
