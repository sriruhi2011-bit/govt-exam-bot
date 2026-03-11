# content_generator.py

from datetime import datetime
from ai_engine import ai
from config.settings import MAX_NEWS_POSTS
from config.logger import setup_logger

logger = setup_logger("content_gen")


class ContentGenerator:

    def __init__(self):
        self.today_nice = datetime.now().strftime("%d %B %Y")
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.time_now = datetime.now().strftime("%H:%M:%S")

    def create_summary(self, article):
        prompt = f"""Create a concise news summary for UPSC exam students.

USE THIS EXACT FORMAT:
📌 HEADLINE (rewrite in 1 clear line)

📰 What happened:
(2-3 simple sentences)

📝 Key Exam Points:
• Point 1
• Point 2
• Point 3

🏷️ Category: {article['evaluation']['category']}
⭐ Importance: {article['evaluation']['importance']}/10

ARTICLE:
Title: {article['title']}
Content: {article['content'][:1500]}

RULES:
- Maximum 120 words
- Simple English
- Focus on facts, dates, names, numbers
- No opinions"""

        response = ai.query(prompt, temperature=0.3, max_tokens=400)
        return response

    def generate_all_posts(self, filtered_articles):
        articles = filtered_articles[:MAX_NEWS_POSTS]

        categories = {}
        for article in articles:
            cat = article['evaluation'].get('category', 'General')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(article)

        all_posts = []
        post_data = []

        header = (
            f"📰 DAILY CURRENT AFFAIRS 📰\n"
            f"📅 {self.today_nice}\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 Total: {len(articles)} important news items\n"
            f"━━━━━━━━━━━━━━━━━━━━━"
        )
        all_posts.append(header)

        post_number = 0
        for category, cat_articles in categories.items():
            cat_header = f"\n\n🔷 {category.upper()}\n{'─' * 28}\n"
            all_posts.append(cat_header)

            for article in cat_articles[:4]:
                post_number += 1
                logger.info(
                    f"Writing post {post_number}/{len(articles)}: "
                    f"{article['title'][:50]}..."
                )

                summary = self.create_summary(article)

                if summary:
                    post_text = f"\n{summary}\n\n━━━━━━━━━━━━━━━━━━━━━\n"
                    all_posts.append(post_text)

                    post_data.append({
                        'post_number': post_number,
                        'date': self.today,
                        'time_generated': self.time_now,
                        'category': category,
                        'title': article['title'],
                        'source': article['source'],
                        'importance': article['evaluation']['importance'],
                        'summary': summary[:500],
                        'link': article['link'],
                        'key_facts': ', '.join(
                            article['evaluation'].get('key_facts', [])
                        )
                    })

        footer = (
            f"\n━━━━━━━━━━━━━━━━━━━━━\n"
            f"📚 Stay updated. Stay ahead.\n"
            f"🔔 Turn on notifications!\n"
            f"⏰ Quiz at 7:00 PM\n\n"
            f"#CurrentAffairs #UPSC #SSC #GovtExams"
        )
        all_posts.append(footer)

        logger.info(f"Generated {post_number} news posts")

        return all_posts, post_data


if __name__ == "__main__":
    print("content_generator.py loaded successfully")