# import sqlite3

# class TaskRepository:
#     def __init__(self, db_path= "tasks.db"):
#         self._db = db_path
#         self._init()

#     def _init(self):
#         with sqlite3.connect(self._db) as c:
#             c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")

#     def all(self):
#         with sqlite3.connect(self._db) as c:
#             rows = c.execute("SELECT id, title FROM tasks").fetchall()
#             return [{"id": r[0], "title": r[1]} for r in rows]
        
#     def add(self, title):
#         with sqlite3.connect(self._db) as c:
#             cur = c.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
#             return {"id": cur.lastrowid, "title": title}
        
#     def remove(self, task_id):
#         with sqlite3.connect(self._db) as c:
#             cur = c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
#             return cur.rowcount > 0

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Task

class TaskRepository:
    def __init__(self, db: Session):
        self._db = db

    def all(self) -> list[Task]:
        return list(self._db.scalars(select(Task)))
    
    def find(self, task_id: int) -> Task:
        return self._db.get(Task, task_id)
    
    def add(self, title: str, owner_id: int) -> Task:
        task = Task(title=title, owner_id=owner_id)
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