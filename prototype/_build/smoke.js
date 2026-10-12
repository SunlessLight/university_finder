// Integration check (Session 2): opens prototype/index.html from file:// in headless Chrome over
// the DevTools protocol, clicks the real path through all 7 screens, and fails on any console
// output. No dependencies (Node 24 + local Chrome).
//
// usage: node smoke.js <repo_root> <screenshot_dir> [--dump <file.json>]
//   --dump  also writes the markup of every screen (in each of its states) plus a few style
//           measurements. Diff two dumps to prove a refactor changed nothing on screen.
//
// If a run is killed mid-way, a headless Chrome may be left holding port 9347: end the chrome.exe
// whose command line contains "proto-smoke" before re-running.
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { pathToFileURL, fileURLToPath } = require('url');

const repo = process.argv[2];
const shots = process.argv[3];
const dumpAt = process.argv.indexOf('--dump');
const dumpFile = dumpAt === -1 ? null : process.argv[dumpAt + 1];
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9347;
const proto = path.join(repo, 'prototype');
const page = pathToFileURL(path.join(proto, 'index.html')).href;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const ORDER = ['landing', 'onboarding', 'waiting', 'results', 'list', 'report', 'decide'];
const WIDE = 1366;     // the demo laptop
const NARROW = 1024;   // a projector, or a browser window that is not maximised

const results = [];
const check = (name, ok, detail) => results.push({ name, ok: !!ok, detail });

