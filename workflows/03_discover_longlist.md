# Workflow: Stage 3 — Discover → Longlist (→ master_list.csv)

## Objective

Cast a **wide, cheap** net: find 20-40 plausible university+course candidates across the student's target
countries, score them at snippet level, and land them in `master_list.csv` as **Longlist**. Facts here are
*provisional* — they get verified against official sources in Stage 4. Don't deep-research yet.

## Tools used (in order)

1. `firecrawl_search.py --student <slug>` — discovery: runs search queries, saves results to
   `.tmp/<slug>/search_results.json`. **Costs credits — ask the user before running.**
2. *(agent step)* review results, extract candidates → write `.tmp/<slug>/uni_candidates.json`.
3. `sync_shortlist.py --student <slug>` — scores, dedupes, appends Longlist rows to `master_list.csv`.

## Per-destination query playbook

Generate ~8-15 queries spanning aggregators (for breadth) **and** official course pages (for the real
data). Substitute `<field>`, `<course>`, `<level>`.

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
> not just the scholarship columns. As of 2026 the need-blind-for-internationals list is only ~10 schools
> (Harvard, Yale, Princeton, MIT, Amherst, Dartmouth, Bowdoin, Washington & Lee, + Brown and Notre Dame
> from the Class of 2029) — and a sub-5%-acceptance deal-breaker removes the first four.
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
> **Don't invent a `key_deadline`** — leave it blank and verify at Stage 4; a fabricated date is worse
> than an empty cell.
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

**Singapore/Malaysia (local)** → NUS/NTU/SMU + MQA:
```
NUS OR NTU OR SMU <course> admissions
<course> Malaysia university intake <intake>
MQA recognised programme <course>
```

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

**China** → English-taught + CSC:
```
<course> English-taught bachelor China university
CSC scholarship <field> bachelor
<university> international admissions <course>
```

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
> per program rather than assuming — and **don't fabricate a `key_deadline`**; leave it blank and verify
> at Stage 4.
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

## Run discovery

