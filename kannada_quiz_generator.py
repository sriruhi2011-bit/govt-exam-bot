# kannada_quiz_generator.py
# Generates quiz questions in Kannada language for Telegram channel

import json
import os
import random
from datetime import datetime, timezone, timedelta

from ai_engine import get_ai_engine
from config.settings import KAN_QUIZ_DIR, MAX_QUIZ_QUESTIONS, CONTENT_TRUNCATION_LENGTH
from config.logger import setup_logger

logger = setup_logger("kan_quiz")


class KannadaQuizGenerator:

    def __init__(self):
        # Use IST timezone (UTC+5:30)
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today = datetime.now(ist_offset).strftime("%Y-%m-%d")
        self.today_nice = datetime.now(ist_offset).strftime("%d %B %Y")
        self.time_now = datetime.now(ist_offset).strftime("%H:%M:%S")

    def make_questions(self, article):
        """Generate 2 MCQ questions from article in Kannada"""
        prompt = f"""You are a Karnataka government exam question setter.
Create exactly 2 MCQ questions from this news in KANNADA.

ನಿಯಮಗಳು:
1. 4 ಆಯ್ಕೆಗಳು (A, B, C, D)
2. ಕೇವಲ 1 ಸರಿಯಾದ ಉತ್ತರ
3. ವಿವರಣೆ ಅಗತ್ಯ
4. ಪರೀಕ್ಷೆ-ಯೋಗ್ಯ ಕಠಿಣತೆ

Respond ONLY IN JSON FORMAT in Kannada:
{{"questions": [{{"question": "ಪ್ರಶ್ನೆ?", "option_a": "ಆಯ್ಕೆ A", "option_b": "ಆಯ್ಕೆ B", "option_c": "ಆಯ್ಕೆ C", "option_d": "ಆಯ್ಕೆ D", "correct_answer": "A", "explanation": "ಏಕೆ A ಸರಿ?"}}, {{"question": "ಎರಡನೇ ಪ್ರಶ್ನೆ?", "option_a": "ಆಯ್ಕೆ A", "option_b": "ಆಯ್ಕೆ B", "option_c": "ಆಯ್ಕೆ C", "option_d": "ಆಯ್ಕೆ D", "correct_answer": "C", "explanation": "ಏಕೆ C ಸರಿ?"}}]}}

ಸುದ್ದಿ:
ಶೀರ್ಷಿಕೆ: {article['title']}
ವರ್ಗ: {article['evaluation']['category']}
ವಿಷಯ: {article['content'][:CONTENT_TRUNCATION_LENGTH]}
ಮುಖ್ಯ ಅಂಶಗಳು: {article['evaluation'].get('key_facts', [])}"""

        response = get_ai_engine().query(prompt, temperature=0.3, max_tokens=800)

        if response:
            parsed = get_ai_engine().extract_json(response)
            if parsed and 'questions' in parsed:
                questions = parsed['questions']
                for q in questions:
                    q['source_article'] = article['title']
                    q['category'] = article['evaluation']['category']
                    q['source'] = article['source']
                    q['article_link'] = article['link']
                    q['date'] = self.today
                    q['generated_at'] = self.time_now
                return questions

        logger.warning(f"Could not generate MCQ for: {article['title'][:50]}")
        return []

    def generate_daily_quiz(self, filtered_articles):
        """Generate daily quiz from filtered Kannada articles"""
        all_questions = []

        quiz_articles = filtered_articles[:15]

        for i, article in enumerate(quiz_articles, 1):
            logger.info(
                f"[{i}/{len(quiz_articles)}] Making MCQs: "
                f"{article['title'][:50]}..."
            )
            questions = self.make_questions(article)
            all_questions.extend(questions)

        random.shuffle(all_questions)
        daily_quiz = all_questions[:MAX_QUIZ_QUESTIONS]

        for i, q in enumerate(daily_quiz, 1):
            q['question_number'] = i

        output_file = os.path.join(KAN_QUIZ_DIR, f"kan_quiz_{self.today}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(daily_quiz, f, ensure_ascii=False, indent=2)

        logger.info(f"Generated {len(daily_quiz)} Kannada quiz questions")
        return daily_quiz

    def format_for_telegram(self, questions):
        """Format quiz for Telegram posting in Kannada"""
        posts = []

        # Enhanced header in Kannada
        header = (
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "   🧠 <b>ದೈನಿಕ ಪ್ರಸ್ತುತ ವಿಷಯಗಳ ಕ್ವಿಜ್</b> 🧠\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   📅 <b>{self.today_nice}</b>\n"
            "   ⏰ <i>ಸಂಜೆ ಆವೃತ್ತಿ</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   📝 <b>ಪ್ರಶ್ನೆಗಳು:</b> <i>{len(questions)}</i>\n"
            "   ⏱️ <b>ಸಮಯ:</b> <i>15 ನಿಮಿಷ</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        posts.append(("text", header))

        for q in questions:
            options = [
                q.get('option_a', 'ಆಯ್ಕೆ A')[:100],
                q.get('option_b', 'ಆಯ್ಕೆ B')[:100],
                q.get('option_c', 'ಆಯ್ಕೆ C')[:100],
                q.get('option_d', 'ಆಯ್ಕೆ D')[:100]
            ]

            correct_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            correct_id = correct_map.get(
                q.get('correct_answer', 'A').upper(), 0
            )

            quiz_data = {
                "question": f"ಪ್ರ. {q['question_number']}. {q['question']}"[:300],
                "options": options,
                "correct_option_id": correct_id,
                "explanation": q.get('explanation', '')[:200],
                "is_anonymous": True
            }
            posts.append(("quiz", quiz_data))

        footer = (
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📊 <b>ನೀವು ಎಷ್ಟು ಅಂಕ ಪಡೆದಿರಿ?</b>\n"
            "🔔 <i>ಅಧಿಸೂಚನೆಗಳನ್ನು ಚಾಲ್ತಿಗೊಳಿಸಿ!</i>\n"
            "🌅 <b>ನಾಳೆ ಬೆಳಗ್ಗೆ 7:00 ಕ್ಕೆ ಸುದ್ದಿ</b>\n\n"
            "#ದೈನಿಕಕ್ವಿಜ್ #ಪ್ರಸ್ತುತವಿಷಯಗಳು #ಕರ್ನಾಟಕ #KAS"
        )
        posts.append(("text", footer))

        return posts


if __name__ == "__main__":
    print("kannada_quiz_generator.py loaded successfully")