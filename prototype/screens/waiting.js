/* Screen 3 of 7: waiting. Owner: Session A.
   "We're building your list": what is happening now, the WhatsApp promise, and a preview of
   what comes back so the page is not empty. Once state.ready is true it becomes "your list is
   ready" with a button to the results.

   Reads what the presenter typed in onboarding (state.onboardingForm), falling back to
   DATA.student when they opened this screen directly.

   Screen-only constant (not in DATA; named here so Session 2 can move it):
     PREVIEW_KEYS  the spreadsheet columns shown in the preview. Their labels come from DATA.columns. */
(function () {
  'use strict';

  const esc = App.esc;

  const PREVIEW_KEYS = ['university', 'admissionLikelihood', 'gradesVsEntryBar', 'approxTotalMyr', 'keyDeadline'];
  const PREVIEW_BANDS = ['reach', 'match', 'match', 'safety'];

  function steps(who) {
    return [
      { title: 'Got your answers',
        detail: who.qualification + ', ' + who.grades + ' · ' + who.course },
      { title: 'Finding universities that fit',
        detail: who.course + ' in ' + who.countries.join(', ') + '.' },
      { title: 'Looking up fees, entry requirements and deadlines',
        detail: 'On the university\'s own page where we can. Each row says whether it was checked there.' },
      { title: 'Costing each whole degree in ringgit',
        detail: 'Fees and living costs for all the years, so a 3-year and a 4-year degree can be compared.' },
      { title: 'Sorting into Reach, Match and Safety',
        detail: 'Against your grades, so the list is balanced and not just the famous names.' },
      { title: 'Sending it to your WhatsApp',
        detail: 'One message with a link back to this page.' }
    ];
  }

  function stepList(who, ready) {
    // Before the list is ready: the first step is done and the second is the one in progress.
    const active = 1;
    return '<ol class="wt-steps">' + steps(who).map((s, i) => {
      const status = ready || i < active ? 'is-done' : i === active ? 'is-active' : 'is-pending';
      return `
        <li class="wt-step ${status}"${status === 'is-active' ? ' aria-current="step"' : ''}>
          <span class="wt-dot" aria-hidden="true">${status === 'is-done' ? '&#10003;' : ''}</span>
          <div>
            <p class="wt-step-title">${esc(s.title)}</p>
            <p class="wt-step-detail muted">${esc(s.detail)}</p>
          </div>
        </li>`;
    }).join('') + '</ol>';
  }

  function preview(data, ready) {
    const cols = PREVIEW_KEYS.map((key) => data.columns.find((c) => c.key === key)).filter(Boolean);
    const list = data.deliverables[0];
    const later = data.deliverables.slice(1);
    return `
      <aside class="card wt-preview">
        <p class="section-title">${ready ? 'What is in it' : 'What is coming'}</p>
        <h2>${esc(list.name)}</h2>
        <p class="muted">${esc(list.oneLine)}</p>
        <div class="wt-ghost" aria-hidden="true">
          <div class="wt-ghost-row wt-ghost-head">${cols.map((c) => '<span>' + esc(c.label) + '</span>').join('')}</div>
          ${PREVIEW_BANDS.map((band, i) => `
            <div class="wt-ghost-row">
              <span><i class="wt-bone" style="width:${[72, 58, 64, 80][i]}%"></i></span>
              <span><i class="wt-bone wt-bone-pill badge-${band}"></i></span>
              <span><i class="wt-bone" style="width:${[60, 44, 44, 52][i]}%"></i></span>
              <span><i class="wt-bone" style="width:${[78, 62, 62, 70][i]}%"></i></span>
              <span><i class="wt-bone" style="width:${[66, 70, 54, 60][i]}%"></i></span>
            </div>`).join('')}
        </div>
        <p class="wt-preview-note muted">${data.columns.length} columns for each university, as a spreadsheet you can download and keep.</p>
        <p class="section-title wt-later-title">After that</p>
        <ul class="wt-later">
          ${later.map((d) => '<li><strong>' + esc(d.name) + '</strong><span class="muted">' + esc(d.oneLine) + '</span></li>').join('')}
        </ul>
      </aside>`;
  }

  App.register('waiting', {
    render: function (root, state, data) {
      const form = state.onboardingForm || {};
      const s = data.student;
      const who = {
        nickname: form.nickname || s.nickname,
        qualification: form.qualification || s.qualification,
        grades: form.grades || s.grades,
        course: form.course || s.course,
        countries: form.countries && form.countries.length ? form.countries : s.countries
      };
      const ready = state.ready;

      const note = ready
        ? '<p class="wt-note"><strong>It is ready.</strong> This is the page your WhatsApp message brings you back to.</p>'
        : '<p class="wt-note"><strong>We\'ll WhatsApp you' + (form.whatsapp ? ' on ' + esc(form.whatsapp) : '') +
          ' when it\'s ready.</strong> You can close this page. There is nothing to refresh and no login to remember.</p>';

      root.innerHTML = `
        <div class="wt-layout">
          <section class="card wt-status">
            <p class="section-title">${ready ? 'Done' : 'In progress'}</p>
            <h1>${ready ? 'Your list is ready' : 'We\'re building your list'}, ${esc(who.nickname)}</h1>
            <p class="wt-lede muted">${ready
              ? 'Here is what we did with your answers.'
              : 'This is real research, so it is not instant. Here is what happens to your answers.'}</p>
            ${stepList(who, ready)}
            ${note}
            <div class="wt-actions">
              ${ready
                ? '<button type="button" class="btn btn-primary" data-go="results">See your list</button>'
                : '<button type="button" class="btn btn-ghost btn-sm wt-skip" data-skip>Skip ahead (demo)</button>'}
            </div>
          </section>
          ${preview(data, ready)}
        </div>`;

      // Demo control: pretend the list has been built, then show it.
      const skip = root.querySelector('[data-skip]');
      if (skip) {
        skip.addEventListener('click', function () {
          App.setState({ ready: true });
          App.go('results');
        });
      }
    }
  });
})();
