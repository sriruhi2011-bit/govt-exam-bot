# setup_features.py
# Run this ONCE to create all feature files correctly
# Usage: python setup_features.py

import os

print("=" * 55)
print("   SETTING UP ALL NEW FEATURES")
print("=" * 55)

# ══════════════════════════════════════════
# FILE 1: extras.py
# ══════════════════════════════════════════

extras_code = '''# extras.py
# Extra daily content: History, Vocabulary, GK, Countdown, ELI5, Comparisons

import random
from datetime import datetime, date
from ai_engine import ai
from config.logger import setup_logger

logger = setup_logger("extras")

# ══════════════════════════════════════
# PRELIMS COUNTDOWN DATA
# Update these dates for current year
# ══════════════════════════════════════

EXAM_DATES = {
    "UPSC Prelims 2025": "2025-05-25",
    "UPSC Mains 2025": "2025-09-19",
    "SSC CGL 2025": "2025-06-15",
    "KPSC KAS Prelims 2025": "2025-06-22",
    "KPSC FDA/SDA 2025": "2025-07-20",
    "RBI Grade B 2025": "2025-08-10",
    "IBPS PO 2025": "2025-10-04",
}

# ══════════════════════════════════════
# DAILY STRATEGY TIPS
# ══════════════════════════════════════

STRATEGY_TIPS = [
    "Revise current affairs from the last 12 months. Focus on government schemes and international summits.",
    "Solve at least 50 MCQs daily from previous year papers. Analyze why you got wrong answers.",
    "Make short notes of today's news. Use keywords, not full sentences. Review them weekly.",
    "Focus on NCERT books for static GK. Class 6-12 covers 60%% of Prelims syllabus.",
    "Practice answer writing for 30 minutes daily. Even bullet points help build the habit.",
    "Read one editorial from The Hindu or Indian Express daily. Note 3 key arguments.",
    "Revise one subject's static portion today. Rotate subjects through the week.",
    "Attempt a full-length mock test this weekend. Analyze mistakes more than score.",
    "Map-based questions are increasing. Practice marking rivers, national parks on a blank map.",
    "Focus on linking current affairs with static GK. Examiners love connected questions.",
    "Create mnemonics for lists (Articles, Amendments, Committees). They save time in exam.",
    "Revise Government Schemes — name, ministry, launch year, target beneficiaries.",
    "Practice reading comprehension passages. Time yourself — 8 minutes per passage max.",
    "Study constitutional amendments from last 5 years. They are exam favorites.",
    "Review India's bilateral relations with neighboring countries. Focus on recent summits.",
    "Revise Art & Culture basics — classical dances, music forms, painting styles, GI tags.",
    "Environment questions are increasing. Focus on COP decisions, Ramsar sites, biosphere reserves.",
    "Economic Survey key highlights from last 2 years are important for Prelims.",
    "Practice Data Interpretation — read budget figures, economic indicators with understanding.",
    "Revise Science & Tech — space missions, defense tech, biotech developments of last year.",
    "International organizations — headquarters, heads, member countries, recent summits.",
    "Indian geography — major crops, soil types, climate zones. Use maps for revision.",
    "Focus on Acts passed by Parliament in the last 2 years. Know key provisions.",
    "Revise Panchayati Raj and Urban Local Bodies — 73rd and 74th Amendments thoroughly.",
    "Practice eliminating wrong options. In MCQs, elimination is as important as knowing the answer.",
    "Create a revision timetable. Spend 60%% time on revision, 40%% on new topics.",
    "Study landmark Supreme Court judgments from the last 3 years.",
    "Revise disaster management basics — NDRF, SDRF, Sendai Framework.",
    "Focus on India's trade agreements — RCEP, CEPA, FTAs signed recently.",
    "Mental health matters. Take a 30-minute break. A fresh mind learns better.",
]

# ══════════════════════════════════════
# ELI5 TOPICS
# ══════════════════════════════════════

ELI5_TOPICS = [
    "What is Repo Rate and how does it affect common people",
    "What is GDP and how is it calculated",
    "What is Fiscal Deficit and why it matters",
    "How does the GST system work in India",
    "What is the difference between Lok Sabha and Rajya Sabha",
    "What is a Money Bill vs Ordinary Bill",
    "How does the Election Commission conduct elections",
    "What is the role of the CAG (Comptroller and Auditor General)",
    "What is the difference between Fundamental Rights and DPSP",
    "How does the Supreme Court work — PIL, Appellate, Advisory",
    "What is Article 370 and what changed",
    "What is the National Green Tribunal",
    "How does RBI control inflation",
    "What is the difference between FDI and FII",
    "What is the Paris Agreement on climate change",
    "What is QUAD and why is it important for India",
    "What is Digital Rupee (CBDC) and how it works",
    "What is the difference between Current Account and Capital Account",
    "How does Panchayati Raj system work (3 tiers)",
    "What is Anti-Defection Law (10th Schedule)",
    "What is NITI Aayog and how it replaced Planning Commission",
    "What is Aadhaar and its legal basis",
    "How does the Indian Space Program (ISRO) work",
    "What is the National Education Policy (NEP) 2020",
    "What is One Nation One Election concept",
    "What is UPI and how India leads in digital payments",
    "What is PM KISAN scheme and how farmers benefit",
    "What is the Cauvery Water Dispute about",
    "What is the difference between National Park and Wildlife Sanctuary",
    "What is the Nuclear Triad and India's nuclear doctrine",
]

# ══════════════════════════════════════
# COMPARISON TOPICS
# ══════════════════════════════════════

COMPARISON_TOPICS = [
    "Fundamental Rights vs Directive Principles of State Policy (DPSP)",
    "Lok Sabha vs Rajya Sabha",
    "Governor vs President of India",
    "Money Bill vs Ordinary Bill vs Finance Bill",
    "National Park vs Wildlife Sanctuary vs Biosphere Reserve",
    "FDI vs FII vs FPI",
    "Fiscal Policy vs Monetary Policy",
    "NITI Aayog vs Planning Commission",
    "Written Constitution (India) vs Unwritten Constitution (UK)",
    "Unitary vs Federal system of government",
    "Fundamental Rights vs Legal Rights",
    "Parliamentary vs Presidential system",
    "Supreme Court vs High Court jurisdiction",
    "CAG vs Finance Commission",
    "Censure Motion vs No Confidence Motion",
    "Emergency under Article 352 vs 356 vs 360",
    "Revenue Expenditure vs Capital Expenditure",
    "CBI vs NIA vs ED — roles and differences",
    "Classical dances: Bharatanatyam vs Kathak vs Odissi",
    "Tropical Evergreen Forest vs Tropical Deciduous Forest",
]


class ExtraContent:

    def __init__(self):
        self.today = datetime.now()
        self.day = self.today.day
        self.month = self.today.strftime("%B")
        self.date_nice = self.today.strftime("%d %B %Y")
        self.day_name = self.today.strftime("%A")
        self.day_of_week = self.today.weekday()

    def this_day_in_history(self):
        """Post 1: This Day in History"""
        logger.info("Generating This Day in History...")

        prompt = f"""List 5 important historical events that happened on {self.day} {self.month} (any year).

Include:
- 2-3 events related to 