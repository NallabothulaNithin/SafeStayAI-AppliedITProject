import sqlite3

class TaskRepository:
    def __init__(self, db_path= "tasks.db"):
        self._db = db_path
        self._init()

    def _init(self):
        with sqlite3.connect(self._db) as c:
            c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")

    def all(self):
        with sqlite3.connect(self._db) as c:
            rows = c.execute("SELECT id, title FROM tasks").fetchall()
            return [{"id": r[0], "title": r[1]} for r in rows]
        
    def add(self, title):
        with sqlite3.connect(self._db) as c:
            cur = c.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            return {"id": cur.lastrowid, "title": title}
        
    def remove(self, task_id):
        with sqlite3.connect(self._db) as c:
            cur = c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cur.rowcount > 0    