# 
from sqlalchemy.orm import Session
from sqlalchemy import select
 
from app.models import Task
 
class TaskRepository:
    def __init__(self, db: Session):
        self._db = db
 
    def all(self) -> list[Task]:
        return list(self._db.scalars(select(Task)))
    
    def find(self, task_id: int):
        return (
            self._db.query(Task)
            .filter(Task.id == task_id)
            .first()
        )
    
    def add(self, title: str, owner_id: int) -> Task:
        task = Task(title=title, owner_id=owner_id)
        self._db.add(task)
        self._db.commit()
        self._db.refresh(task)
        return task
    
    def remove(self, task_id: int):
        task = self.find(task_id)
        if task is None:
            return None
        self._db.delete(task)
        self._db.commit()
        return True
    
    def all_for_user(self, owner_id: int) -> list[Task]:
        return list(self._db.scalars(select(Task).where(Task.owner_id == owner_id)))