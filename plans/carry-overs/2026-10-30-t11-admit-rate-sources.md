# Carry-over: T11 admit-rate sources (2026-10-30)

**Goal:** task T11 in [plans/list_pdf_plan.md](../list_pdf_plan.md): one "Admit rate source" line in each of the 10 `workflows/countries/*.md` files, so row-fillers (T5) and T7 know where to read `Admit rate`.
**Where it stands:** research ~80% done, **no files written**. Findings below exist only in this note.

## Done this session
- Researched 7 of 10 countries and opened an official source for each (checked 2026-10-29/30). Results, ready to turn into lines:
  - **USA, yes:** each university's own Common Data Set, item C1, gives first-time, first-year applicants and admits (all applicants). It has an optional In-State/Out-of-State split; take an international figure only where the university gives one. No central host. Opened: Towson CDS 2025-26 section C.
  - **UK, some universities:**
    - Oxford "Current Undergraduate admissions statistics" (`ox.ac.uk/about/the-university/facts-and-figures/admissions-statistics/undergraduate/current`): links "Nationality and Domicile" and "Applications by course" (Tableau) plus the Annual Admissions Statistical Report 2026. Counts applications, offers and admitted.
    - Cambridge "Undergraduate Admissions Statistics 2025 cycle" (published May 2026; index at `undergraduate.study.cam.ac.uk/apply/before/application-statistics`): Table 3.2 gives applications and offers by country, outside the UK only, Malaysia included. "Offer" = conditional or unconditional offer of a place.
    - UCAS provider-level end-of-cycle data (2023 entry page): the page text says applications and acceptances, not offers. Acceptance ≠ offer, so don't derive a rate from it.
    - Other UK universities: None published.
  - **Japan, yes, per university:** each university's 入試結果 table, which includes the 私費外国人留学生 (privately funded international) track with 志願者数 (applicants) and 合格者数 (passed/admitted) per faculty. Opened: Nagoya (令和4年度 一覧) and Kitami (2024–2026).
  - **Malaysia, none:** the KPT media statement of 22 May 2026 gives national totals only. Public universities: none per university.
  - **Hong Kong, none for non-JUPAS:** EDB reply of 13 May 2022 (accessinfo.hk "non_jupas_admissions_statistics"): EDB/UGC does not keep non-JUPAS application or offer counts. JUPAS figures are local HKDSE applicants, city-wide totals only.
  - **Taiwan, none:** MOE 113學年度 校務資訊公開項目 list has 外國學生數 (enrolled) and 新生註冊率 (enrolment rate) only, no application or admission counts.
  - **Germany, none:** Marburg's Auswahlgrenzen page publishes cut-off grades, plus applications/places that exclude internationals. No admit rate.
- checked by: pages and PDFs read in this session; nothing written to files.

## Decisions (don't re-ask)
- Evan rejected a chained Firecrawl command (three `firecrawl_search.py` runs in one Bash call). Claude switched to Chrome. Unclear whether Evan objects to Firecrawl itself or only to the chained form; Claude's default is Chrome first, then Firecrawl one query at a time.

## Not done yet
- **Australia:** the publications page says the Department collects applications, offers and acceptances. The 2025 report PDF wouldn't render as text in Chrome. A search snippet said "domestic applications… Table A universities", so it is likely "None published for international applicants", but this is unconfirmed.
- **Singapore:** NUS IGP page returned no text. No official applicant/offer figures found. Expected "None published".
- **China:** no official source opened. Expected "None published".
- Lines not written; T11 "Done when" not run; T11 not ticked in the Progress table; no commit.
- End-of-session steps (build log, STATUS.md Now box, Notion) skipped because no files changed. Do them when T11 lands.

## Next steps
1. Confirm Australia: download the PDF via the Read tool (WebFetch saves it), read its scope page. Then Singapore (NUS/NTU admissions pages) and China (one top university's international admissions page). Free first; Firecrawl single queries if blocked.
2. Add a `## Admit rate source` heading plus one line in each of the 10 files, just before or after "Known-good sources". Pointers only, **no figures**. Format: publication · counts (all/international; admitted/offered) · checked 2026-10-30, or "None published (checked 2026-10-30)".
3. Verify: `grep -c "Admit rate source" workflows/countries/*.md` returns 1 each.
4. Tick T11 in the plan's Progress table, offer the commit (10 country files + plan), then the build log, Now box and Notion.

## Read first
- [plans/list_pdf_plan.md](../list_pdf_plan.md): Decisions item 9 (cell shape), the T11 "Done when" and the T11 prompt.
- `workflows/countries/usa.md` "Known-good sources" for the house style of these files.

## Gotchas
- WebFetch helpers return PDFs as raw bytes. Read the saved PDF yourself with the Read tool (`pages`); that worked every time.
- Plain fetch gets 403 from `ox.ac.uk`, and its old `…/undergraduate-students/current/overall-numbers` URL is now a 404. Use the `/about/the-university/…/undergraduate/current` page above.
- `ucas.com` works in Chrome; `get_page_text` can fail once on a redirect, so re-check the tab and retry.
- The education.gov.au "2025" link on the publications page points at the 2022–2024 resource.
