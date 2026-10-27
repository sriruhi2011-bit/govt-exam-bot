# config/settings.py

import os

# ════════════════════════════════════════════════════
#  API KEYS
#  On your PC: uses the value after the comma
#  On GitHub: reads from secrets (environment variable)
#
#  REPLACE each PASTE_xxx with your REAL key!
# ════════════════════════════════════════════════════

# Load local keys from gitignored files if running on local PC
_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _fname in [".env", "my_keys.txt", "key.txt"]:
    _fpath = os.path.join(_base, _fname)
    if os.path.exists(_fpath):
        try:
            with open(_fpath, "r", encoding="utf-8") as _f:
                for _line in _f:
                    if "=" in _line:
                        _k, _v = _line.strip().split("=", 1)
                        _k, _v = _k.strip(), _v.strip().strip('"').strip("'")
                        if _k and _v and _k not in os.environ:
                            os.environ[_k] = _v
        except Exception:
            pass

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@kansiri_daily_updates")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_API_KEY_2 = os.environ.get("GEMINI_API_KEY_2", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# ════════════════════════════════════════════════════
#  KANNADA CHANNEL CONFIGURATION
# ════════════════════════════════════════════════════

KAN_BOT_TOKEN = os.environ.get("KAN_BOT_TOKEN", BOT_TOKEN)
KAN_CHANNEL_ID = os.environ.get("KAN_CHANNEL_ID", CHANNEL_ID)

# ════════════════════════════════════════════════════
#  WHATSAPP CHANNEL CONFIGURATION (Optional - Green API)
# ════════════════════════════════════════════════════

WHATSAPP_ENABLED = os.environ.get("WHATSAPP_ENABLED", "false").lower() == "true"
WHATSAPP_INSTANCE_ID = os.environ.get("WHATSAPP_INSTANCE_ID", "")
WHATSAPP_API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN", "")
WHATSAPP_CHAT_ID = os.environ.get("WHATSAPP_CHAT_ID", "")  # e.g., 120363xxx@newsletter or group ID

# ════════════════════════════════════════════════════
#  CONSTANTS - Magic numbers extracted to named constants
# ════════════════════════════════════════════════════

MIN_CONTENT_LENGTH = 30  # Minimum paragraph length to consider valid content
MIN_DUPLICATE_CHECK_LENGTH = 50  # Characters to use for duplicate detection
DEFAULT_TEMPERATURE = 0.2  # Default AI temperature
CONTENT_TRUNCATION_LENGTH = 1500  # Truncate content for AI prompts
AI_TIMEOUT_SECONDS = 60  # Timeout for AI API calls
REQUEST_DELAY_SECONDS = 0.5  # Delay between requests to same source
TELEGRAM_MESSAGE_SPLIT_LENGTH = 4000  # Max characters per Telegram message
TELEGRAM_DELAY_SECONDS = 0  # No delay between Telegram messages
MAX_RETRIES = 3  # Maximum retry attempts


# ════════════════════════════════════════════════════
#  ASPIRANT MASTER SCHEDULE (IST)
# ════════════════════════════════════════════════════

MORNING_KICKOFF_TIME = "06:30"     # Mindset, Targets, Inspiration
DAILY_DOSSIER_TIME = "08:30"       # 360° Issue Dossier (Syllabus deep dive)
PRELIMS_DRILL_TIME = "13:00"       # 3 High-Yield Interactive Quiz Polls
MAINS_CHALLENGE_TIME = "17:00"     # Mains Question + Blueprint + Keywords
CAPSULE_TIME = "19:30"             # Micro-learning Flashcard Capsule
MODEL_ANSWER_TIME = "20:30"        # Comprehensive Model Answer Drop
NIGHT_AUDIT_TIME = "21:30"         # Active Recall Check + Night Reflection

# Legacy schedule aliases for backwards compatibility
MORNING_GREETING_TIME = MORNING_KICKOFF_TIME
MORNING_NEWS_TIME = DAILY_DOSSIER_TIME
EVENING_QUIZ_TIME = MAINS_CHALLENGE_TIME
GOOD_NIGHT_TIME = NIGHT_AUDIT_TIME

# ════════════════════════════════════════════════════
#  LIMITS
# ════════════════════════════════════════════════════

MAX_ARTICLES_PER_SOURCE = 15
MAX_ARTICLE_CONTENT_LENGTH = 3000
MIN_IMPORTANCE_SCORE = 5
MAX_NEWS_POSTS = 20
MAX_NEWS_POSTS_PER_CATEGORY = 4  # used for per-category posting blocks
MAX_QUIZ_QUESTIONS = 10    # Reduced to 10 questions
MAX_QUIZ_ARTICLES_POOL_PER_CATEGORY = 2  # number of filtered articles per category to use for quiz generation
REQUEST_TIMEOUT = 15

# ════════════════════════════════════════════════════
#  FILE PATHS (automatic — don't change)
# ════════════════════════════════════════════════════

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_NEWS_DIR = os.path.join(DATA_DIR, "raw_news")
FILTERED_NEWS_DIR = os.path.join(DATA_DIR, "filtered_news")
QUIZ_DIR = os.path.join(DATA_DIR, "quizzes")
EXCEL_DIR = os.path.join(DATA_DIR, "excel_reports")
LOG_DIR = os.path.join(BASE_DIR, "logs")

