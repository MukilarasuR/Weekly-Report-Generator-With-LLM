from sqlalchemy.orm import Session
from datetime import date
from .models import Project, Phase, Task

def load_sample_data(db: Session):
    project = Project(
        name="Mall Construction",
        status="in_progress",
        manager="Arjun Mehta",
        start_date=date(2024, 1, 10),
        end_date=date(2025, 12, 31)
    )

    phase1 = Phase(name="Foundation", status="completed", project=project)
    phase2 = Phase(name="Structural Work", status="in_progress", project=project)
    phase3 = Phase(name="Interiors", status="not_started", project=project)

    task1 = Task(name="Lay foundation", status="COMPLETED", estimated_budget=1000000, actual_budget=1000000, phase=phase1)
    task2 = Task(name="Waterproofing base", status="COMPLETED", estimated_budget=150000, actual_budget=150000, phase=phase1)
    task3 = Task(name="Concrete frame setup", status="IN_PROGRESS", estimated_budget=2000000, actual_budget=500000, phase=phase2)
    task4 = Task(name="Beam testing", status="NOT_STARTED", estimated_budget=500000, actual_budget=0, phase=phase2)
    task5 = Task(name="HVAC Layout", status="NOT_STARTED", estimated_budget=800000, actual_budget=0, phase=phase3)

    db.add(project)
    db.commit()
