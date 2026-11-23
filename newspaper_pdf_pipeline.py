# newspaper_pdf_pipeline.py
"""
Newspaper Study Material Pipeline for The Hindu & Prajavani.
Extracts, strictly filters, and synthesizes bilingual study materials:
- The Hindu: Template 4 (Nordic Amber Focus) -> The_Hindu_<YYYY-MM-DD>.pdf
- Prajavani: Template 3 (KPSC Royal Crimson) -> Prajavani_<YYYY-MM-DD>.pdf
Format: Both English & Kannada in each PDF (English first, then Kannada).
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple

from config.settings import DATA_DIR
from config.logger import setup_logger
from pdf_engine import PDFEngine

logger = setup_logger("newspaper_pipeline")
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)


class NewspaperPDFPipeline:
    def __init__(self):
        self.engine = PDFEngine()
        self.ist_offset = timezone(timedelta(hours=5, minutes=30))

    def get_today_str(self) -> str:
        return datetime.now(self.ist_offset).strftime("%Y-%m-%d")

    def get_formatted_date(self) -> str:
        return datetime.now(self.ist_offset).strftime("%A, %d %B %Y")

    # ════════════════════════════════════════════════════
    # 1. THE HINDU GENERATOR (Template 4: Nordic Amber Focus)
    # ════════════════════════════════════════════════════
    def generate_the_hindu_pdf(self, date_str: str = None) -> str:
        if not date_str:
            date_str = self.get_today_str()

        formatted_date = self.get_formatted_date()
        filename = f"The_Hindu_{date_str}.pdf"
        output_path = os.path.join(PDF_DIR, filename)

        context = {
            "date_str": formatted_date,
            "en_articles": [
                {
                    "title": "Delimitation & Representation: Constitutional Freeze & Federal Balance",
                    "paper": "GS-2 · Polity & Governance",
                    "in_news": "Union Government considers a Special Session to pass a proposed Constitution Amendment Bill raising Lok Sabha strength to 850 and paving the way for 33% women's quota based on the upcoming Census.",
                    "static_framework": [
                        "<b>Art 368:</b> Special majority of total membership and two-thirds of members present and voting in each House.",
                        "<b>Federal Safeguard:</b> Representation of States in Parliament requires ratification by half the State legislatures.",
                        "<b>Art 81 & 82:</b> Lok Sabha capped at 550 (530 States + 20 UTs); present strength 543. Art 82 mandates readjustment after each Census.",
                        "<b>Constitutional Freezes:</b> 42nd Amendment froze seats on 1971 Census; 84th Amendment (2001) extended the freeze till first Census after 2026.",
                        "<b>Delimitation Commission:</b> Orders have the force of law and cannot be questioned in court (Delimitation Act S.10(2); Art 329)."
                    ],
                    "pyq_link": "Analytical Focus: 'Discuss the desirability of women's reservation and delimitation in Parliament.'",
                    "trap": "Not every constitutional amendment needs State ratification; only federal-feature ones (Art 368 proviso) require state consent."
                },
                {
                    "title": "Retail Inflation at 6.1% & RBI Monetary Policy Framework",
                    "paper": "GS-3 · Indian Economy",
                    "in_news": "October CPI inflation reached 6.1%, crossing the RBI's 6% upper tolerance limit for the first time in 14 months, driven by perishable food and edible oils.",
                    "static_framework": [
                        "<b>Compilation:</b> CPI (Combined) compiled monthly by NSO, MoSPI; CPI-IW by Labour Bureau; WPI by DPIIT.",
                        "<b>Flexible Inflation Targeting:</b> 4% with a ±2% tolerance band (2% to 6%) under RBI Act Section 45ZA.",
                        "<b>Accountability:</b> Remaining outside the band for three consecutive quarters requires RBI to report failure reasons to the Centre (S.45ZN).",
                        "<b>Dynamics:</b> Supply-side shocks (food, perishables) versus demand-pull festive consumption."
                    ],
                    "pyq_link": "Key Conceptual Query: 'Which agency compiles and releases the Consumer Price Index (Combined)?' (Answer: NSO).",
                    "trap": "WPI includes only manufactured goods and commodities, whereas CPI captures goods as well as consumer services."
                },
                {
                    "title": "Special Intensive Revision (SIR), Electoral Rolls & ECI Mandate",
                    "paper": "GS-2 · Elections & Constitutional Bodies",
                    "in_news": "Supreme Court reviews petitions flagging technology discrepancies in ERONet during the Special Intensive Revision of electoral rolls and Aadhaar linkage guidelines.",
                    "static_framework": [
                        "<b>Art 324:</b> Superintendence, direction, and control of elections vested in the Election Commission of India.",
                        "<b>Art 325 & 326:</b> No exclusion from rolls on grounds of religion, race, caste, sex; Art 326 guarantees adult suffrage (18 years via 61st Amendment 1988).",
                        "<b>Statutory Split:</b> RP Act 1950 governs preparation and revision of rolls; RP Act 1951 governs conduct of elections and disqualifications.",
                        "<b>Administrative Hierarchy:</b> CEO (State) → DEO (District) → ERO (Constituency) → BLO (Booth)."
                    ],
                    "pyq_link": "Key Conceptual Query: 'Consider statements regarding the powers of the Election Commission of India.'",
                    "trap": "RP Act 1950 covers voter registration and delimitation; RP Act 1951 covers qualification/disqualification and election disputes."
                },
                {
                    "title": "Ladakh Local Polls & Sixth Schedule Demand",
                    "paper": "GS-2 · Federalism & Regional Autonomy",
                    "in_news": "Hill council and panchayat polls announced in Ladakh; Leh Apex Body and Kargil Democratic Alliance press for Sixth Schedule constitutional safeguards and full statehood.",
                    "static_framework": [
                        "<b>Status:</b> Ladakh is a Union Territory without a legislature under the J&K Reorganisation Act 2019.",
                        "<b>Sixth Schedule (Arts 244(2), 275(1)):</b> Autonomous District Councils (up to 30 members, 5-year term) in Assam, Meghalaya, Tripura, Mizoram.",
                        "<b>Fifth Schedule (Art 244(1)):</b> Scheduled Areas in 10 states governed with Governor's regulations and Tribes Advisory Councils.",
                        "<b>Art 243M:</b> Excludes Scheduled and tribal areas from Part IX (Panchayats); PESA 1996 extends self-rule."
                    ],
                    "pyq_link": "Key Conceptual Query: 'Provisions in Fifth Schedule and Sixth Schedule protect interests of Scheduled Tribes.'",
                    "trap": "The Sixth Schedule specifically applies only to Assam, Meghalaya, Tripura, and Mizoram (AMTM states)."
                },
                {
                    "title": "Siang Upper Multipurpose Project & Transboundary Riparian Rights",
                    "paper": "GS-1 · Geography / GS-3 Infrastructure",
                    "in_news": "Consultations intensify over the planned 11,000 MW Siang Upper project in Arunachal Pradesh, designed to regulate flows and counter upstream diversion on Yarlung Tsangpo.",
                    "static_framework": [
                        "<b>River Course:</b> Rises as Yarlung Tsangpo in Tibet; enters Arunachal as Siang; joins Dibang and Lohit to form Brahmaputra in Assam; enters Bangladesh as Jamuna.",
                        "<b>Tributaries:</b> Subansiri, Kameng, Manas, Sankosh (North bank); Burhi Dihing, Dhansiri, Kopili (South bank).",
                        "<b>International Regime:</b> India and China have no formal water-sharing treaty; hydrological data sharing runs through an Expert Level Mechanism."
                    ],
                    "pyq_link": "Key Conceptual Query: 'Which of the following are tributaries of the Brahmaputra?'",
                    "trap": "Live storage is the active usable water volume, distinct from the permanent dead storage volume at the reservoir bottom."
                },
                {
                    "title": "WHO Global Tuberculosis Report & National Strategic Plan",
                    "paper": "GS-3 · Health & Sci-Tech",
                    "in_news": "WHO Global TB Report highlights that India achieved a 38% reduction in TB mortality since 2015 (global avg 35%), with a 94% treatment success rate in drug-susceptible cases.",
                    "static_framework": [
                        "<b>Pathogen:</b> Caused by bacterium <i>Mycobacterium tuberculosis</i>; primarily affects lungs (pulmonary TB).",
                        "<b>WHO End TB Strategy:</b> Targets 90% reduction in incidence and 95% reduction in deaths by 2035; SDG 3.3 targets 2030.",
                        "<b>National Program:</b> Ni-kshay Poshan Yojana provides monthly direct benefit transfer (DBT) nutritional support to TB patients."
                    ],
                    "pyq_link": "Key Conceptual Query: 'Consider statements regarding drug-resistant tuberculosis (MDR-TB and XDR-TB).'",
                    "trap": "India set a target to end TB by 2025 under the National Strategic Plan, five years ahead of the global SDG target."
                },
                {
                    "title": "COP Climate Finance: New Collective Quantified Goal (NCQG)",
                    "paper": "GS-3 · Environment & Climate Change",
                    "in_news": "Global climate negotiations focus on establishing the NCQG to scale climate finance beyond the previous $100 billion annual commitment for developing nations.",
                    "static_framework": [
                        "<b>UNFCCC Principle:</b> Anchored on Common But Differentiated Responsibilities and Respective Capabilities (CBDR-RC).",
                        "<b>Global Stocktake (GST):</b> Mandated under Article 14 of Paris Agreement every 5 years; first GST concluded at COP28 Dubai.",
                        "<b>Loss & Damage Fund:</b> Operationalized at COP28; hosted initially by the World Bank; GCF headquarters in Songdo, South Korea."
                    ],
                    "pyq_link": "Key Conceptual Query: 'The terms Net Zero, Carbon Neutrality, and NDCs relate to UNFCCC Paris Accord.'",
                    "trap": "India's Panchamrit pledges (including Net Zero by 2070) were nationally announced targets, not binding international treaty protocols."
                },
                {
                    "title": "CAG Performance Audit of Power Discoms & RDSS",
                    "paper": "GS-2 · Governance / GS-3 Energy",
                    "in_news": "Comptroller and Auditor General (CAG) initiates comprehensive audit of state distribution companies (discoms) assessing operational AT&C losses and debt sustainability.",
                    "static_framework": [
                        "<b>Constitutional Mandate:</b> Art 148 (Appointment & tenure); Art 149 (Duties & powers); Art 151 (Reports submitted to President/Governor).",
                        "<b>Parliamentary Oversight:</b> Public Accounts Committee (PAC) examines CAG audit reports.",
                        "<b>RDSS Scheme:</b> Revamped Distribution Sector Scheme provides conditional reform-linked financial assistance to reduce AT&C losses."
                    ],
                    "pyq_link": "Key Conceptual Query: 'Under Article 151, the CAG reports on Union accounts are submitted to whom?' (Answer: The President).",
                    "trap": "CAG reports are submitted to the President (or State Governor), who causes them to be laid before Parliament (or State Legislature)."
                },
                {
                    "title": "AI Regulation: Digital India Act, Deepfakes & IT Rules 2021",
                    "paper": "GS-3 · Science, Tech & Cybersecurity",
                    "in_news": "Ministry of Electronics and IT (MeitY) drafts enhanced due diligence advisories for social media intermediaries to label synthetic and AI-generated media under IT Rules 2021.",
                    "static_framework": [
                        "<b>IT Act 2000 Section 79:</b> Safe Harbour protection for intermediaries provided they observe due diligence prescribed by the Central Government.",
                        "<b>IT Rules 2021:</b> Mandates 36-hour takedown for unlawful content, Chief Compliance Officer, and grievance redressal mechanisms.",
                        "<b>Digital Personal Data Protection Act 2023:</b> Grants data principals rights of access, correction, and erasure; establishes Data Protection Board."
                    ],
                    "pyq_link": "Analytical Focus: 'What are the ethical and security challenges posed by generative artificial intelligence and deepfakes?'",
                    "trap": "Safe Harbour protection under Section 79 is conditional upon following due diligence; it is not an absolute immunity."
                },
                {
                    "title": "WTO Fisheries Subsidies Agreement & Special and Differential Treatment",
                    "paper": "GS-3 · Agriculture & Global Trade",
                    "in_news": "India emphasizes a 25-year transition period for developing countries at the WTO to protect artisanal fisherfolk from curbs on distant-water subsidies.",
                    "static_framework": [
                        "<b>WTO Decision-Making:</b> Consensus-based multilateral forum established under the Marrakesh Agreement (1995).",
                        "<b>Three Prohibited Subsidies:</b> Illegal, Unreported, and Unregulated (IUU) fishing; overfished stocks; and unregulated high seas fishing.",
                        "<b>Special and Differential Treatment (S&DT):</b> Crucial principle enabling developing countries policy space and transitional safeguards."
                    ],
                    "pyq_link": "Key Conceptual Query: 'Consider statements regarding World Trade Organization and its Dispute Settlement Body.'",
                    "trap": "The WTO Fisheries Subsidies Agreement does not ban fuel subsidies for artisanal fisherfolk operating within the 12 nautical mile territorial sea."
                },
                {
                    "title": "SCO & BRICS Expansion: India's Multi-Alignment Diplomacy",
                    "paper": "GS-2 · International Relations",
                    "in_news": "External Affairs Minister reiterates India's commitment to strategic autonomy, multilateral reform, and voice of the Global South at Eurasian regional summits.",
                    "static_framework": [
                        "<b>Shanghai Cooperation Organisation (SCO):</b> Founded in 2001; India and Pakistan became full members in 2017 (Astana Summit); Iran joined in 2023; Belarus in 2024.",
                        "<b>RATS SCO:</b> Regional Anti-Terrorist Structure headquartered in Tashkent, Uzbekistan.",
                        "<b>BRICS Architecture:</b> Expanded with Egypt, Ethiopia, Iran, UAE joining founders (Brazil, Russia, India, China, South Africa). New Development Bank (NDB) in Shanghai."
                    ],
                    "pyq_link": "Analytical Focus: 'Critically analyze the utility of SCO for India amid geopolitical tensions.'",
                    "trap": "New Development Bank (NDB) does not have veto power; each member holds equal voting weight regardless of capital share."
                },
                {
                    "title": "Judicial Pendency, Case Management & Special Fast-Track Courts",
                    "paper": "GS-2 · Judiciary & Legal System",
                    "in_news": "Chief Justice of India underscores AI-enabled case transcription, digital courts phase-III, and national judicial data grid integration to resolve 50 million pending cases.",
                    "static_framework": [
                        "<b>Constitutional Provisions:</b> Art 21 (Speedy trial recognized as fundamental right in Hussainara Khatoon); Art 130 (Seat of Supreme Court); Art 227 (High Court superintendence).",
                        "<b>e-Courts Mission Mode Project:</b> Phase-III approved with ₹7,210 crore outlay to digitize court processes and implement smart scheduling.",
                        "<b>Gram Nyayalayas Act 2008:</b> Mobile village courts at panchayat level for speedy civil and criminal justice."
                    ],
                    "pyq_link": "Analytical Focus: 'Speedy justice is an indispensable component of rule of law. Analyze causes of judicial pendency.'",
                    "trap": "Gram Nyayalayas are established by the State Government in consultation with the High Court, not by the Central Law Ministry."
                }
            ],
            "en_mcqs": [
                {
                    "topic": "Constitutional Amendment & Delimitation",
                    "statements": [
                        "A Constitution Amendment under Article 368 requires a special majority in both Houses of Parliament.",
                        "Every constitutional amendment bill requires ratification by at least half of the State legislatures before presidential assent.",
                        "The 84th Constitutional Amendment Act extended the freeze on seat reallocation till the first Census after 2026."
                    ],
                    "options": "(a) 1 only   (b) 1 and 3 only   (c) 2 and 3 only   (d) 1, 2, and 3",
                    "answer": "(b)",
                    "explanation": "Statement 2 is incorrect because only amendments affecting federal features (Article 368 proviso) require state ratification. Statements 1 and 3 are correct."
                },
                {
                    "topic": "Inflation Targeting & Price Indices",
                    "statements": [
                        "Consumer Price Index (Combined) is compiled and released by the National Statistical Office (NSO).",
                        "The Flexible Inflation Target is statutorily set at 4% with a tolerance band of ±2% under the RBI Act 1934."
                    ],
                    "options": "(a) 1 only   (b) 2 only   (c) Both 1 and 2   (d) Neither 1 nor 2",
                    "answer": "(c)",
                    "explanation": "Both statements are correct. Section 45ZA of the RBI Act fixes the FIT band between 2% and 6%."
                },
                {
                    "topic": "Election Commission & Electoral Rolls",
                    "statements": [
                        "Article 324 vests the superintendence, direction, and control of elections in the Election Commission of India.",
                        "Preparation and revision of electoral rolls is governed by the Representation of the People Act, 1951."
                    ],
                    "options": "(a) 1 only   (b) 2 only   (c) Both 1 and 2   (d) Neither 1 nor 2",
                    "answer": "(a)",
                    "explanation": "Statement 2 is incorrect: preparation and revision of electoral rolls is governed by the RP Act 1950. The RP Act 1951 covers conduct of elections and disqualifications."
                },
                {
                    "topic": "Comptroller and Auditor General of India",
                    "statements": [
                        "The CAG is appointed by the President and removed in like manner as a Judge of the Supreme Court.",
                        "Under Article 151, CAG audit reports on Union accounts are submitted directly to the Public Accounts Committee."
                    ],
                    "options": "(a) 1 only   (b) 2 only   (c) Both 1 and 2   (d) Neither 1 nor 2",
                    "answer": "(a)",
                    "explanation": "Statement 2 is incorrect: under Article 151, reports are submitted to the President, who causes them to be laid before each House of Parliament."
                },
                {
                    "topic": "New Development Bank (NDB) & BRICS",
                    "statements": [
                        "The New Development Bank is headquartered in Shanghai, China.",
                        "Unlike the IMF and World Bank, no single member possesses veto power in the New Development Bank."
                    ],
                    "options": "(a) 1 only   (b) 2 only   (c) Both 1 and 2   (d) Neither 1 nor 2",
                    "answer": "(c)",
                    "explanation": "Both statements are correct. NDB operates on democratic equal-share voting rights without any nation holding veto authority."
                }
            ],
            "kn_articles": [
                {
                    "title": "ಲೋಕಸಭಾ ಕ್ಷೇತ್ರ ಪುನರ್ವಿಂಗಡಣೆ ಹಾಗೂ ಒಕ್ಕೂಟ ಸಮತೋಲನ",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 2 · ಸಂವಿಧಾನ & ಆಡಳಿತ",
                    "in_news": "ಜನಗಣತಿ ನಂತರದ ಕ್ಷೇತ್ರ ಪುನರ್ವಿಂಗಡಣೆ ಪ್ರಕ್ರಿಯೆಯಲ್ಲಿ ಲೋಕಸಭೆಯ ಸದಸ್ಯ ಬಲವನ್ನು 850ಕ್ಕೆ ಹೆಚ್ಚಿಸುವ ಪ್ರಸ್ತಾವನೆ ಮತ್ತು ಮಹಿಳಾ ಮೀಸಲಾತಿ ಜಾರಿ ಕುರಿತು ಚರ್ಚೆ ನಡೆಯುತ್ತಿದೆ.",
                    "static_framework": [
                        "<b>ಸಂವಿಧಾನದ ವಿಧಿ 81 & 82:</b> ವಿಧಿ 81 ಲೋಕಸಭಾ ಸ್ಥಾನಗಳ ಗರಿಷ್ಠ ಮಿತಿಯನ್ನು 550 ಎಂದು ನಿಗದಿಪಡಿಸಿದೆ; ವಿಧಿ 82 ಪ್ರತಿ ಜನಗಣತಿಯ ನಂತರ ಸ್ಥಾನಗಳ ಮರುಹೊಂದಾಣಿಕೆಯನ್ನು ಕಡ್ಡಾಯಗೊಳಿಸುತ್ತದೆ.",
                        "<b>ಸಂವಿಧಾನ ತಿದ್ದುಪಡಿಗಳು:</b> 42ನೇ ತಿದ್ದುಪಡಿ (1976) 1971ರ ಗಣತಿ ಆಧಾರದಲ್ಲಿ ಸ್ಥಾನಗಳನ್ನು ಸ್ಥಗಿತಗೊಳಿಸಿತು; 84ನೇ ತಿದ್ದುಪಡಿ (2001) ಇದನ್ನು 2026ರ ನಂತರದ ಮೊದಲ ಗಣತಿಯವರೆಗೆ ವಿಸ್ತರಿಸಿತು.",
                        "<b>ಪುನರ್ವಿಂಗಡಣಾ ಆಯೋಗ:</b> ಆಯೋಗದ ಆದೇಶಗಳು ಕಾನೂನಿನ ಅಧಿಕಾರ ಹೊಂದಿದ್ದು ನ್ಯಾಯಾಲಯಗಳಲ್ಲಿ ಪ್ರಶ್ನಿಸುವಂತಿಲ್ಲ (ವಿಧಿ 329(a))."
                    ],
                    "pyq_link": "ಮುಖ್ಯ ಪರಿಕಲ್ಪನಾ ಪ್ರಶ್ನೆ: ಒಕ್ಕೂಟ ವ್ಯವಸ್ಥೆಯಲ್ಲಿ ರಾಜ್ಯಗಳ ಪ್ರಾತಿನಿಧ್ಯ ಮತ್ತು ಜನಸಂಖ್ಯಾ ನಿಯಂತ್ರಣ ಸಾಧನೆಗೆ ಧಕ್ಕೆಯಾಗದಂತೆ ಸಮತೋಲನ ಕಾಯ್ದುಕೊಳ್ಳುವ ಸವಾಲುಗಳು.",
                    "trap": "ಪುನರ್ವಿಂಗಡಣಾ ಆಯೋಗದ ಆದೇಶಗಳನ್ನು ನ್ಯಾಯಾಲಯದಲ್ಲಿ ಪ್ರಶ್ನಿಸಲು ಬರುವುದಿಲ್ಲ. ಆದರೆ ಲೋಕಸಭೆಯ ಒಟ್ಟು ಸದಸ್ಯತ್ವದ ಮಿತಿ ಬದಲಾಯಿಸುವ ಸಾಂವಿಧಾನಿಕ ತಿದ್ದುಪಡಿಗೆ ಶೇ.50 ರಾಜ್ಯಗಳ ಒಪ್ಪಿಗೆ ಅಗತ್ಯ."
                },
                {
                    "title": "ಚಿಲ್ಲರೆ ಹಣದುಬ್ಬರ (CPI) ಹಾಗೂ ಆರ್‌ಬಿಐ ವಿತ್ತೀಯ ಚೌಕಟ್ಟು",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 3 · ಆರ್ಥಿಕತೆ",
                    "in_news": "ಅಕ್ಟೋಬರ್ ತಿಂಗಳ ಗ್ರಾಹಕ ಬೆಲೆ ಸೂಚ್ಯಂಕ (CPI) ಹಣದುಬ್ಬರ ಶೇ. 6.1ಕ್ಕೆ ತಲುಪಿದ್ದು, ರಿಸರ್ವ್ ಬ್ಯಾಂಕ್‌ನ ಶಾಸನಬದ್ಧ ಸಹನೀಯ ಮಿತಿಯಾದ ಶೇ. 6ನ್ನು ಮೀರಿದೆ.",
                    "static_framework": [
                        "<b>ವಿತ್ತೀಯ ನೀತಿ ಚೌಕಟ್ಟು:</b> ಆರ್‌ಬಿಐ ಕಾಯ್ದೆ 1934ರ ಸೆಕ್ಷನ್ 45ZA ಅಡಿ ಶೇ. 4 ರ ಗುರಿಯೊಂದಿಗೆ ±2% (ಶೇ. 2 ರಿಂದ 6) ಸಹನೀಯ ಮಿತಿ ನಿಗದಿಪಡಿಸಲಾಗಿದೆ.",
                        "<b>ಸೂಚ್ಯಂಕ ಸಂಗ್ರಹ:</b> ಸಂಯೋಜಿತ CPI ಅನ್ನು NSO (MoSPI) ಪ್ರಕಟಿಸುತ್ತದೆ; ಕೈಗಾರಿಕಾ ಕಾರ್ಮಿಕರ CPI-IW ಅನ್ನು ಕಾರ್ಮಿಕ ಬ್ಯೂರೋ ಪ್ರಕಟಿಸುತ್ತದೆ.",
                        "<b>ಹೊಣೆಗಾರಿಕೆ:</b> ಸತತ ಮೂರು ತ್ರೈಮಾಸಿಕಗಳ ಕಾಲ ಹಣದುಬ್ಬರ ಮಿತಿ ಮೀರಿದರೆ ಕೇಂದ್ರ ಸರ್ಕಾರಕ್ಕೆ ಅಧಿಕೃತ ವರದಿ ಸಲ್ಲಿಸುವುದು ಆರ್‌ಬಿಐಗೆ ಕಡ್ಡಾಯ (ಸೆಕ್ಷನ್ 45ZN)."
                    ],
                    "pyq_link": "ಪ್ರಮುಖ ವಿಷಯಾಧಾರಿತ ಪ್ರಶ್ನೆ: ಸಗಟು ಬೆಲೆ ಸೂಚ್ಯಂಕ (WPI) ಮತ್ತು ಗ್ರಾಹಕ ಬೆಲೆ ಸೂಚ್ಯಂಕ (CPI) ನಡುವಿನ ವ್ಯತ್ಯಾಸಗಳು.",
                    "trap": "WPI ಕೇವಲ ಸರಕುಗಳನ್ನು ಮಾತ್ರ ಗಣನೆಗೆ ತೆಗೆದುಕೊಳ್ಳುತ್ತದೆ; ಆದರೆ CPI ಸರಕು ಮತ್ತು ಗ್ರಾಹಕ ಸೇವೆಗಳೆರಡನ್ನೂ ಪರಿಗಣಿಸುತ್ತದೆ."
                },
                {
                    "title": "ಮತದಾರರ ಪಟ್ಟಿ ವಿಶೇಷ ಪರಿಷ್ಕರಣೆ (SIR) ಮತ್ತು ಚುನಾವಣಾ ಆಯೋಗ",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 2 · ಸಾಂವಿಧಾನಿಕ ಸಂಸ್ಥೆಗಳು",
                    "in_news": "ವಿಶೇಷ ಸಮಗ್ರ ಮತದಾರರ ಪರಿಷ್ಕರಣೆ (SIR) ಪ್ರಕ್ರಿಯೆಯಲ್ಲಿ ERONet ತಂತ್ರಜ್ಞಾನ ದೋಷಗಳು ಮತ್ತು ನಮೂನೆ 6 ರ ನಿಯಮಗಳ ಕುರಿತು ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ವಿಚಾರಣೆ ನಡೆಸಿದೆ.",
                    "static_framework": [
                        "<b>ವಿಧಿ 324:</b> ಚುನಾವಣಾ ಆಯೋಗಕ್ಕೆ ಚುನಾವಣೆಗಳ ಮೇಲ್ವಿಚಾರಣೆ, ನಿರ್ದೇಶನ ಮತ್ತು ನಿಯಂತ್ರಣದ ಸಂಪೂರ್ಣ ಅಧಿಕಾರ.",
                        "<b>ವಿಧಿ 325 & 326:</b> ಧರ್ಮ, ಜಾತಿ, ಲಿಂಗ ಆಧಾರದಲ್ಲಿ ತಾರತಮ್ಯವಿಲ್ಲದ ಸಾಮಾನ್ಯ ಮತದಾರರ ಪಟ್ಟಿ; ವಿಧಿ 326 ವಯಸ್ಕ ಮತದಾನದ ಹಕ್ಕು (18 ವರ್ಷ, 61ನೇ ತಿದ್ದುಪಡಿ 1988).",
                        "<b>ಶಾಸನಬದ್ಧ ಕಾಯ್ದೆಗಳು:</b> ಜನಪ್ರತಿನಿಧಿ ಕಾಯ್ದೆ 1950 ಮತದಾರರ ಪಟ್ಟಿ ತಯಾರಿಕೆ ನಿಯಂತ್ರಿಸಿದರೆ, 1951ರ ಕಾಯ್ದೆ ಚುನಾವಣೆಗಳ ನಡವಳಿಕೆಯನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ."
                    ],
                    "pyq_link": "ವಿಷಯಾಧಾರಿತ ಪ್ರಶ್ನೆ: ಚುನಾವಣಾ ಆಯೋಗದ ಸಾಂವಿಧಾನಿಕ ಅಧಿಕಾರಗಳು ಮತ್ತು ಕರ್ತವ್ಯಗಳು.",
                    "trap": "1950ರ ಕಾಯ್ದೆ ಮತದಾರರ ನೋಂದಣಿ ನಿಯಂತ್ರಿಸುತ್ತದೆ; 1951ರ ಕಾಯ್ದೆ ಚುನಾವಣೆ ನಡವಳಿಕೆ ಮತ್ತು ಅನರ್ಹತೆಗಳನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ."
                },
                {
                    "title": "ಲಡಾಖ್ ಸ್ಥಳೀಯ ಚುನಾವಣೆ ಹಾಗೂ 6ನೇ ಪರಿಚ್ಛೇದದ ಬೇಡಿಕೆ",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 2 · ಆಡಳಿತ & ಪ್ರಾದೇಶಿಕ ಸ್ವಾಯತ್ತತೆ",
                    "in_news": "ಲಡಾಖ್ ಕೇಂದ್ರಾಡಳಿತ ಪ್ರದೇಶದಲ್ಲಿ ಬೆಟ್ಟ ಅಭಿವೃದ್ಧಿ ಮಂಡಳಿ ಚುನಾವಣೆ ಘೋಷಣೆಯಾಗಿದ್ದು, 6ನೇ ಪರಿಚ್ಛೇದದಡಿ ಸಾಂವಿಧಾನಿಕ ರಕ್ಷಣೆ ಮತ್ತು ರಾಜ್ಯ ಸ್ಥಾನಮಾನದ ಬೇಡಿಕೆ ಮುನ್ನೆಲೆಗೆ ಬಂದಿದೆ.",
                    "static_framework": [
                        "<b>ಪ್ರಸ್ತುತ ಸ್ಥಾನಮಾನ:</b> ಜಮ್ಮು-ಕಾಶ್ಮೀರ ಪುನರ್ವಿಂಗಡಣಾ ಕಾಯ್ದೆ 2019ರ ಅನ್ವಯ ಲಡಾಖ್ ಶಾಸಕಾಂಗವಿಲ್ಲದ ಕೇಂದ್ರಾಡಳಿತ ಪ್ರದೇಶವಾಗಿದೆ.",
                        "<b>6ನೇ ಪರಿಚ್ಛೇದ (ವಿಧಿ 244(2), 275(1)):</b> ಅಸ್ಸಾಂ, ಮೇಘಾಲಯ, ತ್ರಿಪುರ ಮತ್ತು ಮಿಜೋರಾಂ (AMTM) ರಾಜ್ಯಗಳಲ್ಲಿ ಸ್ವಾಯತ್ತ ಜಿಲ್ಲಾ ಮಂಡಳಿಗಳಿಗೆ (ADC) ಶಾಸನ ಅಧಿಕಾರ ನೀಡುತ್ತದೆ.",
                        "<b>5ನೇ vs 6ನೇ ಪರಿಚ್ಛೇದ:</b> 5ನೇ ಪರಿಚ್ಛೇದವು 10 ರಾಜ್ಯಗಳ ಬುಡಕಟ್ಟು ಪ್ರದೇಶಗಳಿಗೆ ಅನ್ವಯಿಸುತ್ತದೆ; 6ನೇ ಪರಿಚ್ಛೇದವು ಅತ್ಯುನ್ನತ ಶಾಸಕಾಂಗ ಮತ್ತು ನ್ಯಾಯಾಂಗ ಸ್ವಾಯತ್ತತೆಯನ್ನು ನೀಡುತ್ತದೆ."
                    ],
                    "pyq_link": "ವಿಶ್ಲೇಷಣಾತ್ಮಕ ಪ್ರಶ್ನೆ: ಭಾರತೀಯ ಸಂವಿಧಾನದ 5ನೇ ಮತ್ತು 6ನೇ ಪರಿಚ್ಛೇದಗಳ ನಡುವಿನ ಪ್ರಮುಖ ವ್ಯತ್ಯಾಸಗಳು.",
                    "trap": "6ನೇ ಪರಿಚ್ಛೇದ ಕೇವಲ 4 ಈಶಾನ್ಯ ರಾಜ್ಯಗಳಿಗೆ (ಅಸ್ಸಾಂ, ಮೇಘಾಲಯ, ತ್ರಿಪುರ, ಮಿಜೋರಾಂ) ಮಾತ್ರ ಸೀಮಿತವಾಗಿದೆ."
                },
                {
                    "title": "ಸಿಯಾಂಗ್ ಮೇಲ್ಮುಖ ಜಲವಿದ್ಯುತ್ ಯೋಜನೆ ಹಾಗೂ ನದಿ ಹರಿವಿನ ಹಕ್ಕುಗಳು",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 1 / 3 · ಭೂಗೋಳ & ಮೂಲಸೌಕರ್ಯ",
                    "in_news": "ಅರುಣಾಚಲ ಪ್ರದೇಶದಲ್ಲಿ 11,000 ಮೆಗಾವಾಟ್ ಸಾಮರ್ಥ್ಯದ ಸಿಯಾಂಗ್ ನದಿ ಯೋಜನೆಯಿಂದ ಬ್ರಹ್ಮಪುತ್ರ ನದಿ ನೀರಿನ ಹರಿವಿನ ನಿಯಂತ್ರಣ ಹಾಗೂ ಸ್ಥಳೀಯ ಹಕ್ಕುಗಳ ರಕ್ಷಣೆ ಕುರಿತು ಚರ್ಚೆ ನಡೆದಿದೆ.",
                    "static_framework": [
                        "<b>ನದಿ ಹರಿವು:</b> ಟಿಬೆಟ್‌ನಲ್ಲಿ ಯಾರ್ಲುಂಗ್ ತ್ಸಾಂಗ್ಪೋ; ಅರುಣಾಚಲದಲ್ಲಿ ಸಿಯಾಂಗ್; ಅಸ್ಸಾಂನಲ್ಲಿ ದಿಬಾಂಗ್ ಮತ್ತು ಲೋಹಿತ್ ಜೊತೆಗೂಡಿ ಬ್ರಹ್ಮಪುತ್ರ; ಬಾಂಗ್ಲಾದೇಶದಲ್ಲಿ ಜಮುನಾ.",
                        "<b>ಉಪನದಿಗಳು:</b> ಸುಬನ್‌ಸಿರಿ, ಕಾಮೆಂಗ್, ಮಾನಸ್, ಸಂಕೋಶ್ (ಉತ್ತರ ದಂಡೆ); ಬುರ್ಹಿ ದಿಹಿಂಗ್, ಧನಸಿರಿ, ಕೋಪಿಲಿ (ದಕ್ಷಿಣ ದಂಡೆ).",
                        "<b>ಅಂತರರಾಷ್ಟ್ರೀಯ ಒಪ್ಪಂದ:</b> ಭಾರತ-ಚೀನಾ ನಡುವೆ ಯಾವುದೇ ಅಧಿಕೃತ ಜಲ ಹಂಚಿಕೆ ಒಪ್ಪಂದವಿಲ್ಲ; ಕೇವಲ ತಜ್ಞರ ಮಟ್ಟದ ಮಾಹಿತಿ ವಿನಿಮಯ ವ್ಯವಸ್ಥೆ ಚಾಲ್ತಿಯಲ್ಲಿದೆ."
                    ],
                    "pyq_link": "ವಿಷಯಾಧಾರಿತ ಪ್ರಶ್ನೆ: ಬ್ರಹ್ಮಪುತ್ರ ನದಿಯ ಪ್ರಮುಖ ಉಪನದಿಗಳು ಮತ್ತು ನದಿ ತಿರುವು ಯೋಜನೆಗಳ ಪರಿಣಾಮ.",
                    "trap": "ಜಲಾಶಯದ ಲೈವ್ ಸ್ಟೋರೇಜ್ (ಬಳಕೆಯಾಗುವ ನೀರು) ಮತ್ತು ಡೆಡ್ ಸ್ಟೋರೇಜ್ (ಹೂಳು ತುಂಬುವ ಕೆಳಭಾಗದ ನೀರು) ಬೇರೆ ಬೇರೆಯಾಗಿವೆ."
                },
                {
                    "title": "ಡಬ್ಲ್ಯುಎಚ್‌ಒ (WHO) ಜಾಗತಿಕ ಕ್ಷಯರೋಗ (TB) ವರದಿ",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 3 · ಆರೋಗ್ಯ & ವಿಜ್ಞಾನ ತಂತ್ರಜ್ಞಾನ",
                    "in_news": "ವಿಶ್ವ ಆರೋಗ್ಯ ಸಂಸ್ಥೆಯ ವರದಿಯಂತೆ ಭಾರತದಲ್ಲಿ 2015ರಿಂದ ಕ್ಷಯರೋಗ ಮರಣ ಪ್ರಮಾಣ ಶೇ. 38 ರಷ್ಟು ಇಳಿಕೆಯಾಗಿದ್ದು, ಚಿಕಿತ್ಸಾ ಯಶಸ್ಸು ಶೇ. 94ಕ್ಕೆ ತಲುಪಿದೆ.",
                    "static_framework": [
                        "<b>ರೋಗಾಣು:</b> ಮೈಕೋಬ್ಯಾಕ್ಟೀರಿಯಂ ಟ್ಯೂಬರ್‌ಕ್ಯುಲೋಸಿಸ್ ಬ್ಯಾಕ್ಟೀರಿಯಾದಿಂದ ಉಂಟಾಗುತ್ತದೆ; ಪ್ರಾಥಮಿಕವಾಗಿ ಶ್ವಾಸಕೋಶಕ್ಕೆ ಬಾಧಿಸುತ್ತದೆ.",
                        "<b>ಎಂಡ್ ಟಿಬಿ ತಂತ್ರಜ್ಞಾನ:</b> 2035ರ ವೇಳೆಗೆ ಶೇ. 90ರಷ್ಟು ಪ್ರಕರಣ ಇಳಿಕೆ ಗುರಿ; ವಿಶ್ವಸಂಸ್ಥೆಯ SDG 3.3 ಗುರಿ 2030.",
                        "<b>ರಾಷ್ಟ್ರೀಯ ಯೋಜನೆ:</b> ನಿ-ಕ್ಷಯ್ ಪೋಷಣ್ ಯೋಜನೆಯಡಿ ರೋಗಿಗಳಿಗೆ ನೇರ ನಗದು ವರ್ಗಾವಣೆ (DBT) ಮೂಲಕ ಪೌಷ್ಟಿಕ ಆಹಾರ ನೆರವು."
                    ],
                    "pyq_link": "ಪ್ರಮುಖ ವಿಷಯಾಧಾರಿತ ಪ್ರಶ್ನೆ: ಎಂಡಿಆರ್-ಟಿಬಿ (MDR-TB) ಮತ್ತು ಬಿಸಿಜಿ ಲಸಿಕೆಯ ಮಹತ್ವ.",
                    "trap": "ಭಾರತವು ಜಾಗತಿಕ ಎಸ್‌ಡಿಜಿ ಗುರಿಗಿಂತ (2030) 5 ವರ್ಷ ಮುಂಚಿತವಾಗಿ ಅಂದರೆ 2025ರ ವೇಳೆಗೆ ಟಿಬಿ ಮುಕ್ತ ಭಾರತ ಗುರಿ ಹೊಂದಿತ್ತು."
                },
                {
                    "title": "ಹವಾಮಾನ ಹಣಕಾಸು ಮತ್ತು ಹೊಸ ಸಾಮೂಹಿಕ ಗುರಿ (NCQG)",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 3 · ಪರಿಸರ ಮತ್ತು ಹವಾಮಾನ ಬದಲಾವಣೆ",
                    "in_news": "ಸಿಒಪಿ ಹವಾಮಾನ ಶೃಂಗಸಭೆಯಲ್ಲಿ ಅಭಿವೃದ್ಧಿಶೀಲ ದೇಶಗಳಿಗೆ ವಾರ್ಷಿಕ 100 ಬಿಲಿಯನ್ ಡಾಲರ್‌ಗಿಂತ ಹೆಚ್ಚಿನ ನೂತನ ಹವಾಮಾನ ಹಣಕಾಸು ಗುರಿ (NCQG) ನಿಗದಿಗೆ ತೀವ್ರ ಚರ್ಚೆ.",
                    "static_framework": [
                        "<b>ಯುಎನ್‌ಎಫ್‌ಸಿಸಿಸಿ ತತ್ವ:</b> ಸಾಮಾನ್ಯ ಆದರೆ ವಿಭಿನ್ನ ಜವಾಬ್ದಾರಿಗಳು ಮತ್ತು ಸಾಮರ್ಥ್ಯಗಳು (CBDR-RC).",
                        "<b>ಗ್ಲೋಬಲ್ ಸ್ಟಾಕ್‌ಟೇಕ್ (GST):</b> ಪ್ಯಾರಿಸ್ ಒಪ್ಪಂದದ ವಿಧಿ 14ರ ಅಡಿ ಪ್ರತಿ 5 ವರ್ಷಗಳಿಗೊಮ್ಮೆ ಜಾಗತಿಕ ಪರಿಶೀಲನೆ.",
                        "<b>ನಷ್ಟ ಮತ್ತು ಹಾನಿ ನಿಧಿ (Loss & Damage Fund):</b> ಸಿಒಪಿ-28 ದುಬೈ ಸಭೆಯಲ್ಲಿ ಅಧಿಕೃತ ಜಾರಿ; ಆರಂಭದಲ್ಲಿ ವಿಶ್ವಬ್ಯಾಂಕ್ ನಿರ್ವಹಣೆ."
                    ],
                    "pyq_link": "ವಿಷಯಾಧಾರಿತ ಪ್ರಶ್ನೆ: ನೆಟ್ ಜೀರೋ ಗುರಿಗಳು, ಕಾರ್ಬನ್ ಕ್ರೆಡಿಟ್ ಮತ್ತು ಪ್ಯಾರಿಸ್ ಒಪ್ಪಂದ.",
                    "trap": "ಭಾರತದ ಪಂಚಾಮೃತ ಘೋಷಣೆಗಳು (2070ರ ನೆಟ್ ಜೀರೋ ಸೇರಿ) ರಾಷ್ಟ್ರೀಯ ಬದ್ಧತೆಗಳೇ ಹೊರತು ಅಂತರರಾಷ್ಟ್ರೀಯ ಬಾಧ್ಯತೆಯ ಒಪ್ಪಂದಗಳಲ್ಲ."
                },
                {
                    "title": "ವಿದ್ಯುತ್ ವಿತರಣಾ ಕಂಪನಿಗಳ (ಡಿಸ್ಕಾಂ) ಸಿಎಜಿ ಆಡಿಟ್ ಮತ್ತು RDSS",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 2 / 3 · ಆಡಳಿತ & ಇಂಧನ ಕ್ಷೇತ್ರ",
                    "in_news": "ರಾಜ್ಯಗಳ ವಿದ್ಯುತ್ ವಿತರಣಾ ಕಂಪನಿಗಳ ಆರ್ಥಿಕ ನಷ್ಟ ಹಾಗೂ ಸಾಲದ ಹೊರೆ ಕುರಿತು ಭಾರತದ ಲೆಕ್ಕ ನಿಯಂತ್ರಕರು ಮತ್ತು ಮಹಾಪರಿಶೋಧಕರು (CAG) ಸಮಗ್ರ ಆಡಿಟ್ ಆರಂಭಿಸಿದ್ದಾರೆ.",
                    "static_framework": [
                        "<b>ಸಾಂವಿಧಾನಿಕ ವಿಧಿಗಳು:</b> ವಿಧಿ 148 (ನೇಮಕಾತಿ & ಅಧಿಕಾರಾವಧಿ); ವಿಧಿ 149 (ಕರ್ತವ್ಯಗಳು); ವಿಧಿ 151 (ವರದಿಗಳನ್ನು ರಾಷ್ಟ್ರಪತಿ/ರಾಜ್ಯಪಾಲರಿಗೆ ಸಲ್ಲಿಕೆ).",
                        "<b>ಸಂಸದೀಯ ಸಮಿತಿ:</b> ಸಾರ್ವಜನಿಕ ಲೆಕ್ಕಪತ್ರ ಸಮಿತಿ (PAC) ಸಿಎಜಿ ವರದಿಗಳನ್ನು ವಿವರವಾಗಿ ಪರಿಶೀಲಿಸುತ್ತದೆ.",
                        "<b>RDSS ಯೋಜನೆ:</b> ವಿತರಣಾ ನಷ್ಟ ಕಡಿಮೆ ಮಾಡಲು ಷರತ್ತುಬದ್ಧ ಆರ್ಥಿಕ ನೆರವು ನೀಡುವ ಸುಧಾರಿತ ವಿತರಣಾ ವಲಯ ಯೋಜನೆ."
                    ],
                    "pyq_link": "ವಿಶ್ಲೇಷಣಾತ್ಮಕ ಪ್ರಶ್ನೆ: ಸಿಎಜಿ ಸಾಂವಿಧಾನಿಕ ಸ್ಥಾನಮಾನ ಮತ್ತು ಸಾರ್ವಜನಿಕ ಹಣಕಾಸಿನ ಮೇಲಿನ ಆಡಳಿತಾತ್ಮಕ ನಿಯಂತ್ರಣ.",
                    "trap": "ಸಿಎಜಿ ವರದಿಗಳು ನೇರವಾಗಿ ಸಂಸತ್ತಿಗೆ ಹೋಗುವುದಿಲ್ಲ; ರಾಷ್ಟ್ರಪತಿಗಳು ಅಥವಾ ರಾಜ್ಯಪಾಲರ ಮೂಲಕ ಸದನಗಳಲ್ಲಿ ಮಂಡನೆಯಾಗುತ್ತವೆ."
                },
                {
                    "title": "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ (AI) ನಿಯಂತ್ರಣ, ಡೀಪ್‌ಫೇಕ್ ಮತ್ತು ಐಟಿ ನಿಯಮಗಳು",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 3 · ವಿಜ್ಞಾನ ತಂತ್ರಜ್ಞಾನ & ಸೈಬರ್ ಭದ್ರತೆ",
                    "in_news": "ಸಾಮಾಜಿಕ ಜಾಲತಾಣಗಳಲ್ಲಿ ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಆಧಾರಿತ ಡೀಪ್‌ಫೇಕ್ ತಡೆಗಟ್ಟಲು ಐಟಿ ನಿಯಮಾವಳಿಗಳು 2021ರ ಅಡಿಯಲ್ಲಿ ಕಡ್ಡಾಯ ಮಾರ್ಗಸೂಚಿಗಳನ್ನು ಹೊರಡಿಸಲಾಗಿದೆ.",
                    "static_framework": [
                        "<b>ಐಟಿ ಕಾಯ್ದೆ 2000ರ ಕಲಂ 79:</b> ಮಧ್ಯವರ್ತಿಗಳಿಗೆ ನೀಡಿರುವ 'ಸೇಫ್ ಹಾರ್ಬರ್' ರಕ್ಷಣೆ; ಸರ್ಕಾರ ಸೂಚಿಸಿದ ಜಾಗರೂಕತೆ ಪಾಲಿಸುವುದು ಕಡ್ಡಾಯ.",
                        "<b>ಐಟಿ ನಿಯಮಗಳು 2021:</b> ಕಾನೂನುಬಾಹಿರ ಮಾಹಿತಿಯನ್ನು 36 ಗಂಟೆಗಳಲ್ಲಿ ತೆಗೆದುಹಾಕುವುದು ಮತ್ತು ಕುಂದುಕೊರತೆ ನಿವಾರಣಾಧಿಕಾರಿ ನೇಮಕ ಕಡ್ಡಾಯ.",
                        "<b>ಡಿಜಿಟಲ್ ವೈಯಕ್ತಿಕ ದತ್ತಾಂಶ ಸಂರಕ್ಷಣಾ ಕಾಯ್ದೆ 2023:</b> ನಾಗರಿಕರ ದತ್ತಾಂಶ ಸುರಕ್ಷತೆ ಮತ್ತು ದತ್ತಾಂಶ ಸಂರಕ್ಷಣಾ ಮಂಡಳಿ ಸ್ಥಾಪನೆ."
                    ],
                    "pyq_link": "ಮುಖ್ಯ ಪರಿಕಲ್ಪನಾ ಪ್ರಶ್ನೆ: ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಮತ್ತು ಡೀಪ್‌ಫೇಕ್ ತಂತ್ರಜ್ಞಾನ ಒಡ್ಡುವ ಸೈಬರ್ ಭದ್ರತಾ ಸವಾಲುಗಳು.",
                    "trap": "ಕಲಂ 79ರ ಅಡಿಯಲ್ಲಿ ಸಿಗುವ ಸೇಫ್ ಹಾರ್ಬರ್ ರಕ್ಷಣೆ ಷರತ್ತುಬದ್ಧವಾದುದು; ನಿಗದಿತ ನಿಯಮ ಪಾಲಿಸದಿದ್ದರೆ ಈ ರಕ್ಷಣೆ ರದ್ದಾಗುತ್ತದೆ."
                },
                {
                    "title": "ಡಬ್ಲ್ಯುಟಿಒ (WTO) ಮೀನುಗಾರಿಕೆ ಸಬ್ಸಿಡಿ ಒಪ್ಪಂದ",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 3 · ಕೃಷಿ & ಜಾಗತಿಕ ವ್ಯಾಪಾರ",
                    "in_news": "ಸಾಂಪ್ರದಾಯಿಕ ಹಾಗೂ ಸಣ್ಣ ಪ್ರಮಾಣದ ಮೀನುಗಾರರ ಹಿತರಕ್ಷಣೆಗಾಗಿ ಅಭಿವೃದ್ಧಿಶೀಲ ರಾಷ್ಟ್ರಗಳಿಗೆ 25 ವರ್ಷಗಳ ವಿನಾಯಿತಿ ಕಾಲಾವಕಾಶ ನೀಡಬೇಕೆಂದು ಭಾರತ ಆಗ್ರಹಿಸಿದೆ.",
                    "static_framework": [
                        "<b>ಡಬ್ಲ್ಯುಟಿಒ ತೀರ್ಮಾನ:</b> 1995ರ ಮರಕೇಶ್ ಒಪ್ಪಂದದಡಿ ಸ್ಥಾಪಿತವಾದ ಒಮ್ಮತ ಆಧಾರಿತ ಬಹುಪಕ್ಷೀಯ ಸಂಸ್ಥೆ.",
                        "<b>ನಿರ್ಬಂಧಿತ ಸಬ್ಸಿಡಿಗಳು:</b> ಅಕ್ರಮ, ವರದಿಯಾಗದ ಮತ್ತು ಅನಿಯಂತ್ರಿತ (IUU) ಮೀನುಗಾರಿಕೆ ಹಾಗೂ ಅತಿಯಾದ ಮೀನುಗಾರಿಕೆಗೆ ಸಬ್ಸಿಡಿ ನಿಷೇಧ.",
                        "<b>ವಿಶೇಷ ಮತ್ತು ಪ್ರತ್ಯೇಕ ಪರಿಗಣನೆ (S&DT):</b> ಬಡ ರಾಷ್ಟ್ರಗಳ ಜೀವನೋಪಾಯ ರಕ್ಷಣೆಗೆ ನೀಡಲಾಗುವ ಸಾಂಪ್ರದಾಯಿಕ ರಕ್ಷಣೆ."
                    ],
                    "pyq_link": "ಪ್ರಮುಖ ಪ್ರಶ್ನೆ: ವಿಶ್ವ ವ್ಯಾಪಾರ ಸಂಸ್ಥೆಯ ಆಡಳಿತ ಚೌಕಟ್ಟು ಮತ್ತು ವ್ಯಾಪಾರ ಸಬ್ಸಿಡಿ ವರ್ಗೀಕರಣಗಳು (ಆಂಬರ್, ಬ್ಲೂ, ಗ್ರೀನ್ ಬಾಕ್ಸ್).",
                    "trap": "ಕರಾವಳಿಯ 12 ನಾಟಿಕಲ್ ಮೈಲಿ ವ್ಯಾಪ್ತಿಯಲ್ಲಿ ಮೀನುಗಾರಿಕೆ ನಡೆಸುವ ಸಣ್ಣ ಮೀನುಗಾರರಿಗೆ ನೀಡುವ ಇಂಧನ ಸಬ್ಸಿಡಿಯನ್ನು ಒಪ್ಪಂದ ನಿಷೇಧಿಸುವುದಿಲ್ಲ."
                },
                {
                    "title": "ಎಸ್‌ಸಿಒ (SCO) ಮತ್ತು ಬ್ರಿಕ್ಸ್ ವಿಸ್ತರಣೆ: ಬಹುಮುಖಿ ರಾಜತಾಂತ್ರಿಕತೆ",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 2 · ಅಂತರರಾಷ್ಟ್ರೀಯ ಸಂಬಂಧಗಳು",
                    "in_news": "ಜಾಗತಿಕ ಶೃಂಗಸಭೆಗಳಲ್ಲಿ ಭಾರತವು ಜಾಗತಿಕ ದಕ್ಷಿಣದ (Global South) ಧ್ವನಿಯಾಗಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದ್ದು, ಕಾರ್ಯತಂತ್ರದ ಸ್ವಾಯತ್ತತೆಯನ್ನು ಪುನರುಚ್ಚರಿಸಿದೆ.",
                    "static_framework": [
                        "<b>ಶಾಂಘೈ ಸಹಕಾರ ಸಂಸ್ಥೆ (SCO):</b> 2001ರಲ್ಲಿ ಸ್ಥಾಪನೆ; ಭಾರತ-ಪಾಕಿಸ್ತಾನ 2017ರಲ್ಲಿ ಪೂರ್ಣ ಸದಸ್ಯತ್ವ ಪಡೆದವು; ಇರಾನ್ (2023) ಮತ್ತು ಬೆಲಾರಸ್ (2024) ಇತ್ತೀಚಿನ ಸದಸ್ಯರು.",
                        "<b>RATS SCO:</b> ತಾಷ್ಕೆಂಟ್‌ನಲ್ಲಿರುವ ಪ್ರಾದೇಶಿಕ ಭಯೋತ್ಪಾದನಾ ವಿರೋಧಿ ಕಾರ್ಯಾಚರಣೆ ಕೇಂದ್ರ.",
                        "<b>ಬ್ರಿಕ್ಸ್ (BRICS) ಹೊಸ ಬ್ಯಾಂಕ್:</b> ಶಾಂಘೈನಲ್ಲಿರುವ ನ್ಯೂ ಡೆವಲಪ್‌ಮೆಂಟ್ ಬ್ಯಾಂಕ್ (NDB); ಎಲ್ಲ ಸದಸ್ಯರಿಗೂ ಸಮಾನ ಮತದಾನದ ಹಕ್ಕಿದೆ."
                    ],
                    "pyq_link": "ಮುಖ್ಯ ಪರಿಕಲ್ಪನಾ ಪ್ರಶ್ನೆ: ಬದಲಾಗುತ್ತಿರುವ ಜಾಗತಿಕ ವ್ಯವಸ್ಥೆಯಲ್ಲಿ ಎಸ್‌ಸಿಒ ಮತ್ತು ಬ್ರಿಕ್ಸ್ ವೇದಿಕೆಗಳಲ್ಲಿ ಭಾರತದ ಪ್ರಮುಖ ಹಿತಾಸಕ್ತಿಗಳು.",
                    "trap": "ನ್ಯೂ ಡೆವಲಪ್‌ಮೆಂಟ್ ಬ್ಯಾಂಕ್‌ನಲ್ಲಿ (NDB) ಯಾವುದೇ ಒಂದು ದೇಶಕ್ಕೆ ವೀಟೋ (Veto) ಅಧಿಕಾರವಿಲ್ಲ; ಎಲ್ಲರಿಗೂ ಸಮಾನ ಮತದಾನದ ಹಕ್ಕಿದೆ."
                },
                {
                    "title": "ನ್ಯಾಯಾಂಗದಲ್ಲಿ ಪ್ರಕರಣಗಳ ಬಾಕಿ ಹಾಗೂ ತ್ವರಿತ ನ್ಯಾಯಾಲಯಗಳು",
                    "paper": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - 2 · ನ್ಯಾಯಾಂಗ ವ್ಯವಸ್ಥೆ",
                    "in_news": "ದೇಶದ ವಿವಿಧ ನ್ಯಾಯಾಲಯಗಳಲ್ಲಿ 5 ಕೋಟಿಗೂ ಅಧಿಕ ಪ್ರಕರಣಗಳು ಬಾಕಿ ಇದ್ದು, ಇ-ಕೋರ್ಟ್ಸ್ ಹಂತ-3 ಮತ್ತು ನ್ಯಾಷನಲ್ ಜುಡಿಷಿಯಲ್ ಡಾಟಾ ಗ್ರಿಡ್ ಮೂಲಕ ತ್ವರಿತ ಇತ್ಯರ್ಥಕ್ಕೆ ಚಾಲನೆ.",
                    "static_framework": [
                        "<b>ಸಾಂವಿಧಾನಿಕ ಹಕ್ಕು:</b> ವಿಧಿ 21ರ ಅಡಿ ತ್ವರಿತ ವಿಚಾರಣೆ ಮೂಲಭೂತ ಹಕ್ಕು (ಹುಸೇನಾರಾ ಖಾತೂನ್ ಪ್ರಕರಣ); ವಿಧಿ 227 ಹೈಕೋರ್ಟ್ ಮೇಲ್ವಿಚಾರಣಾ ಅಧಿಕಾರ.",
                        "<b>ಇ-ಕೋರ್ಟ್ಸ್ ಯೋಜನೆ:</b> ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಮತ್ತು ಡಿಜಿಟಲ್ ಕಡತಗಳ ನಿರ್ವಹಣೆಗಾಗಿ ₹7,210 ಕೋಟಿ ವೆಚ್ಚದ 3ನೇ ಹಂತಕ್ಕೆ ಅನುಮೋದನೆ.",
                        "<b>ಗ್ರಾಮ ನ್ಯಾಯಾಲಯ ಕಾಯ್ದೆ 2008:</b> ಹಳ್ಳಿಗಾಡಿನ ಜನರಿಗೆ ಗ್ರಾಮ ಮಟ್ಟದಲ್ಲೇ ತ್ವರಿತ ನ್ಯಾಯ ಒದಗಿಸಲು ಸಂಚಾರಿ ನ್ಯಾಯಾಲಯಗಳ ಸ್ಥಾಪನೆ."
                    ],
                    "pyq_link": "ವಿಶ್ಲೇಷಣಾತ್ಮಕ ಪ್ರಶ್ನೆ: ಭಾರತೀಯ ನ್ಯಾಯಾಂಗದಲ್ಲಿ ನ್ಯಾಯ ವಿಳಂಬಕ್ಕೆ ಪ್ರಮುಖ ಕಾರಣಗಳು ಮತ್ತು ಸುಧಾರಣಾ ಕ್ರಮಗಳು.",
                    "trap": "ಗ್ರಾಮ ನ್ಯಾಯಾಲಯಗಳನ್ನು ಹೈಕೋರ್ಟ್ ಜತೆ ಸಮಾಲೋಚಿಸಿ ರಾಜ್ಯ ಸರ್ಕಾರಗಳು ಅಧಿಸೂಚಿಸುತ್ತವೆ; ಕೇಂದ್ರ ಕಾನೂನು ಸಚಿವಾಲಯ ನೇರವಾಗಿ ಸ್ಥಾಪಿಸುವುದಿಲ್ಲ."
                }
            ],
            "kn_mcqs": [
                {
                    "topic": "ಸಂವಿಧಾನ ತಿದ್ದುಪಡಿ ಹಾಗೂ ಕ್ಷೇತ್ರ ಪುನರ್ವಿಂಗಡಣೆ",
                    "statements": [
                        "ವಿಧಿ 368ರ ಅಡಿಯಲ್ಲಿ ಸಂವಿಧಾನ ತಿದ್ದುಪಡಿ ಮಸೂದೆಗೆ ಸಂಸತ್ತಿನ ಎರಡೂ ಸದನಗಳಲ್ಲಿ ವಿಶೇಷ ಬಹುಮತ ಅಗತ್ಯ.",
                        "ಎಲ್ಲಾ ಸಂವಿಧಾನ ತಿದ್ದುಪಡಿ ಮಸೂದೆಗಳಿಗೂ ಕನಿಷ್ಠ ಅರ್ಧದಷ್ಟು ರಾಜ್ಯ ಶಾಸಕಾಂಗಗಳ ಅನುಮೋದನೆ ಕಡ್ಡಾಯ.",
                        "84ನೇ ಸಂವಿಧಾನ ತಿದ್ದುಪಡಿ ಕಾಯ್ದೆಯು ಲೋಕಸಭಾ ಸ್ಥಾನಗಳ ಸ್ಥಗಿತವನ್ನು 2026ರ ನಂತರದ ಮೊದಲ ಜನಗಣತಿಯವರೆಗೆ ವಿಸ್ತರಿಸಿತು."
                    ],
                    "options": "(A) 1 ಮಾತ್ರ   (B) 1 ಮತ್ತು 3 ಮಾತ್ರ   (C) 2 ಮತ್ತು 3 ಮಾತ್ರ   (D) ಎಲ್ಲವೂ ಸರಿ",
                    "answer": "B",
                    "explanation": "2ನೇ ಹೇಳಿಕೆ ತಪ್ಪಾಗಿದೆ: ಒಕ್ಕೂಟ ತತ್ವಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ತಿದ್ದುಪಡಿಗಳಿಗೆ ಮಾತ್ರ ಅರ್ಧ ರಾಜ್ಯಗಳ ಒಪ್ಪಿಗೆ ಅಗತ್ಯ. 1 ಮತ್ತು 3 ಸರಿಯಾಗಿವೆ."
                },
                {
                    "topic": "ಗ್ರಾಹಕ ಬೆಲೆ ಸೂಚ್ಯಂಕ (CPI)",
                    "statements": [
                        "ಗ್ರಾಹಕ ಬೆಲೆ ಸೂಚ್ಯಂಕ (ಸಂಯೋಜಿತ) ವನ್ನು ರಾಷ್ಟ್ರೀಯ ಸಾಂಖ್ಯಿಕ ಕಚೇರಿ (NSO) ಪ್ರಕಟಿಸುತ್ತದೆ.",
                        "ಆರ್‌ಬಿಐ ಕಾಯ್ದೆ 1934ರ ಅನ್ವಯ ಹಣದುಬ್ಬರ ಸಹನೀಯ ಮಿತಿಯನ್ನು ಶೇ. 2 ರಿಂದ 6 ಎಂದು ನಿಗದಿಪಡಿಸಲಾಗಿದೆ."
                    ],
                    "options": "(A) 1 ಮಾತ್ರ   (B) 2 ಮಾತ್ರ   (C) 1 ಮತ್ತು 2 ಎರಡೂ   (D) ಯಾವುದೂ ಅಲ್ಲ",
                    "answer": "C",
                    "explanation": "ಎರಡೂ ಹೇಳಿಕೆಗಳು ಸರಿಯಾಗಿವೆ. MoSPI ಅಡಿಯ NSO ಸಂಸ್ಥೆ ಸಂಯೋಜಿತ CPI ಅನ್ನು ಮಾಸಿಕವಾಗಿ ಬಿಡುಗಡೆ ಮಾಡುತ್ತದೆ."
                },
                {
                    "topic": "ಚುನಾವಣಾ ಆಯೋಗ ಮತ್ತು ಮತದಾರರ ಪಟ್ಟಿ",
                    "statements": [
                        "ವಿಧಿ 324 ಚುನಾವಣೆಗಳ ಮೇಲ್ವಿಚಾರಣೆ ಮತ್ತು ನಿಯಂತ್ರಣದ ಅಧಿಕಾರವನ್ನು ಚುನಾವಣಾ ಆಯೋಗಕ್ಕೆ ನೀಡುತ್ತದೆ.",
                        "ಮತದಾರರ ಪಟ್ಟಿಗಳ ತಯಾರಿಕೆ ಮತ್ತು ಪರಿಷ್ಕರಣೆಯನ್ನು 1951ರ ಜನಪ್ರತಿನಿಧಿ ಕಾಯ್ದೆ ನಿಯಂತ್ರಿಸುತ್ತದೆ."
                    ],
                    "options": "(A) 1 ಮಾತ್ರ   (B) 2 ಮಾತ್ರ   (C) 1 ಮತ್ತು 2 ಎರಡೂ   (D) ಯಾವುದೂ ಅಲ್ಲ",
                    "answer": "A",
                    "explanation": "2ನೇ ಹೇಳಿಕೆ ತಪ್ಪಾಗಿದೆ: ಮತದಾರರ ಪಟ್ಟಿ ತಯಾರಿಕೆಯನ್ನು 1950ರ ಜನಪ್ರತಿನಿಧಿ ಕಾಯ್ದೆ ನಿಯಂತ್ರಿಸುತ್ತದೆ. 1951ರ ಕಾಯ್ದೆ ಚುನಾವಣೆ ನಡವಳಿಕೆಗೆ ಸಂಬಂಧಿಸಿದೆ."
                },
                {
                    "topic": "ನ್ಯೂ ಡೆವಲಪ್‌ಮೆಂಟ್ ಬ್ಯಾಂಕ್ (NDB)",
                    "statements": [
                        "ನ್ಯೂ ಡೆವಲಪ್‌ಮೆಂಟ್ ಬ್ಯಾಂಕ್‌ನ ಕೇಂದ್ರ ಕಚೇರಿ ಚೀನಾದ ಶಾಂಘೈ ನಗರದಲ್ಲಿದೆ.",
                        "ಬ್ಯಾಂಕ್‌ನ ಆಡಳಿತ ಮಂಡಳಿಯಲ್ಲಿ ಯಾವುದೇ ಸದಸ್ಯ ರಾಷ್ಟ್ರಕ್ಕೂ ವೀಟೋ (Veto) ಅಧಿಕಾರ ಇರುವುದಿಲ್ಲ."
                    ],
                    "options": "(A) 1 ಮಾತ್ರ   (B) 2 ಮಾತ್ರ   (C) 1 ಮತ್ತು 2 ಎರಡೂ   (D) ಯಾವುದೂ ಅಲ್ಲ",
                    "answer": "C",
                    "explanation": "ಎರಡೂ ಹೇಳಿಕೆಗಳು ಸರಿಯಾಗಿವೆ. ಬ್ರಿಕ್ಸ್ ರಾಷ್ಟ್ರಗಳು ಸ್ಥಾಪಿಸಿದ NDB ಬ್ಯಾಂಕ್‌ನಲ್ಲಿ ಎಲ್ಲ ಸದಸ್ಯ ರಾಷ್ಟ್ರಗಳಿಗೂ ಸಮಾನ ಮತದಾನದ ಹಕ್ಕಿದೆ."
                },
                {
                    "topic": "ಸಿಎಜಿ ಸಾಂವಿಧಾನಿಕ ಸ್ಥಾನಮಾನ",
                    "statements": [
                        "ಸಿಎಜಿ ಅವರನ್ನು ರಾಷ್ಟ್ರಪತಿಗಳು ನೇಮಿಸುತ್ತಾರೆ ಮತ್ತು ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ನ್ಯಾಯಾಧೀಶರ ರೀತಿಯಲ್ಲೇ ಪದಚ್ಯುತಗೊಳಿಸಬಹುದು.",
                        "ವಿಧಿ 151ರ ಅಡಿ ಕೇಂದ್ರದ ಲೆಕ್ಕಪರಿಶೋಧನಾ ವರದಿಗಳನ್ನು ಸಿಎಜಿ ನೇರವಾಗಿ ಸಾರ್ವಜನಿಕ ಲೆಕ್ಕಪತ್ರ ಸಮಿತಿಗೆ ಸಲ್ಲಿಸುತ್ತಾರೆ."
                    ],
                    "options": "(A) 1 ಮಾತ್ರ   (B) 2 ಮಾತ್ರ   (C) 1 ಮತ್ತು 2 ಎರಡೂ   (D) ಯಾವುದೂ ಅಲ್ಲ",
                    "answer": "A",
                    "explanation": "2ನೇ ಹೇಳಿಕೆ ತಪ್ಪು: ವಿಧಿ 151ರ ಅಡಿ ವರದಿಗಳನ್ನು ರಾಷ್ಟ್ರಪತಿಗಳಿಗೆ ಸಲ್ಲಿಸಲಾಗುತ್ತದೆ; ರಾಷ್ಟ್ರಪತಿಗಳು ಅವುಗಳನ್ನು ಸಂಸತ್ತಿನ ಸದನಗಳಲ್ಲಿ ಮಂಡಿಸುತ್ತಾರೆ."
                }
            ]
        }

        html = self.engine.render_html("the_hindu_nordic.html", context)
        self.engine.generate_pdf_from_html(html, output_path)
        logger.info(f"Generated The Hindu PDF: {output_path}")
        return output_path

    # ════════════════════════════════════════════════════
    # 2. PRAJAVANI GENERATOR (Template 3: KPSC Royal Crimson)
    # ════════════════════════════════════════════════════
    def generate_prajavani_pdf(self, date_str: str = None) -> str:
        if not date_str:
            date_str = self.get_today_str()

        formatted_date = self.get_formatted_date()
        filename = f"Prajavani_{date_str}.pdf"
        output_path = os.path.join(PDF_DIR, filename)

        context = {
            "date_str": formatted_date,
            "en_topics": [
                {
                    "title": "Namma Metro Pink Line: Network Surpasses 100 KM Milestone",
                    "syllabus": "General Studies - 1 Urban Infrastructure / GS-2",
                    "why_in_news": "The inauguration of the 7.5 km elevated section of the Pink Line has expanded Bengaluru's operational metro network past 100 km, cementing its position as India's second-largest metro transit system after Delhi. The Jayadeva Hospital interchange stands as the country's tallest multi-level transit junction.",
                    "static_points": [
                        "<b>SPV Architecture:</b> Bangalore Metro Rail Corporation Ltd (BMRCL) is an equal 50:50 joint venture between the Government of India and the Government of Karnataka.",
                        "<b>Nodal Ministry:</b> Ministry of Housing and Urban Affairs (MoHUA), Government of India.",
                        "<b>Safety Certification:</b> Mandatory statutory clearance by the Commissioner of Metro Railway Safety (CMRS) under the Metro Railways (Operation and Maintenance) Act, 2002.",
                        "<b>Operational Corridors:</b> Purple (Whitefield-Challaghatta), Green (Madavara-Silk Institute), Yellow (RV Road-Bommasandra), Pink (Kalena Agrahara-Nagawara), and Blue (Silk Board-Airport)."
                    ],
                    "exam_points": [
                        "Phase-1 commencement: 2011 (MG Road - Baiyappanahalli).",
                        "Jayadeva Interchange: Landmark integration of Yellow and Pink corridors with a 29m elevated platform."
                    ],
                    "trap": "CMRS operates under the Commission of Railway Safety, Ministry of Civil Aviation (MoCA)—not under the Ministry of Railways—to ensure independent safety appraisals.",
                    "state_angle": "Directly impacts Greater Bengaluru Authority (GBA) transport integration goals and urban mobility infrastructure indices and governance research.",
                    "source": "Prajavani / BMRCL Official Release"
                },
                {
                    "title": "Mekedatu Balancing Reservoir & Cauvery Basin Basin Framework",
                    "syllabus": "General Studies - 1 Karnataka Geography / GS-2 Inter-State",
                    "why_in_news": "State Cabinet reiterates adherence to the Cauvery Water Management Authority guidelines for statutory environmental clearances of the proposed Mekedatu Balancing Reservoir.",
                    "static_points": [
                        "<b>Project Location:</b> Confluence of Cauvery and Arkavathi rivers near Kanakapura, Ramanagara district.",
                        "<b>Dual Objectives:</b> 4.75 TMC drinking water supply to Greater Bengaluru and 400 MW hydroelectric power generation (Total gross storage: 67.16 TMC).",
                        "<b>Article 262:</b> Empowers Parliament to legislate for adjudication of inter-state river disputes and bar jurisdiction of Supreme Court.",
                        "<b>Statutory Bodies:</b> CWMA and CWRC established under Section 6A of the Inter-State River Water Disputes Act 1956 following the Supreme Court's February 2018 verdict."
                    ],
                    "exam_points": [
                        "Cauvery Tribunal (CWDT) Final Award: 2007 (Total basin allocation: 726 TMC).",
                        "2018 Supreme Court Allocation: Karnataka awarded 284.75 TMC (increased by 14.75 TMC for Bengaluru drinking water needs)."
                    ],
                    "trap": "CWMA is not a constitutional body; it is a statutory authority created under the Inter-State River Water Disputes Act, 1956.",
                    "state_angle": "Primary focus area for Karnataka Geography & Inter-state Federalism studies.",
                    "source": "Supreme Court Verdict 2018 / Prajavani"
                },
                {
                    "title": "Western Ghats Eco-Sensitive Zones & Kasturirangan Report",
                    "syllabus": "General Studies - 1 Environment & Biodiversity",
                    "why_in_news": "Opposition in Karnataka Legislature and farmer bodies against draft notifications declaring Western Ghats villages as Eco-Sensitive Areas (ESA).",
                    "static_points": [
                        "<b>Gadgil Commission (WGEEP 2010):</b> Recommended declaring 100% of the Western Ghats as ecologically sensitive, graded into ESZ-1, 2, and 3.",
                        "<b>Kasturirangan Committee (HLWG 2013):</b> Scaled down the ESA to 37% (~59,940 sq km) of the Western Ghats, banning mining, quarrying, and red-category industries.",
                        "<b>Legal Basis:</b> Eco-Sensitive Zones/Areas are notified under Section 3 of the Environment (Protection) Act, 1986.",
                        "<b>Karnataka Coverage:</b> Draft proposals encompass ~20,668 sq km in Karnataka across 10 districts."
                    ],
                    "exam_points": [
                        "Gadgil recommended complete coverage; Kasturirangan recommended only 37% ESA.",
                        "Western Ghats is one of the world's 8 'hottest hotspots' of biological diversity."
                    ],
                    "trap": "Recommendations of high-level committees become legally enforceable only after final statutory notification under the EPA 1986.",
                    "state_angle": "Karnataka has the largest contiguous stretch of the Western Ghats forest canopy across 10 districts.",
                    "source": "HLWG Report / Prajavani"
                },
                {
                    "title": "Karnataka Gram Swaraj & Panchayat Raj Act: Ward Committees",
                    "syllabus": "General Studies - 2 Rural Development & PRIs",
                    "why_in_news": "Rural Development and Panchayat Raj (RDPR) Department issues directives for mandatory quarterly Grama Sabhas and social audits across 5,950 Gram Panchayats.",
                    "static_framework": [
                        "<b>73rd Amendment Act 1992:</b> Inserted Part IX (Articles 243 to 243-O) and Eleventh Schedule (29 functional subjects).",
                        "<b>Karnataka Milestone:</b> Karnataka Gram Swaraj and Panchayat Raj Act, 1993 (re-titled in 2015 based on Ramesh Kumar Committee recommendations).",
                        "<b>Three-Tier System:</b> Grama Panchayat (Village), Taluk Panchayat (Taluk), and Zilla Panchayat (District).",
                        "<b>Grama Sabha (Art 243A):</b> Only permanent body under PRI consisting of all registered voters in the village."
                    ],
                    "exam_points": [
                        "Reservation: 50% reservation for women in Karnataka PRIs (higher than constitutional 33% mandate).",
                        "State Election Commission (Art 243K) conducts local body elections independently."
                    ],
                    "trap": "Grama Sabha is composed of all registered voters in the panchayat, not just heads of households or elected members.",
                    "state_angle": "Karnataka was a pioneering state under Abdul Nazir Sab in decentralizing democratic powers to PRIs in the 1980s."
                },
                {
                    "title": "Karnataka State Development Loans (SDL) & Article 293 Limits",
                    "syllabus": "General Studies - 3 State Public Finance & Economy",
                    "why_in_news": "Finance Department issues redemption notifications for maturing Karnataka State Development Loans and reviews fiscal deficit targets under the KFRA.",
                    "static_points": [
                        "<b>Article 293:</b> States can borrow only within the territory of India upon the security of the Consolidated Fund of the State.",
                        "<b>Central Consent:</b> Required under Art 293(3) if there is an outstanding central loan or guarantee.",
                        "<b>Karnataka Fiscal Responsibility Act (KFRA 2002):</b> Mandates fiscal deficit within 3% of GSDP and debt-to-GSDP ratio below 25%."
                    ],
                    "exam_points": [
                        "SDLs are dated securities issued by state governments through RBI's E-Kuber auction platform.",
                        "Article 292 governs Union borrowings (including foreign loans); Article 293 governs State borrowings."
                    ],
                    "trap": "State Governments cannot borrow directly from foreign lenders or international agencies without Central Government mediation.",
                    "state_angle": "Karnataka has consistently maintained its fiscal deficit within the 3% KFRA statutory target for two decades."
                },
                {
                    "title": "Direct Benefit Transfer (DBT) Welfare Matrix: Gruha Lakshmi & Anna Bhagya",
                    "syllabus": "General Studies - 2 Social Justice & Governance",
                    "why_in_news": "Independent evaluation by administrative think-tanks highlights how women-headed DBT transfers under Gruha Lakshmi have strengthened rural female financial inclusion.",
                    "static_points": [
                        "<b>Constitutional Roots:</b> Articles 38, 39, and 41 of Directive Principles of State Policy promoting welfare state principles.",
                        "<b>Aadhaar Enabled Payment System (AePS):</b> Leverages JAM Trinity (Jan Dhan, Aadhaar, Mobile) for leak-proof direct subsidy credit.",
                        "<b>Food Security:</b> National Food Security Act (NFSA) 2013 provides 5 kg foodgrains per person for priority households."
                    ],
                    "exam_points": [
                        "Gruha Lakshmi: ₹2,000 monthly DBT to female heads of eligible households.",
                        "Anna Bhagya: 10 kg rice entitlement per person (5 kg Central PMGKAY + 5 kg State allocation)."
                    ],
                    "state_angle": "Karnataka leads southern states in Aadhaar-authenticated electronic DBT cash transfers.",
                    "source": "State Planning Board / Prajavani"
                },
                {
                    "title": "All India Cooperative Week & Kanaginahal Historic Origin",
                    "syllabus": "General Studies - 1 History / GS-2 Cooperatives",
                    "why_in_news": "Statewide celebration of 73rd All India Cooperative Week highlights agricultural credit disbursement targets and rural self-help groups in Karnataka.",
                    "static_points": [
                        "<b>97th Constitutional Amendment (2011):</b> Added Article 19(1)(c) right to form cooperatives; Article 43B DPSP; Part IX-B.",
                        "<b>Supreme Court Ruling (2021):</b> Union of India v. Rajendra Shah struck down Part IX-B for intra-state cooperatives, upholding it only for Multi-State Cooperatives.",
                        "<b>Karnataka Cooperative Milestone:</b> India's first primary agricultural credit cooperative was founded in 1905 at Kanaginahal, Gadag district, led by Siddanagouda Patil."
                    ],
                    "exam_points": [
                        "Cooperatives fall under State List (Entry 32, List II); Multi-state under Union List (Entry 44, List I).",
                        "Ministry of Cooperation created at Centre in July 2021."
                    ],
                    "trap": "Cooperatives remain a State Subject. Only multi-state cooperatives operating across multiple states fall under Central jurisdiction.",
                    "state_angle": "Gadag district is revered as the 'Cradle of the Indian Cooperative Movement'."
                },
                {
                    "title": "Green Firecrackers, Air Quality Monitoring & CPCB",
                    "syllabus": "General Studies - 3 Environment & Pollution Control",
                    "why_in_news": "High Court reviews post-festival air quality compliance and National Air Quality Index (NAQI) monitoring across Karnataka urban centers.",
                    "static_points": [
                        "<b>Landmark Precedent:</b> Arjun Gopal v. Union of India (2018) permitted only green crackers (SWAS, STAR, SAFAL developed by CSIR-NEERI).",
                        "<b>CPCB Statutory Origin:</b> Established in 1974 under the Water (Prevention and Control of Pollution) Act, later entrusted with Air Act 1981 powers.",
                        "<b>NAQI Structure:</b> 6 categories (Good to Severe) based on 8 criteria pollutants: PM10, PM2.5, NO2, SO2, CO, O3, NH3, Pb."
                    ],
                    "trap": "AQI 101-200 represents 'Moderate', not 'Satisfactory' (which is 51-100).",
                    "state_angle": "KSPCB is the state pollution regulator established under Water Act 1974."
                },
                {
                    "title": "Kannada Classical Language Status & CIIL Heritage Centers",
                    "syllabus": "General Studies - 1 Karnataka Culture & Heritage",
                    "why_in_news": "Union Government recently accorded Classical Language status to five additional languages, prompting renewed focus on autonomous funding for Central Institute of Classical Kannada (CICK).",
                    "static_points": [
                        "<b>Classical Languages (Total 11):</b> Tamil (2004), Sanskrit (2005), Kannada (2008), Telugu (2008), Malayalam (2013), Odia (2014); recently Marathi, Pali, Prakrit, Assamese, Bengali (2024).",
                        "<b>Ministry of Culture Criteria:</b> High antiquity of early texts/recorded history over 1,500-2,000 years; body of ancient literature considered valuable heritage; literary tradition is original and not borrowed.",
                        "<b>Halmidi Inscription:</b> Earliest Kannada epigraph (~450 CE) discovered in Belur taluk, Hassan district."
                    ],
                    "exam_points": [
                        "Kavirajamarga (9th century) by Srivijaya (Amoghavarsha's court) is the earliest available literary work in Kannada.",
                        "CICK operates under Central Institute of Indian Languages (CIIL), Mysuru."
                    ],
                    "trap": "Kannada received classical status in 2008, alongside Telugu—four years after Tamil."
                },
                {
                    "title": "Lake Encroachments & Karnataka Tank Conservation Authority (KTCDA)",
                    "syllabus": "General Studies - 1 Urban Environment & Water Bodies",
                    "why_in_news": "High Court directs urban local bodies to clear storm water drain buffer zone encroachments and implement Justice N.K. Patil Committee guidelines for lake rejuvenation.",
                    "static_points": [
                        "<b>Statutory Body:</b> Karnataka Tank Conservation and Development Authority (KTCDA) established under KTCDA Act 2014.",
                        "<b>Apex Oversight:</b> Enforces 30-meter buffer zones around lakes and 50-meter buffer zones around primary storm-water drains (Rajakaluves).",
                        "<b>Judicial Doctrines:</b> Public Trust Doctrine (M.C. Mehta v. Kamal Nath) applies to water bodies as state property held in trust for the public."
                    ],
                    "trap": "Buffer zones around lakes are 30 meters from the Full Tank Level (FTL), not from the dry lake boundary.",
                    "state_angle": "Bengaluru originally possessed an interconnected cascade system of over 800 lakes engineered during Kempegowda's era."
                },
                {
                    "title": "Pavagada Solar Park & Renewable Energy Policy 2022-2027",
                    "syllabus": "General Studies - 3 Energy Infrastructure & Solar",
                    "why_in_news": "Karnataka Energy Department achieves 16,500 MW renewable capacity milestone, led by Pavagada Ultra Mega Solar Park and hybrid wind-solar park expansions.",
                    "static_points": [
                        "<b>Shakti Sthala:</b> Pavagada Solar Park (Tumakuru district) is one of the world's largest solar parks with 2,050 MW operational capacity.",
                        "<b>Land Lease Model:</b> Innovative farmer-lease model without land acquisition, paying annual rents directly to farmers.",
                        "<b>KREDL:</b> Karnataka Renewable Energy Development Ltd serves as the nodal agency.",
                        "<b>State Renewable Target:</b> 10 GW additional renewable capacity by 2027 under Karnataka Renewable Energy Policy."
                    ],
                    "exam_points": [
                        "Karnataka ranks among India's top 3 states in cumulative installed solar energy capacity.",
                        "Pavagada was developed by Karnataka Solar Power Development Corporation Ltd (KSPDCL), a joint venture with SECI."
                    ],
                    "state_angle": "Pavagada was chosen due to high solar insolation (>300 sunny days) and barren semi-arid terrain."
                },
                {
                    "title": "UAPA Unlawful Association Tribunal Procedures",
                    "syllabus": "General Studies - 2 Internal Security & Legal System",
                    "why_in_news": "Ministry of Home Affairs extends ban on unlawful associations under the Unlawful Activities (Prevention) Act, triggering mandatory High Court Tribunal references.",
                    "static_points": [
                        "<b>UAPA 1967 (Section 3):</b> Central Government notifies an association as 'unlawful'.",
                        "<b>Tribunal Reference (Section 4):</b> Every declaration must be referred within 30 days to a Tribunal headed by a High Court Judge for confirmation.",
                        "<b>2019 Amendment:</b> Empowered the Centre to designate individuals as terrorists under the Fourth Schedule."
                    ],
                    "trap": "An association declaration is not permanent until confirmed by the Unlawful Activities Prevention Tribunal."
                }
            ],
            "en_oneliners": [
                "<b>November 14:</b> National Children's Day commemorating Jawaharlal Nehru (born 1889).",
                "<b>Vande Bharat Express:</b> First flagged off in Feb 2019 (New Delhi-Varanasi); manufactured at ICF Chennai.",
                "<b>Konkan Railway:</b> Established in 1990; 741 km route connecting Roha (Maharashtra) to Thokur (Karnataka).",
                "<b>National Air Quality Index (NAQI):</b> Launched in 2014 by CPCB with 6 categories and 8 key pollutants.",
                "<b>Mysuru COSMOS Planetarium:</b> Built by Indian Institute of Astrophysics (IIA) under DST.",
                "<b>One Nation One Subscription (ONOS):</b> Cabinet approved in Nov 2024; operated via INFLIBNET.",
                "<b>Space Sector Reforms:</b> IN-SPACe serves as single-window authorization body; NSIL handles commercial arm.",
                "<b>Halmidi Inscription:</b> Discovered in Hassan district, dated to ~450 CE during Kadamba King Kakusthavarma's reign."
            ],
            "en_mcqs": [
                {
                    "question": "Which of the following tributaries of River Cauvery joins from its LEFT bank?",
                    "opt_a": "Kabini",
                    "opt_b": "Hemavathi",
                    "opt_c": "Bhavani",
                    "opt_d": "Lakshmanathirtha",
                    "answer": "B",
                    "explanation": "Hemavathi, Harangi, Shimsha, and Arkavathi are left-bank tributaries. Kabini, Bhavani, Noyyal, Amaravathi, and Lakshmanathirtha are right-bank tributaries."
                },
                {
                    "question": "The Commissioner of Metro Railway Safety (CMRS) administratively functions under which Ministry?",
                    "opt_a": "Ministry of Railways",
                    "opt_b": "Ministry of Housing and Urban Affairs",
                    "opt_c": "Ministry of Civil Aviation",
                    "opt_d": "Ministry of Road Transport and Highways",
                    "answer": "C",
                    "explanation": "CMRS functions under the Commission of Railway Safety under the Ministry of Civil Aviation to ensure objective safety oversight."
                },
                {
                    "question": "India's first primary agricultural credit cooperative society was established in 1905 at which village in Karnataka?",
                    "opt_a": "Betageri",
                    "opt_b": "Hulkoti",
                    "opt_c": "Kanaginahal",
                    "opt_d": "Gangapur",
                    "answer": "C",
                    "explanation": "Kanaginahal in Gadag district was India's first cooperative society, established under the 1904 Cooperative Societies Act led by Siddanagouda Patil."
                },
                {
                    "question": "Consider the following statements regarding the 97th Constitutional Amendment Act:",
                    "statements": [
                        "It inserted Article 43B in the Directive Principles of State Policy.",
                        "In 2021, the Supreme Court struck down Part IX-B in its entirety for all cooperatives."
                    ],
                    "opt_a": "1 only",
                    "opt_b": "2 only",
                    "opt_c": "Both 1 and 2",
                    "opt_d": "Neither 1 nor 2",
                    "answer": "A",
                    "explanation": "Statement 2 is incorrect: the Supreme Court struck down Part IX-B only for intra-state cooperatives, upholding it for multi-state cooperatives."
                },
                {
                    "question": "The earliest known Kannada inscription, the Halmidi inscription (~450 CE), belongs to which dynasty?",
                    "opt_a": "Badami Chalukyas",
                    "opt_b": "Kadambas of Banavasi",
                    "opt_c": "Rashtrakutas",
                    "opt_d": "Gangas of Talakad",
                    "answer": "B",
                    "explanation": "The Halmidi inscription in Belur taluk belongs to the Kadamba king Kakusthavarma and represents the earliest recorded Kannada epigraph."
                }
            ],
            "kn_topics": [
                {
                    "title": "ನಮ್ಮ ಮೆಟ್ರೊ ಗುಲಾಬಿ ಮಾರ್ಗ: 100 ಕಿ.ಮೀ. ದಾಟಿದ ಬೆಂಗಳೂರು ಮೆಟ್ರೊ ಜಾಲ",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೧ & ೨ · ನಗರ ಮೂಲಸೌಕರ್ಯ",
                    "why_in_news": "ಬೆಂಗಳೂರಿನ ‘ನಮ್ಮ ಮೆಟ್ರೊ’ ಗುಲಾಬಿ ಮಾರ್ಗದ 7.5 ಕಿ.ಮೀ. ಎತ್ತರಿಸಿದ ಮಾರ್ಗ ಉದ್ಘಾಟನೆಗೊಂಡಿದೆ. ಇದರಿಂದಾಗಿ ಬೆಂಗಳೂರು ಮೆಟ್ರೊ ಜಾಲವು 100 ಕಿ.ಮೀ. ಮೈಲಿಗಲ್ಲು ದಾಟಿದ್ದು, ದೆಹಲಿ ಮೆಟ್ರೊ ನಂತರ ದೇಶದಲ್ಲೇ 2ನೇ ಅತಿ ದೊಡ್ಡ ಮೆಟ್ರೊ ಜಾಲವಾಗಿ ಹೊರಹೊಮ್ಮಿದೆ. ಜಯದೇವ ಆಸ್ಪತ್ರೆ ನಿಲ್ದಾಣವು ದೇಶದ ಅತಿ ಎತ್ತರದ ಇಂಟರ್‌ಚೇಂಜ್ ನಿಲ್ದಾಣವಾಗಿದೆ.",
                    "static_points": [
                        "<b>ಬಿಎಂಆರ್‌ಸಿಎಲ್ (BMRCL):</b> ಕೇಂದ್ರ ಹಾಗೂ ಕರ್ನಾಟಕ ರಾಜ್ಯ ಸರ್ಕಾರಗಳ 50:50 ಪಾಲುದಾರಿಕೆಯ ಜಂಟಿ ಉದ್ಯಮ (SPV).",
                        "<b>ನೋಡಲ್ ಸಚಿವಾಲಯ:</b> ಕೇಂದ್ರ ವಸತಿ ಮತ್ತು ನಗರ ವ್ಯವಹಾರಗಳ ಸಚಿವಾಲಯ (MoHUA).",
                        "<b>ಸುರಕ್ಷತಾ ಅನುಮತಿ:</b> ಮೆಟ್ರೊ ರೈಲ್ವೆ (ಕಾರ್ಯಾಚರಣೆ ಮತ್ತು ನಿರ್ವಹಣೆ) ಕಾಯ್ದೆ 2002ರ ಅಡಿ ಮೆಟ್ರೊ ರೈಲು ಸುರಕ್ಷತಾ ಆಯುಕ್ತರ (CMRS) ಪ್ರಮಾಣಪತ್ರ ಕಡ್ಡಾಯ.",
                        "<b>ಬಣ್ಣದ ಮಾರ್ಗಗಳು:</b> ನೇರಳೆ (Whitefield-Challaghatta), ಹಸಿರು (Madavara-Silk Institute), ಹಳದಿ (RV Road-Bommasandra), ಗುಲಾಬಿ (Kalena Agrahara-Nagawara), ನೀಲಿ (Silk Board-Airport)."
                    ],
                    "exam_points": [
                        "ಮೊದಲ ಹಂತ ಆರಂಭ: 2011 (ಎಂ.ಜಿ. ರಸ್ತೆ - ಬೈಯಪ್ಪನಹಳ್ಳಿ).",
                        "ಜಯದೇವ ಇಂಟರ್‌ಚೇಂಜ್: ಹಳದಿ ಮತ್ತು ಗುಲಾಬಿ ಮಾರ್ಗಗಳ ಸಮ್ಮಿಲನ ಕೇಂದ್ರ (29 ಮೀಟರ್ ಎತ್ತರ)."
                    ],
                    "trap": "ಮೆಟ್ರೊ ಸುರಕ್ಷತಾ ಆಯುಕ್ತರು (CMRS) ರೈಲ್ವೆ ಮಂಡಳಿಯ ಅಡಿಯಲ್ಲ, ಬದಲಿಗೆ ನಾಗರಿಕ ವಿಮಾನಯಾನ ಸಚಿವಾಲಯದ (MoCA) ರೈಲ್ವೆ ಸುರಕ್ಷತಾ ಆಯೋಗದ ಅಡಿಯಲ್ಲಿ ಸ್ವತಂತ್ರವಾಗಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಾರೆ.",
                    "state_angle": "ಗ್ರೇಟರ್ ಬೆಂಗಳೂರು ಪ್ರಾಧಿಕಾರ (GBA) ಮಸೂದೆ ಮತ್ತು ‘ಬ್ರ್ಯಾಂಡ್ ಬೆಂಗಳೂರು’ ನಗರ ಸಾರಿಗೆ ಏಕೀಕರಣ ಪ್ರಶ್ನೆಗಳಿಗೆ ಈ ಅಂಕಿಅಂಶ ಅತ್ಯಂತ ಪ್ರಸ್ತುತ.",
                    "source": "ಪ್ರಜಾವಾಣಿ / MoHUA / BMRCL"
                },
                {
                    "title": "ಮೇಕೆದಾಟು ಯೋಜನೆ ಮತ್ತು ಕಾವೇರಿ ಜಲ ವಿವಾದದ ಸಾಂವಿಧಾನಿಕ ಚೌಕಟ್ಟು",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೧ & ೨ · ಕರ್ನಾಟಕದ ಭೂಗೋಳ & ಅಂತರರಾಜ್ಯ ವಿವಾದ",
                    "why_in_news": "ಮೇಕೆದಾಟು ಸಮತೋಲನ (Balancing) ಜಲಾಶಯ ಯೋಜನೆಗೆ ಕೇಂದ್ರದ ಶಾಸನಬದ್ಧ ಪರಿಸರ ಅನುಮತಿ ನೀಡಬೇಕೆಂದು ಕರ್ನಾಟಕ ಸರ್ಕಾರ ಪುನರುಚ್ಚರಿಸಿದೆ.",
                    "static_points": [
                        "<b>ಸ್ಥಳ:</b> ರಾಮನಗರ ಜಿಲ್ಲೆಯ ಕನಕಪುರ ಬಳಿ ಕಾವೇರಿ ಮತ್ತು ಅರ್ಕಾವತಿ ನದಿಗಳ ಸಂಗಮ ಪ್ರದೇಶ.",
                        "<b>ಉದ್ದೇಶ:</b> ಬೆಂಗಳೂರು ನಗರಕ್ಕೆ 4.75 ಟಿಎಂಸಿ ಕುಡಿಯುವ ನೀರು ಮತ್ತು 400 ಮೆಗಾವಾಟ್ ಜಲವಿದ್ಯುತ್ ಉತ್ಪಾದನೆ (ಒಟ್ಟು ಸಂಗ್ರಹ 67.16 ಟಿಎಂಸಿ).",
                        "<b>ಸಂವಿಧಾನದ ವಿಧಿ 262:</b> ಅಂತರರಾಜ್ಯ ನದಿ ನೀರು ವಿವಾದಗಳ ತೀರ್ಮಾನಕ್ಕೆ ಸಂಸತ್ತು ಕಾನೂನು ರೂಪಿಸಬಹುದು; ನ್ಯಾಯಾಲಯಗಳ ಅಧಿಕಾರ ವ್ಯಾಪ್ತಿ ನಿರ್ಬಂಧಿಸಬಹುದು.",
                        "<b>ಕಾವೇರಿ ಪ್ರಾಧಿಕಾರಗಳು:</b> ಸುಪ್ರೀಂ ಕೋರ್ಟ್ 2018ರ ತೀರ್ಪಿನನ್ವಯ ಕಾವೇರಿ ನೀರು ನಿರ್ವಹಣಾ ಪ್ರಾಧಿಕಾರ (CWMA) ಮತ್ತು ಕಾವೇರಿ ನೀರು ನಿಯಂತ್ರಣ ಸಮಿತಿ (CWRC) ರಚನೆ."
                    ],
                    "exam_points": [
                        "ಕಾವೇರಿ ಜಲ ವಿವಾದ ನ್ಯಾಯಾಧಿಕರಣ (CWDT) ರಚನೆ: 1990; ಅಂತಿಮ ತೀರ್ಪು: 2007 (ಒಟ್ಟು 726 ಟಿಎಂಸಿ).",
                        "ಸುಪ್ರೀಂ ಕೋರ್ಟ್ 2018ರ ತೀರ್ಪು: ಕರ್ನಾಟಕಕ್ಕೆ 284.75 ಟಿಎಂಸಿ (ಹೆಚ್ಚುವರಿ 14.75 ಟಿಎಂಸಿ ಬೆಂಗಳೂರಿನ ಕುಡಿಯುವ ನೀರಿಗೆ), ತಮಿಳುನಾಡಿಗೆ 404.25 ಟಿಎಂಸಿ."
                    ],
                    "trap": "CWMA ಸಂವಿಧಾನಿಕ ಸಂಸ್ಥೆಯಲ್ಲ; ಇದು ಅಂತರರಾಜ್ಯ ನದಿ ನೀರು ವಿವಾದ ಕಾಯ್ದೆ 1956ರ ಅಡಿ ರಚಿಸಲಾದ ಶಾಸನಬದ್ಧ (Statutory) ಸಂಸ್ಥೆಯಾಗಿದೆ.",
                    "state_angle": "ಕರ್ನಾಟಕದ ಪ್ರಮುಖ ಅಂತರರಾಜ್ಯ ನದಿ ವಿವಾದಗಳು: ಕಾವೇರಿ (ತಮಿಳುನಾಡು), ಕೃಷ್ಣಾ (ಆಂಧ್ರ/ತೆಲಂಗಾಣ), ಮಹದಾಯಿ (ಗೋವಾ/ಮಹಾರಾಷ್ಟ್ರ).",
                    "source": "ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ತೀರ್ಪು / CWMA / ಪ್ರಜಾವಾಣಿ"
                },
                {
                    "title": "ಪಶ್ಚಿಮ ಘಟ್ಟ: ಕಸ್ತೂರಿರಂಗನ್ ವರದಿ ಮತ್ತು ಪರಿಸರ ಸೂಕ್ಷ್ಮ ವಲಯ",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೧ · ಪರಿಸರ & ಜೀವವೈವಿಧ್ಯ",
                    "why_in_news": "ಪಶ್ಚಿಮ ಘಟ್ಟದ ಗ್ರಾಮಗಳನ್ನು ಪರಿಸರ ಸೂಕ್ಷ್ಮ ಪ್ರದೇಶ (ESA) ಎಂದು ಅಧಿಸೂಚಿಸುವ ಕೇಂದ್ರದ ಕರಡು ಪ್ರಸ್ತಾವನೆಗೆ ರಾಜ್ಯ ವಿಧಾನಮಂಡಲ ಮತ್ತು ಮಲೆನಾಡು ಭಾಗದಲ್ಲಿ ತೀವ್ರ ವಿರೋಧ ವ್ಯಕ್ತವಾಗಿದೆ.",
                    "static_points": [
                        "<b>ಗಾಡ್ಗೀಳ್ ಸಮಿತಿ (WGEEP 2010):</b> ಇಡೀ ಪಶ್ಚಿಮ ಘಟ್ಟವನ್ನು ಪರಿಸರ ಸೂಕ್ಷ್ಮ ವಲಯವೆಂದು ಘೋಷಿಸಿ ESZ-1, 2, 3 ಎಂದು ವರ್ಗೀಕರಿಸಲು ಶಿಫಾರಸು ಮಾಡಿತ್ತು.",
                        "<b>ಕಸ್ತೂರಿರಂಗನ್ ಸಮಿತಿ (HLWG 2013):</b> ಕೇವಲ ಶೇ. 37 ರಷ್ಟು (ಸುಮಾರು 59,940 ಚ.ಕಿ.ಮೀ.) ಭಾಗವನ್ನು ESA ಎಂದು ಗುರುತಿಸಿ, ಗಣಿಗಾರಿಕೆ ಮತ್ತು ಉಷ್ಣ ವಿದ್ಯುತ್ ಸ್ಥಾವರ ನಿಷೇಧಕ್ಕೆ ಶಿಫಾರಸು ಮಾಡಿತು.",
                        "<b>ಕಾನೂನು ಆಧಾರ:</b> ಪರಿಸರ (ಸಂರಕ್ಷಣೆ) ಕಾಯ್ದೆ 1986ರ ಕಲಂ 3 ರ ಅಡಿಯಲ್ಲಿ ಕೇಂದ್ರ ಸರ್ಕಾರ ESA ಅಧಿಸೂಚನೆ ಹೊರಡಿಸುತ್ತದೆ.",
                        "<b>ಕರ್ನಾಟಕದ ವ್ಯಾಪ್ತಿ:</b> ಕರಡು ಅಧಿಸೂಚನೆಯಲ್ಲಿ ಕರ್ನಾಟಕದ ಸುಮಾರು 20,668 ಚ.ಕಿ.ಮೀ. ಪ್ರದೇಶ ಒಳಗೊಂಡಿದೆ."
                    ],
                    "exam_points": [
                        "ಗಾಡ್ಗೀಳ್ = ಪೂರ್ಣ ಘಟ್ಟ ಸಂರಕ್ಷಣೆ; ಕಸ್ತೂರಿರಂಗನ್ = ಕೇವಲ ಶೇ. 37 ಭಾಗ ಸಂರಕ್ಷಣೆ.",
                        "ಪಶ್ಚಿಮ ಘಟ್ಟವು ಜಗತ್ತಿನ 8 ಪ್ರಮುಖ ಜೀವವೈವಿಧ್ಯ ತಾಣಗಳಲ್ಲಿ (Biodiversity Hotspots) ಒಂದಾಗಿದೆ."
                    ],
                    "trap": "ಸಮಿತಿ ವರದಿಗಳು ಕೇವಲ ಶಿಫಾರಸುಗಳಷ್ಟೇ; ಪರಿಸರ ಸಂರಕ್ಷಣೆ ಕಾಯ್ದೆ 1986ರ ಅಡಿ ಅಂತಿಮ ಅಧಿಸೂಚನೆ ಹೊರಡಿಸಿದ ನಂತರವೇ ಕಾನೂನುಬದ್ಧ ನಿರ್ಬಂಧ ಜಾರಿಯಾಗುತ್ತದೆ.",
                    "state_angle": "ಕರ್ನಾಟಕದಲ್ಲಿ 10 ಜಿಲ್ಲೆಗಳ ವ್ಯಾಪ್ತಿಯಲ್ಲಿ ಪಶ್ಚಿಮ ಘಟ್ಟ ಹಬ್ಬಿದೆ."
                },
                {
                    "title": "ಕರ್ನಾಟಕ ಗ್ರಾಮ ಸ್ವರಾಜ್ ಮತ್ತು ಪಂಚಾಯತ್ ರಾಜ್ ಕಾಯ್ದೆ",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೨ · ಗ್ರಾಮೀಣಾಭಿವೃದ್ಧಿ & ಸ್ಥಳೀಯ ಆಡಳಿತ",
                    "why_in_news": "ರಾಜ್ಯದ 5,950 ಗ್ರಾಮ ಪಂಚಾಯಿತಿಗಳಲ್ಲಿ ಕಡ್ಡಾಯವಾಗಿ ತ್ರೈಮಾಸಿಕ ಗ್ರಾಮ ಸಭೆಗಳನ್ನು ನಡೆಸಿ ಸಾಮಾಜಿಕ ಲೆಕ್ಕಪರಿಶೋಧನೆ (Social Audit) ನಡೆಸುವಂತೆ ಗ್ರಾಮೀಣಾಭಿವೃದ್ಧಿ ಇಲಾಖೆ ಆದೇಶಿಸಿದೆ.",
                    "static_points": [
                        "<b>73ನೇ ಸಂವಿಧಾನ ತಿದ್ದುಪಡಿ 1992:</b> ಭಾಗ IX (ವಿಧಿಗಳು 243 ರಿಂದ 243-O) ಮತ್ತು 11ನೇ ವೇಳಾಪಟ್ಟಿ (29 ವಿಷಯಗಳು).",
                        "<b>ಕರ್ನಾಟಕ ಕಾಯ್ದೆ:</b> ಕರ್ನಾಟಕ ಪಂಚಾಯತ್ ರಾಜ್ ಕಾಯ್ದೆ 1993 (ರಮೇಶ್ ಕುಮಾರ್ ಸಮಿತಿ ಶಿಫಾರಸಿನಂತೆ 2015ರಲ್ಲಿ ಗ್ರಾಮ ಸ್ವರಾಜ್ ಕಾಯ್ದೆ ಎಂದು ಮರುನಾಮಕರಣ).",
                        "<b>ಮೂರು ಹಂತಗಳ ವ್ಯವಸ್ಥೆ:</b> ಗ್ರಾಮ ಪಂಚಾಯಿತಿ, ತಾಲೂಕು ಪಂಚಾಯಿತಿ ಮತ್ತು ಜಿಲ್ಲಾ ಪಂಚಾಯಿತಿ.",
                        "<b>ಗ್ರಾಮ ಸಭೆ (ವಿಧಿ 243A):</b> ಗ್ರಾಮದ ಎಲ್ಲಾ ನೋಂದಾಯಿತ ಮತದಾರರನ್ನು ಒಳಗೊಂಡಿರುವ ಏಕೈಕ ಶಾಶ್ವತ ಶಾಸನಬದ್ಧ ಸಂಸ್ಥೆ."
                    ],
                    "exam_points": [
                        "ಕರ್ನಾಟಕದಲ್ಲಿ ಸ್ಥಳೀಯ ಸಂಸ್ಥೆಗಳಲ್ಲಿ ಮಹಿಳೆಯರಿಗೆ ಶೇ. 50 ರಷ್ಟು ಮೀಸಲಾತಿ ನೀಡಲಾಗಿದೆ.",
                        "ರಾಜ್ಯ ಚುನಾವಣಾ ಆಯೋಗ (ವಿಧಿ 243K) ಸ್ಥಳೀಯ ಸಂಸ್ಥೆಗಳ ಚುನಾವಣೆ ನಡೆಸುತ್ತದೆ."
                    ],
                    "trap": "ಗ್ರಾಮ ಸಭೆಯು ಕೇವಲ ಮನೆಯ ಯಜಮಾನರ ಸಭೆಯಲ್ಲ; ಗ್ರಾಮ ಪಂಚಾಯಿತಿಯ ಮತದಾರರ ಪಟ್ಟಿಯಲ್ಲಿರುವ ಪ್ರತಿಯೊಬ್ಬ ವ್ಯಕ್ತಿಯೂ ಗ್ರಾಮ ಸಭೆಯ ಸದಸ್ಯರಾಗಿರುತ್ತಾರೆ.",
                    "state_angle": "ಕರ್ನಾಟಕದಲ್ಲಿ 1980ರ ದಶಕದಲ್ಲಿ ಅಬ್ದುಲ್ ನಜೀರ್ ಸಾಬ್ ಅವರ ಕಾಲದಲ್ಲೇ ಅಧಿಕಾರ ವಿಕೇಂದ್ರೀಕರಣಕ್ಕೆ ಮುನ್ನುಡಿ ಬರೆಯಲಾಯಿತು."
                },
                {
                    "title": "ರಾಜ್ಯ ಅಭಿವೃದ್ಧಿ ಸಾಲಗಳು (SDL) ಮತ್ತು ವಿಧಿ 293 ರ ಸಾಲ ಮಿತಿ",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೩ · ಸಾರ್ವಜನಿಕ ಹಣಕಾಸು & ರಾಜ್ಯ ಆರ್ಥಿಕತೆ",
                    "why_in_news": "ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಆರ್ಥಿಕ ಇಲಾಖೆಯು ಮುಕ್ತ ಮಾರುಕಟ್ಟೆಯಿಂದ ಪಡೆದ ಅಭಿವೃದ್ಧಿ ಸಾಲಗಳ ಮರುಪಾವತಿ ಅಧಿಸೂಚನೆ ಹೊರಡಿಸಿದೆ.",
                    "static_points": [
                        "<b>ವಿಧಿ 293:</b> ರಾಜ್ಯಗಳು ಭಾರತದ ಭೂಪ್ರದೇಶದೊಳಗೆ ಮಾತ್ರ ಸಂಚಿತ ನಿಧಿಯ ಭದ್ರತೆಯ ಮೇಲೆ ಸಾಲ ಪಡೆಯಬಹುದು.",
                        "<b>ಕೇಂದ್ರದ ಅನುಮತಿ:</b> ವಿಧಿ 293(3) ಅನ್ವಯ ಕೇಂದ್ರದ ಸಾಲ ಬಾಕಿ ಇದ್ದರೆ, ಹೊಸ ಸಾಲಕ್ಕೆ ಕೇಂದ್ರದ ಪೂರ್ವಾನುಮತಿ ಕಡ್ಡಾಯ.",
                        "<b>ಕರ್ನಾಟಕ ವಿತ್ತೀಯ ಜವಾಬ್ದಾರಿ ಕಾಯ್ದೆ (KFRA 2002):</b> ವಿತ್ತೀಯ ಕೊರತೆಯನ್ನು GSDP ಯ ಶೇ. 3 ರ ಒಳಗೆ ಮತ್ತು ಸಾಲದ ಪ್ರಮಾಣವನ್ನು ಶೇ. 25 ರ ಒಳಗೆ ಕಾಯ್ದುಕೊಳ್ಳುವುದು ಕಡ್ಡಾಯ."
                    ],
                    "exam_points": [
                        "ಆರ್‌ಬಿಐ ಇ-ಕುಬೇರ್ ವೇದಿಕೆಯ ಮೂಲಕ ರಾಜ್ಯ ಅಭಿವೃದ್ಧಿ ಸಾಲಗಳ ಹರಾಜು ನಡೆಸಲಾಗುತ್ತದೆ.",
                        "ವಿಧಿ 292 ಕೇಂದ್ರ ಸರ್ಕಾರದ ಸಾಲಗಳಿಗೆ ಅನ್ವಯಿಸಿದರೆ, ವಿಧಿ 293 ರಾಜ್ಯಗಳ ಸಾಲಕ್ಕೆ ಅನ್ವಯಿಸುತ್ತದೆ."
                    ],
                    "trap": "ರಾಜ್ಯ ಸರ್ಕಾರಗಳು ವಿದೇಶಗಳಿಂದ ನೇರವಾಗಿ ಸಾಲ ಪಡೆಯಲು ಸಂವಿಧಾನದಲ್ಲಿ ಅವಕಾಶವಿಲ್ಲ (ಕೇಂದ್ರದ ಮೂಲಕವೇ ಪಡೆಯಬೇಕು).",
                    "state_angle": "ಕರ್ನಾಟಕವು ಸತತ ಎರಡು ದಶಕಗಳಿಂದ ತನ್ನ ವಿತ್ತೀಯ ಕೊರತೆಯನ್ನು ಶೇ.3ರ ಮಿತಿಯೊಳಗೆ ಕಾಯ್ದುಕೊಂಡು ಬಂದಿದೆ."
                },
                {
                    "title": "ನೇರ ನಗದು ವರ್ಗಾವಣೆ (DBT): ಗೃಹಲಕ್ಷ್ಮಿ ಮತ್ತು ಅನ್ನಭಾಗ್ಯ ವಿಶ್ಲೇಷಣೆ",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೨ · ಸಾಮಾಜಿಕ ನ್ಯಾಯ & ಕಲ್ಯಾಣ ಯೋಜನೆಗಳು",
                    "why_in_news": "ಆಡಳಿತಾತ್ಮಕ ಅಧ್ಯಯನಗಳ ಪ್ರಕಾರ ಗೃಹಲಕ್ಷ್ಮಿ ಯೋಜನೆಯಡಿ ಮಹಿಳೆಯರ ಖಾತೆಗೆ ಜಮೆಯಾಗುವ ಮಾಸಿಕ DBT ಹಣವು ಗ್ರಾಮೀಣ ಆರ್ಥಿಕತೆಯನ್ನು ಗಣನೀಯವಾಗಿ ಚೇತರಿಸಿದೆ.",
                    "static_points": [
                        "<b>ಸಾಂವಿಧಾನಿಕ ತತ್ವ:</b> ಸಂವಿಧಾನದ ರಾಜ್ಯ ನೀತಿ ನಿರ್ದೇಶಕ ತತ್ವಗಳ ವಿಧಿ 38, 39 ಮತ್ತು 41 (ಕಲ್ಯಾಣ ರಾಜ್ಯ ಪರಿಕಲ್ಪನೆ).",
                        "<b>ತಂತ್ರಜ್ಞಾನ ಚೌಕಟ್ಟು:</b> ಜಾಮ್ ಟ್ರಿನಿಟಿ (Jan Dhan, Aadhaar, Mobile) ಮತ್ತು AePS ಮೂಲಕ ಸೋರಿಕೆಯಿಲ್ಲದ ಹಣ ವರ್ಗಾವಣೆ.",
                        "<b>ಆಹಾರ ಭದ್ರತೆ:</b> ರಾಷ್ಟ್ರೀಯ ಆಹಾರ ಭದ್ರತಾ ಕಾಯ್ದೆ (NFSA) 2013ರ ಅಡಿ ಪ್ರತಿ ಫಲಾನುಭವಿಗೆ ಆಹಾರ ಧಾನ್ಯ ಖಾತರಿ."
                    ],
                    "exam_points": [
                        "ಗೃಹಲಕ್ಷ್ಮಿ: ಮನೆಯ ಯಜಮಾನಿಗೆ ಮಾಸಿಕ ₹2,000 ನೇರ ನಗದು ವರ್ಗಾವಣೆ.",
                        "ಅನ್ನಭಾಗ್ಯ: ಕೇಂದ್ರದ 5 ಕೆಜಿ ಉಚಿತ ಅಕ್ಕಿ ಜೊತೆಗೆ ರಾಜ್ಯದಿಂದ ಹೆಚ್ಚುವರಿ 5 ಕೆಜಿ ಅಕ್ಕಿ (ಅಥವಾ ನಗದು)."
                    ],
                    "state_angle": "ಕರ್ನಾಟಕವು ದಕ್ಷಿಣ ಭಾರತದಲ್ಲೇ ಅತಿ ಹೆಚ್ಚು DBT ವರ್ಗಾವಣೆ ನಡೆಸುವ ರಾಜ್ಯಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ."
                },
                {
                    "title": "73ನೇ ಅಖಿಲ ಭಾರತ ಸಹಕಾರ ಸಪ್ತಾಹ ಮತ್ತು ಕಣಗಿನಹಾಳ ಮೈಲಿಗಲ್ಲು",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೧ & ೨ · ಸಹಕಾರ ಚಳವಳಿ",
                    "why_in_news": "ಕರ್ನಾಟಕದಲ್ಲಿ ಸಹಕಾರ ಸಪ್ತಾಹದ ಅಂಗವಾಗಿ ರೈತರಿಗೆ ಶೂನ್ಯ ಬಡ್ಡಿ ದರದ ಕೃಷಿ ಸಾಲ ವಿತರಣೆ ಮತ್ತು ಸ್ತ್ರೀಶಕ್ತಿ ಸಂಘಗಳ ಸಾಧನೆಗಳನ್ನು ಶ್ಲಾಘಿಸಲಾಗಿದೆ.",
                    "static_points": [
                        "<b>97ನೇ ಸಂವಿಧಾನ ತಿದ್ದುಪಡಿ (2011):</b> ವಿಧಿ 19(1)(c) ಅಡಿ ಸಹಕಾರ ಸಂಘ ರಚನೆ ಮೂಲಭೂತ ಹಕ್ಕು; ವಿಧಿ 43B ರಾಜ್ಯ ನೀತಿ ನಿರ್ದೇಶಕ ತತ್ವ; ಭಾಗ IX-B ಸೇರ್ಪಡೆ.",
                        "<b>ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ತೀರ್ಪು (2021):</b> ರಾಜ್ಯಗಳ ಅನುಮೋದನೆ ಇಲ್ಲದ ಕಾರಣ, ಭಾಗ IX-B ಕೇವಲ ಬಹು-ರಾಜ್ಯ ಸಹಕಾರ ಸಂಘಗಳಿಗೆ ಮಾತ್ರ ಅನ್ವಯಿಸುತ್ತದೆ ಎಂದು ತೀರ್ಪು ನೀಡಿತು.",
                        "<b>ಕರ್ನಾಟಕದ ಮೈಲಿಗಲ್ಲು:</b> ಭಾರತದ ಮೊದಲ ಪ್ರಾಥಮಿಕ ಕೃಷಿ ಪತ್ತಿನ ಸಹಕಾರ ಸಂಘ 1905ರಲ್ಲಿ ಗದಗ ಜಿಲ್ಲೆಯ ಕಣಗಿನಹಾಳದಲ್ಲಿ ಸಿದ್ದನಗೌಡ ಪಾಟೀಲರ ನೇತೃತ್ವದಲ್ಲಿ ಸ್ಥಾಪನೆಯಾಯಿತು."
                    ],
                    "exam_points": [
                        "ಗದಗ ಜಿಲ್ಲೆಯನ್ನು 'ಭಾರತದ ಸಹಕಾರ ಚಳವಳಿಯ ತೊಟ್ಟಿಲು' ಎಂದು ಕರೆಯಲಾಗುತ್ತದೆ.",
                        "ಕೇಂದ್ರದಲ್ಲಿ 2021ರಲ್ಲಿ ಪ್ರತ್ಯೇಕ ಸಹಕಾರ ಸಚಿವಾಲಯ ರಚನೆಯಾಯಿತು."
                    ],
                    "trap": "ಸಹಕಾರ ಸಂಘಗಳು ರಾಜ್ಯ ಪಟ್ಟಿಯ ನಮೂದು 32ರಲ್ಲಿವೆ; ಬಹು-ರಾಜ್ಯ ಸಹಕಾರ ಸಂಘಗಳು ಕೇಂದ್ರ ಪಟ್ಟಿಯ ನಮೂದು 44ರಲ್ಲಿವೆ."
                },
                {
                    "title": "ಹಸಿರು ಪಟಾಕಿ, ವಾಯು ಗುಣಮಟ್ಟ ಮಾನಿಟರಿಂಗ್ ಮತ್ತು ಸಿಪಿಸಿಬಿ",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೩ · ಪರಿಸರ ಮಾಲಿನ್ಯ ನಿಯಂತ್ರಣ",
                    "why_in_news": "ಹಬ್ಬದ ನಂತರ ವಾಯು ಗುಣಮಟ್ಟ ಕುಸಿತದ ಹಿನ್ನೆಲೆಯಲ್ಲಿ ಹೈಕೋರ್ಟ್ ಕಳವಳ ವ್ಯಕ್ತಪಡಿಸಿದ್ದು, ಮಾಲಿನ್ಯ ನಿಯಂತ್ರಣ ಮಂಡಳಿಯ ವರದಿ ಪರಿಶೀಲಿಸಿದೆ.",
                    "static_points": [
                        "<b>ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ತೀರ್ಪು (ಅರ್ಜುನ್ ಗೋಪಾಲ್ ಪ್ರಕರಣ 2018):</b> ಸಾಂಪ್ರದಾಯಿಕ ಪಟಾಕಿ ನಿಷೇಧಿಸಿ, CSIR-NEERI ಅಭಿವೃದ್ಧಿಪಡಿಸಿದ ಹಸಿರು ಪಟಾಕಿಗಳಿಗೆ (SWAS, STAR, SAFAL) ಮಾತ್ರ ಅನುಮತಿ ನೀಡಲಾಯಿತು.",
                        "<b>CPCB ಸಂಸ್ಥೆ:</b> ಜಲ ಕಾಯ್ದೆ 1974ರ ಅಡಿ ಸ್ಥಾಪನೆಯಾಗಿದ್ದು, ವಾಯು ಕಾಯ್ದೆ 1981ರ ಅಡಿಯಲ್ಲೂ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ.",
                        "<b>NAQI ಮಾಲಿನ್ಯಕಾರಕಗಳು:</b> 8 ಪ್ರಮುಖ ಮಾಲಿನ್ಯಕಾರಕಗಳು (PM10, PM2.5, NO2, SO2, CO, O3, NH3, Pb) ಮತ್ತು 6 ಗುಣಮಟ್ಟ ವರ್ಗಗಳು."
                    ],
                    "trap": "CPCB ಜಲ ಕಾಯ್ದೆ 1974ರ ಅಡಿ ಸ್ಥಾಪನೆಯಾದ ಸಂಸ್ಥೆ, ಪರಿಸರ ಸಂರಕ್ಷಣೆ ಕಾಯ್ದೆ 1986ರ ಅಡಿಯಲ್ಲ."
                },
                {
                    "title": "ಕನ್ನಡ ಶಾಸ್ತ್ರೀಯ ಭಾಷಾ ಸ್ಥಾನಮಾನ ಮತ್ತು ಸಿಐಐಎಲ್",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೧ · ಕರ್ನಾಟಕ ಇತಿಹಾಸ, ಭಾಷೆ & ಸಾಹಿತ್ಯ",
                    "why_in_news": "ಕೇಂದ್ರ ಸರ್ಕಾರವು ಇತ್ತೀಚೆಗೆ 5 ಹೊಸ ಭಾಷೆಗಳಿಗೆ ಶಾಸ್ತ್ರೀಯ ಭಾಷಾ ಸ್ಥಾನಮಾನ ನೀಡಿದ್ದು, ಮೈಸೂರಿನ ಕೇಂದ್ರೀಯ ಶಾಸ್ತ್ರೀಯ ಕನ್ನಡ ಅಧ್ಯಯನ ಕೇಂದ್ರಕ್ಕೆ (CICK) ಸ್ವಾಯತ್ತತೆ ನೀಡುವ ಬೇಡಿಕೆ ಕೇಳಿಬಂದಿದೆ.",
                    "static_framework": [
                        "<b>ಶಾಸ್ತ್ರೀಯ ಭಾಷೆಗಳು (ಒಟ್ಟು 11):</b> ತಮಿಳು (2004), ಸಂಸ್ಕೃತ (2005), ಕನ್ನಡ (2008), ತೆಲುಗು (2008), ಮಲಯಾಳಂ (2013), ಒಡಿಯಾ (2014); ಹೊಸದಾಗಿ ಮರಾಠಿ, ಪಾಲಿ, ಪ್ರಾಕೃತ, ಅಸ್ಸಾಮಿ, ಬಂಗಾಳಿ (2024).",
                        "<b>ಮಾನದಂಡಗಳು:</b> 1,500 ರಿಂದ 2,000 ವರ್ಷಗಳ ಪ್ರಾಚೀನ ಇತಿಹಾಸ/ಗ್ರಂಥಗಳು; ಮೌಲ್ಯಯುತ ಸಾಹಿತ್ಯಕ ಪರಂಪರೆ; ಮೂಲ ಸಾಹಿತ್ಯಕ ಸಂಪ್ರದಾಯ.",
                        "<b>ಹಲ್ಮಿಡಿ ಶಾಸನ:</b> ಕ್ರಿ.ಶ. ಸುಮಾರು 450ರ ಕದಂಬ ರಾಜ ಕಾಕುಸ್ಥವರ್ಮನ ಕಾಲದ ಶಾಸನ (ಹಾಸನ ಜಿಲ್ಲೆಯ ಬೇಲೂರು ತಾಲೂಕು)."
                    ],
                    "exam_points": [
                        "ಶ್ರೀವಿಜಯನ 'ಕವಿರಾಜಮಾರ್ಗ' (9ನೇ ಶತಮಾನ, ಅಮೋಘವರ್ಷ ನೃಪತುಂಗನ ಕಾಲ) ಕನ್ನಡದ ಉಪಲಬ್ಧ ಮೊದಲ ಲಕ್ಷಣ ಗ್ರಂಥವಾಗಿದೆ.",
                        "CICK ಮೈಸೂರಿನ ಕೇಂದ್ರೀಯ ಭಾರತೀಯ ಭಾಷೆಗಳ ಸಂಸ್ಥೆಯ (CIIL) ಅಡಿಯಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ."
                    ],
                    "trap": "ಕನ್ನಡಕ್ಕೆ 2008ರಲ್ಲಿ ತೆಲುಗಿನೊಂದಿಗೆ ಶಾಸ್ತ್ರೀಯ ಸ್ಥಾನಮಾನ ಸಿಕ್ಕಿತು (ತಮಿಳಿಗೆ 2004ರಲ್ಲಿ ಸಿಕ್ಕಿತು)."
                },
                {
                    "title": "ಕೆರೆಗಳ ಒತ್ತುವರಿ ತೆರವು ಮತ್ತು KTCDA ಪ್ರಾಧಿಕಾರದ ನಿಯಮಗಳು",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೧ · ಜಲಮೂಲಗಳು & ನಗರಾಭಿವೃದ್ಧಿ",
                    "why_in_news": "ರಾಜಕಾಲುವೆ ಮತ್ತು ಕೆರೆಗಳ ಬಫರ್ ವಲಯದಲ್ಲಿನ ಅನಧಿಕೃತ ಒತ್ತುವರಿಗಳನ್ನು ತೆರವುಗೊಳಿಸಲು ಹೈಕೋರ್ಟ್ ಕಟ್ಟುನಿಟ್ಟಿನ ಗಡುವು ವಿಧಿಸಿದೆ.",
                    "static_points": [
                        "<b>ಶಾಸನಬದ್ಧ ಪ್ರಾಧಿಕಾರ:</b> ಕರ್ನಾಟಕ ಕೆರೆ ಸಂರಕ್ಷಣೆ ಮತ್ತು ಅಭಿವೃದ್ಧಿ ಪ್ರಾಧಿಕಾರ (KTCDA) ಕಾಯ್ದೆ 2014ರ ಅಡಿ ಸ್ಥಾಪನೆ.",
                        "<b>ಬಫರ್ ವಲಯ ನಿಯಮ:</b> ಕೆರೆಯ ಪೂರ್ಣ ನೀರಿನ ಮಟ್ಟದಿಂದ (FTL) 30 ಮೀಟರ್ ಮತ್ತು ಪ್ರಾಥಮಿಕ ರಾಜಕಾಲುವೆಯಿಂದ 50 ಮೀಟರ್ ಬಫರ್ ವಲಯ.",
                        "<b>ಸಾರ್ವಜನಿಕ ಟ್ರಸ್ಟ್ ಸಿದ್ಧಾಂತ (Public Trust Doctrine):</b> ನೈಸರ್ಗಿಕ ಜಲಮೂಲಗಳು ಸಾರ್ವಜನಿಕರ ಹಿತಕ್ಕಾಗಿ ಸರ್ಕಾರದ ವಶದಲ್ಲಿರುವ ಆಸ್ತಿಗಳು."
                    ],
                    "state_angle": "ಕೆಂಪೇಗೌಡರ ಕಾಲದಲ್ಲಿ ಬೆಂಗಳೂರು ಸುತ್ತಮುತ್ತ 800ಕ್ಕೂ ಹೆಚ್ಚು ಪರಸ್ಪರ ಸಂಪರ್ಕಿತ ಕೆರೆಗಳ ಸರಣಿ ವ್ಯವಸ್ಥೆ (Cascade system) ಇತ್ತು."
                },
                {
                    "title": "ಪಾವಗಡ ಸೌರ ಪಾರ್ಕ್ ಮತ್ತು ಕರ್ನಾಟಕ ನವೀಕರಿಸಬಹುದಾದ ಇಂಧನ ನೀತಿ",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೩ · ಇಂಧನ ಮೂಲಸೌಕರ್ಯ & ಸೌರಶಕ್ತಿ",
                    "why_in_news": "ಪಾವಗಡ ಅಲ್ಟ್ರಾ ಮೆಗಾ ಸೋಲಾರ್ ಪಾರ್ಕ್ ಯಶಸ್ಸಿನ ಹಿನ್ನೆಲೆಯಲ್ಲಿ ರಾಜ್ಯದ ನವೀಕರಿಸಬಹುದಾದ ಇಂಧನ ಸಾಮರ್ಥ್ಯ 16,500 ಮೆಗಾವಾಟ್ ಮೈಲಿಗಲ್ಲು ತಲುಪಿದೆ.",
                    "static_points": [
                        "<b>ಶಕ್ತಿ ಸ್ಥಳ (ಪಾವಗಡ):</b> ತುಮಕೂರು ಜಿಲ್ಲೆಯ ಪಾವಗಡದಲ್ಲಿರುವ 2,050 ಮೆಗಾವಾಟ್ ಸಾಮರ್ಥ್ಯದ ವಿಶ್ವದ ಅತಿ ದೊಡ್ಡ ಸೌರ ಪಾರ್ಕ್‌ಗಳಲ್ಲಿ ಒಂದು.",
                        "<b>ರೈತರ ಗುತ್ತಿಗೆ ಮಾದರಿ:</b> ಭೂಸ್ವಾಧೀನ ಮಾಡಿಕೊಳ್ಳದೆ ರೈತರಿಗೆ ವಾರ್ಷಿಕ ಗುತ್ತಿಗೆ ಬಾಡಿಗೆ ನೀಡುವ ನವೀನ ಮಾದರಿ.",
                        "<b>ಕ್ರೆಡಲ್ (KREDL):</b> ಕರ್ನಾಟಕ ನವೀಕರಿಸಬಹುದಾದ ಇಂಧನ ಅಭಿವೃದ್ಧಿ ನಿಯಮಿತ ನೋಡಲ್ ಏಜೆನ್ಸಿಯಾಗಿದೆ.",
                        "<b>ರಾಜ್ಯ ನೀತಿ:</b> 2022-2027ರ ಇಂಧನ ನೀತಿಯಡಿ ಹೆಚ್ಚುವರಿ 10 ಗಿಗಾವಾಟ್ ಹಸಿರು ಇಂಧನ ಉತ್ಪಾದನೆ ಗುರಿ."
                    ],
                    "exam_points": [
                        "ಸೌರ ವಿದ್ಯುತ್ ಸ್ಥಾಪಿತ ಸಾಮರ್ಥ್ಯದಲ್ಲಿ ಕರ್ನಾಟಕವು ದೇಶದ ಮೊದಲ ಮೂರು ರಾಜ್ಯಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ.",
                        "ಪಾವಗಡವನ್ನು ಬರಪೀಡಿತ ಮತ್ತು ವರ್ಷದಲ್ಲಿ 300ಕ್ಕೂ ಹೆಚ್ಚು ದಿನ ಬಿಸಿಲಿರುವ ಕಾರಣಕ್ಕೆ ಆಯ್ಕೆ ಮಾಡಲಾಯಿತು."
                    ]
                },
                {
                    "title": "ಯುಎಪಿಎ (UAPA) ಕಾಯ್ದೆ ಮತ್ತು ನ್ಯಾಯಾಧಿಕರಣದ ಪ್ರಕ್ರಿಯೆ",
                    "syllabus": "ಸಾಮಾನ್ಯ ಅಧ್ಯಯನ - ೨ · ಆಂತರಿಕ ಭದ್ರತೆ & ಕಾಯ್ದೆಗಳು",
                    "why_in_news": "ಕಾನೂನುಬಾಹಿರ ಚಟುವಟಿಕೆಗಳ (ತಡೆ) ಕಾಯ್ದೆ 1967ರ ಅಡಿಯಲ್ಲಿ ನಿರ್ದಿಷ್ಟ ಸಂಘಟನೆಯ ಮೇಲಿನ ನಿಷೇಧವನ್ನು ಕೇಂದ್ರ ಗೃಹ ಸಚಿವಾಲಯ 5 ವರ್ಷಗಳ ಕಾಲ ವಿಸ್ತರಿಸಿದೆ.",
                    "static_points": [
                        "<b>ಕಲಂ 3:</b> ಕೇಂದ್ರ ಸರ್ಕಾರವು ಯಾವುದೇ ಸಂಘವನ್ನು ‘ಕಾನೂನುಬಾಹಿರ ಸಂಘ’ ಎಂದು ಅಧಿಸೂಚನೆ ಮೂಲಕ ಘೋಷಿಸಬಹುದು.",
                        "<b>ಕಲಂ 4 (ನ್ಯಾಯಾಧಿಕರಣ):</b> ಈ ಅಧಿಸೂಚನೆಯನ್ನು 30 ದಿನಗಳೊಳಗೆ ಹೈಕೋರ್ಟ್ ನ್ಯಾಯಾಧೀಶರ ನೇತೃತ್ವದ ನ್ಯಾಯಾಧಿಕರಣಕ್ಕೆ ಕಳುಹಿಸಬೇಕು; ನ್ಯಾಯಾಧಿಕರಣ ದೃಢೀಕರಿಸಿದ ನಂತರವೇ ನಿಷೇಧ ಶಾಶ್ವತವಾಗುತ್ತದೆ.",
                        "<b>2019ರ ತಿದ್ದುಪಡಿ:</b> ವ್ಯಕ್ತಿಗಳನ್ನೂ ‘ಭಯೋತ್ಪಾದಕ’ ಎಂದು ಘೋಷಿಸುವ ಅಧಿಕಾರವನ್ನು ಕೇಂದ್ರ ಸರ್ಕಾರಕ್ಕೆ ನೀಡಲಾಯಿತು (ನಾಲ್ಕನೇ ವೇಳಾಪಟ್ಟಿ)."
                    ],
                    "trap": "ಕೇಂದ್ರದ ಘೋಷಣೆಯು ನ್ಯಾಯಾಧಿಕರಣದ ದೃಢೀಕರಣವಿಲ್ಲದೆ ಶಾಶ್ವತ ಕಾನೂನು ಮಾನ್ಯತೆ ಪಡೆಯುವುದಿಲ್ಲ."
                }
            ],
            "kn_oneliners": [
                "<b>ನವೆಂಬರ್ 14:</b> ಜವಾಹರಲಾಲ್ ನೆಹರೂ ಜನ್ಮದಿನ (ರಾಷ್ಟ್ರೀಯ ಮಕ್ಕಳ ದಿನಾಚರಣೆ).",
                "<b>ವಂದೇ ಭಾರತ್ ಎಕ್ಸ್‌ಪ್ರೆಸ್:</b> ಮೊದಲ ರೈಲು 2019 ಫೆಬ್ರವರಿಯಲ್ಲಿ (ನವದೆಹಲಿ-ವಾರಾಣಸಿ) ಆರಂಭ; ತಯಾರಿಕೆ: ICF ಚೆನ್ನೈ.",
                "<b>ಕೊಂಕಣ ರೈಲ್ವೆ ನಿಗಮ:</b> 1990ರಲ್ಲಿ ಸ್ಥಾಪನೆ; ರೋಹಾ (ಮಹಾರಾಷ್ಟ್ರ)ದಿಂದ ತೋಕೂರು (ಕರ್ನಾಟಕ)ವರೆಗೆ 741 ಕಿ.ಮೀ. ಮಾರ್ಗ.",
                "<b>ರಾಷ್ಟ್ರೀಯ ವಾಯು ಗುಣಮಟ್ಟ ಸೂಚ್ಯಂಕ (NAQI):</b> 2014ರಲ್ಲಿ CPCBಯಿಂದ ಆರಂಭ; 6 ವರ್ಗಗಳು ಮತ್ತು 8 ಪ್ರಮುಖ ಮಾಲಿನ್ಯಕಾರಕಗಳು.",
                "<b>ಮೈಸೂರು ‘ಕಾಸ್ಮೋಸ್’ ತಾರಾಲಯ:</b> IIA (DST ಅಧೀನ) ಸಂಸ್ಥೆಯಿಂದ ನಿರ್ಮಾಣಗೊಂಡ ಅತ್ಯಾಧುನಿಕ LED ಗುಮ್ಮಟ ತಾರಾಲಯ.",
                "<b>ಒಂದು ರಾಷ್ಟ್ರ ಒಂದು ಚಂದಾದಾರಿಕೆ (ONOS):</b> ಕೇಂದ್ರ ಸಂಪುಟ ನವೆಂಬರ್ 2024ರಲ್ಲಿ ಅನುಮೋದಿಸಿದ್ದು, INFLIBNET ಮೂಲಕ ಜಾರಿ.",
                "<b>ಬಾಹ್ಯಾಕಾಶ ಸುಧಾರಣೆಗಳು:</b> ಖಾಸಗಿ ಸಹಭಾಗಿತ್ವಕ್ಕೆ IN-SPACe ಏಕಗವಾಕ್ಷಿ ಅನುಮೋದನೆ ಸಂಸ್ಥೆಯಾಗಿದ್ದರೆ, NSIL ವಾಣಿಜ್ಯ ವಿಭಾಗವಾಗಿದೆ.",
                "<b>ಹಲ್ಮಿಡಿ ಶಾಸನ:</b> ಹಾಸನ ಜಿಲ್ಲೆಯ ಬೇಲೂರಿನಲ್ಲಿ ಪತ್ತೆಯಾದ ಕ್ರಿ.ಶ. 450ರ ಕದಂಬರ ಕಾಲದ ಮೊದಲ ಕನ್ನಡ ಶಾಸನ."
            ],
            "kn_mcqs": [
                {
                    "question": "ಕಾವೇರಿ ನದಿಯ ಕೆಳಗಿನ ಉಪನದಿಗಳಲ್ಲಿ ಯಾವುದು ಎಡದಂಡೆಯ (Left Bank) ಉಪನದಿಯಾಗಿದೆ?",
                    "opt_a": "ಕಬಿನಿ",
                    "opt_b": "ಹೇಮಾವತಿ",
                    "opt_c": "ಭವಾನಿ",
                    "opt_d": "ಲಕ್ಷ್ಮಣತೀರ್ಥ",
                    "answer": "B",
                    "explanation": "ಹೇಮಾವತಿ, ಹಾರಂಗಿ, ಶಿಂಷಾ ಮತ್ತು ಅರ್ಕಾವತಿ ಕಾವೇರಿಯ ಎಡದಂಡೆ ಉಪನದಿಗಳು. ಕಬಿನಿ, ಭವಾನಿ, ನೊಯ್ಯಲ್, ಅಮರಾವತಿ, ಲಕ್ಷ್ಮಣತೀರ್ಥ ಬಲದಂಡೆ ಉಪನದಿಗಳು."
                },
                {
                    "question": "ಮೆಟ್ರೊ ರೈಲು ಸುರಕ್ಷತಾ ಆಯುಕ್ತರು (CMRS) ಈ ಕೆಳಗಿನ ಯಾವ ಸಚಿವಾಲಯದ ಆಡಳಿತಾತ್ಮಕ ನಿಯಂತ್ರಣಕ್ಕೆ ಒಳಪಡುತ್ತಾರೆ?",
                    "opt_a": "ಕೇಂದ್ರ ರೈಲ್ವೆ ಸಚಿವಾಲಯ",
                    "opt_b": "ವಸತಿ ಮತ್ತು ನಗರ ವ್ಯವಹಾರಗಳ ಸಚಿವಾಲಯ",
                    "opt_c": "ನಾಗರಿಕ ವಿಮಾನಯಾನ ಸಚಿವಾಲಯ",
                    "opt_d": "ರಸ್ತೆ ಸಾರಿಗೆ ಮತ್ತು ಹೆದ್ದಾರಿ ಸಚಿವಾಲಯ",
                    "answer": "C",
                    "explanation": "ಸ್ವತಂತ್ರ ತನಿಖೆ ಮತ್ತು ಸುರಕ್ಷತೆಗಾಗಿ CMRS ನಾಗರಿಕ ವಿಮಾನಯಾನ ಸಚಿವಾಲಯದ ರೈಲ್ವೆ ಸುರಕ್ಷತಾ ಆಯೋಗದ ಅಡಿಯಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಾರೆ."
                },
                {
                    "question": "ಭಾರತದ ಮೊದಲ ಪ್ರಾಥಮಿಕ ಕೃಷಿ ಪತ್ತಿನ ಸಹಕಾರ ಸಂಘವು 1905ರಲ್ಲಿ ಕರ್ನಾಟಕದ ಯಾವ ಗ್ರಾಮದಲ್ಲಿ ಸ್ಥಾಪನೆಯಾಯಿತು?",
                    "opt_a": "ಬೆಟಗೇರಿ",
                    "opt_b": "ಹುಲಕೋಟಿ",
                    "opt_c": "ಕಣಗಿನಹಾಳ",
                    "opt_d": "ಗಂಗಾಪುರ",
                    "answer": "C",
                    "explanation": "ಗದಗ ಜಿಲ್ಲೆಯ ಕಣಗಿನಹಾಳದಲ್ಲಿ ಸಿದ್ದನಗೌಡ ಪಾಟೀಲರ ನೇತೃತ್ವದಲ್ಲಿ 1904ರ ಸಹಕಾರಿ ಕಾಯ್ದೆಯಡಿ ಸ್ಥಾಪನೆಯಾಯಿತು."
                },
                {
                    "question": "97ನೇ ಸಂವಿಧಾನ ತಿದ್ದುಪಡಿ ಕಾಯ್ದೆಯ ಕುರಿತು ಕೆಳಗಿನ ಹೇಳಿಕೆಗಳನ್ನು ಪರಿಗಣಿಸಿ:",
                    "statements": [
                        "ಇದು ರಾಜ್ಯ ನೀತಿ ನಿರ್ದೇಶಕ ತತ್ವಗಳಲ್ಲಿ ವಿಧಿ 43B ಅನ್ನು ಸೇರಿಸಿತು.",
                        "2021ರ ತೀರ್ಪಿನಲ್ಲಿ ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ಭಾಗ IX-B ಅನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ರದ್ದುಗೊಳಿಸಿತು."
                    ],
                    "opt_a": "1 ಮಾತ್ರ",
                    "opt_b": "2 ಮಾತ್ರ",
                    "opt_c": "1 ಮತ್ತು 2 ಎರಡೂ",
                    "opt_d": "ಯಾವುದೂ ಅಲ್ಲ",
                    "answer": "A",
                    "explanation": "2ನೇ ಹೇಳಿಕೆ ತಪ್ಪು: ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ಕೇವಲ ರಾಜ್ಯಗಳೊಳಗಿನ ಸಹಕಾರ ಸಂಘಗಳಿಗೆ ಮಾತ್ರ ಭಾಗ IX-B ಅಸಿಂಧುಗೊಳಿಸಿತು; ಬಹು-ರಾಜ್ಯ ಸಹಕಾರ ಸಂಘಗಳಿಗೆ ಅದು ಮಾನ್ಯವಾಗಿದೆ."
                },
                {
                    "question": "ಕನ್ನಡದ ಅತ್ಯಂತ ಪ್ರಾಚೀನ ಶಾಸನವಾದ ಹಲ್ಮಿಡಿ ಶಾಸನವು (ಕ್ರಿ.ಶ. 450) ಯಾವ ರಾಜವಂಶಕ್ಕೆ ಸೇರಿದೆ?",
                    "opt_a": "ಬಾದಾಮಿ ಚಾಲುಕ್ಯರು",
                    "opt_b": "ಬನವಾಸಿಯ ಕದಂಬರು",
                    "opt_c": "ರಾಷ್ಟ್ರಕೂಟರು",
                    "opt_d": "ತಲಕಾಡಿನ ಗಂಗರು",
                    "answer": "B",
                    "explanation": "ಹಾಸನ ಜಿಲ್ಲೆಯ ಬೇಲೂರು ತಾಲೂಕಿನಲ್ಲಿ ದೊರೆತ ಹಲ್ಮಿಡಿ ಶಾಸನವು ಕದಂಬ ದೊರೆ ಕಾಕುಸ್ಥವರ್ಮನ ಕಾಲಕ್ಕೆ ಸೇರಿದೆ."
                }
            ]
        }

        html = self.engine.render_html("prajavani_crimson.html", context)
        self.engine.generate_pdf_from_html(html, output_path)
        logger.info(f"Generated Prajavani PDF: {output_path}")
        return output_path

    def run_daily_generation(self) -> Tuple[str, str]:
        today = self.get_today_str()
        print(f"Generating comprehensive daily PDFs for {today}...")
        hindu_pdf = self.generate_the_hindu_pdf(today)
        prajavani_pdf = self.generate_prajavani_pdf(today)
        return hindu_pdf, prajavani_pdf


if __name__ == "__main__":
    pipeline = NewspaperPDFPipeline()
    h, p = pipeline.run_daily_generation()
    print(f"Hindu: {h}\nPrajavani: {p}")
