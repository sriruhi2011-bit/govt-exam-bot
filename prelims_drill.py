# prelims_drill.py
"""
Daily Prelims & Objective MCQ Drill Engine.
Generates UPSC & KPSC standard multi-statement MCQs formatted for native Telegram Quiz Polls.
Features:
- Statement-based questions ("Consider the following statements...")
- Native Telegram quiz mode with instantaneous correct answer confirmation
- Educational explanation popups upon answering
"""

import sys
from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone, timedelta
from curriculum_bank import get_daily_module
from config.logger import setup_logger

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

logger = setup_logger("prelims_drill")


class PrelimsDrillEngine:
    def __init__(self):
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today_date = datetime.now(ist_offset).strftime("%d %B %Y")

    def generate_drill_intro(self, module: Dict[str, Any] = None, is_kannada: bool = False, is_bilingual: bool = True) -> str:
        if not module:
            module = get_daily_module()

        if is_bilingual:
            kannada_theme = module.get('kannada_title', module['title'])
            return f"""🎯 <b>DAILY PRELIMS DRILL | ದೈನಂದಿನ ಪ್ರಿಲಿಮ್ಸ್ ಕ್ವಿಜ್ ({self.today_date})</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 <b>Subject / ವಿಷಯ:</b> {module['paper']}
📌 <b>Theme / ವಿಷಯ:</b> {module['title']}
🇮🇳 <b>ಕನ್ನಡ:</b> {kannada_theme}
🔢 <b>Questions / ಪ್ರಶ್ನೆಗಳು:</b> 3 Bilingual MCQs (ದ್ವಿಭಾಷಾ ಕ್ವಿಜ್)
⏱️ <b>Time / ಸಮಯ:</b> 1 Min per Question
━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 <i>Attempt the interactive bilingual polls below! Tap to reveal the answer & explanation popup.
ಕೆಳಗಿನ ಕ್ವಿಜ್ ಪೋಲ್‌ಗಳಲ್ಲಿ ಸರಿಯಾದ ಉತ್ತರವನ್ನು ಆಯ್ಕೆ ಮಾಡಿ!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━
#PrelimsDrill #UPSC #KPSC #ದ್ವಿಭಾಷಾಕ್ವಿಜ್"""
        elif is_kannada:
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
        else:
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

    def get_poll_items(self, module: Dict[str, Any] = None, is_bilingual: bool = True) -> List[Dict[str, Any]]:
        if not module:
            module = get_daily_module()

        polls = []
        for mcq in module.get("prelims_mcqs", []):
            if is_bilingual and "bilingual_poll" in mcq:
                bp = mcq["bilingual_poll"]
                polls.append({
                    "question": bp["question"][:300],
                    "options": [opt[:100] for opt in bp["options"]][:10],
                    "correct_option_id": bp.get("correct_option_id", mcq.get("correct_option_id", 0)),
                    "explanation": bp.get("explanation", "")[:200]
                })
            else:
                polls.append({
                    "question": mcq["question"][:300],
                    "options": [opt[:100] for opt in mcq["options"]][:10],
                    "correct_option_id": mcq["correct_option_id"],
                    "explanation": mcq["explanation"][:200]
                })
        return polls


if __name__ == "__main__":
    drill = PrelimsDrillEngine()
    print("Intro text:")
    print(drill.generate_drill_intro())
    print("Poll items count:", len(drill.get_poll_items()))
