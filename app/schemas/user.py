from pydantic import BaseModel
from typing import List
from app.schemas.task import TaskInDB

class UserCreate(BaseModel):
    name: str
    max_tasks: int
    password: str


class UserUpdate(BaseModel):
    max_tasks: int


class UserInDB(UserCreate):
    id: int

    class Config:
        from_attributes = True

class UserWithTasks(BaseModel):
    id: int
    name: str
    max_tasks: int
    tasks: List[TaskInDB]
