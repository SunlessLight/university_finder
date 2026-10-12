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

  const COLUMNS = [
    {
      "key": "listStatus",
      "label": "List status"
    },
    {
      "key": "desirability",
      "label": "Desirability"
    },
    {
      "key": "tier",
      "label": "Tier"
    },
    {
      "key": "admissionLikelihood",
      "label": "Admission likelihood"
    },
    {
      "key": "warnings",
      "label": "Warnings"
    },
    {
      "key": "university",
      "label": "University"
    },
    {
      "key": "course",
      "label": "Course"
    },
    {
      "key": "courseAtAGlance",
      "label": "Course at a glance"
    },
    {
      "key": "country",
      "label": "Country"
    },
    {
      "key": "city",
      "label": "City"
    },
    {
      "key": "studentLife",
      "label": "Student life"
    },
    {
      "key": "subjectRank",
      "label": "Subject rank"
    },
    {
      "key": "overallRank",
      "label": "Overall rank"
    },
    {
      "key": "entryRequirements",
      "label": "Entry requirements"
    },
    {
      "key": "studentGrades",
      "label": "Student grades"
    },
    {
      "key": "gradesVsEntryBar",
      "label": "Grades vs entry bar"
    },
    {
      "key": "englishReq",
      "label": "English req"
    },
    {
      "key": "annualTuition",
      "label": "Annual tuition"
    },
    {
      "key": "totalTuition",
      "label": "Total tuition"
    },
    {
      "key": "estLivingPerYear",
      "label": "Est. living/yr"
    },
    {
      "key": "durationYears",
      "label": "Duration (yrs)"
    },
    {
      "key": "approxTotalMyr",
      "label": "Approx total (MYR)"
    },
    {
      "key": "scholarshipAndPortal",
      "label": "Scholarship & portal"
    },
    {
      "key": "scholarshipCoverage",
      "label": "Scholarship coverage"
    },
    {
      "key": "scholarshipCompetitiveness",
      "label": "Scholarship competitiveness"
    },
    {
      "key": "howToGetScholarship",
      "label": "How to get the scholarship"
    },
    {
      "key": "moneyToShowVisa",
      "label": "Money to show (visa)"
    },
    {
      "key": "workRightsAfterGraduating",
      "label": "Work rights after graduating"
    },
    {
      "key": "recognisedInMalaysia",
      "label": "Recognised in Malaysia?"
    },
    {
      "key": "howToApply",
      "label": "How to apply"
    },
    {
      "key": "keyDeadline",
      "label": "Key deadline"
    },
    {
      "key": "intake",
      "label": "Intake"
    },
    {
      "key": "notes",
      "label": "Notes"
    },
    {
      "key": "courseUrl",
      "label": "Course URL"
    },
    {
      "key": "infoSource",
      "label": "Info source"
    }
  ];

  const ROWS = [
    {
      "id": "mit",
      "shortName": "MIT",
      "listStatus": "Finalist",
      "desirability": 89,
      "tier": "A",
      "admissionLikelihood": "Reach (very selective)",
      "warnings": "None",
      "university": "Massachusetts Institute of Technology",
      "course": "Mechanical Engineering (Course 2) — robotics track",
      "courseAtAGlance": "Core ME curriculum (mechanics, dynamics, thermo, design) plus required thesis; robotics via 2.12 Intro to Robotics or the flexible 2-A track.",
      "country": "USA",
      "city": "Cambridge, MA",
      "studentLife": "All first-years must live on campus (~20 residence halls); halal is via one Student Center vendor plus the W11 musalla, not every dining hall.",
      "subjectRank": "QS #1 world for engineering & mech eng",
      "overallRank": "QS #1",
      "entryRequirements": "Holistic; no fixed grade cutoff or course list. SAT or ACT required (no cutoff or recommended scores); take by Nov 30 (Early Action) or Dec 31 (Regular Action).",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "No TOEFL/IELTS required for undergrad admission (optional). Arif's English-medium A-Levels satisfy it.",
      "annualTuition": "USD 66720",
      "totalTuition": "USD 266880",
      "estLivingPerYear": "USD 26040",
      "durationYears": 4,
      "approxTotalMyr": 1499002,
      "scholarshipAndPortal": "No merit scholarships — MIT meets 100% of demonstrated financial need with MIT Scholarship grants (never repaid).",
      "scholarshipCoverage": "Need blind + meets 100% of demonstrated need for all, incl. international; MIT FAQ: 'one of only nine' US schools.",
      "scholarshipCompetitiveness": "The aid is guaranteed by policy once admitted — no separate scholarship contest.",
      "howToGetScholarship": "(1) Apply by 2027-01-04; (2) file CSS Profile (code 3514), upload parent tax/income docs to IDOC by aid deadline: 2026-11-30 (Early Action) or 2027-02-15 (Regular Action); (3) offer by email.",
      "moneyToShowVisa": "student visa form financial documentation",
      "workRightsAfterGraduating": "STEM-designated: post-study work permit 12 mo + science post-study work extension 24 mo = up to 3 yrs; strong US tech market + strong USD.",
      "recognisedInMalaysia": "ABET-accredited (Course 2) + USA is a Washington Accord signatory — supports BEM registration; confirm the exact MQA equivalence entry at mqa.gov.my.",
      "howToApply": "MIT application (not Common App)",
      "keyDeadline": "2027-01-04 (Regular Action; Early Action 2026-11-01)",
      "intake": "2027 Sept",
      "notes": "MIT says it is need blind and meets 100% of demonstrated need for all undergrads incl. international; aid never includes loans. Class of 2029: 4.6% admitted overall; intl 136 of 6,926.",
      "courseUrl": "https://meche.mit.edu/",
      "infoSource": "Official page"
    },
    {
      "id": "oxford",
      "shortName": "Oxford",
      "listStatus": "Finalist",
      "desirability": 66,
      "tier": "B",
      "admissionLikelihood": "Reach (test + interview)",
      "warnings": "None",
      "university": "University of Oxford",
      "course": "Engineering Science MEng (robotics/mechatronics specialise later)",
      "courseAtAGlance": "4-yr MEng: common core Yrs 1-2, then specialise from Yr 3 into 1 of 8 branches; robotics sits in Control, Information and Solid Mechanics.",
      "country": "UK",
      "city": "Oxford",
      "studentLife": "Collegiate Oxford; hands-on via Oxford University Racing (undergrad-run Formula Student) and Team ORIon inside the Engineering Science dept.",
      "subjectRank": "THE Engineering #2 (2026); QS top 5",
      "overallRank": "QS ~#3",
      "entryRequirements": "A*A*A at A-level incl A* in Maths + Physics; ESAT (Engineering & Science Admissions Test) + interview. Holistic selection.",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "IELTS 7.5 overall (7.0 per component), Oxford 'higher level'; waived for recent English-medium study.",
      "annualTuition": "GBP 62820 (2026/27 overseas, OFFICIAL - one all-in fee, no separate college fee)",
      "totalTuition": "GBP 251280 (4 yrs)",
      "estLivingPerYear": "GBP 16000",
      "durationYears": 4,
      "approxTotalMyr": 1724582,
      "scholarshipAndPortal": "Reach Oxford Scholarship — Oxford's main full route for students from eligible developing countries. Apply for admission first (UCAS by 15 Oct 2026), then the Reach Oxford application;",
      "scholarshipCoverage": "Full ride: tuition, college fees, a living-costs grant and one return flight a year, for the whole course.",
      "scholarshipCompetitiveness": "Extremely competitive — only ~2-3 Reach Oxford scholarships are awarded across ALL subjects each year, and Oxford has no back-up funding for near-misses.",
      "howToGetScholarship": "Must first be offered a place at Oxford, then be selected.",
      "moneyToShowVisa": "Student visa: first-year tuition + ~GBP 16k/yr living + college fee shown",
      "workRightsAfterGraduating": "UK Graduate Route — 18 months for applications from 1 Jan 2027 (reduced from 2 years; Arif falls under the 18-month rule), then a Skilled Worker visa is needed;",
      "recognisedInMalaysia": "MEng is accredited by the UK Engineering Council (CEng route) and the UK is a Washington Accord signatory — supports BEM registration;",
      "howToApply": "UCAS (+ ESAT admissions test + interview)",
      "keyDeadline": "2026-10-15 (UCAS; ESAT registration closes ~2026-09-28)",
      "intake": "2027 Oct",
      "notes": "No standalone 'Robotics' degree - robotics/mechatronics come via optional papers/projects in Yrs 3-4; entry needs PAT admissions test, not just grades.",
      "courseUrl": "https://www.ox.ac.uk/admissions/undergraduate/courses/course-listing/engineering-science",
      "infoSource": "Official page"
    },
    {
      "id": "nus",
      "shortName": "NUS",
      "listStatus": "Finalist",
      "desirability": 85,
      "tier": "A",
      "admissionLikelihood": "Match",
      "warnings": "None",
      "university": "National University of Singapore",
      "course": "BEng Robotics & Machine Intelligence (RMI)",
      "courseAtAGlance": "4-yr direct-honours BEng across 5 depts, blending design, control theory, programming and AI/ML/IoT/automation; hands-on projects and internships.",
      "country": "Singapore",
      "city": "Singapore",
      "studentLife": "Kent Ridge campus; Makers@CDE and Tinkering Corner labs (3D printing, laser cutting); NUS RoboMaster team competes internationally.",
      "subjectRank": "QS Mechanical, Aeronautical & Manufacturing Eng #3 in the world (2026); NUS overall QS #8",
      "overallRank": "QS ~#8",
      "entryRequirements": "Highly competitive; strong A-levels incl A-level Maths; holistic (published grade profile). ~A*A*A* competitive band",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Meets",
      "englishReq": "Not required — NUS asks A-Level applicants for no English test; IELTS/TOEFL optional to submit",
      "annualTuition": "SGD 18050 (ASEAN, MOE Tuition Grant, AY2026/27 CDE schedule; non-subsidised SGD 39700)",
      "totalTuition": "SGD 72200",
      "estLivingPerYear": "SGD 12000",
      "durationYears": 4,
      "approxTotalMyr": 383438,
      "scholarshipAndPortal": "Two realistic routes. (1)",
      "scholarshipCoverage": "MOE Tuition Grant = ~50-60% fee subsidy (with a 3-yr Singapore work bond).",
      "scholarshipCompetitiveness": "MOE Tuition Grant is broadly available (near-automatic for admitted international students who accept the bond) = low competitiveness.",
      "howToGetScholarship": "Apply for NUS undergraduate admission; you are automatically considered for the ASEAN Undergraduate Scholarship through that application (shortlisted candidates may be interviewed) — no separate form.",
      "moneyToShowVisa": "Student's Pass: tuition + living shown",
      "workRightsAfterGraduating": "No post-study work visa, but the tuition-grant bond requires 3 years with a Singapore-registered company — a guaranteed route into an SGD salary.",
      "recognisedInMalaysia": "Caution — RMI is NOT on IES's Washington Accord list (18 other CDE degrees are); switch to BEng Mech Eng + Robotics spec. (same admissions) for BEM recognition",
      "howToApply": "Direct (NUS online application)",
      "keyDeadline": "2027-02-17 (AY2027/28 international window: 16 Dec 2026 - 17 Feb 2027, per NUS Office of Admissions)",
      "intake": "2027 Aug",
      "notes": "New AY2025/26 programme, first intake just started, so no grad track record yet; interdisciplinary across ME, BME, ChBE, ECE and MSE depts.",
      "courseUrl": "https://cde.nus.edu.sg/me/undergraduate/beng-rmi/overview/",
      "infoSource": "Official page"
    },
    {
      "id": "princeton",
      "shortName": "Princeton",
      "listStatus": "Finalist",
      "desirability": 83,
      "tier": "A",
      "admissionLikelihood": "Reach (very selective)",
      "warnings": "None",
      "university": "Princeton University",
      "course": "BSE Mechanical & Aerospace Engineering (robotics)",
      "courseAtAGlance": "4-yr BSE MAE degree; senior independent work/thesis capstone; robotics via elective courses + optional interdisciplinary Robotics minor.",
      "country": "USA",
      "city": "Princeton, NJ",
      "studentLife": "An active, fast-growing Muslim community; residential-college dining, then eating clubs for upper years.",
      "subjectRank": "QS Mech Eng ~top 30; strong MAE",
      "overallRank": "QS ~#22",
      "entryRequirements": "Holistic; top academics (~A*A*A*A*) + essays; no fixed cutoff",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "No TOEFL/IELTS required — Princeton waives it for students in an English-medium school. Arif's A-Levels qualify.",
      "annualTuition": "USD 68140 (2026-27 official)",
      "totalTuition": "USD 272560",
      "estLivingPerYear": "USD 26484",
      "durationYears": 4,
      "approxTotalMyr": 1529124,
      "scholarshipAndPortal": "No merit scholarships and NO student loans — 100% need met with grants (never repaid) for all four years.",
      "scholarshipCoverage": "Need-blind for internationals; one of the few US schools that never caps international aid.",
      "scholarshipCompetitiveness": "Guaranteed once admitted — no separate contest. Gate = admission: ~4% admit (Class of 2029 not released); record 14.1% international in the entering class.",
      "howToGetScholarship": "Be admitted, then file the PFAA + CSS Profile + tax docs by the aid deadline (with the Nov 1 SCEA or Jan 1 RD application). Need-blind = no penalty for requesting aid.",
      "moneyToShowVisa": "student visa form financial documentation",
      "workRightsAfterGraduating": "STEM-designated: post-study work permit 12 mo + science post-study work extension 24 mo = up to 3 yrs; strong USD.",
      "recognisedInMalaysia": "MAE is ABET-accredited + USA Washington Accord signatory — supports BEM; confirm MQA equivalence at mqa.gov.my.",
      "howToApply": "Common App",
      "keyDeadline": "2027-01-01 (Regular Decision; Single-Choice Early Action 2026-11-01)",
      "intake": "2027 Sept",
      "notes": "Test-optional through fall 2027 entry; SAT/ACT required from 2027-28 cycle (fall 2028 entry) on. No dedicated robotics major - reached via MAE electives + Robotics minor.",
      "courseUrl": "https://mae.princeton.edu/",
      "infoSource": "Official page"
    },
    {
      "id": "tsinghua",
      "shortName": "Tsinghua",
      "listStatus": "Finalist",
      "desirability": 73,
      "tier": "B",
      "admissionLikelihood": "Reach (very selective)",
      "warnings": "None",
      "university": "Tsinghua University",
      "course": "BEng - Global Talents in Science & Engineering (Zijing College), Mechanical Engineering major (English-taught)",
      "courseAtAGlance": "4-yr, fully English-taught residential BEng hosted by Zijing College, Tsinghua's undergrad residential college.",
      "country": "China",
      "city": "Beijing",
      "studentLife": "Intense and high-achieving — China's most competitive university, with a serious academics-plus-activities culture.",
      "subjectRank": "QS #7 world for Engineering & Technology; THE #13 Engineering",
      "overallRank": "QS #14 (2027 edition); THE #12, 1st in Asia",
      "entryRequirements": "Outstanding academics + intl test (A-Level/SAT/AP/IB); holistic selection. English route = the Global Talents programme (Zijing College);",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "IELTS/TOEFL required; no fixed minimum published (holistic)",
      "annualTuition": "CNY 100000",
      "totalTuition": "CNY 400000",
      "estLivingPerYear": "CNY 40000",
      "durationYears": 4,
      "approxTotalMyr": 336000,
      "scholarshipAndPortal": "Chinese Government Scholarship (CSC), the main full-ride route - apply Type A via the Chinese Embassy in Malaysia (agency 4581) on studyinchina.csc.edu.cn; NOT Type B via Tsinghua for undergrads.",
      "scholarshipCoverage": "CSC full award: tuition, campus accommodation, monthly stipend and medical insurance. Airfare not included.",
      "scholarshipCompetitiveness": "Very competitive - Tsinghua is China's top university and CSC does not publish per-university award rates, so treat exact odds as unpublished.",
      "howToGetScholarship": "Separate from admission, on an earlier deadline (~early Feb). Mandatory CSCA test: Maths + Physics or Chemistry, in English; Professional Chinese waived for English-taught.",
      "moneyToShowVisa": "Bank statement for X1 student visa (modest)",
      "workRightsAfterGraduating": "Work (Z) visa possible but hard for fresh grads; weak fit for Arif's stronger-currency migration goal",
      "recognisedInMalaysia": "Yes academically — Tsinghua is on Malaysia's recognised-China list. For BEM, the specific programme must be CEEAA-accredited; confirm with BEM.",
      "howToApply": "Direct - apply.join-tsinghua.edu.cn/international (+ CSC applied separately)",
      "keyDeadline": "2027-02-28 (approx; 2026 cycle closed 28 Feb - confirm exact 2027 date)",
      "intake": "2027 Sept",
      "notes": "Zijing College is Tsinghua's 1st English-taught residential college; ME sits alongside IST, civil eng & design science in one multidisciplinary STEAM curriculum. App fee RMB800 + RMB800/yr insurance.",
      "courseUrl": "https://international.join-tsinghua.edu.cn/info/1082/1151.htm",
      "infoSource": "Official page"
    },
    {
      "id": "stanford",
      "shortName": "Stanford",
      "listStatus": "Finalist",
      "desirability": 89,
      "tier": "A",
      "admissionLikelihood": "Reach (very selective)",
      "warnings": "None",
      "university": "Stanford University",
      "course": "Mechanical Engineering — robotics",
      "courseAtAGlance": "BS ME: shared core (structures, dynamics, thermo, design) + electives, not a formal track; robotics via ME320 and tech electives.",
      "country": "USA",
      "city": "Stanford, CA",
      "studentLife": "Four-year on-campus housing guarantee; Product Realization Lab makerspace and Stanford Robotics Club open to any undergrad, not just ME majors.",
      "subjectRank": "QS top-3 world engineering",
      "overallRank": "QS ~#6",
      "entryRequirements": "Holistic; top academics expected",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "No TOEFL/IELTS required for undergrad admission (optional). English-medium A-Levels satisfy it.",
      "annualTuition": "USD 67731",
      "totalTuition": "USD 270924",
      "estLivingPerYear": "USD 28269",
      "durationYears": 4,
      "approxTotalMyr": 1551360,
      "scholarshipAndPortal": "No merit scholarships — need-based aid only. Requested via the CSS Profile + the International Student Application for Financial Assistance (ISAFA) with the admission application.",
      "scholarshipCoverage": "Meets 100% of demonstrated need for all admitted students incl. internationals.",
      "scholarshipCompetitiveness": "Stanford is need-AWARE for internationals: asking for aid is a factor in admission, and the international aid budget is limited. Admit rate ~4%.",
      "howToGetScholarship": "Indicate the aid request on the admission application, then file the CSS Profile + ISAFA.",
      "moneyToShowVisa": "student visa form financial documentation",
      "workRightsAfterGraduating": "STEM-designated: post-study work permit 12 mo + science post-study work extension 24 mo = up to 3 yrs;",
      "recognisedInMalaysia": "Mechanical Engineering is ABET-accredited + USA Washington Accord signatory — supports BEM; confirm MQA equivalence at mqa.gov.my.",
      "howToApply": "Common App",
      "keyDeadline": "2027-01-05 (Regular Decision; Restrictive Early Action 2026-11-01)",
      "intake": "2027 Sept",
      "notes": "No dedicated robotics/mechatronics degree or concentration at Stanford ME; robotics learned via electives, ME320, and student robotics clubs/labs.",
      "courseUrl": "https://me.stanford.edu/",
      "infoSource": "Official page"
    },
    {
      "id": "unsw",
      "shortName": "UNSW",
      "listStatus": "Shortlist",
      "desirability": 82,
      "tier": "A",
      "admissionLikelihood": "Safety",
      "warnings": "None",
      "university": "UNSW Sydney",
      "course": "BEng (Hons) Robotics and Mechatronics Engineering",
      "courseAtAGlance": "4-yr BEng (Hons) combining mechanical, control & software engineering; flexible first year, 60 days mandatory industry placement.",
      "country": "Australia",
      "city": "Sydney, NSW",
      "studentLife": "Large engineering-heavy campus 15 min from Sydney's eastern beaches; trimesters and big student teams.",
      "subjectRank": "QS Mech Eng ~top 30-40; UNSW overall QS ~#19",
      "overallRank": "QS ~#19",
      "entryRequirements": "A-levels incl Maths; indicative ~AAB-A*AA equivalent (A-level assessment under review for 2026 curriculum)",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Above",
      "englishReq": "IELTS 6.5 (6.0)",
      "annualTuition": "AUD 61500 (2026 indicative yr-1; later years higher)",
      "totalTuition": "AUD 265500 (2026 indicative full degree)",
      "estLivingPerYear": "AUD 30000",
      "durationYears": 4,
      "approxTotalMyr": 1121805,
      "scholarshipAndPortal": "Two routes. (1) UNSW International Scientia Coursework Scholarship — FULL tuition for the whole degree (UNSW's flagship award), by separate application. (2)",
      "scholarshipCoverage": "Scientia = FULL tuition (the best scholarship in the Australian pool).",
      "scholarshipCompetitiveness": "Scientia is highly competitive (UNSW's 'crown jewel' — academic merit + leadership + impact; small number awarded, count not published).",
      "howToGetScholarship": "Scientia: submit its separate application (merit + leadership/extracurriculars + statement). International Student Award: after/with your offer, apply on the UNSW portal with a 500-word statement;",
      "moneyToShowVisa": "Student visa (subclass 500): tuition + ~AUD 29,710/yr living + travel shown (CoE)",
      "workRightsAfterGraduating": "post-study work visa ~2-3 yrs; strong AUD",
      "recognisedInMalaysia": "Washington Accord (Engineers Australia); MQA: verify",
      "howToApply": "Direct / UAC International",
      "keyDeadline": "Rolling; ~Apr 2027 for Jul (T2) 2027 intake (~Nov 2026 for Feb/T1 2027)",
      "intake": "2027 (Jul/T2 realistic; Feb/T1 2027 too early for A2 results)",
      "notes": "Kensington campus; ChallEng industry projects, Robogals & Women in Engineering societies; optional Nuclear Engineering minor.",
      "courseUrl": "https://www.unsw.edu.au/study/undergraduate/bachelor-of-engineering-honours-robotics-mechatronics",
      "infoSource": "Official page"
    },
    {
      "id": "harvard",
      "shortName": "Harvard",
      "listStatus": "Finalist",
      "desirability": 86,
      "tier": "A",
      "admissionLikelihood": "Reach (very selective)",
      "warnings": "None",
      "university": "Harvard University",
      "course": "SB Mechanical Engineering (ABET-accredited; mechatronics/robotics via SEAS)",
      "courseAtAGlance": "Standalone ABET-accredited SB Mechanical Eng (20 courses), distinct from AB/SB Engineering Sciences; covers mechatronics/robotics; declared end yr1.",
      "country": "USA",
      "city": "Cambridge, MA",
      "studentLife": "All first-years live in Harvard Yard and eat in Annenberg — a strong built-in community from day one.",
      "subjectRank": "SEAS engineering ~QS top 30 for Mech Eng; strong robotics research",
      "overallRank": "QS ~#4; US News ~#3",
      "entryRequirements": "Holistic; top academics (~A*A*A*A*) + essays; no fixed cutoff",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "No TOEFL/IELTS required — waived for English-medium instruction; Arif's English-medium A-Levels qualify.",
      "annualTuition": "USD 59320 (approx 2026/27)",
      "totalTuition": "USD 237280",
      "estLivingPerYear": "USD 28000",
      "durationYears": 4,
      "approxTotalMyr": 1411091,
      "scholarshipAndPortal": "Harvard is NEED-BLIND for all applicants incl. internationals and meets 100% of demonstrated need with grants, no loans. Requested via the CSS Profile + IDOC with the Common App.",
      "scholarshipCoverage": "Full demonstrated need met with grants (never repaid), no loans.",
      "scholarshipCompetitiveness": "Guaranteed by policy once admitted — need-blind for internationals (one of only ~a handful of US schools), so requesting aid does NOT affect admission.",
      "howToGetScholarship": "Be admitted, then file the CSS Profile + IDOC parent income docs by the aid deadline (with the Nov REA or Jan RD application). Need-blind = no penalty for requesting aid.",
      "moneyToShowVisa": "student visa form financial documentation",
      "workRightsAfterGraduating": "STEM-designated (SB): post-study work permit 12 mo + science post-study work extension 24 mo = up to 3 yrs; strong USD.",
      "recognisedInMalaysia": "SB Mechanical Engineering is ABET-accredited + USA is a Washington Accord signatory - supports BEM. The AB Engineering Sciences track is NOT accredited.",
      "howToApply": "Common App",
      "keyDeadline": "2027-01-01 (Regular Decision; Restrictive Early Action 2026-11-01)",
      "intake": "2027 Sept",
      "notes": "Aid is 100% need-based, no merit scholarships (incl. int'l applicants). Robotics is a track within ME, not standalone; access to Wyss Institute and Microrobotics Lab.",
      "courseUrl": "https://seas.harvard.edu/",
      "infoSource": "Official page"
    },
    {
      "id": "imperial",
      "shortName": "Imperial",
      "listStatus": "Finalist",
      "desirability": 66,
      "tier": "B",
      "admissionLikelihood": "Reach (test + interview)",
      "warnings": "None",
      "university": "Imperial College London",
      "course": "Mechanical Engineering MEng (robotics/mechatronics streams)",
      "courseAtAGlance": "4-yr MEng (5-yr with industry/abroad placement); robotics/mechatronics woven in via core Mechatronics 1-3 modules, not a separate stream.",
      "country": "UK",
      "city": "London",
      "studentLife": "South Kensington campus on the Exhibition Road museum row by Hyde Park; 380+ clubs incl. Robotics Society and Formula Racing; Ethos gym on site.",
      "subjectRank": "QS top-10 world for engineering",
      "overallRank": "QS ~#2",
      "entryRequirements": "A*A*A incl A* in Maths + Physics (A*AAA for 4 A-levels); ESAT (Maths 1, Maths 2, Physics) required + interview for those meeting the threshold.",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "IELTS 6.5-7.0 overall (6.0-6.5 per element), College-approved test; waived for recent English-medium study.",
      "annualTuition": "GBP 43700 (2026/27 est; 2025/26 ~GBP 40,940)",
      "totalTuition": "GBP 174800",
      "estLivingPerYear": "GBP 18000",
      "durationYears": 4,
      "approxTotalMyr": 1349996,
      "scholarshipAndPortal": "Imperial Inspires Scholarship (GBP 15k/yr, via UCAS from Sept 2026 + an invited essay) + Khazanah Global Scholarship (full; Imperial is an approved uni). GREAT Scholarships are postgraduate-only.",
      "scholarshipCoverage": "Imperial Inspires: GBP 15,000/yr every year (~GBP 60k over 4 yrs), overseas-only - partial, not a full ride.",
      "scholarshipCompetitiveness": "Imperial Inspires: at least 300 awards for 2027 entry across Engineering/NatSci/Medicine/Business; merit-assessed essay, not means-tested.",
      "howToGetScholarship": "Apply via UCAS from Sept 2026; if you meet minimum entry requirements you are invited to answer an extra Imperial Inspires essay. Awards decided by mid-April 2027.",
      "moneyToShowVisa": "Student visa: tuition + ~GBP 18k/yr London living shown",
      "workRightsAfterGraduating": "UK Graduate Route — 18 months for applications from 1 Jan 2027 (reduced from 2 years; Arif falls under the 18-month rule), then a Skilled Worker visa is needed;",
      "recognisedInMalaysia": "MEng is accredited by the UK Engineering Council (CEng route) and the UK is a Washington Accord signatory — supports BEM registration;",
      "howToApply": "UCAS (+ ESAT admissions test + interview)",
      "keyDeadline": "2027-01-13 (UCAS equal consideration)",
      "intake": "2027 Sept",
      "notes": "No dedicated robotics stream - mechatronics integrated into core ME curriculum; ESAT admissions test required; ~13:1 applicant ratio (2025).",
      "courseUrl": "https://www.imperial.ac.uk/study/courses/",
      "infoSource": "Official page"
    },
    {
      "id": "monash",
      "shortName": "Monash",
      "listStatus": "Shortlist",
      "desirability": 77,
      "tier": "A",
      "admissionLikelihood": "Safety",
      "warnings": "None",
      "university": "Monash University",
      "course": "Bachelor of Robotics and Mechatronics Engineering (Honours)",
      "courseAtAGlance": "4-yr BEng(Hons): common first year, specialise in robotics/mechatronics from Yr2, design-build projects Yr3-4, 12-wk work placement after Yr3.",
      "country": "Australia",
      "city": "Melbourne, VIC",
      "studentLife": "Large suburban Clayton campus in Melbourne with standout student teams (Motorsport, Nova Rover).",
      "subjectRank": "QS Mech Eng ~top 40-50; Monash overall QS ~#37",
      "overallRank": "QS ~#37",
      "entryRequirements": "A-levels incl Maths; indicative ~BBB-ABB (well within A*A*A*A*)",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Above",
      "englishReq": "IELTS 6.5 (6.0)",
      "annualTuition": "AUD 53200 (2026, Australia/Clayton campus)",
      "totalTuition": "AUD 212800",
      "estLivingPerYear": "AUD 28000",
      "durationYears": 4,
      "approxTotalMyr": 945168,
      "scholarshipAndPortal": "Monash International Merit Scholarship — AUD 15,000 per year (2026 rate) toward tuition, paid each year until you finish, on academic merit.",
      "scholarshipCoverage": "Partial — a fixed AUD 15,000/yr (~28% of the ~AUD 53k fee); no full ride, no living stipend.",
      "scholarshipCompetitiveness": "Merit-based and competitive; Monash publishes no award count/rate. A*A*A*A* is well above entry so competitive for the award.",
      "howToGetScholarship": "Applied for through/with your admission application (check the scholarship page for whether a separate form is needed for your intake); awarded on academic merit. No bond.",
      "moneyToShowVisa": "Student visa (subclass 500): tuition + ~AUD 29,710/yr living + travel shown (CoE)",
      "workRightsAfterGraduating": "post-study work visa ~2-3 yrs; strong AUD",
      "recognisedInMalaysia": "Washington Accord (Engineers Australia); MQA: verify",
      "howToApply": "Direct / UAC International",
      "keyDeadline": "Rolling; ~Apr 2027 for Jul 2027 intake (~Nov 2026 for Feb 2027)",
      "intake": "2027 (Jul realistic; Feb 2027 too early for A2 results)",
      "notes": "Clayton campus hosts Monash Nova Rover, a student team building Mars rovers for the University Rover Challenge in Utah.",
      "courseUrl": "https://www.monash.edu/engineering",
      "infoSource": "Official page"
    },
    {
      "id": "ntu",
      "shortName": "NTU",
      "listStatus": "Shortlist",
      "desirability": 86,
      "tier": "A",
      "admissionLikelihood": "Match",
      "warnings": "None",
      "university": "Nanyang Technological University",
      "course": "BEng Robotics (AI & Mechatronics Systems)",
      "courseAtAGlance": "4-year BEng blending mechanical, electrical, mechatronics & AI courses; accelerated 3.5-year track for high performers.",
      "country": "Singapore",
      "city": "Singapore",
      "studentLife": "NTU's 'smart campus' runs driverless buses & campus-wide robotics; MAE Robotics Club, RoboMaster Society, and a Makerspace at The Arc.",
      "subjectRank": "Engineering strong; NTU overall QS ~#15",
      "overallRank": "QS ~#15",
      "entryRequirements": "Good passes in >=3 A-levels incl A-level Maths or Further Maths; competitive for intl places",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Meets",
      "englishReq": "IELTS 6.0 (Writing 6, Speaking 6)",
      "annualTuition": "SGD 20700 (ASEAN, with MOE Tuition Grant; non-subsidised ~SGD 45600)",
      "totalTuition": "SGD 82800",
      "estLivingPerYear": "SGD 12000",
      "durationYears": 4,
      "approxTotalMyr": 417252,
      "scholarshipAndPortal": "Two routes. (1) MOE Tuition Grant — the standard subsidised-fee route for international students: cuts the engineering fee from ~SGD 45,600 to ~SGD 20,700/yr for a 3-year Singapore work bond;",
      "scholarshipCoverage": "NTU ASEAN Undergraduate Scholarship = full subsidised tuition (after the MOE grant)",
      "scholarshipCompetitiveness": "MOE Tuition Grant is broadly available (near-automatic for admitted international students who accept the bond).",
      "howToGetScholarship": "Apply for NTU undergraduate admission; you are considered for the ASEAN Undergraduate Scholarship through that application (shortlisted applicants may be interviewed) — no separate form for most.",
      "moneyToShowVisa": "Student's Pass: tuition + living shown",
      "workRightsAfterGraduating": "No post-study work visa, but the tuition-grant bond requires 3 years with a Singapore-registered company — a guaranteed route into an SGD salary.",
      "recognisedInMalaysia": "Yes — NTU engineering is accredited under the Washington Accord (via IES Singapore) and NTU degrees are recognised by MQA;",
      "howToApply": "Direct (NTU online application)",
      "keyDeadline": "2027-02-23 (approx; Aug 2027 intake portal opens ~Dec 2026, closes ~late Feb 2027 — confirm exact date)",
      "intake": "2027 Aug",
      "notes": "Ranked #1 Asia/#4 world for Mechanical/Aeronautical/Manufacturing (QS 2025); no mandatory internship stated on programme page.",
      "courseUrl": "https://www.ntu.edu.sg/education/undergraduate-programme/bachelor-of-engineering-in-robotics",
      "infoSource": "Official page"
    },
    {
      "id": "rose-hulman",
      "shortName": "Rose-Hulman",
      "listStatus": "Longlist",
      "desirability": 81,
      "tier": "A",
      "admissionLikelihood": "Safety",
      "warnings": "None",
      "university": "Rose-Hulman Institute of Technology",
      "course": "BS Mechanical Engineering (Robotics minor)",
      "courseAtAGlance": "ABET-accredited BS Mechanical Engineering plus a 7-course Robotics minor most finish in 4 yrs; Mechatronics (ME430) is required for all ME majors.",
      "country": "USA",
      "city": "Terre Haute, Indiana",
      "studentLife": "Small Terre Haute campus; 90+ clubs, MakerLab, and robotics teams compete in Intelligent Ground Vehicle and MATE-ROV competitions.",
      "subjectRank": "#1 undergraduate engineering (US News 2027, non-doctoral schools) and #1 mechanical engineering, both per Rose-Hulman's own pages",
      "overallRank": "Specialist undergrad engineering leader (low global brand recognition)",
      "entryRequirements": "Holistic review, no fixed grade cutoff. Expects 4 yrs math, 4 English, 3 lab science (bio, chem, physics), 2 social science. SAT/ACT not required (optional).",
      "studentGrades": "A*A*A*A* predicted (Maths, Further Maths, Physics, Chemistry)",
      "gradesVsEntryBar": "Above",
      "englishReq": "IELTS 6.5 (6.0 each); TOEFL iBT 88 (20 each) or 4.5 new scale; Duolingo 110; PTE 59. Waived: SAT EBRW 500+/ACT Eng 21+",
      "annualTuition": "USD 59772",
      "totalTuition": "USD 239088",
      "estLivingPerYear": "USD 24720",
      "durationYears": 4,
      "approxTotalMyr": 1365391,
      "scholarshipAndPortal": "Merit scholarship (every applicant); FIRST/VEX USD 10,000/yr (Feb 1); Competition Teams USD 1,000-2,500/yr (Apr 1, 2026-27 award). Intl eligibility not stated. rose-hulman.edu portal.",
      "scholarshipCoverage": "Merit: amount unpublished. FIRST/VEX USD 10,000/yr; Competition Teams USD 1,000-2,500/yr. Intl eligibility not stated.",
      "scholarshipCompetitiveness": "No award-rate statistics published. Intl students pay ~USD 45,000/yr on average; full-tuition awards 'extremely limited'; cannot meet full need.",
      "howToGetScholarship": "1) Apply by Early Action Nov 1 or Regular Feb 1; merit is offered to every applicant. 2) If admitted: FIRST/VEX form by Feb 1; Competition Teams interest form by Apr 1.",
      "moneyToShowVisa": "student visa: show net cost on the student visa form",
      "workRightsAfterGraduating": "student visa post-study work permit 12 + 24-month science post-study work extension (36 months); very strong placement into US engineering roles",
      "recognisedInMalaysia": "ME is ABET-accredited (RHIT page). ABET is a Washington Accord signatory, so BEM can recognise it. MQA/eSISRAF status not checked; confirm there.",
      "howToApply": "Common App",
      "keyDeadline": "2027-02-01 (Regular Decision; Early Action 2026-11-01, non-binding)",
      "intake": "Fall 2027",
      "notes": "Robotics is a 7-course minor on the ME degree, not a degree. Annual tuition is the combined tuition-and-fees line. Intl students also pay ~USD 1,091/yr health insurance, not in cost columns.",
      "courseUrl": "https://www.rose-hulman.edu/academics/academic-departments/mechanical-engineering/index.html",
      "infoSource": "Official page"
    },
    {
      "id": "northeastern",
      "shortName": "Northeastern",
      "listStatus": "Longlist",
      "desirability": 83,
      "tier": "A",
      "admissionLikelihood": "Match",
      "warnings": "None",
      "university": "Northeastern University",
      "course": "Mechanical Engineering, BSME (Boston) with Robotics Minor (co-op)",
      "courseAtAGlance": "BSME takes 4 yrs with 2 six-month co-ops, or 5 yrs with 3; the Robotics minor (5 courses: ME, EECE, CS) is run by the ECE dept and added on top.",
      "country": "USA",
      "city": "Boston, Massachusetts",
      "studentLife": "Boston campus in a major city; NURobotics club (470+ members, 8 robots) is one of the largest engineering clubs on campus.",
      "subjectRank": "Rising national engineering; defining feature is the co-op (paid work-integrated) program; robotics minor + research",
      "overallRank": "US News national ~#40s (risen fast); QS ~#150s globally",
      "entryRequirements": "Holistic; no minimum grades published. SAT/ACT test-optional. Needs physics, chemistry, precalculus. A-Level predicted grades accepted; final results required.",
      "studentGrades": "A*A*A*A* predicted (Maths, Further Maths, Physics, Chemistry)",
      "gradesVsEntryBar": "Meets",
      "englishReq": "No minimum; IELTS, TOEFL iBT, DET or PTE (admits' IELTS 7.5-8.0). Waiver: 4 straight yrs English-medium schooling.",
      "annualTuition": "USD 71050",
      "totalTuition": "USD 284200",
      "estLivingPerYear": "USD 27272",
      "durationYears": 4,
      "approxTotalMyr": 1588884,
      "scholarshipAndPortal": "International Scholars Award (merit); John Martinson Honors invite. International students get merit only, no need-based aid. Considered automatically via the Common App/Coalition application.",
      "scholarshipCoverage": "International Scholars Award up to USD 28,000/yr; does not cover full cost of attendance (about USD 98,322/yr)",
      "scholarshipCompetitiveness": "No statistics published; described as 'extremely competitive'. Admission is need-aware for internationals.",
      "howToGetScholarship": "(1) Apply by 2027-01-01 (Regular Decision) via Common App or Coalition; (2) submit the Declaration and Certification of Finances; (3) no separate form: merit is decided with admission.",
      "moneyToShowVisa": "student visa: show net cost on the student visa form (co-op is authorized work under CPT)",
      "workRightsAfterGraduating": "Co-op → strong job pipeline; student visa post-study work permit 12 + 24-month science post-study work extension (36 months); excellent employability",
      "recognisedInMalaysia": "ABET-accredited BS Mechanical Engineering → Washington Accord (USA) → supports BEM. Confirm MQA equivalence.",
      "howToApply": "Common App",
      "keyDeadline": "2027-01-01 (Regular Decision; Early Action 2026-11-01; Early Decision I 2026-11-01, Early Decision II 2027-01-01)",
      "intake": "Fall 2027",
      "notes": "Co-op is optional, but 90%+ of Mechanical & Industrial Eng undergrads do one. Job offers after co-op are shown in dept student stories; no conversion rate is published.",
      "courseUrl": "https://catalog.northeastern.edu/undergraduate/engineering/mechanical-industrial/bsme/",
      "infoSource": "Official page"
    },
    {
      "id": "melbourne",
      "shortName": "Melbourne",
      "listStatus": "Longlist",
      "desirability": 75,
      "tier": "A",
      "admissionLikelihood": "Safety",
      "warnings": "None",
      "university": "University of Melbourne",
      "course": "BSc (Mechatronics Systems major) + Master of Mechatronics Engineering",
      "courseAtAGlance": "3-yr BSc then a 2-yr master's (the Melbourne Model) — about 5 years total for the accredited qualification.",
      "country": "Australia",
      "city": "Melbourne, VIC",
      "studentLife": "Lively Parkville campus beside inner-city Melbourne; cultural and walkable rather than outdoorsy.",
      "subjectRank": "Engineering ~top 30; Melbourne overall QS ~#13 (Australia's top)",
      "overallRank": "QS ~#13",
      "entryRequirements": "A-levels incl Maths for BSc entry; Master needs BSc (Mechatronics Systems) grade average >=65%",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Above",
      "englishReq": "IELTS 6.5 (6.0)",
      "annualTuition": "AUD ~49188 BSc yr / ~58000 Master yr",
      "totalTuition": "AUD ~263564 (3yr BSc + 2yr Master)",
      "estLivingPerYear": "AUD 28000",
      "durationYears": 5,
      "approxTotalMyr": 1174371,
      "scholarshipAndPortal": "Melbourne International Undergraduate Scholarship — a fee remission on the Bachelor of Science part, automatically considered when you apply.",
      "scholarshipCoverage": "Partial — 20% of BSc tuition (from 2027) for the undergraduate years only;",
      "scholarshipCompetitiveness": "Automatically considered (no separate form); awarded on academic merit with course/region quotas — competitive, but 225 awards/yr from 2027.",
      "howToGetScholarship": "Automatic on applying for the BSc — no separate application. Merit-assessed against a quota. The Master years need separate graduate funding.",
      "moneyToShowVisa": "Student visa (subclass 500): tuition + ~AUD 29,710/yr living + travel shown (CoE)",
      "workRightsAfterGraduating": "post-study work visa; master's = longer PSW eligibility; strong AUD",
      "recognisedInMalaysia": "Washington Accord (Engineers Australia, via Master); MQA: verify",
      "howToApply": "Direct / UAC International",
      "keyDeadline": "Rolling; ~Apr 2027 for Jul (S2) 2027 intake (~Nov 2026 for Feb/S1 2027)",
      "intake": "2027 (Jul/S2 realistic; Feb/S1 2027 too early for A2 results)",
      "notes": "Melbourne Model: 3-yr BSc major + 2-yr Master required for Engineers Australia accreditation (~5 yrs total); grade average ≥65% needed to progress from BSc into Master.",
      "courseUrl": "https://study.unimelb.edu.au/find/courses/graduate/master-of-mechatronics-engineering/",
      "infoSource": "Official page"
    },
    {
      "id": "cmu",
      "shortName": "Carnegie Mellon",
      "listStatus": "Rejected",
      "desirability": 70,
      "tier": "B",
      "admissionLikelihood": "Reach (very selective)",
      "warnings": "Scholarship gap: no need-based aid for international undergraduates — clashes with his #1 priority.",
      "university": "Carnegie Mellon University",
      "course": "BS Mechanical Engineering (+ Robotics Institute minor)",
      "courseAtAGlance": "BS Mechanical Engineering, flexible curriculum; pairs with RI's Robotics Minor (controls, kinematics, 2 electives) for a robotics track.",
      "country": "USA",
      "city": "Pittsburgh, PA",
      "studentLife": "Pittsburgh campus, 350+ clubs incl. robotics/engineering teams; CMU's Robotics Institute pioneered robotics research and education.",
      "subjectRank": "#1 robotics globally (Robotics Institute); QS Eng ~top 20",
      "overallRank": "QS ~#52",
      "entryRequirements": "Holistic; top STEM academics (~A*A*A*A*) + essays; highly selective",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "TOEFL 100+ / IELTS 7.5+",
      "annualTuition": "USD 67020 (2025/26 tuition; +USD 1,076 fees — official). 2026/27 ~+4%.",
      "totalTuition": "USD 268080 (4 yrs, 2025/26 base)",
      "estLivingPerYear": "USD 18894 (room USD 11,250 + board USD 7,644, 2025/26)",
      "durationYears": 4,
      "approxTotalMyr": 1388370,
      "scholarshipAndPortal": "CMU does NOT award need-based institutional aid to international undergraduates — only DACA students and a small number from specific countries (e.g.",
      "scholarshipCoverage": "None realistically available — no need-based or merit aid for international undergraduates. External sponsors only.",
      "scholarshipCompetitiveness": "N/A — there is no CMU aid to compete for as an international undergrad.",
      "howToGetScholarship": "No CMU route. Only path to funding = external Malaysian sponsors (JPA/MARA/Yayasan) or private scholarships, applied for separately and not guaranteed. Otherwise budget the full ~USD 348k (~RM1.64M).",
      "moneyToShowVisa": "student visa form financial documentation",
      "workRightsAfterGraduating": "STEM-designated: post-study work permit 12 mo + science post-study work extension 24 mo = up to 3 yrs; strong US tech market + strong USD.",
      "recognisedInMalaysia": "BS Mechanical Engineering is ABET-accredited + USA is a Washington Accord signatory — supports BEM; confirm MQA equivalence at mqa.gov.my.",
      "howToApply": "Common App",
      "keyDeadline": "2027-01-03 (Regular Decision; Early Decision ~2026-11-01)",
      "intake": "2027 Sept",
      "notes": "Robotics Minor needs 2.5 QPA, max 2 courses double-counted with ME major; CMU founded the field's first Robotics Institute (1979).",
      "courseUrl": "https://www.meche.cmu.edu/",
      "infoSource": "Official page"
    }
  ];

  /* ---- GENERATED from business/university_report.md, "What is inside a report". ---- */

  const REPORT_SECTIONS = [
    {
      "n": 1,
      "title": "Snapshot",
      "tells": "A one-table summary: university, course, city, rankings, how you apply, your chance of getting in, and your own priorities listed in order.",
      "question": "Orientation"
    },
    {
      "n": 2,
      "title": "Identity and what it's known for",
      "tells": "What the university is trying to be, and what it is famous for.",
      "question": "Who is this place?"
    },
    {
      "n": 3,
      "title": "Who it's for",
      "tells": "The kind of student the place attracts and shapes, and an honest read on whether you fit.",
      "question": "Who is this place?"
    },
    {
      "n": 4,
      "title": "Getting in",
      "tells": "The entry requirements, how your grades compare, what admitted students really looked like, and what the application makes you submit.",
      "question": "Can I get in?"
    },
    {
      "n": 5,
      "title": "What you'll actually study",
      "tells": "The subjects, how long it takes, and how hard it is to change course once you start.",
      "question": "What would I study?"
    },
    {
      "n": 6,
      "title": "Signature academic experiences",
      "tells": "Named opportunities such as undergraduate research, work placements and study abroad.",
      "question": "What would I study?"
    },
    {
      "n": 7,
      "title": "Culture and vibe",
      "tells": "Whether students compete or cooperate, how heavy the workload is, how teaching is done.",
      "question": "Will I belong?"
    },
    {
      "n": 8,
      "title": "Student life, housing and food",
      "tells": "Where you live, what you eat, clubs, the first-year experience, and links to real students describing it.",
      "question": "Will I belong?"
    },
    {
      "n": 9,
      "title": "The city, the area and belonging",
      "tells": "Safety, transport, things to do, the Malaysian community, prayer facilities.",
      "question": "Will I belong?"
    },
    {
      "n": 10,
      "title": "Costs (full)",
      "tells": "Tuition, living costs, fees and deposit, added into one total for the whole degree in ringgit.",
      "question": "Can I afford it?"
    },
    {
      "n": 11,
      "title": "Scholarships and financial aid",
      "tells": "Funding from the university, from governments and from Malaysian sponsors, with who qualifies for each.",
      "question": "Can I afford it?"
    },
    {
      "n": 12,
      "title": "Outcomes, network and practising in Malaysia",
      "tells": "Graduate jobs and salaries, whether the degree is accepted back home, and whether you may stay and work after graduating.",
      "question": "What is the payoff?"
    },
    {
      "n": 13,
      "title": "Unique facts and quirks",
      "tells": "Traditions and notable graduates in your field. The detail that makes the place feel real.",
      "question": "Colour"
    },
    {
      "n": 14,
      "title": "Why here / why hesitate",
      "tells": "Two to four reasons to choose this university and the reasons to hesitate, tied to your priorities.",
      "question": "Should I?"
    },
    {
      "n": 15,
      "title": "Sources",
      "tells": "Every source used, labelled as official or not, with the admission year it applies to.",
      "question": "Can I trust this?"
    }
  ];

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
