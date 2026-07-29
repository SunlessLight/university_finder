# Workflow: Stage 3 — Discover → Longlist (→ master_list.csv)

## Objective

Produce, for **ONE country per session**, 8-12 university+course rows in `master_list.csv` with **all 35
columns filled from official sources**. Every row is a **Longlist** row the student can cut on at a
glance; Stage 4 no longer re-verifies it, it only writes reports on the survivors.

> **The master list is the PRODUCT.** The client receives it as a spreadsheet, so a blank cell reads as
> breakage, not as work-in-progress (established 2026-07-29, after an audit of all 8 student CSVs found
> `Course at a glance` filled on 1 of 44 rows for one student and 24 of 24 for another — the workflow
> itself used to say "leave it for Stage 4"). Completeness is now enforced in code twice:
> `merge_candidates.py` before the CSV, `check_master_list.py` after it.
>
> **Completeness must never become invention.** The counterweight is `SENTINEL_VALUES` in
> `tools/shortlist_schema.py`: the honest ways to say there is no answer — `Rolling` /
> `Not published — check portal` for a deadline, `Not ranked` for a rank a university genuinely
> doesn't hold, `No statistics published` for scholarship odds, `Not published` for a grade bar,
> `None` for clean warnings. A sentinel is for *"there is no answer"*, never for *"I didn't find it"* —
> if the fact exists and you couldn't reach it, say so in `notes`.

> **The longlist is a SCANNING surface, not a report.** A row carries only what the student needs in
> order to **cut** — enough to say "keep looking at this one" or "drop it" at a glance in Google Sheets.
> Anything that needs a paragraph belongs somewhere else: the long-form research goes to
> `research_notes.md` now, and the real depth goes into the Stage-4 **university report**
> (`04_university_report.md`), which is the document the student actually reads to *decide*. Cell
> length budgets enforce this in code — see the readability rules below.

## Tools used (in order)

**One country per session.** Do not run two in one pass — that is what keeps this session's context
small enough to research 35 columns a row, and it's now a hard gate (`--country` on both tools).

```
0. Pick the country      — from the files, never ask. See "Pick the next country".
1. Roster sweep          — free WebSearch, 6-10 queries -> 8-12 rows of
                           university + course + city + course URL ONLY.
2. Country constants     — researched ONCE, reused by every row: visa money, work
                           rights, how to apply, intake, living benchmark, ranks.
                           -> .tmp/<slug>/country_<code>.json
3. Row fill              — PARALLEL row-filler subagents, one per university.
                           -> .tmp/<slug>/candidates/<uni-slug>.json
4. python tools/merge_candidates.py --student <slug> --country "<Country>"
                           merges the fragments; HARD-ERRORS naming every gap.
5. python tools/sync_shortlist.py --student <slug> --country "<Country>"
                           scores, dedupes, appends Longlist rows.
6. python tools/check_master_list.py --student <slug>
   python tools/build_glossary_sheet.py --student <slug>
7. Update status.md      — name the NEXT country explicitly.
```

**Search routing: free first, Firecrawl when free is blocked.** Claude's `WebSearch`/`WebFetch` is the
default for everything here, official course pages included. Escalate to `firecrawl_search.py` the
moment free search is *blocked* — meaning an error **or a response that doesn't contain the fact you
went there for** (a JS-rendered fee table coming back empty is the usual case, and it's a block even
though nothing errored). Then just run it; credits are there to be spent, no permission needed. The
full rule is **guardrail 6 in `00_overview.md`** — this is the only copy that stage-specific detail
belongs in.

## Pick the next country (don't ask the student)

`preferences.json → target_countries` is already in the student's stated preference order — that
order **is** the discovery sequence. Never open a session by asking "which country should we start
with" or "which country next" — work it out from the files, the same discipline `resume.md` uses
for the rest of the pipeline state:

1. **Read `target_countries`** from `data/students/<slug>/preferences.json` (e.g. `["Australia",
   "Singapore", "Malaysia", "China"]`) — this is the full ordered scope.
2. **Read `master_list.csv`'s `Country` column** (if the file exists yet) to see which of those
   countries already have rows. Zero rows ⇒ not yet discovered; any rows ⇒ at least started.
   `master_list.csv` is the source of truth here, not `status.md`'s prose — if they disagree, trust
   the CSV, same rule as `resume.md`'s "files win over the note."
3. **Next country = the first entry in `target_countries` with no rows yet.** Run **exactly one**
   country per session — roster → constants → row fill → merge → sync. Not a preference: `--country`
   on `merge_candidates.py` and `sync_shortlist.py` refuses a mixed batch, because a 35-column
   country pass is the most context this session can hold and still research honestly.
4. **Every target country already has rows ⇒ Stage 3 discovery is done**, not "pick one to redo" —
   move on to Stage 4 (see "Done when").
5. **Singapore and Malaysia are separate entries** (split 2026-07-29 — `COUNTRY_NORMALIZE` used to
   fuse them into one `Singapore/Malaysia` token, which handed Foo De Mi six Singapore rows for a
   country she never picked). They are two countries, two passes, two syncs. The same goes for any
   grouped label you meet in an older `preferences.json` — split it before you start.

The one case actually worth surfacing to the student: `target_countries` is empty/missing, or names
a country with no playbook section below and no obvious query pattern to improvise from. Everything
else is inferable from the files.

**Update `status.md` after every country's pass, not just at the end of the whole stage.** Rewrite
the "Master list state → Destinations covered" line and the "Next action" line to name the specific
next country (e.g. "Next: run Singapore discovery"), so a fresh session — or you, next message —
never has to ask again.

## Per-destination query playbook

**This section has two readers.** You use it for the **roster sweep** (step 1) — 6-10 queries to name
the country's 8-12 candidate universities and courses. Each **row-filler subagent** is told to read its
country's block first, because the dated traps below (the Australian domestic-fee trap, Singapore's
five-tier fee table, the SMU name collision, XJTLU's Year-2 entry) are exactly what a cold researcher
gets wrong. **They live here and only here** — never copy them into the agent file.

Substitute `<field>`, `<course>`, `<level>`. Aggregators are fine for *finding* universities in the
roster sweep; they are never the source of a number that lands in a cell.

**Cross-country (discovery only — never the source of record for a hard fact):**
```
<course> bachelor StudyPortals
QS world university rankings <field>
Times Higher Education <field> subject ranking
best universities for <course> <country>
```

**UK** → UCAS + official entry-requirement pages:
```
<course> UCAS course search
site:ac.uk <course> entry requirements
<course> BSc UK tuition fees international students
UK Graduate Route post study work
```

