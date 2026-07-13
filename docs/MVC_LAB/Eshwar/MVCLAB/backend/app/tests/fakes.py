from app.models import Task, User

class FakeTaskRepository:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def all_for_user(self, owner_id: int) -> list[Task]:
        return [task for task in self._tasks if task.owner_id == owner_id]

    def find(self, task_id: int) -> Task | None:
        return next((task for task in self._tasks if task.id == task_id), None)

    def add(self, title: str, owner_id: int) -> Task:
        task = Task(id=self._next_id, title=title, owner_id=owner_id)
        self._next_id += 1
        self._tasks.append(task)
        return task

    def remove(self, task_id: int) -> bool:
        task = self.find(task_id)
        if task is None:
            return False
        self._tasks.remove(task)
        return True

class FakeUserRepository:
    def __init__(self, users: list[User] | None = None):
        self._users = {user.id: user for user in (users or [])}

    def find(self, user_id: int) -> User | None:
        return self._users.get(user_id)      