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
from app.repositories.user_repository import UserRepository

class TaskNotFoundError(Exception):
    pass

class UserNotFoundError(Exception):
    pass
    
class TaskService:    
    def __init__(self, tasks: TaskRepository, users: UserRepository):
        self._tasks = tasks
        self._users = users
    
    def list_tasks(self):
        return self._tasks.all()
    # def create_task(self, title): return self._repo.add(title)
    
    def create_task(self, title: str, owner_id: int):
        """
        strip title; raise ValueError if empty.
        Look up the user; raise UserNotFoundError if missing.
        Delegate the insert to the repository.
        Hint: you'll need a way to find a User - add UserRepository
        or expose a method on TaskRepository.

        """
        ...
        if self._users.find(owner_id) is None:
            raise UserNotFoundError(owner_id)
        
        return self._tasks.add(title, owner_id)
    
    def delete_task(self, task_id):
        return self._tasks.remove(task_id)
    
    def get_task(self, task_id):
        task = self._tasks.find(task_id)
        if task is None:
            return TaskNotFoundError(task_id)
        return task