# China — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> a China row. Split out of `03_discover_longlist.md` on 2026-07-30 — see that file's
> "Per-destination query playbook" section for how this fits into Step 1 and Step 3.

**China** → English-taught + CSC:
```
<course> English-taught bachelor China university
CSC scholarship <field> bachelor
<university> international admissions <course>
```

## Known-good sources (locations, never values)

> Places to **fetch**, never facts to quote — a fee, deadline or cutoff comes off the page every
> time (guardrail 2). `free` = plain `WebFetch` works; `blocked` = the page exists but 403s a
> plain fetch, so skip the retries and go straight to `firecrawl_search.py`; `quirk` = reachable
> only at the exact address given. Confirmed 2026-08-08. If one 404s, go up to the site root
> rather than guessing a deeper path — then fix the row here. **Cross-country sources —
> rankings, Malaysian sponsors, MQA + the professional bodies, English tests — are in
> `workflows/sources.md`**, not repeated per country.

| Answers | URL | Fetch |
|---|---|---|
| Official programme + CSC scholarship search (the government portal) | `https://www.studyinchina.edu.cn/` | free |

> **`campuschina.org` is dead — the domain no longer resolves.** It was the old CSC portal and still
> turns up in search results and older notes; `studyinchina.edu.cn` replaced it. Don't spend a retry
> on it (also recorded in `workflows/sources.md`).

The Sino-foreign JV universities (XJTLU, Duke Kunshan, NYU Shanghai, UNNC) are **not** on the CSC
portal in any useful way — go to each one's own international-admissions page, per the trap below.

> **For Humanities/History/Philosophy specifically, a literal English-taught "BA History" does not
> exist at mainstream Chinese universities — confirmed twice now (learned 2026-07-16 and re-confirmed
> 2026-07-28).** A china-admissions.com sweep of 9 History bachelor's programmes
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
>   trap as the USA (see `usa.md`), just transplanted onto a China row, so don't let the "China" label
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

## Traps — Engineering (learned 2026-09-23, HaotoWin's Mechanical Engineering pass)

The Humanities block above is about a missing *subject*. These are about the English-taught
international tracks generally, and they bit every row of a 6-university engineering pass.

1. **The English-taught double wall — check this BEFORE building a row for a scholarship-dependent
   student.** The tracks a non-Chinese-speaking student can actually take are the same tracks that
   (a) CSC undergraduate funding structurally excludes and (b) CEEAA accreditation visibly doesn't
   cover. Confirmed independently across four universities:
   - **Funding** — at **Wuhan University of Technology** *no* scholarship route applies to the
     English-taught bachelor's at all: its own CSC Bilateral option and CSC Type A/B both require
     Chinese-taught registration at bachelor's level. Not WHUT-specific — it is the CSC rule.
   - **Recognition** — CEEAA accreditation (China's Washington Accord carrier, see the constants
     template) was found only for the **Chinese-taught** majors at **BIT** (2014/2017) and **WHUT**
     (accredited 2015, **expired Dec 2023** on its face), and was **unconfirmed** at **Tsinghua**
     for the Zijing English track.
   So "China is a full Washington Accord signatory since June 2016" is true and still does not
   settle a row. Verify per programme; if you cannot, say so — do not let the country-level yes stand in.

2. **The joint ventures do NOT cleanly rescue recognition.** A foreign parent's accreditation does
   not automatically extend to the China campus, and nobody publishes a clear statement either way:
   - **XJTLU** routes via University of Liverpool to **IET / UK Engineering Council — not IMechE**,
     and only **partially** meets CEng (fully meets IEng). Likely fine for BEM, not certain.
   - **ZJU-UIUC (ZJUI)**: UIUC's own BS Mechanical Engineering is ABET-accredited, but no page
     confirms that accreditation for the **Haining delivery**; the ZJU BEng half's CEEAA status is
     unconfirmed too.

3. **XJTLU has no programme titled "Mechanical Engineering."** Confirmed against XJTLU's full
   52-programme list and the Liverpool mirror. The closest real match is **BEng (Hons) Mechatronics
   and Robotic Systems**. Don't dispatch a row-filler for a course title that doesn't exist.
   **XJTLU's fee is now CNY 99,000/yr** (official), not the CNY 93,000 recorded in the Humanities
   block above — that figure is stale.

4. **Tongji has no English-taught Mechanical Engineering bachelor's.** Its own International
   Students Office list of English-taught bachelor's programmes (updated Nov 2025) names exactly
   three: Civil Engineering (International Class), MBBS, and Architecture (International Class).
   Aggregators (BestEduChina, older SICAS/CUCAS listings) advertise a Tongji "Mechanical
   Engineering" in English; CUCAS's own page for it actually describes a **Chinese-taught doctoral**
   programme requiring HSK Band 4. Returning no fragment is the correct outcome here.

5. **`key_deadline` for a student more than a year out: use the sentinel, not the last published
   date.** Chinese universities publish one cycle at a time. Copying the most recent closed date
   (e.g. `2026-06-30`) makes `feasibility_flags()` stamp **"Deadline passed"**, which tells a
   student they *missed* something when the truth is it *hasn't opened*. Use
   `Not published — check portal` and put the historical date in `research_notes`.

6. **HSK is usually not required for admission to an English-taught track, but may be required to
   graduate** — confirmed not-required for admission at BIT and WHUT; the graduation requirement
   could not be confirmed at either. Check it and state which of the two you mean.
