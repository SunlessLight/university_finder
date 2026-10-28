# 05. University report instructions (Stage 4 report + standalone quick report)

*Fact audit, 2026-10-28. Written for Evan (no technical background). Labels: G guess, A advice,
Y yapping, J unlabelled judgment, L loophole. Severity: High reaches a student, Medium could,
Low internal.*

## What this part makes
This part is the rulebook for the **university report**: the 15-section, roughly 25-page PDF a
student gets for each university they pick as a finalist (Stage 4), or for one university they
already have in mind (the "quick report", which needs no intake form). The rulebook is three
files. `workflows/04_university_report.md` is the how-to: what goes in each section. 
`.claude/agents/report-writer.md` is the job description for the AI helper (a "subagent", meaning
a separate AI worker sent off to do one job) that researches and writes each report.
`workflows/quick_university_report.md` covers what changes when there is no student. Two short
`/report` and `/quick-report` launcher files start these jobs. A script (`build_report.py`) turns
the helper's notes into the report, and a checker (`check_report.py`, like a spell-checker for
structure) looks it over before it becomes a PDF.

**Which sections are facts and which are judgment, by design:**
- **Pure facts with sources (by design):** §1 Snapshot (except Admission likelihood and net
  cost), §2 Identity, §5 What you'll study, §6 Signature experiences, §10 Costs, §11 Scholarships,
  §12 Outcomes and recognition, §15 Sources.
- **Facts from forums and social media (opinion dressed as texture):** §7 Culture & vibe, §8
  Student life, §9 City & belonging, the "who gets in" part of §4, and §13 Unique facts ("colour").
