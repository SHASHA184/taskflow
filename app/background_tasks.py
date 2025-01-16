from app.celery_app import celery_app
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task import Task
from app.models.user import User
from app.database import get_sync_db
from app.enums.task_status import TaskStatus
from app.enums.task_priority import TaskPriority
from sqlalchemy.orm import Session
from app.utils import get_password_hash
from sqlalchemy.sql import func
import asyncio
from sqlalchemy.exc import IntegrityError

@celery_app.task(name="app.background_tasks.distribute_tasks")
def distribute_tasks():
    """Розподіл завдань між виконавцями з урахуванням пріоритету та завантаження."""
    db: Session = next(get_sync_db())  # Отримання синхронної сесії

    # Отримання завдань зі статусом "pending" за пріоритетом
    pending_tasks = db.query(Task).filter(
        Task.status == TaskStatus.PENDING
    ).order_by(Task.priority).all()

    # Підрахунок активних завдань для кожного виконавця
    task_count_subquery = (
        db.query(Task.assigned_to, func.count(Task.id).label("task_count"))
        .filter(Task.status == TaskStatus.IN_PROGRESS)
        .group_by(Task.assigned_to)
        .subquery()
    )

    for task in pending_tasks:
        # Пошук виконавця з найменшим завантаженням
        worker = (
            db.query(User)
            .outerjoin(task_count_subquery, User.id == task_count_subquery.c.assigned_to)
            .filter(
                (func.coalesce(task_count_subquery.c.task_count, 0) < User.max_tasks)
            )
            .order_by(func.coalesce(task_count_subquery.c.task_count, 0))  # Сортування за кількістю завдань
            .first()
        )

        if not worker:
            break  # Якщо немає доступних виконавців, залишаємо завдання в черзі

        # Призначення завдання виконавцю
        task.assigned_to = worker.id
        task.status = TaskStatus.IN_PROGRESS
        db.commit()

    # Якщо завдань > 10, додаємо нового виконавця
    if len(pending_tasks) > 10:
        add_new_worker(db)

    # Якщо завдань < 5, скорочуємо кількість виконавців до 2
    if len(pending_tasks) < 5:
        reduce_workers_to_two(db)

def add_new_worker(db):
    """Додає нового виконавця з унікальним іменем."""
    base_name = "Worker"
    count = 1
    while True:
        new_worker_name = f"{base_name}_{count}"
        existing_worker = db.query(User).filter(User.name == new_worker_name).first()
        if not existing_worker:
            try:
                new_worker = User(
                    name=new_worker_name,
                    max_tasks=5,
                    password=get_password_hash("default_password"),
                )
                db.add(new_worker)
                db.commit()
                break
            except IntegrityError:
                db.rollback()
        count += 1

def reduce_workers_to_two(db):
    """Зменшує кількість виконавців до двох."""
    workers = db.query(User).all()
    if len(workers) > 2:
        for worker in workers[2:]:
            db.delete(worker)
        db.commit()
