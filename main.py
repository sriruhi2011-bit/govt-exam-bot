# main.py
"""
Master Orchestrator for Aspirant Master Bot.
Replaces the noisy raw news pipeline with a comprehensive, professional
Civil Services & State PSC (UPSC / KPSC KAS) daily learning engine.

Schedule (IST):
06:30 AM - Morning Kickoff & Focus Targets
08:30 AM - Daily 360° Issue Dossier
01:00 PM - Prelims & Objective MCQ Drill (Interactive Telegram Polls)
09:30 PM - Night Revision Audit & Rest
"""

import json
import os
import sys
import time
import schedule
from datetime import datetime, timedelta, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from dossier_generator import DossierGenerator
from mains_engine import MainsEngine
from prelims_drill import PrelimsDrillEngine
from capsule_engine import CapsuleEngine
from habit_tracker import HabitTracker
from curriculum_bank import get_daily_module
from telegram_poster import TelegramPoster, run_async
from whatsapp_poster import WhatsAppPoster
from config.settings import (
    DATA_DIR,
    MORNING_KICKOFF_TIME,
    DAILY_DOSSIER_TIME,
    PRELIMS_DRILL_TIME,
    NEWSPAPER_PREP_TIME,
    NEWSPAPER_BROADCAST_TIME,
    NIGHT_AUDIT_TIME,
    KAN_CHANNEL_ID,
    CHANNEL_ID
)
from config.logger import setup_logger

logger = setup_logger('main')

STATE_FILE = os.path.join(DATA_DIR, 'job_state.json')
IS_GITHUB = os.environ.get('GITHUB_ACTIONS') == 'true'
ist_offset = timezone(timedelta(hours=5, minutes=30))


def get_ist_date():
    return datetime.now(ist_offset).strftime('%Y-%m-%d')


def get_local_time_for_ist(ist_time_str):
    try:
        hour, minute = map(int, ist_time_str.split(':'))
        now_ist = datetime.now(ist_offset)
        target_ist = now_ist.replace(hour=hour, minute=minute, second=0, microsecond=0)
        target_local = target_ist.astimezone()
        return target_local.strftime("%H:%M")
    except Exception as e:
        logger.error(f"Error converting IST time {ist_time_str} to local: {e}")
        return ist_time_str


def is_done_today(job_name):
    if IS_GITHUB:
        return False
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
            today = get_ist_date()
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
    today = get_ist_date()
    if today not in state:
        state[today] = {}
    state[today][job_name] = datetime.now(ist_offset).strftime('%H:%M:%S')
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


# ════════════════════════════════════════════════════
#  PIPELINE JOBS
# ════════════════════════════════════════════════════

def job_morning_kickoff():
    """06:30 AM - Morning Motivation, Target Setting & Mindset"""
    if is_done_today('morning_kickoff'):
        print('Morning kickoff already done today! Skipping.')
        return

    print("\n" + "=" * 55)
    print("   🌅 06:30 AM PIPELINE: MORNING KICKOFF")
    print("=" * 55)

    tracker = HabitTracker()
    poster = TelegramPoster()
    wa = WhatsAppPoster()
    module = get_daily_module()

    # Generate English and Kannada Kickoffs
    en_msg = tracker.generate_morning_kickoff(module, is_kannada=False)
    kn_msg = tracker.generate_morning_kickoff(module, is_kannada=True)

    # Post to primary channel
    print("   Posting English Kickoff to Telegram...")
    run_async(poster.send_text(en_msg, target_channel=CHANNEL_ID))

    # If Kannada channel is distinct, post Kannada version
    if KAN_CHANNEL_ID and KAN_CHANNEL_ID != CHANNEL_ID:
        print("   Posting Kannada Kickoff to KanSiri channel...")
        run_async(poster.send_text(kn_msg, target_channel=KAN_CHANNEL_ID))

    if wa.is_enabled:
        print("   Broadcasting Morning Kickoff to WhatsApp...")
        wa.send_text(en_msg)

    mark_done('morning_kickoff')
    print("   DONE: Morning kickoff posted successfully!")


