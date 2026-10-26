# capsule_engine.py
"""
Micro-Learning Flashcard Capsule Engine.
Delivers compact, high-retention factual nuggets (Articles, Passes, Schemes, Commissions)
vital for rapid revision in UPSC and KPSC exams.
"""

from typing import Dict, Any
from datetime import datetime, timezone, timedelta
from curriculum_bank import get_daily_module
from config.logger import setup_logger

logger = setup_logger("capsule_engine")


class CapsuleEngine:
    def __init__(self):
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today_date = datetime.now(ist_offset).strftime("%d %B %Y")

    def generate_capsule(self, module: Dict[str, Any] = None, is_kannada: bool = False) -> str:
        if not module:
            module = get_daily_module()

        cap = module.get("capsule", {})
        title = cap.get("kannada_title" if is_kannada else "title", cap.get("title", "EXAM CAPSULE"))
        fact = cap.get("kannada_fact" if is_kannada else "key_fact", cap.get("key_fact", ""))
        pyq = cap.get("pyq_note", "")

        if not is_kannada:
            post = f"""💡 <b>HIGH-YIELD REVISION CAPSULE | {self.today_date}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 <b>{title}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 <b>Core High-Yield Retention Fact:</b>
<blockquote>
{fact}
</blockquote>

📚 <b>Previous Year Exam Connection (PYQ):</b>
<i>{pyq}</i>

━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐ <b>Pro Tip:</b> Save this message to your Telegram 'Saved Messages' for rapid revision before the exam!
━━━━━━━━━━━━━━━━━━━━━━━━━━
#ExamCapsule #UPSC #KPSC #StaticGK #RapidRevision"""
            return post

        else:
            post = f"""💡 <b>ದೈನಂದಿನ ಪ್ರಮುಖ ಪುನರಾವರ್ತನಾ ಕ್ಯಾಪ್ಸೂಲ್ | {self.today_date}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 <b>{title}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 <b>ನೆನಪಿಡಬೇಕಾದ ಪ್ರಮುಖ ಪರೀಕ್ಷಾ ಸತ್ಯಾಂಶ:</b>
<blockquote>
{fact}
</blockquote>

📚 <b>ಹಿಂದಿನ ಪ್ರಶ್ನೆಪತ್ರಿಕೆಗಳ ಸಂಪರ್ಕ (PYQ):</b>
<i>{pyq}</i>

━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐ <b>ಸಲಹೆ:</b> ಪರೀಕ್ಷೆಯ ಕೊನೆಯ ಹಂತದ ಪುನರಾವರ್ತನೆಗಾಗಿ ಈ ಸಂದೇಶವನ್ನು 'Saved Messages' ನಲ್ಲಿ ಉಳಿಸಿಕೊಳ್ಳಿ!
━━━━━━━━━━━━━━━━━━━━━━━━━━
#KPSCಕ್ಯಾಪ್ಸೂಲ್ #KAS #PSI #FDA #ಪುನರಾವರ್ತನೆ"""
            return post


if __name__ == "__main__":
    ce = CapsuleEngine()
    print("--- ENGLISH CAPSULE ---")
    print(ce.generate_capsule()[:300])
    print("\n--- KANNADA CAPSULE ---")
    print(ce.generate_capsule(is_kannada=True)[:300])
