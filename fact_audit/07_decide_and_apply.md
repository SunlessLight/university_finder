# 07. Decide and apply (Stage 5 recommendation + deadline calendar; Stage 8 "how to apply" guides)

*Fact audit, 2026-10-28. Written for Evan (no technical background). Labels: G guess, A advice,
Y yapping, J unlabelled judgment, L loophole. Severity: High reaches a student, Medium could,
Low internal.*

## What this part makes

Three things a student gets at the end. (1) **`recommendation.md`** (Stage 5): a hand-written note
that ranks the student's finalist universities and suggests how to apply (which ones, how many,
in what order). Nothing builds or checks it; Claude writes it freely, following
`workflows/05_decide_and_apply.md`. (2) **`calendar.md`** (Stage 5): one table of every date
across the finalists, built by the script `tools/build_calendar.py` from the deadline column of the
student's list plus the dates each university report saved. (3) **The "how to apply" guide**
(Stage 8), one per region (US, UK…): Claude researches official pages into a data file (JSON, a
structured text file like a form with labelled boxes), then `tools/build_application_prep.py` turns
it into a document with fixed headings, checklists, a glossary ("Key terms", from
`tools/apply_glossary.py`) and a date table, and `tools/apply_prep_to_pdf.py` turns that into a PDF.
The writing style comes from the `application-guide` skill (a "skill" is a saved instruction sheet
Claude loads before a task). A public, anonymised US sample guide sits in the sales pack.

## Who sees it

- **Student:** `recommendation.md`, `calendar.md`, `application_prep/<region>.md` + `.pdf`.
- **The public:** `business/sales/sample_pack/sample_apply-guide_US.pdf` (28 pages; pages 1-10 and
  23-28 read for this audit).
- **Helpers/Claude only:** the workflow files, the skill, the command files.

Stage 5 is advice by design (a "recommendation" and a "strategy"). The question is whether that
advice is labelled as advice, and whether the facts around it (deadlines, documents, fees) each
carry a source and a date. Short answer: the guide's facts are well sourced and dated at the back,
but advice is mixed into the same sentences as the facts with no label, and the calendar shows
every date as a bare fact with no source, no date checked, and no way to mark an estimate.

## Findings

