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
   |
Session 3  Design pass           optional, after Session 2; one screen per sitting
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
comment at the top of the file. (Session 2 added `.btn-lg` and `.btn-sm`.)

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
  decision, feedback, pricing) is hand-written in the template. **Superseded by Session 2:**
  `gen.py` now skips any screen file that exists, so it only rewrites `data.js`. Edit
  `data.template.js` and re-run it; never hand-edit `data.js`.
- `smoke.js` — headless-Chrome click-through over `file://`, no dependencies (Node 24 + local
  Chrome). **Rewritten by Session 2 against the real screens** (see that section for what it
  covers); the stub version described here is gone.
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
5. **SAT: resolved 2026-10-12.** The sample CSV now says the SAT or ACT is required, so the
   downloaded spreadsheet, `data.js` and the MIT report agree. The `gen.py` override that used
   to patch MIT's `entryRequirements` is gone (`OVERRIDES = {}`).
6. **Ringgit totals: resolved 2026-10-12.** The sample pack was rebuilt at the 2026-09-05
   rates (USD 4.04) and `data.js` regenerated from it; MIT shows RM 1,499,002.

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

### Session 2 status (2026-10-10) — DONE, VERIFIED

Verified 2026-10-10: `node --check` clean on every script; `smoke.js` prints `145/145 checks
passed` (exit 0) with an empty console; screenshots of all 7 screens at 1366px and landing at
1024px reviewed by eye (`.tmp/proto-shots/session-2/`, disposable). **Not committed. Self-review
only, no independent code review.**

Steps 1-5 passed on the prototype exactly as A, B and C left it; nothing needed fixing.

Run the check: `mkdir -p .tmp/proto-shots && node prototype/_build/smoke.js . .tmp/proto-shots`
Regenerate `data.js` after editing the template:
`python prototype/_build/gen.py . prototype/_build/data.template.js`

**`_build/smoke.js` is now the integration check for the real screens.** It covers: the click
path 1 → 7 with the buttons a presenter uses (3 onboarding steps included); all 4 journey items
from all 7 screens; waiting before and after skip ahead; both download links resolve to the real
CSV and PDF on disk; cost and grades on `results` = the same rows on `list` = `DATA`; the list's
tick / expand / cut-row behaviour; the step 6 and step 7 rules below; cold opens on `#list` and
`#waiting`; an empty console. `--dump <file.json>` also writes every screen's markup in each of
its 12 states, so two dumps can be diffed to prove a refactor changed nothing on screen.

**Step 6 — where each reported constant went.** Proven by diffing dumps: all 12 states had
byte-identical markup before and after the move.

| Was | Now |
|---|---|
| `landing.js` `TIER_OF` | `DATA.deliverables[].tier` (`free` / `firstFree` / `paid`) |
| `onboarding.js` `DEMO_WHATSAPP` | `DATA.student.whatsapp` |
| `onboarding.js` `QUALIFICATIONS`, `EXTRA_COUNTRIES`, `OTHER_BUDGET_BANDS` | `DATA.intake.{qualifications, extraCountries, budgetBands}`. `budgetBands` is all three; `student.budget.band` is `budgetBands[0]`, so the placeholder is typed once |
| `results.js`, `list.js`, `decide.js` `BANDS` | `DATA.bands[]` `{key, label}` |
| `results.js`, `list.js` `place()` | `university.place` (derived per row) |
| `list.js` `GROUPS` | `DATA.columnGroups[]` |
| `report.js` `OPEN_SECTION` | `DATA.report.openSection` (section number, still found by title) |
| `decide.js` `ROUNDS` | `DATA.decision.rounds` |
| `decide.js` "one per country you apply to" | `DATA.deliverables[apply].scope` |

Ruling — five reported constants stay in their screen file, because each describes that file's
own markup and moving it would let the data and the markup fall out of step: `landing.js`
`SHORT_QUOTE` (a character threshold for card placement), `waiting.js` `PREVIEW_KEYS` (tied to
the 5 hard-coded ghost cells per row), `list.js` `HEADS` and `IN_ROW` (tied to the cell order in
`row()`), `list.js` `value()` (a formatter). Cost if wrong: five small moves.

**Step 7 — what was evened out.**