def job_daily_dossier():
    """08:30 AM - Daily 360° Issue Dossier (Syllabus Deep Dive)"""
    if is_done_today('daily_dossier'):
        print('Daily dossier already done today! Skipping.')
        return

    print("\n" + "=" * 55)
    print("   📑 08:30 AM PIPELINE: DAILY 360° ISSUE DOSSIER")
    print("=" * 55)

    dossier_gen = DossierGenerator()
    poster = TelegramPoster()
    wa = WhatsAppPoster()
    module = get_daily_module()

    en_dossier = dossier_gen.generate_english_dossier(module)
    kn_dossier = dossier_gen.generate_kannada_dossier(module)

    print(f"   Posting 360° Dossier: {module['title']}...")
    run_async(poster.send_text(en_dossier, target_channel=CHANNEL_ID))

    if KAN_CHANNEL_ID and KAN_CHANNEL_ID != CHANNEL_ID:
        print("   Posting Kannada Dossier to KanSiri channel...")
        run_async(poster.send_text(kn_dossier, target_channel=KAN_CHANNEL_ID))

    if wa.is_enabled:
        print("   Broadcasting Daily Dossier to WhatsApp...")
        wa.send_text(en_dossier)

    mark_done('daily_dossier')
    print("   DONE: Daily 360° Dossier posted successfully!")


def job_prelims_drill():
    """01:00 PM - Prelims & Objective MCQ Drill (Interactive Bilingual Telegram Polls)"""
    if is_done_today('prelims_drill'):
        print('Prelims drill already done today! Skipping.')
        return

    print("\n" + "=" * 55)
    print("   🎯 01:00 PM PIPELINE: PRELIMS & OBJECTIVE DRILL")
    print("=" * 55)

    drill = PrelimsDrillEngine()
    poster = TelegramPoster()
    wa = WhatsAppPoster()
    module = get_daily_module()

    intro_text = drill.generate_drill_intro(module, is_bilingual=True)
    polls = drill.get_poll_items(module, is_bilingual=True)

    print("   Posting Bilingual Drill Intro...")
    run_async(poster.send_text(intro_text, target_channel=CHANNEL_ID))

    print(f"   Posting {len(polls)} interactive Bilingual Quiz Polls...")
    run_async(poster.send_poll_series(polls, target_channel=CHANNEL_ID))

    if KAN_CHANNEL_ID and KAN_CHANNEL_ID != CHANNEL_ID:
        print("   Posting Bilingual Drill to Kannada channel...")
        run_async(poster.send_text(intro_text, target_channel=KAN_CHANNEL_ID))
        run_async(poster.send_poll_series(polls, target_channel=KAN_CHANNEL_ID))

    if wa.is_enabled:
        print("   Broadcasting Prelims Drill to WhatsApp...")
        wa.send_text(intro_text)
        for p in polls:
            wa.send_quiz_poll(p)

    mark_done('prelims_drill')
    print("   DONE: Prelims Drill posted successfully!")


def job_mains_challenge():
    """05:00 PM - Daily Mains Answer Writing Challenge"""
    if is_done_today('mains_challenge'):
        print('Mains challenge already done today! Skipping.')
        return

    print("\n" + "=" * 55)
    print("   ✍️ 05:00 PM PIPELINE: DAILY MAINS CHALLENGE")
    print("=" * 55)

    mains = MainsEngine()
    poster = TelegramPoster()
    wa = WhatsAppPoster()
    module = get_daily_module()

    en_q = mains.generate_question_drop(module, is_kannada=False)
    kn_q = mains.generate_question_drop(module, is_kannada=True)

    print("   Posting Mains Question & Blueprint...")
    run_async(poster.send_text(en_q, target_channel=CHANNEL_ID))

    if KAN_CHANNEL_ID and KAN_CHANNEL_ID != CHANNEL_ID:
        print("   Posting Kannada Mains Question...")
        run_async(poster.send_text(kn_q, target_channel=KAN_CHANNEL_ID))

    if wa.is_enabled:
        print("   Broadcasting Mains Challenge to WhatsApp...")
        wa.send_text(en_q)

    mark_done('mains_challenge')
    print("   DONE: Daily Mains Challenge posted successfully!")


