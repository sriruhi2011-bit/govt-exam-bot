# main.py

import json
import os
import sys
import time
import schedule
from datetime import datetime, date, timedelta

from news_scraper import NewsScraper
from news_filter import NewsFilter
from content_generator import ContentGenerator
from quiz_generator import QuizGenerator
from excel_saver import ExcelSaver
from telegram_poster import TelegramPoster, run_async
from extras import ExtraContent
from config.settings import (
    MORNING_NEWS_TIME, EVENING_QUIZ_TIME,
    FILTERED_NEWS_DIR, DATA_DIR
)
from config.logger import setup_logger

logger = setup_logger('main')

STATE_FILE = os.path.join(DATA_DIR, 'job_state.json')
IS_GITHUB = os.environ.get('GITHUB_ACTIONS') == 'true'


def is_done_today(job_name):
    if IS_GITHUB:
        return False
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
    if IS_GITHUB:
        return
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
    state[today][job_name] = datetime.now().strftime('%H:%M:%S')
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def morning_news_pipeline():
    if is_done_today('morning_news'):
        print('Morning news already done today! Skipping.')
        return

    start = datetime.now()
    print('')
    print('=' * 55)
    print(f'   MORNING NEWS PIPELINE - {start.strftime("%H:%M:%S")}')
    print('=' * 55)

    from config.settings import BOT_TOKEN, CHANNEL_ID, GEMINI_API_KEY, GROQ_API_KEY
    print(f'   Running on: {"GitHub Actions" if IS_GITHUB else "Local PC"}')
    bt = 'YES' if BOT_TOKEN and 'PASTE_' not in BOT_TOKEN and 'YOUR_' not in BOT_TOKEN else 'NO'
    gm = 'YES' if GEMINI_API_KEY and 'PASTE_' not in GEMINI_API_KEY and 'YOUR_' not in GEMINI_API_KEY else 'NO'
    gr = 'YES' if GROQ_API_KEY and 'PASTE_' not in GROQ_API_KEY and 'YOUR_' not in GROQ_API_KEY else 'NO'
    print(f'   BOT_TOKEN: {bt} | CHANNEL: {CHANNEL_ID} | GEMINI: {gm} | GROQ: {gr}')

    excel = ExcelSaver()

    try:
        print('\n>>> STEP 1: Scraping news...')
        scraper = NewsScraper()
        raw = scraper.fetch_all_news()
        print(f'   Got {len(raw)} articles')
        excel.save_scraped_news(raw)

        if not raw:
            print('   ERROR: No articles found!')
            return

        print('\n>>> STEP 2: AI Filtering...')
        filterer = NewsFilter()
        filtered, stats = filterer.filter_articles(raw)
        print(f'   Selected {len(filtered)} relevant articles')
        excel.save_filtered_news(filtered, stats)

        if not filtered:
            print('   WARNING: No relevant articles today!')
            return

        print('\n>>> STEP 3: Creating news posts...')
        generator = ContentGenerator()
        posts, post_data = generator.generate_all_posts(filtered)
        print(f'   Created {len(posts)} posts')
        excel.save_posts(post_data)

        print('\n>>> STEP 4: Posting news to Telegram...')
        if skip_telegram:
            print('   SKIPPING Telegram posting (will post separately at exact time)')
            # Save posts to file for later posting
            import json
            posts_to_save = []
            for p in posts:
                if isinstance(p, dict):
                    posts_to_save.append(p)
                # Skip string posts (header/footer)
            if posts_to_save:
                posts_file = os.path.join(DATA_DIR, 'pending_news_posts.json')
                with open(posts_file, 'w', encoding='utf-8') as f:
                    json.dump({'posts': posts_to_save}, f, ensure_ascii=False)
                print(f'   Saved {len(posts_to_save)} posts to pending_news_posts.json')
            excel.save_posting_log('Morning News', 'Processing Done', 'Will post at 7:00 AM')
        else:
            poster = TelegramPoster()
            ok, fail = run_async(poster.post_news(posts))
            print(f'   Results: {ok} sent, {fail} failed')
            excel.save_posting_log('Morning News', 'Success', f'Sent:{ok} Failed:{fail}')

        print('\n>>> STEP 5: Posting extra content...')
        if skip_telegram:
            print('   SKIPPING extra content (will post separately at exact time)')
        else:
            try:
                extra = ExtraContent()
                extra_posts = extra.get_todays_extras()
                print(f'   Generated {len(extra_posts)} extras for {extra.day_name}')
                for name, post_content in extra_posts:
                    print(f'   Posting: {name}...')
                    result = run_async(poster.send_text(post_content))
                    status = 'OK' if result else 'FAILED'
                    print(f'   {status}: {name}')
                    time.sleep(3)
                excel.save_posting_log('Extra Content', 'Success', f'{len(extra_posts)} extras')
            except Exception as e:
                print(f'   Extra content error (not critical): {e}')

        mark_done('morning_news')
        elapsed = (datetime.now() - start).total_seconds()
        print(f'\nDONE in {elapsed:.0f} seconds!')

    except Exception as e:
        print(f'\nERROR: {e}')
        import traceback
        traceback.print_exc()
        try:
            excel.save_posting_log('Morning News', 'Failed', str(e))
        except:
            pass


