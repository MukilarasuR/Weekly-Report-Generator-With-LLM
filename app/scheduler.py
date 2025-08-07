from apscheduler.schedulers.background import BackgroundScheduler
from app.services.report_service import generate_report  # ✅ FIXED: Removed generate_phase_report
from app.utils.gmail_sender import send_email
from app.utils.outlook_sender import send_outlook_email
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Project
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
        all_projects = db.query(Project).all()

        for project in all_projects:
            result = generate_report(db, project_id=project.id, channel="gmail")
            subject = f"📊 Weekly Report – {result['project_name']}"
            body = result["project_report"]

            # ✅ Send to Project Manager
            send_email(result["project_manager_email"], subject, body)
            logging.info(f"✅ Gmail report sent to Project Manager: {result['project_manager_email']}")

            # ✅ Send to Phase Managers
            for phase in result["phases"]:
                email = phase.get("phase_manager_email")
                if email and phase.get("report"):
                    send_email(email, f"📌 Phase Update – {phase['phase_name']}", phase["report"])
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
        all_projects = db.query(Project).all()

        for project in all_projects:
            result = generate_report(db, project_id=project.id, channel="outlook")
            subject = f"📊 Weekly Outlook Report – {result['project_name']}"
            body = result["project_report"]

            # ✅ Send to Project Manager
            send_outlook_email(result["project_manager_email"], subject, body)
            logging.info(f"✅ Outlook report sent to Project Manager: {result['project_manager_email']}")

            # ✅ Send to Phase Managers
            for phase in result["phases"]:
                email = phase.get("phase_manager_email")
                if email and phase.get("report"):
                    send_outlook_email(email, f"📌 Phase Update – {phase['phase_name']}", phase["report"])
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
    scheduler.add_job(scheduled_weekly_gmail_report, 'cron', day_of_week='mon-sun', hour=16, minute=15, id="test_gmail_job")
    scheduler.add_job(scheduled_weekly_outlook_report, 'cron', day_of_week='mon-sun', hour=13, minute=48, id="test_outlook_job")
    scheduler.start()
    logging.info("🧪 Test Scheduler started (Daily Gmail @ 7:20 PM, Outlook @ 1:48 PM)")
