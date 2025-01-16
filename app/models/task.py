from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Index
from app.database import Base
from app.enums.task_priority import TaskPriority
from app.enums.task_status import TaskStatus

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        Index("idx_tasks_priority_status", "priority", "status"),
    )