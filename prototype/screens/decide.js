/* Screen 7 of 7: decide. Owner: Session C.
   The end goal, all from DATA.decision: the recommended university, the application list,
   the deadline calendar and the apply steps. Every name, cost and date is read from DATA. */
(function () {
  'use strict';

  const esc = App.esc;
  const BANDS = [['reach', 'Reach'], ['match', 'Match'], ['safety', 'Safety']];
  const ROUNDS = { early: 'Early round', regular: 'Regular round' };

  /* DATA keeps dates in year-month-day form inside its sentences; show them the way
     App.fmt.date does. */
  function withDates(text) {
    return esc(text).replace(/\d{4}-\d{2}-\d{2}/g, (iso) => App.fmt.date(iso));
  }

  function verifiedBadge(uni) {
    return uni.verified
      ? '<span class="badge badge-verified">Checked on official page</span>'
      : '<span class="badge badge-unverified">Not verified</span>';
  }

  function hero(decision, uni) {
    const pick = decision.plan.find((p) => p.id === uni.id);
    const deadline = decision.deadlines.find((d) => d.universityId === uni.id);
    return `<section class="dc-hero">
        <div class="dc-hero-main">
          <p class="dc-hero-label">Apply here first</p>
          <h2>${esc(uni.university)}</h2>
          <p class="dc-hero-course">${esc(uni.course)} · ${esc(uni.city)}, ${esc(uni.country)}</p>
          <p class="dc-hero-badges">
            <span class="badge badge-${uni.band}">${esc(uni.admissionLikelihood)}</span>
            ${verifiedBadge(uni)}
          </p>
          ${pick ? `<p class="dc-hero-reason">${esc(pick.reason)}</p>` : ''}
          <button type="button" class="btn btn-ghost" data-go="report">Read the ${esc(uni.shortName)} report</button>
        </div>
        <dl class="dc-stats">
          ${deadline ? `<div><dt>${esc(deadline.what)}</dt><dd>${App.fmt.date(deadline.date)}</dd></div>` : ''}
          <div><dt>Your grades vs the entry bar</dt><dd>${esc(uni.gradesVsEntryBar)}</dd></div>
          <div><dt>Full price, before any aid</dt><dd>${App.fmt.myr(uni.approxTotalMyr)}</dd></div>
        </dl>
      </section>`;
  }

  function planRow(pick, i, decision) {
    const uni = App.uni(pick.id);
    return `<li class="dc-pick" data-plan="${esc(uni.id)}">
        <span class="dc-num">${i + 1}</span>
        <div class="dc-pick-text">
          <p class="dc-pick-name">
            <strong>${esc(uni.shortName)}</strong>
            <span class="badge badge-${uni.band}">${esc(uni.admissionLikelihood)}</span>
            <span class="dc-round">${ROUNDS[pick.round] || esc(pick.round)}</span>
            ${uni.id === decision.recommendedId ? '<span class="dc-first">First choice</span>' : ''}
          </p>
          <p class="muted dc-pick-course">${esc(uni.course)} · ${esc(uni.country)}</p>
          <p class="dc-pick-reason">${esc(pick.reason)}</p>
        </div>
        <div class="dc-pick-cost">
          <strong>${App.fmt.myr(uni.approxTotalMyr)}</strong>
          <span class="muted">full price, whole degree</span>
          ${verifiedBadge(uni)}
        </div>
      </li>`;
  }

  /* One calendar entry per date, so universities sharing a deadline sit under one tile. */
  function calendar(deadlines) {
    const groups = [];
    deadlines.forEach((d) => {
      const last = groups[groups.length - 1];
      if (last && last.date === d.date) last.items.push(d);
      else groups.push({ date: d.date, items: [d] });
    });
    return groups.map((g, i) => {
      const parts = g.date ? App.fmt.date(g.date).split(' ') : null;
      return `<li class="dc-day${i === 0 ? ' is-next' : ''}">
          <div class="dc-tile">${parts
            ? `<span class="dc-tile-day">${parts[0]}</span><span class="dc-tile-month">${parts.slice(1).join(' ')}</span>`
            : `<span class="dc-tile-open">${App.fmt.date(g.date)}</span>`}</div>
          <div class="dc-day-items">
            ${i === 0 ? '<p class="dc-next-label">First deadline</p>' : ''}
            ${g.items.map((d) => `<div class="dc-deadline" data-deadline="${esc(d.universityId)}">
              <p class="dc-deadline-name">
                <strong>${esc(d.university)}</strong> · ${esc(d.what)}
                ${d.confirmed ? '' : '<span class="badge badge-unverified">Confirm the exact date</span>'}
              </p>
              <p class="muted">${withDates(d.text)}</p>
            </div>`).join('')}
          </div>
        </li>`;
    }).join('');
  }

  App.register('decide', {
    render: function (root, state, data) {
      const decision = data.decision;
      const uni = App.uni(decision.recommendedId);
      const guide = data.deliverables.find((d) => d.id === 'apply');

      root.innerHTML = `
        <header class="dc-head">
          <p class="section-title">Decide and apply · ${esc(data.student.nickname)}'s plan</p>
          <h1>${esc(decision.headline)}</h1>
          <p class="muted">${esc(data.student.sampleNote)}</p>
        </header>

        ${hero(decision, uni)}

        <section class="dc-block">
          <div class="dc-block-head">
            <div>
              <p class="section-title">Where to apply</p>
              <h2>${decision.plan.length} applications, balanced on purpose</h2>
            </div>
            <p class="dc-balance">
              ${BANDS.map(([band, label]) => `<span class="badge badge-${band}">${decision.balance[band]} ${label}</span>`).join('')}
            </p>
          </div>
          <ol class="card dc-plan">
            ${decision.plan.map((pick, i) => planRow(pick, i, decision)).join('')}
          </ol>
        </section>

        <div class="dc-two">
          <section class="dc-block">
            <p class="section-title">When</p>
            <h2>Deadline calendar</h2>
            <ol class="card dc-cal">
              ${calendar(decision.deadlines)}
            </ol>
          </section>

          <section class="dc-block">
            <p class="section-title">How</p>
            <h2>What to do, in order</h2>
            <ol class="card dc-steps">
              ${decision.applySteps.map((step) => `<li class="dc-step" data-step>
                <h3>${esc(step.title)}</h3>
                <p class="muted">${withDates(step.detail)}</p>
              </li>`).join('')}
            </ol>
          </section>
        </div>

        <div class="dc-two">
          <section class="dc-risks">
            <p class="section-title">Still open</p>
            <h2>What could change this plan</h2>
            <ul>
              ${decision.openRisks.map((risk) => `<li data-risk>${esc(risk)}</li>`).join('')}
            </ul>
          </section>

          ${guide ? `<section class="card dc-guide">
            <p class="section-title">Going deeper</p>
            <h2>${esc(guide.name)} <span class="badge dc-paid">${esc(data.pricing.paid.label)}</span></h2>
            <p>${esc(guide.oneLine)}</p>
            <p class="muted">The steps on this page are the outline. The guide is the full version, one per country you apply to.</p>
          </section>` : ''}
        </div>

        <footer class="dc-foot">
          <button type="button" class="btn btn-ghost" data-go="list">Back to your list</button>
          <button type="button" class="btn btn-ghost" data-go="landing">Back to the start</button>
        </footer>`;
    }
  });
})();
