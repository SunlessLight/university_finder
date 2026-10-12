/*
 * data.js — window.DATA. Owner: Session 1. Read-only for Sessions A, B, C.
 *
 * Anything shown on more than one screen (names, costs, grades, prices, dates) lives here.
 * Never retype a number in a screen file: read it from DATA.
 *
 * Only the anonymised sample student ("Arif") is used. Sources:
 *   business/sales/sample_pack/sample_master_list.csv          -> columns, universities
 *   business/sales/sample_pack/sample_university-report_MIT.pdf -> report summary, why here / why hesitate
 *   business/university_report.md ("What is inside a report")   -> report.sections
 *   business/sales/pitch/university-research-service-poster.html -> brand, feedback, report.pullQuote
 *   business/sales/service-tiers.md                             -> deliverables, pricing wording
 *   business/decide_report.md, business/apply_guide_report.md   -> shape of decision
 *
 * window.DATA
 *   brand         { name, tagline }
 *   student       { nickname, isSample, sampleNote, whatsapp, qualification, grades, subjects[],
 *                   course, countries[], budget { band, ceilingMyr }, scholarshipNeeded, priorities[] }
 *   intake        { qualifications[], extraCountries[], budgetBands[] } the choices the sign-up
 *                   form offers besides the sample student's own answers
 *   bands[]       { key, label } reach / match / safety, in display order
 *   columns[]     { key, label } for all 35 spreadsheet columns, in spreadsheet order
 *   columnGroups[] { title, keys[] } how those columns group when a list row is opened. A column
 *                   named in no group falls into the last one
 *   universities[] one object per spreadsheet row: the 35 column keys, plus
 *                   id            stable id, e.g. "mit"
 *                   shortName     "MIT"
 *                   band          "reach" | "match" | "safety"  (from admissionLikelihood; use
 *                                 with the .badge-<band> classes)
 *                   verified      true when infoSource is "Official page"
 *                   deadlineDate  first YYYY-MM-DD in keyDeadline, or null
 *                   place         "City · Country" (a city-state is named once: "Singapore")
 *   top5[]        university ids for the results cards (a Reach / Match / Safety spread)
 *   findings[]    one-line "what we found" strings, computed from the rows
 *   deliverables[] { id, name, oneLine, tier } the three things a student gets. tier is "free",
 *                   "firstFree" or "paid"; the Apply Guide also has scope ("one per country...")
 *   report        MIT: { universityId, title, sampleNote, pages, questions[], summary[{label,value}],
 *                   sections[{n,title,tells,question}], openSection (the n of the section shown
 *                   in full), whyHere[{theme,text}], whyHesitate[{theme,text}], pullQuote{text,source} }
 *   decision      { recommendedId, headline, balance{reach,match,safety}, rounds{early,regular},
 *                   plan[{id,round,reason}],
 *                   deadlines[{universityId,university,date,rolling,what,text,confirmed}],
 *                   applySteps[{title,detail}], openRisks[] }
 *   feedback      { label, list{...}, report{...} } exactly as printed on the poster
 *   pricing       { free{label,items[]}, paid{label,items[]}, reportRule{freeCount,text}, pricePerReport }
 *   files         { list{href,label}, report{href,label} }
 */
