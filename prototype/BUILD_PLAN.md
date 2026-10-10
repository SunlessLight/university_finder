# Prototype build plan — split by session

Clickable skeleton for an accelerator demo. Presenter-only, laptop, one fixed path. No backend, no
login, no build step: `prototype/index.html` opens by double-click (`file://`). The plan is approved.
**Do not re-plan or brainstorm; read your session's section and build.**

Each session reads this file, does **only its own section**, and edits **only the files it owns**.

## Order

```
Session 1  Foundation            alone, first (blocks everything)
   |
   +-- Session A  Sign-up side   screens 1-3  \
   +-- Session B  List side      screens 4-5   >  in parallel, after Session 1 is done
   +-- Session C  Report side    screens 6-7  /
   |
Session 2  Integration check     alone, last
```

A, B and C never touch the same file, so they can run at the same time. If time is short, C is the
one to drop: its stub screens from Session 1 still click through.

## Rules for every session

- Works from `file://`: plain `<script src>` tags only. No `fetch`, no `type="module"`, no
  libraries, no CDN links.
- Anything shown on more than one screen (names, costs, grades, prices, dates) comes from
  `window.DATA`. Never retype a number in a screen file.
- Only the anonymised sample student ("Arif") is used. Sources: `business/sales/sample_pack/`,
  `business/*.md`, the poster HTML. **Never read `data/students/` or `data/feedback/`.**
- No "every fee checked" claim. Per-row "Checked on official page" badge, driven by the row's
  `infoSource`. Feedback is labelled "early testers".
- Nothing outside `prototype/` is edited.
- Layout, spacing and wording inside a screen are free.

## The contract (Session 1 builds it; A, B, C build against it)

**Files**

| File | Owner |
|---|---|
| `index.html`, `styles.css`, `data.js`, `app.js`, `_build/` | Session 1. Read-only for A, B, C |
| `screens/landing.{js,css}`, `screens/onboarding.{js,css}`, `screens/waiting.{js,css}` | Session A |
| `screens/results.{js,css}`, `screens/list.{js,css}` | Session B |
| `screens/report.{js,css}`, `screens/decide.{js,css}` | Session C |

**Script order in `index.html`:** `data.js`, `app.js`, the 7 `screens/*.js`, then `App.start()`.
All 7 screen CSS files are linked in `<head>` after `styles.css`.

**`app.js`**

- `App.register(id, { render(root, state, data) })` — `render` fills `root` (sets `innerHTML`,
  attaches any listeners). Called again on every state change.
- `App.go(id)` — show a screen, scroll to top, update the journey bar.
- `App.setState(patch)` — merge into `App.state` and re-render the current screen.
- `App.state` — `{ ready: false, onboardingStep: 1, picked: [] }` (`picked` = university ids ticked
  for a deep report).
- Any element with `data-go="<id>"` navigates on click (handled once, globally). Prefer this over
  per-screen click handlers.
- Journey bar: Sign up (`landing`, `onboarding`, `waiting`) → Your list (`results`, `list`) →
  Reports (`report`) → Decide and apply (`decide`). Clicking "Your list" while `state.ready` is
  false goes to `waiting`.
- Each screen's root element gets class `screen-<id>`.

**`data.js`** — `window.DATA`:

- `student` — nickname, qualification, grades, course, countries, budget, scholarship needed.
- `universities[]` — every row of `sample_master_list.csv`, camelCase keys, plus a stable `id`.
  Keep all 35 columns (the list screen expands to show the rest).
