# Taiwan — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> a Taiwan row. See `03_discover_longlist.md`, "Per-destination query playbook", for how this
> fits into Step 1 and Step 3.
>
> **Added 2026-09-23** — Taiwan became the 9th supported destination when a student (`haotowin`)
> named National Taiwan University by hand. **This file has never survived a real Stage 3 pass.**
> Everything below is desk research, not run experience: treat the traps as leads to confirm, and
> **write back what the first pass actually learns** — that is how `hong-kong.md` got useful.

**Taiwan** → English-taught + IEET accreditation + the MOE scholarship:
```
<course> English-taught bachelor Taiwan university international students
<university> international degree student admission <course>
<university> <course> IEET accredited programme
MOE Taiwan Scholarship <field> undergraduate
```

## Known-good sources (locations, never values)

> Places to **fetch**, never facts to quote — a fee, deadline or cutoff comes off the page every
> time (guardrail 2). `free` = plain `WebFetch` works; `blocked` = the page exists but 403s a
> plain fetch, so go straight to `firecrawl_search.py`; `untested` = found via search, not yet
> fetched — **stamp it the first time you use it.** **Cross-country sources — rankings, Malaysian
> sponsors, MQA + the professional bodies, English tests — are in `workflows/sources.md`**, not
> repeated per country.

| Answers | URL | Fetch |
|---|---|---|
| Official government study portal (programme search, visa, scholarships) | `https://www.studyintaiwan.org/` | untested |
| NTU international undergraduate admissions (deadlines, steps, dept limit) | `https://admissions.ntu.edu.tw/apply/degree-students/international-students/` | free ✅ 2026-09-23 |
| NTU tuition + fees for internationals | `https://isss.ntu.edu.tw/finances/tuition-fees/` | untested |
| NTU work-after-graduation / post-study visa | `https://isss.ntu.edu.tw/work/internship-work-after-graduation/` | untested |
| **MQA↔HEEACT Joint Statement of Confidence** (the Malaysian recognition gate) | `https://www.mqa.gov.my/new/soc_heeact_msia.cfm` | free ✅ 2026-09-23 |
| **HEEACT Taiwan Quality Institution Directory** — is this institution actually covered? | `https://tqid.heeact.edu.tw/` | untested |
| **IEET** — is this *programme* Washington Accord accredited? | `https://www.ieet.org.tw/` | untested |
| IEA qualification checker, Chinese Taipei entry | `https://www.internationalengineeringalliance.org/for-engineers/qualification-checker/element/206/Form?country=chinese-taipei` | untested |
| MOE Taiwan Scholarship — official guidelines | `https://taiwanscholarship.moe.gov.tw/web/pages.aspx?p=7` | untested |
| **TECO Malaysia** — the Malaysia-specific scholarship round + deadlines | `https://www.roc-taiwan.org/my_en/post/12502.html` | untested |
| Work-permit points system for foreign graduates (EZ Work Taiwan, official) | `https://ezworktaiwan.wda.gov.tw/en/cp.aspx?n=8E87472D9CB255FF&s=72F47A2275C6E3AF` | untested |
| NTUST (Taiwan Tech) admissions | `https://admissions.ntust.edu.tw/` | untested |
| Taipei Tech (NTUT) tuition | `https://oia.ntut.edu.tw/p/412-1032-13790.php?Lang=en` | untested |

## Traps (desk research 2026-09-23 — none yet confirmed by a real pass)

> **1. Fees are quoted PER SEMESTER, and the degree is 4 years.** This is the big one, and it
> under-reports cost by a factor of ~8 if you take the headline number as an annual figure.
> A Taiwanese bachelor's is **4 years** (not the UK's 3), and public universities quote tuition
> **per semester, two semesters a year**. NTU's international undergraduate tuition sits around
> **TWD 50,460–62,100 per semester** depending on subject area (engineering sits at the top of
> that band, humanities at the bottom) → roughly **TWD 101k–124k/year** → **~MYR 13k–16k/year**
> → **~MYR 52k–64k for the whole degree, tuition only.** Always fetch the per-semester number
> off the university's own fees page, multiply by 2, then by 4, and put the **total** in the
> row (guardrail 4: total cost in MYR, never annual tuition).

> **2. Taiwan will look impossibly cheap next to the UK/US — because it is.** Tuition an order of
> magnitude below a UK international fee is the correct answer, not a parsing bug. Don't "sanity
> check" it away. Do make sure **living costs are actually included** in the row's total, since
> they are a much larger share of the Taiwan total than of a UK one; and note the visa financial
> proof of about **NT$500,000** in a bank statement, which is a real cash-flow requirement even
> though it isn't a cost.

> **3. Washington Accord recognition is per-PROGRAMME, not per-country.** Taiwan's **IEET**
> (Institute of Engineering Education Taiwan) has been a **full Washington Accord signatory since
> 20 June 2007**, and is also a signatory of the Sydney and Seoul Accords. That is genuinely
> strong for a Malaysian engineering student — it is the same mechanism that carries a degree
> toward **BEM** registration back home. **But the Accord only covers programmes IEET has
> actually accredited.** A Taiwanese engineering degree from an unaccredited programme carries
> nothing. Check the specific programme against IEET's accredited list before writing anything
> into `recognition_route`, and never infer it from the university's reputation.