(function () {
  'use strict';

  /* ---- GENERATED from sample_master_list.csv. Do not hand-edit these two blocks. ---- */

  const COLUMNS = /*@COLUMNS@*/;

  const ROWS = /*@UNIVERSITIES@*/;

  /* ---- GENERATED from business/university_report.md, "What is inside a report". ---- */

  const REPORT_SECTIONS = /*@REPORT_SECTIONS@*/;

  /* ---- Helpers (local to this file) ---- */

  const ISO_DATE = /\d{4}-\d{2}-\d{2}/g;
  const rm = (n) => 'RM ' + Math.round(n).toLocaleString('en-US');
  const byId = (id) => ROWS.find((u) => u.id === id);
  const names = (rows) => {
    const n = rows.map((u) => u.shortName);
    return n.length > 1 ? n.slice(0, -1).join(', ') + ' and ' + n[n.length - 1] : n[0] || '';
  };

  /* ---- Fields derived from each row ---- */

  ROWS.forEach((u) => {
    u.band = /^reach/i.test(u.admissionLikelihood) ? 'reach'
      : /^match/i.test(u.admissionLikelihood) ? 'match' : 'safety';
    u.verified = u.infoSource === 'Official page';
    u.deadlineDate = (u.keyDeadline.match(ISO_DATE) || [null])[0];
    /* "Singapore · Singapore" reads as a mistake, so a city-state is shown once. */
    u.place = u.city === u.country ? u.country : u.city + ' · ' + u.country;
  });

  const bands = [
    { key: 'reach', label: 'Reach' },
    { key: 'match', label: 'Match' },
    { key: 'safety', label: 'Safety' }
  ];

  /* How the spreadsheet columns group when a list row is opened. Titles only: each column's
     label and value still come from COLUMNS and the row. */
  const columnGroups = [
    { title: 'The course', keys: ['courseAtAGlance', 'studentLife', 'intake'] },
    { title: 'Getting in', keys: ['entryRequirements', 'studentGrades', 'englishReq', 'howToApply', 'keyDeadline'] },
    { title: 'What it costs', keys: ['annualTuition', 'totalTuition', 'estLivingPerYear', 'durationYears', 'moneyToShowVisa'] },
    { title: 'Scholarships', keys: ['scholarshipAndPortal', 'scholarshipCoverage', 'scholarshipCompetitiveness', 'howToGetScholarship'] },
    { title: 'After you graduate', keys: ['workRightsAfterGraduating', 'recognisedInMalaysia'] },
    { title: 'How it ranks', keys: ['subjectRank', 'overallRank', 'desirability', 'tier', 'listStatus'] },
    { title: 'Good to know', keys: [] }
  ];

  /* ---- Student (anonymised sample) ---- */

  const priorities = ['Scholarship', 'Hands-on experience', 'Ranking', 'Location', 'Employability',
    'Recognition (hard gate)'];

  /* What the sign-up form offers. All placeholder choices for the demo, none are facts about
     the sample student. budgetBands are the intake form's three bands, lowest first. */
  const intake = {
    qualifications: ['A-Levels', 'STPM', 'IB', 'UEC', 'Foundation'],
    extraCountries: ['Hong Kong', 'Germany', 'Taiwan'],
    budgetBands: ['Under RM 500,000', 'RM 500,000 to 1,000,000', 'Above RM 1,000,000']
  };

  const student = {
    nickname: 'Arif',
    isSample: true,
    sampleNote: 'Sample student. A real end-to-end search with the name, school and family finances removed.',
    whatsapp: '012-345 6789',   /* made up, so the sign-up form has something to show */
    qualification: intake.qualifications[0],
    grades: ROWS[0].studentGrades,
    subjects: ['Maths', 'Further Maths', 'Physics', 'Chemistry'],
    course: 'Mechanical Engineering (robotics)',
    countries: ROWS.map((u) => u.country).filter((c, i, all) => all.indexOf(c) === i),
    /* The sample pack only says "a lower-income band". This is the intake form's lowest budget
       option, used so the onboarding screen has something to pre-fill. */
    budget: { band: intake.budgetBands[0], ceilingMyr: 500000 },
    scholarshipNeeded: true,
    priorities: priorities
  };

  /* ---- Results: top picks and findings ---- */

  const top5 = ['mit', 'oxford', 'nus', 'ntu', 'unsw'];

  const total = ROWS.length;
  const clearing = ROWS.filter((u) => /above|meets/i.test(u.gradesVsEntryBar)).length;
  const reachCount = ROWS.filter((u) => u.band === 'reach').length;
  const byCost = ROWS.slice().sort((a, b) => a.approxTotalMyr - b.approxTotalMyr);
  const cheapest = byCost[0];
  const dearest = byCost[byCost.length - 1];
  const needBlind = ROWS.filter((u) => u.listStatus !== 'Rejected' &&
    /need[- ]blind/i.test(u.scholarshipAndPortal + ' ' + u.scholarshipCoverage + ' ' + u.scholarshipCompetitiveness));
  const cut = ROWS.filter((u) => u.listStatus === 'Rejected');
  const unverified = ROWS.filter((u) => !u.verified);

  const findings = [
    `Your grades clear the published entry bar at ${clearing === total ? 'all ' + total : clearing + ' of ' + total} universities. ` +
      `The ${reachCount} marked Reach are a stretch because they are very selective, not because your grades fall short.`,
    `The whole degree costs from ${rm(cheapest.approxTotalMyr)} (${cheapest.shortName}) to ${rm(dearest.approxTotalMyr)} (${dearest.shortName}) ` +
      `before any scholarship. That is more than ${Math.floor(dearest.approxTotalMyr / cheapest.approxTotalMyr)} times the price for the same course area.`,
    `${names(needBlind)} decide admission without looking at whether you asked for aid, then cover the full gap. ` +
      `${names(cut)} gives international undergraduates no aid, so we cut it from your list.`,
    `${total - unverified.length} of ${total} rows are checked on the official university page. ` +
      (unverified.length
        ? `The other ${unverified.length} (${names(unverified)}) stay marked "Not verified" until they are.`
        : 'Any row we cannot check stays marked "Not verified" until it is.')
  ];

  /* ---- The three deliverables (names from the poster, one-liners from service-tiers.md) ---- */

  const deliverables = [
    { id: 'list', name: 'The List', tier: 'free',
      oneLine: 'Know your real options, costed in ringgit and sorted into reaches and safeties.' },
    { id: 'report', name: 'The Report', tier: 'firstFree',
      oneLine: 'For your favourites: can I get in, will I belong, and what will it take?' },
    { id: 'apply', name: 'The Apply Guide', tier: 'paid',
      oneLine: 'Now go do it: every deadline in one place, every application costed and checklisted.',
      scope: 'one per country you apply to' }
  ];

  /* ---- Report (MIT) ---- */

  const mit = byId('mit');
  const NET_COST_PER_YEAR = 22000;   /* "your share" after aid, from the report's Snapshot */
  const NET_COST_TOTAL = 87000;

  const report = {
    universityId: mit.id,
    title: 'University Report — ' + mit.university,
    sampleNote: 'Sample, anonymised demo. A real report with the student\'s identity removed.',
    pages: 19,
    questions: ['Can I get in?', 'Will I belong there and do well?', 'What will applying demand of me?'],
    summary: [
      { label: 'University', value: mit.university },
      { label: 'Course', value: mit.course },
      { label: 'Location', value: mit.country + ' / ' + mit.city },
      { label: 'Overall rank', value: 'QS #1 in the world, 2026-27 (fifteenth consecutive year); #1 for engineering' },
      { label: 'How to apply', value: 'MIT\'s own application portal, not the Common App; non-binding Early Action or Regular Action' },
      { label: 'Admission likelihood', value: 'Reach — 4.6% overall, 2.0% for international applicants' },
      { label: 'Full price, whole degree', value: rm(mit.approxTotalMyr) },
      { label: 'Est. net cost after aid', value: `~${rm(NET_COST_PER_YEAR)}/yr your share (~${rm(NET_COST_TOTAL)} over four years); expected parent contribution RM 0` },
      { label: 'Your priorities', value: priorities.map((p, i) => (i + 1) + '. ' + p).join(' · ') }
    ],
    sections: REPORT_SECTIONS,
    openSection: (REPORT_SECTIONS.find((s) => /why here/i.test(s.title)) || { n: null }).n,
    whyHere: [
      { theme: 'Scholarship — your top priority',
        text: 'The best answer on your entire list, and not close. Need-blind for internationals, meets 100% of need with grants and no loans, zero expected parent contribution at your family\'s income.' },
      { theme: 'Hands-on experience — your second priority',
        text: 'Maxed out. Undergraduate research from first year, 2.007\'s robot competition, 2.009\'s product build, open machine shops, and an entrepreneurship stack that speaks directly to your goal of building products.' },
      { theme: 'Ranking',
        text: 'QS number one in the world for the fifteenth consecutive year, and first for engineering. Nothing on your list is stronger.' },
      { theme: 'Recognition — your hard gate',
        text: 'Cleared. Course 2 and Course 2-A are ABET-accredited and the US is a Washington Accord signatory, which is the recognised route to BEM registration if you return.' }
    ],
    whyHesitate: [
      { theme: 'Getting in',
        text: 'The reason MIT cannot be the plan. A 2.0% international admit rate means a superb application still fails most of the time, and the SAT — mandatory, no test-optional route — is not yet sat.' },
      { theme: 'Workload',
        text: 'All of the hands-on work sits inside the heaviest workload on your list. Fewer than half of MIT undergraduates call their own workload "about right".' },
      { theme: 'The aid is conditional',
        text: `It leaves roughly ${rm(NET_COST_PER_YEAR)} a year you are expected to earn yourself from campus work, and it depends on being admitted and filing the CSS Profile and IDOC documents. There are no merit awards to fall back on.` },
      { theme: 'Location',
        text: 'The weakest fit. Cambridge is safe, walkable and well connected, but it is urban, the New England winter runs November to March, and outdoors is a planned weekend rather than a Tuesday afternoon.' }
    ],
    pullQuote: {
      text: '\'Drinking from a firehose\' (a phrase coined by a former MIT president) — the workload is genuinely heavy and relentless; students describe never fully \'catching up\'.',
      source: 'From the "what\'s studying there like" section'
    }
  };

  /* ---- Decision: recommendation, deadlines, apply steps ---- */

  const nus = byId('nus');
  const ntu = byId('ntu');
  const unsw = byId('unsw');
  const princeton = byId('princeton');
  const harvard = byId('harvard');

  const plan = [
    { id: 'mit', round: 'early',
      reason: 'The best answer to your number-one priority: admission ignores whether you asked for aid, and full need is met with grants. Use the non-binding early round here.' },
    { id: 'princeton', round: 'regular',
      reason: 'The same aid promise as MIT: need-blind for international students, full need met, no loans.' },
    { id: 'harvard', round: 'regular',
      reason: 'Need-blind for international students, with full need met by grants. Apply for the accredited SB Mechanical Engineering, not the AB track.' },
    { id: 'nus', round: 'regular',
      reason: `Your strongest realistic option. The tuition grant brings the whole degree to about ${rm(nus.approxTotalMyr)}, in exchange for a three-year Singapore work bond.` },
    { id: 'ntu', round: 'regular',
      reason: `A dedicated robotics degree at about ${rm(ntu.approxTotalMyr)}, with the same tuition grant and bond.` },
    { id: 'unsw', round: 'regular',
      reason: `Your grades are above the entry bar. The catch is money: without the competitive Scientia scholarship the degree costs ${rm(unsw.approxTotalMyr)}.` }
  ];

  const planRows = plan.map((p) => byId(p.id));
  const balance = { reach: 0, match: 0, safety: 0 };
  planRows.forEach((u) => { balance[u.band] += 1; });

  const deadlines = plan.map((p) => {
    const u = byId(p.id);
    const all = (u.keyDeadline.match(ISO_DATE) || []).slice().sort();
    const date = p.round === 'early' ? (all[0] || null) : u.deadlineDate;
    return {
      universityId: u.id,
      university: u.shortName,
      date: date,
      rolling: !date && /^rolling/i.test(u.keyDeadline),
      what: p.round === 'early' ? 'Early round application' : 'Application deadline',
      text: u.keyDeadline,
      confirmed: !!date && !/approx|confirm|~/i.test(u.keyDeadline)
    };
  }).sort((a, b) => (a.date || '9999').localeCompare(b.date || '9999'));

  const firstDeadline = deadlines[0];
  const commonApp = planRows.filter((u) => u.howToApply === 'Common App');

  const decision = {
    recommendedId: mit.id,
    headline: `Put ${mit.shortName} first, and make sure the rest of your list carries the weight.`,
    balance: balance,
    rounds: { early: 'Early round', regular: 'Regular round' },
    plan: plan,
    deadlines: deadlines,
    applySteps: [
      { title: 'Book the SAT',
        detail: `${mit.shortName} requires it, with no test-optional route, and it is only offered a handful of times a year. It has the longest lead time, so it goes first.` },
      { title: `Start the ${mit.shortName} application`,
        detail: `${mit.howToApply}. Aim for the early round on ${firstDeadline.date}: it is non-binding, so you stay free to compare offers.` },
      { title: 'Ask your teachers for references and request your transcript',
        detail: 'Every application on this list needs them, so collect them once.' },
      { title: 'File the financial aid forms',
        detail: `The aid is not automatic. For ${mit.shortName}: ${mit.howToGetScholarship}` },
      { title: `Fill in the Common App once for ${names(commonApp)}`,
        detail: 'One shared form and one main essay cover both. Each then asks for a few extras of its own.' },
      { title: `Apply to ${nus.shortName} and ${ntu.shortName} on their own websites`,
        detail: `Each has its own application. ${nus.shortName}: ${nus.keyDeadline}` }
    ],
    openRisks: [
      `Your grades are predicted (${student.grades}). The plan needs a fallback if a result comes in lower.`,
      `The SAT is not yet sat, and ${mit.shortName} will not consider an application without it.`,
      `${unsw.shortName} is safe on grades, not on money. Without a scholarship it costs ${rm(unsw.approxTotalMyr)}.`
    ]
  };

  /* ---- Feedback, exactly as printed on the poster ---- */

  const feedback = {
    label: 'Early testers',
    list: {
      title: 'On the spreadsheet',
      question: 'How confident do you feel narrowing down your choices with it?',
      score: 4.1,
      outOf: 5,
      respondents: 13,
      breakdown: [{ rating: 5, count: 4 }, { rating: 4, count: 6 }, { rating: 3, count: 3 }],
      bars: [
        { title: 'Most useful column', outOf: 13, items: [
          { label: 'Course at a glance', count: 4 },
          { label: 'Entry requirements', count: 3 },
          { label: 'Total cost in ringgit', count: 2 },
          { label: 'Recognised in Malaysia', count: 1 }
        ] }
      ],
      quotes: [
        'There are a lot of universities I haven\'t seen before.',
        'I really like how it’s divided into many different parts and comprises of everything, from the basic scratch up till the very detailed parts, such as campus life and the traditions within the school. It allowed me to gain a better understanding of the school that I desire and also what i would be able to expect there.'
      ]
    },
    report: {
      title: 'On the report',
      question: 'How much time did it save you in your university research?',
      score: 4.2,
      outOf: 5,
      respondents: 6,
      breakdown: [{ rating: 5, count: 2 }, { rating: 4, count: 3 }, { rating: 3, count: 1 }],
      bars: [
        { title: 'Gave the most clarity', outOf: 6, items: [
          { label: 'Getting in & your fit', count: 5 },
          { label: 'Academic structure', count: 4 },
          { label: 'Costs & financial aid', count: 2 },
          { label: 'Outcomes & network', count: 2 }
        ] },
        { title: 'Most interesting to read', outOf: 6, items: [
          { label: 'Culture & vibe', count: 4 },
          { label: 'Student life & food', count: 3 },
          { label: 'The city & belonging', count: 2 },
          { label: 'Unique facts & quirks', count: 2 }
        ] }
      ],
      quotes: []
    }
  };

  /* ---- Pricing wording. No ringgit figure: a per-report price has not been set. ---- */

  const pricing = {
    free: {
      label: 'Free',
      items: [
        'The 2-minute form',
        deliverables[0].name + ' — ' + deliverables[0].oneLine,
        'Your first University Report, on any university from your list'
      ]
    },
    paid: {
      label: 'Paid',
      items: [
        'Each extra University Report',
        deliverables[2].name + ' — ' + deliverables[2].oneLine
      ]
    },
    reportRule: { freeCount: 1, text: 'Your first report is free. Each one after that is paid.' },
    pricePerReport: null
  };

  /* ---- Files the download buttons open (paths relative to prototype/index.html) ---- */

  const files = {
    list: { href: '../business/sales/sample_pack/sample_master_list.csv', label: 'Download the spreadsheet' },
    report: { href: '../business/sales/sample_pack/sample_university-report_MIT.pdf', label: 'Download the PDF' }
  };

  window.DATA = {
    brand: {
      name: 'University & Course Research',
      tagline: 'Real universities that actually fit your grades and budget — not just the famous names.'
    },
    student: student,
    intake: intake,
    bands: bands,
    columns: COLUMNS,
    columnGroups: columnGroups,
    universities: ROWS,
    top5: top5,
    findings: findings,
    deliverables: deliverables,
    report: report,
    decision: decision,
    feedback: feedback,
    pricing: pricing,
    files: files
  };
})();
