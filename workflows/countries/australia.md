# Australia — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> an Australian row. Split out of `03_discover_longlist.md` on 2026-07-30 — see that file's
> "Per-destination query playbook" section for how this fits into Step 1 and Step 3.

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
