# habit_tracker.py
"""
Daily Habit & Aspirant Greetings (Small, Simple & Inspiring).
Provides:
1. Morning Kickoff (06:30 AM IST): Crisp greeting, date, inspiring quote, and today's core focus.
2. Night Reflection (09:30 PM IST): Short calming reflection and rest reminder.
"""

import random
from typing import Dict, Any
from datetime import datetime, timezone, timedelta
from curriculum_bank import get_daily_module
from config.logger import setup_logger

logger = setup_logger("habit_tracker")

MORNING_QUOTES = [
    {
        "quote": "Cultivation of mind should be the ultimate aim of human existence.",
        "author": "Dr. B.R. Ambedkar",
        "kannada": "ಮನಸ್ಸಿನ ವಿಕಾಸವೇ ಮಾನವ ಅಸ್ತಿತ್ವದ ಅಂತಿಮ ಗುರಿಯಾಗಿರಬೇಕು."
    },
    {
        "quote": "Success comes to those who dare and act; it seldom goes to the timid.",
        "author": "Jawaharlal Nehru",
        "kannada": "ಧೈರ್ಯದಿಂದ ಕರ್ತವ್ಯ ನಿರ್ವಹಿಸುವವರನ್ನೇ ಯಶಸ್ಸು ಅರಸಿ ಬರುತ್ತದೆ."
    },
    {
        "quote": "Arise, awake, and stop not till the goal is reached.",
        "author": "Swami Vivekananda",
        "kannada": "ಏಳಿ, ಎದ್ದೇಳಿ, ಗುರಿ ತಲುಪುವ ತನಕ ನಿಲ್ಲದಿರಿ."
    },
    {
        "quote": "You have to dream before your dreams can come true.",
        "author": "Dr. A.P.J. Abdul Kalam",
        "kannada": "ಕನಸುಗಳು ನನಸಾಗುವ ಮುನ್ನ ನೀವು ಆ ಕನಸನ್ನು ಕಾಣಬೇಕು."
    },
    {
        "quote": "Wisdom is knowing what to do next, skill is knowing how to do it, and virtue is doing it.",
        "author": "David Starr Jordan",
        "kannada": "ಜ್ಞಾನ, ಕೌಶಲ್ಯ ಮತ್ತು ನಿರಂತರ ಅಭ್ಯಾಸವೇ ಯಶಸ್ಸಿನ ಸೂತ್ರ."
    }
]

NIGHT_THOUGHTS = [
    {
        "text": "Review today's learning once before sleeping. Memory consolidation works wonders!",
        "kannada": "ಮಲಗುವ ಮುನ್ನ ಇಂದು ಕಲಿತ ವಿಷಯಗಳನ್ನು ಒಮ್ಮೆ ನೆನಪಿಸಿಕೊಳ್ಳಿ. ಇದು ನೆನಪಿನ ಶಕ್ತಿಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ."
    },
    {
        "text": "Rest is not idleness. Tomorrow's success is built on tonight's recovery.",
        "kannada": "ಉತ್ತಮ ವಿಶ್ರಾಂತಿಯು ನಾಳಿನ ಗೆಲುವಿಗೆ ಅತ್ಯಗತ್ಯ. ಶಾಂತವಾಗಿ ನಿದ್ರಿಸಿ."
    },
    {
        "text": "Be proud of the efforts you put in today. Every small step counts toward your dream rank.",
        "kannada": "ಇಂದು ನೀವು ಪಟ್ಟ ಪರಿಶ್ರಮವೇ ನಿಮ್ಮ ಯಶಸ್ಸಿನ ಮೆಟ್ಟಿಲು. ನಿಮ್ಮ ಪ್ರಯತ್ನಕ್ಕೆ ತಕ್ಕ ಫಲ ಸಿಗಲಿದೆ."
    }
]


class HabitTracker:
    def __init__(self):
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today_date = datetime.now(ist_offset).strftime("%d %B %Y")
        self.day_name = datetime.now(ist_offset).strftime("%A")

    def generate_morning_kickoff(self, module: Dict[str, Any] = None, is_kannada: bool = False) -> str:
        if not module:
            module = get_daily_module()

        if not is_kannada:
            topic = module.get('sub_topic', 'Current Affairs & GS')
            return f"🌅 <b>Good morning, future officers!</b>\n🎯 <b>Today's Focus:</b> {topic}. Stay focused and make today count! 💪"
        else:
            topic = module.get('kannada_title', module.get('sub_topic', 'ಪ್ರಚಲಿತ ಘಟನೆಗಳು'))
            return f"🌅 <b>ಶುಭೋದಯ, ಭಾವಿ ಅಧಿಕಾರಿಗಳೇ!</b>\n🎯 <b>ಇಂದಿನ ವಿಷಯ:</b> {topic}. ಪರಿಶ್ರಮ ಮುಂದುವರಿಯಲಿ, ಶುಭದಿನ! 💪"

    def generate_night_audit(self, module: Dict[str, Any] = None, is_kannada: bool = False) -> str:
        if not is_kannada:
            return "🌙 <b>Good night, aspirants!</b>\n💤 Rest well tonight, recharge completely, and wake up refreshed for tomorrow!"
        else:
            return "🌙 <b>ಶುಭರಾತ್ರಿ, ಭಾವಿ ಅಧಿಕಾರಿಗಳೇ!</b>\n💤 ಶಾಂತವಾಗಿ ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ, ನಾಳೆ ಹೊಸ ಹುರುಪಿನೊಂದಿಗೆ ಕಲಿಯೋಣ!"


if __name__ == "__main__":
    ht = HabitTracker()
    print("--- MORNING ---")
    print(ht.generate_morning_kickoff())
    print("\n--- NIGHT ---")
    print(ht.generate_night_audit())
