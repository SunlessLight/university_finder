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
