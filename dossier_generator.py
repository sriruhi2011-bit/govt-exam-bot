# dossier_generator.py
"""
Daily 360° Issue Dossier Generator.
Transforms high-yield syllabus themes into comprehensive exam-ready analytical dossiers
suitable for UPSC and KPSC (KAS / PSI) Mains and Prelims.
Formats for Telegram with clean HTML typography and expandable quotes.
"""

from typing import Dict, Any, Tuple
from datetime import datetime, timezone, timedelta
from curriculum_bank import get_daily_module
from config.logger import setup_logger

logger = setup_logger("dossier_gen")


class DossierGenerator:
    def __init__(self):
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today_date = datetime.now(ist_offset).strftime("%d %B %Y")
        self.today_day = datetime.now(ist_offset).strftime("%A")

    def generate_english_dossier(self, module: Dict[str, Any] = None) -> str:
        if not module:
            module = get_daily_module()

        static_points = "\n".join([f"• <b>{pt.split(':')[0]}:</b> {':'.join(pt.split(':')[1:])}" if ':' in pt else f"• {pt}" for pt in module["static_framework"]])
        analytical_points = "\n".join([f"• <b>{pt.split(':')[0]}:</b> {':'.join(pt.split(':')[1:])}" if ':' in pt else f"• {pt}" for pt in module["analytical_points"]])
        committees = "\n".join([f"⚖️ <b>{c.split(':')[0]}:</b> {':'.join(c.split(':')[1:])}" if ':' in c else f"• {c}" for c in module["committees"]])

        post = f"""📑 <b>DAILY 360° ISSUE DOSSIER | {self.today_date}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️ <b>Category:</b> {module['paper']}
🎯 <b>Focus Area:</b> {module['sub_topic']}
━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 <b>TOPIC: {module['title']}</b>

⚡ <b>The Trigger & Current Context:</b>
<i>"{module['trigger']}"</i>

🏛️ <b>Constitutional & Static Core:</b>
<blockquote expandable>
{static_points}
</blockquote>

🔍 <b>Key Exam Dimensions & Analytical Debates:</b>
<blockquote expandable>
{analytical_points}
</blockquote>

📜 <b>Landmark Committees, Commissions & Judgments:</b>
<blockquote expandable>
{committees}
</blockquote>

🧭 <b>Pragmatic Way Forward:</b>
💡 {module['way_forward']}

━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Exam Takeaway:</b>
<i>Use this dossier for today's 5:00 PM Mains Challenge and 1:00 PM Prelims Quiz Drill!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━
#UPSC #KPSC #KAS #Mains360 #{module['id'].split('_')[0]}"""
        return post

    def generate_kannada_dossier(self, module: Dict[str, Any] = None) -> str:
        if not module:
            module = get_daily_module()

        static_points = "\n".join([f"• {pt}" for pt in module["static_framework"]])
        analytical_points = "\n".join([f"• {pt}" for pt in module["analytical_points"]])
        committees = "\n".join([f"⚖️ {c}" for c in module["committees"]])

        post = f"""📑 <b>ದೈನಂದಿನ 360° ಸಮಗ್ರ ವಿಶ್ಲೇಷಣೆ | {self.today_date}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️ <b>ವಿಭಾಗ:</b> {module['paper']}
🎯 <b>ವಿಷಯ:</b> {module['sub_topic']}
━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 <b>ವಿಷಯ: {module.get('kannada_title', module['title'])}</b>

⚡ <b>ಪ್ರಸ್ತುತ ಹಿನ್ನೆಲೆ:</b>
<i>"{module.get('kannada_trigger', module['trigger'])}"</i>

🏛️ <b>ಸಾಂವಿಧಾನಿಕ ಹಾಗೂ ಮೂಲ ಚೌಕಟ್ಟು:</b>
<blockquote expandable>
{static_points}
</blockquote>

🔍 <b>ಮುಖ್ಯ ಚರ್ಚಾ ಆಯಾಮಗಳು & ವಿಶ್ಲೇಷಣೆ:</b>
<blockquote expandable>
{analytical_points}
</blockquote>

📜 <b>ಪ್ರಮುಖ ಆಯೋಗಗಳು ಮತ್ತು ತೀರ್ಪುಗಳು:</b>
<blockquote expandable>
{committees}
</blockquote>

🧭 <b>ಮುಂದಿರುವ ದಾರಿ (Way Forward):</b>
💡 {module.get('kannada_way_forward', module['way_forward'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>ಪರೀಕ್ಷಾ ದೃಷ್ಟಿಕೋನ:</b>
<i>ಇಂದಿನ ಮೈನ್ಸ್ ಪ್ರಶ್ನೆ ಹಾಗೂ ಪ್ರಿಲಿಮ್ಸ್ ಕ್ವಿಜ್ ಈ ವಿಷಯದ ಮೇಲಿರುತ್ತದೆ!</i>
━━━━━━━━━━━━━━━━━━━━━━━━━━
#KPSC #KAS #PSI #FDA #UPSCಕನ್ನಡ"""
        return post


if __name__ == "__main__":
    gen = DossierGenerator()
    print("--- ENGLISH DOSSIER ---")
    print(gen.generate_english_dossier()[:400])
    print("\n--- KANNADA DOSSIER ---")
    print(gen.generate_kannada_dossier()[:400])
