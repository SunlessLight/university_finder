# Germany — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> a Germany row. See `03_discover_longlist.md`, "Per-destination query playbook", for how this
> fits into Step 1 and Step 3.
>
> **Added 2026-09-23** — Germany became the 10th supported destination alongside Taiwan, both
> requested by the same student (`haotowin`). **This file has never survived a real Stage 3
> pass.** Everything below is desk research, not run experience: treat the traps as leads to
> confirm, and **write back what the first pass actually learns**.

**Germany** → English-taught + tuition-free public + the recognition gap:
```
<course> English-taught bachelor Germany public university
<university> international bachelor admission <course> English
DAAD international programmes <field> bachelor English
<university> <course> ASIIN EUR-ACE accredited
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
| **DAAD programme database** — the authoritative "is it English-taught?" search | `https://www2.daad.de/deutschland/studienangebote/international-programmes/en/` | untested |
| Official government study portal (requirements, visa, costs) | `https://www.study-in-germany.de/en/` | untested |
| **uni-assist** — the shared application service most public unis use | `https://www.uni-assist.de/en/how-to-apply/get-information/bachelor-staatsexamen/` | untested |
| **uni-assist admission checker** — direct entry vs Studienkolleg | `https://www.uni-assist.de/en/tools/check-university-admission/` | untested |
| **anabin** — how Germany classifies a Malaysian/A-Level certificate (H+ / H+-) | `https://anabin.kmk.org/anabin.html` | untested |
| **IEA Washington Accord signatory list** — confirms Germany is absent | `https://www.internationalengineeringalliance.org/accords/washington-accord` | free ✅ 2026-09-23 |
| **BEM** — registration routes incl. the non-Accord assessment path | `https://bem.org.my/Landing/register` | untested |
| ASIIN (German engineering/science accreditor, EUR-ACE label) | `https://www.asiin.de/en/home.html` | untested |
| DAAD Malaysia-specific admission requirements | `https://www.daad-indonesia.org/en/study-research-in-germany/eight-steps-to-germany/admission-requierments-malaysia/` | untested |

## Traps (desk research 2026-09-23 — none yet confirmed by a real pass)

> **1. Germany is NOT a Washington Accord signatory — this is the single biggest finding.**
> Confirmed against the IEA's own signatory list 2026-09-23: the 25 full signatories include
> Malaysia (BEM), the UK (ECUK), Australia (EA), Singapore (IES), Japan (JABEE), Hong Kong
> (HKIE) and **Chinese Taipei (IEET)** — but **Germany appears nowhere**, not as a full signatory
> and not among the 7 provisional ones. Germany's ASIIN holds the European **EUR-ACE** label
> instead, which is a different system. Secondary sources describing ASIIN as a "provisional
> member since 2003" are **out of date or wrong — trust the IEA list.**
>
> **What this means for a Malaysian engineering student:** BEM has been a full Accord signatory
> since 2009 and recognises overseas degrees *through* the Accord. A German engineering degree
> does not arrive with that recognition. It is **not a dead end** — BEM runs a **Graduate
> Assessment Programme (BEM-GAP)** for 4-year engineering degrees accredited in their home
> country but outside the Accord — but it is an extra hurdle, extra time and extra risk that a
> UK or Taiwan degree simply does not carry. **For any `recognition_targets` containing BEM or
> Washington Accord, this belongs in the row's `Warnings`, not buried in `recognition_route`,**
> and it should be said plainly in a Stage 4 report. Verify the current BEM-GAP terms on BEM's
> own site — do not quote this paragraph as the fact.

> **2. "Tuition-free" is true and still not the total cost.** Public universities charge **no
> tuition** to international students at bachelor level, in all 16 states. What they do charge is
> a **semester contribution of roughly €70–€430**, which usually bundles a *Semesterticket* giving
> unlimited regional public transport — genuinely good value, but not zero. The row's total must
> therefore be driven by **living costs**, not tuition, or Germany will show up as a ~RM 0 degree
> and out-rank everything for the wrong reason. Put the real total in (guardrail 4).

> **3. Baden-Württemberg charges non-EU students €1,500 per semester — and it is where the famous
> engineering schools are.** This exception catches exactly the universities a strong engineering
> student would shortlist: **KIT (Karlsruhe), Stuttgart, Heidelberg, Freiburg**. That is
> **€3,000/year, ~€12,000 over a 4-year degree** on top of living costs, against €0 in most other
> states. **Always check which state the university is in before writing "tuition-free."**

