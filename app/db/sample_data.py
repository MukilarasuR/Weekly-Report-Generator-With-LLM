from sqlalchemy.orm import Session
from datetime import date
from app.db.models import (
    User,
    Project,
    Phase,
    Task,
    FinanceRequest,
    ProjectStatus,
    PhaseStatus,
    TaskStatus
)

def load_sample_data(db: Session):
    # Check if sample data already exists
    existing_user = db.query(User).filter(User.email == "arjun.mehta@company.com").first()
    if existing_user:
        print("Sample data already exists, skipping...")
        return

    # -------------------------------------
    # ✅ 1. Users (project manager + phase managers)
    # -------------------------------------
    project_manager = User(name="Arjun Mehta", email="arjun.mehta@company.com")
    foundation_manager = User(name="Priya Sharma", email="priya.sharma@company.com")
    structural_manager = User(name="Rahul Verma", email="rahul.verma@company.com")
    interiors_manager = User(name="Sneha Kapoor", email="sneha.kapoor@company.com")

    db.add_all([project_manager, foundation_manager, structural_manager, interiors_manager])
    db.commit()

    # -------------------------------------
    # ✅ 2. Project
    # -------------------------------------
    project = Project(
        name="Mall Construction",
        status=ProjectStatus.IN_PROGRESS,
        manager_id=project_manager.id,
        start_date=date(2024, 1, 10),
        end_date=date(2025, 12, 31)
    )
    db.add(project)
    db.commit()

    # -------------------------------------
    # ✅ 3. Phases with phase managers
    # -------------------------------------
    phase1 = Phase(
        name="Foundation",
        status=PhaseStatus.COMPLETED,
        project_id=project.id,
        phase_manager_id=foundation_manager.id
    )
    phase2 = Phase(
        name="Structural Work",
        status=PhaseStatus.IN_PROGRESS,
        project_id=project.id,
        phase_manager_id=structural_manager.id
    )
    phase3 = Phase(
        name="Interiors",
        status=PhaseStatus.NOT_STARTED,
        project_id=project.id,
        phase_manager_id=interiors_manager.id
    )
    db.add_all([phase1, phase2, phase3])
    db.commit()

    # -------------------------------------
    # ✅ 4. Tasks with due dates
    # -------------------------------------
    task1 = Task(
        name="Lay foundation",
        status=TaskStatus.COMPLETED,
        estimated_budget=1000000,
        actual_budget=1000000,
        due_date=date(2024, 3, 10),
        phase_id=phase1.id
    )
    task2 = Task(
        name="Waterproofing base",
        status=TaskStatus.COMPLETED,
        estimated_budget=150000,
        actual_budget=150000,
        due_date=date(2024, 4, 5),
        phase_id=phase1.id
    )
    task3 = Task(
        name="Concrete frame setup",
        status=TaskStatus.IN_PROGRESS,
        estimated_budget=2000000,
        actual_budget=500000,
        due_date=date(2025, 8, 10),  # Upcoming
        phase_id=phase2.id
    )
    task4 = Task(
        name="Beam testing",
        status=TaskStatus.NOT_STARTED,
        estimated_budget=500000,
        actual_budget=0,
        due_date=date(2025, 7, 31),  # Overdue
        phase_id=phase2.id
    )
    task5 = Task(
        name="HVAC Layout",
        status=TaskStatus.NOT_STARTED,
        estimated_budget=800000,
        actual_budget=0,
        due_date=date(2025, 8, 15),
        phase_id=phase3.id
    )

    db.add_all([task1, task2, task3, task4, task5])
    db.commit()

    # -------------------------------------
    # ✅ 5. Finance request
    # -------------------------------------
    finance = FinanceRequest(
        project_id=project.id,
        requested_amount=2000000,
        approved_amount=500000,
        request_date=date(2025, 8, 4)
    )
    db.add(finance)
    db.commit()
