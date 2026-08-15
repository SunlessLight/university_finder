"""
apply_glossary.py — plain-English glossary of admissions jargon + the logic that
renders a "Key terms" section and auto-links jargon in an application-prep guide.

The apply-prep guides (build_application_prep.py) are dense with shorthand a
Malaysian 18-year-old hasn't met yet — RD, ED, SCEA, REA, need-blind, CSS Profile,
IDOC, ESAT, CSCA… This module is the single source of truth for what those mean and
how they get surfaced:

- build_glossary_section(text) → a "Key terms" markdown block listing ONLY the terms
  that actually appear in the guide (each with an explicit <a id> anchor to jump to).
- link_terms(text) → wraps the FIRST occurrence per section of each present term with
  a markdown link to its glossary anchor, so the student can tap any term to see what
  it means. First-occurrence-per-section (not every occurrence) keeps it from getting
  noisy, and it skips headings, code, URLs, and existing links so nothing breaks.

Reused by build_application_prep.py (and any future guide tool). Pure stdlib.
"""

import re

# --------------------------------------------------------------------------- #
# The glossary. canonical term -> definition + optional extra surface forms.
# `present_terms` filters this down to what a given guide actually uses, so extra
# entries here are free — they only render when the guide mentions them.
# Definitions are one plain-English line, written to the student ("you").
# --------------------------------------------------------------------------- #
GLOSSARY = {
    # --- Early-application types (the ones the student called out) ------------
    "ED": {
        "aliases": ["Early Decision"],
        "definition": "**Early Decision** — apply early and, if admitted, you are *bound* to enrol "
                      "and withdraw your other applications. Avoid it if you need to compare aid offers.",
    },
    "EA": {
        "aliases": ["Early Action"],
        "definition": "**Early Action** — apply early for an earlier decision; *non-binding*, so you "
                      "stay free to compare offers and decline.",
    },
    "RD": {
        "aliases": ["Regular Decision"],
        "definition": "**Regular Decision** — the standard round with the normal (later) deadline; "
                      "non-binding.",
    },
    "SCEA": {
        "aliases": ["Single-Choice Early Action"],
        "definition": "**Single-Choice Early Action** — a restrictive early option: non-binding, but "
                      "you may not apply early to most *other* private universities at the same time.",
    },
    "REA": {
        "aliases": ["Restrictive Early Action"],
        "definition": "**Restrictive Early Action** — like SCEA: non-binding early action that bars "
                      "you from applying early to other private schools.",
    },
    # --- Financial aid --------------------------------------------------------
    # NOTE: no "need" alias on demonstrated need / no "cost" alias on cost of attendance —
    # surface matching is case-insensitive and word-boundary only, so a bare common word
    # would link every innocent "you need to..." in the guide.
    "cost of attendance": {
        "aliases": ["COA"],
        "definition": "The university's official all-in yearly price — tuition **plus** housing, food, "
                      "fees, books and personal expenses. This is the number financial aid is measured "
                      "against, not the tuition figure alone.",
    },
    "demonstrated need": {
        "aliases": ["financial need"],
        "definition": "Your cost of attendance minus what the university calculates your family can "
                      "pay. \"Meets 100% of need\" means it covers that gap — it does not automatically "
                      "mean you pay nothing, so check what's left for you.",
    },
    "student contribution": {
        "aliases": ["summer work expectation"],
        "definition": "The amount a US aid package expects *you* (not your parents) to contribute each "
                      "year, usually from summer or term-time campus work. It is part of the package, "
                      "so it is not covered by the grant.",
    },
    "need-blind": {
        "aliases": [],
        "definition": "The university decides admission *without* looking at whether you asked for "
                      "financial aid — requesting aid can't hurt your chances.",
    },
    "need-aware": {
        "aliases": ["need-sensitive"],
        "definition": "Your ability to pay *can* factor into the admission decision — you still request "
                      "aid, but it is a consideration.",
    },
    "CSS Profile": {
        "aliases": ["CSS"],
        "definition": "The College Board's detailed financial-aid application most US universities use "
                      "to assess your need (separate from the FAFSA). Opens 1 October.",
    },
    "IDOC": {
        "aliases": [],
        "definition": "College Board's Institutional Documentation Service — where you upload your "
                      "parents' tax/income documents for financial aid.",
    },
    "PFAA": {
        "aliases": ["Princeton Financial Aid Application"],
        "definition": "**Princeton Financial Aid Application** — Princeton's own aid form, filed "
                      "alongside the CSS Profile.",
    },
    "ISAFA": {
        "aliases": ["International Student Financial Aid Application"],
        "definition": "**International Student Financial Aid Application** — Stanford's alternative aid "
                      "form if you can't pay the CSS Profile fee.",
    },
    "fee waiver": {
        "aliases": [],
        "definition": "A request to cancel the application fee on the grounds of financial need — so "
                      "you pay nothing to apply.",
    },
    # --- Application mechanics ------------------------------------------------
    "Common App": {
        "aliases": ["Common Application"],
        "definition": "The Common Application — one online form plus one main essay you reuse across "
                      "many US universities.",
    },
    "self-report": {
        "aliases": ["self-reported", "self-reporting"],
        "definition": "You type your own test scores into the application; you only pay to send "
                      "official scores once you enrol.",
    },
    "supplement": {
        "aliases": ["supplement essay", "supplements", "supplement essays"],
        "definition": "Extra, school-specific essay(s) on top of the shared Common App essay.",
    },
    "School Report": {
        "aliases": [],
        "definition": "A form (plus a letter) your school counsellor submits about you and your school.",
    },
    "mid-year report": {
        "aliases": [],
        "definition": "An update your school sends partway through the year with your latest grades.",
    },
    "I-20": {
        "aliases": [],
        "definition": "The US immigration form your university issues after you're admitted — you need "
                      "it to apply for a student visa.",
    },
    # --- Tests ----------------------------------------------------------------
    "SAT": {
        "aliases": [],
        "definition": "A standardised US university-entrance exam; many US universities require the "
                      "SAT or the ACT.",
    },
    "ACT": {
        "aliases": [],
        "definition": "A standardised US university-entrance exam; an accepted alternative to the SAT.",
    },
    "IELTS": {
        "aliases": [],
        "definition": "International English Language Testing System — an English-proficiency test. Your "
                      "English-medium A-Levels waive it at many universities, but not all.",
    },
    "TOEFL": {
        "aliases": [],
        "definition": "Test of English as a Foreign Language — an English-proficiency test; an "
                      "alternative to IELTS.",
    },
    "ESAT": {
        "aliases": [],
        "definition": "Engineering and Science Admissions Test — required by Oxford and Imperial "
                      "engineering; register and sit it in autumn.",
    },
    "CSCA": {
        "aliases": [],
        "definition": "China's common standardised admission assessment that international "
                      "undergraduates must sit *before* applying to Chinese universities.",
    },
    "HSK": {
        "aliases": [],
        "definition": "Hanyu Shuiping Kaoshi — the standard Chinese-language proficiency test; higher "
                      "levels (e.g. HSK 5) are needed for Chinese-taught degrees.",
    },
    # --- Scholarships / sponsors ---------------------------------------------
    "CSC": {
        "aliases": ["China Scholarship Council"],
        "definition": "China Scholarship Council scholarship — the main full-ride government "
                      "scholarship for international students in China.",
    },
    "MOE Tuition Grant": {
        "aliases": [],
        "definition": "Singapore's Ministry of Education subsidy that cuts tuition sharply in exchange "
                      "for a 3-year work bond after graduation.",
    },
    "JPA": {
        "aliases": ["JPA-MARA", "PKJM"],
        "definition": "Malaysian government overseas-study sponsorship (JPA / MARA, via the PKJM "
                      "programme) — a route to full funding for eligible students.",
    },
    "Yayasan Khazanah": {
        "aliases": [],
        "definition": "A Malaysian foundation offering competitive scholarships to study at top global "
                      "universities.",
    },
    "UAC": {
        "aliases": [],
        "definition": "Universities Admissions Centre — the shared applications hub for Australian "
                      "Year-12 students; international applicants usually apply to each university "
                      "directly instead.",
    },
    # --- Recognition, outcomes & academic structure (report terms) ------------
    # These surface mostly in the reports (build_report.py) rather than the apply
    # guides — recognition-back-home, post-study work, and department shorthand.
    "OPT": {
        "aliases": ["Optional Practical Training"],
        # "OPT" is also the English verb, and it is matched case-sensitively, so a cell
        # that shouts "you must OPT IN on the application" looked like the visa acronym
        # and was rewritten to "you must post-study work permit IN". Excluded by context.
        "not_followed_by": r"\s+(?:in|out)\b",
        "definition": "**Optional Practical Training** — US work permission that lets you work in "
                      "your field for up to 12 months after graduating on a student visa.",
    },
    "STEM OPT": {
        "aliases": ["STEM-OPT", "STEM extension", "STEM OPT extension"],
        "definition": "**STEM OPT extension** — a 24-month extension of OPT for science/engineering "
                      "degrees, giving up to 36 months of US work authorisation after you graduate.",
    },
    "ABET": {
        "aliases": [],
        "definition": "The US accreditation board for engineering and technology degrees. An "
                      "ABET-accredited degree is recognised internationally and eases professional "
                      "registration back home.",
    },
    "Washington Accord": {
        "aliases": [],
        "definition": "An international agreement that mutually recognises engineering degrees "
                      "between member countries (the US, UK, Australia and Malaysia all belong), so "
                      "an accredited degree carries over.",
    },
    "BEM": {
        "aliases": ["Board of Engineers Malaysia"],
        "definition": "**Board of Engineers Malaysia** — the body you register with to practise as "
                      "an engineer in Malaysia; it recognises accredited degrees via the Washington "
                      "Accord.",
    },
    "MQA": {
        "aliases": ["Malaysian Qualifications Agency"],
        "definition": "**Malaysian Qualifications Agency** — the Malaysian body that recognises "
                      "foreign qualifications; check its register to confirm your degree counts back "
                      "home.",
    },
    "Common Data Set": {
        "aliases": ["CDS"],
        "definition": "A standardised set of admissions and enrolment statistics each US university "
                      "publishes — the reliable place to check real admit rates and what admitted "
                      "students look like.",
    },
    "land-grant": {
        "aliases": [],
        "definition": "A US university originally funded by federal land grants to teach practical "
                      "fields like agriculture and engineering alongside the liberal arts.",
    },
    "MAE": {
        "aliases": [],
        "definition": "Mechanical & Aerospace Engineering — a common name for the university "
                      "department or school that houses mechanical engineering degrees.",
    },
    "ECE": {
        "aliases": [],
        "definition": "Electrical & Computer Engineering — a common name for the university "
                      "department covering electrical engineering and computer hardware.",
    },
    # --- Malaysian sponsors + US campus shorthand (report terms) --------------
    "MARA": {
        "aliases": ["Majlis Amanah Rakyat"],
        "definition": "**Majlis Amanah Rakyat** — a Malaysian government agency that sponsors and "
                      "lends to Bumiputera students for pre-university and degree study, locally "
                      "and abroad.",
    },
    "PKJM": {
        "aliases": ["Program Khas JPA-MARA", "Program Khas JPA MARA"],
        "definition": "**Program Khas JPA-MARA** — a joint JPA and MARA sponsorship that takes "
                      "high-scoring Bumiputera SPM leavers through a preparatory year and then a "
                      "first degree overseas, including in the US.",
    },
    "CPT": {
        "aliases": ["Curricular Practical Training"],
        "definition": "**Curricular Practical Training** — US work permission that lets you take an "
                      "internship connected to your degree while you are still studying.",
    },
    "PRL": {
        "aliases": ["Product Realization Lab"],
        "definition": "**Product Realization Lab** — Stanford's student machine shop and makerspace, "
                      "covering welding, machining, woodworking and rapid prototyping.",
    },
    "SAIL": {
        "aliases": ["Stanford Artificial Intelligence Laboratory"],
        "definition": "**Stanford Artificial Intelligence Laboratory** — Stanford's long-running AI "
                      "and robotics research lab, founded in 1962.",
    },
    "BOSP": {
        "aliases": ["Bing Overseas Studies Program"],
        "definition": "**Bing Overseas Studies Program** — Stanford's own study-abroad system, where "
                      "credit transfers automatically and roughly half of each class takes part.",
    },
    "VPUE": {
        "aliases": ["Vice Provost for Undergraduate Education"],
        "definition": "**Vice Provost for Undergraduate Education** — the Stanford office that funds "
                      "undergraduate research through named student grants.",
    },
    "coterm": {
        "aliases": ["coterminal", "coterminal degree"],
        "definition": "**Coterminal degree** — Stanford's route to take a master's alongside your "
                      "bachelor's, usually finishing both in about five years.",
    },
    "CALS": {
        "aliases": ["College of Agriculture and Life Sciences"],
        "definition": "**College of Agriculture and Life Sciences** — one of Cornell's eight "
                      "admitting undergraduate colleges, and a New York State contract college, so "
                      "New York residents pay a lower tuition rate there than at the endowed colleges.",
    },
    "ORIE": {
        "aliases": ["Operations Research and Information Engineering"],
        "definition": "**Operations Research and Information Engineering** — Cornell's engineering "
                      "school for optimisation, probability and financial engineering; a well-known "
                      "feeder into quantitative trading and analytics roles.",
    },
    "CIP code": {
        "aliases": ["CIP"],
        "definition": "**Classification of Instructional Programs code** — the US government's "
                      "subject code printed on your I-20. Whether yours is on the STEM list is what "
                      "decides if you get the 24-month STEM OPT extension.",
    },
    "S/NC": {
        "aliases": ["Satisfactory/No Credit", "SNC"],
        "definition": "**Satisfactory/No Credit** — Brown's alternative to a letter grade. You either "
                      "pass the course or it leaves no trace on your external transcript; there is no "
                      "D and no F anywhere in Brown's system.",
    },
    "UTRA": {
        "aliases": ["Undergraduate Teaching and Research Award", "Undergraduate Teaching and Research Awards"],
        "definition": "**Undergraduate Teaching and Research Award** — Brown's paid scheme for working "
                      "on a faculty research or teaching project, over the summer or during a semester.",
    },
    "PLME": {
        "aliases": ["Program in Liberal Medical Education"],
        "definition": "**Program in Liberal Medical Education** — Brown's eight-year combined "
                      "undergraduate and medical degree, applied for at the same time as the main "
                      "application and admitted separately.",
    },
    "BRDD": {
        "aliases": ["Brown|RISD Dual Degree", "Brown-RISD Dual Degree"],
        "definition": "**Brown|RISD Dual Degree** — a five-year programme run jointly with the Rhode "
                      "Island School of Design next door, ending in two degrees, one from each school.",
    },
    "SHIP": {
        "aliases": ["Student Health Insurance Plan"],
        "definition": "**Student Health Insurance Plan** — the university's own health cover, billed "
                      "automatically each year unless you prove you have comparable insurance and get "
                      "a waiver approved.",
    },
    # --- UK terms (report terms) ----------------------------------------------
    "RSS": {
        "aliases": ["Royal Statistical Society"],
        "definition": "**Royal Statistical Society** — the UK professional body for statisticians. It "
                      "accredits degrees, and an accredited degree is the fast route to its "
                      "GradStat professional grade.",
    },
    "GradStat": {
        "aliases": ["Graduate Statistician"],
        "definition": "**Graduate Statistician** — the Royal Statistical Society's entry professional "
                      "grade, awarded automatically to graduates of an accredited degree with a "
                      "2:1 or better, and the first step towards Chartered Statistician.",
    },
    "CStat": {
        "aliases": ["Chartered Statistician"],
        "definition": "**Chartered Statistician** — the Royal Statistical Society's full professional "
                      "grade, earned after several years of practice on top of GradStat.",
    },
    "IHS": {
        "aliases": ["Immigration Health Surcharge", "immigration health surcharge"],
        "definition": "**Immigration Health Surcharge** — a compulsory up-front UK fee, paid per year of "
                      "your visa, that buys access to the National Health Service while you study.",
    },
    "CAS": {
        "aliases": ["Confirmation of Acceptance for Studies"],
        "definition": "**Confirmation of Acceptance for Studies** — the electronic reference number your "
                      "UK university issues once you accept an unconditional place. You cannot apply "
                      "for a Student visa without it.",
    },
    "IGCSE": {
        "aliases": [],
        "definition": "**International General Certificate of Secondary Education** — the international "
                      "version of the UK's GCSE, sat at around age 16. UK universities often set a "
                      "minimum GCSE or IGCSE grade in English and Maths on top of A-Level grades.",
    },
    "NSS": {
        "aliases": ["National Student Survey"],
        "definition": "**National Student Survey** — the UK-wide survey of final-year undergraduates. "
                      "Its course-level satisfaction scores are published on Discover Uni.",
    },
    "Discover Uni": {
        "aliases": [],
        "definition": "The UK government's official course-comparison site, carrying verified "
                      "satisfaction, continuation and graduate-earnings data per course.",
    },
    "PTPTN": {
        "aliases": [],
        "definition": "**Perbadanan Tabung Pendidikan Tinggi Nasional** — Malaysia's national education "
                      "*loan* fund, not a scholarship. It is aimed at study at approved institutions and "
                      "is repayable.",
    },
    "Kijang Scholarship": {
        "aliases": ["Kijang", "BNM Kijang"],
        "definition": "Bank Negara Malaysia's scholarship for high-scoring Malaysians to study abroad in "
                      "finance-adjacent fields, including data science; it carries a service bond of two "
                      "years for each sponsored year.",
    },
    "UPC": {
        "aliases": ["Undergraduate Preparatory Certificate"],
        "definition": "**Undergraduate Preparatory Certificate** — UCL's own international foundation "
                      "year, for students whose school qualification UCL does not accept for direct "
                      "entry. A-Levels are accepted, so it is not a route for A-Level students.",
    },
    "SEVIS": {
        "aliases": ["Student and Exchange Visitor Information System"],
        "definition": "**Student and Exchange Visitor Information System** — the US government database "
                      "that tracks student-visa holders. Every applicant pays a one-off I-901 SEVIS fee "
                      "before the visa interview.",
    },
    "UROP": {
        "aliases": ["Undergraduate Research Opportunities Program"],
        "definition": "**Undergraduate Research Opportunities Program** — MIT's system for pairing "
                      "undergraduates with faculty research projects, for pay, for credit or as a "
                      "volunteer, from first year onwards.",
    },
    "GIRs": {
        "aliases": ["GIR", "General Institute Requirements"],
        "definition": "**General Institute Requirements** — the core every MIT undergraduate takes "
                      "whatever the major: maths, physics, chemistry, biology, a lab, plus eight "
                      "humanities, arts and social science subjects.",
    },
    "HASS": {
        "aliases": [],
        "definition": "**Humanities, Arts and Social Sciences** — MIT's breadth requirement, eight "
                      "subjects outside science and engineering, two of them writing-intensive.",
    },
    "IAP": {
        "aliases": ["Independent Activities Period"],
        "definition": "**Independent Activities Period** — the four weeks each January when MIT "
                      "suspends normal classes for projects, short courses, competitions, internships "
                      "and travel. No extra tuition for students enrolled in the surrounding terms.",
    },
    "MSA": {
        "aliases": ["Muslim Students Association"],
        "definition": "**Muslim Students Association** — the student-run Muslim society found on most "
                      "US campuses, usually running the prayer room, Jumu'ah and Ramadan meals.",
    },
    "musalla": {
        "aliases": ["musallah"],
        "definition": "A dedicated Muslim prayer room, typically with washing facilities for wudu.",
    },
    "Pass/No Record": {
        "aliases": ["P/NR"],
        "definition": "**Pass/No Record** — MIT's first-semester grading shield: a passing grade shows "
                      "only as 'P' on your transcript and a failing one is not recorded at all, so you "
                      "can take hard classes while you find your feet.",
    },
    "MBTA": {
        "aliases": ["the T"],
        "definition": "**Massachusetts Bay Transportation Authority** — greater Boston's public "
                      "transport network, known locally as 'the T'; its Red Line subway stops on "
                      "MIT's campus at Kendall/MIT.",
    },
    "E-Verify": {
        "aliases": [],
        "definition": "The US government system employers use to confirm a hire may legally work. "
                      "Only an E-Verify employer can sponsor the 24-month STEM OPT extension.",
    },
    # --- Naval architecture / marine engineering + UK routes (report terms) ---
    "RINA": {
        "aliases": ["Royal Institution of Naval Architects"],
        "definition": "**Royal Institution of Naval Architects** — the UK professional body for "
                      "naval architects; a RINA-accredited degree counts toward Chartered/Incorporated "
                      "Engineer status.",
    },
    "IMarEST": {
        "aliases": ["Institute of Marine Engineering, Science and Technology"],
        "definition": "**Institute of Marine Engineering, Science & Technology** — the UK professional "
                      "body for marine engineers; accredits degrees toward Chartered/Incorporated "
                      "Engineer status.",
    },
    "CEng": {
        "aliases": ["Chartered Engineer"],
        "definition": "**Chartered Engineer** — the UK's full professional-engineer status; it usually "
                      "needs an accredited MEng (or a BEng plus further learning) and maps to the "
                      "Washington Accord, so it's the route Malaysia's BEM recognises for Ir. registration.",
    },
    "IEng": {
        "aliases": ["Incorporated Engineer"],
        "definition": "**Incorporated Engineer** — a UK professional grade below Chartered. A BEng on "
                      "its own typically meets IEng, which maps to the Sydney Accord — a lower tier than "
                      "the Washington Accord chartered route.",
    },
    "Sydney Accord": {
        "aliases": [],
        "definition": "An international agreement recognising engineering-technologist / Incorporated-"
                      "Engineer qualifications between member countries — a separate, lower tier than the "
                      "Washington Accord for chartered engineers.",
    },
    "EAC": {
        "aliases": ["Engineering Accreditation Council"],
        "definition": "**Engineering Accreditation Council** — the Malaysian body that accredits "
                      "engineering degrees for the Washington Accord and for BEM Professional Engineer "
                      "(Ir.) registration.",
    },
    "UCAS": {
        "aliases": [],
        "definition": "The UK's central undergraduate application service — one form to apply to up to "
                      "five UK universities, with a mid-January equal-consideration deadline.",
    },
    "Graduate Route": {
        "aliases": [],
        "definition": "The UK's post-study work visa — lets graduates stay and work after their degree "
                      "(18 months for bachelor's/master's applying from 1 January 2027).",
    },
    "NAOME": {
        "aliases": [],
        "definition": "Naval Architecture, Ocean & Marine Engineering — the name of Strathclyde's "
                      "department for these degrees.",
    },
    # --- Master-list terms: Malaysian recognition ladder ----------------------
    # These surface in the master list's "Recognised in Malaysia?" column. The two
    # accreditation ladders (EAC/BEM/Washington vs ETAC/MBOT/Sydney) are NOT
    # interchangeable — see the table in workflows/03_discover_longlist.md.
    "ETAC": {
        "aliases": ["Engineering Technology Accreditation Council"],
        "definition": "**Engineering Technology Accreditation Council** — the Malaysian body that "
                      "accredits *engineering technology* degrees. A separate, lower ladder than EAC: "
                      "it leads to MBOT, not to BEM Professional Engineer registration.",
    },
    "MBOT": {
        "aliases": ["Malaysia Board of Technologists"],
        "definition": "**Malaysia Board of Technologists** — the register for Professional Technologists "
                      "(Ts.), the counterpart to BEM's engineer register (Ir.).",
    },
    "Ir.": {
        "aliases": [],
        "definition": "The title of a **Professional Engineer** registered with BEM — the qualification "
                      "you need to sign off engineering work in Malaysia.",
    },
    "Ts.": {
        "aliases": [],
        "definition": "The title of a **Professional Technologist** registered with MBOT — a separate "
                      "(and, for regulated engineering roles, lower) status than Ir.",
    },
    "MQR": {
        "aliases": ["Malaysian Qualifications Register"],
        "definition": "**Malaysian Qualifications Register** — the public list of MQA-recognised "
                      "programmes, showing the professional body and the accreditation dates. Check the "
                      "end date: an entry can be expired on its face.",
    },
    "PLO": {
        "aliases": ["Programme Learning Outcomes"],
        "definition": "**Programme Learning Outcomes** — what a degree promises you'll be able to do on "
                      "graduating. The wording gives the accreditation ladder away: \"complex engineering "
                      "problems\" means the Washington Accord, \"broadly-defined\" means the Sydney one.",
    },
    "UPU": {
        "aliases": [],
        "definition": "The central application system for Malaysian public universities — one form, "
                      "used instead of applying to each university directly.",
    },
    "MUET": {
        "aliases": ["Malaysian University English Test"],
        "definition": "**Malaysian University English Test** — the English test Malaysian public "
                      "universities require through UPU, in place of IELTS.",
    },
    "STPM": {
        "aliases": [],
        "definition": "Malaysia's national pre-university qualification (Sijil Tinggi Persekolahan "
                      "Malaysia), the local route into a degree alongside A-Levels.",
    },
    "UEC": {
        "aliases": ["Unified Examination Certificate"],
        "definition": "**Unified Examination Certificate** — the Malaysian independent-Chinese-school "
                      "qualification. Some scholarships are UEC-only, so an A-Level student can't claim them.",
    },
    # --- Master-list terms: destination-specific ------------------------------
    "H-1B": {
        "aliases": [],
        "definition": "The US employer-sponsored work visa most graduates need after their post-study "
                      "work permit runs out. It is allocated by lottery, so it is not guaranteed.",
    },
    "SEVP": {
        "aliases": ["SEVP certification"],
        "definition": "**Student and Exchange Visitor Program** — the US government certification a "
                      "university must hold to enrol international students and issue the I-20.",
    },
    "SEAS": {
        "aliases": [],
        "definition": "Harvard's **John A. Paulson School of Engineering and Applied Sciences** — the "
                      "school that houses every engineering and computer science concentration.",
    },
    "F-1": {
        # "F-1 visa" is listed so the longest-surface-first ordering swallows the trailing
        # noun too; matching bare "F-1" alone turned "F-1 visa" into "student visa visa".
        "aliases": ["F-1 visa", "F-1 student visa"],
        "definition": "The standard US student visa.",
    },
    "OOS": {
        "aliases": ["out-of-state"],
        "definition": "**Out-of-state** — the higher tuition rate a US public university charges students "
                      "from outside its state. International students pay this rate.",
    },
    "ATAR": {
        "aliases": [],
        "definition": "Australian Tertiary Admission Rank — the score Australian universities admit on. "
                      "A-Levels are converted to it, so published cutoffs are arithmetic, not a guess.",
    },
    "WAM": {
        "aliases": ["Weighted Average Mark"],
        "definition": "**Weighted Average Mark** — the Australian grade average, used for honours entry "
                      "and scholarships.",
    },
    "subclass 485": {
        # "485 Temporary Graduate visa" is listed first so the longest-surface-first
        # ordering consumes the bare number too, rather than stranding it.
        "aliases": ["485 Temporary Graduate visa", "Temporary Graduate visa (subclass 485)",
                    "485 visa", "Temporary Graduate visa"],
        "definition": "Australia's post-study work visa — lets you stay and work for a few years after "
                      "graduating. Regional campuses can qualify for an extra year.",
    },
    "IGP": {
        "aliases": ["Indicative Grade Profile"],
        "definition": "**Indicative Grade Profile** — the grade range Singapore universities publish for "
                      "students they admitted last year. It is based on Singapore-Cambridge A-Levels and "
                      "international places are capped, so treat it as indicative, not a cutoff.",
    },
    "COMPASS": {
        "aliases": [],
        "definition": "Singapore's points system for approving an Employment Pass — it scores your "
                      "salary, qualifications and the employer's hiring mix.",
    },
    "Employment Pass": {
        "aliases": [],
        "definition": "Singapore's work visa for professionals. There is no post-study work visa there, "
                      "so staying on means landing a job above a set salary bar and clearing COMPASS.",
    },
    "EAB": {
        "aliases": ["Engineering Accreditation Board"],
        "definition": "**Engineering Accreditation Board** — Singapore's engineering accreditor. Its "
                      "degrees carry the Washington Accord, so they map onto Malaysia's BEM route.",
    },
    "IES": {
        "aliases": ["Institution of Engineers Singapore"],
        "definition": "**Institution of Engineers, Singapore** — the professional body behind EAB "
                      "accreditation.",
    },
    "IANG": {
        "aliases": ["Immigration Arrangements for Non-local Graduates"],
        "definition": "**Immigration Arrangements for Non-local Graduates** — Hong Kong's post-study work "
                      "route. Graduates get 24 months to stay and work with no job offer needed, then "
                      "renew 2+2+3 years; seven continuous years qualifies for permanent residency.",
    },
    "JUPAS": {
        "aliases": ["Joint University Programmes Admissions System"],
        "definition": "Hong Kong's central admissions system — for local students sitting the HKDSE only. "
                      "A Malaysian A-Level applicant never uses it, so JUPAS entry scores do not apply to "
                      "you; apply through each university's own international route instead.",
    },
    "non-JUPAS": {
        "aliases": ["non-local admission", "non-local student"],
        "definition": "Everyone in Hong Kong who isn't a local HKDSE student. It is the admissions route "
                      "you use — and the tuition rate you pay: non-local fees run four to six times the "
                      "subsidised local rate shown beside them on the same fee page.",
    },
    "G30": {
        "aliases": [],
        "definition": "A Japanese government programme of degrees taught entirely in English — one of "
                      "the few routes in without Japanese-language qualifications.",
    },
    "SGU": {
        "aliases": ["Super Global University"],
        "definition": "**Super Global University** — the Japanese government's successor to G30, funding "
                      "universities to run English-taught degrees.",
    },
    "MEXT": {
        "aliases": [],
        "definition": "Japan's government scholarship — can cover tuition, a monthly living allowance and "
                      "airfare, but it is highly competitive and application-heavy.",
    },
    "JASSO": {
        "aliases": [],
        "definition": "Japan Student Services Organisation — runs smaller monthly stipends for "
                      "international students, separate from MEXT.",
    },
    "JABEE": {
        "aliases": [],
        "definition": "Japan's engineering accreditor. Japan signs the Washington Accord through JABEE, "
                      "but not every Japanese programme is accredited — check the specific degree.",
    },
    "EJU": {
        "aliases": [],
        "definition": "Examination for Japanese University Admission — the entrance exam for "
                      "Japanese-taught degrees. English-taught programmes usually skip it.",
    },
    "JLPT": {
        "aliases": [],
        "definition": "Japanese-Language Proficiency Test — Japanese-taught degrees typically want the "
                      "top levels (N1/N2). It also shapes how employable you are after graduating.",
    },
    "RU11": {
        "aliases": [],
        "definition": "A group of 11 leading Japanese research universities — a rough marker of research "
                      "strength, like Australia's Group of Eight.",
    },
    "Go8": {
        "aliases": ["Group of Eight"],
        "definition": "**Group of Eight** — Australia's eight oldest research-intensive universities; "
                      "the closest thing the country has to an Ivy League label.",
    },
    "Commonwealth Supported Place": {
        "aliases": ["CSP"],
        "definition": "A government-subsidised university place in Australia, open to **domestic students "
                      "only**. Its fee is printed next to the international one — if an Australian annual "
                      "fee looks under about A$25,000, this is the number you are reading.",
    },
    "GES": {
        "aliases": ["Graduate Employment Survey"],
        "definition": "**Graduate Employment Survey** — Singapore's official annual survey of what "
                      "graduates earn and how fast they find work, published per university and degree.",
    },
}


