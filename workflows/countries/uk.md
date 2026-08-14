# UK — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> a UK row. Split out of `03_discover_longlist.md` on 2026-07-30 — see that file's "Per-destination
> query playbook" section for how this fits into Step 1 and Step 3.

**UK** → UCAS + official entry-requirement pages:
```
<course> UCAS course search
site:ac.uk <course> entry requirements
<course> BSc UK tuition fees international students
UK Graduate Route post study work
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
| Who offers the course + its entry requirements (UCAS course search) | `https://www.ucas.com/explore/search/courses` | **blocked** |
| Student visa rules **and** the financial-proof figure | `https://www.gov.uk/student-visa` · `https://www.gov.uk/student-visa/money` | free |
| Graduate Route post-study work | `https://www.gov.uk/graduate-visa` | free |
| Fee status, term-time working rules, living-cost guidance for internationals | `https://www.ukcisa.org.uk/` | free |
| Course-level outcomes and satisfaction — **official (gov-run), not an aggregator** | `https://discoveruni.gov.uk/` | free |

The whole `ucas.com` domain 403s scripted and plain fetches alike, so treat it as a Firecrawl target
from the first attempt. The university's own course page carries the same entry requirements and is
free to fetch — prefer it, and use UCAS for what only UCAS has (the cross-university course search
and the cycle deadlines).

> **The UK has NO meets-full-need or need-blind equivalent for internationals — if `scholarship_required`
> is a hard gate, say so plainly (learned 2026-07-28).** Unlike the USA (see `usa.md`), a wide
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
>
> **QS's subject-ranking table (`topuniversities.com`) is JavaScript-rendered — a plain fetch
> returns an empty shell, and it fought back on Firecrawl too (learned 2026-08-05
> backfill).** Every `Subject rank` lookup for History/Philosophy that hit this table needed
> repeated WebFetch + Firecrawl retries; Manchester, UCL Philosophy, Cardiff, and Exeter never
> recovered an exact number even after 4-5 scrape attempts each and had to report a verified band
> (e.g. "QS Philosophy #51-100, exact position not published") or a labelled THE-table proxy
> instead — that is the correct outcome per the "don't fake `Not ranked`" rule, just an expensive
> one to reach. **Try the university's own press release / rankings page first** — Oxford,
> Edinburgh, and Durham's subject figures all came from an official page citing their own QS
> position directly, no scrape needed. Cap retries against `topuniversities.com` itself at 2-3
> attempts before settling for the honest band/proxy; past that it is very unlikely to render.