> **4. English-taught bachelor's degrees are RARE at German public universities.** This is the
> practical filter that decides whether Germany is viable at all. The overwhelming majority of
> *undergraduate* teaching is in German; English-medium provision is concentrated at **master's**
> level. DAAD's own programme database lists on the order of **116** fully-English bachelor
> programmes nationwide — a real number, but small, and not evenly spread across fields. Search
> the **DAAD database**, not an aggregator listicle. Where English-taught bachelor's do exist in
> volume it is often at **private** universities, which **do charge full tuition** — so an
> English-taught German degree and a tuition-free German degree are frequently *not the same
> option*. Do not let trap 2's "free" halo attach to a private-university row.

> **5. German-taught means a real language bar.** A German-medium programme needs **TestDaF, DSH
> or Goethe at roughly B2–C1**. For a Malaysian student with no German, that is typically a year
> of language study before the degree even starts — a genuine cost in time and money that belongs
> in `duration_years` and the total, not a footnote. English-taught programmes typically want
> **IELTS 6.0–6.5 / TOEFL 80–100** (aggregator-level figures — confirm per university).

> **6. Direct entry is not automatic: it depends on the anabin classification.** Whether a student
> enters a bachelor's directly or must first do a one-year **Studienkolleg** and pass the
> *Feststellungsprüfung* is decided by how the **anabin** database rates their school-leaving
> certificate — **H+** means direct access, **H+/-** means Studienkolleg first. **British
> A-Levels are normally H+ and exempt from Studienkolleg**, which is good news for this pipeline's
> typical student, but **STPM, UEC and matriculation routes are a separate question and must be
> checked, not assumed.** Use uni-assist's admission checker per student, and note that a
> Studienkolleg year makes it a 4-year commitment.

> **7. uni-assist is the closest thing to UCAS, and it charges per application.** Many (not all)
> public universities route international applications through **uni-assist**, which costs **€75
> for the first application and €30 for each additional one** in the same cycle. Some universities
> apply direct instead — check per university rather than assuming. Note this is a *processing*
> service, not a central clearing house: it does not rank or allocate, it verifies documents.

> **8. The blocked account (Sperrkonto) is a hard cash requirement before the visa.** A student
> visa needs proof of funds in a blocked German account — on the order of **€11,904 for the year**
> (roughly €992/month released), with the job-seeker/Opportunity Card figure quoted separately at
> about **€1,027/month**. The money is not *spent* on the degree, but the family must be able to
> park it up front, so it belongs in the affordability conversation even though it is not a cost.
> **Figures move most years — fetch the current one, never quote this line.**

> **9. Post-study work is genuinely strong: an 18-month job-seeker residence permit.** Any
> graduate of a German degree, regardless of nationality, can stay **up to 18 months** to look for
> work related to their degree (*Aufenthaltserlaubnis zur Arbeitsplatzsuche*). That is materially
> better than the UK's Graduate Route, which is shortening to 18 months for applications from
> 2027 and was 2 years before — worth surfacing for any student weighting employability or
> migration, and worth setting against trap 1 when the student's real goal is practising in
> Malaysia rather than staying.

> **10. MQA recognition of German degrees is NOT yet researched.** Unlike Taiwan (which has an
> explicit MQA↔HEEACT Joint Statement of Confidence — see `taiwan.md`), no equivalent
> Germany-specific MQA arrangement was found in this desk pass, and **absence of evidence is not
> evidence of absence — it was not searched properly.** The first Germany row must establish this
> from MQA's own site before anything is stamped `Info source = Official page`, and must not
> infer it from trap 1 (BEM and MQA are different gates).

> **11. Currency.** Germany uses the **euro (EUR)**, which was **already** in `FX_TO_MYR` in
> `tools/shortlist_schema.py` before Germany was supported — no FX change was needed when the
> country was added on 2026-09-23. Check `FX_AS_OF` is not stale rather than assuming the rate is
> fresh.

## Learned during the run itself

_Nothing yet — this file has not been through a Stage 3 pass. First run: fill this section, stamp
the `untested` rows in the source table, and correct any trap above that desk research got wrong.
Trap 10 (MQA) is the highest-priority gap to close._
