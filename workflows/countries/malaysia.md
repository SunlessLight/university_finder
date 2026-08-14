# Malaysia — query playbook (Stage 3 discovery)

> Read by the main session for the roster sweep and by the `row-filler` subagent researching
> a Malaysian row. Split out of `03_discover_longlist.md` on 2026-07-30 — see that file's
> "Per-destination query playbook" section for how this fits into Step 1 and Step 3.

**Malaysia (home country)** → public + private + the accreditation register:
```
<course> Malaysia public university intake <intake>
<course> degree Malaysia private university international campus
MQA recognised programme <course>
<university> Malaysia <course> local student fees UPU
EAC accredited engineering programme Malaysia
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
| UPU — the public-university application system (the **local**-rate route, MUET not IELTS) | `https://upu.mohe.gov.my/` | free |
| MOHE — public higher-education policy, intakes, funding | `https://www.mohe.gov.my/` | free |

Recognition is the whole game on a Malaysian row and it lives in `workflows/sources.md`: the **MQR**
register (every domestic programme is on it — a floor, not a distinction) and the professional ladder
that actually scores, **EAC/BEM/Washington vs ETAC/MBOT/Sydney**. The Malaysian sponsors are there
too. Private and branch-campus fees come off each university's own page — no central register lists
them, and aggregators quote the international rate by default (see the trap below).

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
