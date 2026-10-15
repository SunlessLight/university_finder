# B2B research — progress and context

*Last updated 2026-10-15. Read this first, whether you're Evan or a fresh session picking up the work.*

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
- `report.md` and `report.pdf`: **not written yet.** They combine the six fragments into one
  report, built in the main session, because ranking who to approach first is a judgement call.

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

## Next step

Assemble `report.md` from the six fragments (11 sections, listed in the plan), then render the PDF:

```
python tools/md_to_pdf.py --type report --input business/b2b_research/report.md
```

Do this in a **fresh session**: the six fragments are about 190 KB of reading. Say
"assemble the B2B report from the plan" and point it at this file. After that, update guess D in
`business/launchx/status.md` to point at the report and its first contact targets.

Before the report goes to Evan, the plan also asks for:
- 3–5 key numbers spot-checked by opening their sources (commission rates, package prices, tool prices).
- A search of the whole folder for student names.
- The PDF opened and checked so the tables and glossary display properly.
