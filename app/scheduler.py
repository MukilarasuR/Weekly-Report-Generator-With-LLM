from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Project
from app.services.report_service import generate_report
from app.utils.gmail_sender import send_email
from app.utils.outlook_sender import send_outlook_email
import logging

logging.basicConfig(format="%(asctime)s — %(levelname)s — %(message)s", level=logging.INFO)

# ----------------------------------------------------------------------
# ✅ Gmail Scheduler Task
# ----------------------------------------------------------------------
def scheduled_weekly_gmail_report():
    logging.info("📧 Running Gmail weekly report...")
    db: Session = SessionLocal()
    for proj in db.query(Project).all():
        logging.info(f"🔍 Processing project: {proj.name} (ID: {proj.id})")
        res = generate_report(db, proj.id, channel="gmail")
        # Project-manager
        pm = res["project_manager_email"]
        pr = res["project_report"]
        subj = f"📊 Weekly Report – {res['project_name']}"
        if pm and pr:
            send_email(pm, subj, pr)
            logging.info(f"✅ Sent PM report to {pm}")
        # Phase-managers
        for phase in res["phases"]:
            em = phase["phase_manager_email"]
            rf = phase["report"]
            if em and rf:
                send_email(em, f"📌 Phase Update – {phase['phase_name']}", rf)
                logging.info(f"✅ Sent phase report to {em}")


# ----------------------------------------------------------------------
# ✅ Project Count Check for Gmail
# ----------------------------------------------------------------------
# def scheduled_weekly_gmail_report():
#     logging.info("📧 Running Gmail weekly report...")
#     try:
#         db: Session = SessionLocal()
#         all_projects = db.query(Project).all()
#         logging.info(f"📂 Total projects found: {len(all_projects)}")

#         for proj in all_projects:
#             logging.info(f"🔍 Processing project: {proj.name} (ID: {proj.id})")

#             res = generate_report(db, proj.id, channel="gmail")
#             if not res:
#                 logging.warning(f"⚠️ Report generation failed or returned empty for project ID {proj.id}")
#                 continue

#             # ✅ Project Manager Report
#             pm_email = res.get("project_manager_email")
#             pm_body = res.get("project_report")
#             subject_pm = f"📊 Weekly Report – {res['project_name']}"

#             if pm_email and pm_body:
#                 send_email(pm_email, subject_pm, pm_body)
#                 logging.info(f"✅ Sent PM report to {pm_email}")
#             else:
#                 logging.warning(f"⚠️ Missing project manager email or body for project: {proj.name}")

#             # ✅ Phase Managers Reports
#             for phase in res.get("phases", []):
#                 email = phase.get("phase_manager_email")
#                 report = phase.get("report")
#                 phase_name = phase.get("phase_name")

#                 if email and report:
#                     send_email(email, f"📌 Phase Update – {phase_name}", report)
#                     logging.info(f"✅ Sent phase report to {email}")
#                 else:
#                     logging.warning(f"⚠️ Skipping phase email: missing data for {phase_name}")

#     except Exception as e:
#         logging.error(f"❌ Exception in Gmail weekly report scheduler: {e}")

# ----------------------------------------------------------------------
# ✅ # Project Count Check for Outlook
# ----------------------------------------------------------------------
def scheduled_weekly_outlook_report():
    logging.info("📤 Running Outlook weekly report...")
    db: Session = SessionLocal()
    for proj in db.query(Project).all():
        logging.info(f"🔍 Processing project: {proj.name} (ID: {proj.id})")
        res = generate_report(db, proj.id, channel="outlook")
        pm = res["project_manager_email"]
        pr = res["project_report"]
        subj = f"📊 Weekly Outlook Report – {res['project_name']}"
        if pm and pr:
            send_outlook_email(pm, subj, pr)
            logging.info(f"✅ Sent PM report to {pm}")
        for phase in res["phases"]:
            em = phase["phase_manager_email"]
            rf = phase["report"]
            if em and rf:
                send_outlook_email(em, f"📌 Phase Update – {phase['phase_name']}", rf)
                logging.info(f"✅ Sent phase report to {em}")

# ----------------------------------------------------------------------
# ✅ Outlook Scheduler Task
# ----------------------------------------------------------------------
# from sqlalchemy.orm import Session
# from app.db.database import SessionLocal
# from app.db.models import Project
# from app.services.report_service import generate_report
# from app.utils.outlook_sender import send_outlook_email
# import logging

# def scheduled_weekly_outlook_report():
#     logging.info("📤 Running Outlook weekly report...")

#     try:
#         db: Session = SessionLocal()
#         all_projects = db.query(Project).all()
#         logging.info(f"📂 Total projects found: {len(all_projects)}")

#         for proj in all_projects:
#             logging.info(f"🔍 Processing project: {proj.name} (ID: {proj.id})")
#             res = generate_report(db, proj.id, channel="outlook")

#             if not res:
#                 logging.warning(f"⚠️ Report generation failed or returned empty for project ID {proj.id}")
#                 continue

#             # ✅ Project Manager Report
#             pm_email = res.get("project_manager_email")
#             pm_body = res.get("project_report")
#             subject_pm = f"📊 Weekly Outlook Report – {res['project_name']}"

#             if pm_email and pm_body:
#                 send_outlook_email(pm_email, subject_pm, pm_body)
#                 logging.info(f"✅ Sent PM report to {pm_email}")
#             else:
#                 logging.warning(f"⚠️ Missing PM email or report body for project: {proj.name}")

#             # ✅ Phase Managers Reports
#             for phase in res.get("phases", []):
#                 email = phase.get("phase_manager_email")
#                 report = phase.get("report")
#                 phase_name = phase.get("phase_name")

#                 if email and report:
#                     send_outlook_email(email, f"📌 Phase Update – {phase_name}", report)
#                     logging.info(f"✅ Sent phase report to {email}")
#                 else:
#                     logging.warning(f"⚠️ Skipping phase email: missing data for {phase_name}")

#     except Exception as e:
#         logging.error(f"❌ Exception in Outlook weekly report scheduler: {e}")


# ----------------------------------------------------------------------
# ✅ Main Scheduler
# ----------------------------------------------------------------------
# MAIN vs TEST scheduler blocks
# def start_main_scheduler():
#     scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
#     scheduler.add_job(scheduled_weekly_gmail_report, 'cron', day_of_week='mon', hour=10, minute=0)
#     scheduler.add_job(scheduled_weekly_outlook_report,'cron',day_of_week='mon',hour=10,minute=5)
#     scheduler.start()
#     logging.info("🗓️ Production scheduler started")


# ----------------------------------------------------------------------
# ✅ Test Scheduler
# ----------------------------------------------------------------------
def start_test_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(scheduled_weekly_gmail_report,'cron', day_of_week='mon-sun', hour=00, minute=11)
    scheduler.add_job(scheduled_weekly_outlook_report,'cron', day_of_week='mon-sun', hour=13, minute=48)
    scheduler.start()
    logging.info("🧪 Test Scheduler started")
