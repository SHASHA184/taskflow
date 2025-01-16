from app.database import get_sync_db
from app.models.user import User
from app.models.task import Task
from app.enums.task_priority import TaskPriority
from app.enums.task_status import TaskStatus
import json


def load_users(file_path: str, db):
    """Завантаження користувачів із JSON-файлу в базу даних."""
    with open(file_path, "r") as file:
        users_data = json.load(file)

    for user_data in users_data:
        user = User(
            id=user_data["id"],
            name=user_data["name"],
            max_tasks=user_data["max_tasks"],
            password=user_data["password"],
        )
        db.add(user)
    db.commit()
    print(f"Додано {len(users_data)} користувачів до бази даних.")


def load_tasks(file_path: str, db):
    """Завантаження завдань із JSON-файлу в базу даних."""
    with open(file_path, "r") as file:
        tasks_data = json.load(file)

    for task_data in tasks_data:
        task = Task(
            id=task_data["id"],
            description=task_data["description"],
            priority=TaskPriority[task_data["priority"]],
            status=TaskStatus[task_data["status"]],
            created_at=task_data["created_at"],
            completed_at=task_data["completed_at"],
            assigned_to=task_data["assigned_to"],
        )
        db.add(task)
    db.commit()
    print(f"Додано {len(tasks_data)} завдань до бази даних.")


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
