# Service tiers — what's actually in the package

The thing students don't know: they think they're buying **a spreadsheet**. The spreadsheet is the
visible tip. Everything that makes the decision — the verified facts, the dossiers, the apply guide —
sits underneath it, and they never see it because nobody's ever shown them.

This file names the package so you can point at it. It sections the 5-stage pipeline into a **3-tier
product ladder**. The pitch ([pitch/](pitch/)) and the scripts ([scripts.md](scripts.md)) draw their
numbers from here; the reasoning behind the pricing is in [positioning.md](positioning.md).

The tiers stack — each one is only worth doing on options that survived the tier before it. That's the
whole design: research depth escalates as the list narrows, so nobody burns deep effort on a uni that
was never going to make the cut.

---

## Before Tier 1 — the intake (invisible, but it's where the fit comes from)

*Stages 1–2 · `profile.json` + `preferences.json`*

Before any uni is on any list, we pin down **who you are and what you actually want**: grades, budget,
English status, which countries are live, the field — and if you're **undecided on course**, a
career-backwards interest-discovery conversation to work it out. This is unglamorous input work, but
it's why the list that comes out is *yours* and not a generic "top unis" list. For an undecided
student, this is a real service on its own.

You don't sell this tier. You mention it: *"first I figure out what actually fits you, then I go find it."*

---

## Tier 1 — The List

*Stages 3–4 · `master_list.csv` · the 34-column spreadsheet*

**One line:** *Know your real options — costed in ringgit, sorted into reaches and safeties.*

What you get:
- **A longlist of 20–40 universities** that fit your grades, budget and countries — not famous names,
  *your* names.
- Narrowed to a **verified shortlist of 8–12**, where every hard fact (fees, entry requirements,
  English, deadlines) has been **re-checked against the university's own page / UCAS / Common App** —
  not a rankings site.
- **34 columns per uni**, in a spreadsheet that opens in Excel / Google Sheets.
- Two things a normal list never separates, kept in separate columns:
  - **Desirability** (a 0–100 score) — how good a fit the uni is, *excluding* whether you can get in.
  - **Admission likelihood** — **Reach / Match / Safety**, computed from your grade margin. A cheap uni
    you can't get into can never rank #1. That separation is enforced in code, not promised.
- **Total cost of the whole degree in ringgit** — not annual tuition. A 3-year UK degree and a 4-year
  US one are finally comparable.
- **`Info source`** on every row: `Not verified` until a human confirmed it on the official page,
  `Official page` after. You can see exactly what's been checked.
- **Recognised in Malaysia?** — for regulated professions (medicine / engineering / law / accounting),
  whether the degree lets you actually practise back home. A dealbreaker, flagged as one.
- Scholarship route, coverage and how competitive it is, per uni.

**This is the tier they picture.** It's real and it's the foundation — but on its own it's a comparison
table. The decision happens in Tiers 2–3.

---

## Tier 2 — The Dossiers

*Stage 5a · `dossiers/<uni>.pdf` · a deep file per finalist*

**One line:** *For your 3–5 favourites: can I get in, will I belong, and what will it take?*

What you get, **as a PDF per finalist** (3–5 of them):
- A **16-section decision dossier** — not a comparison row, a document you read to *decide*.
- **"Who actually gets in"** — real admitted-student texture pulled from Reddit / The Student Room
  offer-holder threads, the Common Data Set, NUS IGP cutoffs: the grades, extracurriculars and essay
  angles of people who actually got in. Most students don't know these sources exist. This is the
  genuinely irreplaceable section.
- **Will I belong** — study intensity, the student archetype, clubs and city feel, the
  Malaysian / halal / prayer angle where it matters.
- **Full cost, scholarships and financial aid** — including Malaysian sponsors (JPA, MARA, Yayasan).
- **Visa, work rights after graduating, recognition back home.**
- **"Why here / why hesitate"** — and yes, it includes *reasons to hesitate*. A list that only says
  nice things about every uni is a list nobody trusts. Every dossier tells you where a uni is weak for
  *you*. This is the most credibility-building thing in the whole package.

**This is the biggest part of the iceberg they can't see.** When a student says "I just want the
spreadsheet," this is the tier they don't know they're leaving on the table.

---

## Tier 3 — The Apply Pack

*Stages 5b + 8 · `recommendation.md` + `calendar.md` + `application_prep/<region>.pdf`*

**One line:** *Now go do it — every deadline in one place, every application costed and checklisted.*

What you get:
- A **ranked recommendation** with the application strategy spelled out.
- **One deadline calendar** — every application, scholarship and admissions-test date across every
  country, in a single list, so nothing gets missed. (Miss one you didn't know existed and the whole
  exercise was for nothing.)
- A **per-region "how to apply" guide, as a PDF** (US, UK, Australia, Singapore, China — one at a
  time), grouped **by application system** so shared work is done **once**: e.g. all the Common App
  schools filed together, MIT's own portal broken out separately. Each uni gets its checklist, tests,
  fees, essays and — the load-bearing part for a scholarship student — the **exact financial-aid
  mechanics**: the real cost of attendance, what aid actually covers, the residual you still pay, which
  forms (CSS Profile / IDOC) and their dates.
- The grouping-by-system move is **product design, not research** — no prompt produces it, because you
  don't know to ask for it.

**This is the tier that turns a decision into filed applications.** It's the difference between "I know
where I want to go" and "I applied, on time, to all of them, without missing an aid deadline."

---

## How to use this when selling

- The student thinks the product = **Tier 1**. Your job in one sentence: *"the spreadsheet is step one
  — after that you get deep files on your top picks and a step-by-step apply guide per country, all as
  PDFs you keep."*
- **Show, don't list.** The [sample pack](sample_pack/) is one row of the spreadsheet, one dossier, one
  apply-guide page — the three tiers made visible. Send that, then stop typing. (See
  [positioning.md §3](positioning.md).)
- Numbers, not adjectives: *"34 columns · 8–12 verified unis · 16-section dossiers · a deadline
  calendar across 5 countries."* Never "comprehensive."
