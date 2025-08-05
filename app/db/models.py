from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

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

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(Enum(ProjectStatus))
    manager = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    phases = relationship("Phase", back_populates="project")

class Phase(Base):
    __tablename__ = "phases"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(Enum(PhaseStatus))
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="phases")
    tasks = relationship("Task", back_populates="phase")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(Enum(TaskStatus))
    estimated_budget = Column(BigInteger)
    actual_budget = Column(BigInteger)
    phase_id = Column(Integer, ForeignKey("phases.id"))
    phase = relationship("Phase", back_populates="tasks")

