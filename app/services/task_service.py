from app.models.task import Task
from app.services.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func


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