> **The UK has NO meets-full-need or need-blind equivalent for internationals — if `scholarship_required`
> is a hard gate, say so plainly (learned 2026-07-28, Francena).** Unlike the US block above, a wide
> UK search (9 unis incl. Oxbridge/Imperial/UCL/Russell Group) turned up only generic "international
> scholarships search" portals — no named award with a confirmed amount survived snippet-level
> discovery. UK international scholarships are typically **partial merit awards** (a few thousand GBP/yr
> off tuition), not the US's full-cost-of-attendance model. Score `scholarship_opportunity` modestly and
> uniformly at Longlist (there's rarely a documented reason to rank one uni above another on this axis
> yet), and flag the gap explicitly in `status.md` follow-ups for the Stage-4 conversation with the
> student — don't let a low, unremarked score quietly bury her #1 priority.
>
> **A-Level entry bars for Chemistry (and likely other sciences) cluster in two clean tiers, which
> makes `entry_margin` easy to source:** Russell Group non-Oxbridge sits at **AAB-ABB** (Nottingham,
> Southampton) down to **ABB-BBC/BBB** (Cardiff, Glasgow, Strathclyde), while UCL/Imperial ask **AAA/A*AA**
> and Oxbridge's **A\*A\*A** is holistic on top. A UK A-Level student with strong grades (A\*A\*A here)
> can look "Safety" by grades alone across most of the list — that's a correct, honest signal per
> `entry_margin`'s grade-only rule, not a bug to second-guess. Reserve the `admission_likelihood`
> override for genuinely holistic gates: Oxbridge's interview + admissions test, and a small-quota
> "very competitive" case like Imperial where the exact grade text wasn't sourced.
>
> **Course pages sometimes show a course-specific fee GROUP/BAND, not a flat rate — read for the
> subject match before taking the first number.** Cambridge's official fee table lists tuition by
> subject group (e.g. "Natural Sciences; Psychological and Behavioural Sciences" was Group 4 at
> £44,214/yr, 2026/27) rather than one university-wide figure — confirm Chemistry's actual group,
> don't assume the lowest or an average. Oxford, similarly, bands overseas fees **£37,380-£62,820**
> by course, and Chemistry (a lab science) sits at the **top** of that range, not the middle.

**USA** → Common App + department + outcomes:
```
<course> Common App universities
<university> <department> admissions requirements international
US News best <field> programs
OPT STEM <field> post study work
```

> **For the USA, FUNDING is the real axis — not sticker price.** A 4-year US degree runs ~840k-1.8M MYR,
> so for most Malaysian budgets *every* US row busts the ceiling at sticker and the list is meaningless
> unless built around aid. Always add these queries:
> ```
> US universities that meet full financial need for international students undergraduate
> need-blind admissions for international students US universities list
> <university> international students financial aid CSS Profile
> ```
> **Need-BLIND vs need-AWARE for internationals is the distinction that matters** — at a need-aware
> school, *requesting aid actively lowers admission odds*, so it belongs in `entry_margin` and `Notes`,
> not just the scholarship columns. And a sub-5%-acceptance deal-breaker removes the most selective end.
>
> **The need-blind-for-international cohort membership drifts — always re-check against each university's
> OWN current page, not a remembered list or even a past "confirmed" note in this file (learned
> 2026-07-28, Teoh Yu Shan; corrected again same day after a second session re-verified).** Bowdoin's July
> 2022 press release states *"Bowdoin joins Harvard University, Princeton University, Massachusetts
> Institute of Technology, Yale University, Dartmouth College, and Amherst College in including all
> students, regardless of citizenship, under its need-blind admissions policy"* — a clean, citable 7-school
> cohort **as of 2022**. Brown is widely reported to have joined later (~Class of 2029) — plausible but
> re-verify the year. **Washington & Lee and Notre Dame have since joined too — both are need-blind AND
> meet 100% of demonstrated need for international undergraduates, per their own pages, verified
> 2026-07-28:** Notre Dame's `admissions.nd.edu/apply/resources-for/international-applicants/international-faqs/`
> states "We offer need-based financial aid that meets the full demonstrated need of all undergraduate
> students, domestic and international"; W&L's `wlu.edu/admissions/financial-aid/types-of-aid/international-student-aid`
> states "W&L is need-blind in its admissions decisions" and "meets 100% of demonstrated financial need
> without loans for every admitted student." Both changes came from large 2024 gifts — Notre Dame's
> "Pathways to Notre Dame" initiative (announced 2024-09-13, effective Class of 2029) and W&L's $132M gift
> (announced 2024-10-24/25, effective Class of 2029) — **both postdating Bowdoin's 2022 anchor**, which is
> exactly why an earlier pass of this note (same session, same day) checked Notre Dame's general costs page
> instead of its international-applicants FAQ, found no international mention, and wrongly concluded
> need-aware/uncertain. **The actual lesson, twice-learned: "absent from an older confirmed list" is not the
> same as "excluded" — a school can join after the anchor source's date, so always check for a MORE RECENT
> institutional announcement before treating an exclusion as settled,** and prefer a page written for
> international applicants specifically (an FAQ, an "International Student Aid" page) over a general costs
> page that may simply not mention international status either way. Don't assume this correction is final
> either — this cohort keeps growing; re-verify against each university's own current page every time, and
> don't just trust this note's snapshot indefinitely.
>
> **Headline admit rates lie for aid-seeking internationals.** Duke publishes ~6% but funds only **20-25
> international students a year** university-wide, in a *separate* pool — the effective rate is far lower.
> Read the aid page, not the admissions brochure.
>
> **Expect the US list to be all Reach**, and say so rather than manufacturing a fake Safety: meets-full-need
> ∩ >5% admit ∩ good ranking is a tiny set with no safe end. The balanced-shortlist rule applies **across
> the whole list, not per country** — source the Safety from the UK/Australia/local instead.
>
> **The liberal-arts trap:** the most aid-generous schools (Amherst, Grinnell, Richmond, Bowdoin, W&L) have
> **no QS rank** and little Malaysian employer recognition, and often offer data science only as a *minor*.
> They score badly on ranking-led priorities despite being strongest on funding. Surface the trade-off and
> ask the student what "the name" means to them — QS rank or US reputation. Don't silently drop or inflate them.
>
> **Check the testing policy per school.** Test-optional is receding: Cornell, Dartmouth, Brown, Yale and
> Penn have all reinstated the SAT/ACT. If the student has no score, flag it — it's an action item with a
> deadline, not a disqualifier.

**Australia** → course catalogs + visa:
```
<course> bachelor Australia university course
QS Australia <field>
Australia 485 graduate visa <field>
<university> international tuition <course>
```

