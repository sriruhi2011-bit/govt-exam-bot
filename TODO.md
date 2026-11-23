# Aspirant Master Prep Engine (KanSiri Daily CA & GS)

## Daily Schedule & Automation Architecture (IST)
- [x] **06:30 AM IST**: Morning Kickoff, Mindset Framing & Target Setting (`habit_tracker.py`).
- [x] **08:30 AM IST**: Daily 360° Issue Dossier with constitutional framework, analytical dimensions, and committees (`dossier_generator.py`).
- [x] **11:00 AM & 03:30 PM IST**: Official Exam Notification Monitor - automatic scraping of KPSC, KEA, UPSC portals (`exam_notification_monitor.py`).
- [x] **01:00 PM IST**: Prelims & Objective MCQ Drill with native Telegram Quiz Polls and explanation popups (`prelims_drill.py`).
- [x] **05:15 PM IST**: Daily Newspaper Study Material PDFs (The Hindu & Prajavani) generated and sent to Admin for review & approval (`newspaper_pdf_pipeline.py`, `approval_manager.py`).
- [x] **06:35 PM IST**: Broadcast Confirmed Newspaper Study Material PDFs to Telegram & WhatsApp channels upon approval.
- [x] **09:30 PM IST**: Night Revision Audit & Active Recall (`habit_tracker.py`).

## Automated Triggers
- [x] **GitHub Actions Workflow**: `.github/workflows/daily_bot.yml` runs on UTC cron schedule and supports manual `workflow_dispatch` triggers for all jobs (`auto`, `kickoff`, `dossier`, `drill`, `prep`, `broadcast`, `check-notifications`, `night`, `status`).
- [x] **Local 24/7 Scheduler**: `python main.py start` runs continuous daemon with missed-job catchup.