- **Buttons were five sizes (53 / 50 / 43 / 35 / 30px tall); now three named ones** in
  `styles.css`: standard, `.btn-lg` (landing "Start", onboarding "Next" / "Build my list") and
  `.btn-sm` (waiting "Skip ahead", report "Jump to section"). No screen CSS sets a button size.
- `waiting` h1 was 30.4px; now the shared 33.6px like screens 2-7. Landing's 40px headline and
  the 30.4px university name in `decide`'s navy card are deliberate and left.
- `onboarding`'s card started 12px lower than every other screen's content; now level.
- `results` had two `.btn-primary`; the one in the last tile is now `.btn-ghost`. `smoke.js`
  asserts at most one primary per screen.
- **Top bar no longer overflows at 1024px** (Session C's finding): a `max-width: 1100px` rule in
  `styles.css` tightens the journey bar. Holds down to about 940px.
- **UNSW's deadline read "Rolling" on `list` and "To confirm" on `decide`** (Session B's
  finding). `DATA.decision.deadlines[].rolling` is new; the `decide` tile says "Rolling" when
  every entry under it is rolling. The "Confirm the exact date" badge stays.

Left as they are, on purpose:

- `.screen-list` is 1300px wide against 1080px elsewhere, so the top bar's edges do not line up
  with the table. The 8-column table needs the width.
- `decide` has no `.btn-primary` (it is the end of the path).
- `results` / `report` / `decide` read the nickname from `DATA.student`; `waiting` reads what was
  typed in onboarding. They differ only if the presenter retypes the name live.
- `decide` still reformats ISO dates at render time (`withDates()`); an opened `list` row shows
  the same `keyDeadline` text raw, as the spreadsheet has it.
- Truncated sample cells (e.g. NUS `scholarshipAndPortal` = "Two realistic routes. (1)") come
  from the sample CSV outside `prototype/`.

Incident, for the record: `gen.py` was run unguarded once this session (a failed patch followed by
the generator on the next shell line) and overwrote all 14 screen files with stubs. They were
restored from git (commit `1bd2c84`) and confirmed byte-identical to a pre-session backup before
any other edit. The guard described above is the fix; it was then verified by a run that reported
"0 written, 14 existing screen files left alone".

## Session 3 — Design pass from Figma references (optional, after Session 2)

Restyle the screens using layouts from five Figma Community templates Evan picked on 2026-10-11.
**Borrow layout, not branding:** structure, spacing, density and component shapes come from the
reference; colours, fonts, wording and every number stay the prototype's own.

### Session 3 status (2026-10-12) — NOT STARTED, waiting on Evan's frame links

Nothing is built. The table below has no frame links yet; a screen cannot start until its row has
one (or a screenshot, see "Fallback").

### Evan's steps, once per template (no code needed)

1. Open the Community link in the table and click **Open in Figma**. That saves a copy to your own
   Figma account. The connector can only read files in your account, not the public gallery.
2. Click once on the one screen (Figma calls it a "frame") you like most.
3. Right-click it, choose **Copy link to selection**, and paste the link into the "Frame link"
   column below. One frame per row is enough.

### References

