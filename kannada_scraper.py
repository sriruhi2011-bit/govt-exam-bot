# kannada_scraper.py
# Scrapes news from Kannada RSS feeds

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import json
import hashlib
import os
import time

from config.settings import (
    KAN_RSS_FEEDS, KAN_RAW_NEWS_DIR,
    MAX_ARTICLES_PER_SOURCE,
    MAX_ARTICLE_CONTENT_LENGTH,
    REQUEST_TIMEOUT, MIN_CONTENT_LENGTH, MIN_DUPLICATE_CHECK_LENGTH,
    REQUEST_DELAY_SECONDS
)
from config.logger import setup_logger

logger = setup_logger("kan_scraper")


class KannadaScraper:

    def __init__(self):
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )
        }
        # Use IST timezone (UTC+5:30)
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.today = datetime.now(ist_offset).date()
        self.timestamp = datetime.now(ist_offset).strftime("%Y-%m-%d %H:%M:%S")

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

    def parse_date(self, entry):
        """Parse publication date from RSS entry"""
        try:
            if hasattr(entry, 'published'):
                return entry.published
            elif hasattr(entry, 'updated'):
                return entry.updated
            return None
        except:
            return None

    def fetch_feed(self, source_name, feed_url):
        """Fetch and parse a single RSS feed"""
        articles = []
        count = 0

        try:
            logger.info(f"   Fetching: {source_name}")
            feed = feedparser.parse(feed_url)

            if not feed.entries:
                logger.warning(f"   No entries in {source_name}")
                return articles

            for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
                try:
                    title = entry.title.strip() if hasattr(entry, 'title') else ''
                    link = entry.link.strip() if hasattr(entry, 'link') else ''

                    if not title or not link:
                        continue

                    # Get summary/description
                    summary = ""
                    if hasattr(entry, 'summary'):
                        summary = entry.summary
                    elif hasattr(entry, 'description'):
                        summary = entry.description
                    
                    # Clean HTML from summary
                    if summary:
                        soup = BeautifulSoup(summary, 'html.parser')
                        summary = soup.get_text().strip()

                    # Try to get full article content
                    content = self.get_article_text(link)
                    if content:
                        full_content = content
                    else:
                        full_content = summary[:MAX_ARTICLE_CONTENT_LENGTH]

                    if len(full_content) < MIN_CONTENT_LENGTH:
                        continue

                    articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary[:500] if summary else '',
                        'content': full_content,
                        'source': source_name,
                        'date': str(self.today),
                        'scraped_at': self.timestamp
                    })
                    count += 1

                    time.sleep(REQUEST_DELAY_SECONDS)

                except Exception as e:
                    logger.debug(f"   Error parsing entry: {e}")
                    continue

            logger.info(f"   Got {count} articles from {source_name}")

        except Exception as e:
            logger.error(f"   Error with {source_name}: {e}")

        return articles

    def fetch_all_news(self):
        """Fetch news from all Kannada RSS feeds"""
        all_articles = []
        seen_titles = set()

        logger.info(f"Starting Kannada news collection from {len(KAN_RSS_FEEDS)} sources...")

        for source_name, feed_url in KAN_RSS_FEEDS.items():
            articles = self.fetch_feed(source_name, feed_url)
            
            for article in articles:
                # Check for duplicates
                title_hash = hashlib.md5(
                    article['title'][:MIN_DUPLICATE_CHECK_LENGTH].encode()
                ).hexdigest()
                
                if title_hash not in seen_titles:
                    seen_titles.add(title_hash)
                    all_articles.append(article)

        # Save to file
        output_file = os.path.join(
            KAN_RAW_NEWS_DIR, f"raw_kan_{self.today}.json"
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)

        logger.info(f"Total: {len(all_articles)} unique Kannada articles")
        return all_articles


if __name__ == "__main__":
    print("Testing Kannada Scraper...")
    scraper = KannadaScraper()
    articles = scraper.fetch_all_news()
    print(f"\nScraped {len(articles)} Kannada articles")
    for a in articles[:5]:
        print(f"  [{a['source']}] {a['title'][:70]}")