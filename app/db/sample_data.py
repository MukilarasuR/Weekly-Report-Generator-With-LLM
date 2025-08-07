from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.db.models import (
    User,
    Project,
    Phase,
    Task,
    FinanceRequest,
    ProjectStatus,
    PhaseStatus,
    TaskStatus,
)

def load_sample_data(db: Session):
    if db.query(Project).first():
        print("Sample data already exists, skipping...")
        return

    # 1️⃣ USERS
    users = [
        User(name="Arjun Mehta", email="arjun.mehta@company.com"),
        User(name="Priya Sharma", email="priya.sharma@company.com"),
        User(name="Rahul Verma", email="rahul.verma@company.com"),
        User(name="Neha Reddy", email="neha.reddy@company.com"),
        User(name="Varun Patel", email="varun.patel@company.com"),
        User(name="Divya Kaur", email="divya.kaur@company.com"),
        User(name="Karan Singh", email="karan.singh@company.com"),
        User(name="Ayesha Jain", email="ayesha.jain@company.com"),
        User(name="Rohan Deshmukh", email="rohan.deshmukh@company.com"),
    ]
    db.add_all(users)
    db.commit()

    arjun, priya, rahul, neha, varun, divya, karan, ayesha, rohan = users

    # 2️⃣ PROJECTS
    project1 = Project(
        name="Mall Construction",
        status=ProjectStatus.IN_PROGRESS,
        manager_id=arjun.id,
        start_date=date(2024, 1, 10),
        end_date=date(2025, 12, 31),
    )
    project2 = Project(
        name="Airport Expansion",
        status=ProjectStatus.NOT_STARTED,
        manager_id=neha.id,
        start_date=date(2024, 5, 1),
        end_date=date(2026, 5, 31),
    )
    project3 = Project(
        name="IT Tower Renovation",
        status=ProjectStatus.IN_PROGRESS,
        manager_id=karan.id,
        start_date=date(2023, 7, 1),
        end_date=date(2024, 9, 15),
    )
    db.add_all([project1, project2, project3])
    db.commit()

    # 3️⃣ PHASES
    phases = [
        # Project 1
        Phase(name="Foundation", status=PhaseStatus.COMPLETED, project_id=project1.id, phase_manager_id=priya.id),
        Phase(name="Structural Work", status=PhaseStatus.IN_PROGRESS, project_id=project1.id, phase_manager_id=rahul.id),
        Phase(name="Interiors", status=PhaseStatus.NOT_STARTED, project_id=project1.id, phase_manager_id=priya.id),
        # Project 2
        Phase(name="Planning", status=PhaseStatus.NOT_STARTED, project_id=project2.id, phase_manager_id=varun.id),
        Phase(name="Terminal Setup", status=PhaseStatus.NOT_STARTED, project_id=project2.id, phase_manager_id=divya.id),
        # Project 3
        Phase(name="Demolition", status=PhaseStatus.COMPLETED, project_id=project3.id, phase_manager_id=ayesha.id),
        Phase(name="Wiring & HVAC", status=PhaseStatus.IN_PROGRESS, project_id=project3.id, phase_manager_id=rohan.id),
    ]
    db.add_all(phases)
    db.commit()

    # 4️⃣ TASKS
    today = date(2025, 8, 7)
    tasks = [
        # Project 1 – Foundation
        Task(name="Lay foundation", status=TaskStatus.COMPLETED, estimated_budget=1_000_000, actual_budget=1_000_000, due_date=date(2024, 3, 10), phase_id=phases[0].id),
        Task(name="Waterproofing base", status=TaskStatus.COMPLETED, estimated_budget=500_000, actual_budget=500_000, due_date=date(2024, 4, 5), phase_id=phases[0].id),
        # Project 1 – Structural Work
        Task(name="Concrete frame setup", status=TaskStatus.IN_PROGRESS, estimated_budget=2_000_000, actual_budget=800_000, due_date=today + timedelta(days=3), phase_id=phases[1].id),
        Task(name="Beam testing", status=TaskStatus.NOT_STARTED, estimated_budget=800_000, actual_budget=0, due_date=today - timedelta(days=7), phase_id=phases[1].id),
        # Project 1 – Interiors
        Task(name="HVAC Layout", status=TaskStatus.NOT_STARTED, estimated_budget=1_200_000, actual_budget=0, due_date=today + timedelta(days=10), phase_id=phases[2].id),
        # Project 2 – Planning
        Task(name="Environmental clearance", status=TaskStatus.NOT_STARTED, estimated_budget=300_000, actual_budget=0, due_date=date(2024, 6, 1), phase_id=phases[3].id),
        # Project 2 – Terminal
        Task(name="Terminal blueprint", status=TaskStatus.NOT_STARTED, estimated_budget=900_000, actual_budget=0, due_date=date(2024, 7, 15), phase_id=phases[4].id),
        # Project 3 – Demolition
        Task(name="Office Demolition", status=TaskStatus.COMPLETED, estimated_budget=500_000, actual_budget=450_000, due_date=date(2023, 12, 1), phase_id=phases[5].id),
        # Project 3 – Wiring & HVAC
        Task(name="Wiring reinstallation", status=TaskStatus.IN_PROGRESS, estimated_budget=400_000, actual_budget=200_000, due_date=today + timedelta(days=7), phase_id=phases[6].id),
    ]
    db.add_all(tasks)
    db.commit()

    # 5️⃣ FINANCE
    finances = [
        FinanceRequest(project_id=project1.id, requested_amount=2_000_000, approved_amount=500_000, request_date=today),
        FinanceRequest(project_id=project2.id, requested_amount=5_000_000, approved_amount=0, request_date=date(2024, 5, 5)),
        FinanceRequest(project_id=project3.id, requested_amount=1_200_000, approved_amount=1_000_000, request_date=date(2024, 3, 12)),
    ]
    db.add_all(finances)
    db.commit()

    print("✅ Sample data for 3 projects loaded.")
