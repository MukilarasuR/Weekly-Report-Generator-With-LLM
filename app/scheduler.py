from apscheduler.schedulers.background import BackgroundScheduler
from app.services.report_service import generate_report
from app.utils.gmail_sender import send_email
from app.utils.outlook_sender import send_outlook_email
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
import logging

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

        # Send to Project Manager
        send_email("mukilarasu0923@gmail.com", subject, body)
        logging.info("✅ Gmail report sent to Project Manager")

        # Optional: Send to Phase Managers
        if "phases" in report_data:
            for phase in report_data["phases"]:
                email = phase.get("phase_manager_email")
                if email:
                    send_email(email, f"📌 Phase Update – {phase['phase_name']}", body)
                    logging.info(f"✅ Gmail report sent to Phase Manager: {email}")
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

        # Send to Project Manager
        send_outlook_email("mukilarasu0923@outlook.com", subject, body)
        logging.info("✅ Outlook report sent to Project Manager")

        # Optional: Send to Phase Managers
        if "phases" in report_data:
            for phase in report_data["phases"]:
                email = phase.get("phase_manager_email")
                if email:
                    send_outlook_email(email, f"📌 Phase Update – {phase['phase_name']}", body)
                    logging.info(f"✅ Outlook report sent to Phase Manager: {email}")
    except Exception as e:
        logging.error(f"❌ Outlook sending error: {e}")

# --------------------------------------------------------------------------
# ✅ MAIN SCHEDULER – Runs Every Monday at Fixed Times (Production)
# --------------------------------------------------------------------------
# def start_main_scheduler():
#     scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
#     scheduler.add_job(scheduled_weekly_gmail_report, 'cron', day_of_week='mon', hour=10, minute=0, id="weekly_gmail_job")
#     scheduler.add_job(scheduled_weekly_outlook_report, 'cron', day_of_week='mon', hour=10, minute=5, id="weekly_outlook_job")
#     scheduler.start()
#     logging.info("🗓️ Main Production Scheduler started (Mon Gmail @ 10:00, Outlook @ 10:05)")

# --------------------------------------------------------------------------
# 🧪 TEST SCHEDULER – Runs Daily at Set Times (Development)
# --------------------------------------------------------------------------
def start_test_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(scheduled_weekly_gmail_report, 'cron', day_of_week='mon-sun', hour=17, minute=11, id="test_gmail_job")
    scheduler.add_job(scheduled_weekly_outlook_report, 'cron', day_of_week='mon-sun', hour=13, minute=48, id="test_outlook_job")
    scheduler.start()
    logging.info("🧪 Test Scheduler started (Daily Gmail @ 3:20 PM, Outlook @ 1:48 PM)")
