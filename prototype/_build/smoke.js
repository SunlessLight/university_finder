// Session 1 smoke test: opens prototype/index.html from file:// in headless Chrome over the
// DevTools protocol, clicks the whole path, and fails on any console output.
// usage: node smoke.js <repo_root> <screenshot_dir>
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { pathToFileURL } = require('url');

const repo = process.argv[2];
const shots = process.argv[3];
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9347;
const page = pathToFileURL(path.join(repo, 'prototype', 'index.html')).href;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const results = [];
const check = (name, ok, detail) => results.push({ name, ok: !!ok, detail });

(async () => {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'proto-smoke-'));
  const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT,
    '--remote-allow-origins=*', '--user-data-dir=' + profile, '--no-first-run',
    '--window-size=1366,768', 'about:blank'], { stdio: 'ignore' });
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
    const shot = async (name) => {
      const r = await send('Page.captureScreenshot', { format: 'png' });
      fs.writeFileSync(path.join(shots, name + '.png'), Buffer.from(r.result.data, 'base64'));
    };
    const click = (sel) => ev('document.querySelector(' + JSON.stringify(sel) + ').click()');
    const cur = () => ev('App.current');

    await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');

    // --- 1. open by file:// and check the start state
    await open(page);
    check('opens from file://', page.startsWith('file:///'), page);
    check('starts on landing', (await cur()) === 'landing', await cur());
    check('root gets class screen-landing',
      (await ev('document.querySelector("#app > div").className')) === 'screen screen-landing');
    check('state starts as contract says',
      (await ev('JSON.stringify(App.state)')) === '{"ready":false,"onboardingStep":1,"picked":[]}',
      await ev('JSON.stringify(App.state)'));
    check('journey bar has 4 steps', (await ev('document.querySelectorAll("[data-journey]").length')) === 4);
    // Under file:// a stylesheet's rules are unreadable (cross-origin) and link.sheet is set even
    // for a missing file, so neither proves a load. styles.css is proven by one of its tokens; a
    // missing screen stylesheet is caught by the empty-console check in step 8 (ERR_FILE_NOT_FOUND).
    const navy = await ev('getComputedStyle(document.documentElement).getPropertyValue("--navy").trim()');
    check('8 stylesheet links, styles.css applied',
      (await ev('document.querySelectorAll(\'link[rel="stylesheet"]\').length')) === 8 && navy === '#10233f', navy);
    await shot('1-landing');

    // --- 2. "Your list" before ready goes to waiting
    await click('[data-journey="1"]');
    check('"Your list" before ready -> waiting', (await cur()) === 'waiting', await cur());
    await ev('App.go("landing")');

    // --- 3. click the whole path, in order
    const order = ['landing', 'onboarding', 'waiting', 'results', 'list', 'report', 'decide'];
    for (let i = 0; i < order.length; i++) {
      const id = order[i];
      check('on ' + id + ': heading + one line present',
        await ev('!!document.querySelector(".screen-' + id + ' h1") && !!document.querySelector(".screen-' + id + ' p.muted")'));
      check('on ' + id + ': journey bar marks one current step',
        (await ev('document.querySelectorAll(".journey-step.is-current").length')) === 1);
      if (i === order.length - 1) break;
      if (id === 'waiting') {
        check('waiting has no data-go (skip is its only control)', (await ev('document.querySelectorAll("#app [data-go]").length')) === 0);
        await click('#app [data-skip]');
        check('skip ahead sets ready', (await ev('App.state.ready')) === true);
      } else {
        await click('#app [data-go]');
      }
      check(id + ' -> ' + order[i + 1], (await cur()) === order[i + 1], await cur());
      check('scrolled to top after ' + id, (await ev('window.scrollY')) === 0);
    }
    await shot('2-decide');
    await click('#app [data-go]');
    check('decide -> back to landing', (await cur()) === 'landing', await cur());

    // --- 4. journey bar jumps (list is ready now)
    const jumps = ['landing', 'results', 'report', 'decide'];
    for (let i = jumps.length - 1; i >= 0; i--) {
      await click('[data-journey="' + i + '"]');
      check('journey step ' + (i + 1) + ' -> ' + jumps[i], (await cur()) === jumps[i], await cur());
      check('journey step ' + (i + 1) + ' is marked current',
        await ev('document.querySelector(\'[data-journey="' + i + '"]\').classList.contains("is-current")'));
    }
    await click('.brand');
    check('brand link -> landing', (await cur()) === 'landing');

    // --- 5. setState merges and re-renders in place; hash navigation
    await ev('App.go("list"); App.setState({ picked: ["mit"] })');
    check('setState merges, keeps screen',
      (await cur()) === 'list' && (await ev('JSON.stringify(App.state)')) === '{"ready":true,"onboardingStep":1,"picked":["mit"]}',
      await ev('JSON.stringify(App.state)'));
    await ev('location.hash = "report"'); await sleep(100);
    check('hash change navigates', (await cur()) === 'report', await cur());
    await shot('3-report');

    // --- 6. data contract
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
      deadlines: DATA.decision.deadlines.map(x => x.university + ' ' + App.fmt.date(x.date) + (x.confirmed ? '' : ' (to confirm)')),
      steps: DATA.decision.applySteps.map(s => s.title),
      scores: [DATA.feedback.list.score, DATA.feedback.report.score, DATA.feedback.label],
      student: DATA.student,
      files: [DATA.files.list.href, DATA.files.report.href],
      mit: [App.fmt.myr(App.uni('mit').approxTotalMyr), App.fmt.myrShort(App.uni('mit').approxTotalMyr), App.fmt.myrShort(App.uni('nus').approxTotalMyr)],
      undef: JSON.stringify(DATA).includes('undefined') || JSON.stringify(DATA).includes('NaN'),
      esc: App.esc('<b>"R&D"</b>')
    })`));
    check('15 universities', d.n === 15, d.n);
    check('35 columns, none missing on any row', d.cols === 35 && d.missing === 0, d.cols + '/' + d.missing);
    check('15 unique ids', new Set(d.ids).size === 15, d.ids.join(','));
    check('every row has a band', d.bands.every((b) => ['reach', 'match', 'safety'].includes(b)), d.bands.join(','));
    check('numeric columns are numbers', d.numeric);
    check('13 verified rows (2 "Not verified" in the sample)', d.verified === 13, d.verified);
    check('top5 is a Reach/Match/Safety spread', d.top5.length === 5 && ['reach', 'match', 'safety'].every((b) => d.top5.includes(b)), d.top5.join(','));
    check('3-4 findings', d.findings.length >= 3 && d.findings.length <= 4, d.findings.length);
    check('15 report sections, why here + why hesitate filled', d.sections === 15 && d.whyHere > 0 && d.whyHesitate > 0);
    check('recommended id is a real row', d.ids.includes(d.rec), d.rec);
    check('feedback as on poster', d.scores[0] === 4.1 && d.scores[1] === 4.2, d.scores.join(','));
    check('no "undefined"/NaN leaked into DATA', d.undef === false);
    check('App.esc escapes', d.esc === '&lt;b&gt;&quot;R&amp;D&quot;&lt;/b&gt;', d.esc);
    check('both download files exist on disk',
      d.files.every((f) => fs.existsSync(path.join(repo, 'prototype', f))), d.files.join(' | '));
    check('money format', d.mit.join('|') === 'RM 1,743,888|RM 1.74M|RM 452k', d.mit.join('|'));

    // --- 7. opening straight on a later screen
    // Leave the page first: step 5 left us on index.html#report, and going from there to
    // index.html#list only changes the hash, so Chrome fires no load event (and it would not be
    // a cold open anyway).
    await open('about:blank');
    await open(page + '#list');
    check('index.html#list opens on list with ready=true', (await cur()) === 'list' && (await ev('App.state.ready')) === true);

    // --- 8. console must be empty
    check('browser console is empty', consoleOut.length === 0, consoleOut.join(' || '));

    const failed = results.filter((r) => !r.ok);
    results.forEach((r) => { if (!r.ok) console.log('FAIL  ' + r.name + (r.detail !== undefined ? '  -> ' + r.detail : '')); });
    console.log(results.length - failed.length + '/' + results.length + ' checks passed');
    console.log('\nfindings:\n- ' + d.findings.join('\n- '));
    console.log('\ndeadlines:\n- ' + d.deadlines.join('\n- '));
    console.log('\napply steps:\n- ' + d.steps.join('\n- '));
    console.log('\nbalance: ' + JSON.stringify(d.balance) + '\nstudent: ' + JSON.stringify(d.student));
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
