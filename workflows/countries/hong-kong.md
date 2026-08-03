# Hong Kong — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> a Hong Kong row. Split out of `03_discover_longlist.md` on 2026-07-30 — see that file's
> "Per-destination query playbook" section for how this fits into Step 1 and Step 3.

**Hong Kong** → English-taught + **non-local** admissions:
```
<course> bachelor Hong Kong university non-local student admissions
HKU OR CUHK OR HKUST OR PolyU OR CityU OR HKBU OR Lingnan <course> international admissions
<university> non-local student tuition fee 2026-27
<university> <course> medium of instruction language requirement
<university> entrance scholarship non-local students international qualifications
IANG Hong Kong post-study work visa immd.gov.hk
```

## Traps (learned 2026-08-03, Teoh — first real HK pass)

> **Set `currency: "HKD"`** (in `FX_TO_MYR` at 0.60) or the MYR total silently blanks.

> **Local vs non-local is THE fee trap.** Every UGC-funded university's fee page shows the
> local/HKSAR-resident rate (~HKD 42,100/yr, government-subsidised) *beside* the non-local
> rate, which is 4-6x higher. A Malaysian student is **non-local**. Quote the non-local rate
> only — this is Hong Kong's version of the Australian domestic-fee trap.

> **HKU splits its non-local fee STEM vs non-STEM (2026-27 cohort).** HKD **224,000**/yr for
> non-STEM faculties (Arts, Social Sciences, Business, Law, Architecture, Education) and HKD
> **249,000**/yr "inclusive of STEM Fee" for Dentistry/Engineering/Medicine/Science/Computing.
> A humanities BA is the **224,000** figure. No other HK university had this split in 2026-27.
> Non-local rates seen this pass: HKUST 215,000 · CUHK 214,000 · HKBU 190,000 · Lingnan 175,000.

> **JUPAS is for local HKDSE students only.** A Malaysian A-Level applicant applies **direct to
> each university's own international / non-JUPAS portal** — separate application, fee and
> deadline per university. `jupas.edu.hk` pages surface constantly in search and are useful for
> programme *descriptions*, but their entry bars are HKDSE-only and must never land in
> `Entry requirements` for a non-local applicant. Find the international-qualifications page.

> **IANG is 24 months, not 36.** `immd.gov.hk` (checked 2026-08-03) grants an initial stay of
> **24 months**, no job offer needed if applied within 6 months of graduation, free to change
> employer; renewals run 2+2+3 yrs, and 7 continuous years qualifies for permanent residency.
> Aggregator blogs (studyin.hk among them) were pushing a "36-month extension 2026" headline
> that the official page does not support. Use the 24-month figure.

> **Medium of instruction is a real cut, not a formality.** Several HK humanities degrees are
> Chinese-medium or bilingual and assume academic Chinese: PolyU's BA (Hons) in Chinese History
> and Culture is taught in "Chinese (Putonghua) & English" and expects graduates to write modern
> Chinese; CityU's BA Chinese and History states applicants "are expected to be proficient in
> Chinese and should provide recognized qualifications" to prove it. Both were **dropped from
> the roster** for an English-medium A-Level student. HKBU's BA (Hons) in Humanities is
> deliberately bilingual (English + Chinese tuition) — keep it, but say so in `notes`.
> Ethnic-Chinese Malaysian ≠ academic Chinese literacy; check the page, don't assume.

> **`admission.cuhk.edu.hk` refused `WebFetch` (ECONNREFUSED) on 2026-08-03** while its pages
> ranked fine in `WebSearch`. That is a "free search blocked" case — escalate to
> `firecrawl_search.py` for CUHK fee/entry pages rather than quoting a search snippet.
> Programme URLs follow `admission.cuhk.edu.hk/programme/<code>/` (`histn` History, `philn`
> Philosophy).

> **Degrees are 4 years** (HK moved to the 4-year norm in 2012) — so a HK BA is one year longer
> than a UK one, and the total-cost comparison must use 4.

> **Non-local quota rose 40% → 50% of local intake (Sept 2025).** Places are widening, not
> tightening; don't score HK admission as tighter than it is on quota grounds.

