# kannada_filter.py
# Filters Kannada news articles using AI for exam relevance

import json
import os
from datetime import datetime, timezone, timedelta

from ai_engine import get_ai_engine
from config.settings import (
    SYLLABUS_CATEGORIES, KAN_FILTERED_NEWS_DIR, 
    MIN_IMPORTANCE_SCORE, CONTENT_TRUNCATION_LENGTH
)
from config.logger import setup_logger

logger = setup_logger("kan_filter")


class KannadaFilter:

    def __init__(self):
        # Use IST timezone (UTC+5:30)
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today = datetime.now(ist_offset).strftime("%Y-%m-%d")
        self.timestamp = datetime.now(ist_offset).strftime("%Y-%m-%d %H:%M:%S")

    def quick_keyword_check(self, article):
        """Check for Karnataka/government exam related keywords"""
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

        # Kannada-specific keywords for government exams
        kannada_keywords = [
            'karnataka', 'bangalore', 'bengaluru', 'mysore', 'mysuru',
            'kasaragod', 'dakshina kannada', 'udupi', 'uttara kannada',
            'hassan', 'mandya', 'shimoga', 'tumkur', 'belgaum', 'belagavi',
            'gulbarga', 'kalaburagi', 'raichur', 'bidar', 'koppal',
            'government', 'ministry', 'policy', 'launched', 'announced',
            'approved', 'signed', 'summit', 'committee', 'bill', 'act',
            'high court', 'district', 'municipal', 'zilla', 'panchayat',
            'election', 'commission', 'KASSEM', 'KAS', 'PC', 'FDA', 'SDA'
        ]

        for keyword in kannada_keywords:
            if keyword.lower() in text:
                return True, "Karnataka news"

        # General keywords
        for category, keywords in SYLLABUS_CATEGORIES.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    return True, category

        general_news_words = [
            'government', 'ministry', 'india', 'policy', 'launched',
            'announced', 'approved', 'signed', 'summit', 'committee'
        ]

        for word in general_news_words:
            if word.lower() in text:
                return True, "General news"

        return False, "No relevant keywords found"

    def ai_analyze(self, article):
        """Use AI to analyze relevance for Karnataka government exams"""
        prompt = f"""You are an expert Karnataka government exam preparation analyst.
Analyze this news article for KAS, PC, Police exam relevance.

ವರ್ಗಗಳು (CATEGORIES):
1. ರಾಜ್ಯ ಸರ್ಕಾರ ಮತ್ತು ಆಡಳಿತ (State Governance)
2. ಆರ್ಥಿಕತೆ (Economy)
3. ಅಂತರರಾಷ್ಟ್ರೀಯ ಸಂಬಂಧಗಳು (International Relations)
4. ವಿಜ್ಞಾನ ಮತ್ತು ತಂತ್ರಜ್ಞಾನ (Science & Technology)
5. ಪರಿಸರ ಮತ್ತು ಪರಿಸರ ವಿಜ್ಞಾನ (Environment)
6. ಸಾಮಾಜಿಕ ಸಮಸ್ಯೆಗಳು (Social Issues)
7. ಭೌಗೋಳಿಕ (Geography)
8. ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು (Government Schemes)
9. ರಕ್ಷಣೆ ಮತ್ತು ಭದ್ರತೆ (Defense & Security)
10. ಪ್ರಶಸ್ತಿಗಳು ಮತ್ತು ನೇಮಕಗಳು (Awards & Appointments)
11. ಕರ್ನಾಟಕ ವಿಶೇಷ (Karnataka Specific)

ಲೇಖನ:
ಶೀರ್ಷಿಕೆ: {article['title']}
ಮೂಲ: {article['source']}
ವಿಷಯ: {article['content'][:CONTENT_TRUNCATION_LENGTH]}

RESPOND ONLY IN THIS EXACT JSON FORMAT AND NOTHING ELSE:
{{"is_relevant": true, "category": "ಕರ್ನಾಟಕ ವಿಶೇಷ", "importance": 7, "key_facts": ["ಅಂಶ 1", "ಅಂಶ 2", "ಅಂಶ 3"], "one_line_summary": "ಸಂಕ್ಷಿಪ್ತ ಸಾರಾಂಶ"}}

If not relevant for exams:
{{"is_relevant": false, "category": "None", "importance": 0, "key_facts": [], "one_line_summary": ""}}"""

        response = get_ai_engine().query(prompt, temperature=0.1, max_tokens=400)

        if response:
            result = get_ai_engine().extract_json(response)
            return result

        return None

    def filter_articles(self, articles):
        """Filter Kannada articles for exam relevance"""
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

        logger.info(f"Filtering {len(articles)} Kannada articles...")

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

            if not isinstance(analysis, dict):
                stats['ai_errors'] += 1
                logger.warning(f"   AI analysis returned invalid format")
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
            KAN_FILTERED_NEWS_DIR, f"filtered_kan_{self.today}.json"
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)

        logger.info(f"")
        logger.info(f"{'=' * 50}")
        logger.info(f"KANNADA FILTERING RESULTS:")
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
    print("Testing Kannada Filter...")
    from kannada_scraper import KannadaScraper
    
    scraper = KannadaScraper()
    articles = scraper.fetch_all_news()
    
    filterer = KannadaFilter()
    filtered, stats = filterer.filter_articles(articles)
    
    print(f"\nSelected {len(filtered)} Kannada articles for posting!")