def job_capsule():
    """07:30 PM - High-Yield Micro Learning Capsule"""
    if is_done_today('capsule'):
        print('Capsule already done today! Skipping.')
        return

    print("\n" + "=" * 55)
    print("   💡 07:30 PM PIPELINE: HIGH-YIELD CAPSULE")
    print("=" * 55)

    capsule_gen = CapsuleEngine()
    poster = TelegramPoster()
    wa = WhatsAppPoster()
    module = get_daily_module()

    en_cap = capsule_gen.generate_capsule(module, is_kannada=False)
    kn_cap = capsule_gen.generate_capsule(module, is_kannada=True)

    print("   Posting Revision Capsule...")
    run_async(poster.send_text(en_cap, target_channel=CHANNEL_ID))

    if KAN_CHANNEL_ID and KAN_CHANNEL_ID != CHANNEL_ID:
        print("   Posting Kannada Revision Capsule...")
        run_async(poster.send_text(kn_cap, target_channel=KAN_CHANNEL_ID))

    if wa.is_enabled:
        print("   Broadcasting Capsule to WhatsApp...")
        wa.send_text(en_cap)

    mark_done('capsule')
    print("   DONE: High-Yield Capsule posted successfully!")


def job_model_answer():
    """08:30 PM - Official Model Answer Drop"""
    if is_done_today('model_answer'):
        print('Model answer already done today! Skipping.')
        return

    print("\n" + "=" * 55)
    print("   📑 08:30 PM PIPELINE: OFFICIAL MODEL ANSWER DROP")
    print("=" * 55)

    mains = MainsEngine()
    poster = TelegramPoster()
    wa = WhatsAppPoster()
    module = get_daily_module()

    en_ans = mains.generate_model_answer_drop(module, is_kannada=False)
    kn_ans = mains.generate_model_answer_drop(module, is_kannada=True)

    print("   Posting Model Answer...")
    run_async(poster.send_text(en_ans, target_channel=CHANNEL_ID))

    if KAN_CHANNEL_ID and KAN_CHANNEL_ID != CHANNEL_ID:
        print("   Posting Kannada Model Answer...")
        run_async(poster.send_text(kn_ans, target_channel=KAN_CHANNEL_ID))

    if wa.is_enabled:
        print("   Broadcasting Model Answer to WhatsApp...")
        wa.send_text(en_ans)

    mark_done('model_answer')
    print("   DONE: Official Model Answer posted successfully!")


def job_night_audit():
    """09:30 PM - Night Revision Audit & Rest"""
    if is_done_today('night_audit'):
        print('Night audit already done today! Skipping.')
        return

    print("\n" + "=" * 55)
    print("   🌙 09:30 PM PIPELINE: NIGHT REVISION AUDIT")
    print("=" * 55)

    tracker = HabitTracker()
    poster = TelegramPoster()
    wa = WhatsAppPoster()
    module = get_daily_module()

    en_night = tracker.generate_night_audit(module, is_kannada=False)
    kn_night = tracker.generate_night_audit(module, is_kannada=True)

    print("   Posting Night Audit...")
    run_async(poster.send_text(en_night, target_channel=CHANNEL_ID))

    if KAN_CHANNEL_ID and KAN_CHANNEL_ID != CHANNEL_ID:
        print("   Posting Kannada Night Audit...")
        run_async(poster.send_text(kn_night, target_channel=KAN_CHANNEL_ID))

    if wa.is_enabled:
        print("   Broadcasting Night Audit to WhatsApp...")
        wa.send_text(en_night)

    mark_done('night_audit')
    print("   DONE: Night Audit posted successfully!")


