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
📌 <b>HEADLINE</b> (rewrite in 1 clear line)

📰 <b>What happened:</b>
(2-3 simple sentences)

📝 <b>Key Exam Points:</b>
• Point 1
• Point 2
• Point 3

🏷️ <b>Category:</b> {article['evaluation']['category']}
⭐ <b>Importance:</b> {article['evaluation']['importance']}/10

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

        # Enhanced header with better formatting
        header = (
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "   📰 <b>DAILY CURRENT AFFAIRS</b> 📰\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   📅 <b>{self.today_nice}</b>\n"
            "   ⏰ <i>Morning Edition</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   📊 <b>Total:</b> <i>{len(articles)}</i> news | 📚 <b>Categories:</b> <i>{len(categories)}</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━"
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
                    
                    # Enhanced format with bold headers and underline
                    post_text = (
                        f"\n📌 <b>{article['title']}</b>\n\n"
                        f"{summary}\n\n"
                        f"─────────────────────────\n"
                        f"📍 <b>Source:</b> <i>{article['source']}</i>\n"
                        f"🔗 <a href=\"{article['link']}\"><b>Read Full Article</b></a>\n"
                        f"─────────────────────────\n"
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
            "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📚 <b>Stay updated. Stay ahead.</b>\n"
            "🔔 <i>Turn on notifications!</i>\n"
            "⏰ <b>Quiz at 7:00 PM</b>\n\n"
            "#CurrentAffairs #UPSC #SSC #GovtExams"
        )
        all_posts.append(footer)

        logger.info(f"Generated {post_number} news posts")

        return all_posts, post_data


if __name__ == "__main__":
    print("content_generator.py loaded successfully")
