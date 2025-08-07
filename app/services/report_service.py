from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from app.db.models import Project, WeeklyReport
from app.utils.llm_generator import render_llm_prompt, generate_llm_report


def get_deadline_alerts(tasks):
    today = date.today()
    overdue_tasks = []
    upcoming_tasks = []

    for task in tasks:
        if task.due_date:
            if task.due_date < today and task.status != "COMPLETED":
                overdue_tasks.append({
                    "name": task.name,
                    "due_date": task.due_date,
                    "status": task.status,
                    "days_overdue": (today - task.due_date).days
                })
            elif today <= task.due_date <= today + timedelta(days=7) and task.status != "COMPLETED":
                upcoming_tasks.append({
                    "name": task.name,
                    "due_date": task.due_date,
                    "status": task.status,
                    "days_until_due": (task.due_date - today).days
                })

    return overdue_tasks, upcoming_tasks


def generate_report(
    db: Session,
    project_id: int,
    channel: str = "gmail",
    language: str = "English",
    tone: str = "Formal",
    model: str = "gpt-3.5-turbo"
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return {"error": "Project not found."}

    phases = project.phases or []
    tasks = [task for phase in phases for task in phase.tasks or []]

    finance_data = {}
    if project.finance_requests:
        latest = project.finance_requests[-1]
        finance_data = {
            "requested_amount": latest.requested_amount,
            "approved_amount": latest.approved_amount
        }

    overdue_tasks, upcoming_tasks = get_deadline_alerts(tasks)

    last_summary = db.query(WeeklyReport).filter(
        WeeklyReport.project_id == project_id
    ).order_by(WeeklyReport.report_date.desc()).first()

    # Static placeholders (or replace with LLM later)
    accomplishments = ["Foundation completed", "Finance request approved"]
    recommendations = ["Complete beam testing ASAP", "Review HVAC contractor bids"]
    risks = ["Beam testing is overdue", "Rain may delay HVAC layout"]
    agenda_items = ["Finalize structural phase", "Discuss resource load"]
    notes = ["Site inspection scheduled next Monday", "Contractor invoices pending"]

    estimated_total = sum([t.estimated_budget or 0 for t in tasks])
    actual_spent = sum([t.actual_budget or 0 for t in tasks])
    budget_status = f"₹{actual_spent:,} / ₹{estimated_total:,}"
    resource_status = "All team members are on track"

    # -------------------------------------------
    # 📌 Project Manager Report Context
    # -------------------------------------------
    project_context = {
        "report_date": date.today(),
        "channel": channel,
        "language": language,
        "tone": tone,
        "project": {
            "project_name": project.name,
            "status": project.status,
            "project_manager": project.manager.name,
            "start_date": project.start_date,
            "end_date": project.end_date
        },
        "phases": [
            {
                "id": p.id,
                "phase_name": p.name,
                "status": p.status,
                "phase_manager_email": getattr(p.phase_manager, "email", None)
            } for p in phases
        ],
        "tasks": [
            {
                "name": t.name,
                "status": t.status,
                "estimated_budget": t.estimated_budget,
                "actual_budget": t.actual_budget,
                "due_date": t.due_date,
                "phase_id": t.phase_id,
                "phase_name": next((p.name for p in phases if p.id == t.phase_id), None),
            } for t in tasks
        ],
        "finance": finance_data,
        "overdue_tasks": overdue_tasks,
        "upcoming_tasks": upcoming_tasks,
        "summary_text": last_summary.summary_text if last_summary else None,
        "accomplishments": accomplishments,
        "tasks_completed": [t for t in tasks if t.status == "COMPLETED"],
        "milestones": [t for t in tasks if "milestone" in t.name.lower()],
        "risks": risks,
        "budget_status": budget_status,
        "resource_status": resource_status,
        "recommendations": recommendations,
        "agenda_items": agenda_items,
        "notes": notes,
        "sender_name": "Project Automation Bot",
        "sender_position": "AI Assistant"
    }

    project_template_path = "app/templates/weekly_report_prompt.txt"
    project_prompt = render_llm_prompt(project_template_path, project_context)
    project_llm_output = generate_llm_report(project_prompt, model=model)

    db.add(WeeklyReport(
        project_id=project_id,
        summary_text=project_llm_output,
        report_date=date.today()
    ))
    db.commit()

    # -------------------------------------------
    # 📌 Phase Manager Reports (One per phase)
    # -------------------------------------------
    phase_reports = []
    for phase in phases:
        phase_tasks = [t for t in tasks if t.phase_id == phase.id]
        overdue, upcoming = get_deadline_alerts(phase_tasks)

        phase_context = {
            "report_date": date.today(),
            "channel": channel,
            "language": language,
            "tone": tone,
            "project": {
                "project_name": project.name,
                "status": project.status,
                "project_manager": project.manager.name,
                "start_date": project.start_date,
                "end_date": project.end_date
            },
            "phase": {
                "id": phase.id,
                "phase_name": phase.name,
                "status": phase.status,
                "phase_manager_email": getattr(phase.phase_manager, "email", None)
            },
            "tasks": phase_tasks,
            "overdue_tasks": overdue,
            "upcoming_tasks": upcoming,
            "summary_text": last_summary.summary_text if last_summary else None,
            "accomplishments": accomplishments,
            "recommendations": recommendations,
            "risks": risks,
            "budget_status": budget_status,
            "resource_status": resource_status,
            "agenda_items": agenda_items,
            "notes": notes,
            "sender_name": "Project Automation Bot",
            "sender_position": "AI Assistant"
        }

        phase_template_path = "app/templates/weekly_phase_manager_prompt.txt"
        phase_prompt = render_llm_prompt(phase_template_path, phase_context)
        phase_output = generate_llm_report(phase_prompt, model=model)

        phase_reports.append({
            "phase_id": phase.id,
            "phase_name": phase.name,
            "phase_manager_email": getattr(phase.phase_manager, "email", None),
            "report": phase_output
        })

    return {
        "project_id": project.id,
        "project_name": project.name,
        "project_manager_email": project.manager.email,
        "project_report": project_llm_output,
        "phases": phase_reports
    }