def job_publish_study_pdf(lang='both'):
    """Generate and broadcast daily high-yield Study Material PDF to channels"""
    from generate_study_material import get_demo_english_data, get_demo_kannada_data
    from pdf_engine import PDFEngine
    poster = TelegramPoster()
    wa = WhatsAppPoster()
    engine = PDFEngine()

    print("\n" + "=" * 55)
    print("   📑 PUBLISHING HIGH-YIELD STUDY MATERIAL PDF")
    print("=" * 55)

    if lang in ['both', 'en', 'english']:
        print("   Generating English 'The Civils Vault' PDF...")
        en_data = get_demo_english_data()
        en_pdf = engine.generate_english_pdf(en_data)
        caption = "📚 <b>Daily Prelims & Mains Analysis PDF</b>\nComprehensive current affairs with static depth & practice MCQs."
        run_async(poster.send_document(en_pdf, caption=caption, target_channel=CHANNEL_ID))
        if wa.is_enabled:
            wa.send_document(en_pdf, caption="📚 *Daily Prelims & Mains Analysis PDF*")

    if lang in ['both', 'kn', 'kannada']:
        print("   Generating Kannada 'KPSCinsights' PDF...")
        kn_data = get_demo_kannada_data()
        kn_pdf = engine.generate_kannada_pdf(kn_data)
        kn_caption = "📚 <b>ದೈನಂದಿನ ಪರೀಕ್ಷಾ ಮಾರ್ಗದರ್ಶಿ PDF</b>\nಪ್ರಜಾವಾಣಿ & ಡೆಕ್ಕನ್ ಹೆರಾಲ್ಡ್ ಸಮಗ್ರ ಪರೀಕ್ಷಾ ವಿಶ್ಲೇಷಣೆ."
        target_kn = KAN_CHANNEL_ID if (KAN_CHANNEL_ID and KAN_CHANNEL_ID != CHANNEL_ID) else CHANNEL_ID
        run_async(poster.send_document(kn_pdf, caption=kn_caption, target_channel=target_kn))
        if wa.is_enabled:
            wa.send_document(kn_pdf, caption="📚 *ದೈನಂದಿನ ಪ್ರಜಾವಾಣಿ ಪರೀಕ್ಷಾ ವಿಶ್ಲೇಷಣೆ PDF*")

    print("   DONE: Study Material PDF generated and posted successfully!")


def job_newspaper_prep():
    """17:15 IST (Before 5:30 PM) - Generate The Hindu & Prajavani PDFs and send to admin for approval"""
    from approval_manager import ApprovalManager
    mgr = ApprovalManager()
    mgr.prepare_and_send_for_approval()


def job_newspaper_broadcast():
    """18:35 IST (6:35 PM) - Broadcast confirmed PDFs to public channels"""
    from approval_manager import ApprovalManager
    mgr = ApprovalManager()
    mgr.broadcast_at_635pm()


# ════════════════════════════════════════════════════
#  SCHEDULING & AUTOMATION
# ════════════════════════════════════════════════════

def check_missed_jobs(quiet=False):
    now = datetime.now(ist_offset)
    current_minutes = now.hour * 60 + now.minute

    jobs = [
        ("morning_kickoff", MORNING_KICKOFF_TIME, job_morning_kickoff),
        ("daily_dossier", DAILY_DOSSIER_TIME, job_daily_dossier),
        ("prelims_drill", PRELIMS_DRILL_TIME, job_prelims_drill),
        ("newspaper_prep", NEWSPAPER_PREP_TIME, job_newspaper_prep),
        ("newspaper_broadcast", NEWSPAPER_BROADCAST_TIME, job_newspaper_broadcast),
        ("night_audit", NIGHT_AUDIT_TIME, job_night_audit),
    ]

    for name, time_str, func in jobs:
        h, m = map(int, time_str.split(':'))
        target_mins = h * 60 + m
        if current_minutes >= target_mins and not is_done_today(name):
            if not quiet:
                print(f"   Job '{name}' scheduled at {time_str} was missed - running now!")
            func()


def job_exam_notifications():
    try:
        from exam_notification_monitor import ExamNotificationMonitor
        ExamNotificationMonitor().scan_and_process()
    except Exception as e:
        logger.error(f"Exam notification scan error: {e}")


