from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.db.sample_data import load_sample_data
from app.db.database import SessionLocal, get_db
from app.scheduler import start_scheduler
from app.services.report_service import generate_llm_report
from app.api.project import router as project_router

# ------------------------------------------------------------------------------
# 🚀 FastAPI Application
# ------------------------------------------------------------------------------   
app = FastAPI()

# ------------------------------------------------------------------------------
# 🚀 Startup Event — Load Sample Data + Start Background Scheduler
# ------------------------------------------------------------------------------
@app.on_event("startup")
def startup_events():
    db = SessionLocal()
    load_sample_data(db)
    start_scheduler()

# ------------------------------------------------------------------------------
# 📨 API Endpoint: Generate LLM-Based Weekly Report
# ------------------------------------------------------------------------------
@app.get("/api/report")
def get_weekly_report(
    project_id: int = Query(..., description="ID of the project"),
    channel: str = Query("gmail", enum=["gmail", "outlook", "whatsapp"]),
    language: str = Query("English", enum=["English", "Hindi"]),
    tone: str = Query("Formal", enum=["Formal", "Informal"]),
    db: Session = Depends(get_db)
):
    """
    Generate a weekly project report using LLM, formatted based on channel, language, and tone.
    """
    return {
        "report": generate_llm_report(
            project_id=project_id,
            channel=channel,
            language=language,
            tone=tone
        )
    }
