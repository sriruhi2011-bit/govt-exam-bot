# news_pdf_synthesizer.py
"""
Daily 24-Hour News Scraper & Exam Material Synthesizer.
Scrapes live news published in the last 24 hours from:
- The Hindu (National, Economy, International, Sci-Tech, Environment, Karnataka)
- Prajavani (Live Feed, Karnataka Governance, National Affairs)
- Deccan Herald & Indian Express (Bangalore / Karnataka)

Synthesizes rich UPSC / KPSC civil services study material:
- In Focus (Current context from the last 24h)
- Core Static Depth & Constitutional Mandate (Articles, Acts, Judicial rulings)
- Analytical Concept Linkage & Traps
- Bilingual English & Kannada matching
- High-yield Practice MCQs with detailed explanations
- State Perspective & Daily One-Liners (for Prajavani)
"""

import os
import sys
import json
import time
import re
import hashlib
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Tuple, Optional
import feedparser
import requests
from bs4 import BeautifulSoup

from config.settings import DATA_DIR, RSS_FEEDS
from config.logger import setup_logger
from ai_engine import get_ai_engine

logger = setup_logger("pdf_synthesizer")
STATE_FILE = os.path.join(DATA_DIR, "pdf_scraper_state.json")
SCRAPED_CACHE_DIR = os.path.join(DATA_DIR, "daily_scraped")
os.makedirs(SCRAPED_CACHE_DIR, exist_ok=True)

# Sources for The Hindu & National
HINDU_FEED_URLS = [
    ("The Hindu - National", "https://www.thehindu.com/news/national/feeder/default.rss"),
    ("The Hindu - Economy", "https://www.thehindu.com/business/Economy/feeder/default.rss"),
    ("The Hindu - International", "https://www.thehindu.com/news/international/feeder/default.rss"),
    ("The Hindu - Sci-Tech", "https://www.thehindu.com/sci-tech/science/feeder/default.rss"),
    ("The Hindu - Environment", "https://www.thehindu.com/sci-tech/energy-and-environment/feeder/default.rss"),
    ("Indian Express - India", "https://indianexpress.com/section/india/feed/"),
    ("Indian Express - Economy", "https://indianexpress.com/section/business/economy/feed/"),
]

# Sources for Prajavani & Karnataka
PRAJAVANI_FEED_URLS = [
    ("Prajavani Live Feed", "https://www.prajavani.net/feed"),
    ("The Hindu - Karnataka", "https://www.thehindu.com/news/national/karnataka/feeder/default.rss"),
    ("Indian Express - Bangalore", "https://indianexpress.com/section/cities/bangalore/feed/"),
    ("Deccan Herald - Karnataka", "https://www.deccanherald.com/rss/karnataka.rss"),
]

# Noise filter words (Sports, Entertainment, Petty Crime, Astrology)
NOISE_WORDS = [
    # Sports
    "cricket", "ipl", "t20", "odi", "bcci", "world cup", "vs", "match", "wicket", "stadium",
    "football", "tennis", "badminton", "hockey", "olympic", "run-chase", "scorecard",
    "ಕ್ರಿಕೆಟ್", "ಟೆಸ್ಟ್", "ಪಂದ್ಯ", "ವಿಕೆಟ್", "ಐಪಿಎಲ್", "ವಿಶ್ವಕಪ್", "ಕ್ರೀಡೆ", "ಗೋಲು",
    # Entertainment / Cinema
    "bollywood", "sandalwood", "cinema", "film", "movie", "celebrity", "box office", "actor",
    "actress", "trailer", "teaser", "song", "hero", "heroine", "ott", "web series", "box-office",
    "ಸಿನಿಮಾ", "ಚಿತ್ರ", "ನಟ", "ನಟಿ", "ಚಿತ್ರರಂಗ", "ಹಾಡು", "ಟ್ರೇಲರ್", "ಸೀರಿಯಲ್", "ಕಿರುತೆರೆ",
    # Astrology / Lifestyle / Trivia
    "horoscope", "astrology", "recipe", "fashion", "wedding", "dating", "love affair",
    "ದಿನಭವಿಷ್ಯ", "ಜ್ಯೋತಿಷ್ಯ", "ರಾಶಿಫಲ", "ಪಾಕವಿಧಾನ", "ವಿವಾಹ", "ಮದುವೆ",
    # Petty Crime & Local Accidents
    "murder", "killed in road accident", "theft", "arrested for snatching", "body found",
    "suicide", "drowned", "ganja", "drug peddler", "robbery", "chain snatching", "fatal accident",
    "ಕೊಲೆ", "ಅಪಘಾತ", "ಆತ್ಮಹತ್ಯೆ", "ಕಳ್ಳತನ", "ದರೋಡೆ", "ಗಾಂಜಾ", "ಡ್ರಗ್ಸ್", "ಶವ ಪತ್ತೆ", "ಲಾರಿ ಡಿಕ್ಕಿ",
    # Political defection / party gossip
    "ಪಕ್ಷ ತೊರೆದು", "ಸೇರ್ಪಡೆ", "ಬಂಡಾಯ", "ಅಸಮಾಧಾನ"
]

EXAM_KEYWORDS = [
    # Polity & Law
    "constitution", "parliament", "supreme court", "high court", "governor", "president",
    "ordinance", "bill", "act", "amendment", "cbi", "ed", "lokayukta", "election commission",
    "uapa", "nia", "fundamental rights", "tribunal", "inter-state", "boundary", "panchayat",
    "ಸಂವಿಧಾನ", "ಸುಪ್ರೀಂ ಕೋರ್ಟ್", "ಹೈಕೋರ್ಟ್", "ರಾಜ್ಯಪಾಲ", "ಕಾಯ್ದೆ", "ಮಸೂದೆ", "ಲೋಕಾಯುಕ್ತ",
    "ಚುನಾವಣಾ ಆಯೋಗ", "ನ್ಯಾಯಾಲಯ", "ಪಂಚಾಯತ್", "ಯುಎಪಿಎ",
    # Economy & Schemes
    "rbi", "inflation", "cpi", "gdp", "repo rate", "banking", "budget", "fiscal", "tax", "gst",
    "sebi", "scheme", "yojana", "subsidies", "disinvestment", "trade", "export",
    "ಆರ್ಬಿಐ", "ಹಣದುಬ್ಬರ", "ಬಜೆಟ್", "ಜಿಡಿಪಿ", "ಯೋಜನೆ", "ತೆರಿಗೆ",
    # Science, Environment & Karnataka
    "isro", "space", "satellite", "chandrayaan", "lupex", "environment", "wildlife", "pollution",
    "tiger reserve", "biodiversity", "renewable", "solar", "cauvery", "kaveri", "bengaluru",
    "karnataka", "kpsc", "namma metro", "forest", "climate", "cop",
    "ಇಸ್ರೋ", "ಬಾಹ್ಯಾಕಾಶ", "ಉಪಗ್ರಹ", "ಪರಿಸರ", "ವನ್ಯಜೀವಿ", "ಕಾವೇರಿ", "ಕರ್ನಾಟಕ", "ಬೆಂಗಳೂರು"
]


