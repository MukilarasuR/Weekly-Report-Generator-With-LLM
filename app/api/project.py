from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Project
from app.services.report_service import generate_report
from app.utils.gmail_sender import send_email as send_gmail
from app.utils.outlook_sender import send_outlook_email as send_outlook
# from app.utils.whatsapp_sender import send_whatsapp  # Future integration

router = APIRouter()

@router.get("/report/send")
def send_report(
    project_id: int,
    channel: str,
    language: str = "English",
    tone: str = "Formal",
    model: str = "gpt-3.5-turbo",
    db: Session = Depends(get_db)
):
    # Generate the report using LLM
    response = generate_report(
        db=db,
        channel=channel,
        language=language,
        tone=tone,
        model=model
    )

    report = response["report"]

    # Get actual email/phone from project info
    project_data = db.query(Project).filter(Project.id == project_id).first()
    if not project_data:
        raise HTTPException(status_code=404, detail="Project not found")

    manager_email = getattr(project_data, "manager_email", "manager@example.com")
    manager_phone = getattr(project_data, "manager_phone", "+919363332539")

    # Send via selected channel
    if channel == "gmail":
        send_gmail(to=manager_email, subject="Weekly Project Report", body=report)
    elif channel == "outlook":
        send_outlook(to=manager_email, subject="Weekly Project Report", body=report)
    elif channel == "whatsapp":
        # TODO: Implement WhatsApp integration
        # send_whatsapp(to=manager_phone, message=report)
        raise HTTPException(status_code=501, detail="WhatsApp integration not implemented yet")
    else:
        raise HTTPException(status_code=400, detail="Invalid channel selected")

    return {
        "status": f"Report sent successfully via {channel}",
        "channel": channel,
        "language": language,
        "tone": tone,
        "model": model
    }
