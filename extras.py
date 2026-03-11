# extras.py
# Extra daily content: History, Vocabulary, GK, Countdown, ELI5, Comparisons

import random
from datetime import datetime, date
from ai_engine import ai
from config.logger import setup_logger

logger = setup_logger("extras")

EXAM_DATES = {
    "UPSC Prelims 2025": "2025-05-25",
    "UPSC Mains 2025": "2025-09-19",
    "SSC CGL 2025": "2025-06-15",
    "KPSC KAS Prelims 2025": "2025-06-22",
    "KPSC FDA/SDA 2025": "2025-07-20",
    "RBI Grade B 2025": "2025-08-10",
    "IBPS PO 2025": "2025-10-04",
}

STRATEGY_TIPS = [
    "Revise current affairs from the last 12 months. Focus on government schemes and international summits.",
    "Solve at least 50 MCQs daily from previous year papers. Analyze why you got wrong answers.",
    "Make short notes of today's news. Use keywords, not full sentences. Review them weekly.",
    "Focus on NCERT books for static GK. Class 6-12 covers 60% of Prelims syllabus.",
    "Practice answer writing for 30 minutes daily. Even bullet points help build the habit.",
    "Read one editorial from The Hindu or Indian Express daily. Note 3 key arguments.",
    "Revise one subject's static portion today. Rotate subjects through the week.",
    "Attempt a full-length mock test this weekend. Analyze mistakes more than score.",
    "Map-based questions are increasing. Practice marking rivers, national parks on a blank map.",
    "Focus on linking current affairs with static GK. Examiners love connected questions.",
    "Create mnemonics for lists (Articles, Amendments, Committees). They save time in exam.",
    "Revise Government Schemes: name, ministry, launch year, target beneficiaries.",
    "Practice reading comprehension passages. Time yourself: 8 minutes per passage max.",
    "Study constitutional amendments from last 5 years. They are exam favorites.",
    "Review India's bilateral relations with neighboring countries. Focus on recent summits.",
    "Mental health matters. Take a 30-minute break. A fresh mind learns better.",
]

ELI5_TOPICS = [
    "What is Repo Rate and how does it affect common people",
    "What is GDP and how is it calculated",
    "What is Fiscal Deficit and why it matters",
    "How does the GST system work in India",
    "What is the difference between Lok Sabha and Rajya Sabha",
    "What is a Money Bill vs Ordinary Bill",
    "How does the Election Commission conduct elections",
    "What is the role of the CAG",
    "What is the difference between Fundamental Rights and DPSP",
    "How does the Supreme Court work: PIL, Appellate, Advisory",
    "What is Article 370 and what changed",
    "How does RBI control inflation",
    "What is the difference between FDI and FII",
    "What is the Paris Agreement on climate change",
    "What is QUAD and why is it important for India",
    "What is Digital Rupee (CBDC) and how it works",
    "How does Panchayati Raj system work (3 tiers)",
    "What is Anti-Defection Law (10th Schedule)",
    "What is NITI Aayog and how it replaced Planning Commission",
    "What is the Nuclear Triad and India's nuclear doctrine",
]

