# class TaskService:
#     def __init__(self):
#         self._tasks = [
#             {"id": 1, "title": "Learn MVC"},
#             {"id": 2, "title": "Build Docker app"}
#         ]
#     def list_tasks(self):
#         return self._tasks
 
#     def create_task(self, title: str):
#         new_id = max(task["id"] for task in self._tasks) + 1 if self._tasks else 1
#         new_task = {"id": new_id, "title": title}
#         self.tasks.append(_tasks)
#         return new_task
       
#     def get_task(self, task_id: int):
#         for task in self._tasks:
#             if task["id"] == task_id:
#                 return task
#         return None
 
#     def delete_task(self, task_id: int):
#         for i, task in enumerate(self._tasks):
#             if task["id"] == task_id:
#                 del self._tasks[i]
#                 return True
#         return False
 

from app.repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self, repo=None):
        self._repo = repo or TaskRepository()
    
    def list_tasks(self):
        return self._repo.all()
    def create_task(self, title):
        return self._repo.add(title)
    def delete_task(self, task_id):
        return self._repo.remove(task_id)
    