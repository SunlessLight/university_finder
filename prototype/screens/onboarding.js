/* Screen 2 of 7: onboarding. Owner: Session A.
   Three short steps (about you / what you want / money), driven by state.onboardingStep and
   pre-filled from DATA.student so the demo needs no typing.

   What the presenter changes is kept in state.onboardingForm (an extra state key). Chips and
   inputs update it in place, without a re-render, so the keyboard focus stays where it is; only
   moving between steps calls App.setState.

   The choices offered besides the sample student's own answers (qualifications, extra
   countries, budget bands) come from DATA.intake. */
(function () {
  'use strict';

  const esc = App.esc;

  const TOP_PRIORITIES = 3;

  const STEPS = [
    { title: 'About you', lede: 'So we know whose list this is and where to send it.', fields: aboutFields },
    { title: 'What you want', lede: 'Tell us the course and where you would go. We find the universities.', fields: wantFields },
    { title: 'Money', lede: 'We cost every option for the whole degree, so this is the number we compare against.', fields: moneyFields }
  ];

  function defaults(student) {
    return {
      nickname: student.nickname,
      whatsapp: student.whatsapp,
      qualification: student.qualification,
      grades: student.grades,
      course: student.course,
      countries: student.countries.slice(),
      priorities: student.priorities.slice(0, TOP_PRIORITIES),
      budget: student.budget.band,
      scholarship: student.scholarshipNeeded ? 'yes' : 'no'
    };
  }

  // The value from DATA is always offered, even if it is not one of this screen's own options.
  function withValue(options, value) {
    return options.indexOf(value) === -1 ? [value].concat(options) : options;
  }

  function textField(form, name, label, opts) {
    const o = opts || {};
    return `
      <label class="ob-field">
        <span class="ob-label">${esc(label)}</span>
        <input class="ob-input" type="${o.type || 'text'}" name="${name}" value="${esc(form[name])}" autocomplete="off"${o.inputmode ? ' inputmode="' + o.inputmode + '"' : ''}>
        ${o.hint ? '<span class="ob-hint muted">' + esc(o.hint) + '</span>' : ''}
      </label>`;
  }

  function chipField(form, name, label, options, opts) {
    const o = opts || {};
    const picked = (value) => (Array.isArray(form[name]) ? form[name].indexOf(value) !== -1 : form[name] === value);
    return `
      <div class="ob-field" role="group" aria-label="${esc(label)}">
        <span class="ob-label">${esc(label)}</span>
        <div class="ob-chips${o.big ? ' is-big' : ''}">
          ${options.map((opt) => {
            const value = typeof opt === 'string' ? opt : opt.value;
            const text = typeof opt === 'string' ? opt : opt.label;
            return '<button type="button" class="ob-chip" data-field="' + name + '" data-value="' + esc(value) +
              '" aria-pressed="' + picked(value) + '">' + esc(text) + '</button>';
          }).join('')}
        </div>
        ${o.hint ? '<span class="ob-hint muted">' + esc(o.hint) + '</span>' : ''}
      </div>`;
  }

  function aboutFields(form, data) {
    const student = data.student;
    return textField(form, 'nickname', 'What should we call you?') +
      textField(form, 'whatsapp', 'WhatsApp number', { type: 'tel', inputmode: 'tel', hint: 'Your list is sent here. Nothing else is.' }) +
      chipField(form, 'qualification', 'What are you studying now?', withValue(data.intake.qualifications, student.qualification)) +
      textField(form, 'grades', 'Your grades', { hint: student.subjects.join(', ') + '. Predicted grades are fine.' });
  }

  function wantFields(form, data) {
    const student = data.student;
    const priorities = student.priorities.map((p) => ({ value: p, label: p.replace(/\s*\(.*\)$/, '') }));
    return textField(form, 'course', 'What do you want to study?') +
      chipField(form, 'countries', 'Where would you go?', student.countries.concat(data.intake.extraCountries), { hint: 'Pick as many as you like.' }) +
      chipField(form, 'priorities', 'What matters most to you?', priorities, { hint: 'Pick your top ' + TOP_PRIORITIES + '.' });
  }

  function moneyFields(form, data) {
    return chipField(form, 'budget', 'Total budget for the whole degree', withValue(data.intake.budgetBands, data.student.budget.band),
        { big: true, hint: 'Fees and living costs together, for all the years.' }) +
      chipField(form, 'scholarship', 'Do you need a scholarship to go?',
        [{ value: 'yes', label: 'Yes, I need one' }, { value: 'no', label: 'No' }], { big: true });
  }

  App.register('onboarding', {
    render: function (root, state, data) {
      if (!state.onboardingForm) state.onboardingForm = defaults(data.student);
      const form = state.onboardingForm;
      const total = STEPS.length;
      const n = Math.min(Math.max(state.onboardingStep, 1), total);
      const step = STEPS[n - 1];
      const last = n === total;

      root.innerHTML = `
        <form class="card ob-card" novalidate>
          <div class="ob-progress">
            <div class="ob-progress-text">
              <span class="section-title">Step ${n} of ${total}</span>
              <span class="ob-progress-names muted">${STEPS.map((s, i) =>
                '<span class="' + (i === n - 1 ? 'is-current' : i < n - 1 ? 'is-done' : '') + '">' + esc(s.title) + '</span>').join('')}</span>
            </div>
            <div class="ob-bar" role="progressbar" aria-label="Sign-up progress" aria-valuemin="1" aria-valuemax="${total}" aria-valuenow="${n}">
              <span class="ob-bar-fill" style="width:${Math.round(100 * n / total)}%"></span>
            </div>
          </div>

          <h1 tabindex="-1">${esc(step.title)}</h1>
          <p class="ob-lede muted">${esc(step.lede)}</p>

          ${step.fields(form, data)}

          <div class="ob-actions">
            ${n > 1 ? '<button type="button" class="btn btn-ghost" data-back>Back</button>' : '<span></span>'}
            ${last
              ? '<button type="submit" class="btn btn-primary btn-lg ob-next" data-go="waiting">Build my list</button>'
              : '<button type="submit" class="btn btn-primary btn-lg ob-next">Next</button>'}
          </div>
        </form>
        <p class="ob-foot muted">About 2 minutes. No account, no login.</p>`;

      function goToStep(next) {
        App.setState({ onboardingStep: next });
        window.scrollTo(0, 0);
        const heading = document.querySelector('.screen-onboarding h1');
        if (heading) heading.focus();
      }

      const formEl = root.querySelector('form');

      // Enter in a text box, or the Next button. On the last step the button carries data-go,
      // so app.js navigates and this only has to stop the page reloading.
      formEl.addEventListener('submit', function (event) {
        event.preventDefault();
        if (last) App.go('waiting'); else goToStep(n + 1);
      });

      formEl.addEventListener('input', function (event) {
        const el = event.target;
        if (el.name && el.name in form) form[el.name] = el.value;
      });

      formEl.addEventListener('click', function (event) {
        if (event.target.closest('[data-back]')) {
          goToStep(n - 1);
          return;
        }
        const chip = event.target.closest('button[data-field]');
        if (!chip) return;
        const field = chip.getAttribute('data-field');
        const value = chip.getAttribute('data-value');
        if (Array.isArray(form[field])) {
          const at = form[field].indexOf(value);
          if (at === -1) form[field].push(value); else form[field].splice(at, 1);
          chip.setAttribute('aria-pressed', String(at === -1));
        } else {
          form[field] = value;
          formEl.querySelectorAll('button[data-field="' + field + '"]').forEach(function (el) {
            el.setAttribute('aria-pressed', String(el === chip));
          });
        }
      });
    }
  });
})();
