# news_filter.py

import json
import os
from datetime import datetime

from ai_engine import ai
from config.settings import SYLLABUS_CATEGORIES, FILTERED_NEWS_DIR, MIN_IMPORTANCE_SCORE
from config.logger import setup_logger

logger = setup_logger("filter")


class NewsFilter:

    def __init__(self):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def quick_keyword_check(self, article):
        text = (
            article['title'] + ' ' +
            article.get('content', '')
        ).lower()

        skip_words = [
            'cricket score', 'ipl', 'bollywood', 'movie review',
            'celebrity gossip', 'horoscope', 'recipe', 'fashion week',
            'web series', 'box office', 'reality show', 'dating',
            'weight loss', 'skincare'
        ]

        for word in skip_words:
            if word in text:
                return False, f"Contains '{word}'"

        for category, keywords in SYLLABUS_CATEGORIES.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    return True, category

        general_news_words = [
            'government', 'ministry', 'india', 'policy', 'launched',
            'announced', 'approved', 'signed', 'summit', 'committee'
        ]

        for word in general_news_words:
            if word in text:
                return True, "General news"

        return False, "No relevant keywords found"

    def ai_analyze(self, article):
        prompt = f"""You are an expert UPSC/Government exam preparation analyst.
Analyze this news article for government exam relevance.

CATEGORIES TO CHOOSE FROM:
1. Polity & Governance
2. Economy
3. International Relations
4. Science & Technology
5. Environment & Ecology
6. Social Issues
7. Geography
8. Government Schemes
9. Defense & Security
10. Awards & Appointments

ARTICLE:
Title: {article['title']}
Source: {article['source']}
Content: {article['content'][:1500]}

RESPOND ONLY IN THIS EXACT JSON FORMAT AND NOTHING ELSE:
{{"is_relevant": true, "category": "Economy", "importance": 7, "key_facts": ["fact 1", "fact 2", "fact 3"], "one_line_summary": "Brief summary of the news"}}

If the article is NOT relevant for government exams:
{{"is_relevant": false, "category": "None", "importance": 0, "key_facts": [], "one_line_summary": ""}}"""

        response = ai.query(prompt, temperature=0.1, max_tokens=400)

        if response:
            result = ai.extract_json(response)
            return result

        return None

    def filter_articles(self, articles):
        filtered = []
        stats = {
            'total': len(articles),
            'keyword_passed': 0,
            'keyword_skipped': 0,
            'ai_relevant': 0,
            'ai_not_relevant': 0,
            'ai_errors': 0,
            'final_selected': 0
        }

        logger.info(f"Filtering {len(articles)} articles...")

        for i, article in enumerate(articles, 1):
            logger.info(
                f"[{i}/{len(articles)}] {article['title'][:60]}..."
            )

            passed, reason = self.quick_keyword_check(article)

            if not passed:
                stats['keyword_skipped'] += 1
                logger.debug(f"   Skipped: {reason}")
                continue

            stats['keyword_passed'] += 1

            analysis = self.ai_analyze(article)

            if analysis is None:
                stats['ai_errors'] += 1
                logger.warning(f"   AI analysis failed")
                continue

            is_relevant = analysis.get('is_relevant', False)
            importance = analysis.get('importance', 0)

            if is_relevant and importance >= MIN_IMPORTANCE_SCORE:
                stats['ai_relevant'] += 1
                article['evaluation'] = analysis
                article['filtered_at'] = self.timestamp
                filtered.append(article)
                logger.info(
                    f"   YES [{analysis.get('category', '?')}] "
                    f"Importance: {importance}/10"
                )
            else:
                stats['ai_not_relevant'] += 1
                logger.debug(
                    f"   NO (importance: {importance})"
                )

        filtered.sort(
            key=lambda x: x['evaluation'].get('importance', 0),
            reverse=True
        )

        stats['final_selected'] = len(filtered)

        output_file = os.path.join(
            FILTERED_NEWS_DIR, f"filtered_{self.today}.json"
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)

        logger.info(f"")
        logger.info(f"{'=' * 50}")
        logger.info(f"FILTERING RESULTS:")
        logger.info(f"   Total scraped:    {stats['total']}")
        logger.info(f"   Keyword passed:   {stats['keyword_passed']}")
        logger.info(f"   Keyword skipped:  {stats['keyword_skipped']}")
        logger.info(f"   AI relevant:      {stats['ai_relevant']}")
        logger.info(f"   AI not relevant:  {stats['ai_not_relevant']}")
        logger.info(f"   AI errors:        {stats['ai_errors']}")
        logger.info(f"   FINAL SELECTED:   {stats['final_selected']}")
        logger.info(f"{'=' * 50}")

        return filtered, stats


if __name__ == "__main__":
    print("Testing News Filter...")
    print("This will first scrape news, then filter with AI.")
    print("Expected time: 10-20 minutes")
    print()

    from news_scraper import NewsScraper

    scraper = NewsScraper()
    articles = scraper.fetch_all_news()

    filterer = NewsFilter()
    filtered, stats = filterer.filter_articles(articles)

    print(f"\nSelected {len(filtered)} articles for posting!")