def start():
    print("\n" + "=" * 60)
    print("   ASPIRANT MASTER ENGINE - 24/7 SCHEDULER ACTIVE")
    print("=" * 60)
    print(f"   Morning Kickoff:          {MORNING_KICKOFF_TIME} IST")
    print(f"   Daily 360° Dossier:       {DAILY_DOSSIER_TIME} IST")
    print(f"   Prelims Quiz Drill:       {PRELIMS_DRILL_TIME} IST")
    print(f"   PDF Prep (Admin Approval):{NEWSPAPER_PREP_TIME} IST (Ready before 5:30 PM)")
    print(f"   PDF Public Broadcast:     {NEWSPAPER_BROADCAST_TIME} IST (6:35 PM)")
    print(f"   Night Revision Audit:     {NIGHT_AUDIT_TIME} IST")
    print("=" * 60)

    check_missed_jobs()

    # Schedule daily jobs in local time
    schedule.every().day.at(get_local_time_for_ist(MORNING_KICKOFF_TIME)).do(job_morning_kickoff)
    schedule.every().day.at(get_local_time_for_ist(DAILY_DOSSIER_TIME)).do(job_daily_dossier)
    schedule.every().day.at(get_local_time_for_ist(PRELIMS_DRILL_TIME)).do(job_prelims_drill)
    schedule.every().day.at(get_local_time_for_ist(NEWSPAPER_PREP_TIME)).do(job_newspaper_prep)
    schedule.every().day.at(get_local_time_for_ist(NEWSPAPER_BROADCAST_TIME)).do(job_newspaper_broadcast)
    schedule.every().day.at(get_local_time_for_ist(NIGHT_AUDIT_TIME)).do(job_night_audit)
    # Check official exam sites periodically (every 60 minutes)
    schedule.every(60).minutes.do(job_exam_notifications)

    print("\nScheduler initialized. Running... Press Ctrl+C to exit.\n")

    last_missed_check = time.time()
    while True:
        schedule.run_pending()
        if time.time() - last_missed_check >= 60:
            try:
                check_missed_jobs(quiet=True)
            except Exception as e:
                logger.error(f"Periodic check failed: {e}")
            last_missed_check = time.time()
        time.sleep(30)


def run_current_time_job():
    """Determine and execute the appropriate job for the current IST time"""
    now = datetime.now(ist_offset)
    total_minutes = now.hour * 60 + now.minute
    print(f"Auto-detecting job for current IST time: {now.strftime('%H:%M:%S')}...")

    # Quiet Hours Guard: Do not disturb aspirants between 10:30 PM and 05:30 AM IST
    if total_minutes < 330:  # Before 05:30 AM IST
        print(f"Quiet hours ({now.strftime('%H:%M')} IST). Sleeping, no message to post.")
        return
    elif total_minutes >= 1350:  # After 10:30 PM IST
        print(f"Late night quiet hours ({now.strftime('%H:%M')} IST). Sleeping, no message to post.")
        return

    # Active daytime schedule (IST):
    # Check official exam notifications during all daytime/evening hours (06:00 AM to 10:30 PM IST)
    if 360 <= total_minutes <= 1350:
        job_exam_notifications()

    if 330 <= total_minutes < 480:  # 05:30 - 08:00 IST: Morning Kickoff
        job_morning_kickoff()
    elif 480 <= total_minutes < 690:  # 08:00 - 11:30 IST: Daily 360 Dossier
        job_daily_dossier()
    elif 690 <= total_minutes < 990:  # 11:30 - 16:30 IST: Prelims Drill
        job_prelims_drill()
    elif 990 <= total_minutes < 1080:  # 16:30 - 18:00 IST: Newspaper PDFs Prep & Send to Admin
        job_newspaper_prep()
    elif 1100 <= total_minutes < 1275:  # 18:20 - 21:15 IST: Broadcast at 6:35 PM if approved
        job_newspaper_broadcast()
    elif 1275 <= total_minutes < 1350:  # 21:15 - 22:30 IST: Night Reflection
        job_night_audit()
    else:
        print(f"No scheduled daily job for current time ({now.strftime('%H:%M')} IST).")


def run_full_test():
    print("\n" + "=" * 60)
    print("   RUNNING COMPLETE ASPIRANT ENGINE DEMO TEST")
    print("=" * 60)
    print("\n>>> 1. Testing Morning Kickoff...")
    job_morning_kickoff()
    time.sleep(2)

    print("\n>>> 2. Testing Daily 360° Dossier...")
    job_daily_dossier()
    time.sleep(2)

    print("\n>>> 3. Testing Prelims Interactive Drill...")
    job_prelims_drill()
    time.sleep(2)

    print("\n>>> 4. Testing Night Revision Audit...")
    job_night_audit()

    print("\n" + "=" * 60)
    print("   ALL MODULES TESTED SUCCESSFULLY! CHECK YOUR TELEGRAM CHANNEL!")
    print("=" * 60)


