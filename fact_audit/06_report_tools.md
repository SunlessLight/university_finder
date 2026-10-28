# 06. University report tools

*Fact audit, 2026-10-28. Written for Evan (no technical background). Labels: G guess, A advice,
Y yapping, J unlabelled judgment, L loophole. Severity: High reaches a student, Medium could,
Low internal.*

## What this part makes
These seven scripts are the "printing press" for the university report. A helper (an AI agent)
researches one university and writes its findings into a JSON file (a structured text file, like a
form with labelled boxes). `build_report.py` pours that into a fixed 15-section document (Markdown,
a plain-text format with simple headings). `report_to_pdf.py` turns it into the PDF the student gets,
adding a "Key terms" glossary on the way. `check_report.py` is the spell-checker-style gate that reads
the finished document and flags problems. `apply_report_fx.py` swaps old ringgit figures for new ones
when exchange rates (FX, the currency conversion rate) change. `compare_universities.py` prints a
side-by-side table of several universities from the student's master list. `match_finalists.py` and
`flip_finalists.py` are bookkeeping: they find the right spreadsheet row and mark it "Finalist".
Key point: the scripts add very little wording of their own. Most of the risk is in what they *allow
through* (the helper's free text) and what the checker *does not look for*.

## Who sees it
- **Student:** the report PDF (`data/students/<slug>/reports/<name>.pdf`), including the section
  headings, the Snapshot table, the Sources list and the glossary inserted by `report_to_pdf.py`.
- **The public:** the sample pack's MIT report PDF (`business/sales/sample_pack/`) is built with
  these same tools, so every report-level finding below also applies to it.
- **Student, via Evan:** the comparison table from `compare_universities.py` (Stage 4 and Stage 5
  workflows say Evan walks the student through it).
- **Evan / helpers only:** `check_report.py`, `apply_report_fx.py`, `match_finalists.py`,
  `flip_finalists.py` output.

## Findings

| # | Where (file:line) | Quote (≤20 words) | Label | Severity | Why it matters | Suggested fix (one line) | Already in backlog? |
|---|---|---|---|---|---|---|---|
| 1 | tools/build_report.py:124, 125 | "Who it's for — the archetype & your fit" / "Getting in — requirements, who gets in & your fit" | J | High | Two fixed headings in every report ask the writer for a "fit" verdict, and the student reads it as a section of facts. | Rename to "Who it's for" / "Getting in — requirements and who gets in"; move any fit view into one labelled "Our assessment" box. | new |
| 2 | tools/build_report.py:135 | "Why here / why hesitate" | L | High | A fixed heading that invites persuasion and advice ("why you should go") in every report's last section. | Rename to "Summary of facts" (or "Strengths and drawbacks on the record") and require each point to cite a section. | new |
| 3 | tools/build_report.py:128, 134 | "Culture & vibe" / "Unique facts & quirks" | L | Medium | "Vibe" and "quirks" invite impressions and chatty colour rather than checkable facts; nothing downstream asks for sources per section. | Rename to "Campus culture (from official and student-union sources)" / "Notable facts". | new |
| 4 | tools/build_report.py:211, 228 (and 247) | "\| Field \| Value \|" ... ("Admission likelihood", data.get("admission_likelihood")) | J | High | Reach/Match/Safety is a rule-made judgment but sits in a "Field / Value" table next to the university's name and rank, so it reads as a fact. | Label the row "Admission likelihood (our estimate from your grades vs the published bar)". | new |
| 5 | tools/build_report.py:248, 63; tools/check_report.py:67 | ("Est. net cost after aid (MYR)", data.get("net_cost")) / "~RM Xk-Yk/yr (uni's examples, 20XX; approx)" | L | Medium | Ringgit figures in the Snapshot and the Costs prose are free text; neither the builder nor the checker requires the rate used or its date (FX_AS_OF) next to them. | Have build_report.py print one fixed line under Costs: "Converted at RM x per <cur>, rate of <FX_AS_OF>"; checker fails if missing. | new |
| 6 | tools/build_report.py:291-311; tools/report_to_pdf.py:65-67 | "@bottom-center { content: \"Created by: Evan Yeoh\" ..." (no date anywhere) | L | High | The report and its PDF never print the date they were made, so fees and deadlines in a printed report cannot be seen to go stale. | Add "Prepared on <date>" under the title in render_report() and in the PDF footer. | new (close to R9) |
| 7 | tools/build_report.py:270-273, 282; tools/check_report.py:372-373, 386 | "_Sources ... Official unless tagged otherwise._" / `if authority and authority != default_auth:` | L | Medium | A source with a blank authority gets no tag, so the lead note silently labels it "Official"; the checker then inherits the same default, so its "source has no authority" warning (line 419) can never fire on a new report. | Tag blank-authority sources "Unlabelled" in render_sources() and fail the check on them. | new |
| 8 | tools/build_report.py:213 | `if not value: continue` | L | Low | A missing Snapshot field just vanishes from the student's table instead of saying "Not found"; only check_report.py notices, and only if it is run. | Print "Not found" for an empty Snapshot field instead of dropping the row. | new |
| 9 | tools/build_report.py:276 | `title = s.get("title") or s.get("url") or "source"` | L | Low | A source entry with no title and no link prints as the bare word "source", which looks like a citation but points nowhere. | Refuse to build when a source has neither title nor URL. | new |
| 10 | tools/check_report.py:21-28, 67 | "CHECKS = [\"structure\", \"snapshot\", \"notfound\", \"sources\", \"voice\", \"tables\"]" | L | High | No check for hedge words ("likely", "usually", "typically", "around", "probably", "should be"), so guessed facts pass the gate. | Add a "hedges" check listing every hedge word with its line. | new |
| 11 | tools/check_report.py:21-28, 67 | "voice       written TO the student — second person, no student name, no third person" | L | High | No check for advice wording ("you should", "we recommend", "consider", "best to", "make sure"); the voice check only cares about pronouns. | Add an "advice" check with a phrase list; fail on any hit. | new |
| 12 | tools/check_report.py:21-28, 67 | "It is deliberately NOT a synthesis judge." (line 12) | L | High | No check for AI notes-to-self or chatty filler ("Note: I couldn't find", "let me", "it's worth noting", "great choice") in a student document. | Add a "chatter" check with a phrase list; fail on any hit. | new |
| 13 | tools/check_report.py:80, 463-466 | "only {rate:.1f} 'you'/'your' per 1,000 chars ... this is written about the student, or about nobody" | L | Medium | The gate *fails* a report that is too impersonal, which pushes writers toward "you"-sentences, the natural home of advice; plain factual prose ("Tuition is GBP 29,000") is penalised. | Drop the minimum-"you" rule, or pair it with the advice check in #11. | new |
| 14 | tools/check_report.py:72, 346-347, 355-356 | "this reads as half-researched, not as honest reporting" / "research it or say what IS known" | L | Medium | More than 8 honest "Not found" gaps fails the report, but a guess never does, so the cheapest way to pass is to fill a gap with a guess. | Keep the count as information only; fail on hedge words (#10) instead of on honest gaps. | new |
| 15 | tools/check_report.py:77, 399-402 | "MIN_OFFICIAL_SHARE = 0.5" / "the rendered report can't say which source backed which fact" | L | Medium | Up to half the sources may be aggregators, and nothing ties a fee, requirement or deadline to an official source; a fee from an aggregator passes. | Require at least one Official source link inside the Costs and Getting-in sections. | new |
| 16 | tools/check_report.py:391-392, 420-421 | "source has no as-of cycle year" | L | Medium | The checker only asks that a year exists; a 2023 fee page passes as easily as a 2026 one. | Fail sources whose year is older than the current application cycle. | new (close to R9) |
| 17 | tools/check_report.py:506-507 | "2 (topic \| honest read), with each hesitation folded into its verdict" | L | Medium | The checker's own fix message tells the writer to give a "verdict" per topic in the student's last section, i.e. write judgments. | Reword to "2 columns (topic \| fact, with its section number)". | new |
| 18 | tools/report_to_pdf.py:155-157; tools/check_report.py:17-19 | "glossary_md = apply_glossary.build_glossary_section(text, title=\"Key terms\")" | L | Medium | The glossary is added only at PDF time, after check_report.py has run on the .md, so its text is never checked before the student reads it. | Run the hedge/advice checks on the glossary text too (or lint the final Markdown). | new |
| 19 | tools/apply_glossary.py:33 (inserted by tools/report_to_pdf.py:155) | "Avoid it if you need to compare aid offers." | A | High | Fixed advice printed in every report PDF (and apply guide) that mentions Early Decision. | Replace with the fact: "If admitted you must enrol, so you cannot compare aid offers." | new (glossary is shared with the apply guides) |
| 20 | tools/apply_glossary.py:982, 1111 (inserted by tools/report_to_pdf.py:155) | "Roughly AUD 650-800 a year for a single student." / "under about A$25,000" | G | High | Money figures written from memory, hedged, undated and unsourced, in a fixed glossary; about 15 more definitions use "usually", "typically", "roughly" or "often" (e.g. lines 579, 589, 669). | Remove figures from the glossary (definitions only) and strip hedge words from the rest. | new |
| 21 | tools/apply_report_fx.py:93-96 | `if str(old_rate) in p["new"] ...: errors.append(...)` | L | Medium | A rate-statement swap is only checked for "old rate gone"; the new rate is not checked against FX_TO_MYR and need not carry a date (the docstring example "(~RM 4.04 per USD)" has none). | Require the new rate to equal FX_TO_MYR[cur] and to include FX_AS_OF. | new |
| 22 | tools/apply_report_fx.py:98-103 | "warnings.append(... ratio {b / a:.3f}, rate ratio ...)" | L | Medium | A converted figure more than 4% off the real rate is only a warning; the tool still writes it into the student's file. | Make an off-ratio figure refuse the fragment, like the other errors. | new |
| 23 | tools/apply_report_fx.py:40 | "from shortlist_schema import FX_TO_MYR" | L | Low | The tool never calls fx_age_warning(), so it will happily re-convert reports with rates past their 90-day freshness limit. | Call fx_age_warning() at start and refuse when stale. | new |
| 24 | tools/compare_universities.py:180 | "verify exact figures in each university report." | A | Medium | Fixed advice line in a table shown to the student (Stage 4 and 5). | Reword as fact: "Approx total is converted at rates of <FX_AS_OF>; exact figures are in each report." | new |
| 25 | tools/compare_universities.py:180 | "Approx total (MYR) is a rough offline conversion for comparison only" | L | Medium | Says "rough" but gives neither the rate nor its date, so the student cannot tell how old the conversion is. | Print FX_AS_OF and the rates used under the table. | new |
| 26 | tools/compare_universities.py:43, 48 | "\"summary\": [\"List status\", \"Desirability\", \"Tier\", \"Admission likelihood\", \"Warnings\"]" | J | High | The 0-100 Desirability score, Tier, Admission likelihood and "Grades vs entry bar" print as plain "Dimension" rows beside fees, with no note that they are rule-made judgments. | Add one line under the table naming which rows are our scores and how they are made. | new |
| 27 | tools/flip_finalists.py:146-196 (172-183) | "a correction is by definition an overwrite of a filled cell" | L | Medium | A report's "corrections" overwrite master-list cells after only a column-name and length check: no hedge/advice check, no source, and Info source is not re-stamped. | Run check_master_list.py's wording checks on each correction and require a source URL with it. | new |

## What is already solid
- `build_report.py` `validate()` (lines 183-203) refuses to build a report with any empty section or
  no sources, and its error tells the writer to say "Not found — <why>" rather than invent.
- `check_report.py` `check_notfound()` (lines 333-357) fails a bare "Not found" with no reason, so a
  gap must always explain itself.
- The exchange rate itself is dated and sourced: `FX_AS_OF = "2026-09-05"` and the ECB source note in
  `tools/shortlist_schema.py:573-598`, plus a 90-day staleness warning. `apply_report_fx.py` refuses a
  fragment if any ringgit figure in the file is unaccounted for.
- `match_finalists.py` never guesses: an ambiguous or missing name returns "ambiguous"/"not_found"
  and leaves the pick to the student (lines 98-124).
- `flip_finalists.py` refuses to bring back a row the student marked Rejected (lines 231-239) and
  refuses corrections to computed columns such as the score (lines 165-170).
- `compare_universities.py` shows a dash for a blank cell (line 116) and never fills in a value.

## Counts
G: 1 · A: 2 · Y: 0 · J: 3 · L: 21 · Total: 27 (High 10, Medium 14, Low 3)
