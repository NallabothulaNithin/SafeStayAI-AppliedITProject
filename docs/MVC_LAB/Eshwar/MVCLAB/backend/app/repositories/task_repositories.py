# import sqlite3
# from sqlalchemy import select
# from sqlalchemy.orm import Session

# from app.models import Task

# class TaskRepository:
#     def __init__(self, db_path= "tasks.db"):
#         self._db = db_path
#         self._init_db()

#     def _init_db(self):
#          with sqlite3.connect(self._db) as c:
#              c.execute("""
#                        CREATE TABLE IF NOT EXISTS tasks (
#                        id INTEGER PRIMARY KEY, 
#                        title TEXT NOT NULL
#                        )""")

#     def all(self):
#         with sqlite3.connect(self._db) as c:
#             rows = c.execute("SELECT id, title FROM tasks").fetchall()
#             return [{"id": r[0], "title": r[1]} for r in rows]

#     def find(self, task_id: int) -> Task | None:
#         pass    
        
#     def add(self, title):
#         with sqlite3.connect(self._db) as c:
#             cur = c.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
#             return {"id": cur.lastrowid, "title": title}
        
#     def remove(self, task_id):
#         with sqlite3.connect(self._db) as c:
#             cur = c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
#             return cur.rowcount > 0


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
        
    def add(self, title: str, owner_id: int) -> Task:
        new_task = Task(title=title, owner_id=owner_id) 
        self._db.add(new_task)
        self._db.commit()
        self._db.refresh(new_task)
        return new_task
    
    def remove(self, task_id: int) -> bool:
        task = self._db.get(Task, task_id)
        if not task:
            return False
        self._db.delete(task)
        self._db.commit()
        return True
    
    def all_for_user(self, owner_id: int) -> list[Task]:
        return list(
            self._db.scalars(
                select(Task).where(Task.owner_id == owner_id)
            )
        )
        

    def all_for_user(self, owner_id: int) -> list[Task]:
        return list(
            self._db.scalars(
                select(Task).where(Task.owner_id == owner_id)
            )
        )    