| Screen | Order | Reference (Community link) | Frame link (Evan pastes) |
|---|---|---|---|
| `list` | 1 | [Quick Commerce Admin Dashboard: Table & Card Views](https://www.figma.com/community/file/1592210243828177821/quick-commerce-admin-dashboard-ui-table-card-views-free-figma-template) | |
| `list` | 1 | [Figma data tables UI kit (Untitled UI)](https://www.figma.com/community/file/1332203037536263387/figma-data-tables-ui-kit-untitled-ui) | |
| `report` | 2 | [Documentation Website Template](https://www.figma.com/community/file/1504770835230036645/documentation-website-template) | |
| `landing` | 3 | [Website Pricing Tables (BRIX Templates)](https://www.figma.com/community/file/1098325138756147704/website-pricing-tables-brix-templates) | |
| `landing`, `onboarding` | 3 | [Learning Education Website: Responsive Design](https://www.figma.com/community/file/1567639061099198600/learning-education-website-responsive-design-free) | |

`results` has no reference of its own: restyle its cards after `list`, from the same card view.
`waiting` and `decide` are out of scope unless a restyled neighbour makes them look out of place.

None of the five files has been opened. "Free" and "still available" come from search listings
only; confirm on the listing when the file is copied.

### Figma access (checked 2026-10-11)

- Connector `plugin:figma:figma` is signed in as handle "Evan", team "Evan's Cave", **View seat,
  Starter tier**. If its tools are missing in a new session: `/mcp` → figma → authenticate.
- **Assume a very small monthly call allowance** (believed to be about 6 tool calls a month at
  this seat level; not confirmed). Check
  https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/ before the first call and
  write the real figure here.
- Spend calls on `get_design_context` for the linked frame only (it returns the layout, the
  values and a screenshot together). No exploratory `get_metadata` / `get_screenshot` calls, no
  re-reading a frame already read. Save what comes back to `.tmp/proto-refs/<screen>/` so a later
  sitting never pays for the same frame twice.
- Before the first call: invoke the `figma:figma-design-to-code` skill, then `create_session` with
  the file key (both are required by the connector).
- The connector cannot search or browse Figma Community. New references are found by web search.

**Fallback (no allowance left, or a file will not copy):** Evan saves plain screenshots of the
frame to `.tmp/proto-refs/<screen>/`. Rebuild from the picture. Spacing is then by eye, not
measured.

### Rules (on top of "Rules for every session", which all still apply)

- **The connector's code draft is React + Tailwind. Never paste it.** Use it as a measurement
  sheet and write plain HTML/CSS in the existing `render()` functions.
- **Poster tokens stay.** No new colour or font. If a reference needs a value the tokens lack
  (a row height, a shadow, a radius), add it as a named token in `styles.css` and list it in that
  file's header comment.
- **No web fonts, no icon libraries.** Any image or icon taken from a reference is saved under
  `prototype/assets/` (create it) and linked by relative path, so `file://` still works.
- **Reference content is never copied.** Template text and sample data (shop orders, prices) stay
  out; every value on screen still comes from `window.DATA`.
- **One screen per sitting, in the table's order.** Each screen is finished and checked before the
  next starts, so the prototype is demo-ready after any sitting.
- Screen CSS keeps the `.screen-<id>` prefix. A style wanted by two screens goes in `styles.css`
  as a shared class.
- **Behaviour does not change.** Everything under "Behaviour Session 2 should know" in sections
  A, B and C still holds (tick order in `state.picked`, cut rows cannot be ticked, the two states
  of `waiting`, at most one `.btn-primary` per screen, and so on).

### What to take from each reference (confirm against the frame; these are from listings)

- **`list`** — the table/card switch from Quick Commerce (new state key, e.g. `state.listView`,
  default table); row density, header and status-badge treatment from Untitled UI. The expanded
  row, tick boxes and the sticky bar keep their behaviour.
- **`report`** — the docs template's side menu for the 15 `DATA.report.sections` plus an "on this
  page" list. The "Jump to section" control must stay a `scrollIntoView` listener, not an anchor
  link: `app.js` routes on the hash.
- **`landing`** — side-by-side tier cards from the pricing template for free / first report free
  / paid, driven by `DATA.deliverables[].tier` and `DATA.pricing`. Must still cope with
  `pricePerReport: null`. Hero and section rhythm from the education template.
- **`onboarding`** — step layout only, from the education template, if it has one worth taking.

### Done when (per screen)

1. `node --check` clean on the screen's script.
2. `mkdir -p .tmp/proto-shots && node prototype/_build/smoke.js . .tmp/proto-shots` exits 0 with
   an empty console. Markup will change, so a check tied to the old markup may fail: **rewrite
   that check to assert the same behaviour on the new markup; never delete it.** Record the new
   total here (it is 145 before Session 3).
3. Screenshots at 1366px and 1024px reviewed by eye; no sideways scroll at either.
4. The screen still reads as the same product as the screens not yet restyled.

### Credits

Several of these files are CC BY 4.0 (free to use with credit to the creator); BRIX has its own
licence on its listing. For each reference actually used, add a line here with the file name,
creator and licence, and the same line in the header comment of the screen's CSS file.

| Reference used | Creator | Licence | Screen |
|---|---|---|---|
| | | | |