def evening_quiz_pipeline():
    if is_done_today('evening_quiz'):
        print('Evening quiz already done today! Skipping.')
        return

    start = datetime.now()
    print('')
    print('=' * 55)
    print(f'   EVENING QUIZ PIPELINE - {start.strftime("%H:%M:%S")}')
    print('=' * 55)

    from config.settings import BOT_TOKEN, CHANNEL_ID
    print(f'   Running on: {"GitHub Actions" if IS_GITHUB else "Local PC"}')
    bt = 'YES' if BOT_TOKEN and 'PASTE_' not in BOT_TOKEN and 'YOUR_' not in BOT_TOKEN else 'NO'
    print(f'   BOT_TOKEN: {bt} | CHANNEL: {CHANNEL_ID}')

    excel = ExcelSaver()
    today = datetime.now().strftime('%Y-%m-%d')

    try:
        print('\n>>> STEP 1: Loading filtered news...')
        filtered_file = os.path.join(FILTERED_NEWS_DIR, f'filtered_{today}.json')
        if not os.path.exists(filtered_file):
            print('   No filtered file. Running scrape+filter...')
            scraper = NewsScraper()
            raw = scraper.fetch_all_news()
            filterer = NewsFilter()
            filtered, stats = filterer.filter_articles(raw)
            excel.save_scraped_news(raw)
            excel.save_filtered_news(filtered, stats)
        else:
            with open(filtered_file, 'r', encoding='utf-8') as f:
                filtered = json.load(f)
        print(f'   Loaded {len(filtered)} articles')

        if not filtered:
            print('   WARNING: No articles for quiz!')
            return

        print('\n>>> STEP 2: Generating quiz questions...')
        quiz_gen = QuizGenerator()
        questions = quiz_gen.generate_daily_quiz(filtered)
        print(f'   Created {len(questions)} questions')
        excel.save_quiz(questions)

        if not questions:
            print('   WARNING: No questions generated!')
            return

        print('\n>>> STEP 3: Posting quiz to Telegram...')
        quiz_posts = quiz_gen.format_for_telegram(questions)
        poster = TelegramPoster()
        ok, fail = run_async(poster.post_quiz(quiz_posts))
        print(f'   Results: {ok} sent, {fail} failed')
        excel.save_posting_log('Evening Quiz', 'Success', f'Q:{len(questions)} Sent:{ok}')

        print('\n>>> STEP 4: Updating master database...')
        excel.update_master(filtered, questions)

        mark_done('evening_quiz')
        elapsed = (datetime.now() - start).total_seconds()
        print(f'\nDONE in {elapsed:.0f} seconds!')

    except Exception as e:
        print(f'\nERROR: {e}')
        import traceback
        traceback.print_exc()
        try:
            excel.save_posting_log('Evening Quiz', 'Failed', str(e))
        except:
            pass


