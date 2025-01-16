from app.models.task import Task
from app.services.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import datetime
from app.enums.task_status import TaskStatus


class TaskService(BaseService):
    def __init__(self, db):
        super().__init__(db, Task)

    async def get_my_tasks(self, user_id: int):
        """Get all tasks assigned to a user."""
        query = select(Task).filter(Task.assigned_to == user_id)
        tasks = await self.db.execute(query)
        return tasks.scalars().all()

    async def count_tasks_by_status(self):
        """Count tasks by their status."""
        query = select(Task.status, func.count(Task.id).label("count")).group_by(
            Task.status
        )
        result = await self.db.execute(query)
        return dict(result.all())

    async def get_task_details(self, task_id: int):
        """Get detailed information about a task."""
        task = await self.get(task_id)
        return task

    async def update(self, id, obj):
        print(obj)
        print(obj.status == TaskStatus.COMPLETED)
        if obj.status == TaskStatus.COMPLETED:
            await self.update_task_completion_date(id)
        return await super().update(id, obj)

    async def update_task_completion_date(self, id):
        query = select(Task).filter(Task.id == id)
        task = await self.db.execute(query)
        task = task.scalars().first()
        task.completed_at = datetime.now()
        await self.db.commit()
        return task
