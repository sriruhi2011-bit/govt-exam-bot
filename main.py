# main.py

import json
import os
import time
import schedule
from datetime import datetime, date

from news_scraper import NewsScraper
from news_filter import NewsFilter
from content_generator import ContentGenerator
from quiz_generator import QuizGenerator
from excel_saver import ExcelSaver
from telegram_poster import TelegramPoster, run_async
from config.settings import (
    MORNING_NEWS_TIME, EVENING_QUIZ_TIME,
    FILTERED_NEWS_DIR, DATA_DIR
)
from config.logger import setup_logger

logger = setup_logger("main")

STATE_FILE = os.path.join(DATA_DIR, "job_state.json")


def is_done_today(job_name):
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
            today = str(date.today())
            return today in state and job_name in state[today]
    except:
        pass
    return False


def mark_done(job_name):
    state = {}
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
    except:
        pass

    today = str(date.today())
    if today not in state:
        state[today] = {}
    state[today][job_name] = datetime.now().strftime("%H:%M:%S")

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def morning_news_pipeline():
    if is_done_today("morning_news"):
        print("Morning news already done today! Skipping.")
        logger.info("Morning news already done today! Skipping.")
        return

    start = datetime.now()
    print("")
    print("=" * 55)
    print(f"   MORNING NEWS PIPELINE — {start.strftime('%H:%M:%S')}")
    print("=" * 55)
    logger.info("=" * 55)
    logger.info(f"MORNING NEWS PIPELINE STARTED — {start}")
    logger.info("=" * 55)

    excel = ExcelSaver()

    try:
        # STEP 1: Scrape
        print("\n📥 STEP 1: Scraping news from all sources...")
        logger.info("STEP 1: Scraping news...")
        scraper = NewsScraper()
        raw = scraper.fetch_all_news()
        print(f"   Got {len(raw)} articles")
        excel.save_scraped_news(raw)

        if not raw:
            print("   ERROR: No articles found! Stopping.")
            logger.error("No articles found!")
            return

        # STEP 2: Filter
        print("\n🤖 STEP 2: AI Filtering (this takes a few minutes)...")
        logger.info("STEP 2: AI Filtering...")
        filterer = NewsFilter()
        filtered, stats = filterer.filter_articles(raw)
        print(f"   Selected {len(filtered)} relevant articles")
        excel.save_filtered_news(filtered, stats)

        if not filtered:
            print("   WARNING: No relevant articles found today!")
            logger.warning("No relevant articles today!")
            return

        # STEP 3: Generate posts
        print("\n✍️ STEP 3: Writing news summaries...")
        logger.info("STEP 3: Generating summaries...")
        generator = ContentGenerator()
        posts, post_data = generator.generate_all_posts(filtered)
        excel.save_posts(post_data)

        # STEP 4: Post to Telegram
        print("\n📤 STEP 4: Posting to Telegram channel...")
        logger.info("STEP 4: Posting to Telegram...")
        poster = TelegramPoster()
        ok, fail = run_async(poster.post_news(posts))
        excel.save_posting_log("Morning News", "Success", f"Sent:{ok} Failed:{fail}")

        mark_done("morning_news")

        elapsed = (datetime.now() - start).total_seconds()
        print(f"\n✅ MORNING PIPELINE COMPLETE in {elapsed:.0f} seconds!")
        print(f"   {len(raw)} scraped → {len(filtered)} selected → {ok} posted")
        logger.info(f"DONE in {elapsed:.0f} seconds")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.error(f"MORNING PIPELINE ERROR: {e}", exc_info=True)
        try:
            excel.save_posting_log("Morning News", "Failed", str(e))
        except:
            pass


