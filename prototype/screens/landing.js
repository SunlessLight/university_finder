/* Screen 1 of 7: landing. Owner: Session A.
   The pitch, a peek at a real list, the three deliverables, early-tester feedback, and one
   button into onboarding.

   Screen-only constant (not in DATA; named here so Session 2 can move it):
     TIER_OF  which pricing tier each deliverable sits in. The words come from DATA.pricing. */
(function () {
  'use strict';

  const esc = App.esc;

  const TIER_OF = { list: 'free', report: 'firstFree', apply: 'paid' };
  const PEEK_BANDS = ['reach', 'match', 'safety'];
  const SHORT_QUOTE = 120;   // characters; shorter quotes sit under their score card

  function tierTag(id, pricing) {
    const tier = TIER_OF[id];
    if (tier === 'paid') return { cls: 'is-paid', text: pricing.paid.label };
    if (tier === 'free') return { cls: 'is-free', text: pricing.free.label };
    const n = pricing.reportRule.freeCount;
    return { cls: 'is-free', text: (n === 1 ? 'First one ' : 'First ' + n + ' ') + pricing.free.label.toLowerCase() };
  }

  function peekRow(u) {
    return `
      <li class="ld-peek-row">
        <div class="ld-peek-main">
          <strong>${esc(u.shortName)}</strong>
          <span class="badge badge-${u.band}">${esc(u.admissionLikelihood.split(' (')[0])}</span>
          <span class="ld-peek-cost">${esc(App.fmt.myr(u.approxTotalMyr))}</span>
        </div>
        <div class="ld-peek-sub muted">${esc(u.course)}</div>
        <div class="ld-peek-meta">
          <span class="muted">Grades vs entry bar: ${esc(u.gradesVsEntryBar)}</span>
          <span class="badge badge-${u.verified ? 'verified' : 'unverified'}">${u.verified ? 'Checked on official page' : 'Not verified'}</span>
        </div>
      </li>`;
  }

  function peek(data) {
    const s = data.student;
    const featured = data.top5.map(App.uni).filter(Boolean);
    const rows = PEEK_BANDS.map((band) => featured.find((u) => u.band === band)).filter(Boolean);
    return `
      <aside class="card ld-peek" aria-label="A sample list">
        <p class="section-title">A real list, anonymised</p>
        <p class="ld-peek-who"><strong>${esc(s.nickname)}</strong> · ${esc(s.qualification)}, ${esc(s.grades)} · ${esc(s.course)}</p>
        <ul class="ld-peek-rows">${rows.map(peekRow).join('')}</ul>
        <p class="ld-peek-foot muted">${rows.length} of the ${data.universities.length} universities on this list. Costs are for the whole degree, in ringgit, before any scholarship. ${esc(s.sampleNote)}</p>
      </aside>`;
  }

  function deliverable(d, i, pricing) {
    const tag = tierTag(d.id, pricing);
    return `
      <article class="card ld-deliverable">
        <div class="ld-deliverable-head">
          <span class="ld-num">${i + 1}</span>
          <span class="ld-tier ${tag.cls}">${esc(tag.text)}</span>
        </div>
        <h3>${esc(d.name)}</h3>
        <p class="muted">${esc(d.oneLine)}</p>
      </article>`;
  }

  function bars(group) {
    return `
      <div class="ld-bars">
        <p class="ld-bars-title">${esc(group.title)}</p>
        ${group.items.map((item) => `
          <div class="ld-bar">
            <span class="ld-bar-label">${esc(item.label)}</span>
            <span class="ld-bar-track"><span class="ld-bar-fill" style="width:${Math.round(100 * item.count / group.outOf)}%"></span></span>
            <span class="ld-bar-count">${item.count} of ${group.outOf}</span>
          </div>`).join('')}
      </div>`;
  }

  function quote(text, block) {
    return `
      <figure class="card ld-quote">
        <blockquote>&ldquo;${esc(text)}&rdquo;</blockquote>
        <figcaption class="muted">Early tester, ${esc(block.title.toLowerCase())}</figcaption>
      </figure>`;
  }

  function score(block, label) {
    return `
      <div class="ld-score-col">
        <article class="card ld-score">
          <p class="section-title">${esc(block.title)}</p>
          <p class="ld-score-figure"><strong>${block.score}</strong><span> / ${block.outOf}</span></p>
          <p class="ld-score-who">${block.respondents} ${esc(label.toLowerCase())}</p>
          <p class="ld-score-question muted">&ldquo;${esc(block.question)}&rdquo;</p>
          ${block.bars.map(bars).join('')}
        </article>
        ${block.quotes.filter((text) => text.length < SHORT_QUOTE).map((text) => quote(text, block)).join('')}
      </div>`;
  }

  function longQuotes(feedback) {
    return [feedback.list, feedback.report].map((block) =>
      block.quotes.filter((text) => text.length >= SHORT_QUOTE).map((text) => quote(text, block)).join('')).join('');
  }

  App.register('landing', {
    render: function (root, state, data) {
      const fb = data.feedback;
      root.innerHTML = `
        <section class="ld-hero">
          <div class="ld-hero-copy">
            <p class="section-title">${esc(data.brand.name)}</p>
            <h1>${esc(data.brand.tagline)}</h1>
            <p class="ld-lede">Fill in a 2-minute form. We research the universities that fit you, cost each
              whole degree in ringgit, and send the list to your WhatsApp.</p>
            <button type="button" class="btn btn-primary ld-start" data-go="onboarding">Start, 2 minutes</button>
            <p class="ld-hero-note muted">No account, no login.</p>
          </div>
          ${peek(data)}
        </section>

        <section class="ld-section">
          <p class="section-title">What you get</p>
          <h2>Three things, in the order you need them</h2>
          <div class="grid ld-deliverables">
            ${data.deliverables.map((d, i) => deliverable(d, i, data.pricing)).join('')}
          </div>
          <p class="ld-rule muted">${esc(data.pricing.reportRule.text)}</p>
        </section>

        <section class="ld-section">
          <p class="section-title">${esc(fb.label)}</p>
          <h2>What the first students told us</h2>
          <div class="grid ld-scores">
            ${score(fb.list, fb.label)}
            ${score(fb.report, fb.label)}
          </div>
          <div class="ld-quotes">${longQuotes(fb)}</div>
        </section>`;

      // A fresh run of the demo always starts the form at step 1. This runs before the global
      // data-go handler, which then does the navigation.
      root.querySelector('.ld-start').addEventListener('click', function () {
        App.state.onboardingStep = 1;
      });
    }
  });
})();
