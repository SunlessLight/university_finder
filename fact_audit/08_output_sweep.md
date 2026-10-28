# 08. Output sweep: how much guessing/advice/chatter is actually in what students received

*Fact audit, 2026-10-28. Written for Evan (no technical background). Labels: G guess, A advice,
Y yapping, J unlabelled judgment, L loophole. Severity: High reaches a student, Medium could,
Low internal.*

## What this part makes
This part is a measurement, not a tool. A small counting script (`.tmp/fact_audit/sweep.py`)
read every file the pipeline already produced for students. The pipeline is the chain of steps that
turns a student's form into a university list and reports. The script counted how often
"guess words" (likely, usually, ~, confirm…), "advice words" (recommend, you should…) and "chatter
words" (I found, note:, great…) appear. Think of it like a spell-checker that only counts typos: it says
*how many* and *in which column or file type*, never *which student*. No student text was printed or
copied. The two public files (the sample pack spreadsheet and the demo website's data file) were also
scanned, and only those are quoted.

**Scope scanned:** 27 student folders, 493 spreadsheet rows (`master_list.csv`), 27 `research_notes.md`,
42 university reports (15 students), 1 application guide, 1 `recommendation.md`, 1 `calendar.md`, plus
27 `glossary.csv` (the Glossary tab of the student's sheet, added because it is student-facing).

**Caveats (read before the numbers):**
- Counts are word matches, not confirmed problems. Some hits are fine in context (e.g. "~" before a
  currency conversion is the house style for approximate MYR figures; "shortlisted candidates may be
  interviewed" is a fact). They show *where to look*, not a verdict on each cell.
- Words that look like hedges but usually are not were counted separately as "neutral" and are **not**
  findings: "confirmed", "confirmation" (as in Confirmation of Enrolment), "recommended" (usually
  quoting the university), "considered/consideration" (as in "automatically considered", "equal
  consideration"), "Not published" (an honest label meaning the university publishes no number).
- "GREAT" matched once in the sample pack: it is the GREAT Scholarships name, not chatter.

**Final regexes (case-insensitive, Python `re`):**

| Group | Name | Regex |
|---|---|---|
| G | likely | `\blikely\b` |
| G | probably | `\bprobabl[ye]\b` |
| G | usually | `\busually\b` |
| G | typically | `\btypical(?:ly)?\b` |
| G | generally/often | `\b(?:generally\|often)\b` |
| G | ~number | `~\s*(?:[A-Z]{2,3}\s*\|[$£€¥]\s*)?\d` |
| G | approx/around/roughly/about + number | `\b(?:approx(?:imately)?\.?\|around\|roughly\|about)\s*(?:[A-Z]{2,3}\s*\|[$£€¥]\s*)?\d` |
| G | should be | `\bshould be\b` |
| G | may/might/could be | `\b(?:may\|might\|could) be\b` |
| G | confirm (open) | `\b(?:confirm\|confirms\|confirming\|unconfirmed)\b` |
| G | verify/check | `\b(?:re-?)?(?:verify\|check)\b` |
| G | TBC/TBA | `\b(?:to be confirmed\|TBC\|TBA\|to be announced)\b` |
| G | estimate | `\bestimat\w*` |
| G | expect | `\bexpect(?:ed\|s)?\b` |
| A | you/students should | `\b(?:you\|students?\|applicants?) should\b` |
| A | recommend (not "recommended") | `\b(?:we \|i )?recommend(?:s\|ing\|ation\|ations)?\b` |
| A | suggest | `\bsuggest\w*` |
| A | consider (not -ed/-ation) | `\bconsider(?:ing)?\b` |
| A | best to / make sure / don't forget / aim to / try to / avoid / good idea | `\bbest to\b`, `\bmake sure\b`, `\bdon[’']?t forget\b`, `\baim to\b`, `\btry to\b`, `\bavoid\b`, `\bgood idea\b` |
| A | apply/start early | `\b(?:apply\|start\|submit\|book\|begin) (?:early\|now\|as soon as)\b` |
| A | worth applying/considering | `\bworth (?:applying\|it\|a look\|considering)\b` |
| Y | I + verb | `\bI (?:couldn[’']?t\|could not\|found\|was unable\|have\|think\|believe\|checked\|searched)\b\|\bI[’'](?:ve\|m)\b` |
| Y | let me / note: / worth noting | `\blet me\b`, `\bnote:`, `\bworth not(?:ing\|e)\b` |
| Y | great / unfortunately / interestingly / keep in mind | `\bgreat\b(?!\s+britain)`, `\bunfortunately\b`, `\binterestingly\b`, `\bkeep in mind\b` |
| Y | it seems/appears | `\bit seems\b\|\bappears? to\b\|\bseems to\b` |
| NV | Not verified / Not found | `\bnot verified\b\|\bunverified\b`, `\bnot found\b` |

"Word hedge" below means any G pattern **except** `~number` and `estimate` (those two are often the
house style for approximate money).

## Who sees it
- **Student:** `master_list.csv` (their Google Sheet), the Glossary tab (`glossary.csv`), university
  reports (`reports/*.md` and PDFs), the application guide, `recommendation.md`, `calendar.md`.
- **Possibly the student:** `research_notes.md` is described as a "companion file" to the list
  (`workflows/00_overview.md:217`), but whether it is actually sent was not confirmed, so it is rated
  Medium.
- **The public:** `business/sales/sample_pack/sample_master_list.csv`, `sample_glossary.csv`, and the
  demo website's `prototype/data.js`.

## Findings

Student counts are "number of students with at least one hit". "Cells" means spreadsheet cells
containing at least one match.

| # | Where (file:line) | Quote (≤20 words) | Label | Severity | Why it matters | Suggested fix (one line) | Already in backlog? |
|---|---|---|---|---|---|---|---|
| 1 | data/students/*/master_list.csv › `Recognised in Malaysia?` | pattern: confirm / verify / check / generally / likely | G | High | 173 cells, 23 students (confirm 77, verify/check 71, generally/often 36, likely 8). 76 of them sit on rows stamped "Official page". This column gates regulated careers, so a hedge here is the costliest kind. | Write only what MQA/BEM registers show, or the fixed sentinel "Not checked yet". | new |
| 2 | data/students/*/master_list.csv › `English req` | pattern: confirm / typically / verify / likely | G | High | 158 cells, 16 students (confirm 75, typically 46, verify/check 35, likely 32, may/might be 8). 24 on Official-page rows. | Require the exact published score or a sentinel; ban "typically/likely" in this column. | new |
| 3 | data/students/*/master_list.csv › `Key deadline` | pattern: check / ~date / confirm / estimate | G | High | 117 cells, 13 students (verify/check 82, ~ 36, confirm 14, estimate 6). 51 Official-page rows carry a word hedge in this column. | Exact published date, or "Not published yet (last cycle: <date>)". | new |
| 4 | data/students/*/master_list.csv › `Work rights after graduating` | pattern: ~ / likely / confirm | G | High | 117 cells, 20 students (~ 88, likely 31, confirm 15, usually 4). 34 Official-page cells word-hedged. | State the visa rule from the government page; no "likely". | new |
| 5 | data/students/*/master_list.csv › `Money to show (visa)` | pattern: ~ before amount / confirm / check / typically | G | High | 240 cells, 26 students. Mostly `~` (233), largely MYR conversions; 14 Official-page cells carry a word hedge (confirm 14, check 13, typically 8). | Keep "~" only on converted figures; show the official amount in its own currency first. | new |
| 6 | data/students/*/master_list.csv › `Notes` | pattern: ~ / confirm / likely / check / TBC | G | High | 142 cells, 25 students (~ 80, confirm 25, likely 17, check 15, typically 12, TBC 10, estimate 9). | Notes may only hold sourced facts; route open questions to research_notes.md. | new |
| 7 | data/students/*/master_list.csv › `Entry requirements` | pattern: ~ / typically / expect | G | High | 92 cells, 15 students (~ 56, typically 20, expect 12, check 9). 10 Official-page cells word-hedged. | Quote the published requirement; no "typically". | new |
| 8 | data/students/*/master_list.csv › `How to get the scholarship` | pattern: check / ~ / confirm / may be | G | High | 82 cells, 22 students (verify/check 32, ~ 25, confirm 16, typically 4). | Steps from the scholarship page only; no "check whether". | new |
| 9 | data/students/*/master_list.csv › `Scholarship coverage` | pattern: ~ / typically / confirm / likely | G | High | 73 cells, 22 students (~ 52, typically 16, around/approx 7, confirm 4, likely 3). | Published amount or "Amount not published". | new |
| 10 | data/students/*/master_list.csv › `Scholarship competitiveness` | pattern: ~ before a rate or count | G | High | 61 cells, 20 students (~ 60). Approximate award counts or rates with no source shown. | Show a stat only with its source year; else "Not published". | new |
| 11 | data/students/*/master_list.csv › `Annual tuition` | pattern: ~ / check / estimate | G | High | 33 cells, 15 students (~ 26, verify/check 9, estimate 8, TBC 1). A hard-fact column per CLAUDE.md. | Published fee with year; never "~" in the native-currency fee. | new |
| 12 | data/students/*/master_list.csv › `Total tuition` | pattern: ~ / estimate / typically | G | High | 23 cells, 11 students (~ 24, estimate 7, typically 2, likely 1). | Compute from Annual tuition x Duration in the tool, not by hand. | new |
| 13 | data/students/*/master_list.csv › `Est. living/yr` | pattern: ~ / estimate | G | High | 17 cells, 10 students (~ 11, estimate 11). Column is labelled "Est." so this is partly by design. | Cite whose estimate (university or visa office) in the cell. | new |
| 14 | data/students/*/master_list.csv › `Intake` | pattern: check / ~ / confirm | G | High | 29 cells, 6 students (verify/check 19, ~ 6, confirm 3). | Published intake months only. | new |
| 15 | data/students/*/master_list.csv › `Student life` | pattern: ~ before a number | G | High | 42 cells, 20 students (~ 39). Mostly distances/times; low harm but unsourced. | Accept, or drop numbers without a source. | new |
| 16 | data/students/*/master_list.csv › `Scholarship & portal` | pattern: ~ / check / confirm | G | High | 23 cells, 11 students (~ 17, check 6, confirm 2). | Same rule as row 8. | new |
| 17 | data/students/*/master_list.csv › `Subject rank` | pattern: ~ before rank / confirm | G | High | 20 cells, 10 students (~ 14, confirm 4). A rank is a published number, so "~top 40-50" means it was not looked up. | Exact rank + table + year, or "Not ranked in <table>". | new |
| 18 | data/students/*/master_list.csv › `Admission likelihood` | pattern: ~ before a percentage | G | High | 15 cells, 7 students (~ 14, likely 1). Approximate admit rates inside the Reach/Match/Safety label. | Show the published admit rate with year, or none. | new |
| 19 | data/students/*/master_list.csv › `Overall rank`, `Course at a glance`, `Student grades`, `Warnings`, `How to apply` | pattern: check / ~ / expect / confirm | G | High | Small columns together: Overall rank 11 cells, Course at a glance 9, Student grades 9 (expect 5), Warnings 6, How to apply 2. | Same sentinel rule as above. | new |
| 20 | data/students/*/master_list.csv › all columns | pattern: recommend / consider / suggest / apply early / avoid | A | High | 22 cells across 9 students: How to get the scholarship 7, Entry requirements 4, Notes 3, Key deadline 3, Scholarship & portal 2, others 1 each. Low count, but advice should be zero in the list. | Add an advice-word check to check_master_list.py. | new |
| 21 | data/students/*/master_list.csv › all columns | pattern: note: / great / (one) course-at-a-glance chatter | Y | High | 11 cells across 7 students (note: 7, great 3, of which the 2 in `Scholarship & portal` may be the GREAT Scholarships name). Notes-to-self in a student's sheet. | Ban "note:" and first-person words in cells via the checker. | new |
| 22 | data/students/*/master_list.csv › `Info source` (and `Warnings`) | pattern: "Not verified" | G | High | 213 of 493 rows (43%) are "Not verified", across 12 students; Warnings says "Not verified" in 264 cells (19 students). Honestly labelled, but the unverified fact cells still reach the student. | Blank or dim the fact cells of Not-verified rows in the sent copy. | new |
| 23 | data/students/*/master_list.csv › `Notes`, `Subject rank`, `Student grades`, `Recognised in Malaysia?` | pattern: "Not verified" / "Not found" inside a fact cell | G | High | 19 cells (Notes 10, Student grades 5, Subject rank 3, Recognised 1). Honest, but free-text, not the schema's fixed sentinel. | Use one standard sentinel wording everywhere. | new |
| 24 | data/students/*/master_list.csv › rows with `Info source` = Official page | pattern: any word hedge in a fact column | L | High | 162 of 280 "Official page" rows (58%) have a word hedge (confirm, check, likely, typically…) in at least one of 13 fact columns; 260 of 280 counting "~"/estimate. The "Official page" stamp is being given to rows that still contain guesses, and the checker lets it through. | check_master_list.py: fail an Official-page row whose fact cells contain hedge words. | new |
| 25 | data/students/*/reports/*.md | pattern: ~ / around / confirm / check / expect / typically / likely | G | High | 1,827 matches in all 42 reports (15 students): ~ 731, around/approx 280, confirm 211, verify/check 179, expect 132, estimate 69, typically 68, generally/often 44, likely 37, usually 35. | Report JSON: facts need a source; hedge words fail check_report.py. | new |
| 26 | data/students/*/reports/*.md | pattern: recommend / you should / suggest / apply early / worth applying | A | High | 193 matches in all 42 reports (15 students): recommend 58, you should 34, suggest 29, apply/start early 22, consider 21, worth applying 11, make sure 8, avoid 8. | Remove advice phrasing from report templates and the report-writer brief. | new |
| 27 | data/students/*/reports/*.md | pattern: great / I + verb / note: / let me | Y | High | 43 matches in 24 reports (10 students): great 22, I + verb 8, note: 8, it seems 2, let me 2. First-person notes-to-self reached students. | Add a first-person/"note:" check to check_report.py. | new |
| 28 | data/students/*/reports/*.md | pattern: "Not found" / "Not verified" | G | High | 40 matches in 21 reports (11 students): Not found 37, Not verified 3. | Use the fixed sentinel and list gaps in one "Not yet confirmed" box. | new |
| 29 | data/students/*/application_prep/*.md | pattern: around/approx + number / check / typically / confirm | G | High | 102 matches in the 1 guide: around/approx 51, verify/check 12, typically 10, confirm 9, expect 6, estimate 5. | Same source rule as reports. | new |
| 30 | data/students/*/application_prep/*.md | pattern: recommend / apply early | A | High | 32 matches in the 1 guide: recommend 25, apply/start early 4. This is a how-to guide, so some instruction is expected, but "we recommend" is opinion. | Rephrase as the university's requirement, not our recommendation. | new |
| 31 | data/students/*/application_prep/*.md | pattern: I + verb | Y | High | 2 first-person matches in the 1 guide. | Same Y check as row 27. | new |
| 32 | data/students/*/recommendation.md | pattern: ~ / confirm / should be | G | High | 13 matches in the 1 file: ~ 6, confirm 5, should be 1, check 1. | Facts only, sourced. | new |
| 33 | data/students/*/recommendation.md | pattern: recommend | A | High | 2 matches in the 1 file. The file is by design a recommendation, so this is expected; flagged so Evan can decide whether it is labelled as our judgment. | Label it "Our recommendation (a judgment)" at the top. | new |
| 34 | data/students/*/recommendation.md | pattern: note: | Y | High | 1 match in the 1 file. | Same Y check. | new |
| 35 | data/students/*/calendar.md | pattern: expect / confirm / check | G | High | 15 matches in the 1 file: expect 13 (probably "decision expected"), confirm 1, check 1; plus 1 "apply early" (A). | Show expected dates as "last year's date" with the year. | new |
| 36 | data/students/*/glossary.csv (Glossary tab) | pattern: check / confirm / generally / usually / typically | G | High | 115 matches in all 27 glossaries: verify/check 42, confirm 27, generally/often 17, usually 14, typically 8. Term definitions mixing fact with "check…". | Keep definitions to what the term means; no "check/confirm" steps. | new |
| 37 | data/students/*/glossary.csv (Glossary tab) | pattern: avoid / apply early | A | High | 24 matches in 8 students' glossaries: apply/start early 17 (mostly in Early Decision/Early Action definitions, which is terminology), avoid 7 (real advice, see row 44). | Drop "Avoid it if…" from build_glossary_sheet.py's term text. | new |
| 38 | data/students/*/research_notes.md | pattern: ~ / check / confirm / estimate / typically / likely | G | Medium | 2,625 matches in all 27 files: ~ 839, verify/check 437, confirm 425, estimate 272, typically 134, around/approx 126, likely 116, expect 103. | Fine as internal working notes; do not send unless cleaned. | new |
| 39 | data/students/*/research_notes.md | pattern: recommend / suggest / you should | A | Medium | 107 matches in 25 files: recommend 36, suggest 27, you should 15, avoid 12, consider 11. | Same as row 38. | new |
| 40 | data/students/*/research_notes.md | pattern: it seems / note: / I + verb / great | Y | Medium | 96 matches in 25 files: it seems/appears 29, note: 27, I + verb 21, great 15, worth noting 4. Clearly written as AI notes-to-self. | Confirm research_notes.md is never sent; if it is, clean it first. | new |
| 41 | data/students/*/research_notes.md | pattern: "Not verified" / "Not found" | G | Medium | 74 matches in 22 files (Not verified 53, Not found 21). | Same as row 38. | new |
| 42 | business/sales/sample_pack/sample_master_list.csv › `Recognised in Malaysia?`, `Key deadline`, `Subject rank` | "Listed on MQA's eSISRAF register, most likely under its BSc row." · "MQA: verify" · "confirm exact 2027 date" · "QS Mech Eng ~top 40-50" | G | High | 62 G matches across 15 rows: Recognised in Malaysia? 9 cells (of 15), Key deadline 6, Subject rank 5, Money to show 5, Scholarship coverage 4, Annual tuition 4. This is the public sample. | Clean these cells before the sample goes out again. | SP1 |
| 43 | business/sales/sample_pack/sample_master_list.csv › `Info source` | "2027-02-28 (approx; 2026 cycle closed 28 Feb - confirm exact 2027 date)" | L | High | All 15 rows are stamped "Official page", yet 10 of 15 have a word hedge in a fact column (15 of 15 counting "~"). Shows the public the same gap as row 24. | Same checker rule as row 24, run on the sample pack. | SP1 |
| 44 | business/sales/sample_pack/sample_glossary.csv › `What it means` (ED row) | "Avoid it if you need to compare aid offers." | A | High | 4 A matches in 49 terms (1 real "avoid", 3 "apply early" inside ED/EA/SCEA definitions). | Replace with the fact: "binding, so you cannot compare aid offers". | SP1 |
| 45 | business/sales/sample_pack/sample_glossary.csv › `What it means` (MQA row) | "check its register to confirm your degree counts back home" | G | High | 6 G matches (check 2, usually 2, confirm 1, typically 1). | State what MQA does; put the "check" step in the apply guide. | SP1 |
| 46 | prototype/data.js:1090 | "make sure the rest of your list carries the weight." | A | High | Advice in the demo website's decision screen copy; 2 A matches in the file. | Rephrase as a fact about the list's Reach/Match/Safety balance. | new |
| 47 | prototype/data.js:228, :289 | "most likely under its BSc row" · "QS Mech Eng ~top 40-50" | G | High | 68 G matches; the data file copies the sample CSV, so every sample-pack hedge (rows 42-43) is also on the public demo site. | Regenerate data.js from the cleaned sample CSV. | SP1 |

## What is already solid
- **Every row is labelled.** All 493 student rows have an `Info source` value (280 "Official page",
  213 "Not verified", 0 blank). Nothing reaches a student without a verification label.
- **"Not published" is used instead of guessing.** 83 `Grades vs entry bar` cells and 50 `Key deadline`
  cells say "Not published" rather than inventing a number (counted as neutral, not a finding).
- **Several columns came out clean** of every G/A/Y/NV pattern: `List status`, `Desirability`, `Tier`,
  `University`, `Course`, `Country`, `City`, `Duration (yrs)`, `Approx total (MYR)`, `Course URL`, `Grades vs
  entry bar`. `How to apply` had only 2 hits and `Warnings` only 6 (outside its "Not verified" label).
- **Chatter in the spreadsheet is rare:** 11 cells out of about 17,000 (493 rows x 35 columns), so the
  cell-length budgets and Stage 3 rules mostly work. The chatter problem is in reports and research notes.
- **calendar.md has no chatter** (Y = 0) and almost no advice (1 hit).
- **The demo site's own wording about verification is honest**: `prototype/data.js:977` says "Any row we
  cannot check stays marked \"Not verified\" until it is." (counted under NV, not a finding).

## Counts
G: 32 · A: 8 · Y: 5 · J: 0 · L: 2 · Total: 47 (High 43, Medium 4, Low 0)
