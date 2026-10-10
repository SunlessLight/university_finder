/* Screen 6 of 7: report. Owner: Session C.
   The MIT report from DATA.report: the one-page summary first, then the section list with
   "Why here / why hesitate" opened in full. Every name, cost and count is read from DATA. */
(function () {
  'use strict';

  const esc = App.esc;

  function names(list) {
    return list.length > 1 ? list.slice(0, -1).join(', ') + ' and ' + list[list.length - 1] : list[0] || '';
  }

  function whyColumn(kind, title, items) {
    return `<div class="rp-why rp-why-${kind}">
        <p class="rp-why-title">${title}</p>
        ${items.map((w) => `<div class="rp-why-item" data-why="${kind}">
          <h4>${esc(w.theme)}</h4>
          <p>${esc(w.text)}</p>
        </div>`).join('')}
      </div>`;
  }

  function sectionRow(s, report) {
    const open = s.n === report.openSection;   /* the one section this screen shows in full */
    return `<li class="rp-section${open ? ' is-open' : ''}" data-section="${s.n}">
        <span class="rp-num">${s.n}</span>
        <div class="rp-section-text">
          <h3>${esc(s.title)}</h3>
          <p class="muted">${esc(s.tells)}</p>
        </div>
        <span class="rp-q">${esc(s.question)}</span>
        ${open ? `<div class="rp-verdict">
          ${whyColumn('here', 'Why here', report.whyHere)}
          ${whyColumn('hesitate', 'Why hesitate', report.whyHesitate)}
        </div>` : ''}
      </li>`;
  }

  App.register('report', {
    render: function (root, state, data) {
      const report = data.report;
      const uni = App.uni(report.universityId);
      const rule = data.pricing.reportRule;
      const open = report.sections.find((s) => s.n === report.openSection);
      const alsoPicked = state.picked.filter((id) => id !== uni.id).map(App.uni).filter(Boolean)
        .map((u) => u.shortName);

      root.innerHTML = `
        <header class="rp-head">
          <div>
            <p class="section-title">University report · written for ${esc(data.student.nickname)}</p>
            <h1>${esc(uni.university)}</h1>
            <p class="rp-course">${esc(uni.course)} · ${esc(uni.city)}, ${esc(uni.country)}</p>
            <p class="rp-badges">
              <span class="badge badge-${uni.band}">${esc(uni.admissionLikelihood)}</span>
              ${uni.verified
                ? '<span class="badge badge-verified">Checked on official page</span>'
                : '<span class="badge badge-unverified">Not verified</span>'}
            </p>
          </div>
          <div class="rp-actions">
            <a class="btn btn-ghost" href="${esc(data.files.report.href)}" target="_blank" rel="noopener">${esc(data.files.report.label)}</a>
            <p class="muted">${report.pages} pages · ${esc(report.sampleNote)}</p>
          </div>
        </header>

        <p class="rp-note">
          <span class="badge rp-free">${esc(data.pricing.free.label)}</span>
          <span>${esc(rule.text)}${alsoPicked.length
            ? ` You also ticked ${esc(names(alsoPicked))}: each would get a report laid out like this one.`
            : ''}</span>
        </p>

        <section class="rp-questions">
          <p class="rp-questions-title">The ${report.questions.length} questions this report answers</p>
          <ol>
            ${report.questions.map((q) => `<li>${esc(q)}</li>`).join('')}
          </ol>
        </section>

        <section class="card rp-summary">
          <p class="section-title">Page one</p>
          <h2>The one-page summary</h2>
          <dl>
            ${report.summary.map((row) => `<div class="rp-row" data-summary-row>
              <dt>${esc(row.label)}</dt>
              <dd>${esc(row.value)}</dd>
            </div>`).join('')}
          </dl>
        </section>

        <figure class="rp-quote">
          <blockquote>${esc(report.pullQuote.text)}</blockquote>
          <figcaption class="muted">${esc(report.pullQuote.source)}</figcaption>
        </figure>

        <section class="rp-inside">
          <div class="rp-inside-head">
            <div>
              <p class="section-title">The rest of the report</p>
              <h2>${report.sections.length} sections, one opened here</h2>
            </div>
            ${open ? `<button type="button" class="btn btn-ghost btn-sm rp-jump" data-jump>Jump to section ${open.n}: ${esc(open.title.toLowerCase())}</button>` : ''}
          </div>
          <ol class="card rp-sections">
            ${report.sections.map((s) => sectionRow(s, report)).join('')}
          </ol>
        </section>

        <section class="card rp-next">
          <div>
            <h2>Read enough to choose?</h2>
            <p class="muted">Next we turn the list and this report into one plan: where to apply, by when, and what to do first.</p>
          </div>
          <div class="rp-next-actions">
            <button type="button" class="btn btn-ghost" data-go="list">Back to your list</button>
            <button type="button" class="btn btn-primary" data-go="decide">Decide and apply</button>
          </div>
        </section>`;

      const jump = root.querySelector('[data-jump]');
      if (jump) {
        jump.addEventListener('click', () => {
          root.querySelector('.rp-section.is-open').scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      }
    }
  });
})();
