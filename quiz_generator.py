# quiz_generator.py

import json
import os
import random
from datetime import datetime

from ai_engine import get_ai_engine
from config.settings import QUIZ_DIR, MAX_QUIZ_QUESTIONS, CONTENT_TRUNCATION_LENGTH
from config.logger import setup_logger

logger = setup_logger("quiz_gen")


class QuizGenerator:

    def __init__(self):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.today_nice = datetime.now().strftime("%d %B %Y")
        self.time_now = datetime.now().strftime("%H:%M:%S")

    def make_questions(self, article):
        prompt = f"""You are a UPSC exam question setter.
Create exactly 2 MCQ questions from this news.

RULES:
1. 4 options each (A, B, C, D)
2. Only 1 correct answer
3. Include explanation
4. Exam-worthy difficulty

RESPOND ONLY IN JSON FORMAT AND NOTHING ELSE:
{{"questions": [{{"question": "Question text?", "option_a": "Option A", "option_b": "Option B", "option_c": "Option C", "option_d": "Option D", "correct_answer": "A", "explanation": "Why A is correct..."}}, {{"question": "Second question?", "option_a": "Option A", "option_b": "Option B", "option_c": "Option C", "option_d": "Option D", "correct_answer": "C", "explanation": "Why C is correct..."}}]}}

NEWS:
Title: {article['title']}
Category: {article['evaluation']['category']}
Content: {article['content'][:CONTENT_TRUNCATION_LENGTH]}
Key Facts: {article['evaluation'].get('key_facts', [])}"""

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

        output_file = os.path.join(QUIZ_DIR, f"quiz_{self.today}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(daily_quiz, f, ensure_ascii=False, indent=2)

        logger.info(f"Generated {len(daily_quiz)} quiz questions")
        return daily_quiz

    def format_for_telegram(self, questions):
        posts = []

        # Enhanced header with better formatting
        header = (
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "   🧠 <b>DAILY CURRENT AFFAIRS QUIZ</b> 🧠\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   📅 <b>{self.today_nice}</b>\n"
            "   ⏰ <i>Evening Edition</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   📝 <b>Questions:</b> <i>{len(questions)}</i>\n"
            "   ⏱️ <b>Time:</b> <i>15 minutes</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        posts.append(("text", header))

        for q in questions:
            options = [
                q.get('option_a', 'Option A'),
                q.get('option_b', 'Option B'),
                q.get('option_c', 'Option C'),
                q.get('option_d', 'Option D')
            ]

            correct_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            correct_id = correct_map.get(
                q.get('correct_answer', 'A').upper(), 0
            )

            quiz_data = {
                "question": f"Q{q['question_number']}. {q['question']}"[:300],
                "options": options,
                "correct_option_id": correct_id,
                "explanation": q.get('explanation', '')[:200],
                "is_anonymous": True
            }
            posts.append(("quiz", quiz_data))

        footer = (
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📊 <b>How did you score?</b>\n"
            "🔔 <i>Turn on notifications!</i>\n"
            "🌅 <b>Tomorrow's News at 7:00 AM</b>\n\n"
            "#DailyQuiz #CurrentAffairs #UPSC #SSC"
        )
        posts.append(("text", footer))

        return posts


if __name__ == "__main__":
    print("quiz_generator.py loaded successfully")
