# config/settings.py
# THIS IS THE CONTROL PANEL — All settings in one place

import os
from datetime import datetime

# ════════════════════════════════════════════════════
#  STEP A: PASTE YOUR KEYS HERE (from my_keys.txt)
# ════════════════════════════════════════════════════

BOT_TOKEN = "8408260750:AAEAspZEIQm84Y5rwcWYyX0mHi830NVIfPI"
# Example: "7123456789:AAHf-xxxxxxxxxxxxxxxxxxxxxxxxxxx"
# ↑ Replace with YOUR token from @BotFather

CHANNEL_ID = "@kansiri_daily_updates"
# Example: "@daily_ca_upsc_2025"
# ↑ Replace with YOUR channel username (keep the @)

GROQ_API_KEY = "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"
# Example: "gsk_abc123def456ghi789jklmnop..."
# ↑ Replace with YOUR key from console.groq.com

# ════════════════════════════════════════════════════
#  STEP B: AI SETTINGS (no changes needed)
# ════════════════════════════════════════════════════

AI_BACKEND = "groq"
GROQ_MODEL = "llama-3.1-8b-instant"

# ════════════════════════════════════════════════════
#  STEP C: SCHEDULE — When to post (change if you want)
# ════════════════════════════════════════════════════

MORNING_NEWS_TIME = "07:00"    # 7:00 AM — News posting
EVENING_QUIZ_TIME = "19:00"    # 7:00 PM — Quiz posting

# ════════════════════════════════════════════════════
#  STEP D: LIMITS (no changes needed)
# ════════════════════════════════════════════════════

MAX_ARTICLES_PER_SOURCE = 15
MAX_ARTICLE_CONTENT_LENGTH = 3000
MIN_IMPORTANCE_SCORE = 5
MAX_NEWS_POSTS = 20
MAX_QUIZ_QUESTIONS = 15
REQUEST_TIMEOUT = 15

# ════════════════════════════════════════════════════
#  STEP E: FILE PATHS (automatic — don't change)
# ════════════════════════════════════════════════════

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_NEWS_DIR = os.path.join(DATA_DIR, "raw_news")
FILTERED_NEWS_DIR = os.path.join(DATA_DIR, "filtered_news")
QUIZ_DIR = os.path.join(DATA_DIR, "quizzes")
EXCEL_DIR = os.path.join(DATA_DIR, "excel_reports")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Create folders if they don't exist
for directory in [DATA_DIR, RAW_NEWS_DIR, FILTERED_NEWS_DIR,
                  QUIZ_DIR, EXCEL_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# ════════════════════════════════════════════════════
#  STEP F: NEWS SOURCES (RSS feeds of newspapers)
# ════════════════════════════════════════════════════
#
#  RSS feed = A special link that gives news in a
#  format computers can easily read.
#  Every major newspaper provides this for free.

RSS_FEEDS = {
    "The Hindu - National":
        "https://www.thehindu.com/news/national/feeder/default.rss",
    "The Hindu - International":
        "https://www.thehindu.com/news/international/feeder/default.rss",
    "The Hindu - Economy":
        "https://www.thehindu.com/business/Economy/feeder/default.rss",
    "The Hindu - Science":
        "https://www.thehindu.com/sci-tech/science/feeder/default.rss",
    "The Hindu - Environment":
        "https://www.thehindu.com/sci-tech/energy-and-environment/feeder/default.rss",
    "Indian Express - India":
        "https://indianexpress.com/section/india/feed/",
    "Indian Express - Economy":
        "https://indianexpress.com/section/business/economy/feed/",
    "PIB India":
        "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3",
    "Down To Earth":
        "https://www.downtoearth.org.in/rss",
    "Livemint Economy":
        "https://www.livemint.com/rss/economy",
    "Times of India":
        "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
}

# ════════════════════════════════════════════════════
#  STEP G: EXAM SYLLABUS — Topics to filter for
# ════════════════════════════════════════════════════

SYLLABUS_CATEGORIES = {
    "Polity & Governance": [
        "constitution", "parliament", "supreme court", "high court",
        "election commission", "CAG", "governor", "president",
        "fundamental rights", "amendment", "bill", "act",
        "lok sabha", "rajya sabha", "judiciary", "tribunal",
        "RTI", "panchayati raj", "ordinance", "speaker"
    ],
    "Economy": [
        "GDP", "inflation", "RBI", "monetary policy", "fiscal policy",
        "budget", "tax", "GST", "SEBI", "FDI", "banking", "NABARD",
        "unemployment", "poverty", "subsidy", "repo rate", "CRR",
        "NITI Aayog", "fiscal deficit", "current account", "rupee",
        "UPI", "digital rupee", "disinvestment"
    ],
    "International Relations": [
        "UN", "G20", "G7", "BRICS", "QUAD", "NATO", "ASEAN",
        "bilateral", "treaty", "summit", "diplomacy", "sanctions",
        "WHO", "WTO", "IMF", "World Bank", "UNESCO", "SCO"
    ],
    "Science & Technology": [
        "ISRO", "NASA", "satellite", "space", "AI", "quantum",
        "5G", "biotechnology", "genome", "CRISPR", "nuclear",
        "semiconductor", "supercomputer", "cybersecurity", "drone",
        "solar", "hydrogen", "chandrayaan", "gaganyaan", "vaccine"
    ],
    "Environment & Ecology": [
        "climate change", "COP", "biodiversity", "pollution",
        "wildlife", "endangered", "national park", "tiger reserve",
        "wetland", "ramsar", "carbon", "emission", "paris agreement",
        "net zero", "ozone", "forest", "coral reef", "mangrove"
    ],
    "Social Issues": [
        "education", "health", "poverty", "women empowerment",
        "child labor", "malnutrition", "sanitation", "tribal",
        "reservation", "population", "census", "migration",
        "urbanization", "NEP", "smart city"
    ],
    "Geography": [
        "earthquake", "cyclone", "flood", "drought", "monsoon",
        "volcano", "tsunami", "glacier", "river", "el nino",
        "la nina", "landslide", "plate tectonics"
    ],
    "Government Schemes": [
        "PM", "scheme", "yojana", "mission", "ayushman", "mudra",
        "jan dhan", "swachh", "digital india", "make in india",
        "startup india", "skill india", "ujjwala", "awas yojana",
        "jal jeevan", "kisan"
    ],
    "Defense & Security": [
        "army", "navy", "air force", "missile", "defense",
        "military exercise", "DRDO", "HAL", "INS", "BSF",
        "border", "terrorism", "submarine", "nuclear"
    ],
    "Awards & Appointments": [
        "nobel", "bharat ratna", "padma", "award", "appointed",
        "chief justice", "governor", "ambassador", "dronacharya",
        "arjuna award"
    ],
}