def check_missed_jobs():
    now = datetime.now()
    hour = now.hour
    morning_hour = int(MORNING_NEWS_TIME.split(':')[0])
    evening_hour = int(EVENING_QUIZ_TIME.split(':')[0])
    print(f'Checking missed jobs (time: {now.strftime("%H:%M")})...')
    if hour >= morning_hour and not is_done_today('morning_news'):
        print('   Morning news MISSED - running now!')
        morning_news_pipeline()
    elif is_done_today('morning_news'):
        print('   Morning news: Done today')
    else:
        print(f'   Morning news: Scheduled at {MORNING_NEWS_TIME}')
    if hour >= evening_hour and not is_done_today('evening_quiz'):
        print('   Evening quiz MISSED - running now!')
        evening_quiz_pipeline()
    elif is_done_today('evening_quiz'):
        print('   Evening quiz: Done today')
    else:
        print(f'   Evening quiz: Scheduled at {EVENING_QUIZ_TIME}')


def start():
    print('')
    print('=' * 55)
    print('   GOVT EXAM NEWS BOT - ALL FEATURES')
    print('=' * 55)
    print(f'   News + Extras: {MORNING_NEWS_TIME}')
    print(f'   Quiz:          {EVENING_QUIZ_TIME}')
    print('=' * 55)
    check_missed_jobs()
    schedule.every().day.at(MORNING_NEWS_TIME).do(morning_news_pipeline)
    schedule.every().day.at(EVENING_QUIZ_TIME).do(evening_quiz_pipeline)
    print('\n   Running. Press Ctrl+C to stop.\n')
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else 'start'
    if command == 'test':
        print('FULL TEST...')
        morning_news_pipeline()
        print('\nMorning done! Quiz in 10 seconds...\n')
        time.sleep(10)
        evening_quiz_pipeline()
        print('\nCOMPLETE!')
    elif command == 'news':
        morning_news_pipeline()
    elif command == 'quiz':
        evening_quiz_pipeline()
    elif command == 'extras':
        print('Testing extra content only...')
        poster = TelegramPoster()
        extra = ExtraContent()
        extra_posts = extra.get_todays_extras()
        print(f'Generated {len(extra_posts)} posts')
        for name, content in extra_posts:
            print(f'Posting: {name}...')
            run_async(poster.send_text(content))
            time.sleep(3)
        print('Done!')
    elif command == 'start':
        start()
    elif command == 'status':
        today_str = str(date.today())
        print(f'\nStatus for {today_str}:')
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
            if today_str in state:
                for job, t in state[today_str].items():
                    print(f'   Done: {job} at {t}')
            else:
                print('   No jobs done today')
        else:
            print('   No history')
    elif command == 'reset':
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
            print('State reset!')
        else:
            print('No state file found.')
    elif command == 'post-news':
        # Post existing news to Telegram (for scheduled workflow)
        from config.settings import BOT_TOKEN, CHANNEL_ID
        import json
        from datetime import datetime
        from telegram_poster import TelegramPoster, run_async
        
        today = datetime.now().strftime('%Y-%m-%d')
        posts_file = os.path.join(DATA_DIR, 'pending_news_posts.json')
        
        if not os.path.exists(posts_file):
            print(f'ERROR: No pending posts file: {posts_file}')
        else:
            with open(posts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            posts = data.get('posts', [])
            
            poster = TelegramPoster()
            ok, fail = run_async(poster.post_news(posts))
            print(f'Posted: {ok} sent, {fail} failed')
    elif command == 'post-quiz':
        # Post existing quiz to Telegram (for scheduled workflow)
        from config.settings import BOT_TOKEN, CHANNEL_ID
        import json
        from datetime import datetime
        from quiz_generator import QuizGenerator
        from telegram_poster import TelegramPoster, run_async
        
        today = datetime.now().strftime('%Y-%m-%d')
        quiz_file = os.path.join(QUIZ_DIR, f'quiz_{today}.json')
        
        if not os.path.exists(quiz_file):
            print(f'ERROR: No quiz file for today: {quiz_file}')
        else:
            with open(quiz_file, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            
            quiz_gen = QuizGenerator()
            quiz_posts = quiz_gen.format_for_telegram(questions)
            poster = TelegramPoster()
            ok, fail = run_async(poster.post_quiz(quiz_posts))
            print(f'Posted: {ok} sent, {fail} failed')
    else:
        print('Usage: python main.py [test|news|quiz|extras|start|status|reset|post-news|post-quiz]')