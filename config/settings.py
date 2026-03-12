# config/settings.py

import os

# ════════════════════════════════════════════════════
#  API KEYS
#  On your PC: uses the value after the comma
#  On GitHub: reads from secrets (environment variable)
#
#  REPLACE each PASTE_xxx with your REAL key!
# ════════════════════════════════════════════════════

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
# Example: "7123456789:AAHf-xxxxxxxxxxxxxxxxxxxxxxx"

CHANNEL_ID = os.environ.get("CHANNEL_ID", "")
# Example: "@daily_ca_upsc_2025"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
# Example: "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
# Example: "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

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
TELEGRAM_DELAY_SECONDS = 3  # Delay between Telegram messages (increased to avoid flood control)
MAX_RETRIES = 3  # Maximum retry attempts

# ════════════════════════════════════════════════════
#  SCHEDULE
# ════════════════════════════════════════════════════

MORNING_NEWS_TIME = "07:00"
EVENING_QUIZ_TIME = "18:00"

# ════════════════════════════════════════════════════
#  LIMITS
# ════════════════════════════════════════════════════

MAX_ARTICLES_PER_SOURCE = 15
MAX_ARTICLE_CONTENT_LENGTH = 3000
MIN_IMPORTANCE_SCORE = 5
MAX_NEWS_POSTS = 20
MAX_QUIZ_QUESTIONS = 15
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