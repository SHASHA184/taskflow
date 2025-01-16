from app.models.task import Task
from app.services.base_service import BaseService

class TaskService(BaseService):
    def __init__(self, db):
        super().__init__(db, Task)