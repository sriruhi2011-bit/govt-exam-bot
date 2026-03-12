# content_generator.py

import os
from datetime import datetime
from ai_engine import get_ai_engine
from config.settings import MAX_NEWS_POSTS, CONTENT_TRUNCATION_LENGTH
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
Content: {article['content'][:CONTENT_TRUNCATION_LENGTH]}

RULES:
- Maximum 120 words
- Simple English
- Focus on facts, dates, names, numbers
- No opinions"""

        response = get_ai_engine().query(prompt, temperature=0.3, max_tokens=400)
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
            f"📰 <b>DAILY CURRENT AFFAIRS</b> 📰\n"
            f"📅 <i>{self.today_nice}</i>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>Total:</b> {len(articles)} important news items\n"
            f"━━━━━━━━━━━━━━━━━━━━━"
        )
        all_posts.append(header)

        post_number = 0
        for category, cat_articles in categories.items():
            cat_header = f"\n\n🔷 <b>{category.upper()}</b>\n{'─' * 28}\n"
            all_posts.append(cat_header)

            for article in cat_articles[:4]:
                post_number += 1
                logger.info(
                    f"Writing post {post_number}/{len(articles)}: "
                    f"{article['title'][:50]}..."
                )

                summary = self.create_summary(article)

                if summary:
                    # Extract image URL from article if available
                    image_url = article.get('image_url', '')
                    
                    # Format with professional styling
                    post_text = (
                        f"\n📌 <b>{article['title']}</b>\n\n"
                        f"{summary}\n\n"
                        f"📍 <b>Source:</b> {article['source']}\n"
                        f"🔗 <a href=\"{article['link']}\">Read Full Article</a>\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━━\n"
                    )
                    
                    all_posts.append({
                        'text': post_text,
                        'image_url': image_url if image_url else None,
                        'article': article
                    })

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
                        ),
                        'image_url': image_url
                    })

        footer = (
            f"\n━━━━━━━━━━━━━━━━━━━━━\n"
            f"📚 <b>Stay updated. Stay ahead.</b>\n"
            f"🔔 <i>Turn on notifications!</i>\n"
            f"⏰ <b>Quiz at 7:00 PM</b>\n\n"
            f"#CurrentAffairs #UPSC #SSC #GovtExams"
        )
        all_posts.append(footer)

        logger.info(f"Generated {post_number} news posts")

        return all_posts, post_data


if __name__ == "__main__":
    print("content_generator.py loaded successfully")