- **Judgment by design:** §3 "your fit", the personal half of §4 (Reach/Match/Safety, "your
  profile against that"), and §14 "Why here / why hesitate". The rules ask for an "honest"
  opinion here, but never ask for it to be labelled as an opinion or for the reasoning to be shown.

## Who sees it
- **Students:** every finalist report PDF (`data/students/<slug>/reports/*.pdf`) and every quick
  report (`data/quick_reports/*.pdf`).
- **The public:** `business/sales/sample_pack/sample_university-report_MIT.pdf`, the sample
  shown to customers (pages 1–10 audited here).
- **Helpers only:** the three instruction files and two launchers themselves.

## Findings

Rows 1–15 are instructions (what lets the problem in). Rows 16–31 are what actually reached the
public sample PDF ("p" = page).

| # | Where (file:line) | Quote (≤20 words) | Label | Severity | Why it matters | Suggested fix (one line) | Already in backlog? |
|---|---|---|---|---|---|---|---|
| 1 | workflows/04_university_report.md:215-216 | "plus an honest fit check against the student's `profile` / `preferences`." | L (J) | Medium | Orders a personal verdict in §3 with no rule to label it as opinion or show the evidence. Produced rows 22–24. | Replace "honest fit check" with "the student's facts beside what the university says it wants, labelled 'Our read'". | new |
| 2 | workflows/04_university_report.md:219-222 | "Stanford → founders/builders, MIT → makers… name it, then say honestly whether the student *is* that person" | L (G, J) | Medium | The "archetypes" are stereotypes from AI memory with no source required, followed by an order to judge the student against them. Quick mode keeps the archetype "in full" (report-writer.md:59-60). | Archetype must quote the university's own words (admissions page) with a source; drop "say honestly whether". | new |
| 3 | workflows/04_university_report.md:246-251 | "Say plainly where they match and where there's a visible gap — this is admissibility signal, not filler." | L (J) | Medium | Asks for a gap verdict on the student's activities, with nothing measuring it. Produced row 28. | Show the comparison as a two-column table (theirs / admitted profile) with no verdict words. | new |
| 4 | workflows/04_university_report.md:208-211, 229-230 | "admission likelihood… the grade margin → Reach/Match/Safety" | L (J) | Medium | Reach/Match/Safety goes into the Snapshot as a plain value. No rule says the report must explain it is a rule-made label or how it was set. Produced rows 17–18. | Require a one-line footnote: "Reach/Match/Safety is our label, from <rule>; not the university's." | new |
| 5 | workflows/04_university_report.md:72-74 | "research the backup entry route… and its rough entry bar" | L (G) | Medium | "Rough" invites an approximate grade bar from memory, not the pathway provider's published one. | "its published entry bar, or `Not found — <why>`". | new |
| 6 | workflows/04_university_report.md:309-312, 347-351 | "a short honest synthesis… 2–4 reasons to choose… column 2 = the honest read… fold each hesitation into its topic's verdict" | L (J, A) | Medium | §14 is a verdict section by design ("reasons to choose", "verdict"). "Inform, don't sell" stops hype but not opinion, and nothing marks it as judgment. | Rename to "Trade-offs at a glance": each row is a fact from an earlier section plus its source section, no verdict words. | new |
| 7 | workflows/04_university_report.md:189-194, 270-273 | "This is the 'is this energy right for me' section" | L (G) | Medium | Culture, student life and city are built from Reddit/forum snippets, but no rule says to name a claim as one student's view. The sample does this well once (see "solid") but nothing requires it. | Rule: every forum/video claim says whose view it is ("one student on The Student Room says…") and links it. | new |
| 8 | workflows/04_university_report.md:284-285 | "otherwise treat as reassuring background, not a decision driver." | L (Y) | Medium | "Reassuring" asks for comforting tone, not information. | "otherwise state the facts briefly". | new |
| 9 | workflows/04_university_report.md:306-308 | "traditions, notable alumni… fun/quirky facts — the colour that makes it real." | L (Y) | Medium | "Colour" and "fun" invite filler sentences without sources. | "Each quirk is one sourced fact; no commentary." | new |
| 10 | workflows/04_university_report.md:362-363 | "Collect every 'confirm this yourself' task in the section it actually belongs to" | L (A) | Medium | Builds a to-do list for the student into the report. Produced row 30. | Turn into a factual "Not yet confirmed" list (what is unknown and where it is published), no imperatives. | new |
| 11 | workflows/04_university_report.md:242-244, 428-429 | "as leads for the student to dig further… write `\"Not found — <why>\"`" | L (A, Y) | Medium | The "why" is free text with no limits, so advice and AI notes ("free search cannot read Reddit") ride along inside it. Produced rows 27 and 29. | Limit `<why>` to what was searched and where; ban tool names and advice in it; check in `check_report.py`. | new |
| 12 | workflows/04_university_report.md:324-333 | "**Second person.** Write *to* the student ('**you**')… It's their guide, not an internal report." | L (A) | Medium | The writing rules cover skimming, bolding and tables, but never ban advice ("you should", "take it"), hedges ("likely", "realistic") or filler. Writing "to you" plus "guide" pushes towards coaching. | Add one writing rule: "Information, not advice: no imperatives, hedges or verdict words outside a labelled 'Our read' line." | new |
| 13 | tools/check_report.py:24-26, 431-452 | "voice       written TO the student — second person, no student name, no third person" | L | Medium | The only voice check looks for he/she/his. Nothing scans for advice, hedge or filler words, so all of rows 16–31 pass the gate. | Add a `facts` check listing "should / consider / take it / realistic / likely / typically / honest read / verdict". | new |
| 14 | .claude/agents/report-writer.md:66-69; .claude/commands/quick-report.md:2 | "reframe… to a general 'reasons to consider / reasons to hesitate' for the kind of student this place suits" | L (J, A) | Medium | The quick report is sold as "Facts-only", but its §14 is still a judgment about who the place suits, with no student to base it on. | Quick mode: drop §14 or make it a factual trade-off table (see row 6). | new |
| 15 | .claude/agents/report-writer.md:70-72 | "All other 10 sections (`identity_mission`… `culture_vibe`, `student_life`, `city_and_belonging`… `unique_facts`) are already pure facts" | L | Medium | Wrong: four of those are forum texture or "colour" (rows 7, 9). Telling the helper they are "pure facts" removes any caution there. | Say which sections are forum-sourced and must attribute claims. | new |
| 16 | sample PDF p1, Snapshot "Est. net cost after aid" | "~RM 22,000/yr your share (~RM 87,000 over four years) if MIT sets your parents' contribution at zero, as its income bands suggest" | G | High | A worked-out "your share" figure built on a guess ("as its income bands suggest"). This breaks the current rule at 04:288-293 ("no single 'your-share' figure"). It is the cost line a customer reads first. | Rebuild the sample under the current Costs rule: MIT's own income-band examples plus a calculator link. | new (SP1 covers master-list cells only) |
| 17 | sample PDF p1, Snapshot "Admission likelihood" | "Reach — 4.6% admitted overall, 2.0% of international applicants" | J | High | "Reach" is our rule-made label, but it sits in a fact table with no note saying it is a judgment or how it was made. The percentages are facts; the label is not. | Add "(our label; see Getting in)" and the one-line rule. | new |
| 18 | sample PDF p7, §4 "Your read" | "Predicted A*A*A*A* puts you well above any academic bar MIT could set… it cannot be your only US application." | J | High | Says "well above" a bar that, in the next breath, it admits does not exist, and ends with advice (A). Same problem as the "Well above" cell, now in report prose. | State the facts (no cutoff; 2.0% international admit rate) and drop the "well above" and "only application" lines. | new (related to R17/SP1, which cover the CSV cell only) |
| 19 | sample PDF p1-3, Key terms | "so check what's left for you" · "check its register to confirm" · "musalla — typically with washing facilities" · "ABET… eases professional registration back home" | A | High | Glossary lines (written by `tools/apply_glossary.py`) mix advice (2), a hedge (1, G) and an unsourced claim (1). They print in every report that uses the term. | Rewrite those four glossary entries as plain definitions. | new |
| 20 | sample PDF p4, §2 Identity | "this is the identity on your list that most closely describes what you already do. The open question is not whether MIT suits you." | J | High | A fit verdict inside the section meant to be pure identity facts. It says the fit question is settled. | Remove; §2 states what MIT says about itself. | new |
| 21 | sample PDF p4, §2 Identity | "so you can open the first mechanical engineering subjects tonight and find out whether you like them." | A | High | Advice tacked onto a fact (OpenCourseWare exists, it is free). | Keep the fact and link; drop "so you can… tonight". | new |
| 22 | sample PDF p5-6, §3 table "Honest read on your fit" | "Strong." · "Your strongest card in spirit, your weakest in evidence" · "Neutral. Bring one thing you do purely because you enjoy it." | J | High | 8 rows of unscored verdicts (Strong / Neutral / Untested / Under-evidenced) with no scale or method, plus advice in at least one ("Bring one thing…", A). | Column = "On your file" (facts the student gave), with no verdict words. | new |
| 23 | sample PDF p6, "What it means for you" column | "The best fit on your list for your top priority" · "Close to how you already like to work; the workload is the price" | J | High | 4 rows of judgment. "Best fit on your list" compares against other universities with no shown basis. "Collaborative, intense, builder-minded" (Culture row) has no source (G). | Replace with facts (aid policy, class size) or cite a source for each claim. | new |
| 24 | sample PDF p6, §3 "The verdict" | "MIT is being asked to believe in a builder whose building is currently invisible." | J | High | A literary verdict paragraph (also Y). Nothing in it is a checkable fact. | Delete the "verdict" paragraph. | new |
| 25 | sample PDF p7-8, §4 "Where you stand" column | "Clears comfortably" · "decide now who writes the second letter" · "Ask your college early" · "Take it if offered" | A | High | 6 cells: 4 orders, plus "7.5 is the score that also serves MIT" (A) and "The most useful optional item for you" (J). | Column becomes "Your status" with facts only (e.g. "Not yet sat", "Predicted grades on file"). | new |
| 26 | sample PDF p9, §4 Early vs Regular | "Early Action is only realistic if your essays and letters are already under way. Regular Action… costs you nothing in the odds." | J | High | A timing judgment and an odds claim. MIT's sourced line ("no strategic benefit") is fine; the "only realistic" and "costs you nothing" lines are ours, not marked as ours. | Keep MIT's quote and both dates; drop the two judgment sentences. | new |
| 27 | sample PDF p9, "Who actually gets in" | "For unedited voices, read the MIT Admissions blogs… Not found — free search cannot read Reddit, so no thread is quoted here." | Y | High | An AI note about its own tools ("free search cannot read Reddit") reaches the customer, plus a "read the blogs" order (A). | Put the links in Sources; write gaps as "Not found — no public decision threads checked". | new |
| 28 | sample PDF p9, "Your profile against that" | "one real project with its code and a demo is the most direct way to turn the tinkering into evidence before January." | A | High | Coaching advice plus a gap verdict ("The visible gap is everything else", J). | State the Maker Portfolio facts (quoted, sourced); no "most direct way". | new |
| 29 | sample PDF p9, "If you are not admitted" | "Not found — MIT's transfer pages read here give no admit numbers, so treat transfer as a long shot. The realistic plan is a different finalist first" | Y | High | "read here" is an AI note-to-self. "treat as a long shot" is a guess from missing data (G), and "the realistic plan" is advice (A). | "Not found — MIT publishes no transfer admit numbers." Stop there. | new |
| 30 | sample PDF p9, "Confirm these yourself before you submit" | "Re-check the Early Action… dates" · "Ask MIT Admissions how to handle the second teacher letter" | A | High | A 3-item to-do list, made by the rule in row 10. | "Not yet confirmed: MIT's deadline page prints no year." (fact, no order). | new |
| 31 | sample PDF p4, p10 | "It is also a place that gives its work away." · "surprise people who expect a pure engineering school… not a token." | Y | High | Filler framing with no information. Minor, but it is in the public sample. | Cut to the fact (2,500+ free courses; eight HASS subjects required). | new |

## What is already solid
- **No inventing facts.** `report-writer.md:102-105`: "Never fabricate a fact… write `Not found —
  <why>`… rather than… guessing". Empty sections fail the build on purpose
  (`04_university_report.md:428-429`).
- **Every source is labelled.** §15 and `report-writer.md:88-91` require Official/Aggregator plus
  the cycle year, and `check_report.py` fails a report whose sources are too few official pages.
  Hard facts must come from official pages, never aggregators.
- **Costs rule is now factual.** `04_university_report.md:288-293` bans a single "your-share"
  figure and bans working one out from income typed in chat. The `net_cost` template
  (`04:399`) labels its source and "approx". The sample predates this (row 16); the rule itself
  is right.
- **Quick mode removes the personal judgments.** `report-writer.md:55-65` drops Admission
  likelihood, priorities, the fit check and the achievements comparison when there is no student.
- **"Inform, don't sell"** (`04:312`, `04:351`) stops sales hype in §14, though not opinion.
- **The sample shows the right way to report hearsay once.** p9: "That is a student's claim, not
  MIT's." Every forum-sourced claim should work like this (row 7).

## Counts
G: 1 · A: 5 · Y: 3 · J: 7 · L: 15 · Total: 31 (High 16, Medium 15, Low 0)

*Counted by the first label in each row. Rows 1–15 (instructions) are all L; the label in brackets
is what they let through.*
