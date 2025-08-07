from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

# ----------------------------------------------------
# ✅ ENUMS
# ----------------------------------------------------
class ProjectStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class PhaseStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

# ----------------------------------------------------
# ✅ USER (Manager, Phase Manager, etc.)
# ----------------------------------------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)

# ----------------------------------------------------
# ✅ PROJECT
# ----------------------------------------------------
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(Enum(ProjectStatus))
    manager_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    # Relationships
    manager = relationship("User", foreign_keys=[manager_id])
    phases = relationship("Phase", back_populates="project")
    finance_requests = relationship("FinanceRequest", back_populates="project")

# ----------------------------------------------------
# ✅ PHASE
# ----------------------------------------------------
class Phase(Base):
    __tablename__ = "phases"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(Enum(PhaseStatus))
    project_id = Column(Integer, ForeignKey("projects.id"))

    phase_manager_id = Column(Integer, ForeignKey("users.id"))
    assistant_manager_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    project = relationship("Project", back_populates="phases")
    tasks = relationship("Task", back_populates="phase")

    phase_manager = relationship("User", foreign_keys=[phase_manager_id])
    assistant_manager = relationship("User", foreign_keys=[assistant_manager_id])

# ----------------------------------------------------
# ✅ TASK
# ----------------------------------------------------
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(Enum(TaskStatus))
    estimated_budget = Column(BigInteger)
    actual_budget = Column(BigInteger)
    due_date = Column(Date)
    phase_id = Column(Integer, ForeignKey("phases.id"))

    # Relationships
    phase = relationship("Phase", back_populates="tasks")

# ----------------------------------------------------
# ✅ FINANCE REQUEST
# ----------------------------------------------------
class FinanceRequest(Base):
    __tablename__ = "finance_requests"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    requested_amount = Column(BigInteger)
    approved_amount = Column(BigInteger)
    request_date = Column(Date)

    project = relationship("Project", back_populates="finance_requests")

# ----------------------------------------------------
# ✅ WEEKLY REPORT
# ----------------------------------------------------
class WeeklyReport(Base):
    __tablename__ = "weekly_reports"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    summary_text = Column(String)
    report_date = Column(Date)

    # Relationship
    project = relationship("Project", backref="weekly_reports")
