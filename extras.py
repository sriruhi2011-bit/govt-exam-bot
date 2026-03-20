# extras.py
# Extra daily content: History, Vocabulary, GK, Countdown, ELI5, Comparisons

import random
from datetime import datetime, date
from ai_engine import get_ai_engine
from config.logger import setup_logger

logger = setup_logger("extras")

MORNING_GREETINGS = [
    "Every morning brings new potential, but if you dwell on the misfortunes of the day before, you tend to overlook tremendous opportunities.",
    "Success is the sum of small efforts, repeated day in and day out. Keep pushing forward!",
    "The secret of getting ahead is getting started. Your UPSC journey begins with one step today.",
    "Believe you can and you're halfway there. Today's effort is tomorrow's success.",
    "Don't watch the clock; do what it does. Keep going. Stay focused, stay strong!",
    "Wake up with determination. Go to bed with satisfaction. Your dream of becoming an officer is valid.",
    "Small daily improvements are the key to staggering long-term results. Keep learning!",
    "The only way to do great work is to love what you do. Find your purpose in service to the nation.",
]

GOOD_NIGHT_MESSAGES = [
    "As you rest, remember: 'Sleep is the best meditation.' Rest well, wake up refreshed!",
    "Tomorrow is another day to learn something new. Sweet dreams, future officer!",
    "Review today's news once before sleeping. Memory consolidation works wonders!",
    "Rest is not idleness. Tomorrow's success is built on today's learning.",
    "Sleep well, study well, succeed well. Your nation needs capable leaders!",
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
        content = get_ai_engine().query(prompt, temperature=0.3, max_tokens=400)
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
        content = get_ai_engine().query(prompt, temperature=0.5, max_tokens=300)
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
        content = get_ai_engine().query(prompt, temperature=0.4, max_tokens=350)
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

    def eli5_post(self):
        logger.info("Generating ELI5 post...")
        topic = random.choice(ELI5_TOPICS)
        prompt = f"Explain this topic in very simple language: {topic}. Rules: 1) Use a simple real-life analogy first 2) Then explain the actual concept 3) Give 3-4 key points in simple language 4) End with why this matters for exams 5) Maximum 150 words 6) No jargon 7) Plain text only."
        content = get_ai_engine().query(prompt, temperature=0.4, max_tokens=400)
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
        content = get_ai_engine().query(prompt, temperature=0.3, max_tokens=500)
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
        content = get_ai_engine().query(prompt, temperature=0.3, max_tokens=600)
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

    def morning_greeting(self):
        """Generate morning greeting with motivational quote"""
        logger.info("Generating morning greeting...")
        quote = random.choice(MORNING_GREETINGS)
        prompt = f"Create a short, inspiring morning message for UPSC/SSC exam aspirants. Include: 1) A motivational opening (1-2 sentences), 2) Today's date and day, 3) One specific study tip or focus area suggestion, 4) Encouragement to stay focused. Keep it under 150 words. Make it energetic and positive! Plain text only."
        content = get_ai_engine().query(prompt, temperature=0.5, max_tokens=300)
        if not content:
            content = "Rise and shine! Today is another opportunity to learn and grow. Stay focused, stay determined!"
        post = f"""🌅 <b>GOOD MORNING, FUTURE OFFICERS!</b> 🌅
━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 <b>{self.date_nice} - {self.day_name}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

"{quote}"

{content}

━━━━━━━━━━━━━━━━━━━━━━━━━━
💪 <i>Let's make today count!</i>
🔔 <i>Stay tuned for today's news!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━
#GoodMorning #StayMotivated #UPSC #SSC"""
        return post

    def quiz_alert(self):
        """Generate quiz notification message"""
        logger.info("Generating quiz alert...")
        prompt = "Create an exciting, short quiz announcement for government exam aspirants. Include: 1) Excitement about the quiz, 2) Mention it's based on today's current affairs, 3) Encourage participation, 4) Remind about time limit. Keep under 100 words. Plain text only."
        content = get_ai_engine().query(prompt, temperature=0.5, max_tokens=200)
        if not content:
            content = "Test your today's learning with 10 quick questions!"
        post = f"""📢 <b>QUIZ ALERT!</b> 📢
━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 <b>10 Questions</b> from today's current affairs
⏱️ <b>1 minute</b> per question
📝 <b>Test your learning!</b>

{content}

━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ <i>Quiz starting in 2 minutes...</i>
🔔 <i>Turn on notifications!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━
#DailyQuiz #CurrentAffairs #UPSC #SSC"""
        return post

    def good_night_message(self):
        """Generate good night message with revision tip"""
        logger.info("Generating good night message...")
        tip = random.choice(GOOD_NIGHT_MESSAGES)
        prompt = "Create a soothing, encouraging good night message for exam aspirants. Include: 1) A calm closing thought, 2) One quick revision tip for tomorrow, 3) Reminder to rest well, 4) Positive encouragement. Keep under 150 words. Plain text only."
        content = get_ai_engine().query(prompt, temperature=0.5, max_tokens=300)
        if not content:
            content = "Sweet dreams! Tomorrow is another day to learn and grow."
        post = f"""🌙 <b>GOOD NIGHT, FUTURE OFFICERS!</b> 🌙
━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 <b>{self.date_nice}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

"{tip}"

{content}

━━━━━━━━━━━━━━━━━━━━━━━━━━
💤 <i>Sleep well, wake up refreshed!</i>
📚 <i>See you tomorrow with fresh news!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━
#GoodNight #StayMotivated #UPSC"""
        return post

    def get_todays_extras(self):
        posts = []
        history = self.this_day_in_history()
        if history:
            posts.append(("This Day in History", history))
        vocab = self.vocabulary_word()
        if vocab:
            posts.append(("Word of the Day", vocab))
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