def evening_quiz_pipeline():
    if is_done_today("evening_quiz"):
        print("Evening quiz already done today! Skipping.")
        logger.info("Evening quiz already done today! Skipping.")
        return

    start = datetime.now()
    print("")
    print("=" * 55)
    print(f"   EVENING QUIZ PIPELINE — {start.strftime('%H:%M:%S')}")
    print("=" * 55)
    logger.info("=" * 55)
    logger.info(f"EVENING QUIZ PIPELINE STARTED — {start}")
    logger.info("=" * 55)

    excel = ExcelSaver()
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        # STEP 1: Load filtered news
        print("\n📂 STEP 1: Loading today's filtered news...")
        filtered_file = os.path.join(
            FILTERED_NEWS_DIR, f"filtered_{today}.json"
        )

        if not os.path.exists(filtered_file):
            print("   No filtered file found. Running scrape+filter first...")
            logger.warning("No filtered file. Running scrape+filter...")
            scraper = NewsScraper()
            raw = scraper.fetch_all_news()
            filterer = NewsFilter()
            filtered, stats = filterer.filter_articles(raw)
            excel.save_scraped_news(raw)
            excel.save_filtered_news(filtered, stats)
        else:
            with open(filtered_file, 'r', encoding='utf-8') as f:
                filtered = json.load(f)

        print(f"   Loaded {len(filtered)} articles")

        if not filtered:
            print("   WARNING: No articles available for quiz!")
            return

        # STEP 2: Generate quiz
        print("\n🧠 STEP 2: Generating quiz questions...")
        logger.info("STEP 2: Generating quiz...")
        quiz_gen = QuizGenerator()
        questions = quiz_gen.generate_daily_quiz(filtered)
        print(f"   Created {len(questions)} questions")
        excel.save_quiz(questions)

        if not questions:
            print("   WARNING: No questions generated!")
            return

        # STEP 3: Post to Telegram
        print("\n📤 STEP 3: Posting quiz to Telegram...")
        logger.info("STEP 3: Posting quiz...")
        quiz_posts = quiz_gen.format_for_telegram(questions)
        poster = TelegramPoster()
        ok, fail = run_async(poster.post_quiz(quiz_posts))
        excel.save_posting_log("Evening Quiz", "Success", f"Q:{len(questions)} Sent:{ok}")

        # STEP 4: Update master database
        print("\n💾 STEP 4: Updating master database...")
        logger.info("STEP 4: Updating master DB...")
        excel.update_master(filtered, questions)

        mark_done("evening_quiz")

        elapsed = (datetime.now() - start).total_seconds()
        print(f"\n✅ EVENING QUIZ COMPLETE in {elapsed:.0f} seconds!")
        print(f"   {len(questions)} questions posted")
        logger.info(f"DONE in {elapsed:.0f} seconds")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.error(f"EVENING PIPELINE ERROR: {e}", exc_info=True)
        try:
            excel.save_posting_log("Evening Quiz", "Failed", str(e))
        except:
            pass


def check_missed_jobs():
    now = datetime.now()
    hour = now.hour

    morning_hour = int(MORNING_NEWS_TIME.split(":")[0])
    evening_hour = int(EVENING_QUIZ_TIME.split(":")[0])

    print(f"🔍 Checking for missed jobs (time: {now.strftime('%H:%M')})...")

    if hour >= morning_hour and not is_done_today("morning_news"):
        print("   Morning news was MISSED — running now!")
        morning_news_pipeline()
    elif is_done_today("morning_news"):
        print("   Morning news: Already done today ✅")
    else:
        print(f"   Morning news: Scheduled at {MORNING_NEWS_TIME}")

    if hour >= evening_hour and not is_done_today("evening_quiz"):
        print("   Evening quiz was MISSED — running now!")
        evening_quiz_pipeline()
    elif is_done_today("evening_quiz"):
        print("   Evening quiz: Already done today ✅")
    else:
        print(f"   Evening quiz: Scheduled at {EVENING_QUIZ_TIME}")


def start():
    print("")
    print("🚀" + "=" * 53)
    print("   GOVT EXAM NEWS BOT — STARTED")
    print("=" * 55)
    print(f"   📰 Morning News:  {MORNING_NEWS_TIME}")
    print(f"   🧠 Evening Quiz:  {EVENING_QUIZ_TIME}")
    print(f"   🔄 Missed jobs:   Auto-recovery ON")
    print("=" * 55)
    print("")

    check_missed_jobs()

    schedule.every().day.at(MORNING_NEWS_TIME).do(morning_news_pipeline)
    schedule.every().day.at(EVENING_QUIZ_TIME).do(evening_quiz_pipeline)

    print("\n   ✅ Running. Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    import sys

    command = sys.argv[1] if len(sys.argv) > 1 else "start"

    if command == "test":
        print("🧪 RUNNING FULL TEST...")
        print("This will take 20-40 minutes.")
        print("It will scrape news, filter, post, and make quiz.")
        print("")
        morning_news_pipeline()
        print("")
        print("=" * 55)
        print("Morning done! Starting quiz in 10 seconds...")
        print("=" * 55)
        print("")
        time.sleep(10)
        evening_quiz_pipeline()
        print("")
        print("🧪 FULL TEST COMPLETE!")

    elif command == "news":
        morning_news_pipeline()

    elif command == "quiz":
        evening_quiz_pipeline()

    elif command == "start":
        start()

    elif command == "status":
        today_str = str(date.today())
        print(f"\n📊 Status for {today_str}:")
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
            if today_str in state:
                for job, t in state[today_str].items():
                    print(f"   ✅ {job}: Completed at {t}")
            else:
                print("   No jobs completed yet today")
        else:
            print("   No job history found")
        print("")

    else:
        print("Usage: python main.py [command]")
        print("")
        print("Commands:")
        print("  test   — Run everything once right now")
        print("  news   — Run only news pipeline")
        print("  quiz   — Run only quiz pipeline")
        print("  start  — Start scheduler (keeps running)")
        print("  status — Check today's job status")