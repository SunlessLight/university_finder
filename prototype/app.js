/*
 * app.js — the tiny screen switcher. Owner: Session 1. Read-only for Sessions A, B, C.
 *
 * The contract
 *   App.register(id, { render(root, state, data) })
 *       render fills root (sets innerHTML, attaches listeners). It runs again on every state
 *       change, each time with a brand-new root element that is already in the page. Anything
 *       that must survive a re-render (which step, which rows are open) belongs in App.state.
 *   App.go(id)          show a screen, scroll to top, update the journey bar
 *   App.setState(patch) merge into App.state and re-render the current screen (scroll is kept)
 *   App.state           { ready: false, onboardingStep: 1, picked: [] }
 *   data-go="<id>"      on any element: navigates on click. Handled once, here.
 *
 * Extras (not in the plan's contract, safe to use)
 *   App.current         id of the screen being shown
 *   App.esc(text)       escape text before putting it in innerHTML
 *   App.uni(id)         look up one university in DATA.universities
 *   App.fmt.myr(n)      1499002      -> "RM 1,499,002"
 *   App.fmt.myrShort(n) 1499002      -> "RM 1.50M"     (383438 -> "RM 383k")
 *   App.fmt.date(iso)   "2027-01-01" -> "1 Jan 2027"   (null -> "To confirm")
 *   index.html#<id>     opens straight on that screen (handy while building one screen)
 */
(function () {
  'use strict';

  const ORDER = ['landing', 'onboarding', 'waiting', 'results', 'list', 'report', 'decide'];
  const JOURNEY = [
    { label: 'Sign up', screens: ['landing', 'onboarding', 'waiting'] },
    { label: 'Your list', screens: ['results', 'list'], needsReady: true },
    { label: 'Reports', screens: ['report'] },
    { label: 'Decide and apply', screens: ['decide'] }
  ];
  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const ESCAPES = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };

  const screens = {};
  let mount = null;
  let journeyEl = null;

  function esc(text) {
    return String(text == null ? '' : text).replace(/[&<>"']/g, (c) => ESCAPES[c]);
  }

  function renderScreen() {
    const id = App.current;
    const root = document.createElement('div');
    root.className = 'screen screen-' + id;
    mount.replaceChildren(root);
    try {
      screens[id].render(root, App.state, window.DATA);
    } catch (err) {
      // One broken screen must not take the journey bar down with it.
      console.error('Screen "' + id + '" failed to render:', err);
      root.innerHTML = '<div class="card error-card"><h2>This screen hit an error</h2>' +
        '<p class="muted">' + esc(err && err.message) + '</p></div>';
    }
  }

  function renderJourney() {
    const current = JOURNEY.findIndex((step) => step.screens.includes(App.current));
    journeyEl.innerHTML = JOURNEY.map((step, i) => {
      const cls = ['journey-step'];
      if (i === current) cls.push('is-current');
      if (i < current) cls.push('is-done');
      return (i ? '<span class="journey-sep" aria-hidden="true"></span>' : '') +
        '<button type="button" class="' + cls.join(' ') + '" data-journey="' + i + '"' +
        (i === current ? ' aria-current="step"' : '') + '>' +
        '<span class="journey-num">' + (i < current ? '&#10003;' : i + 1) + '</span>' +
        '<span class="journey-label">' + esc(step.label) + '</span></button>';
    }).join('');
  }

  function onClick(event) {
    const target = event.target instanceof Element ? event.target : null;
    if (!target) return;
    const stepEl = target.closest('[data-journey]');
    if (stepEl) {
      const step = JOURNEY[Number(stepEl.getAttribute('data-journey'))];
      App.go(step.needsReady && !App.state.ready ? 'waiting' : step.screens[0]);
      return;
    }
    const goEl = target.closest('[data-go]');
    if (goEl) {
      event.preventDefault();
      App.go(goEl.getAttribute('data-go'));
    }
  }

  function onHashChange() {
    const id = location.hash.slice(1);
    if (screens[id] && id !== App.current) App.go(id);
  }

  const App = {
    state: { ready: false, onboardingStep: 1, picked: [] },
    current: null,

    register: function (id, screen) {
      if (!screen || typeof screen.render !== 'function') {
        console.error('App.register("' + id + '") needs an object with a render function.');
        return;
      }
      screens[id] = screen;
    },

    go: function (id) {
      if (!screens[id]) {
        console.error('App.go: no screen is registered as "' + id + '".');
        return;
      }
      App.current = id;
      if (location.hash.slice(1) !== id) location.hash = id;
      renderScreen();
      renderJourney();
      window.scrollTo(0, 0);
    },

    setState: function (patch) {
      Object.assign(App.state, patch);
      if (!App.current) return;
      const y = window.scrollY;
      renderScreen();
      renderJourney();
      window.scrollTo(0, y);
    },

    start: function () {
      mount = document.getElementById('app');
      journeyEl = document.getElementById('journey');
      document.addEventListener('click', onClick);
      window.addEventListener('hashchange', onHashChange);
      const fromHash = location.hash.slice(1);
      const first = screens[fromHash] ? fromHash : ORDER[0];
      // Opening straight on a later screen means the list already exists.
      if (ORDER.indexOf(first) > ORDER.indexOf('waiting')) App.state.ready = true;
      App.go(first);
    },

    esc: esc,

    uni: function (id) {
      return window.DATA.universities.find((u) => u.id === id) || null;
    },

    fmt: {
      myr: function (n) {
        return 'RM ' + Math.round(n).toLocaleString('en-US');
      },
      myrShort: function (n) {
        return n >= 1e6 ? 'RM ' + (n / 1e6).toFixed(2) + 'M' : 'RM ' + Math.round(n / 1000) + 'k';
      },
      date: function (iso) {
        const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '');
        return m ? Number(m[3]) + ' ' + MONTHS[Number(m[2]) - 1] + ' ' + m[1] : 'To confirm';
      }
    }
  };

  window.App = App;
})();
