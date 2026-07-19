from app.models import User
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository


class UserNotFoundError(Exception):
    ...


class TaskNotFoundError(Exception):
    ...


class NotAuthorizedError(Exception):
    ...


class TaskService:
    def __init__(self, tasks: TaskRepository, users: UserRepository):
        self._tasks = tasks
        self._users = users

    def list_tasks(self, current_user: User):
        """Return only tasks owned by current_user."""
        return self._tasks.all_for_user(current_user.id)

    def get_task(self, task_id: int, current_user: User):
        """Return the task; raise TaskNotFoundError if missing,
        NotAuthorizedError if owned by someone else."""
        task = self._tasks.find(task_id)

        if task is None:
            raise TaskNotFoundError()

        if task.owner_id != current_user.id:
            raise NotAuthorizedError()

        return task

    def create_task(self, title: str, current_user: User):
        """Strip title; raise ValueError if empty; create the task
        with owner_id = current_user.id."""
        title = title.strip()

        if not title:
            raise ValueError("Title cannot be empty")

        return self._tasks.add(title, current_user.id)

    def delete_task(self, task_id: int, current_user: User) -> None:
        """Raise TaskNotFoundError if missing, NotAuthorizedError if
        not owned by current_user. Otherwise delete."""
        task = self._tasks.find(task_id)

        if task is None:
            raise TaskNotFoundError()

        if task.owner_id != current_user.id:
            raise NotAuthorizedError()

        self._tasks.remove(task_id)
