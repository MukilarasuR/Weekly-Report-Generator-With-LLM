from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.db.models import Project, WeeklyReport
from app.utils.llm_generator import render_llm_prompt, generate_llm_report

def get_deadline_alerts(tasks):
    today = date.today()
    overdue, upcoming = [], []
    cutoff = today + timedelta(days=7)
    for t in tasks:
        if not t.due_date or t.status == "COMPLETED":
            continue
        if t.due_date < today:
            overdue.append(t)
        elif today <= t.due_date <= cutoff:
            upcoming.append(t)
    return overdue, upcoming

def generate_report(db: Session, project_id: int, channel="gmail",
                    language="English", tone="Formal", model="gpt-3.5-turbo"):
    project = db.query(Project).get(project_id)
    if not project:
        return {"error": "Project not found."}

    phases = project.phases
    tasks  = [t for p in phases for t in p.tasks]

    # Finance
    finance = {}
    if project.finance_requests:
        fr = project.finance_requests[-1]
        finance = {
            "requested_amount": fr.requested_amount,
            "approved_amount": fr.approved_amount
        }

    # Alerts
    overdue, upcoming = get_deadline_alerts(tasks)

    # Last summary
    last = (db.query(WeeklyReport)
              .filter_by(project_id=project_id)
              .order_by(WeeklyReport.report_date.desc())
              .first())

    # Sample additions (temporarily hardcoded for demo)
    sample_context = {
        "accomplishments": [
            "Structural frame 80% completed",
            "Vendor contract finalized for HVAC",
            "Cleared site inspection checklist"
        ],
        "recommendations": [
            "Increase labor allocation to meet deadline",
            "Replace supplier for delayed materials"
        ],
        "agenda_items": [
            "Resource bottlenecks",
            "Progress on HVAC layout",
            "Finance request review"
        ],
        "notes": [
            "Weather conditions slowed progress",
            "Awaiting approval for next phase budget"
        ],
        "summary_text": last.summary_text if last else (
            "Mall Construction project continues to progress steadily. Structural work is advancing, "
            "with key components nearing completion. Budget utilization is on track, and team performance remains consistent."
        )
    }

    # Context for project-manager template
    proj_ctx = {
        "language":  language,
        "tone":      tone,
        "channel":   channel,
        "project": {
            "project_name":    project.name,
            "status":          project.status,
            "project_manager": project.manager.name,
            "start_date":      project.start_date,
            "end_date":        project.end_date,
        },
        "phases": [
            {
                "id": p.id,
                "phase_name": p.name,
                "status": p.status,
                "phase_manager_email": p.phase_manager.email if p.phase_manager else None
            }
            for p in phases
        ],
        "tasks": [
            {
                "name": t.name,
                "status": t.status,
                "due_date": t.due_date,
                "phase_id": t.phase_id,
                "phase_name": next(p.name for p in phases if p.id == t.phase_id)
            }
            for t in tasks
        ],
        "finance":         finance,
        "overdue_tasks":   overdue,
        "upcoming_tasks":  upcoming,
        "sender_name":     "Project Automation Bot",
        "sender_position": "AI Assistant",
        **sample_context  # Injected additions
    }

    # Render & call LLM for project manager
    proj_prompt = render_llm_prompt("app/templates/weekly_report_prompt.txt", proj_ctx)
    proj_report = generate_llm_report(proj_prompt, model=model)

    # Persist the report
    db.add(WeeklyReport(
        project_id=project_id,
        summary_text=proj_report,
        report_date=date.today()
    ))
    db.commit()

    # Now generate phase manager reports
    phase_reports = []
    for p in phases:
        pts = [t for t in tasks if t.phase_id == p.id]
        od, up = get_deadline_alerts(pts)
        ctx = {
            "report_date": date.today(),
            "project": proj_ctx["project"],
            "phase": {
                "phase_name": p.name,
                "status": p.status,
                "phase_manager_email": p.phase_manager.email if p.phase_manager else None
            },
            "tasks": pts,
            "overdue_tasks": od,
            "upcoming_tasks": up,
            "budget_status": finance.get("approved_amount", 0),
            "resource_status": "Team performing at expected efficiency levels",
            **{k: v for k, v in sample_context.items() if k in (
                "accomplishments", "recommendations", "agenda_items", "notes",
                "sender_name", "sender_position"
            )}
        }
        ph_prompt = render_llm_prompt("app/templates/weekly_phase_manager_prompt.txt", ctx)
        ph_report = generate_llm_report(ph_prompt, model=model)
        phase_reports.append({
            "phase_name": p.name,
            "phase_manager_email": ctx["phase"]["phase_manager_email"],
            "report": ph_report
        })

    return {
        "project_id": project.id,
        "project_name": project.name,
        "project_manager_email": project.manager.email,
        "project_report": proj_report,
        "phases": phase_reports
    }
