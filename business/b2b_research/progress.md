# B2B research — progress and context

*Last updated 2026-10-15 (report assembled). Read this first, whether you're Evan or a fresh session picking up the work.*

## What this folder is

On 15 Oct Evan floated a **pivot** (a big change of direction): stop selling the university
research to families at RM50, and sell it to **education businesses** instead (agents,
paid consultants, pre-university colleges, scholarship bodies, private universities). That idea
is "guess D" in `business/launchx/status.md`.

Evan doesn't yet know how these businesses work, so this folder is a **desk-research pack**
(research done online, without talking to anyone yet). Its job is to tell him **who to talk to
and what to ask**. It can't say whether anyone would pay. Only real conversations can answer
that, so the pack ends in a contact list and an interview script, not a verdict.

Scope: **Malaysia only**, **education only**.

The full plan is in `C:\Users\User\.claude\plans\ok-to-be-honest-starry-thompson.md`.

## How it's built

- `brief.md`: the instruction sheet every research agent followed (rules plus a 10-section template).
- `fragments/`: six research write-ups ("streams"). Each was written by its own background
  research agent.
- `report.md` and `report.pdf`: **done 15 Oct.** 11 sections, 18 pages of reading plus 32 pages of
  sources (section 11 is generated from the fragments' tables, so re-run the append rather than
  hand-editing it if a fragment changes).

## Status of each stream

| # | Fragment | Covers | Status |
|---|---|---|---|
| 1 | `01_agents_portals.md` | Education agents and free portals (IDP, AECC, EduAdvisor…) | Done |
| 2 | `02_paid_consultants.md` | Paid admissions consultants (Crimson, Inquota…) | Done |
| 3 | `03_schools_colleges_scholarships.md` | College counselling offices, international schools, scholarship bodies | Done |
| 4 | `04_institutions_recruitment.md` | Private universities and branch campuses | Done |
| 5 | `05_existing_b2b_tools.md` | Software already sold to these businesses (Cialfo, BridgeU…) | Done |
| 6 | `06_selling_and_rules.md` | How they buy, events and associations, privacy law, agent codes, pricing models, job-ad pain points | Done (15 Oct, checked below) |

## Stream 6: checks and gaps

**Checks passed** (15 Oct):
- Has all 10 template sections, in order.
- 38 sources listed; the agent actually opened 21 of the pages. The rest are search-result previews.
- Claims are labelled: 21 Known (a source says so), 14 Guess, 4 Unknown.
- No student names from `data/students/` appear in it.
- About 4,500 words, longer than the brief's 1,500–3,000. The other streams also ran long; it
  gets trimmed when the report is assembled.

**Strongest part:** the PDPA section. PDPA is the Personal Data Protection Act 2010, Malaysia's
privacy law. The agent read the 2024 amendment (Act A1727) and the PDP Commissioner's official
guidelines in full. This matters because handling another company's student data would make Evan
a **data processor** (someone handling personal data for another company), and since 2024 that
role carries its own legal duties.

**Gaps:** the full list of things the agent couldn't confirm is at the top of `fragments/06_selling_and_rules.md`, in the box headed "Unverified gaps". It lives there so the session that assembles the report sees it while reading the fragment. The biggest one: no Malaysian forum or review evidence, so the pain points come from job ads only.

## Cross-check of all six streams (15 Oct, main session)

All six fragments have the 10 sections and opened sources. Name check across the folder: clean
(67 name tokens from `data/students/`, 0 hits). **Spot-check requirement is met:** 6 numbers were
already checked (Taylor's 2.7% and bursary in stream 4; Scoir, Adventus, Manifest/EduGo and Alice
Smith's Cialfo in stream 5), plus 3 re-opened on 15 Oct (Inquota RM2,000 and its "200+"/"2000+"
contradiction; Ivy Summit package prices exact; Alice Smith's careers page names Unifrog). The only
number type no main session has opened is a **commission rate**. That is optional.

**Four problems. Fix them while assembling the report, not as a separate pass first:**

1. **Inquota is mislabelled in guess D and in `competitors.md`.** Both call it a family-paid
   consultant. Stream 2 found 100+ partner universities and agency-network ties, and the site says
   nothing about who pays it (re-checked 15 Oct). Write it as "unconfirmed: may also earn
   commission". Don't use it as the example of a family-paid buyer. Fix this in the guess D update
   at the end.
2. **Stream 3 is out of date on school software.** It says no Malaysian school was confirmed on
   Cialfo or BridgeU. Stream 5 confirms Cialfo (Alice Smith, ISKL, IGBIS) and BridgeU (King
   Henry VIII). Go with stream 5. Alice Smith probably uses both Unifrog (careers page) and Cialfo
   (2023 blog).
3. **Stream 5's gap 6 is closed.** "348 international schools, 111,185 students" was opened by
   stream 3 (Asia News Network). Cite that source and drop the gap.
4. **Stream 1 has no "Gaps in this research" box.** It was written before the box was added to the
   brief. When building report section 10 (Open unknowns), gather stream 1's `[Unknown]` tags from
   its body instead.

**Also when updating `business/launchx/status.md`:** it is already 123 lines, against the plan's
~70. Trim it, don't just add to it.

**Points for the report that no single fragment makes** (main-session reading, label as Guess):
- Price anchors from nearby products are low: Scoir about RM19 per student per year, Morrisby
  about RM137 per profile, school licences about RM3,300–4,100 a year (repo exchange rates, estimate).
  They don't support "businesses would pay much more than RM50" on their own. Put this in the
  offer-options section.
- PDPA processor rule (stream 6): a client's student data can't be reused for Evan's own purposes.
  University research isn't personal data, so reusing it is fine. The pipeline runs on overseas
  services (Claude, Firecrawl), so each client has to accept the data leaving Malaysia.
- Capacity: a school brings a whole cohort (KTJ sixth form = 300), but guess D's first offer is
  Evan doing it by hand. The offer-options section should say how many students a done-for-you
  pilot can actually take.

## Report assembled (15 Oct)

- All four cross-check problems handled: Inquota written as "unconfirmed: may also earn
  commission" (report 4.2, guess D, and a footnote in `competitors.md`); stream 5 used over
  stream 3 on school software; stream 5's gap 6 marked closed; stream 1's `[Unknown]` tags
  gathered into report section 10.
- Commission rates spot-checked by opening the source: USIM RM1,500 (two RM750 instalments) and
  PIE News 2021/22 per-student averages. Both match.
- Name check across the folder, including report.md: clean (111 tokens; only false alarms were
  "Hong Kong").
- PDF checked visually: tables, the red decision box, the blue Inquota note, and the Key terms
  glossary all render. Two renderer quirks fixed: a list needs a blank line before it, and "MD" in
  a source row pulled in the "Doctor of Medicine" glossary entry.
- `business/launchx/status.md` guess D now points at the report. File trimmed 123 → 106 lines, not
  ~70: going further means deleting open items, which is Evan's call.

## Next step

Evan reads `report.pdf` (sections 1–10, about 30 min), decides the partner-only red line, and
makes the first call (the Sunway placement-office chat already planned). Interview notes go in
this folder; after five calls, revisit the ranking in report section 8.
