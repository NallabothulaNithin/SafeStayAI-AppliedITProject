from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task


class TaskRepository:
    def __init__(self, db: Session):
        self._db = db

    def all(self) -> list[Task]:
        return list(self._db.scalars(select(Task)))

    def find(self, task_id: int) -> Task | None:
        return self._db.get(Task, task_id)

    def add(self, title: str) -> Task:
        task = Task(title=title)
        self._db.add(task)
        self._db.commit()
        self._db.refresh(task)
        return task

    def remove(self, task_id: int) -> bool:
        task = self.find(task_id)

        if task is None:
            return False

        self._db.delete(task)
        self._db.commit()
        return True