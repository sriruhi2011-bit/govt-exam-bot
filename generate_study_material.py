# generate_study_material.py
"""
Study Material PDF Generator & Demo Pipeline.
Creates high-yield study material PDFs matching:
1. 'The Civils Vault' English style (Prelims Notes + Mains Key Editorials + Statement MCQs)
2. 'KPSCinsights' Kannada style (Why in News + Static Background + Traps + Karnataka Perspective + One-Liners + MCQs)
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from pdf_engine import PDFEngine
from curriculum_bank import get_daily_module


def get_demo_english_data():
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist_offset)
    module = get_daily_module()

    return {
        "title": "Prelims & Mains Analysis",
        "brand_title": "The Civils Vault",
        "source_name": "The Hindu & Indian Express",
        "date_str": now.strftime("%A, %d %B %Y"),
        "channel_handle": "t.me/TheCivilsVault",
        "footer_tagline": "Prelims · important items with static depth",
        "prelims_items": [
            {
                "title": "Delimitation and Constitution Amendment Bill",
                "badge": "high-yield",
                "in_news": "Government is considering a Special Session to pass a proposed Constitution Amendment Bill raising Lok Sabha strength to 850 and paving the way for 33% women's quota, based on 2011 Census.",
                "static_points": [
                    "<span class='law-ref'>Art 368:</span> Special majority of total membership and two-thirds of members present and voting in each House.",
                    "<span class='law-ref'>Federal features:</span> E.g. representation of States in Parliament also needs ratification by at least half of the State legislatures.",
                    "<span class='law-ref'>Art 81 & 82:</span> Art 81 caps Lok Sabha at 550 (530 States + 20 UTs); present strength 543. Art 82 mandates readjustment after each Census.",
                    "<span class='law-ref'>42nd & 84th Amendments:</span> 42nd Amendment froze seats on 1971 Census; 84th Amendment (2001) extended the freeze till first Census after 2026.",
                    "<span class='law-ref'>Delimitation Commission:</span> Orders have the force of law and cannot be questioned in any court (Delimitation Act S.10(2); Art 329)."
                ],
                "trap": "Not every constitutional amendment requires State ratification—only amendments impacting federal provisions (e.g., 7th Schedule, Supreme Court, High Courts, representation of States)."
            },
            {
                "title": "Retail Inflation & Monetary Policy Stance",
                "badge": "economy",
                "in_news": "October CPI inflation reached 6.1%, crossing the RBI's 6% upper tolerance limit. Food and beverages hit 8.5%, while transport stood at 5.8%.",
                "static_points": [
                    "<span class='law-ref'>CPI Compilation:</span> CPI (Combined) is compiled monthly by the National Statistical Office (NSO), MoSPI. CPI-IW is compiled by Labour Bureau; WPI by DPIIT.",
                    "<span class='law-ref'>Flexible Inflation Targeting:</span> Statutory mandate of 4% with a tolerance band of ±2% (2% to 6%) under Section 45ZA of the RBI Act 1934.",
                    "<span class='law-ref'>Failure Criteria:</span> If inflation remains outside the 2%–6% band for three consecutive quarters, the RBI must submit a failure report to the Central Government (Section 45ZN)."
                ],
                "trap": "WPI does not include services, only manufactured goods and fuel. CPI captures both goods and consumer services."
            },
            {
                "title": "Sixth Schedule & Ladakh Governance",
                "badge": "polity",
                "in_news": "Hill council elections scheduled; Leh Apex Body and Kargil Democratic Alliance press for Sixth Schedule status and full statehood for the Union Territory of Ladakh.",
                "static_points": [
                    "<span class='law-ref'>Sixth Schedule (Arts 244(2) & 275(1)):</span> Autonomous District Councils (ADCs) in Assam, Meghalaya, Tripura, and Mizoram (AMTM).",
                    "<span class='law-ref'>Council Composition:</span> Up to 30 members (up to 4 nominated by the Governor, 26 elected), with a 5-year tenure and legislative power over land, forests, and customs.",
                    "<span class='law-ref'>Fifth vs Sixth Schedule:</span> Fifth Schedule applies to Scheduled Areas in 10 states; Sixth Schedule grants far higher legislative and judicial autonomy to tribal areas."
                ],
                "trap": "Ladakh is not currently under either the 5th or 6th Schedule; it is governed directly by the Ministry of Home Affairs via a Lieutenant Governor without a legislative assembly."
            }
        ],
        "mains_editorials": [
            {
                "title": "India–Bangladesh Diplomatic Relations Amidst Regional Shifts",
                "paper": "GS2 · International Relations",
                "context": "Recent political transitions in Dhaka and bilateral negotiations over water-sharing treaties highlight new challenges for India's Neighbourhood First Policy.",
                "flowchart": "Political Transition in Dhaka → Treaty Expirations Approaching → Consular Talks Resumed → Focus on Economic Corridors",
                "body_points": [
                    "<b>Strategic Significance:</b> Bangladesh is India's largest trade partner in South Asia and crucial for Northeast connectivity (Chittagong and Mongla ports).",
                    "<b>Water Resource Management:</b> Ganges Water Treaty 1996 approaches its 30-year renewal deadline; Teesta river negotiations remain a critical federal concern.",
                    "<b>Security & Border Stability:</b> 4,096 km border managed by BSF; counter-terrorism intelligence sharing remains vital to contain border crimes and illicit migration."
                ],
                "way_forward_points": [
                    "Delink bilateral developmental initiatives and cross-border power transmission from domestic electoral changes.",
                    "Fast-track negotiations on the Comprehensive Economic Partnership Agreement (CEPA) and border trade infrastructure (Petrapole-Benapole).",
                    "Strengthen institutional frameworks through the Joint River Commission (JRC) to establish predictable hydrological data sharing."
                ],
                "keywords": "Neighbourhood First, Act East, Strategic patience, Teesta riparian rights, BBIN corridor, Border management",
                "practice_question": "“Stability in Bangladesh is inextricably linked to the security and economic integration of India's Northeast.” Critically examine the contemporary strategic challenges and suggest a pragmatic diplomatic roadmap. (15 Marks, 250 Words)"
            }
        ],
        "mcqs": [
            {
                "topic": "Constitutional Amendment & Federalism",
                "statements": [
                    "A Constitution Amendment Bill under Article 368 requires a special majority in both Houses of Parliament.",
                    "Every constitutional amendment bill requires ratification by at least half of the State legislatures before presidential assent.",
                    "The Delimitation Commission orders cannot be questioned before any court of law once published in the Gazette."
                ],
                "options": "(a) 1 only  (b) 1 and 3 only  (c) 2 and 3 only  (d) 1, 2, and 3",
                "answer": "(b)",
                "explanation": "Statement 2 is incorrect. Only amendments seeking to alter federal provisions listed in the proviso to Article 368(2) require ratification by 50% of the State legislatures. Statements 1 and 3 are correct."
            },
            {
                "topic": "Inflation Targeting Framework",
                "statements": [
                    "CPI (Combined) is released monthly by the Office of the Economic Adviser, Ministry of Commerce and Industry.",
                    "Under Section 45ZA of the RBI Act, the inflation target is 4% with an upper tolerance limit of 6% and lower limit of 2%."
                ],
                "options": "(a) 1 only  (b) 2 only  (c) Both 1 and 2  (d) Neither 1 nor 2",
                "answer": "(b)",
                "explanation": "Statement 1 is incorrect: CPI (Combined) is compiled and published by the National Statistical Office (NSO), MoSPI. WPI is released by the Office of Economic Adviser (DPIIT). Statement 2 is correct."
            }
        ]
    }


def get_demo_kannada_data():
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist_offset)
    module = get_daily_module()

    return {
        "brand_title": "KPSCinsights",
        "source_title": "ಪ್ರಜಾವಾಣಿ & ಡೆಕ್ಕನ್ ಹೆರಾಲ್ಡ್",
        "date_str": now.strftime("%d %B %Y"),
        "main_banner": "KPSC / KEA Exams: KAS · PSI · PDO · FDA · SDA & more",
        "sub_banner": "ದೈನಂದಿನ ಪ್ರಜಾವಾಣಿ ಸಮಗ್ರ ವಿಶ್ಲೇಷಣೆ",
        "footer_brand": "KPSCinsights | Daily Prajavani Exam Analysis | Telegram: @kansiri_daily_updates",
        "topics": [
            {
                "title": "ನಮ್ಮ ಮೆಟ್ರೊ ಗುಲಾಬಿ ಮಾರ್ಗ: 100 ಕಿ.ಮೀ. ದಾಟಿದ ಬೆಂಗಳೂರು ಮೆಟ್ರೊ ಜಾಲ",
                "why_in_news": "ಬೆಂಗಳೂರಿನ ‘ನಮ್ಮ ಮೆಟ್ರೊ’ ಗುಲಾಬಿ ಮಾರ್ಗದ 7.5 ಕಿ.ಮೀ. ಎತ್ತರಿಸಿದ ಮಾರ್ಗ ಉದ್ಘಾಟನೆಗೊಂಡಿದೆ. ಇದರಿಂದಾಗಿ ಬೆಂಗಳೂರು ಮೆಟ್ರೊ ಜಾಲವು 100 ಕಿ.ಮೀ. ಮೈಲಿಗಲ್ಲು ದಾಟಿದ್ದು, ದೆಹಲಿ ಮೆಟ್ರೊ ನಂತರ ದೇಶದಲ್ಲೇ 2ನೇ ಅತಿ ದೊಡ್ಡ ಮೆಟ್ರೊ ಜಾಲವಾಗಿ ಹೊರಹೊಮ್ಮಿದೆ. ಜಯದೇವ ಆಸ್ಪತ್ರೆ ನಿಲ್ದಾಣವು ದೇಶದ ಅತಿ ಎತ್ತರದ ಇಂಟರ್‌ಚೇಂಜ್ ನಿಲ್ದಾಣವಾಗಿದೆ.",
                "static_points": [
                    "<b>ಬಿಎಂಆರ್‌ಸಿಎಲ್ (BMRCL):</b> ಕೇಂದ್ರ ಹಾಗೂ ಕರ್ನಾಟಕ ರಾಜ್ಯ ಸರ್ಕಾರಗಳ 50:50 ಪಾಲುದಾರಿಕೆಯ ಜಂಟಿ ಉದ್ಯಮ (SPV).",
                    "<b>ನೋಡಲ್ ಸಚಿವಾಲಯ:</b> ಕೇಂದ್ರ ವಸತಿ ಮತ್ತು ನಗರ ವ್ಯವಹಾರಗಳ ಸಚಿವಾಲಯ (MoHUA).",
                    "<b>ಸುರಕ್ಷತಾ ಅನುಮತಿ:</b> ಮೆಟ್ರೊ ರೈಲ್ವೆ (ಕಾರ್ಯಾಚರಣೆ ಮತ್ತು ನಿರ್ವಹಣೆ) ಕಾಯ್ದೆ 2002ರ ಅಡಿ ಮೆಟ್ರೊ ರೈಲು ಸುರಕ್ಷತಾ ಆಯುಕ್ತರ (CMRS) ಪ್ರಮಾಣಪತ್ರ ಕಡ್ಡಾಯ.",
                    "<b>ಬಣ್ಣದ ಮಾರ್ಗಗಳು:</b> ನೇರಳೆ (Whitefield-Challaghatta), ಹಸಿರು (Madavara-Silk Institute), ಹಳದಿ (RV Road-Bommasandra), ಗುಲಾಬಿ (Kalena Agrahara-Nagawara), ನೀಲಿ (Silk Board-Airport)."
                ],
                "exam_points": [
                    "ಮೊದಲ ಹಂತ ಆರಂಭ: 2011 (ಎಂ.ಜಿ. ರಸ್ತೆ - ಬೈಯಪ್ಪನಹಳ್ಳಿ).",
                    "ಜಯದೇವ ಇಂಟರ್‌ಚೇಂಜ್: ಹಳದಿ ಮತ್ತು ಗುಲಾಬಿ ಮಾರ್ಗಗಳ ಸಮ್ಮಿಲನ ಕೇಂದ್ರ."
                ],
                "trap": "ಮೆಟ್ರೊ ಸುರಕ್ಷತಾ ಆಯುಕ್ತರು (CMRS) ರೈಲ್ವೆ ಮಂಡಳಿಯ ಅಡಿಯಲ್ಲ, ಬದಲಿಗೆ ನಾಗರಿಕ ವಿಮಾನಯಾನ ಸಚಿವಾಲಯದ (MoCA) ರೈಲ್ವೆ ಸುರಕ್ಷತಾ ಆಯೋಗದ ಅಡಿಯಲ್ಲಿ ಸ್ವತಂತ್ರವಾಗಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಾರೆ.",
                "state_angle": "ಗ್ರೇಟರ್ ಬೆಂಗಳೂರು ಪ್ರಾಧಿಕಾರ (GBA) ಮಸೂದೆ ಮತ್ತು ‘ಬ್ರ್ಯಾಂಡ್ ಬೆಂಗಳೂರು’ ನಗರ ಸಾರಿಗೆ ಏಕೀಕರಣ ಪ್ರಶ್ನೆಗಳಿಗೆ ಈ ಅಂಕಿಅಂಶ ಅತ್ಯಂತ ಪ್ರಸ್ತುತ.",
                "source": "ಪ್ರಜಾವಾಣಿ / MoHUA / BMRCL"
            },
            {
                "title": "ಮೇಕೆದಾಟು ಯೋಜನೆ ಮತ್ತು ಕಾವೇರಿ ಜಲ ವಿವಾದದ ಸಾಂವಿಧಾನಿಕ ಚೌಕಟ್ಟು",
                "why_in_news": "ಮೇಕೆದಾಟು ಸಮತೋಲನ (Balancing) ಜಲಾಶಯ ಯೋಜನೆಗೆ ಕೇಂದ್ರದ ಶಾಸನಬದ್ಧ ಪರಿಸರ ಅನುಮತಿ ನೀಡಬೇಕೆಂದು ಕರ್ನಾಟಕ ಸರ್ಕಾರ ಪುನರುಚ್ಚರಿಸಿದೆ.",
                "static_points": [
                    "<b>ಸ್ಥಳ:</b> ರಾಮನಗರ ಜಿಲ್ಲೆಯ ಕನಕಪುರ ಬಳಿ ಕಾವೇರಿ ಮತ್ತು ಅರ್ಕಾವತಿ ನದಿಗಳ ಸಂಗಮ ಪ್ರದೇಶ.",
                    "<b>ಉದ್ದೇಶ:</b> ಬೆಂಗಳೂರು ನಗರಕ್ಕೆ 4.75 ಟಿಎಂಸಿ ಕುಡಿಯುವ ನೀರು ಮತ್ತು 400 ಮೆಗಾವಾಟ್ ಜಲವಿದ್ಯುತ್ ಉತ್ಪಾದನೆ (ಒಟ್ಟು ಸಂಗ್ರಹ 67.16 ಟಿಎಂಸಿ).",
                    "<b>ಸಂವಿಧಾನದ ವಿಧಿ 262:</b> ಅಂತರರಾಜ್ಯ ನದಿ ನೀರು ವಿವಾದಗಳ ತೀರ್ಮಾನಕ್ಕೆ ಸಂಸತ್ತು ಕಾನೂನು ರೂಪಿಸಬಹುದು; ನ್ಯಾಯಾಲಯಗಳ ಅಧಿಕಾರ ವ್ಯಾಪ್ತಿ ನಿರ್ಬಂಧಿಸಬಹುದು.",
                    "<b>ಕಾವೇರಿ ಪ್ರಾಧಿಕಾರಗಳು:</b> ಸುಪ್ರೀಂ ಕೋರ್ಟ್ 2018ರ ತೀರ್ಪಿನನ್ವಯ ಕಾವೇರಿ ನೀರು ನಿರ್ವಹಣಾ ಪ್ರಾಧಿಕಾರ (CWMA) ಮತ್ತು ಕಾವೇರಿ ನೀರು ನಿಯಂತ್ರಣ ಸಮಿತಿ (CWRC) ರಚನೆ."
                ],
                "exam_points": [
                    "ಕಾವೇರಿ ಜಲ ವಿವಾದ ನ್ಯಾಯಾಧಿಕರಣ (CWDT) ರಚನೆ: 1990; ಅಂತಿಮ ತೀರ್ಪು: 2007.",
                    "ಸುಪ್ರೀಂ ಕೋರ್ಟ್ 2018ರ ತೀರ್ಪು: ಕರ್ನಾಟಕಕ್ಕೆ 284.75 ಟಿಎಂಸಿ (ಹೆಚ್ಚುವರಿ 14.75 ಟಿಎಂಸಿ), ತಮಿಳುನಾಡಿಗೆ 404.25 ಟಿಎಂಸಿ."
                ],
                "trap": "CWMA ಸಂವಿಧಾನಿಕ ಸಂಸ್ಥೆಯಲ್ಲ; ಇದು ಅಂತರರಾಜ್ಯ ನದಿ ನೀರು ವಿವಾದ ಕಾಯ್ದೆ 1956ರ ಅಡಿ ರಚಿಸಲಾದ ಶಾಸನಬದ್ಧ (Statutory) ಸಂಸ್ಥೆಯಾಗಿದೆ.",
                "state_angle": "ಕರ್ನಾಟಕದ ಪ್ರಮುಖ ಅಂತರರಾಜ್ಯ ನದಿ ವಿವಾದಗಳು: ಕಾವೇರಿ (ತಮಿಳುನಾಡು), ಕೃಷ್ಣಾ (ಆಂಧ್ರ/ತೆಲಂಗಾಣ), ಮಹದಾಯಿ (ಗೋವಾ/ಮಹಾರಾಷ್ಟ್ರ).",
                "source": "ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ತೀರ್ಪು / CWMA / ಪ್ರಜಾವಾಣಿ"
            }
        ],
        "oneliners": [
            "<b>ನವೆಂಬರ್ 14:</b> ಜವಾಹರಲಾಲ್ ನೆಹರೂ ಜನ್ಮದಿನ (ರಾಷ್ಟ್ರೀಯ ಮಕ್ಕಳ ದಿನಾಚರಣೆ).",
            "<b>ವಂದೇ ಭಾರತ್ ಎಕ್ಸ್‌ಪ್ರೆಸ್:</b> ದೇಶದ ಮೊದಲ ರೈಲು 2019 ಫೆಬ್ರವರಿಯಲ್ಲಿ (ನವದೆಹಲಿ-ವಾರಾಣಸಿ) ಆರಂಭ; ತಯಾರಿಕೆ: ಇಂಟೆಗ್ರಲ್ ಕೋಚ್ ಫ್ಯಾಕ್ಟರಿ (ICF), ಚೆನ್ನೈ.",
            "<b>ಕೊಂಕಣ ರೈಲ್ವೆ ನಿಗಮ:</b> 1990ರಲ್ಲಿ ಸ್ಥಾಪನೆ; ರೋಹಾ (ಮಹಾರಾಷ್ಟ್ರ)ದಿಂದ ತೋಕೂರು (ಕರ್ನಾಟಕ)ವರೆಗೆ 741 ಕಿ.ಮೀ. ಮಾರ್ಗ.",
            "<b>ನ್ಯಾಷನಲ್ ಏರ್ ಕ್ವಾಲಿಟಿ ಇಂಡೆಕ್ಸ್ (NAQI):</b> 2014ರಲ್ಲಿ CPCBಯಿಂದ ಆರಂಭ; 6 ವರ್ಗಗಳು ಮತ್ತು 8 ಪ್ರಮುಖ ಮಾಲಿನ್ಯಕಾರಕಗಳು (PM10, PM2.5, NO2, SO2, CO, O3, NH3, Pb)."
        ],
        "mcqs": [
            {
                "question": "ಕಾವೇರಿ ನದಿಯ ಕೆಳಗಿನ ಉಪನದಿಗಳಲ್ಲಿ ಯಾವುದು ಎಡದಂಡೆಯ (Left Bank) ಉಪನದಿಯಾಗಿದೆ?",
                "opt_a": "ಕಬಿನಿ",
                "opt_b": "ಹೇಮಾವತಿ",
                "opt_c": "ಭವಾನಿ",
                "opt_d": "ಲಕ್ಷ್ಮಣತೀರ್ಥ",
                "answer": "B",
                "explanation": "ಹೇಮಾವತಿ, ಹಾರಂಗಿ, ಶಿಂಷಾ ಮತ್ತು ಅರ್ಕಾವತಿ ಕಾವೇರಿಯ ಎಡದಂಡೆ ಉಪನದಿಗಳು. ಕಬಿನಿ, ಭವಾನಿ, ನೊಯ್ಯಲ್, ಅಮರಾವತಿ, ಲಕ್ಷ್ಮಣತೀರ್ಥ ಬಲದಂಡೆ ಉಪನದಿಗಳಾಗಿವೆ."
            },
            {
                "question": "ಮೆಟ್ರೊ ರೈಲು ಸುರಕ್ಷತಾ ಆಯುಕ್ತರು (CMRS) ಈ ಕೆಳಗಿನ ಯಾವ ಸಚಿವಾಲಯದ ಆಡಳಿತಾತ್ಮಕ ನಿಯಂತ್ರಣಕ್ಕೆ ಒಳಪಡುತ್ತಾರೆ?",
                "opt_a": "ಕೇಂದ್ರ ರೈಲ್ವೆ ಸಚಿವಾಲಯ",
                "opt_b": "ವಸತಿ ಮತ್ತು ನಗರ ವ್ಯವಹಾರಗಳ ಸಚಿವಾಲಯ",
                "opt_c": "ನಾಗರಿಕ ವಿಮಾನಯಾನ ಸಚಿವಾಲಯ",
                "opt_d": "ರಸ್ತೆ ಸಾರಿಗೆ ಮತ್ತು ಹೆದ್ದಾರಿ ಸಚಿವಾಲಯ",
                "answer": "C",
                "explanation": "CMRS ನಾಗರಿಕ ವಿಮಾನಯಾನ ಸಚಿವಾಲಯದ (Ministry of Civil Aviation) ರೈಲ್ವೆ ಸುರಕ್ಷತಾ ಆಯೋಗದ ಅಡಿಯಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಾರೆ. ಸ್ವತಂತ್ರ ತನಿಖೆ ಮತ್ತು ಸುರಕ್ಷತೆಗಾಗಿ ಇದನ್ನು ರೈಲ್ವೆ ಸಚಿವಾಲಯದಿಂದ ಪ್ರತ್ಯೇಕಿಸಲಾಗಿದೆ."
            }
        ]
    }


def generate_all_demo_pdfs():
    print("=" * 60)
    print("   GENERATING HIGH-YIELD STUDY MATERIAL PDFS")
    print("=" * 60)

    engine = PDFEngine()

    # 1. English Civils Vault PDF
    print("\n>>> 1. Compiling English 'The Civils Vault' PDF...")
    en_data = get_demo_english_data()
    en_pdf = engine.generate_english_pdf(en_data, "TheCivilsVault_Daily_Analysis.pdf")
    print(f"   [DONE] Generated: {en_pdf} ({os.path.getsize(en_pdf):,} bytes)")

    # 2. Kannada KPSC Insights PDF
    print("\n>>> 2. Compiling Kannada 'KPSCinsights' Prajavani PDF...")
    kn_data = get_demo_kannada_data()
    kn_pdf = engine.generate_kannada_pdf(kn_data, "KPSCinsights_Prajavani_Analysis.pdf")
    print(f"   [DONE] Generated: {kn_pdf} ({os.path.getsize(kn_pdf):,} bytes)")

    print("\n" + "=" * 60)
    print("   SUCCESS! Both study material PDFs generated cleanly.")
    print("=" * 60)
    return en_pdf, kn_pdf


if __name__ == "__main__":
    generate_all_demo_pdfs()