> **Australia is the SAFETY end of the list — expect it, don't fight it.** Australian entry is
> **cutoff-based, not holistic**: unis publish an explicit A-Level/ATAR bar per course, so
> `entry_margin` is a *measurement* here, not a guess. A strong A-Level student will legitimately
> come out Safety on nearly every row — that is a real result, the mirror image of the US all-Reach
> finding, and it is usually what makes the balanced-shortlist rule satisfiable **across** the list.
> The common deal-breakers (no Oxbridge, no sub-5% admit) are **non-binding** in Australia.
>
> **The A-Level aggregate scale is the unlock.** UNSW and UQ both score **A\*=6, A=5, B=4, C=3, D=2,
> E=1** — UNSW on the best **four** A2 subjects, UQ on the best **three**. Published cutoffs are far
> lower than they look: UNSW's Bachelor of Data Science and Decisions sits at **13.0 of a possible
> 24**, i.e. roughly BBBC. Convert the student's grades to the aggregate and compare — it turns
> "well-ranked but can I get in?" into arithmetic.
>
> **THE DOMESTIC-FEE TRAP — this one will silently destroy a budget column.** Australian course pages
> show the **Commonwealth Supported Place** (domestic) fee *right next to* the international fee, in
> the same visual block. UNSW's page reads "first year full fee **$8,500** / full fee to complete
> degree **$27,000**" — those are domestic. The international figures on the same page are
> **$60,000** and **$189,000**. Aggregators scrape the wrong one constantly (one quoted ANU's
> Applied Data Analytics at ~A$12,240/yr against a real ~A$56,120). **If an Australian annual fee
> looks under ~A$25,000, it is domestic. Do not use it.**
>
> **Duration drives cost more than fee level does.** An Australian bachelor is **3 years**, but an
> **honours** year makes it 4 and is often what's advertised. Sydney's 4-year Bachelor of Advanced
> Computing runs ~1.05M MYR while Melbourne's 3-year BSc runs ~746k on a *similar annual fee* — the
> extra year, not the price, busts the budget. Set `duration_years` to what the course actually runs.
>
> **There is NO September intake.** Semesters start **February** (Sem 1) and **late July** (Sem 2). A
> student whose `preferences.intake` says "Sept" cannot mean Australia — settle which semester before
> Stage 4, because it moves every deadline. For a Malaysian A-Level student finishing in December,
> Sem 1 (Feb) is tight but starts them ~7 months earlier than the UK/US; Sem 2 (July) is the safe fit.
> **Never invent a `key_deadline`** — if the university genuinely publishes none, write the sentinel
> (`Rolling`, or `Not published — check portal`). A fabricated date is worse than either.
>
> **Scholarships are Australia's weak spot** — partial fee remission (20-30%), not the US
> meets-full-need model. If the student ranks scholarship highly, say so plainly. The best structure
> found is **automatic consideration with no application** (e.g. Melbourne's 25% remission, ≥110
> awarded), which is worth more than a bigger award the student must win.
>
> **Subject rank and overall rank disagree sharply in Australia.** UTS is **4th in the country** for
> QS Data Science & AI (76.9) while sitting ~#88 overall; UNSW is ~#19 overall but scores *below*
> Monash and UTS on the subject. `subject_reputation` is scored on the **subject**, so surface the
> split rather than quietly resolving it — for a ranking-led student it's a real question.
>
> Use the official visa living-cost benchmark (**AUD 29,710/yr**, subclass 500, 2026) for
> `est_living_per_year`; Sydney/Melbourne run ~20-40% above it. Adelaide and Wollongong are
> **designated regional areas** — a possible extra year on the 485, which matters if
> `intent_to_migrate` is true.

**Singapore** → the public five + a private/foreign campus for the Safety end:
```
NUS OR NTU OR SMU <course> admissions
SUTD OR SIT <course> undergraduate international admissions
Singapore MOE tuition grant ASEAN undergraduate tuition fees
ASEAN Undergraduate Scholarship NUS NTU
JCU OR Curtin OR SIM Singapore <course> bachelor international fees
Singapore Employment Pass minimum salary graduate
```

> **Singapore and Malaysia were one block until 2026-07-29** — `COUNTRY_NORMALIZE` fused them into a
> single `Singapore/Malaysia` token, so a student who ticked only Malaysia got Singapore rows. They are
> two countries with almost nothing in common operationally (fee tiers, recognition ladder, entry
> system, cost), and now two separate passes.