for directory in [DATA_DIR, RAW_NEWS_DIR, FILTERED_NEWS_DIR,
                  QUIZ_DIR, EXCEL_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# ════════════════════════════════════════════════════
#  NEWS SOURCES
# ════════════════════════════════════════════════════

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
        
        # ── KARNATAKA PAPERS ──
    "Deccan Herald - Karnataka":
        "https://www.deccanherald.com/rss/karnataka.rss",
    "Deccan Herald - Bengaluru":
        "https://www.deccanherald.com/rss/bengaluru.rss",
    "Deccan Herald - National":
        "https://www.deccanherald.com/rss/national.rss",
    "Deccan Herald - Business":
        "https://www.deccanherald.com/rss/business.rss",
    "Deccan Herald - Science":
        "https://www.deccanherald.com/rss/science-and-environment.rss",
    "The Hindu - Karnataka":
        "https://www.thehindu.com/news/national/karnataka/feeder/default.rss",
    "Indian Express - Bangalore":
        "https://indianexpress.com/section/cities/bangalore/feed/",
    "Times of India - Bengaluru":
        "https://timesofindia.indiatimes.com/rssfeeds/4084533.cms",
    "The New Indian Express - Karnataka":
        "https://www.newindianexpress.com/rss/karnataka/rssfeed.xml",
    "Bangalore Mirror":
        "https://bangaloremirror.indiatimes.com/rssfeeds/4738792.cms",
}

# ════════════════════════════════════════════════════
#  KANNADA RSS FEEDS
# ════════════════════════════════════════════════════

KAN_RSS_FEEDS = {
    # Karnataka-focused (English but Karnataka news)
    "Deccan Herald Karnataka":
        "https://www.deccanherald.com/rss/karnataka.rss",
    "Deccan Herald Bengaluru":
        "https://www.deccanherald.com/rss/bengaluru.rss",
    "The Hindu Karnataka":
        "https://www.thehindu.com/news/national/karnataka/feeder/default.rss",
    "Indian Express Bangalore":
        "https://indianexpress.com/section/cities/bangalore/feed/",
    "Times of India Bengaluru":
        "https://timesofindia.indiatimes.com/rssfeeds/4084533.cms",
    "New Indian Express Karnataka":
        "https://www.newindianexpress.com/rss/karnataka/rssfeed.xml",
    "Bangalore Mirror":
        "https://bangaloremirror.indiatimes.com/rssfeeds/4738792.cms",
    # Kannada News Aggregators
    "Karnataka.com":
        "https://www.karnataka.com/feed/",
    "Suvarna News":
        "https://www.suvarnanews.tv/feed/",
    "Vijayavani":
        "https://vijayavani.com/feed",
    "Prajavani":
        "https://www.prajavani.net/rss/english",
    "OneIndia Kannada":
        "https://kannada.oneindia.in/rss/feed",
}

# Kannada specific directories
KAN_DATA_DIR = os.path.join(DATA_DIR, "kannada")
KAN_RAW_NEWS_DIR = os.path.join(KAN_DATA_DIR, "raw_news")
KAN_FILTERED_NEWS_DIR = os.path.join(KAN_DATA_DIR, "filtered_news")
KAN_QUIZ_DIR = os.path.join(KAN_DATA_DIR, "quizzes")

for directory in [KAN_DATA_DIR, KAN_RAW_NEWS_DIR, KAN_FILTERED_NEWS_DIR, KAN_QUIZ_DIR]:
    os.makedirs(directory, exist_ok=True)

# ════════════════════════════════════════════════════
#  EXAM SYLLABUS
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
    "Karnataka & State Affairs": [
        "karnataka", "bengaluru", "bangalore", "mysuru", "mysore",
        "hubli", "dharwad", "mangalore", "mangaluru", "belagavi",
        "belgaum", "gulbarga", "kalaburagi", "shimoga", "shivamogga",
        "davangere", "bellary", "ballari", "raichur", "bidar",
        "karwar", "udupi", "hassan", "mandya", "tumkur", "tumakuru",
        "kolar", "chikkaballapur", "ramanagara", "kodagu", "coorg",
        "BBMP", "BDA", "BMTC", "KSRTC", "namma metro",
        "siddaramaiah", "chief minister karnataka", "KAS", "KPSC",
        "karnataka high court", "vidhana soudha", "vidhan parishad",
        "karnataka budget", "cauvery", "kaveri", "krishna river",
        "tungabhadra", "western ghats karnataka", "bandipur",
        "nagarhole", "kabini", "BR hills", "hampi", "pattadakal",
        "aihole", "badami", "srirangapatna", "mysore palace",
        "karnataka assembly", "karnataka governor",
        "KPTCL", "BESCOM", "karnataka police",
        "state PSC", "karnataka exam", "FDA", "SDA",
        "kannada", "karnataka culture", "dasara", "ugadi"
    ],
}
