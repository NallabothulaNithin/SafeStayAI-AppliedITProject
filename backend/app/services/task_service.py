# from app.repositories.task_repository import TaskRepository


# class TaskService:
#     def __init__(self, repo: TaskRepository):
#         self._repo = repo

#     # ---------------- OLD IMPLEMENTATION ----------------
#     # def __init__(self):
#     #     self._tasks = [
#     #         {"id": 1, "title": "Learn MVC"},
#     #         {"id": 2, "title": "Build Docker app"},
#     #     ]
#     #     self._next_id = 3
#     #
#     # def list_tasks(self):
#     #     return self._tasks
#     #
#     # def get_task(self, task_id: int):
#     #     for task in self._tasks:
#     #         if task["id"] == task_id:
#     #             return task
#     #     return None
#     #
#     # def create_task(self, title: str):
#     #     task = {
#     #         "id": self._next_id,
#     #         "title": title
#     #     }
#     #     self._tasks.append(task)
#     #     self._next_id += 1
#     #     return task
#     #
#     # def delete_task(self, task_id: int):
#     #     for task in self._tasks:
#     #         if task["id"] == task_id:
#     #             self._tasks.remove(task)
#     #             return True
#     #     return False
#     # ----------------------------------------------------

#     def list_tasks(self):
#         return self._repo.all()

#     def get_task(self, task_id: int):
#         return self._repo.find(task_id)

#     def create_task(self, title: str):
#         title = title.strip()

#         if not title:
#             raise ValueError("Title cannot be empty")

#         return self._repo.add(title)

#     def delete_task(self, task_id: int):
#         return self._repo.remove(task_id)

from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository

class UserNotFoundError(Exception):
    ...
class TaskNotFoundError(Exception):
    ...


class TaskService:
    def __init__(self, tasks: TaskRepository, users: UserRepository):
        self._tasks = tasks
        self._users = users

    def list_tasks(self):
        return self._tasks.all()

    def get_task(self, task_id: int):
        task = self._tasks.find(task_id)

        if task is None:
            raise TaskNotFoundError()

        return task

    def create_task(self, title: str, owner_id: int):
        # Check if the user exists
        user = self._users.find(owner_id)
        if user is None:
            raise UserNotFoundError()

        title = title.strip()

        if not title:
            raise ValueError("Title cannot be empty")

        return self._tasks.add(title, owner_id)

    def delete_task(self, task_id: int) -> bool:
        return self._tasks.remove(task_id)