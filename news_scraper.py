# news_scraper.py

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import hashlib
import os
import time

from config.settings import (
    RSS_FEEDS, RAW_NEWS_DIR,
    MAX_ARTICLES_PER_SOURCE,
    MAX_ARTICLE_CONTENT_LENGTH,
    REQUEST_TIMEOUT, MIN_CONTENT_LENGTH, MIN_DUPLICATE_CHECK_LENGTH
)
from config.logger import setup_logger

logger = setup_logger("scraper")


class NewsScraper:

    def __init__(self):
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )
        }
        self.today = datetime.now().date()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_article_text(self, url):
        try:
            response = requests.get(
                url, headers=self.headers, timeout=REQUEST_TIMEOUT
            )
            soup = BeautifulSoup(response.content, 'html.parser')

            for junk in soup.find_all(
                ['script', 'style', 'nav', 'footer',
                 'aside', 'header', 'form', 'iframe']
            ):
                junk.decompose()

            article_containers = [
                soup.find('article'),
                soup.find('div', class_='article-body'),
                soup.find('div', class_='story-element'),
                soup.find('div', class_='content-data'),
                soup.find('div', class_='article__content'),
                soup.find('div', class_='story_details'),
                soup.find('div', class_='entry-content'),
                soup.find('div', {'id': 'article-body'}),
            ]

            article_div = None
            for container in article_containers:
                if container:
                    article_div = container
                    break

            if article_div:
                paragraphs = article_div.find_all('p')
            else:
                paragraphs = soup.find_all('p')

            text = ' '.join([
                p.get_text().strip()
                for p in paragraphs
                if len(p.get_text().strip()) > MIN_CONTENT_LENGTH
            ])

            return text[:MAX_ARTICLE_CONTENT_LENGTH]

        except Exception as e:
            logger.debug(f"Could not read article {url}: {e}")
            return ""

    def fetch_all_news(self):
        all_articles = []

        logger.info(f"Starting news collection from {len(RSS_FEEDS)} sources...")

        for source_name, feed_url in RSS_FEEDS.items():
            try:
                logger.info(f"Reading: {source_name}")

                feed = feedparser.parse(feed_url)

                if not feed.entries:
                    logger.warning(f"   No articles found in {source_name}")
                    continue

                count = 0
                for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:

                    link = entry.get('link', '')
                    if not link:
                        continue

                    article_id = hashlib.md5(link.encode()).hexdigest()[:12]

                    summary = entry.get('summary', '')
                    if summary:
                        summary_soup = BeautifulSoup(summary, 'html.parser')
                        summary = summary_soup.get_text()[:500]

                    content = self.get_article_text(link)

                    if not content and summary:
                        content = summary

                    if not content:
                        continue

                    article = {
                        'id': article_id,
                        'title': entry.get('title', 'No Title').strip(),
                        'link': link,
                        'summary': summary,
                        'source': source_name,
                        'date': str(self.today),
                        'scraped_at': self.timestamp,
                        'content': content,
                        'image_url': self._extract_image_url(entry)
                    }

                    all_articles.append(article)
                    count += 1

                    time.sleep(0.5)

                logger.info(f"   Got {count} articles from {source_name}")

            except Exception as e:
                logger.error(f"   Error with {source_name}: {e}")

        all_articles = self._remove_duplicates(all_articles)

        output_file = os.path.join(
            RAW_NEWS_DIR, f"raw_news_{self.today}.json"
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)

        logger.info(f"Total unique articles: {len(all_articles)}")
        logger.info(f"Saved to: {output_file}")

        return all_articles

    def _remove_duplicates(self, articles):
        seen = set()
        unique = []

        for article in articles:
            signature = article['title'].lower().strip()[:MIN_DUPLICATE_CHECK_LENGTH]

            if signature not in seen:
                seen.add(signature)
                unique.append(article)

        removed = len(articles) - len(unique)
        if removed > 0:
            logger.info(f"   Removed {removed} duplicate articles")

        return unique

    def _extract_image_url(self, entry):
        """Extract image URL from RSS entry"""
        # Try various common RSS image fields
        if hasattr(entry, 'media_content') and entry.media_content:
            return entry.media_content[0].get('url', '')
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            return entry.media_thumbnail[0].get('url', '')
        if hasattr(entry, 'enclosure') and entry.enclosure:
            enclosure = entry.enclosure
            if hasattr(enclosure, 'type') and enclosure.type and enclosure.type.startswith('image'):
                return getattr(enclosure, 'url', '')
        # Try to find image in content
        if hasattr(entry, 'content') and entry.content:
            try:
                content = entry.content[0].value
                soup = BeautifulSoup(content, 'html.parser')
                img = soup.find('img')
                if img and img.get('src'):
                    return img.get('src')
            except:
                pass
        return ""


if __name__ == "__main__":
    print("Testing News Scraper...")
    print("This will take 2-5 minutes...")
    print()

    scraper = NewsScraper()
    articles = scraper.fetch_all_news()

    print()
    print("=" * 50)
    print(f"Fetched {len(articles)} articles!")
    print("=" * 50)

    for a in articles[:5]:
        print(f"  [{a['source']}] {a['title'][:70]}")