# --------------------------------------------------------------------------- #
# Plain-English alternatives — the master list's readability rule.
#
# A master_list cell has to be readable on its own, WITHOUT the glossary sheet; the
# glossary is a safety net, not a prerequisite. So the rule is not "expand every
# acronym" (that makes cells longer, which is the other complaint) — it is:
#
#   * If a shorter plain phrase says the same thing, use the phrase. Those terms are
#     listed here, and check_master_list.py flags them wherever they appear bare.
#   * If the term is a proper noun the student will have to search for on an official
#     page — UCAS, MQA, BEM, Washington Accord, CSS Profile, MEXT — keep it. Replacing
#     it would leave the student unable to find the thing. The glossary sheet
#     (build_glossary_sheet.py) is what explains those.
#
# Terms absent from this map are the second category: deliberately kept as-is.
# --------------------------------------------------------------------------- #
PLAIN_ALTERNATIVES = {
    # Keep these substitutable in place: they must read correctly when swapped straight
    # into an existing sentence, so no trailing parentheticals and no repeated head nouns
    # ("H-1B lottery" must not become "...work visa (by lottery) lottery").
    "OPT": "post-study work permit",
    "STEM OPT": "science post-study work extension",
    "H-1B": "employer-sponsored work visa",
    "I-20": "student visa form",
    "F-1": "student visa",
    "OOS": "out-of-state",
    "subclass 485": "post-study work visa",
    "ATAR": "Australian entry score",
    "WAM": "grade average",
    "IGP": "published grade profile",
    "COMPASS": "work-pass points test",
    "PLO": "programme learning outcomes",
    "MQR": "the MQA register",
    "EJU": "Japanese university entrance exam",
    "JLPT": "Japanese language test",
    "Commonwealth Supported Place": "subsidised place for domestic students only",
    "GES": "Singapore's graduate employment survey",
}


