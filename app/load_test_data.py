from app.database import get_sync_db
from app.models.user import User
from app.models.task import Task
from app.enums.task_priority import TaskPriority
from app.enums.task_status import TaskStatus
import json
from sqlalchemy.orm import Session
from sqlalchemy import text


def reset_sequence(db: Session, table_name: str):
    """Reset the sequence for a table."""
    query = text(f"""
        SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), MAX(id))
        FROM {table_name};
    """)
    db.execute(query)
    db.commit()



def load_users(file_path: str, db):
    """Завантаження або оновлення користувачів із JSON-файлу в базу даних."""
    with open(file_path, "r") as file:
        users_data = json.load(file)

    for user_data in users_data:
        existing_user = db.query(User).filter_by(id=user_data["id"]).first()
        if existing_user:
            # Оновлення існуючого запису
            existing_user.name = user_data["name"]
            existing_user.max_tasks = user_data["max_tasks"]
            existing_user.password = user_data["password"]
            print(f"Оновлено користувача: {existing_user.name}")
        else:
            # Додавання нового запису
            new_user = User(
                id=user_data["id"],
                name=user_data["name"],
                max_tasks=user_data["max_tasks"],
                password=user_data["password"]
            )
            db.add(new_user)
            print(f"Додано нового користувача: {new_user.name}")

    db.commit()

    reset_sequence(db, "users")

    print(f"Оброблено {len(users_data)} користувачів.")


def load_tasks(file_path: str, db):
    """Завантаження або оновлення завдань із JSON-файлу в базу даних."""
    with open(file_path, "r") as file:
        tasks_data = json.load(file)

    for task_data in tasks_data:
        existing_task = db.query(Task).filter_by(id=task_data["id"]).first()
        if existing_task:
            # Оновлення існуючого запису
            existing_task.description = task_data["description"]
            existing_task.priority = TaskPriority[task_data["priority"]]
            existing_task.status = TaskStatus[task_data["status"]]
            existing_task.created_at = task_data["created_at"]
            existing_task.completed_at = task_data["completed_at"]
            existing_task.assigned_to = task_data["assigned_to"]
            print(f"Оновлено завдання: {existing_task.id}")
        else:
            # Додавання нового запису
            new_task = Task(
                id=task_data["id"],
                description=task_data["description"],
                priority=TaskPriority[task_data["priority"]],
                status=TaskStatus[task_data["status"]],
                created_at=task_data["created_at"],
                completed_at=task_data["completed_at"],
                assigned_to=task_data["assigned_to"]
            )
            db.add(new_task)
            print(f"Додано нове завдання: {new_task.id}")

    db.commit()

    reset_sequence(db, "tasks")
    
    print(f"Оброблено {len(tasks_data)} завдань.")



def main():
    users_file = "app/tests/users.json"
    tasks_file = "app/tests/tasks.json"

    db = next(get_sync_db())

    try:
        load_users(users_file, db)
        load_tasks(tasks_file, db)
    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