```powershell
python tools/firecrawl_search.py "query one" "query two" --limit 6 --scrape-top 2
```
Or put queries in a JSON list and pass `--queries-file .tmp/<slug>/queries.json`. Use `--scrape-top N` to
pull full markdown for the most promising official course/prospectus pages (those scrape cleanly;
social/forum URLs return "Website Not Supported" — capture the URL + snippet, don't waste a scrape slot).
Results land in `.tmp/<slug>/search_results.json`. **`--student` (or `--out`) is required** — there is no
shared default path, so parallel sessions can't overwrite each other's results.

## Extract candidates (agent judgement)

Read `.tmp/<slug>/search_results.json`. For each plausible university+course, build a candidate object with honest
**0-5 sub-scores** and an **`entry_margin`** judgement, and write the list to
`.tmp/<slug>/uni_candidates.json`:

```json
[
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
    "scholarship_coverage": "",
    "scholarship_competitiveness": "",
    "scholarship_how_to": "",
    "funds_proof": "~GBP 12000 shown for visa",
    "post_study_work": "Graduate Route 2 yrs",
    "recognised_back_home": "MQA recognised; n/a professional body",
    "application_system": "UCAS",
    "key_deadline": "2027-01-15",
    "intake": "2027 Sept",
    "course_url": "https://www.manchester.ac.uk/...",
    "source_authority": "Not verified",
    "entry_margin": 0,
    "pathway_option": "INTO Manchester Foundation if below AAA",
    "fits_grades": "",
    "notes": "",
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
]
```

**Field notes:**
- **Some JSON fields have no CSV column of their own — they are inputs, not display.** Filling them is
  still mandatory; the master list shows what they *produce*:
  - **`currency`** ⇒ `Approx total (MYR)`. **This one is a silent-failure trap:** `to_myr()` returns
    `None` on a blank or unrecognised currency, which empties the MYR total *and* takes the
    `Over budget` warning down with it — an unaffordable row then looks clean. Always set it, and use a
    code from `FX_TO_MYR` (MYR/GBP/USD/AUD/SGD/CNY/EUR/JPY).
  - **`total_cost_programme`** ⇒ also `Approx total (MYR)`. Leave it empty to let the tool compute
    `total_tuition` + `est_living_per_year` × `duration_years`; set it explicitly only when that model
    can't express the cost (e.g. a mixed-currency 2+2 — see the branch-campus note below).
  - **`meets_english`** ⇒ the `English short` warning. `true`/`false` only; `null`/omit if unknown. It is
    a strict identity check, so the string `"No"` does **not** trigger the flag. The requirement itself
    goes in `english_req`, which *is* a column.
- Put a date in `key_deadline` as `YYYY-MM-DD` so it parses (extra text after the date is fine).
- `entry_margin` is your honest read of the student's grades vs the requirement: **+2** well above … **0**
  borderline/meets … **−2** well below. This maps to Reach/Match/Safety. Don't fold it into the sub-scores.
- `source_authority` stays `"Not verified"` at this stage — Stage 4 flips verified rows to
  `"Official page"`. These are the only two values the `Info source` column takes.

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
> two students can be discovered and synced **in parallel**. The rich scholarship detail columns are
> usually left blank at discovery and filled during Stage 4.

## Sync to the master list

```powershell
python tools/sync_shortlist.py --student <slug>          # add --dry-run to preview first
```
This computes desirability + A/B/C tier, Reach/Match/Safety, feasibility flags, dedupes by canonical
university+course, and appends new rows as **Longlist**. The CSV is created on first run.

## Edge cases & rules

- **Aim wide** — a Longlist of 20-40 across countries is healthy. Include some safe options, not only
  aspirational ones.
- **Don't over-scrape** — tune `--limit` / `--scrape-top` to control credit use; scraping costs more than
  searching. Only scrape the most promising official pages.
- **Provisional facts** — snippet-level fees/requirements are often wrong or out of date. That's fine here;
  Stage 4 verifies. Keep `source_authority = Not verified` until then.
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
- **The schema was slimmed 41 → 34 columns on 2026-07-16** — the master list is read in Google Sheets, and
  seven columns were blank, duplicated another column, or were internal bookkeeping: `Meets English?`,
  `Total cost (programme)`, `Currency`, `Student community links`, `Student life`, `Data as-of`,
  `Dossier status`. All five student CSVs were migrated in one pass (a disposable script, not a `tools/`
  entry — same rationale as the budget backfill below). **The columns went, the candidate-JSON fields
  stayed**: `currency`, `total_cost_programme` and `meets_english` are still required inputs (see Field
  notes above). If you are reading an old dossier or `.bak` that references the dropped columns, that's
  why. Toru's Stage-4 student-life research was rescued to
  `data/students/toru/student_life_research.md` — fold it into a dossier rather than re-researching it.
- **Budget stated as a RANGE silently killed the `Over budget` flag** (fixed 2026-07-16, keep in mind when
  reading older rows). `ingest_form_csv.py` passes the form's budget answer straight through, so a student
  who types `400000-800000` lands a *range string* in `profile.financial.total_budget`. `feasibility_flags()`
  used to do `float(budget)` inside a swallowing `except: pass` — the parse threw and the check silently
  never ran, so over-budget rows looked clean (it worked only for single-number budgets). `budget_ceiling()`
  now parses a range to its **upper bound**. Because sync only *appends*, **rows synced before the fix were
  never retro-flagged**. Don't trust the absence of `Over budget` on an old row; re-check against the ceiling.
  Ong's UK rows were backfilled on 2026-07-16 (UCL 893,850 / Manchester 885,000 / Warwick 841,281) and are
  now clean — worth knowing that the first status note of this named only two of the three, so **re-derive
  which rows are over from the CSV, don't trust a prose list of them.** Backfill is a small one-off script
  reusing `budget_ceiling()`: only range-budget students are affected, so it doesn't belong in `tools/`.
- **Stale `.tmp/<slug>/uni_candidates.json`** — this file is disposable and may carry leftovers from an
  earlier round (different unis, old scoring). Overwrite it fresh each discovery run rather than appending —
  `sync_shortlist.py` syncs whatever is in it.

## Done when

`master_list.csv` holds a broad Longlist with sensible scores and flags. Then proceed to **Stage 4**
(`04_university_dossier.md`) — where the student picks finalists, you verify their hard facts against
official sources, and build a dossier for each survivor.
