# kannada_content_generator.py
# Generates news posts in Kannada language for Telegram channel

import os
from datetime import datetime, timezone, timedelta
from ai_engine import get_ai_engine
from config.settings import MAX_NEWS_POSTS, CONTENT_TRUNCATION_LENGTH, KAN_FILTERED_NEWS_DIR
from config.logger import setup_logger

logger = setup_logger("kan_content")


class KannadaContentGenerator:

    def __init__(self):
        # Use IST timezone (UTC+5:30)
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today = datetime.now(ist_offset)
        self.today_nice = self.today.strftime("%d %B %Y")
        self.today_date = self.today.strftime("%Y-%m-%d")
        self.time_now = self.today.strftime("%H:%M:%S")
        self.day_name = self.today.strftime("%A")

    def create_summary(self, article):
        """Create a concise news summary in Kannada for government exam students"""
        prompt = f"""Create a concise news summary in KANNADA for Karnataka government exam students (KAS, PC, Police).

ಈ ಫಾರ್ಮ್ಯಾಟ್ ಅನ್ನು ನಿಖರವಾಗಿ ಬಳಸಿ:
📌 <b>ಶೀರ್ಷಿಕೆ</b> (ಒಂದು ಸ್ಪಷ್ಟ ಸಾಲಿನಲ್ಲಿ)
📰 <b>ಏನಾಯಿತು:</b>
(2-3 ಸರಳ ವಾಕ್ಯಗಳಲ್ಲಿ)
📝 <b>ಪರೀಕ್ಷೆಗೆ ಮುಖ್ಯ ಅಂಶಗಳು:</b>
• ಅಂಶ 1
• ಅಂಶ 2
• ಅಂಶ 3
🏷️ <b>ವರ್ಗ:</b> {article['evaluation'].get('category', 'General')}
⭐ <b>ಮಹತ್ವ:</b> {article['evaluation'].get('importance', 5)}/10

ಲೇಖನ:
ಶೀರ್ಷಿಕೆ: {article['title']}
ವಿಷಯ: {article['content'][:CONTENT_TRUNCATION_LENGTH]}

ನಿಯಮಗಳು:
- ಗರಿಷ್ಟ 120 ಪದಗಳು
- ಸರಳ ಕನ್ನಡ (ದ್ವಿತೀಯ ಭಾಷೆಯ ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಅರ್ಥವಾಗುವಂತೆ)
- ವಾಸ್ತವಗಳು, ದಿನಾಂಕಗಳು, ಹೆಸರುಗಳು, ಸಂಖ್ಯೆಗಳ ಮೇಲೆ ಕೇಂದ್ರೀಕರಿಸಿ
- ಅಭಿಪ್ರಾಯಗಳಿಲ್ಲ"""

        response = get_ai_engine().query(prompt, temperature=0.3, max_tokens=400)
        return response

    def generate_all_posts(self, filtered_articles):
        """Generate all posts for Kannada channel"""
        articles = filtered_articles[:MAX_NEWS_POSTS]

        categories = {}
        for article in articles:
            cat = article['evaluation'].get('category', 'General')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(article)

        all_posts = []
        post_data = []

        # Enhanced header with Kannada formatting
        header = (
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "   📰 <b>ದೈನಿಕ ಪ್ರಸ್ತುತ ವಿಷಯಗಳು</b> 📰\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   📅 <b>{self.today_nice}</b>\n"
            "   ⏰ <i>ಬೆಳಿಗಿನ ಆವೃತ್ತಿ</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   📊 <b>ಒಟ್ಟು:</b> <i>{len(articles)}</i> ಸುದ್ದಿ | 📚 <b>ವರ್ಗಗಳು:</b> <i>{len(categories)}</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        all_posts.append(header)

        post_number = 0
        for category, cat_articles in categories.items():
            # Use transliterated category names in Kannada
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
                    image_url = article.get('image_url', '')
                    
                    # Format with Kannada headers
                    post_text = (
                        f"\n📌 <b>{article['title']}</b>\n\n"
                        f"{summary}\n\n"
                        f"─────────────────────────\n"
                        f"📍 <b>ಮೂಲ:</b> <i>{article['source']}</i>\n"
                        f"🔗 <a href=\"{article['link']}\"><b>ಪೂರ್ಣ ಲೇಖನ ಓದಿ</b></a>\n"
                        f"─────────────────────────\n"
                    )
                    
                    all_posts.append({
                        'text': post_text,
                        'image_url': image_url if image_url else None,
                        'article': article
                    })

                    post_data.append({
                        'post_number': post_number,
                        'date': self.today_date,
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
            "📚 <b>ನವೀಕರಿತರಾಗಿರಿ. ಮುಂದುವರಿಯಿರಿ.</b>\n"
            "🔔 <i>ಅಧಿಸೂಚನೆಗಳನ್ನು ಚಾಲ್ತಿಗೊಳಿಸಿ!</i>\n"
            "⏰ <b>ಕ್ವಿಜ್ ಸಂಜೆ 7:00 ಕ್ಕೆ</b>\n\n"
            "#ಪ್ರಸ್ತುತವಿಷಯಗಳು #ಕರ್ನಾಟಕ #KAS #ಸರ್ಕಾರಿಪರೀಕ್ಷೆಗಳು"
        )
        all_posts.append(footer)

        logger.info(f"Generated {post_number} Kannada news posts")

        return all_posts, post_data


if __name__ == "__main__":
    print("kannada_content_generator.py loaded successfully")