> **One September intake.** Main international rounds close roughly early Nov to Jan, and the
> earlier round is usually the one considered for entrance scholarships (HKUST's separate
> scholarship deadline was 8 Jan 2026). Deadlines are per-university — verify each.

> **Living costs:** hall HKD 17,000-38,000/yr (285 residential days, excludes summer), off-campus
> HKD 30,000-50,000/yr and often compulsory after year 1 (HKUST says so explicitly), general
> living up to HKD 50,000-60,000/yr. A defensible all-in benchmark is HKD 60,000-90,000/yr.

> **Recognition:** no professional-body gate for humanities. Malaysian recognition runs through
> MQA equivalency (Malaysian Qualifications Register) *after* graduation, and matters for
> JPA/public-service appointment, not for private employers.

## Learned during the run itself (same pass, after the 9 row-fillers came back)

> **Rankings: use QS 2027 for overall, QS 2025/2026 for subject — and don't let an agent inflate
> them.** Two row-fillers on the *same* university returned different overall ranks (CUHK #18 vs
> #32) because they cited different editions, and one produced an unsupported "QS 2026 History #6
> world" for CUHK. **QS World University Rankings 2027** (released June 2026, verified against each
> university's own release): HKU **#11**, CUHK **#18**, HKUST **#33**, PolyU #50, CityU #52, HKBU
> **#216**, EdUHK #406, Lingnan **#581**. By-subject 2027 tables are **not** out — subject ranks
> must stay on the 2025/2026 editions. CUHK's own communications put its **Arts & Humanities broad
> area at #44** and **Philosophy at #28** (QS 2025); **History is not in its published top-50**, so
> any single-digit History figure is wrong. Normalise ranks across the batch before syncing —
> `check_master_list.py` does not catch two rows disagreeing about one university.

> **CUHK's Cultural Studies BA is JUPAS-only.** It is absent from the official programme list at
> `admission.cuhk.edu.hk/programmes/list/`, which CUHK's own International Students Admissions
> Scheme guide names as the authoritative list of programmes open to non-local applicants — while
> the department's own page shows four-route boilerplate on every programme, which reads as if it
> were open. **The catalogue is the tie-breaker, not the department page.** The international-open
> sibling in the same department is **BA in Public Humanities** — use that for a "Humanities &
> Culture" student. Check the catalogue before dispatching, not after.

> **`admission.cuhk.edu.hk` and `join.hkust.edu.hk` both refuse `WebFetch`** (connection/cert
> error) while ranking normally in `WebSearch`. HKUST has usable substitutes carrying the same
> facts (`shss.hkust.edu.hk`, `publication.join.ust.hk`, `registry.hkust.edu.hk`); CUHK does not.
> **Do not work around this with `curl -k`** — that disables TLS certificate verification, and an
> agent did exactly that this pass. The approved escalation is `firecrawl_search.py`.

> **Firecrawl was out of credits during this pass** (`Payment Required: Insufficient credits`), so
> the one approved fallback was unavailable and agents improvised (`curl -k`, the `r.jina.ai`
> reader proxy). Check the credit balance *before* dispatching a Hong Kong batch — this is the
> destination where free fetch fails most. `topuniversities.com` also 403s `WebFetch` consistently,
> so QS numbers must come from each university's own rankings page.

> **A-Level English Literature can satisfy the English requirement outright.** Lingnan's GCE-English
> table accepts an A-Level English grade, so no separate IELTS/TOEFL sitting is needed there; HKU's
> Faculty of Arts bar is the same shape but was not confirmed for English *Literature* specifically.
> Check per university before assuming a test is required.

> **HKBU's BA (Hons) Humanities is genuinely bilingual**, not English-taught with Chinese options:
> HKBU admissions assess applicants with no Chinese qualification **case-by-case, not guaranteed**.
> Say so in `notes` rather than scoring it as a plain English-medium degree.

> **Glossary:** `IANG`, `JUPAS` and `non-JUPAS` were added to `tools/apply_glossary.py` on
> 2026-08-03 — before that, HK rows shipped acronyms the Glossary tab couldn't define.
