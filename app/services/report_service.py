from sqlalchemy.orm import Session
from app.db.models import Project
from app.utils.llm_generator import render_llm_prompt, generate_llm_report


def generate_report(db: Session, channel: str = "gmail", language: str = "English", tone: str = "Formal", model: str = "gpt-3.5-turbo"):
    # Fetch first project for demo purpose
    project = db.query(Project).first()
    if not project:
        return {"error": "No project found in database."}

    # Extract related data
    phases = project.phases or []
    tasks = []
    for phase in phases:
        tasks.extend(phase.tasks or [])

    # Optional: handle finance data if available
    finance_data = {}
    if hasattr(project, 'finance_requests') and project.finance_requests:
        latest_request = project.finance_requests[-1]
        finance_data = {
            "requested_amount": latest_request.requested_amount,
            "approved_amount": latest_request.approved_amount
        }

    # Build prompt context for Jinja2
    context = {
        "channel": channel,
        "language": language,
        "tone": tone,
        "project": {
            "project_name": project.name,
            "status": project.status,
            "project_manager": project.manager,
            "start_date": project.start_date,
            "end_date": project.end_date
        },
        "phases": [{"phase_name": p.name, "status": p.status} for p in phases],
        "tasks": [{"name": t.name, "status": t.status, "estimated_budget": t.estimated_budget, "actual_budget": t.actual_budget} for t in tasks],
        "finance": finance_data
    }

    # Render and generate LLM report
    template_path = "app/templates/weekly_report_prompt.txt"
    prompt = render_llm_prompt(template_path, context)
    llm_output = generate_llm_report(prompt, model=model)

    return {
        "channel": channel,
        "language": language,
        "tone": tone,
        "report": llm_output
    }