> **SINGAPORE — for an ASEAN student, the funded public unis are a genuine mid-band, not a Reach wall
> (learned 2026-07-16, Ong).** The playbook that worked: 10 queries covering NUS / NTU / SMU / SUTD / SIT
> (public) **plus** a private/foreign campus (JCU / Curtin / SIM) for the Safety end, **plus** three
> structural queries — the MOE Tuition Grant bond, the with-grant-vs-without fee split, and the ASEAN
> Undergraduate Scholarship. Add a post-study-work query too (see below). Traps, in order of how badly
> each bites:
>
> **The fee table has FIVE tiers, not two — and the one you want is buried in the middle.** NUS/NTU/SMU
> pages (and NUS's official fee PDF) show, left to right: **Singapore Citizen · Singapore PR · International
> WITH Tuition Grant (ASEAN) · International WITH Tuition Grant (all other) · International WITHOUT Grant.**
> For a **Malaysian (ASEAN) student the correct column is the third**, and it is roughly *half* the
> no-grant column. NUS Computing/Science AY2026/27: ASEAN-with-grant **S$18,050** vs no-grant **S$36,650-39,700**.
> The citizen rate (~S$8,300) is the Australian-domestic-fee trap all over again — **if a Singapore fee
> looks like ~S$8-10k it is the citizen rate; do not use it.** Pick the tier deliberately and say which in
> `notes`. MOE sets the subsidised tiers, so NUS and NTU's ASEAN-with-grant figures match to the dollar —
> a useful cross-check when one page's column labels are ambiguous (NTU's fee page returned *different*
> labels on two fetches; the S$18,050 held because it matched NUS's PDF).
>
> **The Tuition Grant is the row's real story, and its "cost" is a feature for a migration-minded student.**
> ~50% fee cut in exchange for a **3-year bond working for a Singapore-registered company** after
> graduating. For `intent_to_migrate: true`, that bond is close to a guaranteed graduate pathway — it
> should *lift* `post_study_work_fit`, not lower it. The **ASEAN Undergraduate Scholarship** stacks on top:
> **automatic consideration on the admission application (no separate form)**, 100% of post-grant tuition +
> living/accommodation allowances, interview-selected. That auto-consideration structure is worth more than
> a bigger award you must separately win — score it well. Private/foreign campuses (JCU etc.) get **neither**
> the Grant nor the scholarship — their listed fee is the full fee.
>
> **Admissibility is the mirror of Australia — measured, and often a Reach.** NUS/NTU publish an
> **Indicative Grade Profile (IGP)**, but note two things: (1) it is for **Singapore-Cambridge** A-Levels,
> not international A-Levels, and international places are capped — so treat it as *indicative*, not the
> arithmetic Australia gives you; (2) the direct-admit data courses are so oversubscribed the profile is
> **AAA/A at BOTH the 10th and 90th percentile** (no spread) — a single B (Ong's Physics) pushes a student
> into Reach. **The escape hatch is the entry door:** at NUS, applying to the **Faculty of Science** and
> declaring the Data Science major *after* admission has a far softer published profile (ABB/C → AAA/A) than
> the direct-admit courses. Finding the soft door can turn a Reach into a Match at the same university —
> protect it. Don't invent an acceptance rate to test a sub-5% deal-breaker against; NUS/NTU don't publish
> one, and the IGP is not a rate. NTU's IGP is a **PDF that Firecrawl/WebFetch won't render** — if you can't
> get the real bar, say the entry margin is inferred and flag it for Stage 4, don't fake precision.
>
> **Singapore's intake is August — it maps cleanly to a "Sept" preference** (unlike Australia, which has no
> September intake). One intake a year. Public degrees are **4 years** (direct honours). A private
> trimester campus can run a bachelor's in **2 years** (JCU Singapore) — the inverse of the Australian
> honours trap, and usually the cheapest row on the list; but a 2-year BSc raises **two real Stage-4
> checks: MQA recognition, and whether it qualifies for Employment Pass COMPASS points.**
>
> **There is NO post-study work visa.** The Student's Pass lapses at graduation (~30-day grace); staying
> needs an **Employment Pass** — a job offer at **S$6,000/month (non-financial) or S$6,600 (financial)
> from 1 Jan 2027**, plus COMPASS points. Put this in `post_study_work` honestly: the *bond* guarantees
> three years of work, but a *long-term* stay still runs through the EP salary bar.
>
> **The SMU name-collision trap (cost a scrape this session):** `datascience.smu.edu` and `smu.edu` are
> **Southern Methodist University in Dallas, Texas** — not Singapore Management University (`smu.edu.sg`).
> A scrape of the Texas site returned US fees. Any `smu.edu`-without-`.sg` result is the wrong SMU. Also:
> SMU offers data science as a **second major on an Economics/Computing degree**, not a standalone DS
> degree — score `course_match` for what it actually is.

**Malaysia (home country)** → public + private + the accreditation register:
```
<course> Malaysia public university intake <intake>
<course> degree Malaysia private university international campus
MQA recognised programme <course>
<university> Malaysia <course> local student fees UPU
EAC accredited engineering programme Malaysia
```

> **Malaysia is a home-country pass and inverts three habits at once.** The traps are written up in the
> scoring section below rather than here, because each is a scoring rule, not a query — read all three
> before filling a Malaysian row:
> - **`recognition_fit`: MQA is a floor, not a distinction** — every Malaysian programme is MQA-registered,
>   so scoring MQA as recognition makes every domestic row max out for a reason that means nothing. Score
>   the professional ladder (EAC/BEM/Washington vs ETAC/MBOT/Sydney), per programme.
> - **Price at the LOCAL rate, not the international one** — aggregators quote the international fee by
>   default, and the local rate is often 4-10x less at a public university. The local route has its own
>   English requirement (**MUET** via UPU, not IELTS).
> - **A "local" branch-campus row may be a 2+2 in disguise** — a mandatory transfer inverts the cost
>   model, `post_study_work_fit`, and what the row should be compared against.
>
> Malaysia usually supplies the **Safety** end of a list and the only rows where the student can live at
> home — both worth saying out loud when the rest of the list is Reach-heavy.

**China** → English-taught + CSC:
```
<course> English-taught bachelor China university
CSC scholarship <field> bachelor
<university> international admissions <course>
```

> **For Humanities/History/Philosophy specifically, a literal English-taught "BA History" does not
> exist at mainstream Chinese universities — confirmed twice now (learned 2026-07-16 and re-confirmed
> 2026-07-28, Teoh Yu Shan).** A china-admissions.com sweep of 9 History bachelor's programmes
> (Tsinghua, Zhejiang, Wuhan ×2, Sichuan, Beijing Normal, East China Normal, Chongqing, Zhengzhou ×2)
> found every single one Chinese-taught. **The realistic substitutes are Sino-foreign joint-venture
> (JV) universities**, not a mainland public university's own History/Philosophy department:
> - **XJTLU (Xi'an Jiaotong-Liverpool)** — `BA (Hons) China Studies` is an Area/Sinology-Studies
>   degree (not literally History, but its core modules are heavily historical) and a genuine dual
>   degree with University of Liverpool (Russell Group). International A-Level students meeting the
>   bar (**BBB**) enter **directly into Year Two** — this quietly means the real commitment is **3
>   years, not the advertised 4**; set `duration_years` to the years actually attended, not the
>   headline. Fee (own fees page): **RMB 93,000/yr**. Living cost has a wide range on XJTLU's own
>   living-costs page — a frugal dorm-based student runs ~RMB 3,700/month (~44,400/yr) vs a private
>   apartment up to ~RMB 9,600/month (~115,200/yr); pick the frugal figure as the default estimate and
>   flag the range.
> - **Duke Kunshan University** (Duke + Wuhan University JV) and **NYU Shanghai** (part of NYU's
>   global network) both offer genuine English-taught **Philosophy and/or History tracks** inside a
>   Humanities-style major — a tighter course-name match than XJTLU's Area Studies. Both apply via the
>   **Common Application** (Duke Kunshan: commonapp.org/explore/duke-kunshan-university; NYU Shanghai:
>   the same Common App used for NYU's NY/Abu Dhabi campuses — A-Levels accepted with predicted
>   grades). Both are **holistic with no published grade bar** (`entry_margin: "not_published"`) and
>   both are **need-AWARE for internationals, not need-blind** — this is the same US-style funding
>   trap as the USA block above, just transplanted onto a China row, so don't let the "China" label
>   imply cheap. 2026-27 official costs of attendance: Duke Kunshan **~USD 84,065/yr** (own tuition
>   page), NYU Shanghai **~USD 91,676/yr** (own cost-of-attendance page) — both can out-cost the
>   cheapest US rows on the same list.
> - **CSC (Chinese Government Scholarship) does NOT meaningfully apply to any English-taught JV
>   programme.** Its own rules (confirmed via a Chinese-taught-university's international-admissions
>   page restating MOE/CSC policy) state undergraduate scholarship recipients "must register for
>   Chinese-taught credit courses" (Chinese-medium prep year unless HSK-exempt) — CSC targets
>   Chinese-taught majors specifically. A university that surfaces in search as "CSC-eligible for
>   History/Philosophy" (e.g. Jinan University) is offering the **Chinese-taught** version of that
>   major, not an English-medium one — don't treat CSC eligibility as evidence a programme is
>   accessible to a student with no demonstrated Chinese/HSK proficiency.
> - Also checked and excluded for Humanities: **University of Nottingham Ningbo China** offers only
>   English/Communications/Applied-Linguistics majors, no History or Philosophy.

**Hong Kong** → English-taught + non-local admissions (placeholder — no verified traps yet):
```
<course> bachelor Hong Kong university non-local student admissions
HKU OR CUHK OR HKUST OR PolyU OR CityU <course> international admissions
<university> non-local student tuition fees
IANG Hong Kong post-study work visa
```
> **This block has not been run for a real student yet.** Unlike the other destinations above, it
> carries no dated, learned traps (currency, fee tiers, intake quirks) — don't invent any. Fill it
> in with real findings (fee-tier gotchas, intake dates, recognition/accreditation notes) the first
> time a Hong Kong candidate is actually researched, per the Self-Improvement Loop in `CLAUDE.md`.
> Set `currency: "HKD"` (now in `FX_TO_MYR`) or the MYR total silently blanks.

**Japan** → English-taught (G30/SGU) + MEXT:
```
<course> English-taught bachelor Japan university G30
SGU Super Global University <field> undergraduate English
<university> undergraduate international admission English program
MEXT scholarship undergraduate <field>
<university> international tuition admission fee
```

> **Japan is a real Safety-side / affordability play — the mirror of the US, and the reason it earns a
> place in a RM500k budget.** National and public universities run a **near-flat tuition** (national
> standard **~¥535,800/yr**, ~RM 17k) plus a one-off **admission fee ~¥282,000** — an order of magnitude
> under US sticker. Private engineering universities run **~¥1.5-1.8M/yr** (~RM 47-56k), still well
> inside budget. Set `currency: "JPY"` (now in `FX_TO_MYR`) or the MYR total silently blanks.
>
> **English-taught engineering is a NARROW set — this is the real constraint, not cost.** The vast
> majority of Japanese bachelor's are taught in Japanese and gate on **EJU + JLPT N1/N2**. The
> discoverable English-medium (EMI) pool is the **G30 / SGU (Super Global University)** programs: e.g.
> UTokyo (PEAK — humanities/science, very limited), Tokyo Institute of Science, Kyushu, Nagoya, Tohoku,
> Waseda, Sophia, and Ritsumeikan APU. **For mechanical/engineering specifically the EMI list is
> thin** — search per-university rather than trusting an aggregator, and flag any Japanese-language
> requirement honestly in `notes`; it's a real barrier, not a footnote.
>
> **Intake ≠ September.** The Japanese academic year starts in **April**; many EMI/G30 programs *also*
> run an **autumn (Sept/Oct)** intake, but not all. Reconcile against `preferences.intake` (Sept 2027)
> per program rather than assuming — and **never fabricate a `key_deadline`**; where none is published,
> use the sentinel (`Rolling` / `Not published — check portal`).
>
> **MEXT is the scholarship story** — the government scholarship (embassy-recommended or
> university-recommended) can cover tuition + a monthly stipend + airfare, but it is **highly
> competitive and application-heavy**; treat it like the US meets-full-need schools — score
> `scholarship_opportunity` for the *opportunity*, put the competitiveness in `notes`/`entry_margin`,
> don't inflate.
>
> **Recognition:** Japan is a **Washington Accord** signatory via **JABEE** — relevant to Murugaa's
> `recognition_targets` (MQA + BEM + Washington Accord). But **not every program is JABEE-accredited**;
> record it as a Stage-4 verify, not an assumption.
>
> **Post-study work:** graduates switch from the student visa to a work visa ("Engineer/Specialist in
> Humanities" or the "Designated Activities" job-hunting extension, ~1 yr). Japanese-language ability
> heavily shapes actual employability — note it in `post_study_work` rather than treating the visa
> route as the whole answer.

## Step 1 — Roster sweep (free WebSearch, main session)

Name the country's candidates and **nothing else**. 6-10 free `WebSearch` queries off the playbook
block above, and for each plausible hit record only four things:

| university | course | city | course URL |
|---|---|---|---|

**Stop there.** No fees, no entry bars, no scores — those are the row-fillers' job, and pulling them
now means paying for the same page twice and filling this session's context with 12 universities'
worth of detail. Aim for **8-12 rows**: enough to cut from, few enough that each can carry 35
researched columns. Aggregators (StudyPortals, QS, THE) are welcome *here* — this is the one step
where they're the right tool.

Sanity-check the roster before dispatching: drop anything that plainly fails a stated deal-breaker,
doesn't teach the field in English, or is a name collision (`smu.edu` is **Texas**, not Singapore).
Each bad row costs a full subagent.

## Step 2 — Country constants (once per country)

Research **once** what every row in this country would otherwise re-research 10 times, and write it to
`.tmp/<slug>/country_<code>.json`. Every row-filler is handed this path:

```json
{
  "country": "Australia",
  "as_of": "2026-07-29",
  "visa_funds_proof": "AUD 29,710/yr living costs + first-year tuition + return airfare (subclass 500)",
  "post_study_work": "485 graduate visa, 2-3 yrs; +1 yr in designated regional areas",
  "application_system": "Direct to each university (or an agent portal)",
  "intakes": "Semester 1 late Feb; Semester 2 late July. NO September intake.",
  "living_benchmark_per_year": "AUD 29,710 (official); Sydney/Melbourne ~20-40% above",
  "recognition_route": "Washington Accord via Engineers Australia; check MQA recognition per programme",
  "ranking_source": "QS 2026 subject + overall",
  "notes": "Domestic (Commonwealth Supported) fees appear beside international fees on the same page."
}
```

Fill only the keys that are genuinely country-wide. A row-filler is told to prefer a real per-university
exception over these when one exists — and to say so in `research_notes` when it does.

## Step 3 — Row fill (parallel `row-filler` subagents)

Dispatch **one `row-filler` subagent per university, in parallel** (`.claude/agents/row-filler.md`,
pinned to Sonnet). Each researches its one university+course and writes exactly one fragment to
`.tmp/<slug>/candidates/<uni-slug>.json`. Give each dispatch, explicitly:

- the **student slug**,
- the **one university + course** (and city + course URL from the roster),
- the **country**,
- the path to `.tmp/<slug>/country_<code>.json`.

Parallel is safe here and serial is not just slower but *worse*: each agent writes its own fragment
file and never touches `master_list.csv`, so there is nothing to race — unlike Stage 4's report-writer
dispatches, which rewrite the whole CSV and must run one at a time. Keeping the research out of this
session is the point: 12 universities' worth of fetched pages would otherwise all land in one context.

**Parallelised by ROW, not by column.** One agent per university (~2-3 fetches each) beats one agent
per column (~21 agents each re-fetching the same course page). It also matches how the tools work:
`sync_shortlist.py` dedupes by `course_key` and **skips** a repeat university rather than merging into
it, so a column-at-a-time sync is impossible today — and scoring needs all eight sub-scores at once
anyway. Fragments in, one merge, one sync.

When they're all back, read the "Gaps/flags" line of each reply — that's where sentinels and
unverifiable facts get declared — before merging.

> **Firecrawl's rate limit is tight and shared across search+scrape (~10-15 req/min, learned
> 2026-07-28, Francena).** This bites much less now that Firecrawl is a *fallback* rather than the
> primary discovery tool, but it still applies when several row-fillers escalate at once: some queries
> return 0 results, some scrapes silently come back `null`, and the tool still exits 0. **Check the
> `results` count and `markdown` per query before trusting a batch.** Retry a few seconds later (the
> error carries a `retry after Ns` hint), and always to a **different `--out` path** — the tool
> overwrites and has no append mode, so concurrent agents must not share one output file.

## The candidate schema (what each row-filler writes)

> **`specific_courses` from the Broad-Area grid is a sub-category, not a literal course title.**
> The grid's per-area cell (e.g. "Accounting & Finance (Includes Corporate Finance, Banking &
> FinTech)") is the student's course of interest *in their framing* — treat it as decided
> (`interest_discovery.decided = true` already reflects this), but search **broadly across the
> courses implied by that sub-category** (Accounting, Finance, Banking, FinTech, Corporate
> Finance, …), not for an exact title match against the label itself. A course named just
> "BSc Finance" or "BSc Banking & FinTech" both count as candidates for that student.

One fragment per university, at `.tmp/<slug>/candidates/<uni-slug>.json` — a **single** candidate
object, with honest **0-5 sub-scores** and an **`entry_margin`** judgement. **Every field below is
required and non-empty** (`REQUIRED_CANDIDATE_FIELDS` in `tools/shortlist_schema.py`, enforced by
`merge_candidates.py`); `total_cost_programme` is the one exception, where empty means *"compute it
from tuition + living × duration"*, which is the normal case.

```json
{
  "university": "University of Manchester",
  "course": "BSc Computer Science",
  "country": "UK",
  "city": "Manchester",
  "subject_rank": "QS CS #51-100",
  "overall_rank": "QS #34",
  "entry_requirements": "AAA incl. Maths",
  "student_grades": "AAA (predicted)",
  "english_req": "IELTS 6.5 (6.0)",
  "meets_english": true,
  "annual_tuition": "GBP 30000",
  "total_tuition": "GBP 90000",
  "est_living_per_year": "GBP 12000",
  "duration_years": 3,
  "currency": "GBP",
  "total_cost_programme": "",
  "scholarship_portal": "Global Futures Scholarship — apply via the university funding portal",
  "scholarship_coverage": "GBP 5,000/yr off tuition, renewable for all 3 years",
  "scholarship_competitiveness": "No statistics published",
  "scholarship_how_to": "Automatic on the UCAS application; no separate form. Decisions with the offer.",
  "funds_proof": "~GBP 12,000 living costs shown for the visa, plus first-year tuition",
  "post_study_work": "2 yrs work rights after graduating (Graduate Route)",
  "recognised_back_home": "MQA recognised; no professional body needed for pure CS",
  "application_system": "UCAS",
  "key_deadline": "2027-01-15",
  "intake": "2027 Sept",
  "course_url": "https://www.manchester.ac.uk/...",
  "source_authority": "Official page",
  "entry_margin": 0,
  "admission_likelihood": "",
  "admission_reason": "",
  "pathway_option": "INTO Manchester Foundation if below AAA",
  "course_at_a_glance": "3-yr BSc, broad first year then pick a specialism",
  "student_life": "Large city campus, strong industry-placement culture",
  "notes": "Fees confirmed on the course page for 2026/27 entry; 2027 rate not yet published.",
  "research_notes": "Fee page read 2026-07-29 ... (free length — the depth the cells can't hold)",
  "scores": {
    "course_match": 5,
    "subject_reputation": 4,
    "total_cost_fit": 2,
    "post_study_work_fit": 4,
    "scholarship_opportunity": 3,
    "experiential_fit": 3,
    "location_pref_fit": 4,
    "recognition_fit": 5
  }
}
```

**Field notes:**
- **Some JSON fields have no CSV column of their own — they are inputs, not display.** Filling them is
  still mandatory; the master list shows what they *produce*:
  - **`currency`** ⇒ `Approx total (MYR)`. **This one is a silent-failure trap:** `to_myr()` returns
    `None` on a blank or unrecognised currency, which empties the MYR total *and* takes the
    `Over budget` warning down with it — an unaffordable row then looks clean. Always set it, and use a
    code from `FX_TO_MYR` (MYR/GBP/USD/AUD/SGD/CNY/EUR/JPY/HKD).
  - **`total_cost_programme`** ⇒ also `Approx total (MYR)`. Leave it empty to let the tool compute
    `total_tuition` + `est_living_per_year` × `duration_years`; set it explicitly only when that model
    can't express the cost (e.g. a mixed-currency 2+2 — see the branch-campus note below).
  - **`meets_english`** ⇒ the `English short` warning. `true`/`false` only — and it is now **required**,
    so decide it: compare the student's test/score in `profile.english_proficiency` against the
    university's stated bar. It is a strict identity check, so the string `"No"` does **not** trigger
    the flag. The requirement itself goes in `english_req`, which *is* a column.
- Put a date in `key_deadline` as `YYYY-MM-DD` so it parses (extra text after the date is fine). Where
  the university publishes none, write the sentinel — `Rolling` or `Not published — check portal`.
- **`source_authority` is `"Official page"` at Stage 3 now**, because Stage 3 is where hard facts get
  verified (the pre-flight moved here on 2026-07-29 — Stage 4 is report-only). Leave `"Not verified"`
  **only** on a row whose facts you genuinely could not confirm on an official page, and say which fact
  in `notes` — that row can't become a Finalist until someone does. These are the only two values the
  `Info source` column takes.
- **Sentinels, not blanks, not guesses.** Every field is required, so a fact that genuinely doesn't
  exist takes its column's sentinel from `SENTINEL_VALUES` (`Not ranked`, `Rolling`,
  `Not published — check portal`, `No statistics published`, `not_published` as an `entry_margin`).
  A fact that *does* exist but you couldn't reach is not a sentinel case — name the gap in `notes`.

