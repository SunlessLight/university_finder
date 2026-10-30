# Known-good sources — the cross-country ones (locations, never values)

> **This file caches *where to look*, not *what it says*.** A URL here is a starting point you still
> have to fetch. **Never quote a fee, a deadline, a cutoff, a rank or an award amount from this
> file** — those change every cycle, and a cached value is exactly the stale-fact failure guardrail 2
> (`00_overview.md`) exists to prevent. The file says "the sponsor list is here"; you still open it.
>
> Written 2026-08-08 to stop `row-filler` and `report-writer` rediscovering the same standing
> pages by search on every student. It holds only what is the **same for every destination** —
> rankings, Malaysian sponsors, Malaysian recognition bodies, English tests. **Destination-specific
> pages (UCAS, Common App, gov.uk, immi, ICA, IMMD, JASSO…) live in
> `workflows/countries/<code>.md`**, under that file's "Known-good sources" section, because the
> agent researching a UK row already reads `uk.md` and should not have to read a second file. Same
> invariant as the traps: **a URL lives in exactly one file.**

## Who reads this, and when

**Read it only when your work actually needs one of these.** It is not required reading for a
dispatch — a `row-filler` doing `Course at a glance` and `English req` needs nothing here.

| You need | Section |
|---|---|
| `Overall rank` / `Subject rank` | [Rankings](#rankings) |
| `Scholarship & portal`, `How to get the scholarship`, report §6 *Scholarships & financial aid* | [Malaysian sponsors](#malaysian-sponsors-the-standing-ones) |
| `Recognition (MQA/body)`, report §9 *Recognition back home* — **a gate for regulated professions** | [Malaysian recognition](#malaysian-recognition--mqa--the-professional-bodies) |
| `English req` when a university's own page is vague about the test itself | [English tests](#english-tests) |

## How to use an entry

Each row is **the question it answers → the URL → whether a plain fetch works.**

- **`free`** — `WebFetch` gets it. Start there.
- **`blocked`** — verified to exist, but returns 403 to a scripted/plain fetch. That is guardrail 6's
  "blocked" case, so **go straight to `firecrawl_search.py`** rather than burning three retries
  proving it again. If Firecrawl also fails, fall back to the university's own page for the same
  fact (a uni press page usually states its own QS position) and say so in `research_notes`.
- **`quirk`** — reachable, but not at the address you'd guess. Use the exact URL given.
- **`browser`** — the page loads, but the answer sits behind a search form that a plain fetch
  cannot fill in, so `WebFetch` returns the empty form and nothing else. Firecrawl is no help
  either. Only a session that drives a real browser (the `mcp__claude-in-chrome__*` tools) or
  Evan by hand can read it. Subagents have no browser, so they write `Not checked` and leave
  the lookup to the main session. The row's own note says how to drive the form.

**If a URL 404s, do not guess a deeper path** — the deep links here are the ones that rot (five of
the twelve deep paths tried while building this file were already dead). Go up to the section root,
navigate from there, then **fix the row in this file** so the next student doesn't pay for it again.

## Rankings

Rankings are **discovery/positioning**, not hard facts — guardrail 2 still applies, and a rank is
never a reason to skip an official page.

| Answers | URL | Fetch |
|---|---|---|
| Overall world rank (QS) | `https://www.topuniversities.com/world-university-rankings` | **blocked** |
| Subject rank (QS) | `https://www.topuniversities.com/university-subject-rankings` | **blocked** |
| Overall + subject rank (THE) — the usable free alternative | `https://www.timeshighereducation.com/world-university-rankings` | free |

> **QS is the known-bad one, and it is bad in both directions** — 403 to a plain fetch *and*
> JavaScript-rendered, so even a successful fetch can return an empty shell. This is the trap already
> written up in `countries/uk.md` and `countries/australia.md` (learned 2026-08-05: four to
> five scrape attempts per university, several never recovered). **Try the university's own
> rankings/press page first** — Oxford, Edinburgh and Durham all state their own QS subject position
> on an official page, which is a better source anyway. Cap retries against `topuniversities.com` at
> 2-3, then write the honest band (`QS Philosophy #51-100, exact position not published`) or a
> labelled THE proxy. Never write `Not ranked` for a rank you merely failed to reach.

US News is deliberately absent: it timed out on every attempt while this file was built, it paywalls,
and it is an aggregator. Use THE or the university's own page.

## Malaysian sponsors (the standing ones)

The set of Malaysian sponsors barely changes; **their amounts, cycles and open dates change every
year**, and several open for only 10-14 days after SPM/STPM results. So: locations here, dates from
the page.

> **Eligibility is a filter, not a footnote.** `preferences.scholarship_interests` says which the
> student wants looked into, and `profile.ethnicity` gates the Bumiputera-restricted funds (MARA and
> Yayasan Peneraju are Bumiputera-only). Surface only what the student can actually claim — and
> ethnicity stays a research signal, never a desirability input (`00_overview.md`, guardrail 1).

| Sponsor | URL | Fetch |
|---|---|---|
| **JPA** — federal sponsorship, via the MOHE scholarship portal | `https://biasiswa.mohe.gov.my/` | free |
| **MARA** — TESP / YTP (Bumiputera-only); financing overview | `https://www.mara.gov.my/en/index/education/education-financing/` | free |
| **MARA** — the actual application portal | `https://educationloan.mara.gov.my/` | free |
| **PTPTN** — the study *loan*, not a scholarship; say which it is | `https://www.ptptn.gov.my/pinjaman-pendidikan` | free |
| **BNM Kijang Scholarship** — under Bank Negara's careers site, not a standalone domain | `https://www.bnm.gov.my/careers/scholarships` | **quirk** |
| **Yayasan Khazanah** — Khazanah Global Scholarship | `https://www.yayasankhazanah.com.my/` | free |
| **Yayasan Peneraju** (Bumiputera-only) — note: **no `www.`** | `https://yayasanpeneraju.com.my/` | **quirk** |
| **Yayasan Petronas** | `https://www.yayasanpetronas.com.my/` | free |
| MOHE — umbrella for federal study funding | `https://www.mohe.gov.my/` | free |

University-run and country-run awards are **not** here — those are per-university (the uni's own
scholarship page) or per-destination (`countries/<code>.md`).

## Malaysian recognition — MQA + the professional bodies

**A gate, not a footnote** (guardrail 5). For a regulated profession, a degree the body won't
recognise is a dealbreaker. The profession → body mapping lives in `01_intake.md` (finalize step 4);
this is only where each body's register is.

| Answers | URL | Fetch |
|---|---|---|
| Is a **Malaysian** programme MQA-registered? (the searchable register) | `https://www2.mqa.gov.my/mqr/` | free |
| Is a **foreign** qualification recognised in Malaysia? (eSISRAF; the search is at `kelayakan.cfm`) | `https://www2.mqa.gov.my/esisraf/kelayakan.cfm` | **script** |
| MQA generally | `https://www.mqa.gov.my/` | free |
| **Engineering** — Board of Engineers Malaysia (registration) | `https://www.bem.org.my/` | **blocked** |
| **Engineering** — Engineering Accreditation Council (accredited programmes, Washington Accord) | `http://www.eac.org.my/` | **quirk** |
| **Medicine** — Malaysian Medical Council (recognised medical programmes) | `https://mmc.gov.my/` | free |
| **Pharmacy** — Pharmacy Board Malaysia | `https://www.pharmacy.gov.my/` | free |
| **Law** — Legal Profession Qualifying Board | `https://lpqb.org.my/` | **quirk** |
| **Architecture** — Lembaga Arkitek Malaysia | `https://www.lam.gov.my/` | free |
| **Accounting** — Malaysian Institute of Accountants (recognised qualifications) | `https://www.mia.org.my/` | **blocked** |
| **Accounting** — ACCA Malaysia (the usable free route to the same answer) | `https://www.accaglobal.com/my/en.html` | free |
| **Technologist** — MBOT (the ETAC / Sydney Accord ladder, not BEM's) | `https://www.mbot.org.my/` | free |

Two quirks worth the line they cost, because each one has a failure mode that looks like "the site is
down" rather than "wrong address": **EAC serves `http://` only** — `https://www.eac.org.my/` fails
TLS handshake outright. **LPQB works on the bare host only** — `https://www.lpqb.org.my/` fails TLS,
`https://lpqb.org.my/` is fine.

**eSISRAF needs no browser (corrected 2026-10-30, the 2026-10-17 note said it did).** `WebFetch` of
`kelayakan.cfm` returns only the column headings, because the page fills itself in. Call its three
data addresses directly with a plain GET, one request a second:
`get_negara.cfm?term=<country>` → `get_institusi_json.cfm?term=<word>&kod_negara=<id>` →
`get_result.cfm?negara=<id>&institusi=<id>&bidang=&program=` (HTML table; last two columns are field
and qualification). Both lists return JSON `[{id, label}]`, cut at about 20 entries, so search a
specific word. Match the full institution name: loose words land on the wrong entry (`MASSACHUSETTS`
→ Amherst, `MELBOURNE` → RMIT, Monash has 5 entries, `NANYANG` → an old entry that is not NTU). China
is `REPUBLIK RAKYAT CHINA`; searching `CHINA` finds it. To read it by hand instead:
1. Open `kelayakan.cfm` in Chrome.
2. In **Negara** (country), type the English country name, e.g. `UNITED`, then pick `UNITED STATES`.
   The Malay name (`AMERIKA`) finds nothing.
3. In **Institusi**, type part of the name, e.g. `INSTITUTE OF TECHNOLOGY`. The list is long, so
   reading every option through the accessibility tree gets cut off around the letter H. Pull the
   matching option's text with a short page script instead, then click it.
4. Read the results table with `get_page_text`. Each row is one field (`Bidang`) and one
   qualification (`Kelayakan`).

The MIT result was 4 rows: Naval Architecture (degree), Agriculture (BSc), Science (BSc), and Arts
and Social Science (BA). How to read a result:
- **It is the public-service register** ("Sistem Pengiktirafan Kelayakan *Perkhidmatan Awam*").
  A listing means the qualification is recognised for a Malaysian government post.
- **It lists qualifications by broad field, not by programme.** An MIT engineering degree is
  awarded as an SB (Bachelor of Science), so it most likely falls under the "Science / Bachelor of
  Science" row. Say "most likely" in the report, not "confirmed".
- **For a regulated profession it is not the whole gate.** Engineering still goes through
  EAC/BEM (for a US programme, the Washington Accord via ABET accreditation). Medicine goes through
  MMC, and so on, as in the rows above.

**LPQB's actual recognised-degree list is a separate block even from the bare host (learned
2026-09-11, Rey's UK pass).** `https://lpqb.org.my/clp/list-of-qualifications-recognised-to-sit-for-pass-the-clp-examination`
plain-`WebFetch`es to only the nav shell (JS-rendered) — a **block**, not an error, so go straight to
`firecrawl_search.py --scrape-top` on that URL. It is the single named-whitelist page for **UK,
Australia and New Zealand** law degrees eligible for Malaysia's CLP exam (the exam that actually lets a
graduate practise law here) — a law degree from an unlisted university does not qualify, no matter how
good the university is (Edinburgh and Glasgow, for instance, are absent). Re-fetch fresh per student
rather than trusting an old fragment: the Board reviews the list periodically and both adds and
withdraws entries with a stated effective date (Durham's LLB was added effective 1 Jan 2026, binding
only for candidates completing on or after that date) — exactly the kind of dated fact this file's own
rule says never to cache here.

For **Malaysia-as-destination** rows, remember `countries/malaysia.md`'s rule: MQA is a *floor* there
(every domestic programme has it), so the distinction that scores is the professional ladder —
EAC/BEM/Washington vs ETAC/MBOT/Sydney.

## English tests

Only for the test's **own** rules (score validity, test formats, which variant a uni will accept).
**A university's required score comes from the university's page**, never from here.

| Answers | URL | Fetch |
|---|---|---|
| IELTS | `https://ielts.org/` | free |
| TOEFL | `https://www.ets.org/toefl.html` | free |
| **MUET** — the Malaysian public-university route (via UPU, not IELTS) | `https://www.mpm.edu.my/` | free |

## Dead — don't retry these

Recorded so a future session doesn't spend a search rediscovering that they're gone.

| Was | Status | Use instead |
|---|---|---|
| `campuschina.org` — the old CSC "Study in China" portal | **domain no longer resolves** | `https://www.studyinchina.edu.cn/` (see `countries/china.md`) |
| `www.isa.go.jp` — Japan's Immigration Services Agency | does not serve | `https://www.moj.go.jp/isa/` (ISA sits under the Ministry of Justice; see `countries/japan.md`) |

## Keeping this file honest

- **Every URL here was fetched and confirmed on 2026-08-08.** Links rot; a `free` flag is a
  historical observation, not a promise.
- **When a link breaks, fix the row** — that is the whole maintenance contract, and it is cheaper
  than the search it saves. Same for a `blocked` that starts working, or vice versa.
- **Adding a URL: it must be stable and cross-country.** One university's fee page is not a source
  location, it's a value — that belongs in the row's `research_notes`. A destination's visa page
  belongs in `countries/<code>.md`. This file is for pages that are the same on every student.
- **Never let this file grow values.** If you find yourself writing a number, a date or an amount
  into a row here, it belongs on the row of a student's `master_list.csv` instead.