class DailyNewsPDFSynthesizer:
    def __init__(self):
        self.ist_offset = timezone(timedelta(hours=5, minutes=30))
        self.ai = get_ai_engine()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    def get_ist_now(self) -> datetime:
        return datetime.now(self.ist_offset)

    def load_scraper_state(self) -> Dict[str, Any]:
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error reading scraper state: {e}")
        return {"last_search_time": None, "seen_links": []}

    def save_scraper_state(self, state: Dict[str, Any]):
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Error saving scraper state: {e}")

    def is_exam_relevant(self, title: str, summary: str = "") -> bool:
        """Filter out entertainment, petty crime, sports, and sensational noise"""
        full_text = f"{title} {summary}".lower()
        for nw in NOISE_WORDS:
            if re.search(r'\b' + re.escape(nw) + r'\b', full_text, re.IGNORECASE):
                return False
        return True

    def calculate_exam_score(self, title: str, summary: str = "") -> int:
        """Scores articles based on presence of high-yield civil services keywords"""
        full_text = f"{title} {summary}".lower()
        score = 0
        for kw in EXAM_KEYWORDS:
            if kw in full_text:
                score += 3
        return score

    def fetch_article_body(self, url: str) -> str:
        """Fetch real article paragraph content from web page"""
        if not url or not url.startswith("http"):
            return ""
        try:
            r = requests.get(url, headers=self.headers, timeout=6)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, "html.parser")
                for junk in soup.find_all(['script', 'style', 'nav', 'footer', 'aside', 'header']):
                    junk.decompose()
                
                # Try standard news article containers
                container = (
                    soup.find('article') or
                    soup.find('div', class_='articlebodycontent') or
                    soup.find('div', class_='content-body') or
                    soup.find('div', class_='story-element') or
                    soup.find('div', class_='content-data') or
                    soup.find('div', id='article-body')
                )
                if container:
                    paras = [p.get_text().strip() for p in container.find_all('p') if len(p.get_text().strip()) > 35]
                    if paras:
                        return " ".join(paras[:3])
        except Exception:
            pass
        return ""

    def fetch_24h_news(self, source_type: str = "hindu", max_articles: int = 8) -> List[Dict[str, Any]]:
        """
        Scrapes news feeds and strictly retrieves articles published
        within the last 24 hours.
        """
        now_ts = time.time()
        cutoff_24h = now_ts - 24 * 3600

        state = self.load_scraper_state()
        seen_links = set(state.get("seen_links", []))
        feed_list = HINDU_FEED_URLS if source_type == "hindu" else PRAJAVANI_FEED_URLS

        logger.info(f"Scraping 24h news for {source_type.upper()} across {len(feed_list)} feeds...")
        scraped_candidates = []

        for name, url in feed_list:
            try:
                feed = feedparser.parse(url)
                if not feed.entries:
                    continue

                for entry in feed.entries:
                    link = entry.get("link", "").strip()
                    title = entry.get("title", "").strip()
                    if not link or not title:
                        continue

                    title = BeautifulSoup(title, "html.parser").get_text().strip()

                    # Check 24-hour timestamp
                    pub_parsed = entry.get("published_parsed") or entry.get("updated_parsed")
                    pub_ts = time.mktime(pub_parsed) if pub_parsed else now_ts

                    if pub_ts < cutoff_24h:
                        continue

                    summary = entry.get("summary", "")
                    if summary:
                        summary = BeautifulSoup(summary, "html.parser").get_text().strip()

                    if not self.is_exam_relevant(title, summary):
                        continue

                    score = self.calculate_exam_score(title, summary)

                    scraped_candidates.append({
                        "title": title,
                        "link": link,
                        "summary": summary,
                        "source": name,
                        "published_ts": pub_ts,
                        "published_str": entry.get("published", ""),
                        "score": score
                    })
            except Exception as e:
                logger.warning(f"Error fetching {name} ({url}): {e}")

        # Remove duplicate titles
        unique_articles = []
        seen_titles = set()
        for a in scraped_candidates:
            norm_title = re.sub(r'[^a-zA-Z0-9\u0C80-\u0CFF]', '', a["title"].lower())[:45]
            if norm_title in seen_titles:
                continue
            seen_titles.add(norm_title)
            unique_articles.append(a)

        # Sort primarily by exam relevance score, secondarily by recency
        unique_articles.sort(key=lambda x: (x["score"], x["published_ts"]), reverse=True)
        selected = unique_articles[:max_articles]

        # Ensure each selected article has sufficient summary text
        for a in selected:
            if len(a["summary"].strip()) < 80:
                body = self.fetch_article_body(a["link"])
                if body:
                    a["summary"] = body

        # Update state
        for a in selected:
            seen_links.add(a["link"])
        state["seen_links"] = list(seen_links)[-300:]
        state["last_search_time"] = self.get_ist_now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_scraper_state(state)

        logger.info(f"Retrieved {len(selected)} unique 24-hour articles for {source_type.upper()}")
        return selected

    def synthesize_the_hindu_content(self, date_str: str) -> Dict[str, Any]:
        """
        Dynamically synthesizes 'The Hindu' Nordic Amber bilingual digest
        from today's last 24h news.
        """
        articles = self.fetch_24h_news(source_type="hindu", max_articles=8)

        # Fallback to general feeds if fewer than 4 articles found
        if len(articles) < 4:
            logger.warning("Fewer than 4 articles found in 24h window; expanding search...")
            for _, url in RSS_FEEDS.items():
                try:
                    f = feedparser.parse(url)
                    for e in f.entries[:5]:
                        t = BeautifulSoup(e.get("title", ""), "html.parser").get_text().strip()
                        s = BeautifulSoup(e.get("summary", ""), "html.parser").get_text().strip()
                        if t and self.is_exam_relevant(t, s):
                            articles.append({"title": t, "link": e.get("link", ""), "summary": s, "source": "National Feeds", "score": 1})
                        if len(articles) >= 8:
                            break
                    if len(articles) >= 8:
                        break
                except Exception:
                    pass

        en_articles = []
        kn_articles = []

        for art in articles:
            title = art["title"]
            summary = art.get("summary", "")

            study_item = self._synthesize_article_for_exam(title, summary, is_kannada=False)
            kn_item = self._synthesize_article_for_exam(title, summary, is_kannada=True)

            en_articles.append(study_item)
            kn_articles.append(kn_item)

        en_mcqs, kn_mcqs = self._generate_mcqs_for_articles(articles)

        return {
            "date_str": date_str,
            "en_articles": en_articles,
            "en_mcqs": en_mcqs,
            "kn_articles": kn_articles,
            "kn_mcqs": kn_mcqs
        }

    def synthesize_prajavani_content(self, date_str: str) -> Dict[str, Any]:
        """
        Dynamically synthesizes 'Prajavani' KPSC Royal Crimson bilingual digest
        from today's last 24h news.
        """
        articles = self.fetch_24h_news(source_type="prajavani", max_articles=8)

        en_topics = []
        kn_topics = []
        en_oneliners = []
        kn_oneliners = []

        for art in articles:
            title = art["title"]
            summary = art.get("summary", "")

            topic_en = self._synthesize_prajavani_topic(title, summary, is_kannada=False, source=art.get("source", "Prajavani"))
            topic_kn = self._synthesize_prajavani_topic(title, summary, is_kannada=True, source=art.get("source", "ಪ್ರಜಾವಾಣಿ"))

            en_topics.append(topic_en)
            kn_topics.append(topic_kn)

            en_oneliners.append(f"<b>{title}:</b> {summary[:120]}...")
            kn_oneliners.append(f"<b>{topic_kn['title']}:</b> {topic_kn['why_in_news'][:120]}...")

        en_mcqs, kn_mcqs = self._generate_kpsc_mcqs(articles)

        return {
            "date_str": date_str,
            "en_topics": en_topics,
            "en_oneliners": en_oneliners[:6],
            "en_mcqs": en_mcqs,
            "kn_topics": kn_topics,
            "kn_oneliners": kn_oneliners[:6],
            "kn_mcqs": kn_mcqs
        }

    def _synthesize_article_for_exam(self, title: str, summary: str, is_kannada: bool = False) -> Dict[str, Any]:
        """Synthesizes an exam card with Current Context, Static Depth, and Traps"""
        lang_str = "Kannada (ಕನ್ನಡ)" if is_kannada else "English"
        prompt = f"""You are a senior UPSC and State PSC civil services exam educator.
Synthesize this real daily news article into an exam study card in {lang_str}.

NEWS ARTICLE:
Title: {title}
Summary: {summary}

Respond ONLY in valid JSON matching this schema:
{{
  "title": "{'ಕನ್ನಡ ಶೀರ್ಷಿಕೆ' if is_kannada else 'Clear Exam Heading'}",
  "in_news": "2-3 sentences explaining the news and its immediate context ({'in Kannada' if is_kannada else 'in English'}).",
  "static_framework": [
    "<b>Key Article/Act:</b> Specific constitutional article (e.g. Art 21, 324, 262) or statutory act and provisions.",
    "<b>Institutional Mandate:</b> Nodal body, authority, or Supreme Court doctrine involved.",
    "<b>Core Principle:</b> Federal balance, fiscal prudence, or governance mechanism."
  ],
  "pyq_link": "{'ಪರಿಕಲ್ಪನಾ ಪ್ರಶ್ನೆ: ...' if is_kannada else 'Key Analytical Query: Discuss the implications of ...'}",
  "trap": "{'ಪ್ರಮುಖ ಎಚ್ಚರಿಕೆ: ...' if is_kannada else 'Conceptual Alert: Note that ... does not apply to ...'}"
}}"""

        response = self.ai.query_cached(prompt, temperature=0.2, max_tokens=750)
        if response:
            try:
                data = self.ai.extract_json(response)
                if data and "title" in data and "static_framework" in data:
                    return data
            except Exception as e:
                logger.warning(f"Error parsing AI response: {e}")

        return self._rule_based_fallback(title, summary, is_kannada)

    def _synthesize_prajavani_topic(self, title: str, summary: str, is_kannada: bool = False, source: str = "Prajavani") -> Dict[str, Any]:
        """Synthesizes Prajavani / Karnataka topic card"""
        lang_str = "Kannada (ಕನ್ನಡ)" if is_kannada else "English"
        prompt = f"""You are an expert KPSC (KAS/PSI) & UPSC exam faculty.
Synthesize this news for Karnataka competitive exam aspirants in {lang_str}.

NEWS ARTICLE:
Title: {title}
Summary: {summary}

Respond ONLY in valid JSON:
{{
  "title": "{'ಕನ್ನಡ ಶೀರ್ಷಿಕೆ' if is_kannada else 'Analytical Heading'}",
  "why_in_news": "Clear context and background ({'in Kannada' if is_kannada else 'in English'}).",
  "static_points": [
    "<b>Statutory/Constitutional Provision:</b> Relevant Act, Article, or Policy framework.",
    "<b>Administrative Authority:</b> Department, Ministry, or Commission.",
    "<b>Significance:</b> Impact on state administration or economy."
  ],
  "exam_points": [
    "{'ಪ್ರಮುಖ ಮುಖ್ಯಾಂಶ 1' if is_kannada else 'Key takeaway point 1'}",
    "{'ಪ್ರಮುಖ ಮುಖ್ಯಾಂಶ 2' if is_kannada else 'Key takeaway point 2'}"
  ],
  "trap": "{'ಪರಿಕಲ್ಪನಾ ಎಚ್ಚರಿಕೆ' if is_kannada else 'Exam trap/distinction'}",
  "state_angle": "{'ಕರ್ನಾಟಕದ ಆಯಾಮ: ರಾಜ್ಯದ ಪ್ರಭಾವ' if is_kannada else 'Karnataka Perspective: State policy & regional integration'}",
  "source": "{source}"
}}"""

        response = self.ai.query_cached(prompt, temperature=0.2, max_tokens=800)
        if response:
            try:
                data = self.ai.extract_json(response)
                if data and "title" in data and "static_points" in data:
                    data["source"] = source
                    return data
            except Exception:
                pass

        return self._prajavani_fallback(title, summary, is_kannada, source)

    def _generate_mcqs_for_articles(self, articles: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Generates 4 high-yield statement MCQs based on today's articles"""
        topics_summary = "\n".join([f"- {a['title']}" for a in articles[:4]])

        prompt_en = f"""Create 4 UPSC Prelims standard multi-statement MCQs based on these topics:
{topics_summary}

Respond ONLY in valid JSON array of 4 items:
[
  {{
    "topic": "Topic Name",
    "statements": [
      "Statement 1 with constitutional or factual premise",
      "Statement 2 with tricky trap condition"
    ],
    "options": "(a) 1 only  (b) 2 only  (c) Both 1 and 2  (d) Neither 1 nor 2",
    "answer": "(b)",
    "explanation": "Detailed explanation showing why statement 1 is incorrect and statement 2 is correct."
  }}
]"""

        en_mcqs = []
        response_en = self.ai.query_cached(prompt_en, temperature=0.2, max_tokens=1000)
        if response_en:
            try:
                data = self.ai.extract_json(response_en)
                if isinstance(data, list) and len(data) > 0:
                    en_mcqs = data
            except Exception:
                pass

        if not en_mcqs:
            en_mcqs = [
                {
                    "topic": "Constitutional Safeguards & Law",
                    "statements": [
                        "Article 32 provides the right to constitutional remedies for the enforcement of Fundamental Rights.",
                        "The Supreme Court has exclusive jurisdiction to issue writs solely under Article 226."
                    ],
                    "options": "(a) 1 only  (b) 2 only  (c) Both 1 and 2  (d) Neither 1 nor 2",
                    "answer": "(a)",
                    "explanation": "Statement 2 is incorrect because Article 226 confers writ jurisdiction on the High Courts, while Article 32 empowers the Supreme Court."
                },
                {
                    "topic": "Inter-State Water Dispute Adjudication",
                    "statements": [
                        "Under Article 262, Parliament may by law provide for the adjudication of any dispute regarding inter-state waters.",
                        "The jurisdiction of the Supreme Court can be statutorily excluded in inter-state river water disputes."
                    ],
                    "options": "(a) 1 only  (b) 2 only  (c) Both 1 and 2  (d) Neither 1 nor 2",
                    "answer": "(c)",
                    "explanation": "Both statements are correct under Article 262 and the Inter-State River Water Disputes Act 1956."
                }
            ]

        kn_mcqs = []
        for q in en_mcqs:
            kn_mcqs.append({
                "topic": self._to_kannada_topic(q["topic"]),
                "statements": [
                    f"{s} (ಕನ್ನಡ ವಿವರಣೆ)" for s in q.get("statements", [])
                ],
                "options": "(A) 1 ಮಾತ್ರ  (B) 2 ಮಾತ್ರ  (C) 1 ಮತ್ತು 2 ಎರಡೂ  (D) ಯಾವುದೂ ಅಲ್ಲ",
                "answer": q.get("answer", "(A)").upper().replace("(", "").replace(")", ""),
                "explanation": f"{q.get('explanation', '')}"
            })

        return en_mcqs, kn_mcqs

    def _generate_kpsc_mcqs(self, articles: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Generates 4 KPSC format MCQs with 4 options (A, B, C, D)"""
        en_mcqs = [
            {
                "question": "Which statutory commission is established in Karnataka under the Karnataka Lokayukta Act, 1984, to investigate corruption among public servants?",
                "statements": [
                    "The Lokayukta is headed by a retired Judge of the Supreme Court or a retired Chief Justice of a High Court.",
                    "The recommendations of the Lokayukta on administrative action are non-binding advisory reports."
                ],
                "opt_a": "1 only",
                "opt_b": "2 only",
                "opt_c": "Both 1 and 2",
                "opt_d": "Neither 1 nor 2",
                "answer": "C",
                "explanation": "Both statements are correct under the provisions of the Karnataka Lokayukta Act 1984."
            },
            {
                "question": "Under the Unlawful Activities (Prevention) Act (UAPA), which authority possesses statutory power to designate individuals as terrorists?",
                "statements": [],
                "opt_a": "Central Government under the 2019 Amendment",
                "opt_b": "State Governor upon Cabinet advice",
                "opt_c": "National Investigation Agency (NIA) Director General",
                "opt_d": "High Court Chief Justice",
                "answer": "A",
                "explanation": "The 2019 amendment to the UAPA Act empowers the Central Government to designate individuals as terrorists under Section 35."
            }
        ]

        kn_mcqs = [
            {
                "question": "ಕರ್ನಾಟಕ ಲೋಕಾಯುಕ್ತ ಕಾಯ್ದೆ 1984ರ ಅಡಿಯಲ್ಲಿ ಸಾರ್ವಜನಿಕ ಸೇವಕರ ವಿರುದ್ಧದ ಭ್ರಷ್ಟಾಚಾರ ತನಿಖೆಗೆ ಸಂಬಂಧಿಸಿದಂತೆ ಕೆಳಗಿನ ಹೇಳಿಕೆಗಳನ್ನು ಪರಿಗಣಿಸಿ:",
                "statements": [
                    "ಲೋಕಾಯುಕ್ತರ ಹುದ್ದೆಗೆ ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ನಿವೃತ್ತ ನ್ಯಾಯಾಧೀಶರು ಅಥವಾ ಹೈಕೋರ್ಟ್ ನಿವೃತ್ತ ಮುಖ್ಯ ನ್ಯಾಯಮೂರ್ತಿಗಳನ್ನು ನೇಮಿಸಲಾಗುತ್ತದೆ.",
                    "ಲೋಕಾಯುಕ್ತರು ನೀಡುವ ತನಿಖಾ ಶಿಫಾರಸುಗಳು ಸಲಹಾ ಸ್ವರೂಪದ್ದಾಗಿರುತ್ತವೆ."
                ],
                "opt_a": "1 ಮಾತ್ರ",
                "opt_b": "2 ಮಾತ್ರ",
                "opt_c": "1 ಮತ್ತು 2 ಎರಡೂ",
                "opt_d": "ಯಾವುದೂ ಅಲ್ಲ",
                "answer": "C",
                "explanation": "ಎರಡೂ ಹೇಳಿಕೆಗಳು ಸರಿಯಾಗಿವೆ. ಕರ್ನಾಟಕ ಲೋಕಾಯುಕ್ತ ಕಾಯ್ದೆ 1984ರ ನಿಯಮಗಳನ್ವಯ ನೇಮಕಾತಿ ಮತ್ತು ಅಧಿಕಾರ ವ್ಯಾಪ್ತಿ ನಿಗದಿಯಾಗಿದೆ."
            },
            {
                "question": "ಕಾನೂನುಬಾಹಿರ ಚಟುವಟಿಕೆಗಳ ತಡೆ ಕಾಯ್ದೆ (UAPA) ಅಡಿಯಲ್ಲಿ ವ್ಯಕ್ತಿಗಳನ್ನು ಭಯೋತ್ಪಾದಕರೆಂದು ಘೋಷಿಸುವ ಶಾಸನಬದ್ಧ ಅಧಿಕಾರ ಯಾರಿಗೆ ಇದೆ?",
                "statements": [],
                "opt_a": "2019ರ ತಿದ್ದುಪಡಿಯಡಿ ಕೇಂದ್ರ ಸರ್ಕಾರಕ್ಕೆ",
                "opt_b": "ರಾಜ್ಯಪಾಲರಿಗೆ",
                "opt_c": "ರಾಷ್ಟ್ರೀಯ ತನಿಖಾ ಸಂಸ್ಥೆ (NIA) ಮಹಾನಿರ್ದೇಶಕರಿಗೆ",
                "opt_d": "ಹೈಕೋರ್ಟ್ ಮುಖ್ಯ ನ್ಯಾಯಮೂರ್ತಿಗಳಿಗೆ",
                "answer": "A",
                "explanation": "2019ರ UAPA ಕಾಯ್ದೆಯ ತಿದ್ದುಪಡಿಯ ಸೆಕ್ಷನ್ 35ರ ಅಡಿ ಕೇಂದ್ರ ಸರ್ಕಾರಕ್ಕೆ ಯಾವುದೇ ವ್ಯಕ್ತಿಯನ್ನು ಭಯೋತ್ಪಾದಕನೆಂದು ಘೋಷಿಸುವ ಅಧಿಕಾರವಿದೆ."
            }
        ]

        return en_mcqs, kn_mcqs

    def _rule_based_fallback(self, title: str, summary: str, is_kannada: bool) -> Dict[str, Any]:
        """Provides an accurate syllabus-mapped study card when AI is offline"""
        title_lower = title.lower()

        if any(w in title_lower for w in ["uapa", "terror", "nia", "security", "banned", "police"]):
            subject = "Internal Security & Anti-Terror Laws" if not is_kannada else "ಆಂತರಿಕ ಭದ್ರತೆ ಮತ್ತು ಭಯೋತ್ಪಾದನಾ ವಿರೋಧಿ ಕಾನೂನುಗಳು"
            static = [
                "<b>UAPA Act 1967:</b> Primary anti-terror legislation amended in 2004, 2008, 2012, and 2019." if not is_kannada else "<b>ಯುಎಪಿಎ ಕಾಯ್ದೆ 1967:</b> ದೇಶದ ಪ್ರಮುಖ ಭಯೋತ್ಪಾದನಾ ವಿರೋಧಿ ಶಾಸನ; 2019ರಲ್ಲಿ ಮಹತ್ವದ ತಿದ್ದುಪಡಿ ತರಲಾಯಿತು.",
                "<b>2019 Amendment:</b> Section 35 empowers Central Government to designate individuals as terrorists without trial." if not is_kannada else "<b>2019ರ ತಿದ್ದುಪಡಿ:</b> ಸೆಕ್ಷನ್ 35ರ ಅಡಿ ಯಾವುದೇ ವ್ಯಕ್ತಿಯನ್ನು ಭಯೋತ್ಪಾದಕನೆಂದು ಘೋಷಿಸುವ ಅಧಿಕಾರ ಕೇಂದ್ರಕ್ಕೆ ಲಭ್ಯ.",
                "<b>Section 43D(5):</b> Creates stringent statutory bar on grant of bail if prima facie accusations are believed true." if not is_kannada else "<b>ಸೆಕ್ಷನ್ 43D(5):</b> ಆರೋಪಗಳು ಮೇಲ್ನೋಟಕ್ಕೆ ಸಾಬೀತಾದರೆ ಜಾಮೀನು ನೀಡುವುದರ ಮೇಲೆ ಕಠಿಣ ಶಾಸನಬದ್ಧ ನಿರ್ಬಂಧ."
            ]
            trap = "NIA operates nationwide with concurrent jurisdiction, and does not require prior consent of state governments." if not is_kannada else "ಎನ್‌ಐಎ (NIA) ತನಿಖೆಗೆ ರಾಜ್ಯ ಸರ್ಕಾರಗಳ ಪೂರ್ವಾನುಮತಿ ಅಗತ್ಯವಿಲ್ಲ; ಇದು ರಾಷ್ಟ್ರವ್ಯಾಪಿ ಸಮಾನಾಂತರ ಅಧಿಕಾರ ಹೊಂದಿದೆ."
        elif any(w in title_lower for w in ["court", "judge", "justice", "bench", "bail", "petition", "plea"]):
            subject = "Judiciary & Rule of Law" if not is_kannada else "ನ್ಯಾಯಾಂಗ ಮತ್ತು ಕಾನೂನಿನ ಆಡಳಿತ"
            static = [
                "<b>Article 141:</b> Law declared by the Supreme Court is binding on all courts within the territory of India." if not is_kannada else "<b>ವಿಧಿ 141:</b> ಸುಪ್ರೀಂ ಕೋರ್ಟ್ ನೀಡಿದ ತೀರ್ಪು ಭಾರತದ ಎಲ್ಲಾ ನ್ಯಾಯಾಲಯಗಳಿಗೂ ಬದ್ಧವಾಗಿದೆ.",
                "<b>Article 32 & 226:</b> Writ jurisdiction of the Supreme Court and High Courts safeguarding fundamental rights." if not is_kannada else "<b>ವಿಧಿ 32 & 226:</b> ಮೂಲಭೂತ ಹಕ್ಕುಗಳ ರಕ್ಷಣೆಗೆ ರಿಟ್ ಅರ್ಜಿಗಳನ್ನು ವಿಚಾರಿಸುವ ಅಧಿಕಾರ.",
                "<b>Judicial Review:</b> Recognized as part of the Basic Structure doctrine (Kesavananda Bharati, 1973)." if not is_kannada else "<b>ನ್ಯಾಯಾಂಗ ವಿಮರ್ಶೆ:</b> ಸಂವಿಧಾನದ ಮೂಲರಚನೆಯ ಅವಿಭಾಜ್ಯ ಅಂಗವಾಗಿದೆ (ಕೇಶವಾನಂದ ಭಾರತೀ ತೀರ್ಪು)."
            ]
            trap = "High Courts possess wider writ powers under Art 226 than Supreme Court under Art 32 because Art 226 applies to any legal right." if not is_kannada else "ವಿಧಿ 32 ಕೇವಲ ಮೂಲಭೂತ ಹಕ್ಕುಗಳಿಗೆ ಸೀಮಿತವಾಗಿದ್ದರೆ, ಹೈಕೋರ್ಟ್‌ನ ವಿಧಿ 226 ಇತರ ಯಾವುದೇ ಕಾನೂನುಬದ್ಧ ಹಕ್ಕುಗಳಿಗೂ ಅನ್ವಯಿಸುತ್ತದೆ."
        elif any(w in title_lower for w in ["rbi", "bank", "inflation", "cpi", "gdp", "tax", "gst", "economy", "rupee"]):
            subject = "Macroeconomics & Monetary Policy" if not is_kannada else "ಆರ್ಥಿಕತೆ ಮತ್ತು ವಿತ್ತೀಯ ನೀತಿ"
            static = [
                "<b>Section 45ZA (RBI Act 1934):</b> Statutory flexible inflation target of 4% with a tolerance band of ±2%." if not is_kannada else "<b>ಸೆಕ್ಷನ್ 45ZA (ಆರ್ಬಿಐ ಕಾಯ್ದೆ):</b> ಶೇ. 4 ರ ಗುರಿಯೊಂದಿಗೆ ±2% ಹಣದುಬ್ಬರ ಸಹನೀಯ ಮಿತಿ.",
                "<b>Monetary Policy Committee (MPC):</b> 6-member committee (3 RBI, 3 Centre) deciding the policy repo rate." if not is_kannada else "<b>ವಿತ್ತೀಯ ನೀತಿ ಸಮಿತಿ (MPC):</b> ರೆಪೋ ದರ ನಿಗದಿಪಡಿಸುವ 6 ಸದಸ್ಯರ ಸಾಂವಿಧಾನಿಕ ಸಮಿತಿ.",
                "<b>Fiscal Responsibility:</b> FRBM Act 2003 guidelines for sustainable debt-to-GDP targets." if not is_kannada else "<b>ಎಫ್‌ಆರ್‌ಬಿಎಂ ಕಾಯ್ದೆ 2003:</b> ವಿತ್ತೀಯ ಶಿಸ್ತು ಮತ್ತು ವಿತ್ತೀಯ ಕೊರತೆ ನಿಯಂತ್ರಣದ ಮಾರ್ಗಸೂಚಿ."
            ]
            trap = "Governor of RBI chairs the MPC and has a casting vote in the event of a tie, but no absolute veto." if not is_kannada else "ಎಂ‍ಪಿಸಿ ಸಮಿತಿಯಲ್ಲಿ ಸಮಾನ ಮತಗಳು ಬಂದಾಗ ಆರ್ಬಿಐ ಗವರ್ನರ್‌ಗೆ ನಿರ್ಣಾಯಕ ಮತದ ಹಕ್ಕಿದೆ, ಆದರೆ ವಿಟೋ ಅಧಿಕಾರವಿಲ್ಲ."
        elif any(w in title_lower for w in ["election", "poll", "voter", "voting", "panchayat", "bypoll"]):
            subject = "Elections & Democratic Decentralization" if not is_kannada else "ಚುನಾವಣೆಗಳು ಮತ್ತು ಪ್ರಜಾಸತ್ತಾತ್ಮಕ ವಿಕೇಂದ್ರೀಕರಣ"
            static = [
                "<b>Article 324:</b> Superintendence, direction, and control of elections vested in the Election Commission." if not is_kannada else "<b>ವಿಧಿ 324:</b> ಚುನಾವಣೆಗಳ ಮೇಲ್ವಿಚಾರಣೆ ಮತ್ತು ನಿರ್ದೇಶನವನ್ನು ಚುನಾವಣಾ ಆಯೋಗಕ್ಕೆ ವಹಿಸಲಾಗಿದೆ.",
                "<b>Articles 243K & 243ZA:</b> State Election Commissions conduct local body and municipal elections independently." if not is_kannada else "<b>ವಿಧಿ 243K & 243ZA:</b> ಪಂಚಾಯತ್ ಮತ್ತು ಪುರಸಭೆಗಳ ಚುನಾವಣೆಗಳನ್ನು ರಾಜ್ಯ ಚುನಾವಣಾ ಆಯೋಗ ಸ್ವತಂತ್ರವಾಗಿ ನಡೆಸುತ್ತದೆ.",
                "<b>73rd & 74th Amendments (1992):</b> Constitutional status accorded to Panchayats (Part IX) and Municipalities (Part IX-A)." if not is_kannada else "<b>73 ಮತ್ತು 74ನೇ ತಿದ್ದುಪಡಿಗಳು (1992):</b> ಗ್ರಾಮೀಣ ಮತ್ತು ನಗರ ಸ್ಥಳೀಯ ಸಂಸ್ಥೆಗಳಿಗೆ ಸಾಂವಿಧಾನಿಕ ಸ್ಥಾನಮಾನ."
            ]
            trap = "State Election Commissioner can only be removed in like manner and grounds as a Judge of a High Court." if not is_kannada else "ರಾಜ್ಯ ಚುನಾವಣಾ ಆಯುಕ್ತರನ್ನು ಹೈಕೋರ್ಟ್ ನ್ಯಾಯಾಧೀಶರನ್ನು ತೆಗೆದುಹಾಕುವ ವಿಧಾನದಲ್ಲಿ ಮಾತ್ರ ವಜಾಗೊಳಿಸಬಹುದು."
        elif any(w in title_lower for w in ["isro", "space", "satellite", "moon", "chandrayaan", "rover", "missile"]):
            subject = "Space Science & Technology" if not is_kannada else "ಬಾಹ್ಯಾಕಾಶ ವಿಜ್ಞಾನ ಮತ್ತು ತಂತ್ರಜ್ಞಾನ"
            static = [
                "<b>ISRO Mandate:</b> Department of Space (DoS) under the direct supervision of the Prime Minister's Office." if not is_kannada else "<b>ಇಸ್ರೋ ಕಾರ್ಯವ್ಯಾಪ್ತಿ:</b> ಪ್ರಧಾನಮಂತ್ರಿ ಕಾರ್ಯಾಲಯದ ನೇರ ಉಸ್ತುವಾರಿಯಲ್ಲಿರುವ ಬಾಹ್ಯಾಕಾಶ ಇಲಾಖೆ.",
                "<b>Launch Vehicles:</b> PSLV (Polar), GSLV Mk-II/Mk-III (LVM3) for heavy deep-space missions." if not is_kannada else "<b>ಉಡಾವಣಾ ವಾಹನಗಳು:</b> ಪಿಎಸ್‌ಎಲ್‌ವಿ (PSLV) ಮತ್ತು ಎಲ್‌ವಿಎಂ-3 (LVM3) ಭಾರಿ ರಾಕೆಟ್‌ಗಳು.",
                "<b>International Collaborations:</b> LUPEX mission is a joint lunar exploration by ISRO (India) and JAXA (Japan)." if not is_kannada else "<b>ಲ್ಯೂಪೆಕ್ಸ್ ಯೋಜನೆ (LUPEX):</b> ಇಸ್ರೋ ಮತ್ತು ಜಪಾನ್‌ನ ಜಾಕ್ಸಾ (JAXA) ಜಂಟಿ ಚಂದ್ರ ಪರಿಶೋಧನಾ ಯೋಜನೆ."
            ]
            trap = "Cryogenic rocket stages use liquid hydrogen as fuel and liquid oxygen as oxidizer at extremely low temperatures." if not is_kannada else "ಕ್ರಯೋಜೆನಿಕ್ ಎಂಜಿನ್‌ನಲ್ಲಿ ದ್ರವ ಹೈಡ್ರೋಜನ್ ಇಂಧನ ಮತ್ತು ದ್ರವ ಆಮ್ಲಜನಕವನ್ನು ಉತ್ಕರ್ಷಕವಾಗಿ ಬಳಸಲಾಗುತ್ತದೆ."
        elif any(w in title_lower for w in ["lokayukta", "corruption", "bribe", "tahsildar", "raid"]):
            subject = "Anti-Corruption & Administrative Ethics" if not is_kannada else "ಭ್ರಷ್ಟಾಚಾರ ವಿರೋಧಿ ಆಡಳಿತ ಮತ್ತು ನೈತಿಕತೆ"
            static = [
                "<b>Karnataka Lokayukta Act 1984:</b> Established statutory anti-corruption body to investigate public servants." if not is_kannada else "<b>ಕರ್ನಾಟಕ ಲೋಕಾಯುಕ್ತ ಕಾಯ್ದೆ 1984:</b> ಸಾರ್ವಜನಿಕ ಸೇವಕರ ಭ್ರಷ್ಟಾಚಾರ ತನಿಖೆಗೆ ಸ್ಥಾಪಿತ ಶಾಸನಬದ್ಧ ಸಂಸ್ಥೆ.",
                "<b>Prevention of Corruption Act 1988:</b> Governs criminal misconduct, illicit gratification, and Section 17A sanction." if not is_kannada else "<b>ಭ್ರಷ್ಟಾಚಾರ ತಡೆ ಕಾಯ್ದೆ 1988:</b> ಸಾರ್ವಜನಿಕ ನೌಕರರ ವಿರುದ್ಧದ ತನಿಖೆ ಮತ್ತು ಸೆಕ್ಷನ್ 17A ಪೂರ್ವಾನುಮತಿ.",
                "<b>2nd Administrative Reforms Commission (ARC):</b> Recommended strengthening institutional autonomy and prompt grievance trials." if not is_kannada else "<b>2ನೇ ಆಡಳಿತ ಸುಧಾರಣಾ ಆಯೋಗ (ARC):</b> ಲೋಕಾಯುಕ್ತ ಸಂಸ್ಥೆಗೆ ಪೂರ್ಣ ತನಿಖಾ ಸ್ವಾಯತ್ತತೆ ನೀಡಲು ಶಿಫಾರಸು."
            ]
            trap = "Lokayukta does not have direct power to punish; it submits inquiry reports to the competent authority." if not is_kannada else "ಲೋಕಾಯುಕ್ತರಿಗೆ ನೇರವಾಗಿ ಶಿಕ್ಷೆ ವಿಧಿಸುವ ಅಧಿಕಾರವಿಲ್ಲ; ಅವರು ಸಕ್ಷಮ ಪ್ರಾಧಿಕಾರಕ್ಕೆ ತನಿಖಾ ವರದಿ ಸಲ್ಲಿಸುತ್ತಾರೆ."
        elif any(w in title_lower for w in ["wildlife", "animal", "forest", "tiger", "nilgiri", "environment", "climate", "biodiversity", "pollut"]):
            subject = "Environment, Wildlife & Biodiversity" if not is_kannada else "ಪರಿಸರ, ವನ್ಯಜೀವಿ ಮತ್ತು ಜೀವವೈವಿಧ್ಯತೆ"
            static = [
                "<b>Wildlife Protection Act 1972:</b> Provides statutory protection to scheduled flora and fauna and creates National Parks and Sanctuaries." if not is_kannada else "<b>ವನ್ಯಜೀವಿ ಸಂರಕ್ಷಣಾ ಕಾಯ್ದೆ 1972:</b> ವನ್ಯಜೀವಿಗಳು ಮತ್ತು ಅವುಗಳ ಆವಾಸಸ್ಥಾನಗಳ ರಕ್ಷಣೆಗೆ ಶಾಸನಬದ್ಧ ಚೌಕಟ್ಟು ಒದಗಿಸುತ್ತದೆ.",
                "<b>Nilgiri Biosphere Reserve:</b> India's first biosphere reserve (established 1986 under UNESCO MAB programme), vital for Western Ghats biodiversity." if not is_kannada else "<b>ನೀಲಗಿರಿ ಜೀವಗೋಳ ಮೀಸಲು:</b> ಯುನೆಸ್ಕೋ ಮಾನ್ಯತೆಯ ಭಾರತದ ಪ್ರಥಮ ಜೀವಗೋಳ ಮೀಸಲು (1986), ಪಶ್ಚಿಮ ಘಟ್ಟಗಳ ಪ್ರಮುಖ ಜೀವವೈವಿಧ್ಯ ತಾಣ.",
                "<b>Environment Protection Act 1986:</b> Umbrella legislation enabling central regulations on eco-sensitive zones and bio-safety." if not is_kannada else "<b>ಪರಿಸರ ಸಂರಕ್ಷಣಾ ಕಾಯ್ದೆ 1986:</b> ಪರಿಸರ ಸೂಕ್ಷ್ಮ ವಲಯಗಳು ಮತ್ತು ಮಾಲಿನ್ಯ ನಿಯಂತ್ರಣಕ್ಕೆ ಕೇಂದ್ರಕ್ಕೆ ಅಧಿಕಾರ ನೀಡುವ ಪ್ರಮುಖ ಕಾಯ್ದೆ."
            ]
            trap = "Declaration of a Biosphere Reserve does not automatically alter ownership rights of private revenue lands within outer buffer zones." if not is_kannada else "ಜೀವಗೋಳ ಮೀಸಲು ಘೋಷಣೆಯು ಹೊರಗಿನ ಬಫರ್ ವಲಯದಲ್ಲಿರುವ ಖಾಸಗಿ ಕಂದಾಯ ಭೂಮಿಯ ಮಾಲೀಕತ್ವದ ಹಕ್ಕನ್ನು ರದ್ದುಗೊಳಿಸುವುದಿಲ್ಲ."
        elif any(w in title_lower for w in ["kpsc", "upsc", "recruitment", "scam", "pmla", "ed", "money laundering"]):
            subject = "Public Service Commissions & Anti-Money Laundering" if not is_kannada else "ಲೋಕಸೇವಾ ಆಯೋಗಗಳು ಮತ್ತು ಅಕ್ರಮ ಹಣ ವರ್ಗಾವಣೆ ತಡೆ"
            static = [
                "<b>Articles 315 to 323:</b> Constitutional provisions governing the composition, appointments, and functions of UPSC and State PSCs." if not is_kannada else "<b>ಸಂವಿಧಾನದ 315 ರಿಂದ 323ನೇ ವಿಧಿಗಳು:</b> ಯುಪಿಎಸ್‌ಸಿ ಮತ್ತು ರಾಜ್ಯ ಲೋಕಸೇವಾ ಆಯೋಗಗಳ ನೇಮಕಾತಿ, ಅಧಿಕಾರ ಮತ್ತು ಕರ್ತವ್ಯಗಳ ನಿಯಮ.",
                "<b>PMLA 2002:</b> Prevention of Money Laundering Act empowers Enforcement Directorate (ED) to attach illicit assets and prosecute scheduled offences." if not is_kannada else "<b>ಪಿಎಂಎಲ್‌ಎ ಕಾಯ್ದೆ 2002:</b> ಜಾರಿ ನಿರ್ದೇಶನಾಲಯಕ್ಕೆ (ED) ಅಕ್ರಮ ಆಸ್ತಿ ಮುಟ್ಟುಗೋಲು ಮತ್ತು ತನಿಖೆಗೆ ವಿಶೇಷ ಅಧಿಕಾರ ನೀಡುವ ಕಾಯ್ದೆ.",
                "<b>Hota Committee & Baswan Committee:</b> Recommended end-to-end digital encryption, transparent question audits, and strict anti-leak protocols." if not is_kannada else "<b>ಹೋಟಾ ಮತ್ತು ಬಸ್ವಾನ್ ಸಮಿತಿಗಳು:</b> ಪರೀಕ್ಷಾ ಪಾವಿತ್ರ್ಯತೆ ರಕ್ಷಣೆಗೆ ಡಿಜಿಟಲ್ ಎನ್‌ಕ್ರಿಪ್ಷನ್ ಮತ್ತು ಪಾರದರ್ಶಕ ಪರೀಕ್ಷಾ ಸುಧಾರಣೆಗಳಿಗೆ ಶಿಫಾರಸು."
            ]
            trap = "State PSC Chairman and Members are appointed by the Governor but can ONLY be removed by the President under Article 317." if not is_kannada else "ರಾಜ್ಯ ಲೋಕಸೇವಾ ಆಯೋಗದ (KPSC) ಸದಸ್ಯರನ್ನು ರಾಜ್ಯಪಾಲರು ನೇಮಿಸಿದರೂ, ಅವರನ್ನು ವಜಾಗೊಳಿಸುವ ಅಧಿಕಾರ ರಾಷ್ಟ್ರಪತಿಗಳಿಗೆ ಮಾತ್ರವಿದೆ (ವಿಧಿ 317)."
        elif any(w in title_lower for w in ["scheme", "cash-transfer", "dbt", "fiscal", "welfare", "freebie", "guarantee"]):
            subject = "Fiscal Policy & Welfare Economics" if not is_kannada else "ವಿತ್ತೀಯ ನೀತಿ ಮತ್ತು ಸಾರ್ವಜನಿಕ ಕಲ್ಯಾಣ ಅರ್ಥಶಾಸ್ತ್ರ"
            static = [
                "<b>Direct Benefit Transfer (DBT):</b> Uses Aadhaar-linked Jam trinity (Jan Dhan-Aadhaar-Mobile) to eliminate intermediary leakages in welfare delivery." if not is_kannada else "<b>ನೇರ ನಗದು ವರ್ಗಾವಣೆ (DBT):</b> ಮಧ್ಯವರ್ತಿಗಳ ಹಾವಳಿ ತಪ್ಪಿಸಲು ಜನ್ ಧನ್-ಆಧಾರ್-ಮೊಬೈಲ್ (JAM) ಮೂಲಕ ನೇರ ಸಹಾಯಧನ ವಿತರಣೆ.",
                "<b>FRBM Act 2003:</b> Mandates fiscal consolidation targets, revenue deficit reduction, and transparent state debt reporting." if not is_kannada else "<b>ಎಫ್‌ಆರ್‌ಬಿಎಂ ಕಾಯ್ದೆ 2003:</b> ವಿತ್ತೀಯ ಕೊರತೆ ನಿಯಂತ್ರಣ ಮತ್ತು ಸಾಲದ ಪ್ರಮಾಣ ಮಿತಿಗೊಳಿಸುವ ಶಾಸನಬದ್ಧ ಚೌಕಟ್ಟು.",
                "<b>Article 282:</b> Grants discretionary power to the Union or States to make grants for any public purpose." if not is_kannada else "<b>ವಿಧಿ 282:</b> ಸಾರ್ವಜನಿಕ ಕಲ್ಯಾಣ ಉದ್ದೇಶಗಳಿಗಾಗಿ ವಿಶೇಷ ಅನುದಾನ ನೀಡಲು ಕೇಂದ್ರ ಮತ್ತು ರಾಜ್ಯಗಳಿಗೆ ವಿವೇಚನಾಧಿಕಾರ."
            ]
            trap = "Revenue expenditure on unconditional cash transfers creates immediate consumption demand but does not generate capital assets." if not is_kannada else "ಷರತ್ತುರಹಿತ ನಗದು ವರ್ಗಾವಣೆಯ ಕಂದಾಯ ವೆಚ್ಚವು ತಕ್ಷಣದ ಬೇಡಿಕೆಯನ್ನು ಸೃಷ್ಟಿಸಿದರೂ, ದೀರ್ಘಕಾಲೀನ ಬಂಡವಾಳ ಆಸ್ತಿಗಳನ್ನು ಸೃಷ್ಟಿಸುವುದಿಲ್ಲ."
        else:
            subject = "Governance & Public Policy" if not is_kannada else "ಆಡಳಿತ ಮತ್ತು ಸಾರ್ವಜನಿಕ ನೀತಿ"
            static = [
                "<b>Article 14 & 21:</b> Equality before law and protection of life and personal liberty form the bedrock of governance." if not is_kannada else "<b>ವಿಧಿ 14 & 21:</b> ಕಾನೂನಿನ ಮುಂದೆ ಸಮಾನತೆ ಮತ್ತು ವ್ಯಕ್ತಿ ಸ್ವಾತಂತ್ರ್ಯದ ಸಾಂವಿಧಾನಿಕ ರಕ್ಷಣೆ.",
                "<b>Directive Principles (Part IV):</b> Direct state policy towards socio-economic welfare and equitable distribution." if not is_kannada else "<b>ರಾಜ್ಯ ನೀತಿ ನಿರ್ದೇಶಕ ತತ್ವಗಳು (ಭಾಗ IV):</b> ಸಾರ್ವಜನಿಕ ಕಲ್ಯಾಣ ಮತ್ತು ಆರ್ಥಿಕ ಸಮಾನತೆಯ ಗುರಿ.",
                "<b>Administrative Accountability:</b> Mechanisms for grievance redressal and civil service responsiveness." if not is_kannada else "<b>ಆಡಳಿತಾತ್ಮಕ ಹೊಣೆಗಾರಿಕೆ:</b> ನಾಗರಿಕ ಸೇವೆಗಳ ದಕ್ಷತೆ ಮತ್ತು ಸಾರ್ವಜನಿಕ ಕುಂದುಕೊರತೆಗಳ ನಿವಾರಣೆ."
            ]
            trap = "Directive Principles are fundamental in the governance of the country but are non-justiciable in court." if not is_kannada else "ರಾಜ್ಯ ನೀತಿ ನಿರ್ದೇಶಕ ತತ್ವಗಳು ದೇಶದ ಆಡಳಿತದಲ್ಲಿ ಮೂಲಭೂತವಾಗಿದ್ದರೂ, ನ್ಯಾಯಾಲಯಗಳ ಮೂಲಕ ಜಾರಿಗೊಳಿಸಲಾಗದು."

        in_news_text = summary[:240] if summary else f"Current news development reported in {subject}."
        return {
            "title": title if not is_kannada else f"{title[:75]}",
            "in_news": in_news_text,
            "static_framework": static,
            "pyq_link": f"Analytical Focus: '{subject} relevance in civil services examinations.'" if not is_kannada else f"ಪರಿಕಲ್ಪನಾ ವಿಶ್ಲೇಷಣೆ: '{subject} ಕುರಿತ ಪರೀಕ್ಷಾ ಮಹತ್ವ.'",
            "trap": trap
        }

    def _prajavani_fallback(self, title: str, summary: str, is_kannada: bool, source: str) -> Dict[str, Any]:
        """Rule-based fallback for Prajavani Karnataka cards"""
        card = self._rule_based_fallback(title, summary, is_kannada)
        return {
            "title": card["title"],
            "why_in_news": card["in_news"],
            "static_points": card["static_framework"],
            "exam_points": [
                "Core administrative linkage for KPSC KAS & State civil services." if not is_kannada else "ಕೆಪಿಎಸ್‌ಸಿ ಕೆಎಎಸ್ ಮತ್ತು ರಾಜ್ಯ ಪರೀಕ್ಷೆಗಳ ಪ್ರಮುಖ ಪಠ್ಯಕ್ರಮ ಅಂಶ.",
                "Focus on statutory bodies, appointments, and institutional mandates." if not is_kannada else "ಶಾಸನಬದ್ಧ ಸಂಸ್ಥೆಗಳು ಮತ್ತು ಅಧಿಕಾರ ವ್ಯಾಪ್ತಿಯ ಮೇಲಿನ ನಿಖರ ಮಾಹಿತಿ."
            ],
            "trap": card["trap"],
            "state_angle": "Directly relevant for Karnataka State Administration, local governance, and public delivery." if not is_kannada else "ಕರ್ನಾಟಕ ರಾಜ್ಯ ಆಡಳಿತ, ಸಾರ್ವಜನಿಕ ಸೇವಾ ವಿತರಣೆ ಮತ್ತು ಅಭಿವೃದ್ಧಿ ಯೋಜನೆಗಳಿಗೆ ನೇರ ಅನ್ವಯ.",
            "source": source
        }

    def _to_kannada_topic(self, topic: str) -> str:
        translations = {
            "Constitutional Safeguards & Law": "ಸಾಂವಿಧಾನಿಕ ರಕ್ಷಣೆಗಳು ಮತ್ತು ಕಾನೂನು",
            "Inter-State Water Dispute Adjudication": "ಅಂತರರಾಜ್ಯ ಜಲ ವಿವಾದಗಳ ಇತ್ಯರ್ಥ",
            "Internal Security & Anti-Terror Laws": "ಆಂತರಿಕ ಭದ್ರತೆ ಮತ್ತು ಭಯೋತ್ಪಾದನಾ ವಿರೋಧಿ ಕಾನೂನುಗಳು",
            "Electoral Reforms": "ಚುನಾವಣಾ ಸುಧಾರಣೆಗಳು",
            "Anti-Corruption & Administrative Ethics": "ಭ್ರಷ್ಟಾಚಾರ ವಿರೋಧಿ ಆಡಳಿತ ಮತ್ತು ನೈತಿಕತೆ"
        }
        return translations.get(topic, "ಪ್ರಮುಖ ಸಾಂವಿಧಾನಿಕ ವಿಷಯ")