> **4. Malaysian recognition runs through HEEACT, and it is institution-level.** MQA and Taiwan's
> **HEEACT** signed a **Joint Statement of Confidence on 2012-07-20** (renewed 2014 and 2017)
> covering **bachelor-level programmes accredited by each agency** — confirmed on MQA's own page
> 2026-09-23. Roughly **58 public and 99 private** Taiwanese institutions are covered. Two things
> that page says explicitly and that matter: it does **not** list the institutions itself (query
> the **HEEACT TQID directory** instead), and it preserves the right of any Malaysian body to
> "impose additional academic and non-academic requirements." So **MQA confidence is not the same
> as BEM registration** — for a regulated profession you still need trap 3 as well. Both gates,
> separately.

> **5. There is no UCAS. You apply per university, and each application costs money.** Every
> institution runs its own online admissions system. NTU lets an applicant pick **up to 5
> departments** in one cycle, but charges **NTD 2,000 (or USD 80) per department** for a
> first-time applicant — so a full 5-department application is **NTD 10,000**, a real cost that
> no UK row has an equivalent for. Worth surfacing at Stage 5 when the student picks how wide to
> apply.

> **6. Deadlines land in November, long before A-Level results.** NTU's 2027 September entry ran
> a **1st round closing 2026-11-05** (results 2027-01-14) and a **2nd round closing 2027-01-19**
> (results 2027-04-08) — confirmed on NTU's own page 2026-09-23. For a Malaysian A-Level student
> sitting A2 in Oct/Nov with results in January, **the first round closes before results exist**,
> so it is a forecast-grades application by construction, and the second round is tight against a
> January results date. Check each university's rounds individually; do not assume NTU's calendar
> generalises.

> **7. English-taught coverage is real but patchy — verify per programme.** NTU, NTHU, NCKU, NCCU
> and NTUST all advertise English-taught degree options, and **engineering / CS / science are the
> best-covered fields** (humanities much less so). But many departments still teach in Mandarin,
> and a programme listed on an aggregator as "English-taught" is not evidence. Fetch the
> department page. Typical bar where a programme is English-taught: **TOEFL 79+ / IELTS 6.0+**,
> plus a high-school diploma around 75%+ — but these are aggregator-level figures, so confirm
> them per university rather than quoting these.

> **8. Post-study work: a points system, and a possible 2026 policy change to verify.** The
> settled mechanism is a **6-month job-seeking extension after graduation, extendable once to 12
> months total**, and a **points test scored out of 200 where 70 points passes** — clearing it
> lets a graduate bypass the general foreign-worker salary floor of about **NT$47,971/month**.
> Points come from degree level, salary, Chinese and other language ability, work experience and
> "growth experience". **Separately, an aggregator (104.com.tw) reports a 2026 policy giving a
> 2-year open work period with no work permit.** That would be a significant improvement and it
> is plausible, but it is an aggregator claim — **confirm it on EZ Work Taiwan or the Ministry of
> Labor before it goes in a row or a report.**

> **9. Scholarships have a Malaysia-specific round — and it is early.** The **MOE Taiwan
> Scholarship** pays tuition and fees up to **NTD 40,000/semester** plus a **NTD 15,000/month**
> undergraduate stipend, which against trap 1's fee levels can cover most of a degree. For
> Malaysians it is administered by the **Education Division, TECO Malaysia**, and the 2026 cycle
> ran **online applications 1 Feb → 30 Apr**, with hard-copy documents posted within a week of
> submitting online. Assume a similar February–April window and **check TECO Malaysia's own
> announcement for the live year** — this is a separate deadline from the university application
> in trap 6, and missing it is the common failure.

> **10. Naming: "Taiwan" and "Chinese Taipei" are the same place.** Taiwan competes and accredits
> under **"Chinese Taipei"** in several international bodies, the Washington Accord among them. A
> source page or a form answer may use either. `COUNTRY_NORMALIZE` in `tools/ingest_form_csv.py`
> maps both to `Taiwan`. Don't treat an IEA page headed "Chinese Taipei" as a different country.

> **11. Currency.** Taiwan uses the **New Taiwan dollar (TWD)**, added to `FX_TO_MYR` in
> `tools/shortlist_schema.py` on 2026-09-23 at **0.128 MYR** (not part of the 2026-09-05 ECB set,
> so `FX_AS_OF` was deliberately left alone). Watch for sources writing **NT$** or **NTD** — same
> currency, and the row's `cost_currency` must be `TWD` or the MYR total comes out blank.

## Learned during the run itself

_Nothing yet — this file has not been through a Stage 3 pass. First run: fill this section, stamp
the `untested` rows in the source table, and correct any trap above that desk research got wrong._