(async () => {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'proto-smoke-'));
  const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT,
    '--remote-allow-origins=*', '--user-data-dir=' + profile, '--no-first-run',
    '--window-size=' + WIDE + ',768', 'about:blank'], { stdio: 'ignore' });
  let exit = 1;
  try {
    let target = null;
    for (let i = 0; i < 50 && !target; i++) {
      await sleep(200);
      try {
        const list = await (await fetch('http://127.0.0.1:' + PORT + '/json/list')).json();
        target = list.find((t) => t.type === 'page');
      } catch (e) { /* not up yet */ }
    }
    if (!target) throw new Error('Chrome did not start');

    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
    let seq = 0;
    const pending = new Map();
    const consoleOut = [];
    let loaded = null;
    ws.onmessage = (m) => {
      const msg = JSON.parse(m.data);
      if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); return; }
      if (msg.method === 'Runtime.consoleAPICalled') {
        consoleOut.push(msg.params.type + ': ' + msg.params.args.map((a) => a.value || a.description).join(' '));
      } else if (msg.method === 'Runtime.exceptionThrown') {
        const d = msg.params.exceptionDetails;
        consoleOut.push('exception: ' + ((d.exception && d.exception.description) || d.text));
      } else if (msg.method === 'Log.entryAdded') {
        consoleOut.push('log ' + msg.params.entry.level + ': ' + msg.params.entry.text + ' ' + (msg.params.entry.url || ''));
      } else if (msg.method === 'Page.loadEventFired' && loaded) { loaded(); }
    };
    const send = (method, params) => new Promise((res) => {
      const id = ++seq; pending.set(id, res); ws.send(JSON.stringify({ id, method, params: params || {} }));
    });
    const ev = async (expression) => {
      const r = await send('Runtime.evaluate', { expression, returnByValue: true });
      if (r.result.exceptionDetails) throw new Error('eval failed: ' + expression + ' :: ' + JSON.stringify(r.result.exceptionDetails.exception));
      return r.result.result.value;
    };
    const open = async (url) => {
      const done = new Promise((r) => { loaded = r; });
      await send('Page.navigate', { url });
      // a navigation that never fires a load event must fail the run, not hang it
      await Promise.race([done, sleep(10000).then(() => { throw new Error('no load event within 10s: ' + url); })]);
      await sleep(150);
    };
    // A hash-only change fires no load event, so a cold open always goes via about:blank.
    const coldOpen = async (hash) => { await open('about:blank'); await open(page + (hash ? '#' + hash : '')); };
    const width = (w) => send('Emulation.setDeviceMetricsOverride', { width: w, height: 768, deviceScaleFactor: 1, mobile: false });
    const shot = async (name) => {
      const r = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
      fs.writeFileSync(path.join(shots, name + '.png'), Buffer.from(r.result.data, 'base64'));
    };
    const click = async (sel) => {
      const found = await ev('(() => { const el = document.querySelector(' + JSON.stringify(sel) + '); if (el) el.click(); return !!el; })()');
      if (!found) throw new Error('nothing to click: ' + sel);
    };
    const cur = () => ev('App.current');
    const count = (sel) => ev('document.querySelectorAll(' + JSON.stringify(sel) + ').length');
    const text = (sel) => ev('(() => { const el = document.querySelector(' + JSON.stringify(sel) + '); return el ? el.innerText.trim() : null; })()');
    const overflows = () => ev('document.documentElement.scrollWidth > document.documentElement.clientWidth');

    // Things every screen must satisfy, whatever is on it.
    const onScreen = async (id, label) => {
      const where = label || id;
      check(where + ': is the current screen', (await cur()) === id, await cur());
      check(where + ': has exactly one h1', (await count('.screen-' + id + ' h1')) === 1);
      check(where + ': journey bar marks one current step', (await count('.journey-step.is-current')) === 1);
      const leak = await ev('(document.querySelector("#app").innerText.match(/undefined|NaN|RM null|\\[object|\\bnull\\b/) || [null])[0]');
      check(where + ': no undefined / null / NaN on screen', leak === null, leak);
      check(where + ': no sideways scroll at ' + WIDE + 'px', !(await overflows()));
      check(where + ': at most one primary button', (await count('#app .btn-primary')) <= 1, await count('#app .btn-primary'));
    };

    await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');
    await width(WIDE);

    // --- A. open by file:// and check the start state
    await open(page);
    check('opens from file://', page.startsWith('file:///'), page);
    check('starts on landing', (await cur()) === 'landing', await cur());
    check('root gets class screen-landing',
      (await ev('document.querySelector("#app > div").className')) === 'screen screen-landing');
    check('state starts as contract says',
      (await ev('JSON.stringify(App.state)')) === '{"ready":false,"onboardingStep":1,"picked":[]}',
      await ev('JSON.stringify(App.state)'));
    check('journey bar has 4 steps', (await count('[data-journey]')) === 4);
    // Under file:// a stylesheet's rules are unreadable (cross-origin) and link.sheet is set even
    // for a missing file, so neither proves a load. styles.css is proven by one of its tokens; a
    // missing screen stylesheet is caught by the empty-console check (ERR_FILE_NOT_FOUND).
    const navy = await ev('getComputedStyle(document.documentElement).getPropertyValue("--navy").trim()');
    check('8 stylesheet links, styles.css applied', (await count('link[rel="stylesheet"]')) === 8 && navy === '#10233f', navy);

    // --- B. plan step 3, first half: "Your list" before the list is ready goes to waiting
    await click('[data-journey="1"]');
    check('"Your list" before ready -> waiting', (await cur()) === 'waiting', await cur());
    check('ready is still false', (await ev('App.state.ready')) === false);
    await ev('App.go("landing")');

    // --- C. plan step 1: click the whole path 1 -> 7 with the buttons a presenter would use
    await onScreen('landing');
    await shot('1-landing');
    await click('.screen-landing [data-go="onboarding"]');
    for (let step = 1; step <= 3; step++) {
      await onScreen('onboarding', 'onboarding step ' + step);
      check('onboarding shows step ' + step, (await ev('App.state.onboardingStep')) === step, await ev('App.state.onboardingStep'));
      if (step === 1) await shot('2-onboarding');
      await click('.screen-onboarding .ob-next');
    }
    await onScreen('waiting', 'waiting (building)');
    check('waiting (building): skip control, no way forward yet',
      (await count('#app [data-skip]')) === 1 && (await count('#app [data-go]')) === 0);
    await shot('3-waiting');
    await click('#app [data-skip]');
    check('skip ahead sets ready', (await ev('App.state.ready')) === true);
    await onScreen('results');
    check('scrolled to top on results', (await ev('window.scrollY')) === 0);
    await shot('4-results');
    await click('.screen-results [data-go="list"]');
    await onScreen('list');
    await shot('5-list');
    await click('.screen-list [data-pickbar] [data-go="report"]');
    await onScreen('report');
    await shot('6-report');
    await click('.screen-report [data-go="decide"]');
    await onScreen('decide');
    check('scrolled to top on decide', (await ev('window.scrollY')) === 0);
    await shot('7-decide');
    await click('.screen-decide [data-go="landing"]');
    check('decide -> back to the start', (await cur()) === 'landing', await cur());

    // --- D. plan step 3, second half: after skip ahead, waiting says "ready" and "Your list" opens the list
    await ev('App.go("waiting")');
    await onScreen('waiting', 'waiting (ready)');
    check('waiting (ready): no skip control, one button to results',
      (await count('#app [data-skip]')) === 0 && (await count('#app [data-go="results"]')) === 1);
    await click('#app [data-go="results"]');
    check('waiting (ready) -> results', (await cur()) === 'results', await cur());

    // --- E. plan step 1: every journey-bar item, from every screen
    const jumps = ['landing', 'results', 'report', 'decide'];
    let jumpsOk = true;
    let jumpDetail = '';
    for (const from of ORDER) {
      for (let i = 0; i < jumps.length; i++) {
        await ev('App.go(' + JSON.stringify(from) + ')');
        await click('[data-journey="' + i + '"]');
        const marked = await ev('document.querySelector(\'[data-journey="' + i + '"]\').classList.contains("is-current")');
        if ((await cur()) !== jumps[i] || !marked) { jumpsOk = false; jumpDetail += from + '->' + i + ' gave ' + (await cur()) + '; '; }
      }
    }
    check('journey bar: all 4 items work from all 7 screens (28 jumps)', jumpsOk, jumpDetail);
    await ev('App.go("decide")');
    await click('.brand');
    check('brand link -> landing', (await cur()) === 'landing');

    // --- F. plan step 4: both download buttons point at the real sample files
    const fileOf = async (id, sel) => {
      await ev('App.go(' + JSON.stringify(id) + ')');
      return JSON.parse(await ev('(() => { const a = document.querySelector(' + JSON.stringify(sel) + ');' +
        ' return JSON.stringify(a ? { href: a.href, download: a.hasAttribute("download"), target: a.target, label: a.innerText.trim() } : null); })()'));
    };
    const head = (link, bytes) => {
      const file = fileURLToPath(link.href);
      if (!fs.existsSync(file) || fs.statSync(file).size === 0) return null;
      return fs.readFileSync(file).subarray(0, bytes).toString('latin1');
    };
    const csvLinks = [await fileOf('results', '.screen-results a[download]'), await fileOf('list', '.screen-list a[download]')];
    csvLinks.forEach((link, i) => {
      const where = i ? 'list' : 'results';
      check(where + ': spreadsheet button exists and downloads', !!link && link.download, JSON.stringify(link));
      const start = link ? head(link, 200) : null;
      check(where + ': spreadsheet button opens the real sample CSV', !!start && /List status/.test(start) && /University/.test(start), start && start.slice(0, 60));
    });
    const pdfLink = await fileOf('report', '.screen-report .rp-actions a');
    check('report: PDF button exists and opens in a new tab', !!pdfLink && pdfLink.target === '_blank', JSON.stringify(pdfLink));
    const pdfStart = pdfLink ? head(pdfLink, 5) : null;
    check('report: PDF button opens the real sample PDF', pdfStart === '%PDF-', pdfStart);
    check('download buttons use the labels and paths in DATA.files',
      !!csvLinks[0] && !!pdfLink && csvLinks[0].label === (await ev('DATA.files.list.label')) && pdfLink.label === (await ev('DATA.files.report.label')) &&
      csvLinks[0].href === new URL(await ev('DATA.files.list.href'), page).href && pdfLink.href === new URL(await ev('DATA.files.report.href'), page).href);

    // --- G. plan step 5: cost and grade figures on results match the same universities on list
    const figures = (id) => ev('(() => { App.go(' + JSON.stringify(id) + '); const out = {};' +
      ' document.querySelectorAll(' + JSON.stringify(id === 'results' ? '[data-card]' : '[data-row]') + ').forEach((el) => {' +
      ' out[el.getAttribute(' + JSON.stringify(id === 'results' ? 'data-card' : 'data-row') + ')] =' +
      ' el.querySelector("[data-cost]").innerText.trim() + " | " + el.querySelector("[data-grades]").innerText.trim(); });' +
      ' return JSON.stringify(out); })()').then(JSON.parse);
    const onResults = await figures('results');
    const onList = await figures('list');
    const top5 = JSON.parse(await ev('JSON.stringify(DATA.top5)'));
    check('results shows the ' + top5.length + ' cards in DATA.top5', Object.keys(onResults).join() === top5.join(), Object.keys(onResults).join());
    check('list shows every university', Object.keys(onList).length === (await ev('DATA.universities.length')), Object.keys(onList).length);
    const mismatched = top5.filter((id) => !onResults[id] || onResults[id] !== onList[id]);
    check('cost and grades on results = the same rows on list', mismatched.length === 0,
      mismatched.map((id) => id + ': ' + onResults[id] + ' vs ' + onList[id]).join(' || '));
    const fromData = top5.filter((id) => onResults[id] !== undefined).map((id) => ev('App.fmt.myr(App.uni("' + id + '").approxTotalMyr) + " | " + App.uni("' + id + '").gradesVsEntryBar'));
    check('...and both = the row in DATA', (await Promise.all(fromData)).join('#') === top5.map((id) => onResults[id]).join('#'));
    // The recommended university's full price is quoted on five screens; it must be one number.
    const mitCost = await ev('App.fmt.myr(App.uni(DATA.report.universityId).approxTotalMyr)');
    const quoting = [];
    for (const id of ['landing', 'results', 'list', 'report', 'decide']) {
      await ev('App.go("' + id + '")');
      if ((await ev('document.querySelector("#app").innerText')).includes(mitCost)) quoting.push(id);
    }
    check('the sample report university costs ' + mitCost + ' on all five screens that quote it', quoting.length === 5, quoting.join(','));

    // --- H. the list's own controls, and what the next screens do with them
    await ev('App.setState({ picked: [], listOpen: [] }); App.go("list")');
    check('list: nothing ticked -> ghost "sample report" button', (await count('[data-pickbar] .btn-ghost[data-go="report"]')) === 1);
    await click('[data-row="nus"] .row-toggle');
    check('list: clicking a row opens its detail', (await count('#detail-nus')) === 1);
    const colsShown = await ev('(() => { const t = document.querySelector(\'[data-row="nus"]\').innerText + document.querySelector("#detail-nus").innerText;' +
      ' return DATA.columns.filter((c) => App.uni("nus")[c.key] !== "" && !t.includes(c.label) && !t.includes(String(App.uni("nus")[c.key]).slice(0, 12))).map((c) => c.key).join(); })()');
    // The collapsed row shows two columns reworded ("RM 383,438", "Checked"), so those two may differ.
    check('list: an open row shows every filled column',
      colsShown.split(',').filter(Boolean).every((k) => ['approxTotalMyr', 'infoSource'].includes(k)), colsShown);
    await click('[data-row="nus"] .row-toggle');
    check('list: clicking again closes it', (await count('#detail-nus')) === 0);
    await click('[data-pick="nus"]');
    await click('[data-pick="mit"]');
    check('list: ticks are kept in tick order', (await ev('App.state.picked.join()')) === 'nus,mit', await ev('App.state.picked.join()'));
    check('list: bar counts 1 free + 1 paid, no price shown', /1 free/.test(await text('[data-pickbar] .tally')) && /1 paid/.test(await text('[data-pickbar] .tally')) && !/RM/.test(await text('[data-pickbar]')), await text('[data-pickbar] .tally'));
    check('list: a cut university cannot be ticked', (await ev('document.querySelector(\'[data-pick="cmu"]\').disabled')) === true);
    await click('[data-pickbar] [data-go="report"]');
    check('report: names the other university that was ticked', /You also ticked NUS/.test(await text('.screen-report .rp-note')), await text('.screen-report .rp-note'));
    await click('.screen-report [data-go="list"]');
    check('list: ticks survive leaving and coming back', (await count('[data-pick]:checked')) === 2);
    await ev('App.setState({ picked: [] })');

    // --- I. plan step 6: screen-only constants now live in data.js
    const src = (name) => fs.readFileSync(path.join(proto, 'screens', name + '.js'), 'utf8');
    const MOVED = {
      landing: ['TIER_OF'],
      onboarding: ['DEMO_WHATSAPP', 'QUALIFICATIONS', 'EXTRA_COUNTRIES', 'OTHER_BUDGET_BANDS'],
      results: ['const BANDS', 'const place ='],
      list: ['const BANDS', 'const place =', 'const GROUPS'],
      report: ['OPEN_SECTION'],
      decide: ['const BANDS', 'const ROUNDS', 'one per country']
    };
    Object.keys(MOVED).forEach((name) => {
      const left = MOVED[name].filter((needle) => src(name).includes(needle));
      check(name + '.js: constants moved out (' + MOVED[name].join(', ') + ')', left.length === 0, 'still there: ' + left.join(', '));
    });
    const moved = JSON.parse(await ev(`JSON.stringify({
      bands: (DATA.bands || []).map((b) => b.key + ':' + b.label).join(),
      place: DATA.universities.map((u) => u.place),
      tiers: DATA.deliverables.map((d) => d.tier).join(),
      scope: DATA.deliverables.map((d) => d.scope || '').join(''),
      whatsapp: DATA.student.whatsapp,
      intake: DATA.intake || {},
      groups: (DATA.columnGroups || []).map((g) => g.keys).flat(),
      groupKeysReal: (DATA.columnGroups || []).map((g) => g.keys).flat().every((k) => DATA.columns.some((c) => c.key === k)),
      open: DATA.report.openSection,
      openTitle: (DATA.report.sections.find((s) => s.n === DATA.report.openSection) || {}).title,
      rounds: DATA.decision.rounds || {},
      planRounds: DATA.decision.plan.map((p) => p.round),
      band: DATA.student.budget.band, qualification: DATA.student.qualification
    })`));
    check('DATA.bands: reach, match, safety with labels', moved.bands === 'reach:Reach,match:Match,safety:Safety', moved.bands);
    check('every university has a place; the city-state is named once',
      moved.place.every((p) => typeof p === 'string' && p) && moved.place.includes('Singapore') && !moved.place.some((p) => /Singapore.*Singapore/.test(p)), moved.place.join(' / '));
    check('DATA.deliverables carry their tier', moved.tiers === 'free,firstFree,paid', moved.tiers);
    check('the Apply Guide carries its "one per country" scope', /one per country/.test(moved.scope), moved.scope);
    check('DATA.student.whatsapp is the demo number', moved.whatsapp === '012-345 6789', moved.whatsapp);
    check('DATA.intake: qualifications, extra countries, budget bands',
      (moved.intake.qualifications || []).length === 5 && (moved.intake.extraCountries || []).length === 3 && (moved.intake.budgetBands || []).length === 3,
      JSON.stringify(moved.intake));
    check('the student\'s own budget band and qualification are among the intake options',
      (moved.intake.budgetBands || []).includes(moved.band) && (moved.intake.qualifications || []).includes(moved.qualification));
    check('DATA.columnGroups name real columns, none twice', moved.groups.length > 0 && moved.groupKeysReal && new Set(moved.groups).size === moved.groups.length, moved.groups.join());
    check('DATA.report.openSection points at "why here / why hesitate"', /why here/i.test(moved.openTitle || ''), moved.open + ' ' + moved.openTitle);
    check('DATA.decision.rounds labels every round in the plan', moved.planRounds.every((r) => moved.rounds[r]), JSON.stringify(moved.rounds));

    // --- J. data contract (Session 1's checks, unchanged)
    const d = JSON.parse(await ev(`JSON.stringify({
      n: DATA.universities.length,
      cols: DATA.columns.length,
      missing: DATA.universities.map(u => DATA.columns.filter(c => !(c.key in u)).length).reduce((a, b) => a + b, 0),
      ids: DATA.universities.map(u => u.id),
      bands: DATA.universities.map(u => u.band),
      numeric: DATA.universities.every(u => Number.isInteger(u.approxTotalMyr) && Number.isInteger(u.desirability) && Number.isInteger(u.durationYears)),
      verified: DATA.universities.filter(u => u.verified).length,
      top5: DATA.top5.map(id => { const u = App.uni(id); return u ? u.band : null; }),
      findings: DATA.findings,
      sections: DATA.report.sections.length,
      whyHere: DATA.report.whyHere.length, whyHesitate: DATA.report.whyHesitate.length,
      rec: DATA.decision.recommendedId, balance: DATA.decision.balance,
      scores: [DATA.feedback.list.score, DATA.feedback.report.score, DATA.feedback.label],
      price: DATA.pricing.pricePerReport,
      mit: [App.fmt.myr(App.uni('mit').approxTotalMyr), App.fmt.myrShort(App.uni('mit').approxTotalMyr), App.fmt.myrShort(App.uni('nus').approxTotalMyr)],
      undef: JSON.stringify(DATA).includes('undefined') || JSON.stringify(DATA).includes('NaN'),
      esc: App.esc('<b>"R&D"</b>')
    })`));
    check('15 universities', d.n === 15, d.n);
    check('35 columns, none missing on any row', d.cols === 35 && d.missing === 0, d.cols + '/' + d.missing);
    check('15 unique ids', new Set(d.ids).size === 15, d.ids.join(','));
    check('every row has a band', d.bands.every((b) => ['reach', 'match', 'safety'].includes(b)), d.bands.join(','));
    check('numeric columns are numbers', d.numeric);
    check('15 verified rows (none "Not verified" in the sample since 2026-10-12)', d.verified === 15, d.verified);
    check('top5 is a Reach/Match/Safety spread', d.top5.length === 5 && ['reach', 'match', 'safety'].every((b) => d.top5.includes(b)), d.top5.join(','));
    check('3-4 findings', d.findings.length >= 3 && d.findings.length <= 4, d.findings.length);
    // Findings are built from counts and name lists, so an empty list must not leave "0 ()" on screen.
    check('findings: no empty name list or zero count', !d.findings.some((f) => /\(\)|\bother 0\b/.test(f)), d.findings.join(' || '));
    // The sample CSV spells it "Need blind" (MIT's own wording) as well as "need-blind".
    check('findings: aid finding names MIT', d.findings.some((f) => /^MIT, .*decide admission/.test(f)), d.findings[2]);
    check('15 report sections, why here + why hesitate filled', d.sections === 15 && d.whyHere > 0 && d.whyHesitate > 0);
    check('recommended id is a real row', d.ids.includes(d.rec), d.rec);
    check('feedback as on poster, labelled early testers', d.scores[0] === 4.1 && d.scores[1] === 4.2 && /early testers/i.test(d.scores[2]), d.scores.join(','));
    check('no price has been invented', d.price === null, d.price);
    check('no "undefined"/NaN leaked into DATA', d.undef === false);
    check('App.esc escapes', d.esc === '&lt;b&gt;&quot;R&amp;D&quot;&lt;/b&gt;', d.esc);
    check('money format', d.mit.join('|') === 'RM 1,499,002|RM 1.50M|RM 383k', d.mit.join('|'));
    // Rules for every session: no blanket "every fee checked" claim anywhere on screen.
    const claims = [];
    for (const id of ORDER) {
      await ev('App.go("' + id + '")');
      if (/every (fee|fact|number|row) (is |was )?(checked|verified)/i.test(await ev('document.querySelector("#app").innerText'))) claims.push(id);
    }
    check('no "every fee checked" claim on any screen', claims.length === 0, claims.join(','));

    // --- K. plan step 7: the three sides look like one product
    const measure = (id) => ev('(() => { App.go(' + JSON.stringify(id) + '); const px = (el, p) => getComputedStyle(el)[p];' +
      ' const uniq = (sel, f) => Array.from(new Set(Array.from(document.querySelectorAll("#app " + sel)).map(f))).sort().join(" / ");' +
      ' const h1 = document.querySelector("#app h1"); const root = document.querySelector("#app > div");' +
      ' return JSON.stringify({' +
      // decide's navy "apply here first" card titles itself with a display-size h2, on purpose
      ' h1: px(h1, "fontSize"), h2: uniq("h2:not(.dc-hero h2)", (e) => px(e, "fontSize")), h3: uniq("h3", (e) => px(e, "fontSize")),' +
      ' sectionTitle: uniq(".section-title", (e) => px(e, "fontSize") + " " + px(e, "letterSpacing")),' +
      ' card: uniq(".card", (e) => px(e, "paddingTop") + " " + px(e, "paddingLeft") + " r" + px(e, "borderTopLeftRadius")),' +
      ' column: Math.round(root.getBoundingClientRect().width), padTop: px(root, "paddingTop"),' +
      ' firstTop: Math.round(root.firstElementChild.getBoundingClientRect().top + window.scrollY)' +
      ' }); })()').then(JSON.parse);
    const metrics = {};
    for (const id of ORDER) metrics[id] = await measure(id);
    const same = (key) => new Set(ORDER.map((id) => metrics[id][key])).size === 1;
    const spread = (key) => ORDER.map((id) => id + '=' + metrics[id][key]).join('  ');
    // Buttons come in three named sizes (styles.css): standard, .btn-lg and .btn-sm. Each must be
    // one size wherever it appears, in every state a screen can be in.
    const BUTTON_STATES = [
      ['landing', 'App.go("landing")'],
      ['onboarding 1', 'App.setState({ onboardingStep: 1 }); App.go("onboarding")'],
      ['onboarding 3', 'App.setState({ onboardingStep: 3 })'],
      ['waiting building', 'App.setState({ ready: false }); App.go("waiting")'],
      ['waiting ready', 'App.setState({ ready: true })'],
      ['results', 'App.go("results")'], ['list', 'App.go("list")'], ['report', 'App.go("report")'], ['decide', 'App.go("decide")']
    ];
    const sizes = { standard: {}, large: {}, small: {} };
    for (const [name, js] of BUTTON_STATES) {
      const found = JSON.parse(await ev('(() => { ' + js + '; return JSON.stringify(Array.from(document.querySelectorAll("#app .btn")).map((e) => { const s = getComputedStyle(e);' +
        ' return [e.classList.contains("btn-lg") ? "large" : e.classList.contains("btn-sm") ? "small" : "standard",' +
        ' s.fontSize + " " + s.paddingTop + " " + s.paddingLeft + " h" + Math.round(e.getBoundingClientRect().height)]; })); })()'));
      found.forEach(([kind, size]) => { (sizes[kind][size] = sizes[kind][size] || []).push(name); });
    }
    Object.keys(sizes).forEach((kind) => {
      const seen = Object.keys(sizes[kind]);
      check(kind + ' buttons are one size on every screen', seen.length === 1,
        seen.map((size) => size + ' on ' + Array.from(new Set(sizes[kind][size])).join(', ')).join('  ||  ') || 'none found');
    });
    check('small section labels are the same size on every screen', same('sectionTitle'), spread('sectionTitle'));
    check('page headings (h1) are the same size on screens 2-7 (landing\'s headline is bigger on purpose)',
      new Set(ORDER.slice(1).map((id) => metrics[id].h1)).size === 1, spread('h1'));
    check('section headings (h2) are one size on every screen', ORDER.every((id) => !metrics[id].h2.includes('/')) && new Set(ORDER.map((id) => metrics[id].h2).filter(Boolean)).size === 1, spread('h2'));
    check('every screen starts the same distance below the top bar', same('firstTop'), spread('firstTop'));
    // A regular-round deadline must read the same on the plan as on the list ("Rolling", not "To confirm").
    const squash = (t) => String(t).replace(/approx\.?/i, '').replace(/\s+/g, ' ').trim().toLowerCase();
    const regular = JSON.parse(await ev('JSON.stringify(DATA.decision.plan.filter((p) => p.round === "regular").map((p) => p.id))'));
    const dateMismatch = [];
    for (const id of regular) {
      await ev('App.go("decide")');
      const onPlan = squash(await ev('document.querySelector(\'[data-deadline="' + id + '"]\').closest(".dc-day").querySelector(".dc-tile").innerText'));
      await ev('App.go("list")');
      const onTable = squash(await text('[data-row="' + id + '"] .col-deadline'));
      if (onPlan !== onTable) dateMismatch.push(id + ': plan "' + onPlan + '" vs list "' + onTable + '"');
    }
    check('regular-round deadlines read the same on the plan and on the list', dateMismatch.length === 0, dateMismatch.join(' || '));

    await width(NARROW);
    const squeezed = [];
    for (const id of ORDER) {
      await ev('App.go("' + id + '")');
      if (await overflows()) squeezed.push(id + ' (' + (await ev('document.documentElement.scrollWidth')) + ')');
    }
    check('no sideways scroll at ' + NARROW + 'px on any screen', squeezed.length === 0, squeezed.join(', '));
    await ev('App.go("landing")');
    await shot('8-landing-' + NARROW);
    await width(WIDE);

    // --- L. opening straight on a later screen
    await coldOpen('list');
    check('index.html#list opens on list with ready=true', (await cur()) === 'list' && (await ev('App.state.ready')) === true);
    await coldOpen('waiting');
    check('index.html#waiting opens on waiting, not ready', (await cur()) === 'waiting' && (await ev('App.state.ready')) === false);

    // --- optional dump: every screen's markup in each of its states, for before/after diffs
    if (dumpFile) {
      await coldOpen('');
      const html = () => ev('document.querySelector("#app").innerHTML');
      const snap = {};
      const at = async (name, js) => { await ev(js); snap[name] = await html(); };
      await at('landing', 'App.go("landing")');
      await at('onboarding-1', 'App.go("onboarding")');
      await at('onboarding-2', 'App.setState({ onboardingStep: 2 })');
      await at('onboarding-3', 'App.setState({ onboardingStep: 3 })');
      await at('waiting-building', 'App.go("waiting")');
      await at('waiting-ready', 'App.setState({ ready: true })');
      await at('results', 'App.go("results")');
      await at('list', 'App.go("list")');
      await at('list-open-ticked', 'App.setState({ listOpen: ["mit", "nus", "cmu"], picked: ["nus", "mit"] })');
      await at('report-ticked', 'App.go("report")');
      await at('report', 'App.setState({ picked: [] })');
      await at('decide', 'App.go("decide")');
      fs.writeFileSync(dumpFile, JSON.stringify({ metrics, snap }, null, 1));
    }

    // --- M. plan step 2: console must be empty
    check('browser console is empty', consoleOut.length === 0, consoleOut.join(' || '));

    const failed = results.filter((r) => !r.ok);
    results.forEach((r) => { if (!r.ok) console.log('FAIL  ' + r.name + (r.detail !== undefined ? '  -> ' + r.detail : '')); });
    console.log(results.length - failed.length + '/' + results.length + ' checks passed');
    exit = failed.length ? 1 : 0;
    ws.close();
  } catch (err) {
    console.log('ERROR ' + (err && err.stack || err));
  } finally {
    chrome.kill();
    await sleep(300);
    try { fs.rmSync(profile, { recursive: true, force: true }); } catch (e) { /* Chrome may still hold a lock */ }
    process.exit(exit);
  }
})();
