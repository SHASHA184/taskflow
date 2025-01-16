from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import TaskCreate, TaskUpdate, TaskInDB
from app.services.task_service import TaskService
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User

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
