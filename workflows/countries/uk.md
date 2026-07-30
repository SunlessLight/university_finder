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

> **The UK has NO meets-full-need or need-blind equivalent for internationals — if `scholarship_required`
> is a hard gate, say so plainly (learned 2026-07-28, Francena).** Unlike the USA (see `usa.md`), a wide
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
