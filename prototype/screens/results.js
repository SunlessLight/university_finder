/* Screen 4 of 7: results, the "welcome back" page. Owner: Session B.
   Every name, cost and grade is read from DATA; nothing is retyped here.
   data-card / data-cost / data-grades / data-finding are hooks for checks, not for styling. */
(function () {
  'use strict';

  const esc = App.esc;

  const list = (items) => items.length > 1
    ? items.slice(0, -1).join(', ') + ' and ' + items[items.length - 1] : items[0] || '';

  const verifiedBadge = (u) => u.verified
    ? '<span class="badge badge-verified">Checked on official page</span>'
    : '<span class="badge badge-unverified">Not verified</span>';

  function card(u) {
    return `
      <article class="card pick pick-${u.band}" data-card="${esc(u.id)}">
        <div class="pick-top">
          <span class="badge badge-${u.band}">${esc(u.admissionLikelihood)}</span>
          <span class="pick-place muted">${esc(u.place)}</span>
        </div>
        <h3>${esc(u.university)}</h3>
        <p class="pick-course">${esc(u.course)}</p>
        <dl class="pick-facts">
          <div>
            <dt>Total cost, whole degree</dt>
            <dd class="pick-cost" data-cost>${App.fmt.myr(u.approxTotalMyr)}</dd>
            <dd class="pick-note muted">${esc(u.durationYears)} years of tuition and living, before any scholarship</dd>
          </div>
          <div>
            <dt>Your grades vs the entry bar</dt>
            <dd class="pick-grades" data-grades>${esc(u.gradesVsEntryBar)}</dd>
            <dd class="pick-note muted">${esc(u.studentGrades)}</dd>
          </div>
        </dl>
        <div class="pick-foot">${verifiedBadge(u)}</div>
      </article>`;
  }

  App.register('results', {
    render: function (root, state, data) {
      const s = data.student;
      const unis = data.universities;
      const picks = data.top5.map(App.uni).filter(Boolean);
      const rest = unis.length - picks.length;
      const spread = data.bands.map((b) =>
        `<span class="badge badge-${b.key}">${unis.filter((u) => u.band === b.key).length} ${b.label}</span>`).join('');
      const download = `<a class="btn btn-ghost" href="${esc(data.files.list.href)}" download>${esc(data.files.list.label)}</a>`;

      root.innerHTML = `
        <header class="hero">
          <p class="section-title">Your list is ready</p>
          <h1>Welcome back, ${esc(s.nickname)}. Here is what we found.</h1>
          <p class="lede muted">We researched ${unis.length} universities for ${esc(s.course)} across
            ${esc(list(s.countries))}, measured against your ${esc(s.qualification)} (${esc(s.grades)}).</p>
          <p class="spread"><span class="spread-label">Your spread</span>${spread}</p>
          <div class="hero-actions">
            <button type="button" class="btn btn-primary" data-go="list">See the full list</button>
            ${download}
          </div>
        </header>

        <section class="block">
          <p class="section-title">What we found</p>
          <ol class="findings grid">
            ${data.findings.map((f) => `<li class="card" data-finding>${esc(f)}</li>`).join('')}
          </ol>
        </section>

        <section class="block">
          <p class="section-title">Where to start</p>
          <h2>${picks.length} to look at first</h2>
          <p class="muted">A mix of reaches, matches and safeties, not simply the ${picks.length} highest scores.</p>
          <div class="picks grid">
            ${picks.map(card).join('')}
            <div class="card pick-more">
              <h3>${rest > 0 ? 'Plus ' + rest + ' more on your full list' : 'See them side by side'}</h3>
              <p class="muted">Every university with its cost, deadline and scholarship route. Tick the ones you want a deep report on.</p>
              <button type="button" class="btn btn-ghost" data-go="list">See the full list</button>
            </div>
          </div>
        </section>`;
    }
  });
})();
