/* Screen 5 of 7: list, the full table. Owner: Session B.
   Every name, cost, grade and date is read from DATA; nothing is retyped here.

   State (in App.state, because render gets a fresh root on every change)
     picked    university ids ticked for a deep report, in the order they were ticked
     listOpen  university ids whose row is expanded          [this screen's own key]

   data-row / data-pick / data-cost / data-grades / data-pickbar are hooks for the two
   listeners below and for checks, not for styling. */
(function () {
  'use strict';

  const esc = App.esc;
  const BANDS = [['reach', 'Reach'], ['match', 'Match'], ['safety', 'Safety']];
  const HEADS = ['Report', 'University', 'Course', 'Likelihood', 'Grades vs bar', 'Total, whole degree',
    'Deadline', 'Official page'];

  /* Columns the collapsed row already shows; the detail panel shows all the others. */
  const IN_ROW = ['university', 'course', 'country', 'city', 'admissionLikelihood', 'gradesVsEntryBar',
    'approxTotalMyr', 'infoSource', 'warnings'];

  /* How the detail panel groups the remaining spreadsheet columns. Layout only: labels and
     values come from DATA.columns and the row. A column not named here lands in the last group. */
  const GROUPS = [
    { title: 'The course', keys: ['courseAtAGlance', 'studentLife', 'intake'] },
    { title: 'Getting in', keys: ['entryRequirements', 'studentGrades', 'englishReq', 'howToApply', 'keyDeadline'] },
    { title: 'What it costs', keys: ['annualTuition', 'totalTuition', 'estLivingPerYear', 'durationYears', 'moneyToShowVisa'] },
    { title: 'Scholarships', keys: ['scholarshipAndPortal', 'scholarshipCoverage', 'scholarshipCompetitiveness', 'howToGetScholarship'] },
    { title: 'After you graduate', keys: ['workRightsAfterGraduating', 'recognisedInMalaysia'] },
    { title: 'How it ranks', keys: ['subjectRank', 'overallRank', 'desirability', 'tier', 'listStatus'] },
    { title: 'Good to know', keys: [] }
  ];

  const place = (u) => u.city === u.country ? u.country : u.city + ' · ' + u.country;
  const isCut = (u) => u.listStatus === 'Rejected';
  const has = (v) => v !== '' && v != null;

  function groupsFor(columns) {
    const byKey = {};
    columns.forEach((c) => { byKey[c.key] = c; });
    const placed = IN_ROW.concat(...GROUPS.map((g) => g.keys));
    const leftover = columns.filter((c) => !placed.includes(c.key));
    return GROUPS.map((g, i) => ({
      title: g.title,
      cols: g.keys.map((k) => byKey[k]).filter(Boolean).concat(i === GROUPS.length - 1 ? leftover : [])
    }));
  }

  function deadline(u) {
    if (!u.deadlineDate) return /^rolling/i.test(u.keyDeadline) ? 'Rolling' : esc(App.fmt.date(null));
    /* Approximate only when the note is about this date, not a later one in the same cell. */
    const at = u.keyDeadline.indexOf(u.deadlineDate);
    const approx = u.keyDeadline[at - 1] === '~' || /^\s*\(approx/i.test(u.keyDeadline.slice(at + u.deadlineDate.length));
    return esc(App.fmt.date(u.deadlineDate)) + (approx ? ' <span class="approx muted">approx.</span>' : '');
  }

  function value(u, key) {
    const v = u[key];
    if (key === 'courseUrl') return `<a href="${esc(v)}" target="_blank" rel="noopener">${esc(v)}</a>`;
    if (key === 'desirability') return esc(v) + ' / 100';
    return esc(v);
  }

  function detail(u, groups, warningsLabel) {
    const blocks = groups.map((g) => {
      const cols = g.cols.filter((c) => has(u[c.key]));
      if (!cols.length) return '';
      return `<section><h3 class="section-title">${esc(g.title)}</h3><dl>${cols.map((c) =>
        `<div><dt>${esc(c.label)}</dt><dd>${value(u, c.key)}</dd></div>`).join('')}</dl></section>`;
    }).join('');
    return `
      <tr class="detail" id="detail-${esc(u.id)}">
        <td colspan="${HEADS.length}">
          ${has(u.warnings) ? `<p class="warn"><strong>${esc(warningsLabel)}.</strong> ${esc(u.warnings)}</p>` : ''}
          <div class="detail-grid">${blocks}</div>
        </td>
      </tr>`;
  }

  function row(u, ctx) {
    const picked = ctx.picked.includes(u.id);
    const open = ctx.open.includes(u.id);
    const cut = isCut(u);
    const cls = ['row'].concat(picked ? 'is-picked' : [], open ? 'is-open' : [], cut ? 'is-cut' : []).join(' ');
    const tickLabel = cut ? esc(u.shortName) + ' was cut from your list' : 'Tick ' + esc(u.shortName) + ' for a deep report';
    return `
      <tr class="${cls}" data-row="${esc(u.id)}">
        <td class="col-pick">
          <label class="tick" title="${tickLabel}">
            <input type="checkbox" data-pick="${esc(u.id)}" aria-label="${tickLabel}"${picked ? ' checked' : ''}${cut ? ' disabled' : ''}>
          </label>
        </td>
        <td class="col-uni">
          <button type="button" class="row-toggle" aria-expanded="${open}"${open ? ` aria-controls="detail-${esc(u.id)}"` : ''}>
            <span class="chev" aria-hidden="true"></span><span>${esc(u.university)}</span>
          </button>
          <span class="uni-sub muted">${esc(place(u))}</span>
          ${cut ? '<span class="uni-sub tag-cut">Cut from your list. Open the row to see why.</span>' : ''}
          ${u.id === ctx.sampleId ? '<span class="uni-sub tag-sample">Sample report ready</span>' : ''}
        </td>
        <td class="col-course">${esc(u.course)}</td>
        <td><span class="badge badge-${u.band}">${esc(u.admissionLikelihood)}</span></td>
        <td class="col-grades" data-grades>${esc(u.gradesVsEntryBar)}</td>
        <td class="num" data-cost>${App.fmt.myr(u.approxTotalMyr)}</td>
        <td class="col-deadline">${deadline(u)}</td>
        <td>${u.verified
          ? '<span class="badge badge-verified" title="Checked on the official university page">Checked</span>'
          : '<span class="badge badge-unverified">Not verified</span>'}</td>
      </tr>` + (open ? detail(u, ctx.groups, ctx.warningsLabel) : '');
  }

  function pickBar(picked, pricing) {
    const n = picked.length;
    const rule = pricing.reportRule;
    const free = Math.min(n, rule.freeCount);
    const paid = n - free;
    /* No price is set yet (pricePerReport is null), so the amount only appears once there is one. */
    const amount = paid && pricing.pricePerReport != null ? ' · ' + App.fmt.myr(paid * pricing.pricePerReport) : '';
    const tally = (free ? `<span class="badge badge-free">${free} free</span>` : '') +
      (paid ? `<span class="badge badge-paid">${paid} paid${amount}</span>` : '');
    const headline = n
      ? `${n} ${n === 1 ? 'university' : 'universities'} ticked for a deep report`
      : 'No universities ticked yet';
    const sub = n
      ? esc(picked.map((u) => u.shortName).join(', '))
      : 'Tick the ones you want a deep report on.';
    return `
      <div class="pickbar card" data-pickbar aria-live="polite">
        <div class="pickbar-text">
          <strong>${headline}</strong>
          <span class="muted">${sub}</span>
        </div>
        <div class="pickbar-price">
          <span class="tally">${tally}</span>
          <span class="muted">${esc(rule.text)}</span>
        </div>
        <button type="button" class="btn ${n ? 'btn-primary' : 'btn-ghost'}" data-go="report">${
          n ? 'Get my ' + (n === 1 ? 'report' : n + ' reports') : 'See the sample report'}</button>
      </div>`;
  }

  /* setState swaps in a new root, so put the keyboard focus back where it was. */
  function refocus(selector) {
    const el = document.querySelector('.screen-list ' + selector);
    if (el) el.focus({ preventScroll: true });
  }

  App.register('list', {
    render: function (root, state, data) {
      const unis = data.universities;
      const ctx = {
        picked: state.picked || [],
        open: state.listOpen || [],
        groups: groupsFor(data.columns),
        warningsLabel: (data.columns.find((c) => c.key === 'warnings') || { label: 'Warning' }).label,
        sampleId: data.report.universityId
      };
      const spread = BANDS.map(([band, label]) =>
        `<span class="badge badge-${band}">${unis.filter((u) => u.band === band).length} ${label}</span>`).join('');

      root.innerHTML = `
        <header class="head">
          <div>
            <p class="section-title">Your full list</p>
            <h1>All ${unis.length} universities, side by side</h1>
            <p class="muted">Click a row to see everything we found. Tick the ones you want a deep report on.</p>
            <p class="spread">${spread}</p>
          </div>
          <a class="btn btn-ghost" href="${esc(data.files.list.href)}" download>${esc(data.files.list.label)}</a>
        </header>

        <div class="table-wrap card">
          <table>
            <thead><tr>${HEADS.map((h, i) => `<th scope="col"${i === 5 ? ' class="num"' : ''}>${h}</th>`).join('')}</tr></thead>
            <tbody>${unis.map((u) => row(u, ctx)).join('')}</tbody>
          </table>
        </div>

        ${pickBar(ctx.picked.map(App.uni).filter(Boolean), data.pricing)}`;

      root.addEventListener('change', (event) => {
        const box = event.target.closest('[data-pick]');
        if (!box) return;
        const id = box.getAttribute('data-pick');
        const picked = ctx.picked.filter((p) => p !== id);
        if (box.checked) picked.push(id);
        App.setState({ picked: picked });
        refocus('[data-pick="' + id + '"]');
      });

      root.addEventListener('click', (event) => {
        /* Ticking, links and the report button are not "open this row". */
        if (event.target.closest('label, input, a, [data-go]')) return;
        const tr = event.target.closest('[data-row]');
        if (!tr) return;
        const id = tr.getAttribute('data-row');
        const open = ctx.open.includes(id) ? ctx.open.filter((o) => o !== id) : ctx.open.concat(id);
        App.setState({ listOpen: open });
        refocus('[data-row="' + id + '"] .row-toggle');
      });
    }
  });
})();
