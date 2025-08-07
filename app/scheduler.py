from apscheduler.schedulers.background import BackgroundScheduler
from app.services.report_service import generate_report
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

# ----------------------------------------------------------------------
# ✅ Gmail Scheduler: Sends Project + Phase-specific reports
# ----------------------------------------------------------------------
def scheduled_weekly_gmail_report():
    logging.info("📧 Running Gmail weekly report...")
    try:
        db: Session = SessionLocal()
        all_projects = db.query(Project).all()

        for project in all_projects:
            result = generate_report(db, project_id=project.id, channel="gmail")

            # ✅ Project Manager report
            pm_email = result.get("project_manager_email")
            pm_body = result.get("project_report")
            subject_pm = f"📊 Weekly Report – {result['project_name']}"

            if pm_email and pm_body:
                send_email(pm_email, subject_pm, pm_body)
                logging.info(f"✅ Gmail report sent to Project Manager: {pm_email}")
            else:
                logging.warning(f"⚠️ Missing project manager email or body for project: {project.name}")

            # ✅ Each Phase Manager gets their own report
            for phase in result["phases"]:
                email = phase.get("phase_manager_email")
                report = phase.get("report")
                phase_name = phase.get("phase_name")

                if email and report:
                    send_email(email, f"📌 Phase Update – {phase_name}", report)
                    logging.info(f"✅ Gmail report sent to Phase Manager: {email}")
                else:
                    logging.warning(f"⚠️ Missing phase manager email or report for phase: {phase_name}")

    except Exception as e:
        logging.error(f"❌ Gmail sending error: {e}")

# ----------------------------------------------------------------------
# ✅ Outlook Scheduler: Same logic as above
# ----------------------------------------------------------------------
def scheduled_weekly_outlook_report():
    logging.info("📤 Running Outlook weekly report...")
    try:
        db: Session = SessionLocal()
        all_projects = db.query(Project).all()

        for project in all_projects:
            result = generate_report(db, project_id=project.id, channel="outlook")

            # ✅ Project Manager report
            pm_email = result.get("project_manager_email")
            pm_body = result.get("project_report")
            subject_pm = f"📊 Weekly Outlook Report – {result['project_name']}"

            if pm_email and pm_body:
                send_outlook_email(pm_email, subject_pm, pm_body)
                logging.info(f"✅ Outlook report sent to Project Manager: {pm_email}")
            else:
                logging.warning(f"⚠️ Missing project manager email or body for project: {project.name}")

            # ✅ Each Phase Manager gets their own report
            for phase in result["phases"]:
                email = phase.get("phase_manager_email")
                report = phase.get("report")
                phase_name = phase.get("phase_name")

                if email and report:
                    send_outlook_email(email, f"📌 Phase Update – {phase_name}", report)
                    logging.info(f"✅ Outlook report sent to Phase Manager: {email}")
                else:
                    logging.warning(f"⚠️ Missing phase manager email or report for phase: {phase_name}")

    except Exception as e:
        logging.error(f"❌ Outlook sending error: {e}")

# ----------------------------------------------------------------------
# ✅ Main Scheduler (Production: Runs every Monday)
# ----------------------------------------------------------------------
# def start_main_scheduler():
#     scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
#     scheduler.add_job(scheduled_weekly_gmail_report, 'cron', day_of_week='mon', hour=10, minute=0, id="weekly_gmail_job")
#     scheduler.add_job(scheduled_weekly_outlook_report, 'cron', day_of_week='mon', hour=10, minute=5, id="weekly_outlook_job")
#     scheduler.start()
#     logging.info("🗓️ Main Production Scheduler started")

# ----------------------------------------------------------------------
# 🧪 Test Scheduler (Runs every day for development)
# ----------------------------------------------------------------------
def start_test_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(scheduled_weekly_gmail_report, 'cron', day_of_week='mon-sun', hour=18, minute=24, id="test_gmail_job")
    scheduler.add_job(scheduled_weekly_outlook_report, 'cron', day_of_week='mon-sun', hour=13, minute=48, id="test_outlook_job")
    scheduler.start()
    logging.info("🧪 Test Scheduler started")
