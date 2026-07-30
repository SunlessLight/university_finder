# Japan — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> a Japan row. Split out of `03_discover_longlist.md` on 2026-07-30 — see that file's
> "Per-destination query playbook" section for how this fits into Step 1 and Step 3.

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
