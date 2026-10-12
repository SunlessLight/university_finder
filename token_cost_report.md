# Token cost report

Measurements of what real pipeline runs cost, in tokens. A prior version of this file tracked
down a specific token-bloat problem (16k+ token workflow file, uncontrolled `status.md` growth,
`shortlist_schema.py` full-file reads) — that investigation shipped its fixes and the file was
removed (`0f28ab8`). This is a fresh start: measurement of steady-state cost now that those
fixes are in, not a new diagnosis.

**Context for these numbers:** Claude Pro ($20/month) is a flat subscription with a rolling
5-hour usage-window allowance — there is no per-token bill. The dollar figures below are an
API-list-price *ruler* (what the same token volume would cost if pay-per-token), useful for
comparing which workflows are expensive relative to each other. They are not something you are
actually charged. To see your real window usage, run `/cost` in Claude Code right after a task,
and check the account's usage indicator for the % of the current 5-hour window consumed.

---

## #1 — Stage 3 USA longlist pass, wong-de-xin, 2026-09-01

**What ran:** a full country pass under `workflows/03_discover_longlist.md` — roster sweep (main
session, free `WebSearch`), one `country_usa.json` constants file, then **10 `row-filler`
subagents dispatched in parallel** (one per university), followed by
`merge_candidates.py` → `sync_shortlist.py` → `check_master_list.py` → `build_glossary_sheet.py`.
Model: Sonnet 5 (session was switched to Sonnet via `/model sonnet` before this pass; `row-filler`
is separately pinned to Sonnet in its own agent file regardless of the main session's model).

**Subagent token spend** (each figure is that row-filler's own reported total — input + output +
thinking combined, not broken out):

| University | Tokens | Tool calls | Wall-clock |
|---|---:|---:|---:|
| Boston University | 58,604 | 25 | 2m 55s |
| MIT | 63,987 | 26 | 3m 45s |
| Princeton University | 70,810 | 33 | 4m 13s |
| Northeastern University | 67,068 | 30 | 3m 50s |
| Yale University | 77,288 | 42 | 4m 41s |
| RIT | 65,909 | 31 | 4m 17s |
| Case Western Reserve | 68,617 | 30 | 4m 12s |
| Drexel University | 70,208 | 33 | 4m 22s |
| Iowa State University | 75,631 | 38 | 4m 44s |
| UC Irvine | 80,634 | 40 | 5m 19s |
| **Total (10 subagents)** | **698,756** | **328** | **~5m wall-clock (parallel)** |

Average per university: **~69,876 tokens**, ~33 tool calls. All 10 ran concurrently, so
wall-clock for the whole batch was ~5 minutes (the slowest agent), not the ~42 minutes it would
have taken serially — parallel dispatch is a wall-clock win as well as keeping 10 universities'
worth of research out of one context window.

**Not included above:** the main session's own spend for this pass — roster-sweep `WebSearch`
calls (10 queries), the country-constants file, reading `workflows/03_discover_longlist.md` +
`workflows/countries/usa.md`, the merge/sync/check/glossary tool-call cycle, and fixing the two
post-sync validation failures (one `admission_reason` over its char cap, then 21 jargon
substitutions pushing 5 cells over budget, both hand-corrected). That half isn't visible to the
main session after the fact — `/cost` immediately after the pass is the only reliable way to
capture it; it wasn't run this time.

**API-equivalent estimate (Sonnet 5, $2/MTok in · $10/MTok out):** the subagent total alone
brackets to **$1.40 (all-input) – $6.99 (all-output)**. Research-style dispatches like this skew
heavily toward input (reading pages, schema docs, workflow files) rather than output (writing one
JSON fragment each), so the real figure is closer to the low end — roughly **$2–3 equivalent**
for the row-fill step of this one country pass.

**Observed cost driver:** subagent count, not main-session work. Ten universities means ten
Sonnet conversations' worth of research; a country with a naturally smaller roster (e.g.
Singapore, expected ~3-4 universities) should cost proportionally less — worth confirming when
that pass runs, to check whether the ~69,876-token per-university average holds across countries
or is USA-specific (USA rows carry unusually heavy funding/aid research per
`workflows/countries/usa.md`, which may not generalize).

---

## Bottom line so far

One data point isn't a trend yet. The actionable next step is repeating this measurement on a
smaller-roster country (Singapore) and a country with a thinner playbook, to see whether
per-university subagent cost is roughly constant (~70k tokens) regardless of country, or scales
with how much country-specific research each row genuinely requires.