COMPARISON_TOPICS = [
    "Fundamental Rights vs Directive Principles of State Policy",
    "Lok Sabha vs Rajya Sabha",
    "Governor vs President of India",
    "Money Bill vs Ordinary Bill vs Finance Bill",
    "National Park vs Wildlife Sanctuary vs Biosphere Reserve",
    "FDI vs FII vs FPI",
    "Fiscal Policy vs Monetary Policy",
    "NITI Aayog vs Planning Commission",
    "Parliamentary vs Presidential system",
    "Supreme Court vs High Court jurisdiction",
    "Censure Motion vs No Confidence Motion",
    "Emergency under Article 352 vs 356 vs 360",
    "Revenue Expenditure vs Capital Expenditure",
    "CBI vs NIA vs ED: roles and differences",
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
        logger.info("Generating This Day in History...")
        prompt = f"List 5 important historical events that happened on {self.day} {self.month} (any year). Include 2-3 events related to India and 2-3 international events. Focus on events asked in UPSC/SSC exams. FORMAT: YEAR - Event description in 1 clear line. After the 5 events add: EXAM TIP: Which event is most frequently asked and why (1 line). Plain text only."
        content = ai.query(prompt, temperature=0.3, max_tokens=400)
        if not content:
            return None
        post = f"""📜  <b>THIS DAY IN HISTORY</b>
📅  <b>{self.date_nice}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

{content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 <i>History repeats in exams. Learn from it!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
#ThisDayInHistory #UPSC #GovtExams"""
        return post

    def vocabulary_word(self):
        logger.info("Generating Word of the Day...")
        prompt = "Pick ONE advanced English vocabulary word useful for government exams. Provide: WORD (in capitals), PRONUNCIATION, TYPE (noun/verb/adj), MEANING (1 line), EXAMPLE (sentence about government/policy), SYNONYMS (3 words), ANTONYMS (2 words), MEMORY TIP (creative trick to remember, 1 line). Plain text only."
        content = ai.query(prompt, temperature=0.5, max_tokens=300)
        if not content:
            return None
        post = f"""📖  <b>WORD OF THE DAY</b>
📅  <b>{self.date_nice}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

{content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 <i>1 word/day = 365 new words/year!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
#WordOfTheDay #Vocabulary #English"""
        return post

    def daily_static_gk(self):
        logger.info("Generating GK Capsule...")
        topics = [
            "an important Article of Indian Constitution",
            "a Constitutional Amendment of India",
            "a Constitutional Body of India",
            "an important International Organization",
            "a National Park or Tiger Reserve of India",
            "an important river system of India",
            "an Indian Space Mission (ISRO)",
            "a Social Reformer of India",
            "a UNESCO World Heritage Site in India",
            "a classical dance form of India",
            "a Ramsar Wetland Site of India",
            "a GI Tag product of India",
            "a Biosphere Reserve of India",
            "a Schedule of the Indian Constitution",
        ]
        topic = random.choice(topics)
        prompt = f"Create a short exam-focused fact capsule about {topic}. Choose a specific example. Give: TOPIC (specific name), CATEGORY, KEY FACTS (5 facts with dates/numbers), WHY IMPORTANT FOR EXAMS (1 line), EXAM HISTORY (has this been asked? which exam?). Plain text only."
        content = ai.query(prompt, temperature=0.4, max_tokens=350)
        if not content:
            return None
        post = f"""💡  <b>DAILY GK CAPSULE</b>
📅  <b>{self.date_nice}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

{content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 <i>Save this for revision!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
#StaticGK #GKCapsule #UPSC #SSC"""
        return post

    def prelims_countdown(self):
        logger.info("Generating Exam Countdown...")
        today_date = date.today()
        tip = random.choice(STRATEGY_TIPS)
        countdown_lines = []
        for exam_name, exam_date_str in EXAM_DATES.items():
            try:
                exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
                days_left = (exam_date - today_date).days
                if days_left > 0:
                    if days_left <= 30:
                        icon = "🔴"
                    elif days_left <= 90:
                        icon = "🟡"
                    else:
                        icon = "🟢"
                    countdown_lines.append(f"  {icon} <b>{exam_name}</b>")
                    countdown_lines.append(f"     📅 {exam_date.strftime(chr(37)+chr(100)+chr(32)+chr(37)+chr(66)+chr(32)+chr(37)+chr(89))} — <b>{days_left} days left</b>")
                    countdown_lines.append("")
            except:
                pass
        if not countdown_lines:
            countdown_lines = ["  Exam dates will be updated soon!"]
        countdown_text = chr(10).join(countdown_lines)
        post = f"""⏰  <b>EXAM COUNTDOWN</b>
📅  <b>{self.date_nice}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

{countdown_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 <b>Today's Strategy Tip:</b>
<i>{tip}</i>

━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 <b>Daily Checklist:</b>
  ☐ Read today's current affairs
  ☐ Attempt today's quiz
  ☐ Revise 1 static GK topic
  ☐ Solve 30 previous year MCQs
  ☐ Read 1 editorial

━━━━━━━━━━━━━━━━━━━━━━━━━━━
#ExamCountdown #UPSC #Motivation"""
        return post

    def eli5_post(self):
        logger.info("Generating ELI5 post...")
        topic = random.choice(ELI5_TOPICS)
        prompt = f"Explain this topic in very simple language: {topic}. Rules: 1) Use a simple real-life analogy first 2) Then explain the actual concept 3) Give 3-4 key points in simple language 4) End with why this matters for exams 5) Maximum 150 words 6) No jargon 7) Plain text only."
        content = ai.query(prompt, temperature=0.4, max_tokens=400)
        if not content:
            return None
        post = f"""🎯  <b>CONCEPT SIMPLIFIED</b>
📅  <b>{self.date_nice}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 <b>Topic: {topic}</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━

{content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 <i>Complex topic? We simplify it daily!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
#ConceptSimplified #ELI5 #UPSC"""
        return post

    def comparison_table(self):
        logger.info("Generating Comparison Table...")
        topic = random.choice(COMPARISON_TOPICS)
        prompt = f"Create a comparison between: {topic}. Compare on 5 points. For each point give the answer for both items. FORMAT: ITEM 1: (name), ITEM 2: (name), then Point 1: aspect - Item1: answer vs Item2: answer (repeat for 5 points). End with KEY EXAM POINT: what examiners usually ask (1 line). Plain text only."
        content = ai.query(prompt, temperature=0.3, max_tokens=500)
        if not content:
            return None
        post = f"""📊  <b>COMPARE AND LEARN</b>
📅  <b>{self.date_nice}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 <b>{topic}</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━

{content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 <i>Save this table for quick revision!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
#CompareAndLearn #UPSC #QuickRevision"""
        return post

    def weekly_summary(self):
        if self.day_of_week != 6:
            return None
        logger.info("Generating Weekly Summary...")
        prompt = "Create a weekly current affairs summary for UPSC aspirants. List the top 8 most important news from India and world this week. For each: 1 line headline, 1 line exam importance, category (Economy/Polity/IR/Science/Environment/Defense/Schemes). Focus on exam-relevant news. Plain text only."
        content = ai.query(prompt, temperature=0.3, max_tokens=600)
        if not content:
            return None
        post = f"""📚  <b>WEEKLY NEWS RECAP</b>
📅  <b>Week ending {self.date_nice}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━

{content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 <i>Revise this every Sunday for Prelims!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
#WeeklyRevision #SundayRevision #CurrentAffairs"""
        return post

    def get_todays_extras(self):
        posts = []
        history = self.this_day_in_history()
        if history:
            posts.append(("This Day in History", history))
        vocab = self.vocabulary_word()
        if vocab:
            posts.append(("Word of the Day", vocab))
        countdown = self.prelims_countdown()
        if countdown:
            posts.append(("Exam Countdown", countdown))
        day = self.day_of_week
        if day in [0, 3, 6]:
            gk = self.daily_static_gk()
            if gk:
                posts.append(("GK Capsule", gk))
        if day in [1, 4]:
            eli5 = self.eli5_post()
            if eli5:
                posts.append(("Concept Simplified", eli5))
        if day in [2, 5]:
            comp = self.comparison_table()
            if comp:
                posts.append(("Compare and Learn", comp))
        if day == 6:
            weekly = self.weekly_summary()
            if weekly:
                posts.append(("Weekly Summary", weekly))
        return posts


if __name__ == "__main__":
    print("Testing extras...")
    extra = ExtraContent()
    posts = extra.get_todays_extras()
    print(f"Generated {len(posts)} extra posts for {extra.day_name}")
    for name, post in posts:
        print(f"  - {name}: {len(post)} characters")