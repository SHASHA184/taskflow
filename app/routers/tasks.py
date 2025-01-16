from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import TaskCreate, TaskUpdate, TaskInDB
from app.services.task_service import TaskService
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from typing import List

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("/tasks", response_model=TaskInDB)
async def create_task(task_create: TaskCreate, db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    task = await task_service.create(task_create)
    return task


@router.patch("/tasks/{id}", response_model=TaskInDB)
async def update_task(
    id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.get(id)
    assigned_user = task.assigned_to
    if assigned_user != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only update your own tasks"
        )
    task = await task_service.update(id, task_update)
    return task


@router.get("/tasks/", response_model=List[TaskInDB])
async def read_my_tasks(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    task_service = TaskService(db)
    tasks = await task_service.get_my_tasks(current_user.id)
    return tasks


@router.get("/tasks/count", response_model=dict)
async def count_tasks_by_status(db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    counts = await task_service.count_tasks_by_status()
    return counts


@router.get("/tasks/{id}/details", response_model=TaskInDB)
async def get_task_details(id: int, db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    task = await task_service.get_task_details(id)
    return task