| # | Where (file:line) | Quote (≤20 words) | Label | Severity | Why it matters | Suggested fix (one line) | Already in backlog? |
|---|---|---|---|---|---|---|---|
| 1 | sample_apply-guide_US.pdf p2 (from skill .claude/skills/application-guide/SKILL.md:88-90) | "Applying is still worth it because, at your family's income, the aid makes most of them close to free" | A | High | A value judgment ("worth it") sits in a box headed "One honest caveat (your call)", right next to facts. It reads as the service's verdict, not as a labelled opinion. | Keep the odds fact (published admit rate + source); drop "worth it", or move it to a box clearly titled "Our opinion". | new |
| 2 | sample_apply-guide_US.pdf p2 (Start here #2), p3 (section 1, twice) | "Recommendation: spend the early card on Princeton SCEA or MIT Early Action." / "Use it only if that university is your clear first choice." | A | High | 3 advice lines in the strategy section, in bold, mixed into the rules about early rounds. "Recommendation:" is a word, not a label saying who recommends it or why. | State the rules (which rounds stack, which bind); put any pick in a separate, labelled "Our suggestion" line. | new |
| 3 | sample_apply-guide_US.pdf p4 (section 3 heading and body) | "Aid: always ask for it" / "Still request it. You need it" / "Yayasan Khazanah matters most for these four." | A | High | 3 lines of coaching in a section heading and body. "You need it" is a judgment about the student's money; "matters most" is an opinion with no source. | Heading states the fact ("Aid: need-blind vs need-aware"); cut the imperatives and the "matters most" line. | new |
| 4 | sample_apply-guide_US.pdf p2 (Start here #2, #3); rule at SKILL.md:41-43 | "Choose your one early application by 25 Oct 2026." / "Ask your parents this week" | G | High | 25 Oct is not a university date; it is a deadline the AI made up, shown in the same bold style as real published dates (1 Nov). The skill says "Put real dates in it" but never says to mark self-set dates. | Mark self-set dates as "suggested, not a university deadline", or only list published dates in Start here. | new |
| 5 | sample_apply-guide_US.pdf p7 (cost-cycle box, rendered by tools/build_application_prep.py:510) | "Recent rises have been close to 4% a year … Budget about 5% above what you see here" | G | High | An estimate of next year's price and a budgeting tip, from two examples. The student may plan their family's money on a 5% figure nobody published. | State the published figure and its year, and "next year's figure publishes around <month>"; drop the forecast. | new |
| 6 | workflows/08_application_prep.md:159-161; .claude/skills/application-guide/SKILL.md:47-50 | "when the entry-year figures publish, and roughly how much they rise" / "roughly how fast they rise" | L | Medium | The instruction itself asks Claude for a forecast, so finding 5 will repeat in every region's guide. | Change to "which year the figures are from and when the next ones publish". No rise estimate. | new |
| 7 | sample_apply-guide_US.pdf p3 (English-test paragraph) | "You need IELTS Academic for Singapore, Australia and the UK anyway, so one sitting settles this whole question." | G | High | A blanket claim plus advice. The project's own rule (08_application_prep.md:125-128) says UCL, Imperial and KCL accept an English-subject grade (e.g. SPM 1119) instead, so "need IELTS for the UK" is not true as a blanket rule. | Remove; English rules stay per university, in each university's own section. | new (related to R21) |
| 8 | sample_apply-guide_US.pdf p25 (Key terms); now-fixed text at tools/apply_glossary.py:153-156 | "IELTS — … Your English-medium A-Levels waive it at many universities, but not all." | G | High | The public sample still carries the old glossary line that R21 found wrong. The glossary was corrected, but the sample PDF was not rebuilt. SP1 lists seven wrong cells and does not include this one. | Add this line to SP1; rebuild the sample guide from the corrected glossary. | new (same cause as SP1 / R21) |
| 9 | tools/apply_glossary.py:33, :69 (shown on sample p23-24) | "Avoid it if you need to compare aid offers." / "so check what's left for you." | A | High | Advice built into the dictionary, so it lands in every guide that mentions ED or demonstrated need, whatever the student's situation. 2 entries. | Definitions say what a term means and stop: "binding; you withdraw other applications if admitted." | new |
| 10 | tools/apply_glossary.py:90, :207 (CSS line shown on sample p24) | "Opens 1 October." / "A Malaysian foundation offering competitive scholarships to study at top global universities." | G | High | Facts written from memory into a shared dictionary, with no source and no year. If the College Board moves the date, every guide is wrong and nothing flags it. 2 entries. | Move dated facts out of the glossary into the researched, sourced sections; keep definitions date-free. | new |
| 11 | tools/build_application_prep.py:427-429 (sample p1, p8: "1. Princeton University — Reach") | `heading += f" — {likelihood}"` | J | High | Every university heading carries Reach/Match/Safety, which is a label the scoring rules made, not a fact. The guide never explains it, and the glossary has no Reach/Match/Safety entry, so the student can't tell how it was decided. | Add a glossary entry saying it is our label and how it is made, or drop it from headings. | new |
| 12 | sample_apply-guide_US.pdf p2 | "all 9 are extreme Reaches, with single-digit admit rates." | G | High | No admit-rate source appears in the Sources list (p25-28), so "single-digit" is unsourced. "Extreme" is a judgment with no rule behind it. | Cite each admit rate (official Common Data Set or class profile, with year), or remove the figure. | new |
| 13 | sample_apply-guide_US.pdf p4 | "On the income in your file (a lower-income band) you sit below every published zero-parent-contribution line" | J | High | Tells the student they qualify for free tuition everywhere. The workflow says the record holds no family income by design (08_application_prep.md:134-135), so either the rule was broken or this is a guess. Either way it reads as fact. | Show the universities' published income bands only; let the family place themselves. | new |
| 14 | tools/build_application_prep.py:503 and :122 (INTRO); workflows/08_application_prep.md:146 | `f"## {region_title} application strategy"` / "read the strategy" / "write the region-level overview (the cross-cutting strategy)" | L | High | The template gives every guide a section called "strategy", and the INTRO tells the student to read it. Nothing says the strategy must be labelled as advice or kept apart from facts. That is where findings 1-3 come from. | Rename to "How the rules interact" (facts only); if advice stays, put it in its own section titled "Our suggestions". | new |
| 15 | .claude/skills/application-guide/SKILL.md:13-17, :86-87; workflows/08_application_prep.md:31-33 | "an admissions coach who streamlines…" / "Warm, concise, second person… Lead with the action, then the reason." | L | Medium | A coach character invites coaching ("always ask", "do this now"). The skill has rules for layout but none saying "facts only, no advice". | Replace the persona with "state what each university requires; no recommendations unless labelled". | new |
| 16 | .claude/skills/application-guide/SKILL.md:88-90 | "If every option is an extreme Reach, say so up front … never let a tidy checklist imply… a safe bet." | L | Medium | Asks for a prominent judgment ("extreme Reach") in the student file with no source or method. That produced finding 1's box. | Ask for the published admit rate with its source, and the label's meaning, not a verdict. | new |
| 17 | sample_apply-guide_US.pdf p8, p2 | "That is the 2025-26 figure; I could not find a 2026-27 one." / "Anything I could not confirm is marked" | Y | Medium | The AI talks in the first person ("I") in a product sold under a business name. The gap flag itself is good. Medium, not High: cosmetic, no false fact. | Neutral wording: "2026-27 fee not published as of 12 Oct 2026; 2025-26 shown." | new |
| 18 | sample_apply-guide_US.pdf p5, p6 (Visa section) | "Read it now so the costs and the lead time do not surprise you." / "do not leave it until July." | A | High | Coaching and a self-set timing tip inside the visa facts. "July" is not an official date. | Keep the official facts (365 days, 30 days, fees); drop the tips. | new |
| 19 | sample_apply-guide_US.pdf p3, p4, p6 | "November scores usually arrive in time" / "a campus job, and possibly a loan" / "Interviews are generally required" | G | High | 3 hedged statements in a guide sold as facts. "Usually" and "possibly" mean the official page wasn't pinned down, or was paraphrased. | Quote the official wording, with its source, or mark "not stated on <page>, <date>". | new |
| 20 | workflows/08_application_prep.md:122-123 | "your answers suggest you qualify; the university decides, usually from a school letter" | G | Medium | A template sentence with a hedge built in ("usually"), copied into every guide where the student meets the years rule. | Drop "usually from a school letter" unless that university's page says so. | new |
| 21 | .claude/skills/application-guide/SKILL.md:74-76; workflows/08_application_prep.md:70-72 | "Stanford expects ~USD 5,000/yr from the student, Yale USD 3,700, while Princeton abolished its contribution outright." | G | Medium | Undated facts in instructions, which Claude may copy without re-reading. They are already out of date: the sample (p8) found Princeton's own pages disagree. | Mark them "example from the July 2026 run, do not reuse", or strip the figures. | new |
| 22 | tools/build_application_prep.py:343-344 (validate) | `if not data.get("sources"): sys.exit(...)` | L | Medium | One source of any kind passes, including "Aggregator". Nothing checks that each fact has a source, and no check program exists for guides (as `check_report.py` does for reports) to catch "usually", "you should", "I could not". | Add a `check_apply_prep.py` with the same hedge/advice/first-person word lists as the other checks. | new |
| 23 | tools/build_calendar.py:226-229; tools/build_application_prep.py:465-468; tools/build_report.py:335-339 | `"| Date | What | University | Action |"` | L | High | Calendar rows show a date with no source and no "checked on" date. The saved report dates keep only date/label/action and drop anything else, so the source can't travel even if a helper writes one. The student can't tell an official date from one copied off a stale row. | Add `source` + `as_of` to `dated_items`, keep them when saving, and show them as a column. | new (related to R9) |
| 24 | tools/build_calendar.py:72, :229; tools/shortlist_schema.py:485 | `re.search(r"(\d{4})-(\d{2})-(\d{2})", str(text))` | L | High | **The calendar answer:** it keeps the first date in a cell and throws away the rest of the text. "2027-01-15 (estimated from last cycle)" shows as a plain 2027-01-15, so an estimate looks like a published fact. An "opens X, closes Y" cell puts X under "Application deadline". Today there's no way to mark an estimated date. | Show the original text next to the date when it has more than the date; refuse words like "est./approx./expected". | new |
| 25 | workflows/05_decide_and_apply.md:41; tools/build_report.py:90 | "scholarship deadlines, test dates, visa lead times" | L | Medium | A visa lead time is relative ("apply up to 365 days before"). Putting it in a dated calendar means the AI works out a date itself. Nothing says to mark it as worked out, and build_report.py:90 says dates only "where the page gives one". The two rules clash. | Lead times go in the undated list as text ("up to 365 days before start"), never as a computed date. | new |
| 26 | tools/build_calendar.py:73, :77-79 | `system = r.get("How to apply") or "the application portal"` | L | Medium | Fallback text: a row with no portal or no deadline still gets "Application deadline … Submit via the application portal", which reads like an instruction. When the cell is blank, nothing says "not found". | When blank, print "Deadline not found on the list. Check <official page>"; no default portal text. | new |
| 27 | workflows/05_decide_and_apply.md:22-23, :67; .claude/commands/decide.md:16-17, :30 | "Ranked recommendation — the finalists in recommended order, each with 2-3 sentences of why" | A | Medium | Stage 5 is advice by design, and that's fine. But no rule says the file must open by saying "this is our opinion, ranked by <method>". "Don't over-promise" is the only guard. (Student files not opened, so I can't confirm if it reached one.) | Require a first line: "Our recommendation (opinion), ranked by your stated priorities and the score; the decision is yours." | new |
| 28 | workflows/05_decide_and_apply.md:19, :53-58 | "restate for each recommended university: the portal, the steps, and the documents needed" | L | Medium | `recommendation.md` is written by hand, with no data file, no builder and no check. Step 4 copies facts (portals, documents) into it with no source or date rule, so they can drift from the sourced apply guide. | Point to the apply guide instead of restating; or require source + date per restated fact. | new |
| 29 | workflows/05_decide_and_apply.md:27-30 | "a maximum of 5 choices, and you cannot apply to both Oxford and Cambridge … (and often extra essays/tests)" | G | Medium | System rules written from memory with no source or date, which Claude repeats into the student's strategy. "Often" is a hedge. "Help choose the 5" is advice. | Cite UCAS's own page with a checked-on date; let the guide carry the rule. | new |
| 30 | workflows/05_decide_and_apply.md:24-25; .claude/commands/decide.md:17-18 | "confirm the set spans Reach/Match/Safety so the student isn't betting on long-shots alone" | J | Medium | The recommendation repeats Reach/Match/Safety, but nothing asks it to say these are rule-made labels or how they are made. | Require one line defining the labels whenever they appear. | new |
| 31 | workflows/08_application_prep.md:225-227 | "Common App supplement prompts publish ~1 Aug" | G | Low | Hedged, undated fact in an instruction. Internal, but it could be copied into a guide. | Cite Common App's page with a year, or drop the date. | new |
| 32 | tools/apply_glossary.py:1297-1298 (sample p23) | "New to these? Here's what the shorthand in this guide means — tap a linked term" | Y | Medium | Chatty template line in every guide. Medium: harmless, no false fact. | "Definitions of the terms used in this guide." | new |

## What is already solid

- **Official sources with labelled, dated stamps.** The Stage 8 rules (08_application_prep.md:216-222,
  SKILL.md:91-95) ask for official pages and stamps that say what they mean ("Fall-2027 cycle" vs
  "2026-27 figures"). The sample's Sources list (p25-28) follows this for every fact, and says when
  each page was read ("Read on 12 October 2026").
- **Exchange rate stated once, with a date** (`build_application_prep.py:367-372`), so every "~RM"
  figure can be checked.
- **Gaps and conflicts are flagged, not averaged** (SKILL.md:77-80): the sample marks Princeton's
  disagreeing pages and the unlisted US visa fee with ⚠ instead of picking one.
- **The English-waiver rule bans "waived for you"** and asks for each university's own rule
  (08_application_prep.md:115-128). The sample lists each university's waiver separately (p3).
- **Report dates are taken only "where the page gives one"** (`build_report.py:90-91`); anything
  else lands in a separate "Undated / to confirm" list, and the calendar refuses to silently lose
  dates (`build_calendar.py:277-288`).
- **The builder stops on half-finished guides** (`build_application_prep.py:307-344`: deadlines,
  checklist, aid and sources are required; "write 'Not found — <why>'"), and `apply_prep_to_pdf.py`
  only changes the look, never the words.

## Counts
G: 11 · A: 6 · Y: 2 · J: 3 · L: 10 · Total: 32 (High 17, Medium 14, Low 1)