# --------------------------------------------------------------------------- #
# Surface forms + matching
# --------------------------------------------------------------------------- #
def slug(term):
    """Stable glossary anchor id for a canonical term, e.g. 'CSS Profile' -> 'term-css-profile'."""
    s = re.sub(r"[^a-z0-9]+", "-", term.strip().lower()).strip("-")
    return f"term-{s or 'x'}"


def _is_acronym(surface):
    """Acronyms match case-sensitively; ordinary phrases match case-insensitively.

    Two shapes count as an acronym: all-caps letters/digits/hyphens (ABET, H-1B), and a
    single capitalised token containing a digit (Go8, RU11). The second case matters —
    matched case-insensitively, "Go8" also hits a stray "go8" in running prose, which is
    the false-positive class the module docstring warns about.
    """
    if re.fullmatch(r"[A-Z0-9][A-Z0-9\-]*", surface):
        return True
    return re.fullmatch(r"[A-Z][A-Za-z]*\d[A-Za-z0-9]*", surface) is not None


def _surface_forms():
    """All (surface, canonical, exclusion) triples, longest surface first so 'CSS Profile'
    beats 'CSS' — and so an alias that swallows a trailing noun ('F-1 visa') wins over the
    bare acronym, which would otherwise leave the noun stranded."""
    triples = []
    for term, meta in GLOSSARY.items():
        for surface in [term, *meta.get("aliases", [])]:
            triples.append((surface, term, meta.get("not_followed_by")))
    triples.sort(key=lambda t: len(t[0]), reverse=True)
    return triples