- `top5` — ids for the results cards, a Reach/Match/Safety spread, not top five by score.
- `findings[]` — 3-4 one-line "what we found" statements derived from the rows.
- `report` — MIT: summary block, section list, why here / why hesitate.
- `decision` — recommended university id, deadline list (from the rows' `keyDeadline`), apply steps.
- `feedback` — ratings and quotes exactly as printed on the poster.
- `pricing` — free vs paid wording from `business/sales/service-tiers.md`.
- `files` — `../business/sales/sample_pack/sample_master_list.csv` and
  `../business/sales/sample_pack/sample_university-report_MIT.pdf`.

**`styles.css`** — tokens from the poster
(`business/sales/pitch/university-research-service-poster.html`, lines 20-51): `--navy #10233f`,
`--ink #1a1a1a`, `--gray #5b6b7f`, `--line #d7dee7`, `--wash #f4f6f9`, `--accent #1157b8`,
`--gold #b07407`, `--free #17784a`, `--freewash #eaf6ef`; Georgia headings, Segoe UI body.
Shared classes: `.btn`, `.btn-primary`, `.btn-ghost`, `.card`, `.grid`, `.badge`, `.badge-reach`,
`.badge-match`, `.badge-safety`, `.badge-verified`, `.section-title`, `.muted`. List them in a
comment at the top of the file.

**Screen CSS:** every selector starts with `.screen-<id>`, so one session's styles cannot leak into
another's screen. Use the shared classes and tokens before inventing new ones.

**If the contract is missing something:** do not edit a Session 1 file. Keep a screen-only constant
inside your own screen file and name it in your final message so Session 2 can move it.

---

## Session 1 — Foundation (alone, first)

Build `index.html`, `styles.css`, `data.js`, `app.js` to the contract, plus all 14 `screens/` files
as stubs: each stub registers its screen with a heading, one line saying what will go there, and a
`data-go` button to the next screen (`waiting` gets the "skip ahead" control that sets
`ready: true` and goes to `results`).

Sources: `sample_master_list.csv` (rows), the poster HTML (tokens, quotes, ratings),
`business/university_report.md` § "What is inside a report" (report sections),
`business/decide_report.md` and `business/apply_guide_report.md` (decision and apply outline),
`business/sales/service-tiers.md` (pricing wording).

Done when: `index.html` opens by double-click, all 7 screens click through in order, the journey
bar jumps between them, and the browser console is empty.

### Session 1 status (2026-10-10) — DONE, VERIFIED

**A, B and C may start.** Verified 2026-10-10: `node --check` clean on `data.js`, `app.js` and the
7 screen scripts; `smoke.js` prints `64/64 checks passed` (exit 0); the three screenshots show the
journey bar and stub card styled.

Written: `index.html`, `styles.css`, `app.js` (by hand); `data.js` and the 14 `screens/` stubs
(by `_build/gen.py`). None of them needed a change during verification.

`_build/` (Session 1's, read-only for A, B, C; not loaded by `index.html`):

- `gen.py` + `data.template.js` — `data.js` is the template with three blocks injected: the 35
  columns and 15 rows from `sample_master_list.csv`, and the 15 report sections parsed from
  `business/university_report.md`. Everything else in `data.js` (student, findings, report,
  decision, feedback, pricing) is hand-written in the template. **Re-running `gen.py` overwrites
  `data.js` and all 14 stubs**, so never run it now that A, B and C are cleared to start. Edit
  `data.js` directly.
- `smoke.js` — headless-Chrome click-through over `file://`, no dependencies (Node 24 + local
  Chrome). Asserts the stub click path, journey bar, `setState`, hash routing, the data contract,
  and an empty console. Written against the **stubs** (clicks the first `[data-go]` on each
  screen), so it stops being valid once real screens land.
  Run: `mkdir -p .tmp/proto-shots && node prototype/_build/smoke.js . .tmp/proto-shots`

Two bugs fixed in `smoke.js` itself during verification (the prototype was fine both times):

- **It hung forever on its last step.** `Page.navigate` from `index.html#report` to
  `index.html#list` is a hash-only change, which fires no load event. It now goes via
  `about:blank`, and `open()` throws after 10 s instead of waiting.
- **The stylesheet check could not pass under `file://`.** Each stylesheet is cross-origin to the
  page there, so `.cssRules` throws even when loaded, and `link.sheet` is set even for a missing
  file. The check now reads a `styles.css` token (`--navy`); a missing screen stylesheet is caught
  by the empty-console check (`ERR_FILE_NOT_FOUND`). Both were confirmed by hiding a file and
  watching the run fail.

If a run is ever killed mid-way, a headless Chrome may be left holding port 9347: end the
`chrome.exe` whose command line contains `proto-smoke` before re-running.

Additions beyond the contract (documented in each file's header comment; A, B, C may use them):

- `DATA.brand`, `DATA.columns` (`{key,label}` × 35, for the list screen's expanded view),
  `DATA.deliverables` (the three products, for landing).
- Each university also has `shortName`, `band` (`reach|match|safety` → `.badge-<band>`),
  `verified` (from `infoSource`), `deadlineDate` (first ISO date in `keyDeadline`, or null).
- `App.esc`, `App.uni(id)`, `App.fmt.myr / myrShort / date`, `App.current`.
- `index.html#<id>` opens straight on a screen (and sets `ready` for screens after `waiting`).
- `render` gets a **fresh root element on every call**, already attached. UI state that must
  survive a re-render goes in `App.state` via `setState` (extra keys are fine).
- `.badge-unverified` for rows where `verified` is false.

Flags — all settled by Evan on 2026-10-10. A, B, C: build on these, do not re-raise them.

1. **Recommendation is composed, not copied: accepted.** `DATA.decision` (MIT first, then
   Princeton, Harvard, NUS, NTU, UNSW; apply steps; open risks) was written by Session 1 from the
   sample rows and the MIT report. Fine for a prototype.
2. **Budget stays a placeholder** ("Under RM 500,000" in `DATA.student.budget`). Evan will review
   the wording himself; read it from `DATA`, never retype it.
3. **No price yet.** `DATA.pricing.pricePerReport` stays `null` until Evan picks one. Screens show
   "first report free, then paid" and must cope with `null` (no "RM null").
4. **15 sections.** `DATA.report.sections` is the current 15-section list and is what the report
   screen shows. The downloadable sample MIT PDF is the older 16-section layout; leave it.
5. **SAT: the MIT report wins, the spreadsheet is outdated.** MIT's `entryRequirements` in
   `data.js` now says "SAT or ACT required" (an override in `gen.py`, so a re-run keeps it). The
   sample CSV outside `prototype/` still says "optional-ish", so the downloaded spreadsheet does too.
6. **Ringgit totals stay as they are.** They come from an old exchange rate (MIT shows
   RM 1,743,888); for a prototype the exact numbers do not matter.

## Session A — Sign-up side (parallel)

- **`landing`** — one-line pitch, the three deliverables (List, Report, Apply Guide),
  `DATA.feedback` labelled "early testers", one primary button "Start, 2 minutes" → `onboarding`.
- **`onboarding`** — 3 steps with a progress bar, driven by `state.onboardingStep`: about you /
  what you want / money. Inputs pre-filled from `DATA.student` so the demo needs no typing. Last
  step → `waiting`. It should feel lighter than a form: few fields per step, big tap targets.
- **`waiting`** — "We're building your list": progress steps, "we'll WhatsApp you when it's
  ready", a preview of what is coming so the page is not empty. Keep the small "skip ahead"
  control from the stub.

### Session A status (2026-10-10) — DONE, VERIFIED

Written: `screens/landing.{js,css}`, `screens/onboarding.{js,css}`, `screens/waiting.{js,css}`.
No Session 1 file was touched.

Verified 2026-10-10: `node --check` clean on the three scripts; a headless-Chrome click-through
over `file://` passed 70/70 with an empty console (landing → 3 onboarding steps → waiting → skip
ahead → results; cold opens on `#onboarding` and `#waiting`; no overflow at 420px; every selector
starts with `.screen-<id>`). That script was a throwaway and is **not in the repo**; screenshots
are in `.tmp/proto-shots/session-a/` (disposable). Not committed, no independent code review.

Screen-only constants for Session 2 step 6 (all placeholder choices, none are facts about Arif):

| File | Constant | What it is |
|---|---|---|
| `landing.js` | `TIER_OF` | deliverable → free / first-free / paid. The words come from `DATA.pricing` |
| `landing.js` | `SHORT_QUOTE` | layout only: quotes under 120 chars sit under their score card |
| `onboarding.js` | `DEMO_WHATSAPP` | made-up phone number `012-345 6789` |
| `onboarding.js` | `QUALIFICATIONS` | A-Levels, STPM, IB, UEC, Foundation |
| `onboarding.js` | `EXTRA_COUNTRIES` | Hong Kong, Germany, Taiwan (offered, not ticked) |
| `onboarding.js` | `OTHER_BUDGET_BANDS` | the intake form's other two bands; the selected one is `DATA.student.budget.band` |
| `waiting.js` | `PREVIEW_KEYS` | the five columns in the ghost table. Labels come from `DATA.columns` |

Behaviour Session 2 should know:

- **`state.onboardingForm`** (extra state key) holds what was typed or ticked in onboarding. Inputs
  and chips update it in place without a re-render; only a step change calls `setState`.
- **`waiting` reads `state.onboardingForm`** (nickname, WhatsApp number, course, countries) and
  falls back to `DATA.student`. If `results` reads the nickname from `DATA.student`, the two only
  differ when the presenter retypes the name live.
- **`waiting` has two states.** Not ready: `[data-skip]`, no `[data-go]`. Ready: no `[data-skip]`,
  one `[data-go="results"]` ("See your list").
- **The landing "Start" button resets `onboardingStep` to 1**, so a second demo run never opens on
  step 3.
- **Onboarding step 1 has no Back button and no `[data-go]`**; the only `[data-go]` on that screen
  is "Build my list" on step 3. `_build/smoke.js` clicks the first `[data-go]` on each screen, so
  it should now stop at onboarding step 1, as the plan expected. Not re-run by Session A (it shares
  port 9347 with whatever B and C are running).

## Session B — List side (parallel)

- **`results`** — the "welcome back" page. `DATA.top5` as cards: Reach/Match/Safety badge, total
  cost in ringgit, grades vs entry bar, verified badge. `DATA.findings` as a short summary.
  Download-spreadsheet button (`DATA.files`). Button → `list`.
- **`list`** — table of all universities with the key columns (university, course, likelihood,
  grades vs bar, total MYR, deadline, verified). Click a row to expand the remaining columns. Tick
  boxes write to `state.picked`; a bar shows the count and `DATA.pricing` (first report free, then
  paid) with a button → `report`.

### Session B status (2026-10-10) — DONE, VERIFIED

Written: `screens/results.{js,css}`, `screens/list.{js,css}`. No Session 1 file was touched.

Verified 2026-10-10: `node --check` clean on both scripts; a headless-Chrome run over `file://`
passed 52/52 with an empty console (written first and watched fail against the stubs). It covers:
results cards = `DATA.top5` with costs/grades/badges from the rows; findings = `DATA.findings`;
download link = `DATA.files.list` and the file exists; results → list → report; cost and grade
figures on results equal the same rows on list (Session 2 step 5); row expand/collapse; all 35
columns reachable on every row once open; ticking, unticking, tick order, scroll and focus kept;
bar tallies with `pricePerReport` null and with a price set; no overflow at 1366px; every selector
starts with `.screen-<id>`. That script was a throwaway and is **not in the repo**; screenshots
were reviewed by eye and are also not kept. Not committed, no independent code review.

`_build/smoke.js` re-run after A, B and C landed: it stops at onboarding step 1 (no `[data-go]`),
exactly as Session A's note predicts. Not a fault in any screen. `results` and `list` still fit
its shape (an `h1`, a `p.muted`, first `[data-go]` → the next screen).

Screen-only constants for Session 2 step 6 (layout and labels; no number or fact about Arif):

| File | Constant | What it is |
|---|---|---|
| `results.js`, `list.js` | `BANDS` | band → label for the "8 Reach / 3 Match / 4 Safety" count badges. Same in both files |
| `results.js`, `list.js` | `place()` | "City · Country", shown once for a city-state (Singapore). Same in both files |
| `list.js` | `HEADS` | the 8 table headings |
| `list.js` | `IN_ROW` | columns the collapsed row already shows, so the detail panel skips them |
| `list.js` | `GROUPS` | how the detail panel groups the other columns. Labels and values come from `DATA.columns`; a column not named there falls into "Good to know" |
| `list.js` | `value()` | shows `desirability` as "89 / 100" and `courseUrl` as a new-tab link |

Behaviour Session 2 should know:

- **`state.listOpen`** (extra state key) = ids of expanded rows. Unset until the first row is
  opened; the screen treats unset as empty. It and `state.picked` survive leaving and returning.
- **`state.picked` is in tick order**, not table order. The first one ticked is the free one.
- **Rows with `listStatus` "Rejected" (CMU) cannot be ticked.** The box is disabled and the row
  says "Cut from your list. Open the row to see why."; the open row shows `warnings` in a callout.
- **The bar's button always goes to `report`.** Nothing ticked: ghost button "See the sample
  report". One or more: primary "Get my report" / "Get my N reports". The report screen shows MIT
  whatever is ticked, so the row whose id is `DATA.report.universityId` carries a "Sample report
  ready" label to steer the presenter.
- **`results` reads the nickname from `DATA.student`**, not `state.onboardingForm`, so it differs
  from `waiting` only if the presenter retypes the name live (see Session A's note).
- **Verified wording differs by screen on purpose.** Results cards: "Checked on official page".
  List table: "Checked" under an "Official page" heading (width), full wording in the `title`.
- **Deadline cell.** `App.fmt.date(deadlineDate)`; "approx." only when the note is about that
  first date (`~` directly before it, or "(approx" directly after), so Oxford's firm UCAS date is
  not marked approximate by the `~` on its ESAT date. No date and a "Rolling…" cell shows
  "Rolling" (UNSW, Monash, Melbourne); `DATA.decision.deadlines` gives UNSW a null date, so
  `decide` may say "To confirm" for the same row.

For step 7 (evening out):

- `.screen-list` overrides the column to `max-width: 1300px` for the 8-column table; the other
  screens use `--maxw` (1080px).
- `results` has two primary buttons, both "See the full list" (top of page and the last tile).
- The list's bar is `position: sticky; bottom: 16px; z-index: 5` (the top bar is `z-index: 10`).

Data, not code (Session B could not edit it): several sample cells end mid-sentence because the
spreadsheet's cell budget cut them, e.g. NUS `scholarshipAndPortal` = "Two realistic routes. (1)".
They show when that row is opened in front of an audience.

## Session C — Report side (parallel)

- **`report`** — MIT from `DATA.report`: one-page summary first, then the section list with
  "why here / why hesitate" shown in full. Download-PDF button (`DATA.files`). Button → `decide`.
- **`decide`** — the end goal: recommended university, deadline calendar, apply steps, all from
  `DATA.decision`.

### Session C status (2026-10-10) — DONE, VERIFIED

Written: `screens/report.{js,css}`, `screens/decide.{js,css}`. No Session 1 file was touched.

Verified 2026-10-10: `node --check` clean on both scripts; a headless-Chrome run over `file://`
passed 44/44 with an empty console (cold open on `#report`; every `DATA.report` summary row,
question, section and why-here / why-hesitate item on screen; PDF link resolves to a file on disk;
report → decide → report and decide → landing; every `DATA.decision` plan row, deadline, apply step
and open risk on screen; no raw ISO date, `undefined`, `null` or `RM null` in either screen's text;
no sideways scroll at 1366; every selector starts with `.screen-<id>`; no run of 3+ digits in
either script). That script and its screenshots were throwaways in the session scratchpad and are
**not in the repo**. Not committed, no independent code review.

Screen-only constants for Session 2 step 6 (all display labels or matchers, none hold data):

| File | Constant | What it is |
|---|---|---|
| `report.js` | `OPEN_SECTION` | `/why here/i`: picks the one `DATA.report.sections` row shown in full, by title, not by number |
| `decide.js` | `BANDS` | band key → label ("Reach", "Match", "Safety") for the balance badges |
| `decide.js` | `ROUNDS` | `plan[].round` → label ("Early round", "Regular round") |

Behaviour Session 2 should know:

- **`report` always shows `DATA.report` (MIT)**, whatever is in `state.picked`. If `picked` holds
  other ids, the "first report is free" strip also names them ("You also ticked NUS and NTU…").
  The strip's wording is `DATA.pricing.reportRule.text`; no price is shown.
- **`report` has one `.btn-primary`** (`[data-go="decide"]`, in the closing card at the bottom)
  and a `[data-go="list"]` before it in the DOM. The PDF link is a plain `<a target="_blank">` in
  the header. "Jump to section 14" is the only per-screen click listener (`scrollIntoView`); it
  deliberately does not use an anchor link, because `app.js` routes on the hash.
- **`decide` has no `.btn-primary`.** Its `[data-go]`, in DOM order: `report` (in the navy
  recommendation card), `list`, `landing`. `_build/smoke.js` ends by clicking the first `[data-go]`
  on `decide` and expecting `landing`, so that step now fails, as the plan expected. Not re-run by
  Session C.
- **`decide` reformats dates at render time.** `DATA.decision.deadlines[].text` and
  `applySteps[].detail` carry `YYYY-MM-DD` inside sentences; `withDates()` passes each through
  `App.fmt.date`. If Session 2 wants that fixed at the source, it belongs in `data.js`.
- **Deadlines are grouped by `date`**, one tile per date; `date: null` (UNSW) renders the
  `App.fmt.date(null)` text "To confirm". Every entry with `confirmed: false` gets a
  `.badge-unverified` "Confirm the exact date".
- **One sentence is not from `DATA`:** the Apply Guide card on `decide` says the guide is "one per
  country you apply to" (from `business/sales/service-tiers.md`). The guide's name, one-liner and
  "Paid" label are from `DATA.deliverables` and `DATA.pricing.paid.label`.

Found outside Session C's files, left alone:

- **The top bar overflows at 1024px wide on every screen.** `.demo-chip` ends at x=1034 against a
  1009px viewport, so the page scrolls sideways. Fine at 1366. It is in Session 1's `styles.css`;
  a candidate for Session 2 step 7.

## Session 2 — Integration check (alone, last)

1. Open `index.html` in Chrome; click the full path 1 → 7 and every journey-bar item.
2. Console is empty.
3. "Skip ahead" flips waiting to ready; "Your list" before that goes to `waiting`.
4. Both download buttons open the real sample files.
5. Cost and grade figures on `results` match the same universities on `list`.
6. Move any screen-only constants that A, B or C reported into `data.js`.
7. Even out anything that looks inconsistent between the three sides (button sizes, heading
   sizes, spacing). Fix, don't redesign.