if __name__ == '__main__':
    command = sys.argv[1].lower() if len(sys.argv) > 1 else 'start'

    # Route commands
    if command in ['auto', 'cron']:
        run_current_time_job()
    elif command in ['test', 'full']:
        run_full_test()
    elif command in ['kickoff', 'greeting', 'morning']:
        job_morning_kickoff()

    elif command in ['dossier', 'news', 'morning-news']:
        job_daily_dossier()
    elif command in ['drill', 'quiz', 'prelims']:
        job_prelims_drill()
    elif command in ['mains', 'question']:
        job_mains_challenge()
    elif command in ['capsule', 'gk', 'flashcard']:
        job_capsule()
    elif command in ['model-answer', 'answer']:
        job_model_answer()
    elif command in ['night', 'goodnight', 'audit']:
        job_night_audit()
    elif command in ['pdf', 'material', 'study-material']:
        job_publish_study_pdf('both')
    elif command in ['pdf-en', 'pdf-english']:
        job_publish_study_pdf('english')
    elif command in ['pdf-kn', 'pdf-kannada']:
        job_publish_study_pdf('kannada')
    elif command in ['prep-pdf', 'prep-newspaper', 'prep']:
        job_newspaper_prep()
    elif command in ['approve', 'confirm']:
        arg = sys.argv[2] if len(sys.argv) > 2 else None
        if arg and arg.upper().startswith("NOTIF-"):
            from notification_approval import NotificationApprovalManager
            NotificationApprovalManager().approve(arg.upper())
        else:
            from approval_manager import ApprovalManager
            ApprovalManager().approve()
    elif command in ['reject', 'redo']:
        arg = sys.argv[2] if len(sys.argv) > 2 else None
        if arg and arg.upper().startswith("NOTIF-"):
            from notification_approval import NotificationApprovalManager
            NotificationApprovalManager().reject(arg.upper())
        else:
            from approval_manager import ApprovalManager
            ApprovalManager().reject()
    elif command in ['check-notifications', 'scan-notifications', 'notifications', 'notif']:
        from exam_notification_monitor import ExamNotificationMonitor
        ExamNotificationMonitor().scan_and_process()
    elif command in ['list-notifications', 'show-notifications', 'notif-list']:
        from notification_approval import NotificationApprovalManager
        NotificationApprovalManager().list_notifications()
    elif command in ['broadcast', 'post-pdf']:
        job_newspaper_broadcast()
    elif command == 'start':
        start()
    elif command == 'reset':
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
            print("Job state reset successfully!")
        else:
            print("No state file exists.")
    elif command == 'status':
        today = get_ist_date()
        print(f"\nStatus for {today}:")
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
            if today in state:
                for j, t in state[today].items():
                    print(f"   Done: {j} at {t}")
            else:
                print("   No standard jobs recorded today.")
        else:
            print("   No history.")

        # Also show PDF Approval Status
        from approval_manager import APPROVAL_STATE_FILE
        if os.path.exists(APPROVAL_STATE_FILE):
            try:
                with open(APPROVAL_STATE_FILE, 'r') as f:
                    pdf_st = json.load(f)
                if today in pdf_st:
                    p = pdf_st[today]
                    print(f"\n   📄 Newspaper PDFs ({today}):")
                    print(f"      • Status:       {p.get('status').upper()}")
                    print(f"      • Generated At: {p.get('generated_at')}")
                    print(f"      • Approved At:  {p.get('approved_at')}")
                    print(f"      • Posted At:    {p.get('posted_at')}")
            except Exception:
                pass

        # Also show Official Exam Notifications Status
        from exam_notification_monitor import REGISTRY_FILE
        if os.path.exists(REGISTRY_FILE):
            try:
                with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
                    reg = json.load(f)
                pending_cnt = sum(1 for v in reg.values() if v.get("status") == "pending_admin")
                posted_cnt = sum(1 for v in reg.values() if v.get("status") == "broadcasted")
                print(f"\n   🔔 Official Exam Notifications:")
                print(f"      • Total Detected: {len(reg)}")
                print(f"      • Awaiting You:   {pending_cnt} (Run 'python main.py list-notifications')")
                print(f"      • Broadcasted:    {posted_cnt}")
            except Exception:
                pass
    else:
        print(f"Unknown command: '{command}'")
        print("Usage: python main.py [start|test|kickoff|dossier|drill|night|prep-pdf|approve|reject|broadcast|pdf|check-notifications|list-notifications|status]")
