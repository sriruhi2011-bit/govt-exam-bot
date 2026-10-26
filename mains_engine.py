# mains_engine.py
"""
Daily Mains Answer Writing Challenge & Model Answer Engine.
Empowers UPSC & KPSC (KAS) aspirants with:
1. Daily Question Drop (Question, Directive breakdown, Structural blueprint, High-value keywords)
2. Evening Model Answer Drop (Adhering strictly to 150/250-word limits with intro, body, way forward)
"""

from typing import Dict, Any, Tuple
from datetime import datetime, timezone, timedelta
from curriculum_bank import get_daily_module
from config.logger import setup_logger

logger = setup_logger("mains_engine")


class MainsEngine:
    def __init__(self):
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today_date = datetime.now(ist_offset).strftime("%d %B %Y")

    def generate_question_drop(self, module: Dict[str, Any] = None, is_kannada: bool = False) -> str:
        if not module:
            module = get_daily_module()

        bp = module["blueprint"]
        keywords_str = ", ".join([f"<code>{kw}</code>" for kw in module["keywords"]])

        bp_lines = [f"• <b>Introduction:</b> {bp.get('intro', '')}"]
        if 'body_p1' in bp:
            bp_lines.append(f"• <b>Body Dimension 1:</b> {bp['body_p1']}")
        if 'body_p2' in bp:
            bp_lines.append(f"• <b>Body Dimension 2:</b> {bp['body_p2']}")
        if 'body_p3' in bp:
            bp_lines.append(f"• <b>Body Dimension 3 (Committees/Judgments):</b> {bp['body_p3']}")
        bp_lines.append(f"• <b>Way Forward & Conclusion:</b> {bp.get('conclusion', '')}")
        blueprint_text = "\n".join(bp_lines)

        if not is_kannada:
            post = f"""✍️ <b>DAILY MAINS CHALLENGE | {self.today_date}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️ <b>Paper:</b> {module['paper']}
🎯 <b>Target:</b> UPSC CSE / KPSC KAS Mains
⏱️ <b>Recommended Time:</b> 11 Minutes (for 15 Marks / 250 Words)
━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ <b>QUESTION OF THE DAY:</b>
<blockquote>
<b>{module['mains_question']}</b>
</blockquote>

🔍 <b>1. Directive Decoded:</b>
🎯 <b>Directive:</b> <u>{module['directive']}</u>
💡 <b>Examiner's Expectation:</b> {module['directive_tip']}

📐 <b>2. Structural Blueprint (How to structure your answer):</b>
{blueprint_text}

💎 <b>3. High-Value Keywords to Fetch +2 Marks:</b>
{keywords_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 <b>Action for Aspirants:</b>
Take a blank A4 sheet, set a timer for 11 minutes, and write your answer NOW!
⏰ <i>Comprehensive Model Answer will be posted this evening at 8:30 PM!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━
#MainsAnswerWriting #UPSC #KPSC #KAS #TargetMains"""
            return post

        else:
            q_text = module.get("kannada_mains_question", module["mains_question"])
            post = f"""✍️ <b>ದೈನಂದಿನ ಮೈನ್ಸ್ ಪ್ರಶ್ನೆ ಸವಾಲು | {self.today_date}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️ <b>ಪತ್ರಿಕೆ:</b> {module['paper']}
🎯 <b>ಗುರಿ:</b> KPSC KAS / UPSC Mains (ಕನ್ನಡ ಮಾಧ್ಯಮ)
⏱️ <b>ನಿಗದಿತ ಸಮಯ:</b> 11 ನಿಮಿಷಗಳು (15 ಅಂಕಗಳು / 250 ಪದಗಳು)
━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ <b>ಇಂದಿನ ಪ್ರಶ್ನೆ:</b>
<blockquote>
<b>{q_text}</b>
</blockquote>

🔍 <b>1. ಪ್ರಶ್ನೆಯ ನಿರ್ದೇಶನ ಪದ (Directive):</b>
🎯 <b>ನಿರ್ದೇಶನ:</b> <u>{module['directive']}</u>
💡 <b>ಪರೀಕ್ಷಕರ ನಿರೀಕ್ಷೆ:</b> {module['directive_tip']}

📐 <b>2. ಉತ್ತರ ರಚನಾ ಚೌಕಟ್ಟು (Blueprint):</b>
• <b>ಪೀಠಿಕೆ:</b> ಸಾಂವಿಧಾನಿಕ ಅಥವಾ ಪ್ರಸ್ತುತ ಹಿನ್ನೆಲೆಯೊಂದಿಗೆ ಆರಂಭಿಸಿ.
• <b>ಮುಖ್ಯ ಭಾಗ 1:</b> ಸಕಾರಾತ್ಮಕ ಹಾಗೂ ಸಾಂವಿಧಾನಿಕ ಆಧಾರಗಳು.
• <b>ಮುಖ್ಯ ಭಾಗ 2:</b> ಪ್ರಾಯೋಗಿಕ ಸವಾಲುಗಳು ಮತ್ತು ವಿಮರ್ಶಾತ್ಮಕ ಅಂಶಗಳು.
• <b>ಮುಖ್ಯ ಭಾಗ 3:</b> ಸಂಬಂಧಪಟ್ಟ ಆಯೋಗಗಳ ಶಿಫಾರಸುಗಳು (ಸರ್ಕಾರಿಯಾ/ಪೂಂಛಿ).
• <b>ಮುಕ್ತಾಯ:</b> ಭವಿಷ್ಯದ ಸುಧಾರಣಾ ಕ್ರಮಗಳು (Way Forward).

💎 <b>3. ಉತ್ತರದಲ್ಲಿ ಬಳಸಬೇಕಾದ ಪ್ರಮುಖ ಪದಗಳು (Keywords):</b>
{keywords_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 <b>ಅಭ್ಯರ್ಥಿಗಳ ಗಮನಕ್ಕೆ:</b>
ಒಂದು ಖಾಲಿ ಹಾಳೆಯಲ್ಲಿ 11 ನಿಮಿಷಗಳ ಟೈಮರ್ ಇಟ್ಟು ಉತ್ತರಿಸಿ ಅಭ್ಯಾಸ ಮಾಡಿ!
⏰ <i>ಮಾದರಿ ಉತ್ತರವನ್ನು (Model Answer) ಸಂಜೆ 8:30ಕ್ಕೆ ಪ್ರಕಟಿಸಲಾಗುವುದು!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━
#KPSC #KAS #Mainsಕನ್ನಡ #ಉತ್ತರಲೇಖನ"""
            return post

    def generate_model_answer_drop(self, module: Dict[str, Any] = None, is_kannada: bool = False) -> str:
        if not module:
            module = get_daily_module()

        if not is_kannada:
            post = f"""📑 <b>OFFICIAL MODEL ANSWER | {self.today_date}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Reference Question:</b>
<i>"{module['mains_question']}"</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━

{module['model_answer']}

━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐ <b>Self-Evaluation Checklist:</b>
[ ] Did you address the core directive ('{module['directive']}')?
[ ] Did you cite relevant Articles and Landmark Commissions?
[ ] Did you provide a structured Way Forward instead of just criticism?
━━━━━━━━━━━━━━━━━━━━━━━━━━
#ModelAnswer #UPSC #KPSC #KASPrep"""
            return post

        else:
            q_text = module.get("kannada_mains_question", module["mains_question"])
            post = f"""📑 <b>ಅಧಿಕೃತ ಮಾದರಿ ಉತ್ತರ (MODEL ANSWER) | {self.today_date}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>ಪ್ರಶ್ನೆ:</b>
<i>"{q_text}"</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━

{module['model_answer']}

━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐ <b>ಸ್ವಯಂ ಮೌಲ್ಯಮಾಪನ ತಪಾಸಣೆ (Checklist):</b>
[ ] ಪೀಠಿಕೆಯಲ್ಲಿ ಸೂಕ್ತ ಸಾಂವಿಧಾನಿಕ ವಿಧಿಗಳನ್ನು ನಮೂದಿಸಿದ್ದೀರಾ?
[ ] ಮುಖ್ಯ ಅಂಶಗಳನ್ನು ಬುಲೆಟ್ ಪಾಯಿಂಟ್‌ಗಳಲ್ಲಿ ವಿಂಗಡಿಸಿದ್ದೀರಾ?
[ ] ಸಂಬಂಧಪಟ್ಟ ಸಮಿತಿಗಳ (ಸರ್ಕಾರಿಯಾ/ಪೂಂಛಿ) ಶಿಫಾರಸುಗಳನ್ನು ಉಲ್ಲೇಖಿಸಿದ್ದೀರಾ?
[ ] ಭವಿಷ್ಯದ ರಚನಾತ್ಮಕ ಪರಿಹಾರದೊಂದಿಗೆ ಮುಕ್ತಾಯಗೊಳಿಸಿದ್ದೀರಾ?
━━━━━━━━━━━━━━━━━━━━━━━━━━
#KPSC #KAS #ModelAnswer #ಕನ್ನಡಮೈನ್ಸ್"""
            return post


if __name__ == "__main__":
    eng = MainsEngine()
    print("--- MAINS QUESTION ---")
    print(eng.generate_question_drop()[:400])
    print("\n--- MODEL ANSWER ---")
    print(eng.generate_model_answer_drop()[:400])
