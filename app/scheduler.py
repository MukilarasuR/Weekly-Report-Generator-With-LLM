from apscheduler.schedulers.background import BackgroundScheduler
from app.services.report_service import generate_report
from app.utils.gmail_sender import send_email
from app.utils.outlook_sender import send_outlook_email
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
import logging

# ------------------------------------------
# ✅ Setup Logging
# ------------------------------------------
logging.basicConfig(
    format="%(asctime)s — %(levelname)s — %(message)s",
    level=logging.INFO
)

# ------------------------------------------
# ✅ Gmail Scheduler Task
# ------------------------------------------
def scheduled_weekly_gmail_report():
    logging.info("📧 Running Gmail weekly report...")
    try:
        db: Session = SessionLocal()
        report_data = generate_report(db, channel="gmail")
        subject = "📊 Weekly Report – Mall Construction"
        body = report_data["report"]
        send_email("mukilarasu0923@gmail.com", subject, body)
        logging.info("✅ Gmail report sent to mukilarasu0923@gmail.com")
    except Exception as e:
        logging.error(f"❌ Gmail sending error: {e}")

# ------------------------------------------
# ✅ Outlook Scheduler Task
# ------------------------------------------
def scheduled_weekly_outlook_report():
    logging.info("📤 Running Outlook weekly report...")
    try:
        db: Session = SessionLocal()
        report_data = generate_report(db, channel="outlook")
        subject = "📊 Weekly Outlook Report – Mall Construction"
        body = report_data["report"]
        send_outlook_email("mukilarasu0923@outlook.com", subject, body)
        logging.info("✅ Outlook report sent to mukilarasu0923@outlook.com")
    except Exception as e:
        logging.error(f"❌ Outlook sending error: {e}")

# =================================================================================================
# 🕒 ORIGINAL WEEKLY SCHEDULERS — Runs Every Monday (production)
# =================================================================================================

# def start_scheduler():
#     scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
#     scheduler.add_job(
#         scheduled_weekly_gmail_report,
#         trigger='cron',
#         day_of_week='mon',
#         hour=10,
#         minute=0,
#         id="weekly_gmail_job"
#     )
#     scheduler.add_job(
#         scheduled_weekly_outlook_report,
#         trigger='cron',
#         day_of_week='mon',
#         hour=10,
#         minute=5,
#         id="weekly_outlook_job"
#     )
#     scheduler.start()
#     logging.info("🗓️ Weekly Scheduler started (Gmail @ 10:00 AM, Outlook @ 10:05 AM every Monday)")

# =================================================================================================
# 🧪 TEST SCHEDULERS — Runs Daily at Specific Time for Testing
# =================================================================================================

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    # Gmail test job — runs every day at 1:46 PM
    scheduler.add_job(
        scheduled_weekly_gmail_report,
        trigger='cron',
        day_of_week='mon-sun',
        hour=12,  # 1 PM = 13
        minute=21,
        id="test_gmail_job"
    )

    # Outlook test job — runs every day at 1:48 PM
    scheduler.add_job(
        scheduled_weekly_outlook_report,
        trigger='cron',
        day_of_week='mon-sun',
        hour=13,  # 1 PM = 13
        minute=48,
        id="test_outlook_job"
    )

    scheduler.start()
    logging.info("🧪 Daily Test Scheduler started...")  # (Gmail @ 2:46 PM, Outlook @ 1:48 PM)