def _pattern_for(surface, not_followed_by=None):
    """Word-boundary regex for a surface form; case-sensitive only for acronyms.

    `not_followed_by` excludes a context where the surface is not really the term — a few
    acronyms collide with ordinary words (OPT / "opt in").
    """
    flags = 0 if _is_acronym(surface) else re.IGNORECASE
    # The guard is always case-insensitive, even when the surface is not: the collision
    # that motivated it was a SHOUTED "OPT IN", so matching only lowercase "in" would
    # miss exactly the case it exists for.
    guard = f"(?!(?i:{not_followed_by}))" if not_followed_by else ""
    return re.compile(rf"(?<![\w-]){re.escape(surface)}(?![\w-]){guard}", flags)


# Precompute once.
_SURFACES = [(s, c) for s, c, _ in _surface_forms()]
_COMPILED = [(s, c, _pattern_for(s, x)) for s, c, x in _surface_forms()]


def present_terms(text):
    """Canonical terms that actually occur in `text`, in GLOSSARY (definition) order."""
    found = set()
    for surface, canonical, pat in _COMPILED:
        if canonical in found:
            continue
        if pat.search(text):
            found.add(canonical)
    return [t for t in GLOSSARY if t in found]


def build_glossary_section(text, title="Key terms"):
    """Markdown 'Key terms' block for only the terms present in `text`. '' if none."""
    terms = present_terms(text)
    if not terms:
        return ""
    lines = [f"## {title}", "",
             "_New to these? Here's what the shorthand in this guide means — "
             "tap a linked term anywhere below to jump back here._", ""]
    for term in terms:
        anchor = slug(term)
        lines.append(f'- <a id="{anchor}"></a>**{term}** — {GLOSSARY[term]["definition"]}')
    return "\n".join(lines)


