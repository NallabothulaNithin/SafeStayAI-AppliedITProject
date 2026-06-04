# class TaskService:
#     def __init__(self):
#         self.tasks = [
#             {"id": 1, "title": "Learn MVC"},
#             {"id": 2, "title": "Build Docker app"}
#         ]
#         self.next_id = 3

#     def list_tasks(self):
#         return self.tasks

#     def create_task(self, title: str):
#         task = {
#             "id": self.next_id,
#             "title": title
#         }
#         self.tasks.append(task)
#         self.next_id += 1
#         return task

#     def get_task(self, task_id: int):
#         for task in self.tasks:
#             if task["id"] == task_id:
#                 return task
#         return None

#     def delete_task(self, task_id: int):
#         for task in self.tasks:
#             if task["id"] == task_id:
#                 self.tasks.remove(task)
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