> **`entry_margin` means ONE thing: grades vs the published academic bar.** **+2** well above …
> **0** borderline/meets … **−2** well below. It produces the **`Grades vs entry bar`** column
> (`Well above`/`Above`/`Meets`/`Below`/`Well below`/`Not published`) and, by default,
> `Admission likelihood`. Don't fold it into the sub-scores.
>
> **Do NOT push a holistic Reach through `entry_margin` — that was a real bug (fixed 2026-07-25).**
> Agents were setting `entry_margin: -2` on selective US schools to express "unlikely to get in",
> so the grade column printed "No" for a student with A\*A\*A\*A at Duke, Vanderbilt and Georgia
> Tech — while the same student's other file read "Exceeds academic bar" at MIT. Same grades,
> contradictory answers, and a quiet breach of the desirability-vs-admissibility guardrail.
> Anything that is **not** the grade bar — holistic selection, a capped international quota,
> need-aware admission, an interview or admissions test — goes in the override instead:
> ```json
> "entry_margin": 2, "admission_likelihood": "Reach", "admission_reason": "very selective"
> ```
> which renders **`Reach (very selective)`** and answers the student's real question: *why is a
> university I qualify for still a long shot?* Keep `admission_reason` under 24 characters.
> Where a university publishes **no** academic bar at all (holistic US admission, or a profile
> you genuinely could not retrieve), set `Grades vs entry bar` to **`Not published`** — saying so
> beats inventing a comparison. There is no `fits_grades` field any more; the column is derived.