# Spans we must never rewrite inside: existing markdown links, inline code, bare
# URLs, and raw HTML tags. Everything outside these is "free" text we can link in.
_PROTECTED = re.compile(
    r"(\[[^\]]*\]\([^)]*\)"      # [text](url) markdown links
    r"|`[^`]*`"                  # `inline code`
    r"|https?://\S+"             # bare URLs
    r"|<[^>]+>)"                 # raw HTML tags / anchors
)


def link_terms(text):
    """
    Link the first occurrence *per section* of each glossary term to its anchor.

    "Section" resets at each `##` (level-2) heading only — so within one major
    section (e.g. the whole "Grouped by application system" block with its per-
    university sub-headings) a term links just once, not once per university.
    Never links inside any heading, fenced code block, or protected span
    (links/code/URLs/HTML). A term already inside a link won't be re-linked.
    """
    out = []
    seen = set()          # canonical terms already linked in the current section
    in_fence = False
    for line in text.splitlines():
        stripped = line.lstrip()
        # Fenced code blocks: pass through untouched.
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        # Any heading: never link inside it. A level-1/2 heading also starts a
        # fresh section (deeper ### / #### headings do not reset, to avoid
        # re-linking the same term in every university block).
        heading = re.match(r"(#{1,6})\s", stripped)
        if heading:
            if len(heading.group(1)) <= 2:
                seen = set()
            out.append(line)
            continue
        out.append(_link_line(line, seen))
    return "\n".join(out)


