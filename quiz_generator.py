# quiz_generator.py

import json
import os
import random
from datetime import datetime, timezone, timedelta

from ai_engine import get_ai_engine
from config.settings import (
    QUIZ_DIR,
    MAX_QUIZ_QUESTIONS,
    CONTENT_TRUNCATION_LENGTH,
    MAX_QUIZ_ARTICLES_POOL_PER_CATEGORY,
)
from config.logger import setup_logger

logger = setup_logger("quiz_gen")


class QuizGenerator:

    def __init__(self):
        # Use IST timezone (UTC+5:30) for Indian timezone
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today = datetime.now(ist_offset).strftime("%Y-%m-%d")
        self.today_nice = datetime.now(ist_offset).strftime("%d %B %Y")
        self.time_now = datetime.now(ist_offset).strftime("%H:%M:%S")

    def _normalize_correct_answer(self, val):
        if val is None:
            return None
        if isinstance(val, str):
            import re
            v = val.strip().upper()
            # Find all standalone letters A, B, C, D using word boundaries
            match = re.search(r'\b([A-D])\b', v)
            if match:
                return match.group(1)
            # If no word boundaries match (e.g. "(A)"), find the first A-D char by filtering other chars
            cleaned = re.sub(r'[^A-D]', '', v)
            if cleaned:
                return cleaned[0]
        return None

    def _questions_are_valid(self, questions):
        if not isinstance(questions, list) or not questions:
            return False
        for q in questions:
            for key in ["question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "explanation"]:
                if key not in q:
                    return False
            if self._normalize_correct_answer(q.get("correct_answer")) not in {"A", "B", "C", "D"}:
                return False
        return True

    def make_questions(self, article):
        prompt = f"""You are an elite UPSC Civil Services Exam question setter.
Create exactly 2 high-quality, concept-heavy MCQ questions from the provided news article. The questions must test both the current development and static syllabus concepts (such as relevant constitutional articles, parent acts, historical context, or economic theories).

RULES FOR QUESTION 1 (Classic Statement-Based):
1. Must begin with "Consider the following statements regarding [Topic]:" followed by 2 or 3 numbered statements.
2. One statement must test the static/historical background of the topic, and one must test the current development.
3. The question must end with "Which of the statements given above is/are correct?".
4. Options (A, B, C, D) must represent combinations of these statements, for example:
   - A) 1 only
   - B) 2 and 3 only
   - C) 1 and 3 only
   - D) 1, 2 and 3

RULES FOR QUESTION 2 (Modern Elimination-Proof):
1. Must begin with "Consider the following statements regarding [Topic]:" followed by exactly 3 numbered statements.
2. The question must end with "How many of the statements given above are correct?".
3. Options (A, B, C, D) must be EXACTLY:
   - A) Only one
   - B) Only two
   - C) All three
   - D) None

GENERAL RULES:
- Include a detailed explanation for each question explaining which statements are correct/incorrect and why.
- Output MUST be strictly in JSON format. Do not add any markdown blocks or conversational text.

RESPOND ONLY IN JSON FORMAT AND NOTHING ELSE:
{{
  "questions": [
    {{
      "question": "Consider the following statements regarding [Topic]:\\n1. [Statement 1]\\n2. [Statement 2]\\n3. [Statement 3]\\n\\nWhich of the statements given above is/are correct?",
      "option_a": "[Option A]",
      "option_b": "[Option B]",
      "option_c": "[Option C]",
      "option_d": "[Option D]",
      "correct_answer": "[A/B/C/D]",
      "explanation": "[Detailed Explanation]"
    }},
    {{
      "question": "Consider the following statements regarding [Topic]:\\n1. [Statement 1]\\n2. [Statement 2]\\n3. [Statement 3]\\n\\nHow many of the statements given above are correct?",
      "option_a": "Only one",
      "option_b": "Only two",
      "option_c": "All three",
      "option_d": "None",
      "correct_answer": "[A/B/C/D]",
      "explanation": "[Detailed Explanation]"
    }}
  ]
}}

NEWS:
Title: {article['title']}
Category: {article['evaluation']['category']}
Content: {article['content'][:CONTENT_TRUNCATION_LENGTH]}
Key Facts: {article['evaluation'].get('key_facts', [])}"""

        max_attempts = 2
        for attempt in range(1, max_attempts + 1):
            response = get_ai_engine().query_cached(prompt, temperature=0.3, max_tokens=800)
            if not response:
                continue

            parsed = get_ai_engine().extract_json(response)
            if not parsed or "questions" not in parsed:
                continue

            questions = parsed["questions"]

            # Normalize/validate correct_answer
            for q in questions:
                q["correct_answer"] = self._normalize_correct_answer(q.get("correct_answer"))

                q["source_article"] = article["title"]
                q["category"] = article["evaluation"]["category"]
                q["source"] = article["source"]
                q["article_link"] = article["link"]
                q["date"] = self.today
                q["generated_at"] = self.time_now

            if self._questions_are_valid(questions):
                return questions

            logger.warning(
                f"Invalid MCQ JSON for article (attempt {attempt}/{max_attempts}): {article['title'][:50]}"
            )

        logger.warning(f"Could not generate valid MCQ for: {article['title'][:50]}")
        return []

    def generate_daily_quiz(self, filtered_articles):
        all_questions = []

        # Select a quiz article pool per category to improve balance and reduce calls.
        per_cat_pool = MAX_QUIZ_ARTICLES_POOL_PER_CATEGORY
        category_pools = {}
        for a in filtered_articles:
            cat = a.get("evaluation", {}).get("category", "General")
            category_pools.setdefault(cat, []).append(a)

        quiz_pool = []
        for cat, articles in category_pools.items():
            quiz_pool.extend(articles[:per_cat_pool])

        # Bound total pool size (avoid runaway if there are many categories)
        quiz_pool = quiz_pool[:15]
        quiz_pool.sort(key=lambda x: x.get("evaluation", {}).get("importance", 0), reverse=True)

        for i, article in enumerate(quiz_pool, 1):
            logger.info(
                f"[{i}/{len(quiz_pool)}] Making MCQs: "
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
                q.get('option_a', 'Option A')[:100],
                q.get('option_b', 'Option B')[:100],
                q.get('option_c', 'Option C')[:100],
                q.get('option_d', 'Option D')[:100]
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
