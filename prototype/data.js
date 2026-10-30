/*
 * data.js — window.DATA. Owner: Session 1. Read-only for Sessions A, B, C.
 *
 * Anything shown on more than one screen (names, costs, grades, prices, dates) lives here.
 * Never retype a number in a screen file: read it from DATA.
 *
 * Only the anonymised sample student ("Arif") is used. Sources:
 *   business/sales/sample_pack/sample_master_list.csv          -> columns, universities
 *   business/sales/sample_pack/sample_university-report_MIT.pdf -> report summary, why here / why hesitate
 *   business/product_report/university_report.md ("What is inside a report")   -> report.sections
 *   business/sales/pitch/university-research-service-poster.html -> brand, feedback, report.pullQuote
 *   business/sales/service-tiers.md                             -> deliverables, pricing wording
 *   business/product_report/decide_report.md, business/product_report/apply_guide_report.md   -> shape of decision
 *
 * window.DATA
 *   brand         { name, tagline }
 *   student       { nickname, isSample, sampleNote, whatsapp, qualification, grades, subjects[],
 *                   course, countries[], budget { band, ceilingMyr }, scholarshipNeeded, priorities[] }
 *   intake        { qualifications[], extraCountries[], budgetBands[] } the choices the sign-up
 *                   form offers besides the sample student's own answers
 *   bands[]       { key, label } reach / match / safety, in display order
 *   columns[]     { key, label } for all 40 spreadsheet columns, in spreadsheet order
 *   columnGroups[] { title, keys[] } how those columns group when a list row is opened. A column
 *                   named in no group falls into the last one
 *   universities[] one object per spreadsheet row: the 40 column keys, plus
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
    },
    {
      "key": "applicationRequirements",
      "label": "Application requirements"
    },
    {
      "key": "checkedOn",
      "label": "Checked on"
    },
    {
      "key": "admitRate",
      "label": "Admit rate"
    },
    {
      "key": "applyLink",
      "label": "Apply link"
    },
    {
      "key": "scholarshipLink",
      "label": "Scholarship link"
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
      "studentLife": "First-years must live on campus (20 halls). Halal: Maseeh dining hall stations plus Argana Falafel in the Student Center; musalla in W11.",
      "subjectRank": "1",
      "overallRank": "1",
      "entryRequirements": "Holistic; no fixed grade cutoff or course list. SAT or ACT required (no cutoff or recommended scores); take by Nov 30 (Early Action) or Dec 31 (Regular Action).",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Not published",
      "englishReq": "Not required; strongly recommended if you used English under 5 years or not at school. IELTS min 7, recommended 7.5.",
      "annualTuition": "USD 66,720",
      "totalTuition": "USD 266,880",
      "estLivingPerYear": "USD 26,040",
      "durationYears": 4,
      "approxTotalMyr": 1499002,
      "scholarshipAndPortal": "No merit scholarships — MIT meets 100% of demonstrated financial need with MIT Scholarship grants (never repaid).",
      "scholarshipCoverage": "Need blind + meets 100% of demonstrated need for all, incl. international; MIT FAQ: 'one of only nine' US schools.",
      "scholarshipCompetitiveness": "The aid is guaranteed by policy once admitted — no separate scholarship contest.",
      "howToGetScholarship": "(1) Apply by 2027-01-04; (2) file CSS Profile (code 3514), upload parent tax/income docs to IDOC by aid deadline: 2026-11-30 (Early Action) or 2027-02-15 (Regular Action); (3) offer by email.",
      "moneyToShowVisa": "Bank proof meeting MIT's cost of attendance: USD 92,760 for 2026-27",
      "workRightsAfterGraduating": "Post-study work permit 12 mo, plus 24 mo extension for STEM degrees = up to 3 yrs.",
      "recognisedInMalaysia": "ABET-accredited (Course 2); the US is a Washington Accord signatory (basis for BEM registration). MQA eSISRAF lists MIT with a Science (BSc) row.",
      "howToApply": "MIT application (not Common App)",
      "keyDeadline": "2027-01-04 (Regular Action; Early Action 2026-11-01)",
      "intake": "2027 Sept",
      "notes": "MIT says it is need blind and meets 100% of demonstrated need for all undergrads incl. international; aid never includes loans. Class of 2029: 4.6% admitted overall; intl 136 of 6,926.",
      "courseUrl": "https://meche.mit.edu/",
      "infoSource": "Official page",
      "applicationRequirements": "Essay · 2 recommendation letters · Test: SAT or ACT",
      "checkedOn": "2026-10-30",
      "admitRate": "4.6% of all applicants admitted, 2025-26",
      "applyLink": "https://mitadmissions.org/apply/firstyear/deadlines-requirements/",
      "scholarshipLink": "https://sfs.mit.edu/undergraduate-students/types-of-aid/mit-scholarship/"
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
      "subjectRank": "3",
      "overallRank": "10",
      "entryRequirements": "Common Engineering admission with ME and ESP; Maths required; Singapore A-Level profile BBB/C to AAA/A (10th-90th percentile, AY2025/26 offers)",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Meets",
      "englishReq": "Not required — NUS asks A-Level applicants for no English test; IELTS/TOEFL optional to submit",
      "annualTuition": "SGD 18,050",
      "totalTuition": "SGD 72,200",
      "estLivingPerYear": "SGD 13,145",
      "durationYears": 4,
      "approxTotalMyr": 398048,
      "scholarshipAndPortal": "(1) MOE Tuition Grant, taken up on acceptance of the NUS offer; (2) ASEAN Undergraduate Scholarship, via the NUS Applicant Portal application.",
      "scholarshipCoverage": "MOE Tuition Grant cuts the fee from SGD 39,700 to SGD 18,050 a year (54.5% off), with a 3-year Singapore work bond.",
      "scholarshipCompetitiveness": "MOE Tuition Grant is broadly available (near-automatic for admitted international students who accept the bond) = low competitiveness.",
      "howToGetScholarship": "Apply for NUS admission; eligible ASEAN applicants are considered for the ASEAN Undergraduate Scholarship through it, no separate form; shortlisted applicants are interviewed Jan-Jul.",
      "moneyToShowVisa": "ICA publishes no fixed amount; the Student's Pass follows NUS admission and fee payment",
      "workRightsAfterGraduating": "No post-study work visa; the Tuition Grant bond requires 3 years working for a Singapore-registered company after graduation.",
      "recognisedInMalaysia": "RMI is not on the IES Engineering Accreditation Board list (Dec 2025); BEng Mechanical Engineering is, from AY2007/08",
      "howToApply": "Direct (NUS online application)",
      "keyDeadline": "2027-02-17 (AY2027/28 international window: 16 Dec 2026 - 17 Feb 2027, per NUS Office of Admissions)",
      "intake": "2027 Aug",
      "notes": "New programme from AY2025/26, so no graduates yet; admitted through the common Engineering pool shared with Mechanical Engineering; spans ME, BME, ChBE, ECE and MSE depts.",
      "courseUrl": "https://cde.nus.edu.sg/me/undergraduate/beng-rmi/overview/",
      "infoSource": "Official page",
      "applicationRequirements": "Personal statement",
      "checkedOn": "2026-10-30",
      "admitRate": "Not published",
      "applyLink": "https://www.nus.edu.sg/oam/admissions/important-dates",
      "scholarshipLink": "https://www.moe.gov.sg/financial-matters/tuition-grant-scheme"
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
      "courseAtAGlance": "4-yr BEng(Hons) at Clayton: common first year, robotics and mechatronics specialisation from Yr2, 12 weeks of work experience required.",
      "country": "Australia",
      "city": "Melbourne, VIC",
      "studentLife": "Large suburban Clayton campus in Melbourne with standout student teams (Motorsport, Nova Rover).",
      "subjectRank": "70",
      "overallRank": "31",
      "entryRequirements": "GCE A Levels score of 10 for 2027 entry, with Maths and Chemistry or Physics",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Above",
      "englishReq": "IELTS 6.5 (6.0)",
      "annualTuition": "AUD 59,600",
      "totalTuition": "AUD 238,400",
      "estLivingPerYear": "AUD 29,710",
      "durationYears": 4,
      "approxTotalMyr": 1039568,
      "scholarshipAndPortal": "Monash International Merit Scholarship — AUD 15,000 per year (2026 rate) toward tuition, paid each year until you finish, on academic merit.",
      "scholarshipCoverage": "Partial: a fixed AUD 15,000/yr (25% of the AUD 59,600 fee); no full ride, no living stipend.",
      "scholarshipCompetitiveness": "Merit-based; 20 awards a year across all international undergraduate offer-holders; a 70% average each semester keeps it.",
      "howToGetScholarship": "No application: international undergraduates with a full unconditional Monash offer are considered automatically; awarded on academic achievement.",
      "moneyToShowVisa": "Student visa (subclass 500): AUD 29,710 living costs for 12 months, plus tuition fees",
      "workRightsAfterGraduating": "Post-study work visa: 2 years after a bachelor degree (including honours)",
      "recognisedInMalaysia": "Engineers Australia-accredited (Washington Accord), which BEM accepts for Graduate Engineer",
      "howToApply": "Direct online application to Monash (not VTAC)",
      "keyDeadline": "Rolling",
      "intake": "2027 (Jul realistic; Feb 2027 too early for A2 results)",
      "notes": "Clayton campus hosts Monash Nova Rover, a student team building Mars rovers for the University Rover Challenge in Utah.",
      "courseUrl": "https://www.monash.edu/engineering",
      "infoSource": "Official page",
      "applicationRequirements": "Not published",
      "checkedOn": "2026-10-30",
      "admitRate": "Not published",
      "applyLink": "https://www.monash.edu/admissions/apply/international-ug",
      "scholarshipLink": "https://www.monash.edu/study/fees-scholarships/scholarships/find-a-scholarship/international-merit-5770"
    },
    {
      "id": "cambridge",
      "shortName": "Cambridge",
      "listStatus": "Finalist",
      "desirability": 69,
      "tier": "B",
      "admissionLikelihood": "Reach (test + interview)",
      "warnings": "Deadline passed",
      "university": "University of Cambridge",
      "course": "Engineering MEng (general; robotics/mechatronics specialise Yr3-4)",
      "courseAtAGlance": "4-yr MEng: 2 yrs general engineering core, then specialise from Yr3 into disciplines incl. robotics/mechatronics via Info & Computer or Mech Eng.",
      "country": "UK",
      "city": "Cambridge",
      "studentLife": "Collegiate Cambridge; student-run Robotics Society and Formula Student team Full Blue Racing build robots and race cars in dept workshops.",
      "subjectRank": "4",
      "overallRank": "6",
      "entryRequirements": "A*A*A at A-level incl Maths + Physics (plus Further Maths if offered); ESAT (Maths 1, Maths 2, Physics) + interview. Holistic selection.",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "IELTS 7.5 overall (7.0 per element). Waived only for majority English-speaking countries; Malaysia is not one.",
      "annualTuition": "GBP 46,872",
      "totalTuition": "GBP 243,676",
      "estLivingPerYear": "GBP 15,960",
      "durationYears": 4,
      "approxTotalMyr": 1682113,
      "scholarshipAndPortal": "Cambridge Trust scholarships (cambridgetrust.org) — the main international route — plus College awards and country-specific schemes.",
      "scholarshipCoverage": "Mostly partial for international undergraduates (a means-tested fee contribution); full-cost awards are rare.",
      "scholarshipCompetitiveness": "Highly competitive and limited for undergraduates.",
      "howToGetScholarship": "Be offered a place, declare financial need and apply via the Cambridge Trust / College funding routes by their deadlines (means-tested + merit).",
      "moneyToShowVisa": "GBP 10,539 living (9 months at GBP 1,171, outside London) plus first-year course fee on the CAS",
      "workRightsAfterGraduating": "UK Graduate visa: 18 months for applications from 1 Jan 2027; a Skilled Worker visa is needed to stay longer.",
      "recognisedInMalaysia": "MEng accredited by Engineering Council and bodies incl. IMechE, IET, RAeS, depending on papers taken; CEng-accredited UK MEng is Washington Accord-recognised",
      "howToApply": "UCAS (+ college choice, ESAT admissions test + interview)",
      "keyDeadline": "2026-10-15",
      "intake": "2027 Oct",
      "notes": "Progression to Yr3/4 needs min 2.ii; no standalone robotics degree, mechatronics via Info & Computer Eng / Mech Eng in Yr3-4. Total adds 4 yrs of College fee (2027-28 average GBP 14,047).",
      "courseUrl": "https://www.undergraduate.study.cam.ac.uk/courses/engineering",
      "infoSource": "Official page",
      "applicationRequirements": "Personal statement · 1 recommendation letter · Interview · Test: ESAT",
      "checkedOn": "2026-10-30",
      "admitRate": "15.2% of international applicants offered a place, 2025-26",
      "applyLink": "https://www.undergraduate.study.cam.ac.uk/apply/how/ucas-application",
      "scholarshipLink": "https://www.undergraduate.study.cam.ac.uk/international-students/financial-support"
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
      "studentLife": "Residential Zijing College on campus, with academics alongside student activities.",
      "subjectRank": "12",
      "overallRank": "14",
      "entryRequirements": "Foreign passport, full-time high school certificate, transcripts or SAT/ACT/A-Level/AP/IB results; holistic review plus a Comprehensive Assessment.",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "IELTS/TOEFL required; no fixed minimum published (holistic)",
      "annualTuition": "CNY 100,000",
      "totalTuition": "CNY 400,000",
      "estLivingPerYear": "CNY 40,000",
      "durationYears": 4,
      "approxTotalMyr": 336000,
      "scholarshipAndPortal": "Chinese Government Scholarship (CSC), the main full-ride route - apply Type A via the Chinese Embassy in Malaysia (agency 4581) on studyinchina.csc.edu.cn; NOT Type B via Tsinghua for undergrads.",
      "scholarshipCoverage": "CSC full award: tuition, campus accommodation, monthly stipend and medical insurance. Airfare not included.",
      "scholarshipCompetitiveness": "Very competitive - Tsinghua is China's top university and CSC does not publish per-university award rates, so treat exact odds as unpublished.",
      "howToGetScholarship": "Separate from admission: apply for CSC Type A through the Chinese Embassy, listing Tsinghua first. Tsinghua's page gives a Nov 2026 to Apr 2027 window, set per country.",
      "moneyToShowVisa": "Bank statement for X1 student visa (modest)",
      "workRightsAfterGraduating": "Work (Z) visa possible but hard for fresh grads; weak fit for Arif's stronger-currency migration goal",
      "recognisedInMalaysia": "CEEAA accreditation not published for this English-taught Zijing programme; BEM relies on it.",
      "howToApply": "Direct - apply.join-tsinghua.edu.cn/international (+ CSC applied separately)",
      "keyDeadline": "2027-02-28",
      "intake": "2027 Sept",
      "notes": "Zijing College is Tsinghua's 1st English-taught residential college; ME sits alongside IST, civil eng & design science in one multidisciplinary STEAM curriculum. App fee RMB800 + RMB800/yr insurance.",
      "courseUrl": "https://international.join-tsinghua.edu.cn/info/1082/1185.htm",
      "infoSource": "Official page",
      "applicationRequirements": "Test: Comprehensive Assessment",
      "checkedOn": "2026-10-30",
      "admitRate": "Not published",
      "applyLink": "https://apply.join-tsinghua.edu.cn/international/res/SpecialWsbm/index.html",
      "scholarshipLink": "https://international.join-tsinghua.edu.cn/Admission1/Freshmen_Scholarships1.htm"
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
      "subjectRank": "38",
      "overallRank": "27",
      "entryRequirements": "Holistic review of transcript, teacher and counselor letters and essays; no minimum grades or GPA published",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Not published",
      "englishReq": "TOEFL, IELTS Academic, Duolingo or PTE Academic if English is not your native language and school is not English-taught",
      "annualTuition": "USD 68,140",
      "totalTuition": "USD 272,560",
      "estLivingPerYear": "USD 26,484",
      "durationYears": 4,
      "approxTotalMyr": 1529124,
      "scholarshipAndPortal": "No merit scholarships; need-based grants (never repaid) replace loans and meet 100% of demonstrated need, apply via Princeton's own PFAA",
      "scholarshipCoverage": "Need-blind for internationals; one of the few US schools that never caps international aid.",
      "scholarshipCompetitiveness": "Guaranteed once admitted, no separate contest. Gate is admission: 4.4% of all applicants (CDS 2025-26); 241 of 10,567 international applicants (2.3%)",
      "howToGetScholarship": "File Princeton's own PFAA (no CSS Profile) + parents' tax docs: due Nov 9 (Single-Choice Early Action) or Feb 1 (Regular Decision). Need-blind incl. internationals; no merit aid.",
      "moneyToShowVisa": "student visa form financial documentation",
      "workRightsAfterGraduating": "12 months post-study work + 24-month science post-study work extension = up to 3 yrs",
      "recognisedInMalaysia": "MAE's mechanical and aerospace BSE programs are ABET-accredited; the USA is a Washington Accord signatory, the basis for BEM registration",
      "howToApply": "Common App",
      "keyDeadline": "2027-01-01",
      "intake": "2027 Sept",
      "notes": "Test-optional through fall 2027 entry; SAT/ACT required from 2027-28 cycle (fall 2028 entry) on. No dedicated robotics major - reached via MAE electives + Robotics minor.",
      "courseUrl": "https://mae.princeton.edu/",
      "infoSource": "Official page",
      "applicationRequirements": "Personal statement · 3 recommendation letters",
      "checkedOn": "2026-10-30",
      "admitRate": "4.4% of all applicants admitted, 2025-26",
      "applyLink": "https://admission.princeton.edu/apply/application-checklist",
      "scholarshipLink": "https://finaid.princeton.edu/apply-aid-prospective-students"
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
      "subjectRank": "2",
      "overallRank": "=2",
      "entryRequirements": "Holistic review; SAT or ACT required; no minimum grades published",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Not published",
      "englishReq": "No English test required (optional to self-report); fluency in English is a prerequisite for admission.",
      "annualTuition": "USD 67,731",
      "totalTuition": "USD 270,924",
      "estLivingPerYear": "USD 29,814",
      "durationYears": 4,
      "approxTotalMyr": 1576327,
      "scholarshipAndPortal": "No merit scholarships (athletic aside); need-based aid only. Request it on the admission application, then file the CSS Profile (school code 4704).",
      "scholarshipCoverage": "Meets 100% of demonstrated need for every admitted student who requests aid, internationals included.",
      "scholarshipCompetitiveness": "Need-aware for internationals: an aid request is a factor in admission and international aid is limited. Admit rate 3.8% of all applicants.",
      "howToGetScholarship": "Tick the aid request on the admission application, then file the CSS Profile; ISAFA only if you cannot pay the Profile fee. Priority date 2027-02-15.",
      "moneyToShowVisa": "USD 97,545 (one year of funding, Stanford 2026-27 undergraduate budget)",
      "workRightsAfterGraduating": "12 months post-study work + 24-month science post-study work extension = up to 3 yrs.",
      "recognisedInMalaysia": "ABET-accredited Mechanical Engineering BS; USA is a Washington Accord signatory, which supports BEM registration; MQA lists foreign degrees at mqa.gov.my.",
      "howToApply": "Common App",
      "keyDeadline": "2027-01-05",
      "intake": "2027 Sept",
      "notes": "No dedicated robotics/mechatronics degree or concentration at Stanford ME; robotics learned via electives, ME320, and student robotics clubs/labs.",
      "courseUrl": "https://me.stanford.edu/",
      "infoSource": "Official page",
      "applicationRequirements": "Essay · 3 supplemental essays · 3 recommendation letters · Test: SAT or ACT",
      "checkedOn": "2026-10-30",
      "admitRate": "3.8% of all applicants admitted, 2025-26",
      "applyLink": "https://admission.stanford.edu/apply/first-year/index.html",
      "scholarshipLink": "https://financialaid.stanford.edu/undergrad/apply/requirements/rd_international.html"
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
      "subjectRank": "=46",
      "overallRank": "19",
      "entryRequirements": "A-levels aggregate 16.0 (A*=6 to E=1, best 3-4 A2 subjects); assumed knowledge Mathematics Extension 1 and Physics",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Above",
      "englishReq": "IELTS 6.5 (6.0)",
      "annualTuition": "AUD 61,500",
      "totalTuition": "AUD 265,500",
      "estLivingPerYear": "AUD 28,860",
      "durationYears": 4,
      "approxTotalMyr": 1108535,
      "scholarshipAndPortal": "International Scientia Coursework Scholarship (separate application on UNSW Scholarships portal); International Student Award (considered at admission)",
      "scholarshipCoverage": "Scientia: full tuition or AUD 20,000 per year for the minimum program length; Student Award: 20% of tuition",
      "scholarshipCompetitiveness": "Scientia is awarded on academic achievement, leadership and extracurriculars; award numbers not published",
      "howToGetScholarship": "Scientia: apply on the UNSW Scholarships portal by the round closing date (Term 1 2027 round closed 30 Oct 2026). Student Award: after applying, submit a brief motivation statement if invited.",
      "moneyToShowVisa": "Student visa (subclass 500): first-year tuition + AUD 29,710 living costs + travel",
      "workRightsAfterGraduating": "Post-study work visa: 2-3 yrs depending on qualification",
      "recognisedInMalaysia": "Engineers Australia accredited, Washington Accord",
      "howToApply": "Direct (UNSW Applicant Portal)",
      "keyDeadline": "Not published",
      "intake": "Terms 1, 2 and 3 2027",
      "notes": "Kensington campus; ChallEng industry projects, Robogals & Women in Engineering societies; optional Nuclear Engineering minor.",
      "courseUrl": "https://www.unsw.edu.au/study/undergraduate/bachelor-of-engineering-honours-robotics-mechatronics",
      "infoSource": "Official page",
      "applicationRequirements": "Not published",
      "checkedOn": "2026-10-30",
      "admitRate": "Not published",
      "applyLink": "https://apply.unsw.edu.au/",
      "scholarshipLink": "https://www.scholarships.unsw.edu.au/scholarships/id/1988"
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
      "studentLife": "First-years live in dorms in or next to Harvard Yard and eat together at Annenberg Hall.",
      "subjectRank": "=7",
      "overallRank": "5",
      "entryRequirements": "Holistic review, no fixed grade cutoff; SAT or ACT, school report, 2 teacher letters and essays",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Not published",
      "englishReq": "No English test required for first-year applicants (optional to submit).",
      "annualTuition": "USD 68,442",
      "totalTuition": "USD 273,768",
      "estLivingPerYear": "USD 26,692",
      "durationYears": 4,
      "approxTotalMyr": 1537365,
      "scholarshipAndPortal": "Harvard is NEED-BLIND for all applicants incl. internationals and meets 100% of demonstrated need with grants, no loans. Requested via the CSS Profile + IDOC with the Common App.",
      "scholarshipCoverage": "Full demonstrated need met with grants (never repaid), no loans.",
      "scholarshipCompetitiveness": "Aid is need-based and open to every admitted student; requesting aid does not affect admission.",
      "howToGetScholarship": "File the CSS Profile, then upload parent income documents to IDOC by Nov 1 (Restrictive Early Action) or Feb 1 (Regular Decision).",
      "moneyToShowVisa": "No fixed amount; student visa form with aid award letter or bank documents",
      "workRightsAfterGraduating": "12 months post-study work for any degree; 24-month science post-study work extension if the degree is on the US science-degree list.",
      "recognisedInMalaysia": "SB Mechanical Engineering is ABET-accredited + USA is a Washington Accord signatory - supports BEM. The AB Engineering Sciences track is NOT accredited.",
      "howToApply": "Common App",
      "keyDeadline": "2027-01-01",
      "intake": "2027 Sept",
      "notes": "Aid is 100% need-based, no merit scholarships (incl. int'l applicants). Robotics is a track within ME, not standalone; access to Wyss Institute and Microrobotics Lab.",
      "courseUrl": "https://seas.harvard.edu/",
      "infoSource": "Official page",
      "applicationRequirements": "Essay · 5 supplemental essays · 3 recommendation letters · Test: SAT",
      "checkedOn": "2026-10-30",
      "admitRate": "4.2% of all applicants admitted, 2025-26",
      "applyLink": "https://college.harvard.edu/admissions/apply/first-year-applicants",
      "scholarshipLink": "https://college.harvard.edu/financial-aid/how-aid-works"
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
      "subjectRank": "=9",
      "overallRank": "=2",
      "entryRequirements": "A*A*A or A*AAA, with A* in Maths and A/A* in Physics; ESAT (Maths 1, Maths 2, Physics) required; interview for shortlisted applicants.",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Well above",
      "englishReq": "IELTS 6.5, min 6.0 each (Imperial standard level); or SPM English 1119 grade A. No waiver for schooling in English",
      "annualTuition": "GBP 47,800",
      "totalTuition": "GBP 191,200",
      "estLivingPerYear": "GBP 22,722",
      "durationYears": 4,
      "approxTotalMyr": 1543021,
      "scholarshipAndPortal": "Imperial Inspires Scholarship (GBP 15,000/yr, via UCAS + optional statement by 5 Feb 2027) + Khazanah Global Scholarship (full; Imperial approved). GREAT Scholarships are postgraduate-only.",
      "scholarshipCoverage": "Imperial Inspires: GBP 15,000/yr every year (GBP 60,000 over 4 yrs), overseas-only, partial not a full ride.",
      "scholarshipCompetitiveness": "Imperial Inspires: 150 awards for 2027 entry across Engineering, Natural Sciences, Medicine and Business; entry requirements must be met.",
      "howToGetScholarship": "Apply to Imperial via UCAS by 13 Jan 2027; applicants meeting entry requirements are invited to submit an optional 250-word statement by 5 Feb 2027. Decisions by 30 Apr 2027.",
      "moneyToShowVisa": "Student visa: GBP 13,761 living (9 months x GBP 1,529 London) plus first-year tuition",
      "workRightsAfterGraduating": "UK Graduate Route: 18 months for applications from 1 Jan 2027 (2 years if applied by 31 Dec 2026), then a Skilled Worker visa is needed.",
      "recognisedInMalaysia": "MEng accredited by IMechE for the UK Engineering Council (CEng route); UK and Malaysia (BEM) are Washington Accord signatories; year-abroad not accredited.",
      "howToApply": "UCAS (+ ESAT admissions test + interview)",
      "keyDeadline": "2027-01-13 (UCAS equal consideration)",
      "intake": "2027 Sept",
      "notes": "No dedicated robotics stream: mechatronics is built into the core Mechanical Engineering curriculum. ESAT required.",
      "courseUrl": "https://www.imperial.ac.uk/study/courses/",
      "infoSource": "Official page",
      "applicationRequirements": "Personal statement · 1 recommendation letter · Interview · Test: ESAT",
      "checkedOn": "2026-10-30",
      "admitRate": "Not published",
      "applyLink": "https://www.imperial.ac.uk/study/apply/undergraduate/process/",
      "scholarshipLink": "https://www.imperial.ac.uk/study/fees-and-funding/scholarships-search/imperial-inspires-scholarships-undergraduate-20272028.php"
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
      "subjectRank": "5",
      "overallRank": "12",
      "entryRequirements": "A-Level H2 Maths plus Physics, Chemistry, Biology or Computing; UK A-Level needs at least 4 subjects at A2 in one sitting",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Meets",
      "englishReq": "IELTS Academic 6.5 overall, 6.5 Writing, 6.5 Speaking; TOEFL iBT 90 or PTE 55 also accepted",
      "annualTuition": "SGD 18,050",
      "totalTuition": "SGD 72,200",
      "estLivingPerYear": "SGD 10,920",
      "durationYears": 4,
      "approxTotalMyr": 369657,
      "scholarshipAndPortal": "NTU ASEAN Undergraduate Scholarship, form linked at the end of the NTU admission application; MOE Tuition Grant (SGD 18,050/yr for ASEAN, 3-year Singapore work bond)",
      "scholarshipCoverage": "NTU ASEAN Undergraduate Scholarship = full subsidised tuition (after the MOE grant)",
      "scholarshipCompetitiveness": "MOE Tuition Grant is open to admitted international students who sign the 3-year bond; ASEAN Scholarship award statistics are not published",
      "howToGetScholarship": "Submit the NTU admission application, then the scholarship form linked at its end: essay up to 250 words, photo, teacher referee appraisal. Interviews run March to May.",
      "moneyToShowVisa": "ICA Student's Pass page publishes no minimum funds amount",
      "workRightsAfterGraduating": "No post-study work visa; the Tuition Grant bond requires 3 years working for a Singapore entity after graduating.",
      "recognisedInMalaysia": "NTU BEng programmes are accredited by IES Singapore (Washington Accord signatory); IES list does not name Robotics",
      "howToApply": "Direct (NTU online application)",
      "keyDeadline": "2027-03-19",
      "intake": "2027 Aug",
      "notes": "Fee shown is ASEAN with Tuition Grant, AY2026/27, incl. 9% GST; without grant SGD 36,350-40,600. QS 2026 Mechanical, Aeronautical & Manufacturing: 5th.",
      "courseUrl": "https://www.ntu.edu.sg/education/undergraduate-programme/bachelor-of-engineering-in-robotics",
      "infoSource": "Official page",
      "applicationRequirements": "Not published",
      "checkedOn": "2026-10-30",
      "admitRate": "Not published",
      "applyLink": "https://www.ntu.edu.sg/admissions/undergraduate/application",
      "scholarshipLink": "https://www.ntu.edu.sg/admissions/undergraduate/scholarships/scholarship-opportunities/detail/asean-undergraduate-scholarship"
    },
    {
      "id": "rose-hulman",
      "shortName": "Rose-Hulman",
      "listStatus": "Longlist",
      "desirability": 71,
      "tier": "B",
      "admissionLikelihood": "Safety (high admit rate)",
      "warnings": "English short",
      "university": "Rose-Hulman Institute of Technology",
      "course": "BS Mechanical Engineering (Robotics minor)",
      "courseAtAGlance": "ABET-accredited BS Mechanical Engineering plus a 7-course Robotics minor most finish in 4 yrs; Mechatronics (ME430) is required for all ME majors.",
      "country": "USA",
      "city": "Terre Haute, Indiana",
      "studentLife": "Small Terre Haute campus; 90+ clubs, MakerLab, and robotics teams compete in Intelligent Ground Vehicle and MATE-ROV competitions.",
      "subjectRank": "Not ranked",
      "overallRank": "Not ranked",
      "entryRequirements": "Holistic review, no fixed grade cutoff. Coursework: 4 yrs math, 4 English, 3 lab science (bio, chem, physics), 2 social science. SAT/ACT optional.",
      "studentGrades": "A*A*A*A* predicted (Maths, Further Maths, Physics, Chemistry)",
      "gradesVsEntryBar": "Not published",
      "englishReq": "IELTS 6.5 (6.0 each); TOEFL iBT 88 (20 each) or 4.5 new scale; Duolingo 110; PTE 59. Waived: SAT EBRW 500+/ACT Eng 21+",
      "annualTuition": "USD 59,772",
      "totalTuition": "USD 239,088",
      "estLivingPerYear": "USD 24,720",
      "durationYears": 4,
      "approxTotalMyr": 1365391,
      "scholarshipAndPortal": "Merit scholarship (every applicant); FIRST/VEX USD 10,000/yr (Feb 1); Competition Teams USD 1,000-2,500/yr (Apr 1, 2026-27 award). Intl eligibility not stated. rose-hulman.edu portal.",
      "scholarshipCoverage": "Merit: amount unpublished. FIRST/VEX USD 10,000/yr; Competition Teams USD 1,000-2,500/yr. Intl eligibility not stated.",
      "scholarshipCompetitiveness": "No award-rate statistics published. Intl students fund USD 45,000/yr on average; full-tuition awards 'extremely limited'; cannot meet full need.",
      "howToGetScholarship": "1) Apply by Early Action Nov 1 or Regular Feb 1; merit is offered to every applicant. 2) If admitted: FIRST/VEX form by Feb 1; Competition Teams interest form by Apr 1.",
      "moneyToShowVisa": "Affidavit of support + bank statement (under 6 months old) for the school's cost of attendance less aid",
      "workRightsAfterGraduating": "12 months work after graduating, plus 24 more: mechanical engineering is on the US STEM degree list (CIP 14.1901). Intl placement not published.",
      "recognisedInMalaysia": "ME is ABET-accredited. ABET is a Washington Accord signatory, the accord behind BEM recognition.",
      "howToApply": "Common App or GoRose App (Rose-Hulman's own form)",
      "keyDeadline": "2027-02-01 (Regular Decision; Early Action 2026-11-01, non-binding)",
      "intake": "Fall 2027",
      "notes": "Robotics is a 7-course minor on the ME degree, not a degree. Annual tuition is the combined tuition-and-fees line. Intl students also pay USD 1,191/yr health insurance, not in cost columns.",
      "courseUrl": "https://www.rose-hulman.edu/academics/academic-departments/mechanical-engineering/index.html",
      "infoSource": "Official page",
      "applicationRequirements": "1 recommendation letter",
      "checkedOn": "2026-10-30",
      "admitRate": "80.9% of all applicants admitted, 2025-26",
      "applyLink": "https://www.rose-hulman.edu/admissions-and-aid/the-application-process/application-and-deadlines/apply.html",
      "scholarshipLink": "https://www.rose-hulman.edu/admissions-and-aid/financial-aid/scholarships-and-grants/rose-hulman-scholarships/index.html"
    },
    {
      "id": "northeastern",
      "shortName": "Northeastern",
      "listStatus": "Longlist",
      "desirability": 83,
      "tier": "A",
      "admissionLikelihood": "Reach (very selective)",
      "warnings": "None",
      "university": "Northeastern University",
      "course": "Mechanical Engineering, BSME (Boston) with Robotics Minor (co-op)",
      "courseAtAGlance": "BSME takes 4 yrs with 2 six-month co-ops, or 5 yrs with 3; the Robotics minor (5 courses: ME, EECE, CS) is run by the ECE dept and added on top.",
      "country": "USA",
      "city": "Boston, Massachusetts",
      "studentLife": "Urban Boston campus; in 2022 the NURobotics club had 470 members building eight robots, called one of the largest engineering clubs on campus.",
      "subjectRank": "251-300",
      "overallRank": "=385",
      "entryRequirements": "Holistic; no minimum grades published. SAT/ACT test-optional. Needs physics, chemistry, precalculus. A-Level predicted grades accepted; final results required.",
      "studentGrades": "A*A*A*A* predicted (Maths, Further Maths, Physics, Chemistry)",
      "gradesVsEntryBar": "Not published",
      "englishReq": "No minimum; IELTS, TOEFL iBT, DET or PTE (admits' IELTS 7.5-8.0). Waiver: 4 straight yrs English-medium schooling.",
      "annualTuition": "USD 71,050",
      "totalTuition": "USD 284,200",
      "estLivingPerYear": "USD 27,272",
      "durationYears": 4,
      "approxTotalMyr": 1588884,
      "scholarshipAndPortal": "Merit scholarships (amount varies); Stamps Scholars via John Martinson Honors (invite). No need-based aid for internationals. The admission application is the scholarship application.",
      "scholarshipCoverage": "Merit scholarships vary in amount and do not cover the full cost of attendance (USD 98,322/yr)",
      "scholarshipCompetitiveness": "No statistics published; described as very competitive. Admission is need-aware for internationals.",
      "howToGetScholarship": "(1) Apply by 2027-01-01 (Regular Decision) via Common App or Coalition; (2) submit the Declaration and Certification of Finances; (3) no separate form: merit is decided with admission.",
      "moneyToShowVisa": "Funds for one full academic year (tuition, housing, food, personal); DCF form at application, then proof via myOGS",
      "workRightsAfterGraduating": "Post-study work permit 12 months + 24-month science extension (36 total); BSME code 14.1901 is on the US STEM list. Co-op needs school work authorization.",
      "recognisedInMalaysia": "BS Mechanical Eng is ABET-accredited (Northeastern page) -> Washington Accord -> BEM route. eSISRAF lists the Boston BS; BEM status not checked.",
      "howToApply": "Common App or Coalition Application",
      "keyDeadline": "2027-01-01 (Regular Decision; Early Action 2026-11-01; Early Decision I 2026-11-01, Early Decision II 2027-01-01)",
      "intake": "Fall 2027",
      "notes": "Co-op is optional, but 90%+ of Mechanical & Industrial Eng undergrads do one. Job offers after co-op are shown in dept student stories; no conversion rate is published.",
      "courseUrl": "https://catalog.northeastern.edu/undergraduate/engineering/mechanical-industrial/bsme/",
      "infoSource": "Official page",
      "applicationRequirements": "2 recommendation letters",
      "checkedOn": "2026-10-30",
      "admitRate": "5.6% of all applicants admitted, 2025-26",
      "applyLink": "https://admissions.northeastern.edu/application-information/how-to-apply/",
      "scholarshipLink": "https://admissions.northeastern.edu/cost-financial-aid/merit-scholarships/"
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
      "courseAtAGlance": "3-yr BSc then a 2-yr master's (the Melbourne Model), 5 years in total for the accredited qualification.",
      "country": "Australia",
      "city": "Melbourne, VIC",
      "studentLife": "Lively Parkville campus beside inner-city Melbourne; cultural and walkable rather than outdoorsy.",
      "subjectRank": "45",
      "overallRank": "=22",
      "entryRequirements": "A-levels incl Maths for BSc entry; Master needs BSc (Mechatronics Systems) grade average >=65%",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Above",
      "englishReq": "IELTS 6.5 (6.0)",
      "annualTuition": "AUD 66,752",
      "totalTuition": "AUD 333,760",
      "estLivingPerYear": "AUD 29,710",
      "durationYears": 5,
      "approxTotalMyr": 1403522,
      "scholarshipAndPortal": "Melbourne International Excellence Scholarship (Undergraduate): considered automatically when you apply for the BSc.",
      "scholarshipCoverage": "20% of BSc tuition fees, for the whole BSc (2027 entry onwards).",
      "scholarshipCompetitiveness": "At least 140 awards; given to the highest course entry scores.",
      "howToGetScholarship": "No separate application: apply for the BSc. Outcome within 5 working days of a course offer; unsuccessful applicants are not told.",
      "moneyToShowVisa": "Student visa (subclass 500): AUD 29,710 living costs for 12 months, plus tuition fees",
      "workRightsAfterGraduating": "post-study work visa; master's = longer PSW eligibility; strong AUD",
      "recognisedInMalaysia": "Engineers Australia-accredited via the Master of Mechatronics Engineering (Washington Accord)",
      "howToApply": "Direct online application to the University (not VTAC)",
      "keyDeadline": "2027-05-31",
      "intake": "2027 (Jul/S2 realistic; Feb/S1 2027 too early for A2 results)",
      "notes": "Melbourne Model: 3-yr BSc major + 2-yr Master needed for Engineers Australia accreditation (5 yrs total); a BSc grade average of 65% guarantees an international fee place in the Master.",
      "courseUrl": "https://study.unimelb.edu.au/find/courses/graduate/master-of-mechatronics-engineering/",
      "infoSource": "Official page",
      "applicationRequirements": "Not published",
      "checkedOn": "2026-10-30",
      "admitRate": "Not published",
      "applyLink": "https://study.unimelb.edu.au/how-to-apply/your-online-application",
      "scholarshipLink": "https://scholarships.unimelb.edu.au/awards/melbourne-international-excellence-scholarship-undergraduate"
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
      "subjectRank": "=68",
      "overallRank": "55",
      "entryRequirements": "Holistic review; 4 yrs maths (calculus encouraged), 1 yr each chemistry, physics, biology; essays; SAT, ACT or equivalent scores",
      "studentGrades": "A*A*A*A* predicted",
      "gradesVsEntryBar": "Not published",
      "englishReq": "IELTS 7.5 overall; TOEFL iBT 5 overall (exams from 21 Jan 2026; 102 for earlier exams); Duolingo 135",
      "annualTuition": "USD 69,702",
      "totalTuition": "USD 278,808",
      "estLivingPerYear": "USD 19,650",
      "durationYears": 4,
      "approxTotalMyr": 1443928,
      "scholarshipAndPortal": "No CMU institutional aid for international undergraduates; only DACA students and a small number from specific countries qualify (CMU Student Financial Services)",
      "scholarshipCoverage": "None realistically available — no need-based or merit aid for international undergraduates. External sponsors only.",
      "scholarshipCompetitiveness": "N/A — there is no CMU aid to compete for as an international undergrad.",
      "howToGetScholarship": "No CMU route. Funding comes from external Malaysian sponsors (JPA, MARA, Yayasan) or private scholarships, applied for separately. Full cost of attendance is USD 93,614 a year (2026-27).",
      "moneyToShowVisa": "No fixed US minimum; CMU's cost of attendance sets the student visa form figure: USD 93,614 (2026-27)",
      "workRightsAfterGraduating": "12 months post-study work after graduating, plus a 24-month science post-study work extension for a science degree = up to 3 yrs.",
      "recognisedInMalaysia": "ABET-accredited BS Mechanical Engineering; USA is a Washington Accord signatory, the route to Board of Engineers Malaysia registration. MQA: mqa.gov.my.",
      "howToApply": "Common App",
      "keyDeadline": "2027-01-04",
      "intake": "2027 Sept",
      "notes": "Robotics Minor needs 2.5 QPA, max 2 courses double-counted with ME major; CMU founded the field's first Robotics Institute (1979).",
      "courseUrl": "https://www.meche.cmu.edu/",
      "infoSource": "Official page",
      "applicationRequirements": "Essay · 3 supplemental essays · 2 recommendation letters · Test: SAT, ACT, IB, AP or A-Level",
      "checkedOn": "2026-10-30",
      "admitRate": "11.1% of all applicants admitted, 2025-26",
      "applyLink": "https://www.commonapp.org/",
      "scholarshipLink": "https://www.cmu.edu/sfs/financial-aid/international/index.html"
    }
  ];

  /* ---- GENERATED from business/product_report/university_report.md, "What is inside a report". ---- */

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
    { title: 'Getting in', keys: ['entryRequirements', 'studentGrades', 'englishReq', 'applicationRequirements', 'admitRate', 'howToApply', 'applyLink', 'keyDeadline'] },
    { title: 'What it costs', keys: ['annualTuition', 'totalTuition', 'estLivingPerYear', 'durationYears', 'moneyToShowVisa'] },
    { title: 'Scholarships', keys: ['scholarshipAndPortal', 'scholarshipCoverage', 'scholarshipCompetitiveness', 'howToGetScholarship', 'scholarshipLink'] },
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

  const top5 = ['mit', 'cambridge', 'nus', 'ntu', 'unsw'];

  const total = ROWS.length;
  const clearing = ROWS.filter((u) => /above|meets/i.test(u.gradesVsEntryBar)).length;
  // "Not published" = no grade bar to clear (the US rows), so it counts as neither pass nor fail.
  const noBar = ROWS.filter((u) => u.gradesVsEntryBar === 'Not published').length;
  const withBar = total - noBar;
  const reachCount = ROWS.filter((u) => u.band === 'reach').length;
  const byCost = ROWS.slice().sort((a, b) => a.approxTotalMyr - b.approxTotalMyr);
  const cheapest = byCost[0];
  const dearest = byCost[byCost.length - 1];
  const needBlind = ROWS.filter((u) => u.listStatus !== 'Rejected' &&
    /need[- ]blind/i.test(u.scholarshipAndPortal + ' ' + u.scholarshipCoverage + ' ' + u.scholarshipCompetitiveness));
  const cut = ROWS.filter((u) => u.listStatus === 'Rejected');
  const unverified = ROWS.filter((u) => !u.verified);

  const findings = [
    `Your grades clear the entry bar at ${clearing === withBar ? 'all ' + withBar : clearing + ' of ' + withBar} universities that publish one` +
      `${noBar ? `; the other ${noBar} set no grade bar at all` : ''}. ` +
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
    pages: 25,
    questions: ['Can I get in?', 'Will I belong there and do well?', 'What will applying demand of me?'],
    summary: [
      { label: 'University', value: mit.university },
      { label: 'Course', value: mit.course },
      { label: 'Location', value: mit.country + ' / ' + mit.city },
      { label: 'Overall rank', value: 'QS #1 in the world, 2026-27 (fifteenth consecutive year); #1 for engineering' },
      { label: 'How to apply', value: 'MIT\'s own application portal, not the Common App; non-binding Early Action or Regular Action' },
      { label: 'Admission likelihood', value: 'Reach — 4.6% overall, 2.0% for international applicants' },
      { label: 'Full price, whole degree', value: rm(mit.approxTotalMyr) },
      { label: 'Est. net cost after aid', value: `~${rm(NET_COST_PER_YEAR)}/yr your share (~${rm(NET_COST_TOTAL)} over four years); parent contribution likely RM 0` },
      { label: 'Your priorities', value: priorities.map((p, i) => (i + 1) + '. ' + p).join(' · ') }
    ],
    sections: REPORT_SECTIONS,
    openSection: (REPORT_SECTIONS.find((s) => /why here/i.test(s.title)) || { n: null }).n,
    whyHere: [
      { theme: 'Scholarship — your top priority',
        text: 'The best answer on your entire list, and not close. Need-blind for internationals, meets 100% of need with grants and no loans, a likely-zero parent contribution at your family\'s income.' },
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
    list: { href: '../business/sales/sample_pack/sample_list.pdf', label: 'Download the list' },
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