def _link_line(line, seen):
    """Link eligible terms in one line, mutating `seen`. Protects links/code/URLs."""
    parts = _PROTECTED.split(line)
    # split() with one capturing group yields [free, protected, free, protected, ...]
    for i in range(0, len(parts), 2):
        parts[i] = _link_free_segment(parts[i], seen)
    return "".join(parts)


def _link_free_segment(segment, seen):
    """
    Link the first eligible occurrence of each unseen term in one free-text segment.

    Matches are *collected against the original segment* and only then inserted, in a
    single right-to-left pass. Inserting as we scanned used to feed the link we had
    just written back into the search space, so a shorter surface could match inside
    the anchor text of a longer one and nest:

        Single-Choice Early Action -> [Single-Choice [Early Action](#term-ea)](#term-scea)

    python-markdown renders only the outer link and leaks the inner `[...](...)` as
    literal body text. Surfaces arrive longest-first, so keeping the first accepted
    span and dropping any that overlaps it means the longest term wins.
    """
    if not segment.strip():
        return segment

    spans = []          # (start, end, canonical) — non-overlapping, longest-first
    for surface, canonical, pat in _COMPILED:
        if canonical in seen:
            continue
        for m in pat.finditer(segment):
            start, end = m.span()
            if any(start < e and s < end for s, e, _ in spans):
                continue    # overlaps a term already claimed — skip this occurrence
            spans.append((start, end, canonical))
            seen.add(canonical)
            break           # first occurrence only

    for start, end, canonical in sorted(spans, reverse=True):
        anchor = slug(canonical)
        segment = f"{segment[:start]}[{segment[start:end]}](#{anchor}){segment[end:]}"
    return segment
