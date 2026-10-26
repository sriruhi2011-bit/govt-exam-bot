# curriculum_bank.py
"""
High-Yield Curriculum & Topic Bank for UPSC & KPSC (KAS / PSI / PDO) Aspirants.
Contains structured exam-ready themes covering GS-1, GS-2, GS-3, GS-4 and Karnataka Special topics.
Each module includes:
- 360° Issue Dossier (Static + Dynamic + Committees + Recommendations)
- Mains Challenge Question + Structural Blueprint + Keywords
- Comprehensive Model Answer
- 3 UPSC/KPSC standard multi-statement MCQs with trap explanations
- Micro-Learning Flashcard
- Pristine Kannada (ಕನ್ನಡ) bilingual adaptations for Karnataka aspirants.
"""

from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta

CURRICULUM_MODULES: List[Dict[str, Any]] = [
    {
        "id": "GS2_POLITY_01",
        "paper": "GS-2: Polity & Governance",
        "sub_topic": "Federalism & Discretionary Powers of the Governor",
        "title": "Office of the Governor: Constitutional Role, Discretion, and Federal Tensions",
        "kannada_title": "ರಾಜ್ಯಪಾಲರ ಹುದ್ದೆ: ಸಾಂವಿಧಾನಿಕ ಪಾತ್ರ, ವಿವೇಚನಾಧಿಕಾರ ಮತ್ತು ಒಕ್ಕೂಟ ವ್ಯವಸ್ಥೆಯ ಸವಾಲುಗಳು",
        "trigger": "Supreme Court rulings on timely assent to state assembly bills and gubernatorial delays under Article 200.",
        "kannada_trigger": "ವಿಧಾನಸಭೆ ಅಂಗೀಕರಿಸಿದ ಮಸೂದೆಗಳಿಗೆ ಒಪ್ಪಿಗೆ ನೀಡುವಲ್ಲಿ ರಾಜ್ಯಪಾಲರ ವಿಳಂಬ ಹಾಗೂ ಸಂವಿಧಾನದ 200ನೇ ವಿಧಿಯ ಕುರಿತ ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ತೀರ್ಪುಗಳು.",
        "static_framework": [
            "Article 153: Office of the Governor for each state.",
            "Article 163: Council of Ministers to aid and advise the Governor (except where Governor acts in discretion).",
            "Article 200: Governor's options on state bills (Assent, Withhold, Reserve for President, Return for reconsideration).",
            "Article 356: President's rule on Governor's report (proclamation of emergency in states)."
        ],
        "analytical_points": [
            "Dual Role Dilemma: Constitutional nominal head of state vs. Central Government representative.",
            "Lack of Fixed Timeframes: Article 200 does not prescribe a strict deadline for assent, leading to legislative gridlock.",
            "Discretionary grey areas: Discretion in hung assemblies (inviting single largest party vs. pre-poll coalition) and floor tests.",
            "Impact on Federal Harmony: Perceived partisan behavior damages cooperative federalism and legislative autonomy."
        ],
        "committees": [
            "Sarkaria Commission (1988): Governor should be an eminent person outside state politics, rarely invoke Article 356.",
            "Venkatachaliah Commission / NCRWC (2002): Six-month time limit for Governor/President to decide on state bills.",
            "Punchhi Commission (2010): Governor removal by state assembly resolution (like impeachment); clear guidelines on post-election discretion.",
            "Shamsher Singh Case (1974) & Nabam Rebia Case (2016): Governor must act on aid and advice of Council of Ministers; discretion is limited."
        ],
        "way_forward": "Amend Article 200 to enforce a reasonable decision window (e.g., 30-60 days). Implement Sarkaria & Punchhi recommendations on non-partisan appointment and consultation with Chief Ministers.",
        "kannada_way_forward": "200ನೇ ವಿಧಿಗೆ ತಿದ್ದುಪಡಿ ತಂದು ಮಸೂದೆಗಳ ತೀರ್ಮಾನಕ್ಕೆ ಕಾಲಮಿತಿ ನಿಗದಿಪಡಿಸುವುದು. ಸರ್ಕಾರಿಯಾ ಮತ್ತು ಪೂಂಛಿ ಆಯೋಗಗಳ ಶಿಫಾರಸುಗಳನ್ನು ಕಟ್ಟುನಿಟ್ಟಾಗಿ ಪಾಲಿಸಿ, ಮುಖ್ಯಮಂತ್ರಿಗಳೊಂದಿಗೆ ಸಮಾಲೋಚಿಸಿ ತಟಸ್ಥ ವ್ಯಕ್ತಿಗಳನ್ನು ನೇಮಿಸುವುದು.",
        "mains_question": "“The office of the Governor has emerged as a major point of friction in Indian federalism.” Critically analyze the scope of discretionary powers of the Governor with special reference to Article 200 and recent judicial pronouncements. (15 Marks, 250 Words)",
        "kannada_mains_question": "“ಭಾರತೀಯ ಒಕ್ಕೂಟ ವ್ಯವಸ್ಥೆಯಲ್ಲಿ ರಾಜ್ಯಪಾಲರ ಹುದ್ದೆಯು ಕೇಂದ್ರ-ರಾಜ್ಯ ಸಂಘರ್ಷದ ಪ್ರಮುಖ ಕೇಂದ್ರಬಿಂದುವಾಗಿದೆ.” ಸಂವಿಧಾನದ 200ನೇ ವಿಧಿ ಮತ್ತು ಇತ್ತೀಚಿನ ನ್ಯಾಯಾಂಗ ತೀರ್ಪುಗಳ ಬೆಳಕಿನಲ್ಲಿ ರಾಜ್ಯಪಾಲರ ವಿವೇಚನಾಧಿಕಾರಗಳ ವ್ಯಾಪ್ತಿಯನ್ನು ವಿಮರ್ಶಾತ್ಮಕವಾಗಿ ವಿಶ್ಲೇಷಿಸಿ. (15 ಅಂಕಗಳು, 250 ಪದಗಳು)",
        "directive": "Critically Analyze (ವಿಮರ್ಶಾತ್ಮಕವಾಗಿ ವಿಶ್ಲೇಷಿಸಿ)",
        "directive_tip": "Examine both constitutional provisions & ground reality. Highlight arguments for maintaining gubernatorial oversight vs arguments against legislative delay. Conclude with constitutional remedies.",
        "keywords": [
            "Article 200", "Cooperative Federalism", "Sarkaria Commission",
            "Punchhi Commission", "Aid & Advice", "Nabam Rebia Case (2016)", "Legislative Autonomy"
        ],
        "blueprint": {
            "intro": "Define constitutional role under Articles 153/163 and note recent Supreme Court observations on 'pocket veto' practices.",
            "body_p1": "Constitutional provisions: Article 200 choices, Article 163 discretion limits, and Shamsher Singh principle.",
            "body_p2": "Friction points: Indefinite pocketing of bills, partisan friction in non-ruling state governments, hung assembly choices.",
            "body_p3": "Institutional & Judicial Safeguards: Landmark judgments (SR Bommai, Rameshwar Prasad, Nabam Rebia) and committee recommendations.",
            "conclusion": "Emphasize cooperative federalism and institutional trust over political expediency."
        },
        "model_answer": """<b>Introduction</b>
The Governor occupies a unique constitutional position as the constitutional head of the State and a vital link between the Union and the States (Article 153). While envisaged as an impartial anchor of cooperative federalism, the office has frequently drawn criticism for executive overreach and legislative stalling.

<b>Constitutional Provisions & Scope of Discretion</b>
• <b>Article 163(1):</b> Governor must act on the <i>'aid and advice'</i> of the Council of Ministers, except where the Constitution expressly requires personal discretion.
• <b>Article 200 Options:</b> On receiving a bill passed by the state legislature, the Governor may:
  1. Give assent;
  2. Withhold assent;
  3. Return the bill (if not a Money Bill) with a message for reconsideration;
  4. Reserve the bill for the President's consideration (Article 201).
• <b>The Core Friction:</b> Article 200 uses the phrase <i>'as soon as possible'</i> without specifying a numeric timeframe. Governors in several states have effectively exercised a 'pocket veto' by sitting on passed bills for months or years.

<b>Judicial Pronouncements</b>
• <b>Shamsher Singh v. State of Punjab (1974):</b> The Governor does not exercise a parallel executive power; discretionary decisions are strictly circumscribed.
• <b>Nabam Rebia Case (2016):</b> The Supreme Court held that the Governor cannot summon or adjourn the Assembly or reserve bills without cabinet advice unless there is a constitutional breakdown.
• <b>Recent Rulings (2023-2024):</b> The Supreme Court clarified that if the Governor withholds assent under Article 200, the bill <i>must</i> be returned to the legislature for reconsideration. If repassed, the Governor is constitutionally bound to assent.

<b>Way Forward & Committee Recommendations</b>
1. <b>Punchhi Commission (2010):</b> Governor should decide on state bills within 6 months; removal process should mirror impeachment by the State Legislature to ensure neutrality.
2. <b>Sarkaria Commission (1988):</b> Appointments should be made in strict consultation with the Chief Minister, choosing eminent figures detached from local politics.
3. <b>Constitutional Amendment:</b> Setting an express timeline (e.g., 60 days) under Article 200 to safeguard legislative sovereignty.

<b>Conclusion</b>
Dr. B.R. Ambedkar envisioned the Governor as an ornament of constitutional propriety, not an agent of political obstruction. Strengthening institutional conventions and adhering to committee guidelines is essential to preserve the spirit of cooperative federalism.""",
        "prelims_mcqs": [
            {
                "question": "With reference to the Governor's powers regarding State Bills under Article 200 of the Indian Constitution, consider the following statements:\n1. If a bill is returned by the Governor and repassed by the State Legislature, the Governor is bound to give assent.\n2. The Constitution specifies a strict mandatory deadline of 30 days for the Governor to act on non-money bills.\n3. A Money Bill cannot be returned by the Governor for reconsideration.\nWhich of the statements given above are correct?",
                "options": [
                    "1 and 2 only",
                    "1 and 3 only",
                    "2 and 3 only",
                    "1, 2 and 3"
                ],
                "correct_option_id": 1,
                "explanation": "Statements 1 and 3 are correct. Under Art 200, once repassed, the Governor cannot withhold assent. A Money Bill cannot be returned for reconsideration. Statement 2 is incorrect because Article 200 uses 'as soon as possible' and provides no fixed 30-day limit."
            },
            {
                "question": "Which of the following landmark judgments of the Supreme Court of India is primarily associated with laying down guidelines to prevent the misuse of Article 356 (President's Rule)?",
                "options": [
                    "Kesavananda Bharati v. State of Kerala (1973)",
                    "S.R. Bommai v. Union of India (1994)",
                    "Minerva Mills v. Union of India (1980)",
                    "Navtej Singh Johar v. Union of India (2018)"
                ],
                "correct_option_id": 1,
                "explanation": "S.R. Bommai v. Union of India (1994) is the historic ruling that established that proclamation of Article 356 is subject to judicial review and floor test is the only constitutional way to test majority."
            },
            {
                "question": "Which Commission recommended that the appointment of the Governor should be made in consultation with the Chief Minister of the State and that active politicians should not be appointed?",
                "options": [
                    "Kothari Commission",
                    "Sarkaria Commission",
                    "Balwant Rai Mehta Committee",
                    "Nanavati Commission"
                ],
                "correct_option_id": 1,
                "explanation": "The Sarkaria Commission on Centre-State Relations (1988) recommended that the Governor should be an eminent person from outside the state, appointed in consultation with the Chief Minister."
            }
        ],
        "capsule": {
            "title": "CONSTITUTION CAPSULE: Article 200 & 201",
            "kannada_title": "ಸಂವಿಧಾನ ಕ್ಯಾಪ್ಸೂಲ್: ವಿಧಿ 200 ಮತ್ತು 201",
            "key_fact": "Article 200 gives the Governor 4 choices on a State Bill: Assent, Withhold, Return for reconsideration, or Reserve for President (Article 201). If the State Legislature passes the returned bill again with or without amendments, the Governor MUST give assent.",
            "kannada_fact": "ವಿಧಿ 200ರ ಅಡಿಯಲ್ಲಿ ರಾಜ್ಯಪಾಲರಿಗೆ 4 ಆಯ್ಕೆಗಳಿವೆ: ಒಪ್ಪಿಗೆ ನೀಡುವುದು, ತಡೆಹಿಡಿಯುವುದು, ಮರುಪರಿಶೀಲನೆಗೆ ಮರಳಿಸುವುದು, ಅಥವಾ ರಾಷ್ಟ್ರಪತಿಗಳ ಪರಿಶೀಲನೆಗೆ ಕಾಯ್ದಿರಿಸುವುದು (ವಿಧಿ 201). ಶಾಸನಸಭೆಯು ಮಸೂದೆಯನ್ನು ಪುನಃ ಅಂಗೀಕರಿಸಿದರೆ ರಾಜ್ಯಪಾಲರು ಕಡ್ಡಾಯವಾಗಿ ಒಪ್ಪಿಗೆ ನೀಡಲೇಬೇಕು.",
            "pyq_note": "UPSC CSE Prelims 2018 & KPSC KAS Prelims 2020 asked about Governor's discretionary vs bound powers."
        }
    },
    {
        "id": "GS3_ECONOMY_01",
        "paper": "GS-3: Indian Economy & Karnataka Growth",
        "sub_topic": "Fiscal Federalism, 16th Finance Commission & State Revenue Distribution",
        "title": "Fiscal Federalism in India: Vertical vs. Horizontal Devolution and the 16th Finance Commission Mandate",
        "kannada_title": "ಭಾರತದಲ್ಲಿ ವಿತ್ತೀಯ ಒಕ್ಕೂಟ ವ್ಯವಸ್ಥೆ: ಲಂಬ ಮತ್ತು ಸಮತಲ ತೆರಿಗೆ ಹಂಚಿಕೆ ಹಾಗೂ 16ನೇ ಹಣಕಾಸು ಆಯೋಗದ ಜವಾಬ್ದಾರಿಗಳು",
        "trigger": "Commencement of work by the 16th Finance Commission headed by Dr. Arvind Panagariya and debates on southern states' fiscal share.",
        "kannada_trigger": "ಡಾ. ಅರವಿಂದ್ ಪನಗಾರಿಯಾ ನೇತೃತ್ವದ 16ನೇ ಹಣಕಾಸು ಆಯೋಗದ ಕಾರ್ಯಾರಂಭ ಹಾಗೂ ದಕ್ಷಿಣ ಭಾರತದ ರಾಜ್ಯಗಳ ತೆರಿಗೆ ಹಂಚಿಕೆ ಕುರಿತ ಚರ್ಚೆಗಳು.",
        "static_framework": [
            "Article 280: Constitution of the Finance Commission every 5 years by the President.",
            "Article 270: Divisible pool of central taxes shared between Union and States.",
            "Article 275: Grants-in-aid to states in need of assistance.",
            "15th FC Devolution: 41% share to states (1% adjusted for J&K/Ladakh UTs)."
        ],
        "analytical_points": [
            "Vertical Devolution: States demand expanding the divisible pool by rationalizing cesses and surcharges (which Union doesn't share).",
            "Horizontal Devolution Dilemma: Equity (helping poorer states with larger population/needs) vs Efficiency (rewarding states with population control and fiscal discipline).",
            "Cess & Surcharge Problem: Cesses have grown from ~3% of gross tax revenue to over 10-12%, bypassing the divisible pool.",
            "Karnataka's Fiscal Context: High tax contribution (2nd largest GST contributor) vs lower percentage devolution under 15th FC (due to higher GSDP and 2011 census demographic weighting)."
        ],
        "committees": [
            "14th Finance Commission (Y.V. Reddy): Historic leap in vertical devolution from 32% to 42%.",
            "15th Finance Commission (N.K. Singh): Adopted 2011 census data, introduced Demographic Performance (12.5%) and Tax Effort (2.5%) criteria.",
            "16th Finance Commission (Arvind Panagariya): Mandated to review disaster management financing, grants-in-aid, and tax sharing formulas."
        ],
        "way_forward": "Cap cesses and surcharges to a maximum of 10% of Gross Tax Revenue or include them in the divisible pool. Increase weightage for tax efficiency and state-level green efforts.",
        "kannada_way_forward": "ಸೆಸ್ ಮತ್ತು ಸರ್ಚಾರ್ಜ್‌ಗಳನ್ನು ಒಟ್ಟು ತೆರಿಗೆ ಸಂಗ್ರಹದ ಶೇ. 10ಕ್ಕೆ ಸೀಮಿತಗೊಳಿಸುವುದು ಅಥವಾ ಅವುಗಳನ್ನು ಹಂಚಿಕೆಯಾಗುವ ತೆರಿಗೆ ಪೂಲ್‌ಗೆ ಸೇರಿಸುವುದು. ತೆರಿಗೆ ಶ್ರಮ ಮತ್ತು ಪರಿಸರ ಸಂರಕ್ಷಣಾ ಪ್ರಯತ್ನಗಳಿಗೆ ಹೆಚ್ಚಿನ ತೂಕ ನೀಡುವುದು.",
        "mains_question": "“Cesses and surcharges have systematically distorted the constitutional mandate of fiscal federalism in India.” Examine this statement and discuss the key challenges before the 16th Finance Commission. (15 Marks, 250 Words)",
        "kannada_mains_question": "“ಸೆಸ್ ಮತ್ತು ಸರ್ಚಾರ್ಜ್‌ಗಳ ವಿಪರೀತ ಬಳಕೆಯು ಭಾರತೀಯ ಸಂವಿಧಾನದ ವಿತ್ತೀಯ ಒಕ್ಕೂಟ ತತ್ವಕ್ಕೆ ಧಕ್ಕೆ ತರುತ್ತಿದೆ.” ಈ ಹೇಳಿಕೆಯನ್ನು ಪರೀಕ್ಷಿಸಿ ಹಾಗೂ 16ನೇ ಹಣಕಾಸು ಆಯೋಗದ ಮುಂದಿರುವ ಪ್ರಮುಖ ಸವಾಲುಗಳನ್ನು ಚರ್ಚಿಸಿ. (15 ಅಂಕಗಳು, 250 ಪದಗಳು)",
        "directive": "Examine (ಪರೀಕ್ಷಿಸಿ)",
        "directive_tip": "Investigate facts, figures, and structural issues. Contrast the rise of cesses with state fiscal autonomy. Discuss both Union revenue constraints and State expenditure burdens.",
        "keywords": [
            "Article 280", "Divisible Pool", "Horizontal Devolution", "Vertical Devolution",
            "Cess & Surcharge", "16th Finance Commission", "Demographic Performance", "Karnataka GSDP"
        ],
        "blueprint": {
            "intro": "Define Article 280 Finance Commission role as the balancing wheel of Indian fiscal federalism.",
            "body_p1": "The Cess & Surcharge conundrum: Article 271 allows Union exclusive rights, but rapid expansion reduces effective state share from 41% to ~30-32%.",
            "body_p2": "Equity vs Efficiency challenge: Northern vs Southern states demographic debate (2011 census impact, fertility rate differentials).",
            "body_p3": "Specific expectations from the 16th Finance Commission under Dr. Arvind Panagariya.",
            "conclusion": "Propose inclusion of cesses in divisible pool and transparent formula rewarding both equity and productivity."
        },
        "model_answer": """<b>Introduction</b>
The Finance Commission (Article 280) acts as the balancing wheel of fiscal federalism in India, correcting vertical imbalances (between Union and States) and horizontal imbalances (among States). However, recent trends in tax collection architecture have tested this equilibrium.

<b>The Problem of Cesses and Surcharges</b>
• <b>Constitutional Exclusion (Article 271):</b> Surcharges and cesses levied for specific purposes belong exclusively to the Union Government and are excluded from the divisible tax pool under Article 270.
• <b>Revenue Distortion:</b> Over the past decade, non-divisible cesses and surcharges have grown to constitute nearly 12-15% of the Union’s Gross Tax Revenue (GTR).
• <b>Effective Devolution Deficit:</b> While the 15th FC recommended a vertical devolution of 41%, in practice States receive only approximately 30-32% of total collections once cesses and surcharges are factored out.

<b>Key Challenges Before the 16th Finance Commission</b>
1. <b>Rationalizing the Divisible Pool:</b> States have unanimously demanded either bringing cesses into the divisible pool or capping them at a fixed proportion (e.g., 5-10% of GTR).
2. <b>The Equity vs. Performance Paradox:</b>
   • Progressive states like Karnataka and Tamil Nadu, having successfully controlled population growth (TFR &lt; 1.8) and achieved high GSDP growth, face reduced revenue shares when weightage heavily favors 2011 population and income distance.
   • Backward states require substantial fiscal equalization to upgrade healthcare, education, and human development indices.
3. <b>Disaster Risk Management Financing:</b> Addressing the escalating cost of localized climate disasters (floods, landslides in Western Ghats, droughts).

<b>Way Forward</b>
• <b>Constitutional Cap:</b> Amend Article 271 to sunset every cess after a designated period (e.g., 3-5 years) or include permanent cesses in Article 270.
• <b>Balanced Formula:</b> Increase the weightage for <i>Demographic Performance</i> (beyond 12.5%) and introduce explicit incentives for Green Ecology / Forest Canopy preservation.

<b>Conclusion</b>
Fiscal federalism requires mutual trust. The 16th Finance Commission under Dr. Arvind Panagariya has the historic responsibility to recalibrate tax sharing to ensure that neither national equity is compromised nor developmental champions are penalized.""",
        "prelims_mcqs": [
            {
                "question": "With reference to the Finance Commission of India, consider the following statements:\n1. The Finance Commission is constituted by the President of India under Article 280 of the Constitution.\n2. Cesses and surcharges levied by the Central Government are mandatorily included in the divisible tax pool shared with States.\n3. The recommendations made by the Finance Commission are only advisory in nature and not legally binding on the government.\nWhich of the statements given above are correct?",
                "options": [
                    "1 and 2 only",
                    "1 and 3 only",
                    "2 and 3 only",
                    "1, 2 and 3"
                ],
                "correct_option_id": 1,
                "explanation": "Statements 1 and 3 are correct. Under Art 280, the President constitutes the FC, and its recommendations are advisory. Statement 2 is false: under Article 271, cesses and surcharges are excluded from the divisible pool."
            },
            {
                "question": "Who has been appointed as the Chairman of the 16th Finance Commission of India?",
                "options": [
                    "Dr. N.K. Singh",
                    "Dr. Y.V. Reddy",
                    "Dr. Arvind Panagariya",
                    "Dr. C. Rangarajan"
                ],
                "correct_option_id": 2,
                "explanation": "Dr. Arvind Panagariya (former Vice-Chairman of NITI Aayog) is the Chairman of the 16th Finance Commission. N.K. Singh headed the 15th FC."
            },
            {
                "question": "Which of the following criteria carried the highest weightage in the horizontal devolution formula of the 15th Finance Commission?",
                "options": [
                    "Demographic Performance",
                    "Income Distance",
                    "Forest and Ecology",
                    "Tax and Fiscal Effort"
                ],
                "correct_option_id": 1,
                "explanation": "Income Distance carried the highest weightage of 45% in the 15th Finance Commission formula, followed by Area (15%) and Population 2011 (15%)."
            }
        ],
        "capsule": {
            "title": "ECONOMY CAPSULE: Horizontal vs Vertical Devolution",
            "kannada_title": "ಅರ್ಥಶಾಸ್ತ್ರ ಕ್ಯಾಪ್ಸೂಲ್: ಲಂಬ ಮತ್ತು ಸಮತಲ ತೆರಿಗೆ ಹಂಚಿಕೆ",
            "key_fact": "Vertical Devolution = Sharing of central divisible pool between Centre and States (currently 41%). Horizontal Devolution = Distribution among the 28 states based on a weighted formula (Income Distance 45%, Population 15%, Area 15%, Forest/Ecology 10%, Demographic Performance 12.5%, Tax Effort 2.5%).",
            "kannada_fact": "ಲಂಬ ಹಂಚಿಕೆ (Vertical Devolution) = ಕೇಂದ್ರ ಮತ್ತು ರಾಜ್ಯಗಳ ನಡುವಿನ ತೆರಿಗೆ ಹಂಚಿಕೆ (ಪ್ರಸ್ತುತ ಶೇ. 41). ಸಮತಲ ಹಂಚಿಕೆ (Horizontal Devolution) = 28 ರಾಜ್ಯಗಳ ನಡುವೆ ಹಂಚಿಕೆ (ಆದಾಯ ಅಂತರ 45%, ಜನಸಂಖ್ಯೆ 15%, ವಿಸ್ತೀರ್ಣ 15%, ಅರಣ್ಯ 10%, ಜನಸಂಖ್ಯಾ ಸಾಧನೆ 12.5%, ತೆರಿಗೆ ಶ್ರಮ 2.5%).",
            "pyq_note": "Repeatedly asked in UPSC CSE (2015, 2021) and KPSC KAS (2017, 2020)."
        }
    },
    {
        "id": "GS1_GEOGRAPHY_KARNATAKA_01",
        "paper": "GS-1: Geography, Environment & Karnataka Special",
        "sub_topic": "Western Ghats Ecology, Landslides & Sustainable Development (Kasturirangan vs Madhav Gadgil)",
        "title": "Western Ghats Eco-Fragility: Landslide Hazards, Development Pressure, and the Conservation Gridlock",
        "kannada_title": "ಪಶ್ಚಿಮ ಘಟ್ಟಗಳ ಪರಿಸರ ಸೂಕ್ಷ್ಮತೆ: ಭೂಕುಸಿತಗಳು, ಅಭಿವೃದ್ಧಿಯ ಒತ್ತಡ ಹಾಗೂ ಸಂರಕ್ಷಣಾ ಸವಾಲುಗಳು",
        "trigger": "Catastrophic monsoon landslides in Wayanad, Shirur (Uttara Kannada), and Kodagu highlighting fragile slopes in the Western Ghats.",
        "kannada_trigger": "ವಯನಾಡ್, ಉತ್ತರ ಕನ್ನಡದ ಶಿರೂರು ಮತ್ತು ಕೊಡಗಿನಲ್ಲಿ ಉಂಟಾದ ಭೀಕರ ಭೂಕುಸಿತಗಳು ಪಶ್ಚಿಮ ಘಟ್ಟಗಳ ಪರಿಸರ ಸೂಕ್ಷ್ಮತೆಯನ್ನು ಮುನ್ನೆಲೆಗೆ ತಂದಿವೆ.",
        "static_framework": [
            "Western Ghats: UNESCO World Heritage site, one of 36 global biodiversity hotspots.",
            "Water Tower of Peninsular India: Origins of Godavari, Krishna, Cauvery, Tungabhadra, Sharavathi, Netravati.",
            "Ecologically Sensitive Areas (ESA) under Environment (Protection) Act, 1986.",
            "Geological vulnerability: Steep lateritic slopes, high rainfall (>3000 mm), fragile escarpments."
        ],
        "analytical_points": [
            "Anthropogenic Triggers: Unregulated slope cutting for linear infrastructure (highways, railways), quarrying, monoculture plantations replacing deep-rooted shola vegetation.",
            "Climate Change Impact: Shift towards high-intensity, short-duration cloudburst precipitation exceeding soil absorption thresholds.",
            "Livelihood vs Conservation Conflict: Resistance from local farming communities and political stakeholders fearing eviction and agrarian curbs under ESA tag.",
            "Disaster Management Gaps: Lack of micro-level landslide susceptibility mapping and real-time pore-water pressure early warning systems."
        ],
        "committees": [
            "Madhav Gadgil Committee / WLEG (2011): Recommended entire Western Ghats as Ecologically Sensitive Area (ESA), divided into 3 zones with complete ban on mining/quarrying in Zone 1.",
            "Kasturirangan Committee / HLWG (2013): Diluted coverage to 37% of Western Ghats as ESA, distinguishing between cultural landscape (settlements/agriculture) and natural landscape.",
            "High-Level Task Force on Slope Stability (2024): Mandates geo-technical surveys before cutting hillslopes for 4-lane corridors."
        ],
        "way_forward": "Implement zone-based micro-zonation using LiDAR. Enforce strict ban on quarrying within 10 km of fragile slopes. Adopt nature-based bio-engineering (vetiver grass, terracing) and compensate local farmers via Payment for Ecosystem Services (PES).",
        "kannada_way_forward": "ಲಿಡಾರ್ (LiDAR) ತಂತ್ರಜ್ಞಾನ ಬಳಸಿ ಸೂಕ್ಷ್ಮ ವಲಯಗಳನ್ನು ಗುರುತಿಸುವುದು. ಸೂಕ್ಷ್ಮ ಬೆಟ್ಟಗಳ ಪ್ರದೇಶಗಳಲ್ಲಿ ಗಣಿಗಾರಿಕೆ ಮತ್ತು ಕಲ್ಲುಕ್ವಾರಿಗಳನ್ನು ನಿಷೇಧಿಸುವುದು. ಸ್ಥಳೀಯ ರೈತರಿಗೆ ಪರಿಸರ ವ್ಯವಸ್ಥೆ ಸೇವೆಗಳ ಪಾವತಿ (PES) ಯೋಜನೆ ಜಾರಿಗೆ ತರುವುದು.",
        "mains_question": "“The recurring landslides in the Western Ghats are not merely natural calamities, but manufactured disasters.” Critically discuss with reference to the Gadgil and Kasturirangan committee reports. (15 Marks, 250 Words)",
        "kannada_mains_question": "“ಪಶ್ಚಿಮ ಘಟ್ಟಗಳಲ್ಲಿ ಪದೇಪದೇ ಸಂಭವಿಸುತ್ತಿರುವ ಭೂಕುಸಿತಗಳು ಕೇವಲ ನೈಸರ್ಗಿಕ ವಿಕೋಪಗಳಲ್ಲ, ಬದಲಿಗೆ ಮಾನವ ನಿರ್ಮಿತ ವಿಪತ್ತುಗಳು.” ಗಾಡ್ಗೀಳ್ ಮತ್ತು ಕಸ್ತೂರಿರಂಗನ್ ಸಮಿತಿ ವರದಿಗಳ ಹಿನ್ನೆಲೆಯಲ್ಲಿ ಈ ಹೇಳಿಕೆಯನ್ನು ವಿಮರ್ಶಾತ್ಮಕವಾಗಿ ಚರ್ಚಿಸಿ. (15 ಅಂಕಗಳು, 250 ಪದಗಳು)",
        "directive": "Critically Discuss (ವಿಮರ್ಶಾತ್ಮಕವಾಗಿ ಚರ್ಚಿಸಿ)",
        "directive_tip": "Analyze natural factors (rainfall, topography) vs anthropogenic interventions (quarrying, highway expansion, resort tourism). Compare Gadgil vs Kasturirangan approaches and offer pragmatic solutions.",
        "keywords": [
            "Biodiversity Hotspot", "Ecologically Sensitive Area (ESA)", "Madhav Gadgil Committee",
            "Kasturirangan Committee", "Slope Destabilization", "Shola Ecosystem", "LiDAR Micro-zonation"
        ],
        "blueprint": {
            "intro": "Highlight geographic significance of Western Ghats and cite recent disasters (Wayanad, Shirur, Kodagu).",
            "body_p1": "Natural vs Man-made triggers: Heavy orographic rain + steep terrain combined with deforestation, slope cutting, and unscientific stone quarrying.",
            "body_p2": "Comparison of Committees: Gadgil (deep ecocentrism, bottom-up Gram Sabha power) vs Kasturirangan (technocratic 37% compromise).",
            "body_p3": "Local resistance: Why states (Karnataka, Kerala, Maharashtra) hesitated to notify ESAs.",
            "conclusion": "Propose balanced roadmap: Payment for Ecosystem Services (PES), bio-engineering, strict slope governance."
        },
        "model_answer": """<b>Introduction</b>
The Western Ghats, stretching 1,600 km across six States, represent one of the world's eight 'hottest hotspots' of biological diversity. However, catastrophic landslides in Wayanad (2024), Shirur/Uttara Kannada (2024), and Kodagu highlight that climate change combined with unchecked anthropogenic pressures has turned natural hazards into manufactured disasters.

<b>Natural Vulnerability vs. Anthropogenic Triggers</b>
• <b>Inherent Fragility:</b> The Western Ghats feature weathered lateritic capping over steep basaltic/granitic escarpments, receiving torrential monsoon rainfall (>3,500 mm).
• <b>Human Interventions:</b>
  1. <i>Slope Destabilization:</i> Unscientific vertical hill-cutting for linear infrastructure (highways, rail tracks) without retaining walls.
  2. <i>Quarrying & Blasting:</i> Heavy vibratory blasting fractures subterranean bedrock, creating slip planes for rainwater infiltration.
  3. <i>Ecosystem Replacement:</i> Deep-rooted native Shola-forest complexes have been replaced with shallow-rooted tea, coffee, and monoculture rubber plantations.

<b>Gadgil vs. Kasturirangan: The Conservation Debate</b>
• <b>Madhav Gadgil Panel (2011):</b>
  - Classified the entire Western Ghats into three Ecologically Sensitive Zones (ESZ-1, 2, 3).
  - Recommended complete prohibition on mining, quarrying, and thermal plants in ESZ-1.
  - Advocated a bottom-up approach empowering Gram Sabhas. Rejected by States as economically restrictive.
• <b>K. Kasturirangan Committee (2013):</b>
  - Adopted a pragmatic compromise, designating only 37% of the total area as Ecologically Sensitive Area (ESA).
  - Differentiated between <i>cultural landscapes</i> (villages, farms) and <i>natural landscapes</i>.
  - Prohibited high-polluting 'red category' industries while permitting regulated agrarian activity.

<b>The Way Forward</b>
1. <b>Micro-Zonation & Early Warning:</b> Deploy LiDAR-based slope mapping and wireless sensors measuring pore-water pressure along high-risk transport corridors.
2. <b>Enforce Buffer Zones:</b> Strict prohibition on heavy quarrying and multi-story resort developments within 10 km of identified landslide-prone slopes.
3. <b>Payment for Ecosystem Services (PES):</b> Compensate local agrarian communities financially for conserving native forest cover.

<b>Conclusion</b>
Ecological security cannot be traded for short-term commercial growth. Adopting the middle ground of the Kasturirangan framework with rigorous slope-stability governance is indispensable to protect life and peninsular water security.""",
        "prelims_mcqs": [
            {
                "question": "With reference to the Western Ghats ecology, consider the following statements:\n1. The Western Ghats traverse across six Indian states.\n2. The Madhav Gadgil Committee recommended demarcating approximately 37% of the Western Ghats as Ecologically Sensitive Area (ESA).\n3. Shola forests are tropical montane forests found in the higher elevations of the South Indian hills.\nWhich of the statements given above is/are correct?",
                "options": [
                    "1 and 2 only",
                    "1 and 3 only",
                    "3 only",
                    "1, 2 and 3"
                ],
                "correct_option_id": 1,
                "explanation": "Statements 1 and 3 are correct. The Western Ghats cover 6 states (Gujarat, Maharashtra, Goa, Karnataka, Kerala, Tamil Nadu) and Shola forests are tropical montane forests. Statement 2 is incorrect because the 37% recommendation was made by the Kasturirangan Committee, whereas Gadgil recommended covering the entire Ghats across 3 zones."
            },
            {
                "question": "Which among the following rivers does NOT originate in the Western Ghats?",
                "options": [
                    "Godavari",
                    "Cauvery",
                    "Narmada",
                    "Netravati"
                ],
                "correct_option_id": 2,
                "explanation": "Narmada originates from the Amarkantak plateau in Madhya Pradesh (Maikal range), not in the Western Ghats. Godavari (Trimbak), Cauvery (Talakaveri), and Netravati (Kudremukh) originate in the Western Ghats."
            },
            {
                "question": "Under which statutory legislation are Ecologically Sensitive Areas (ESAs) notified in India?",
                "options": [
                    "Wildlife (Protection) Act, 1972",
                    "Forest (Conservation) Act, 1980",
                    "Environment (Protection) Act, 1986",
                    "Biological Diversity Act, 2002"
                ],
                "correct_option_id": 2,
                "explanation": "Ecologically Sensitive Areas (ESAs) and Eco-Sensitive Zones (ESZs) are notified under Section 3 of the Environment (Protection) Act, 1986."
            }
        ],
        "capsule": {
            "title": "GEOGRAPHY CAPSULE: Mountain Passes of Western Ghats",
            "kannada_title": "ಭೂಗೋಳ ಕ್ಯಾಪ್ಸೂಲ್: ಪಶ್ಚಿಮ ಘಟ್ಟಗಳ ಪ್ರಮುಖ ಘಾಟ್‌ಗಳು",
            "key_fact": "Major Ghat Passes: 1) Thal Ghat (Mumbai to Nashik), 2) Bhor Ghat (Mumbai to Pune), 3) Palakkad / Palghat Gap (Kerala to Tamil Nadu - Nilgiris & Anamalai break), 4) Shiradi Ghat (Mangaluru to Bengaluru), 5) Charmadi Ghat (Chikkamagaluru to Mangaluru).",
            "kannada_fact": "ಪ್ರಮುಖ ಘಾಟಿಗಳು: 1) ಥಾಲ್ ಘಾಟ್ (ಮುಂಬೈ-ನಾಸಿಕ್), 2) ಭೋರ್ ಘಾಟ್ (ಮುಂಬೈ-ಪುಣೆ), 3) ಪಾಲ್ಘಾಟ್ ಗ್ಯಾಪ್ (ಕೇರಳ-ತಮಿಳುನಾಡು ಸಂಪರ್ಕ), 4) ಶಿರಾಡಿ ಘಾಟ್ (ಮಂಗಳೂರು-ಬೆಂಗಳೂರು), 5) ಚಾರ್ಮಾಡಿ ಘಾಟ್ (ಚಿಕ್ಕಮಗಳೂರು-ಮಂಗಳೂರು).",
            "pyq_note": "Direct questions in UPSC Prelims (2014, 2017) and KPSC PSI & KAS (2019, 2021)."
        }
    },
    {
        "id": "GS2_GOVERNANCE_KARNATAKA_02",
        "paper": "GS-2: Governance & Karnataka Administrative Reforms",
        "sub_topic": "Right to Public Services & Digital Governance (Sakala Scheme & KASP)",
        "title": "Citizen-Centric Governance: Karnataka’s Sakala Mission, Service Guarantees, and Digital Delivery",
        "kannada_title": "ನಾಗರಿಕ ಕೇಂದ್ರಿತ ಆಡಳಿತ: ಕರ್ನಾಟಕದ ಸಕಾಲ ಯೋಜನೆ, ಸೇವಾ ಖಾತರಿ ಮತ್ತು ಡಿಜಿಟಲ್ ಆಡಳಿತ",
        "trigger": "Karnataka government expanding the Sakala Services Act to cover over 1,100 public services with digitized timeline tracking.",
        "kannada_trigger": "ಕರ್ನಾಟಕ ಸರ್ಕಾರವು 1,100ಕ್ಕೂ ಹೆಚ್ಚು ಸಾರ್ವಜನಿಕ ಸೇವೆಗಳಿಗೆ ಡಿಜಿಟಲ್ ಕಾಲಮಿತಿ ನಿಗದಿಪಡಿಸಿ ಸಕಾಲ ಕಾಯ್ದೆಯನ್ನು ವಿಸ್ತರಿಸಿದೆ.",
        "static_framework": [
            "Karnataka Guarantee of Services to Citizens Act, 2011 (Popularly known as Sakala).",
            "Citizen's Charter Movement: Origin in UK (1991), introduced in India (1997) to ensure accountability, transparency, and quality.",
            "Sevottam Model: 3-pillar framework by Department of Administrative Reforms and Public Grievances (DARPG).",
            "Article 21: Right to timely public service is an integral aspect of life with dignity."
        ],
        "analytical_points": [
            "Pioneering Legacy: Karnataka was among the first states to back citizen charters with statutory penalties on defaulting officers.",
            "De-personalization of Service: Integration with Seva Sindhu portal cuts physical interface with clerks, reducing petty corruption.",
            "Bottlenecks in Execution: Server downtimes, lack of digital literacy among rural citizens, and pendency at field levels (Tahsildar / Village Accountant).",
            "Accountability Mechanisms: Penalty of Rs. 20/day (up to Rs. 500) deducted from the salary of defaulting designated officers."
        ],
        "committees": [
            "2nd Administrative Reforms Commission (ARC) - 12th Report: 'Citizen-Centric Administration - The Heart of Governance'. Recommended statutory backing for Citizen Charters across India.",
            "Karnataka Administrative Reforms Commission-2 (KARC-2 headed by T.M. Vijay Bhaskar): Recommended rationalizing 1,000+ government forms, eliminating physical gazetted attestations, and digitizing Gram Panchayat records."
        ],
        "way_forward": "Implement proactive service delivery using Jan Aadhar / Kutumba data without citizens needing to apply. Strengthen autonomous appellate authorities and automate compensatory payouts.",
        "kannada_way_forward": "ಕುಟುಂಬ (Kutumba) ಡೇಟಾ ಬಳಸಿ ನಾಗರಿಕರು ಅರ್ಜಿ ಸಲ್ಲಿಸದೆಯೇ ಅರ್ಹ ಫಲಾನುಭವಿಗಳಿಗೆ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಸೇವೆ ಒದಗಿಸುವುದು. ಸ್ವತಂತ್ರ ಮೇಲ್ಮನವಿ ಪ್ರಾಧಿಕಾರಗಳನ್ನು ಬಲಪಡಿಸುವುದು.",
        "mains_question": "“Statutory service delivery acts like Karnataka's Sakala have transformed citizens from passive petitioners into empowered right-holders.” Evaluate the successes and systemic challenges of Sakala. (10 Marks, 150 Words)",
        "kannada_mains_question": "“ಕರ್ನಾಟಕದ 'ಸಕಾಲ'ದಂತಹ ಶಾಸನಬದ್ಧ ಸೇವಾ ಖಾತರಿ ಕಾಯ್ದೆಗಳು ಸಾರ್ವಜನಿಕರನ್ನು ಕೇವಲ ಅರ್ಜಿದಾರರಿಂದ ಸಬಲೀಕೃತ ಹಕ್ಕುದಾರರನ್ನಾಗಿ ಪರಿವರ್ತಿಸಿವೆ.” ಸಕಾಲದ ಯಶಸ್ಸು ಮತ್ತು ಎದುರಿಸುತ್ತಿರುವ ಸಾಂಸ್ಥಿಕ ಸವಾಲುಗಳನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡಿ. (10 ಅಂಕಗಳು, 150 ಪದಗಳು)",
        "directive": "Evaluate (ಮೌಲ್ಯಮಾಪನ ಮಾಡಿ)",
        "directive_tip": "Weigh measurable successes (millions of applications cleared, tracking numbers) against lingering pain points (rejections, technical glitches, lack of awareness).",
        "keywords": [
            "Karnataka Sakala Act 2011", "Seva Sindhu", "Citizen's Charter", "2nd ARC 12th Report",
            "Sevottam Model", "Vijay Bhaskar Commission", "Kutumba Database"
        ],
        "blueprint": {
            "intro": "Define Sakala as Karnataka's landmark guarantee of services legislation enacted in 2011.",
            "body_p1": "Successes: 1,100+ services, 95%+ disposal rates, unique Guarantee of Services to Citizens (GSC) number, financial penalty on errant officers.",
            "body_p2": "Challenges: Premature application rejections to escape penalty deadlines, technical server crashes, digital divide in rural areas.",
            "conclusion": "Link to future reforms: Proactive faceless service delivery based on Kutumba architecture."
        },
        "model_answer": """<b>Introduction</b>
The Karnataka Guarantee of Services to Citizens Act, 2011 (popularly known as <i>'Sakala'</i>) operationalized the 2nd Administrative Reforms Commission's recommendation to give Citizen Charters statutory teeth, transforming public service delivery from bureaucratic patronage to a legal right.

<b>Key Successes of Sakala</b>
1. <b>Massive Scope:</b> Covers over 1,100 government services across 30+ departments (revenue, transport, commercial taxes, police).
2. <b>Statutory Accountability:</b> Every application receives a unique GSC (Guarantee of Services to Citizens) tracking number. Defaulting officials face compensatory deductions (Rs. 20/day) from their salaries.
3. <b>High Clearance Rate:</b> The portal consistently clocks an average disposal rate exceeding 95% within statutory deadlines.
4. <b>Digital Integration:</b> Merged with the <i>Seva Sindhu</i> unified portal, significantly cutting physical touting at taluk offices.

<b>Lingering Systemic Challenges</b>
• <b>Tactical Rejections:</b> Field-level officials frequently reject applications on minor clerical pretexts close to the deadline to avoid personal salary deductions.
• <b>Digital Divide & Rural Access:</b> High dependency on private cyber centers and Grama One franchises due to complex documentation interfaces.
• <b>Appellate Inefficiency:</b> Citizens rarely pursue the two-tier appeal process due to lack of awareness regarding monetary compensation.

<b>Way Forward</b>
Following the Vijay Bhaskar Commission (KARC-2) recommendations, Karnataka should transition from 'applied governance' to <b>proactive faceless governance</b>—leveraging the state's <i>Kutumba</i> resident database to deliver caste, income, and welfare certificates automatically without cumbersome application cycles.""",
        "prelims_mcqs": [
            {
                "question": "In which year was the landmark Karnataka Guarantee of Services to Citizens Act (Sakala) enacted?",
                "options": [
                    "2005",
                    "2009",
                    "2011",
                    "2015"
                ],
                "correct_option_id": 2,
                "explanation": "The Karnataka Guarantee of Services to Citizens Act (Sakala) was passed unanimously by the Karnataka Legislature in December 2011 and implemented across the state in 2012."
            },
            {
                "question": "The 'Sevottam' model, developed by DARPG in India, is an assessment framework for:",
                "options": [
                    "Public procurement transparency",
                    "Public service delivery and grievance redressal",
                    "Direct tax simplification",
                    "Environmental impact assessment"
                ],
                "correct_option_id": 1,
                "explanation": "Sevottam (Service + Uttam) is a quality management framework developed by DARPG to assess and enhance the quality of public service delivery, implementation of Citizen's Charters, and grievance redressal mechanisms."
            },
            {
                "question": "Which Committee/Commission in Karnataka recently submitted comprehensive recommendations for administrative rationalization, civil service reforms, and reducing citizen paperwork?",
                "options": [
                    "T.M. Vijay Bhaskar Commission (KARC-2)",
                    "D.M. Nanjundappa Committee",
                    "Chinnappa Reddy Commission",
                    "K. Kasturirangan Task Force"
                ],
                "correct_option_id": 0,
                "explanation": "The Karnataka Administrative Reforms Commission-2 (KARC-2), headed by former Chief Secretary T.M. Vijay Bhaskar, submitted extensive reports recommending reduction of redundant forms, cadre rationalization, and citizen-friendly digital delivery."
            }
        ],
        "capsule": {
            "title": "GOVERNANCE CAPSULE: The 3 Pillars of Sevottam Model",
            "kannada_title": "ಆಡಳಿತ ಕ್ಯಾಪ್ಸೂಲ್: ಸೇವೋತ್ತಮ್ ಮಾದರಿಯ ಮೂರು ಆಧಾರಸ್ತಂಭಗಳು",
            "key_fact": "Sevottam Framework Pillars: 1) Citizen's Charter (defined service standards), 2) Public Grievance Redressal (prompt resolution), 3) Service Delivery Capability (infrastructure and motivated personnel).",
            "kannada_fact": "ಸೇವೋತ್ತಮ್ ಮಾದರಿಯ 3 ಆಧಾರಸ್ತಂಭಗಳು: 1) ನಾಗರಿಕ ಸನ್ನದು (ಸೇವಾ ಮಾನದಂಡಗಳು), 2) ಸಾರ್ವಜನಿಕ ಕುಂದುಕೊರತೆ ನಿವಾರಣೆ, 3) ಸೇವಾ ವಿತರಣಾ ಸಾಮರ್ಥ್ಯ (ಮೂಲಸೌಕರ್ಯ ಮತ್ತು ತರಬೇತಿ).",
            "pyq_note": "Crucial for UPSC GS-4 Ethics and GS-2 Governance, and KPSC KAS General Studies."
        }
    },
    {
        "id": "GS3_ENVIRONMENT_KARNATAKA_03",
        "paper": "GS-3: Environment, Wildlife & Conservation",
        "sub_topic": "Project Tiger, Human-Wildlife Conflict & Elephant Corridors in Nilgiri Biosphere",
        "title": "50 Years of Project Tiger: Habitat Fragmentation, Elephant Corridors, and Mitigation of Human-Animal Conflict",
        "kannada_title": "ಪ್ರಾಜೆಕ್ಟ್ ಟೈಗರ್ 50 ವರ್ಷಗಳು: ಆವಾಸಸ್ಥಾನಗಳ ವಿಘಟನೆ, ಆನೆ ಕಾರಿಡಾರ್‌ಗಳು ಹಾಗೂ ಮಾನವ-ವನ್ಯಜೀವಿ ಸಂಘರ್ಷ",
        "trigger": "Karnataka recording India's 2nd highest tiger population (563) and rising human-elephant conflicts in Hassan, Kodagu, and Chamarajanagar.",
        "kannada_trigger": "ಕರ್ನಾಟಕದಲ್ಲಿ ದೇಶದಲ್ಲೇ 2ನೇ ಅತಿ ಹೆಚ್ಚು ಹುಲಿಗಳು (563) ದಾಖಲಾಗಿದ್ದು, ಹಾಸನ, ಕೊಡಗು ಮತ್ತು ಚಾಮರಾಜನಗರದಲ್ಲಿ ಮಾನವ-ಆನೆ ಸಂಘರ್ಷ ಹೆಚ್ಚುತ್ತಿದೆ.",
        "static_framework": [
            "Project Tiger: Launched on April 1, 1973 from Jim Corbett National Park.",
            "Karnataka's 5 Tiger Reserves: Bandipur, Nagarahole, BRT (Biligiri Ranganatha Temple), Bhadra, and Kali (Anshi-Dandeli).",
            "Nilgiri Biosphere Reserve: First biosphere reserve in India (1986); spans Karnataka, Kerala, Tamil Nadu.",
            "Wildlife (Protection) Act, 1972: Statutory body National Tiger Conservation Authority (NTCA) formed under 2006 amendment."
        ],
        "analytical_points": [
            "Conservation Paradox: Success in increasing carnivore numbers within shrinking, fragmented protected areas pushes animals into agricultural buffer zones.",
            "Linear Infrastructure Menace: Railway tracks, night-traffic highways (NH-766 in Bandipur), and power lines fragment ancient elephant migration routes.",
            "Economic Distress for Farmers: Coffee plantation workers and maize/paddy farmers in Malnad suffer crop destruction, livestock predation, and loss of life.",
            "Technological Interventions: Karnataka's Railway Barricades, Radio-collaring matriarch elephants, and SMS/AI camera alert systems."
        ],
        "committees": [
            "Madhav Gadgil Task Force on Tiger Reserves (2005): Recommended community co-existence in buffer zones and voluntary relocation from core zones.",
            "Elephant Task Force / 'Gajah' Report (headed by Mahesh Rangarajan, 2010): Recommended declaring Elephant as National Heritage Animal and giving statutory status to Elephant Corridors.",
            "Supreme Court Judgment on Sigur Elephant Corridor (2020): Upheld the closure of commercial resorts encroaching on historical elephant migration pathways."
        ],
        "way_forward": "Secure and legally notify key interstate corridors (e.g. Brahmagiri-Nilgiri). Scale up Karnataka's successful discarded-railway-track fences over ineffective solar fencing. Fast-track ex-gratia compensation payments via direct benefit transfer (DBT).",
        "kannada_way_forward": "ಅಂತರರಾಜ್ಯ ಆನೆ ಕಾರಿಡಾರ್‌ಗಳನ್ನು ಕಾನೂನುಬದ್ಧವಾಗಿ ಅಧಿಸೂಚಿಸುವುದು. ಸೌರ ಬೇಲಿಗಳ ಬದಲು ಹಳೆಯ ರೈಲ್ವೆ ಹಳಿಗಳ ಬ್ಯಾರಿಕೇಡ್‌ಗಳನ್ನು ವಿಸ್ತರಿಸುವುದು. ಡಿಬಿಟಿ (DBT) ಮೂಲಕ ಬೆಳೆಹಾನಿ ಪರಿಹಾರವನ್ನು ತ್ವರಿತವಾಗಿ ಪಾವತಿಸುವುದು.",
        "mains_question": "“The success of wildlife conservation in India has paradoxically intensified human-wildlife conflict.” Examine this phenomenon with special reference to Karnataka's Nilgiri Biosphere edge and suggest mitigation strategies. (15 Marks, 250 Words)",
        "kannada_mains_question": "“ಭಾರತದಲ್ಲಿ ವನ್ಯಜೀವಿ ಸಂರಕ್ಷಣೆಯ ಯಶಸ್ಸೇ ವಿಪರ್ಯಾಸವೆಂಬಂತೆ ಮಾನವ-ವನ್ಯಜೀವಿ ಸಂಘರ್ಷವನ್ನು ತೀವ್ರಗೊಳಿಸಿದೆ.” ಕರ್ನಾಟಕದ ನೀಲಗಿರಿ ಬಯೋಸ್ಫಿಯರ್ ಪ್ರದೇಶದ ಹಿನ್ನೆಲೆಯಲ್ಲಿ ಈ ಸಮಸ್ಯೆಯನ್ನು ಪರೀಕ್ಷಿಸಿ ಹಾಗೂ ಪರಿಹಾರ ಕ್ರಮಗಳನ್ನು ಸೂಚಿಸಿ. (15 ಅಂಕಗಳು, 250 ಪದಗಳು)",
        "directive": "Examine (ಪರೀಕ್ಷಿಸಿ)",
        "directive_tip": "Highlight the ecological carrying capacity vs habitat fragmentation paradox. Discuss socioeconomic costs on fringe villages and present tested tech-driven & biological solutions.",
        "keywords": [
            "Project Tiger", "NTCA", "Nilgiri Biosphere Reserve", "Gajah Report 2010",
            "Human-Elephant Conflict (HEC)", "Sigur Corridor", "Railway Barricades"
        ],
        "blueprint": {
            "intro": "Contextualize Karnataka's tiger (563) and elephant population (~6,000) leading to edge-habitat conflicts in Malnad/Chamarajanagar.",
            "body_p1": "Causes of conflict: Carrying capacity saturation, fragmentation by linear infrastructure, invasive species (Lantana camara) choking fodder.",
            "body_p2": "Socio-economic impact: Crop loss, human casualties, retaliatory electrocutions/poisonings of wildlife.",
            "body_p3": "Karnataka's Mitigation Innovations: Steel rail fencing, Elephant Task Force squads, automated AI-camera triggers, early warning SMS.",
            "conclusion": "Emphasize sustainable co-existence, notifying corridors, and community-led conservation."
        },
        "model_answer": """<b>Introduction</b>
Karnataka represents a conservation benchmark in India, harboring over 563 tigers (second only to Madhya Pradesh) and India's largest Asian Elephant population (~6,049). However, this ecological triumph has paradoxically triggered acute Human-Wildlife Conflict (HWC) in frontier landscapes such as Hassan, Kodagu, and Chamarajanagar.

<b>The Ecological Paradox: What Drives the Conflict?</b>
1. <b>Carrying Capacity & Habitat Saturation:</b> Core forests in Bandipur and Nagarahole have reached predator carrying capacity, compelling young tigers and dispersing elephant herds into human-dominated agricultural fringes.
2. <b>Habitat Fragmentation:</b> National highways, power transmission lines, and monoculture plantations fragment contiguous swathes of the Nilgiri Biosphere Reserve, severing traditional migration corridors.
3. <b>Invasive Floral Infestation:</b> Unchecked spread of weeds like <i>Lantana camara</i> and <i>Senna spectabilis</i> has suppressed palatable grasses, forcing herbivores into agricultural crop fields (paddy, sugarcane, banana).

<b>Systemic Impacts on Fringe Communities</b>
• <b>Agrarian Destabilization:</b> Devastating crop depredation leading to farmer distress and indebtedness.
• <b>Retaliatory Violence:</b> Increased instances of deliberate electric fence tapping and snare traps causing unnatural animal mortality.

<b>Mitigation Strategies & Best Practices</b>
1. <b>Physical Barriers:</b> Karnataka’s pioneering deployment of discarded <b>railway track barricades</b> has proven far more durable and tamper-proof than conventional solar power fencing.
2. <b>Technological Early Warning:</b> Deploying radio-collars on herd matriarchs, AI-enabled trail cameras with thermal sensors, and automated voice/SMS alerts to villagers when herds approach within 1 km.
3. <b>Legal Corridor Protection:</b> Enforce the Supreme Court’s Sigur Corridor judgment (2020) by strictly demolishing unauthorized commercial resorts obstructing critical bottlenecks.
4. <b>Timely Compensation:</b> Immediate digital disbursement of ex-gratia relief through Direct Benefit Transfer (DBT) to prevent resentment and retaliatory strikes.

<b>Conclusion</b>
Wildlife conservation cannot succeed in opposition to local communities. Moving from episodic conflict response to long-term landscape-level corridor restoration is essential for harmonious co-existence.""",
        "prelims_mcqs": [
            {
                "question": "Which of the following National Parks / Tiger Reserves was the first Biosphere Reserve to be established in India?",
                "options": [
                    "Nanda Devi Biosphere Reserve",
                    "Nilgiri Biosphere Reserve",
                    "Sundarbans Biosphere Reserve",
                    "Gulf of Mannar Biosphere Reserve"
                ],
                "correct_option_id": 1,
                "explanation": "The Nilgiri Biosphere Reserve, established in 1986, was India's first biosphere reserve under UNESCO's Man and the Biosphere (MAB) programme."
            },
            {
                "question": "Consider the following Tiger Reserves in Karnataka:\n1. Bandipur\n2. Bhadra\n3. Kali (Anshi-Dandeli)\n4. Biligiri Ranganatha Temple (BRT)\nWhich of the above are located in the Western Ghats / Nilgiri landscape?",
                "options": [
                    "1 and 2 only",
                    "2 and 3 only",
                    "1, 2 and 4 only",
                    "1, 2, 3 and 4"
                ],
                "correct_option_id": 3,
                "explanation": "All four (Bandipur, Bhadra, Kali, and BRT, along with Nagarahole) are declared Tiger Reserves in Karnataka located in the Western Ghats / Nilgiris biogeographical zone."
            },
            {
                "question": "The National Tiger Conservation Authority (NTCA) is a statutory body constituted under the provisions of which Act?",
                "options": [
                    "Environment (Protection) Act, 1986",
                    "Wildlife (Protection) Act, 1972",
                    "Forest (Conservation) Act, 1980",
                    "Biological Diversity Act, 2002"
                ],
                "correct_option_id": 1,
                "explanation": "The NTCA was constituted under Section 38L (1) of the Wildlife (Protection) Act, 1972, via the 2006 amendment following recommendations of the Tiger Task Force."
            }
        ],
        "capsule": {
            "title": "ENVIRONMENT CAPSULE: The 5 Tiger Reserves of Karnataka",
            "kannada_title": "ಪರಿಸರ ಕ್ಯಾಪ್ಸೂಲ್: ಕರ್ನಾಟಕದ 5 ಹುಲಿ ಸಂರಕ್ಷಿತ ಪ್ರದೇಶಗಳು",
            "key_fact": "Karnataka's 5 Tiger Reserves: 1) Bandipur (Chamarajanagar), 2) Nagarahole (Kodagu/Mysuru), 3) Bhadra (Chikkamagaluru), 4) Kali / Anshi-Dandeli (Uttara Kannada), 5) BRT Sanctuary (Chamarajanagar). Karnataka has the 2nd highest tiger count in India (563).",
            "kannada_fact": "ಕರ್ನಾಟಕದ 5 ಹುಲಿ ಸಂರಕ್ಷಿತ ಪ್ರದೇಶಗಳು: 1) ಬಂಡೀಪುರ (ಚಾಮರಾಜನಗರ), 2) ನಾಗರಹೊಳೆ (ಕೊಡಗು/ಮೈಸೂರು), 3) ಭದ್ರಾ (ಚಿಕ್ಕಮಗಳೂರು), 4) ಕಾಳಿ (ಉತ್ತರ ಕನ್ನಡ), 5) ಬಿಆರ್‌ಟಿ (ಚಾಮರಾಜನಗರ). ಕರ್ನಾಟಕವು ಭಾರತದಲ್ಲೇ 2ನೇ ಅತಿ ಹೆಚ್ಚು (563) ಹುಲಿಗಳನ್ನು ಹೊಂದಿದೆ.",
            "pyq_note": "A favorite recurring topic in KPSC KAS, PSI, and FDA exams."
        }
    }
]


def get_daily_module(date_str: str = None) -> Dict[str, Any]:
    """
    Selects a deterministic high-yield module for a given date so that
    all modules across the day (Dossier, Drill, Mains, Capsule) align
    to the same theme for deep, structured learning.
    """
    if not date_str:
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        date_str = datetime.now(ist_offset).strftime("%Y-%m-%d")
    
    # Simple day-of-year rotation
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    day_num = dt.timetuple().tm_yday
    idx = (day_num - 1) % len(CURRICULUM_MODULES)
    return CURRICULUM_MODULES[idx]