> **Write cells for a scanning student, not for a report (the 2026-07-25 readability fix).**
> The master list is read in Google Sheets, where a 500-word cell truncates or blows the row
> height up. Three rules, all enforced by **`python tools/check_master_list.py --student <slug>`**
> — run it after every sync:
> 1. **Length budgets per column** (`CELL_BUDGETS` in `shortlist_schema.py`; `Notes` 200 chars,
>    most prose 120-200). Nothing is ever silently truncated — you say it shorter.
> 2. **`notes` vs `research_notes` — two fields, two destinations.** `notes` is the ≤200-char
>    headline that lands in the CSV; **`research_notes`** is free-length and is appended to
>    `data/students/<slug>/research_notes.md` under a `## University - Course` heading. Put the
>    verification stamps, source conflicts and cost traps there. This is what makes the budget
>    survivable — depth is preserved, just not in a spreadsheet cell.
> 3. **Plain English first.** Prefer the plain phrase over the acronym outright — it is *shorter
>    and* clearer (`3 yrs post-study work` beats `OPT + 24mo STEM OPT`). The replaceable terms
>    live in `apply_glossary.PLAIN_ALTERNATIVES`, and the linter flags them with their fix.
>    **Keep** the proper nouns the student must search for on an official page — UCAS, MQA, BEM,
>    Washington Accord, CSS Profile, IELTS; `tools/build_glossary_sheet.py` generates a per-student
>    `glossary.csv` explaining exactly the terms that student's list uses, to import as a second tab.
> - `course_at_a_glance` and `student_life` are **one tight sentence each** — the shape of the
>   degree, and what living there is like. **Research them and fill them here** (they used to be
>   left for Stage 4, which is exactly how they ended up blank on 43 of one student's 44 rows).
>   One real sentence from the course page and the university's own student-life/accommodation
>   pages is enough; an invented sentence about campus culture is a fabricated fact like any other,
>   so if you truly have nothing, say what you *do* know about the degree's shape rather than
>   inventing atmosphere.

**Scoring guide (each 0-5 — these are DESIRABILITY only, never admissibility):**
- `course_match` — how well the course matches the field/goal.
- `subject_reputation` — subject-specific rank + graduate outcomes (not overall vanity rank).
- `total_cost_fit` — full-programme total (MYR) vs the student's budget (lower cost = higher).
- `post_study_work_fit` — visa/post-study-work rights vs `intent_to_migrate`.
- `scholarship_opportunity` — realistic funding this student could actually get.
- `experiential_fit` — hands-on opportunities: projects, research, community involvement, not just exams.
- `location_pref_fit` — matches stated location/lifestyle preferences.
- `recognition_fit` — recognised back home (MQA + professional body) where it matters.

> **Scoring `recognition_fit` for HOME-COUNTRY (Malaysian) rows — MQA is a floor, not a distinction.**
> Every Malaysian programme is MQA-registered, so scoring MQA as recognition makes *every* domestic row
> max out and Malaysia sweeps the list for a reason that means nothing. Score the **professional ladder**
> the degree actually sits on, **per programme, not per university**:
>
> | Degree title says | Accreditor | Register | Accord |
> |---|---|---|---|
> | "Bachelor of **Engineering**" | **EAC** | **BEM** Professional Engineer (**Ir.**) | **Washington** |
> | "Bachelor of Engineering **Technology**" | **ETAC** | **MBOT** Professional Technologist (**Ts.**) | **Sydney** |
> | "Bachelor of Applied **Science**" | — | none | — |
>
> The two ladders are **not interchangeable**, and for a regulated profession this is a gate, not a
> preference. Check `profile.recognition_targets`: if it names **BEM / Washington Accord**, an ETAC row
> **fails the student's own gate even when the course title matches perfectly** — that's a real negative
> finding worth keeping on the list, not a row to quietly score well.
>
> **Tell-tales when the page doesn't name the accreditor** (common — programme pages often omit it):
> - The **degree title** is the strongest signal: "Engineering **Technology**" ⇒ ETAC.
> - The **PLO wording** gives it away: Washington Accord programmes say "**complex** engineering problems"
>   (WK1-WK7); Sydney/ETAC ones say "**broadly-defined** Engineering Technology problems" (SK1-SK4).
> - Registers to check: `eac.org.my` and `etac.org.my` (accredited-programme lists), `bem.org.my`, MQR.
> - If you can only **infer** the ladder, say so in `notes` and flag it for Stage 4 — never let an inferred
>   accreditation reach Shortlist unverified.
>
> **The EAC register is Cloudflare-protected — plan around it (learned 2026-07-16).** The *index* page
> (`eac.org.my/v2/list-of-accredited-engineering-programme-malaysia/`) scrapes fine with Firecrawl and gives
> you the list of accredited **institutions**, each linking to a per-university PDF of its accredited
> **programmes**. Those **PDFs 403 to both WebFetch and curl** (Cloudflare "Just a moment..." — a browser UA
> and Referer do not help), so you cannot confirm a *specific programme* from the register for free. Work
> around it in this order, which is free and was sufficient for all 6 Malaysian rows:
> 1. **The university's own programme page** — often names the accreditor outright ("Professional or
>    Statutory Body of Accreditation: ... Engineering Accreditation Council") and, better, exposes the
>    **PLO wording** tell-tale above. UTM's page did both.
> 2. **The university's FAQ / accreditation page** — UM's states "Board of Engineers Malaysia" + "Washington
>    Accord" explicitly.
> 3. **MQR** (`www2.mqa.gov.my/mqr`) — gives the professional body **and the accreditation window**; check the
>    end date, it may be expired on its face (UniMAP's read 2019-2024) and needs a renewal check at Stage 4.
> Note the institution list is **necessary but not sufficient**: a university on it has *some* accredited
> programme, not necessarily the one you want. Absence, though, is strong evidence — University of Cyberjaya
> is missing from it, matching its ETAC/Sydney-Accord status.

> **A "local" branch-campus row may be a 2+2 in disguise — check before costing it (learned 2026-07-16).**
> Monash Malaysia's Bachelor of Biomedical Engineering is *"a four-year degree where you'll study your first
> two years in Malaysia and your final years at our Clayton campus in Melbourne"* — the transfer is
> **mandatory**. That inverts three things at once, so catch it at discovery, not Stage 4:
> - **Cost** is mixed-currency and roughly 4x the local rate. The `total_tuition` + `living` × `duration`
>   model cannot express it — compute the total yourself and set **`total_cost_programme` explicitly** (in
>   MYR, with `currency: "MYR"`); the tool prefers an explicit value over the computed one.
> - **`post_study_work_fit` flips from floor to high** — the student graduates *in* the destination country
>   and gets its post-study visa (485), so a "Malaysia" row can carry a full migration pathway.
> - **The comparison changes**: score it against the parent university's home row, not the domestic rows.
> Also check **scholarship eligibility by qualification** — Monash Malaysia's RM8,000/yr waiver is UEC-only,
> so an A-Level student gets nothing from it.
> Conversely, don't trust an aggregator that a branch campus offers the field at all: Nottingham Malaysia has
> only Biomedical **Sciences** (BSc), and MMU Cyberjaya has no biomedical programme despite aggregator claims.

> **Home-country rows: price them at the LOCAL rate, not the international one.** Aggregators quote the
> international fee by default (eduadvisor listed UM Biomedical at RM111,400). A domestic student pays the
> subsidised local rate — often 4-10x less at a public university — which is usually what decides whether the
> row clears the budget. The local route also has its **own English requirement**: Malaysian publics take
> **MUET** (via UPU), not IELTS, so a student with no formal test still has an action item, just a different one.
>
> Watch the mirror-image trap too: an **RINA / IMarEST / MARDEP** stamp is genuine and worth noting, but it
> is *not* a substitute for the BEM route if that's what the student asked for.

> **Weights are per-student and live in `data/students/<slug>/weights.json`** — never in
> `tools/shortlist_schema.py`, which is shared source that concurrent sessions would fight over.
> Derive them from the student's `preferences.priorities` with the **`scoring-weights` skill** before
> syncing; `sync_shortlist.py` refuses to run without a valid file. Because no student state is shared,
> two students can be discovered and synced **in parallel**. **The four scholarship columns are filled
> here, not at Stage 4** — they were the single biggest source of blank cells, and for a
> `scholarship_required` student they are the reason the list exists.

## Steps 4-6 — Merge, sync, check

```powershell
python tools/merge_candidates.py  --student <slug> --country "<Country>"   # gaps stop here
python tools/sync_shortlist.py    --student <slug> --country "<Country>"   # --dry-run to preview
python tools/check_master_list.py --student <slug>                          # the gate
python tools/build_glossary_sheet.py --student <slug>                       # refresh Glossary tab
```

`merge_candidates.py` collects `.tmp/<slug>/candidates/*.json` into `.tmp/<slug>/uni_candidates.json`
and **exits 1 naming every `(university, missing field)` pair** — so you re-dispatch only the two
row-fillers that came back short, not the country. It also rejects a fragment whose `country` isn't
this pass's, and two fragments claiming the same university+course. Fixing gaps *before* the CSV is
the whole point: sync only ever appends and dedupes by `course_key`, so a university synced with holes
is silently **skipped** on a re-run rather than topped up.

`sync_shortlist.py` computes desirability + A/B/C tier, Reach/Match/Safety, feasibility flags, dedupes
by canonical university+course, and appends new rows as **Longlist**. It also writes each candidate's
`research_notes` to `research_notes.md`. The CSV is created on first run. **`--country` is required**
and every candidate must match it — one country per pass, enforced.

`check_master_list.py` is the gate — it must come back clean before you hand a list to a student. It
checks the header against the schema, **completeness** (every required column filled; a sentinel only
in a column that allows one), the length budgets, bare jargon that has a plain equivalent, the allowed
values per column, and contradictions between `Grades vs entry bar` and `Admission likelihood` (grades
below the bar can't be a Safety; grades above it that are still a Reach must say why).

## Step 7 — Update `status.md`

Rewrite "Master list state → Destinations covered" and "Next action" to name the **specific** next
country. Record the pass's cost (rough token spend + wall-clock) while you still know it — the
per-country budget is a measurement nobody has taken yet.

## Edge cases & rules

- **8-12 rows per country, not 20-40 in one go.** The old "aim wide" number came from snippet-level
  rows that cost almost nothing; a 35-column officially-sourced row is a different unit of work. Wide
  still matters — get the spread *across* countries and include genuinely safe options, not only
  aspirational ones — but a country pass that returns 25 rows means each got researched a third as well.
- **Don't over-scrape — for signal, not for spend.** Every scraped page lands in context and dilutes it,
  so a wide `--scrape-top` makes the extraction step *worse*, not just pricier. Tune `--limit` /
  `--scrape-top` to the most promising official pages.
- **Facts are official-sourced now, not provisional.** Stage 3 owns verification (the pre-flight moved
  here on 2026-07-29); Stage 4 writes reports and does not re-check the row. So a number in a cell has
  to have come off the university's own page — `source_authority = "Official page"`. A row left
  `Not verified` is an admission of a gap, and it must name the unverified fact in `notes`.
- **CSV append needs a trailing newline** — `sync_shortlist.py` appends rows. If the existing
  `master_list.csv` doesn't end in a newline (e.g. it was hand-edited, or renamed from another file), the
  first appended row used to fuse onto the last existing row, corrupting it into one physical line. The tool
  now auto-inserts a separator (`write_rows`/`needs_leading_newline`), but if you hand-edit the CSV, leave a
  trailing newline. Sanity-check after a sync: row count should rise by the "N new" the tool reports.
- **Header / schema column-order drift** — an older `master_list.csv` may carry the same columns
  in a *different order* than the current `SHORTLIST_HEADERS` (e.g. Toru's file had `Approx total (MYR)`
  at index 8, right after Country). `sync_shortlist.py` builds rows in schema order, so appending to a
  drifted file used to misalign every column of the new rows (data intact, but under the wrong headers).
  The tool now reorders appended rows to the *existing file's* header (`reorder_to_header`) and refuses
  if the column *set* differs (a real schema change → migrate first). If you find a drifted file, rewrite
  it once into `SHORTLIST_HEADERS` order (keyed by column name) so it matches the schema and the sibling
  students. Sanity-check after a sync that a spot-checked row's `Approx total (MYR)`/`City`/`Intake`
  line up under their headers.
- **The schema went 34 → 35 columns on 2026-07-25** (the readability fix). `Fits grades?` was renamed
  **`Grades vs entry bar`** and is now derived from `entry_margin` alone; `Backup entry route` was
  dropped from the CSV (it is a Stage-4 report section now — see `04_university_report.md`); and
  **`Course at a glance`** + **`Student life`** were added, one sentence each. All five student CSVs were
  migrated in one disposable pass. Two new per-student files came with it: `research_notes.md` (the
  long-form research the cells no longer hold) and `glossary.csv` (the Google Sheets Glossary tab).
- **The schema was slimmed 41 → 34 columns on 2026-07-16** — the master list is read in Google Sheets, and
  seven columns were blank, duplicated another column, or were internal bookkeeping: `Meets English?`,
  `Total cost (programme)`, `Currency`, `Student community links`, `Student life`, `Data as-of`,
  `Report status`. All five student CSVs were migrated in one pass (a disposable script, not a `tools/`
  entry — same rationale as the budget backfill below). **The columns went, the candidate-JSON fields
  stayed**: `currency`, `total_cost_programme` and `meets_english` are still required inputs (see Field
  notes above). If you are reading an old report or `.bak` that references the dropped columns, that's
  why. Toru's Stage-4 student-life research was rescued to
  `data/students/toru/student_life_research.md` — fold it into a report rather than re-researching it.
- **A missing `Over budget` flag on an OLD row proves nothing** (the free-text-budget era, closed
  2026-07-29). Budget used to be a free-text form question passed straight through, so a student who typed
  `400000-800000` landed a *range string* in `profile.financial.total_budget`; `feasibility_flags()` did
  `float(budget)` inside a swallowing `except: pass`, the parse threw, and the check silently never ran —
  over-budget rows looked clean. Two fixes closed it: `budget_ceiling()` parses a range to its **upper
  bound** (2026-07-16) and now also **rejects implausible values** (anything under 1000 → `None`, so
  `"~ 1 million? Idk"` no longer yields a ceiling of `1.0`); and the form's budget question became a
  **four-band dropdown** (2026-07-29), so nothing but a number or null reaches `total_budget_ceiling` any
  more — see the band table in `01_intake.md`.
  **Sync only ever appends, so rows synced before those fixes were never retro-flagged.** Don't read the
  absence of `Over budget` on a pre-2026-07-29 row as affordable; re-check it against the ceiling. Ong's UK
  rows were backfilled on 2026-07-16 (UCL 893,850 / Manchester 885,000 / Warwick 841,281) and are now
  clean — worth knowing that the first status note of this named only two of the three, so **re-derive
  which rows are over from the CSV, don't trust a prose list of them.** Backfill is a small one-off script
  reusing `budget_ceiling()`: only the affected students matter, so it doesn't belong in `tools/`.
- **Stale `.tmp/<slug>/candidates/`** — fragments are disposable and a stale one from an earlier round
  (different course, old scoring) merges just as happily as a fresh one. **Clear the directory before
  each country's pass**, and remember `merge_candidates.py` reads *every* `*.json` in it. Same for
  `uni_candidates.json`, which is overwritten, and which `sync_shortlist.py` syncs verbatim.
- **The 35 columns are all required now (2026-07-29)** — `REQUIRED_COLUMNS` in `shortlist_schema.py`,
  everything but `Warnings`, which is written `None` when a row is clean rather than left empty. The
  eight existing student CSVs were **not** backfilled: they predate the policy and will fail the
  completeness check until someone re-researches them. That's expected, not a regression — the policy
  applies to new students and new country passes.

## Done when

For **this country**: 8-12 rows in `master_list.csv`, every one of the 35 columns populated,
`merge_candidates.py` and `check_master_list.py` both clean, and `status.md` naming the next country.

For **Stage 3 overall**: every entry in `preferences.json → target_countries` has rows (see "Pick the
next country" — that's what makes this checkable without asking), with a Reach/Match/Safety spread
*across* the whole list rather than per country.

What carries forward is a **verified** list, not a provisional one. Stage 4 no longer re-checks these
facts — it takes the student's finalists and writes reports. Proceed to **Stage 4**
(`04_university_report.md`).
