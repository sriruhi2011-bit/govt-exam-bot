# prelims_drill.py
"""
Daily Prelims & Objective MCQ Drill Engine.
Generates UPSC & KPSC standard multi-statement MCQs formatted for native Telegram Quiz Polls.
Features:
- Statement-based questions ("Consider the following statements...")
- Native Telegram quiz mode with instantaneous correct answer confirmation
- Educational explanation popups upon answering
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone, timedelta
from curriculum_bank import get_daily_module
from config.logger import setup_logger

logger = setup_logger("prelims_drill")


class PrelimsDrillEngine:
    def __init__(self):
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today_date = datetime.now(ist_offset).strftime("%d %B %Y")

    def generate_drill_intro(self, module: Dict[str, Any] = None, is_kannada: bool = False) -> str:
        if not module:
            module = get_daily_module()

        if not is_kannada:
            return f"""🎯 <b>DAILY PRELIMS & OBJECTIVE DRILL | {self.today_date}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 <b>Subject:</b> {module['paper']}
📌 <b>Theme:</b> {module['title']}
🔢 <b>Questions:</b> 3 High-Yield Standard MCQs
⏱️ <b>Time:</b> 1 Minute per Question
━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 <i>Attempt the interactive polls below! Tap your answer to check correctness & read the explanation popup.</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━
#PrelimsDrill #UPSC #KPSC #MCQPractice"""
        else:
            return f"""🎯 <b>ದೈನಂದಿನ ಪ್ರಿಲಿಮ್ಸ್ ಕ್ವಿಜ್ ಸರಣಿ | {self.today_date}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 <b>ವಿಷಯ:</b> {module['paper']}
📌 <b>ಪ್ರಮುಖಾಂಶ:</b> {module.get('kannada_title', module['title'])}
🔢 <b>ಪ್ರಶ್ನೆಗಳು:</b> 3 ಗುಣಮಟ್ಟದ ಬಹುಆಯ್ಕೆ ಪ್ರಶ್ನೆಗಳು (MCQs)
⏱️ <b>ಸಮಯ:</b> ಪ್ರತಿ ಪ್ರಶ್ನೆಗೆ 1 ನಿಮಿಷ
━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 <i>ಕೆಳಗಿನ ಕ್ವಿಜ್ ಪೋಲ್‌ಗಳಲ್ಲಿ ಸರಿಯಾದ ಉತ್ತರವನ್ನು ಆಯ್ಕೆ ಮಾಡಿ! ಉತ್ತರ ನೀಡಿದ ತಕ್ಷಣ ವಿವರಣಾ ಬಾಕ್ಸ್ ತೆರೆಯುತ್ತದೆ.</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━
#KPSC #KAS #PSI #FDA #ಕ್ವಿಜ್"""

    def get_poll_items(self, module: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        if not module:
            module = get_daily_module()

        polls = []
        for mcq in module.get("prelims_mcqs", []):
            polls.append({
                "question": mcq["question"][:300],
                "options": mcq["options"],
                "correct_option_id": mcq["correct_option_id"],
                "explanation": mcq["explanation"][:200]
            })
        return polls


if __name__ == "__main__":
    drill = PrelimsDrillEngine()
    print("Intro text:")
    print(drill.generate_drill_intro())
    print("Poll items count:", len(drill.get_poll_items()))
