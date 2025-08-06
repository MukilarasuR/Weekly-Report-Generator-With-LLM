from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.models import Project
from app.utils.llm_generator import render_llm_prompt, generate_llm_report

# ✅ New helper function to find deadline-based tasks
def get_deadline_alerts(tasks):
    today = datetime.now().date()
    upcoming_threshold = today + timedelta(days=7)

    overdue = []
    upcoming = []

    for task in tasks:
        if not hasattr(task, 'due_date') or task.due_date is None:
            continue
        if task.due_date < today and task.status != "COMPLETED":
            overdue.append(task)
        elif today <= task.due_date <= upcoming_threshold and task.status != "COMPLETED":
            upcoming.append(task)

    return overdue, upcoming

# ✅ Main function — with phase manager email added
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

    # Optional finance data
    finance_data = {}
    if hasattr(project, 'finance_requests') and project.finance_requests:
        latest_request = project.finance_requests[-1]
        finance_data = {
            "requested_amount": latest_request.requested_amount,
            "approved_amount": latest_request.approved_amount
        }

    # ✅ Deadline alerts
    overdue_tasks, upcoming_tasks = get_deadline_alerts(tasks)

    # ✅ Build context for prompt
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
        "phases": [
            {
                "phase_name": p.name,
                "status": p.status,
                "id": p.id,
                # ✅ New field for scheduler to send report
                "phase_manager_email": getattr(p.phase_manager, "email", None),  # Safe access
                "assistant_manager_email": getattr(p.assistant_manager, "email", None)  # Optional
            }
            for p in phases
        ],
        "tasks": [
            {
                "name": t.name,
                "status": t.status,
                "estimated_budget": t.estimated_budget,
                "actual_budget": t.actual_budget,
                "due_date": t.due_date,
                "phase_id": t.phase_id,
                "phase_name": next((p.name for p in phases if p.id == t.phase_id), None)
            }
            for t in tasks
        ],
        "finance": finance_data,

        "overdue_tasks": [
            {
                "name": t.name,
                "due_date": t.due_date,
                "phase_name": next((p.name for p in phases if p.id == t.phase_id), None)
            }
            for t in overdue_tasks
        ],
        "upcoming_tasks": [
            {
                "name": t.name,
                "due_date": t.due_date,
                "phase_name": next((p.name for p in phases if p.id == t.phase_id), None)
            }
            for t in upcoming_tasks
        ]
    }

    # ✅ Render prompt and get LLM response
    template_path = "app/templates/weekly_report_prompt.txt"
    prompt = render_llm_prompt(template_path, context)
    llm_output = generate_llm_report(prompt, model=model)

    return {
        "channel": channel,
        "language": language,
        "tone": tone,
        "report": llm_output,
        # ✅ Include phases in report_data for scheduler to use
        "phases": context["phases"]
    }
