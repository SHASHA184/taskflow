from pydantic import BaseModel
from app.enums.task_status import TaskStatus
from app.enums.task_priority import TaskPriority
from datetime import datetime


class TaskCreate(BaseModel):
    description: str
    priority: TaskPriority


class TaskUpdate(BaseModel):
    status: TaskStatus


class TaskInDB(TaskCreate):
    id: int
    status: TaskStatus
    created_at: datetime
    completed_at: datetime
    assigned_to: int

    class Config:
        orm_mode = True