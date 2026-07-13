# # class TaskService:
# #     def __init__(self):
# #         self.tasks = [
# #             {"id": 1, "title": "Learn MVC"},
# #             {"id": 2, "title": "Build Docker app"}
# #         ]
# #         self.next_id = 3
 
# #     def list_tasks(self):
# #         return self.tasks
 
# #     def create_task(self, title: str):
# #         task = {
# #             "id": self.next_id,
# #             "title": title
# #         }
# #         self.tasks.append(task)
# #         self.next_id += 1
# #         return task
 
# #     def get_task(self, task_id: int):
# #         for task in self.tasks:
# #             if task["id"] == task_id:
# #                 return task
# #         return None
 
# #     def delete_task(self, task_id: int):
# #         for task in self.tasks:
# #             if task["id"] == task_id:
# #                 self.tasks.remove(task)
# #                 return True
# #         return False
# from app.repositories.task_repository import TaskRepository
# class TaskService:
#     def __init__(self, repo=None):
#         self._repo = repo or TaskRepository()
 
#     def list_tasks(self):
#         return self._repo.all()
 
#     def create_task(self, title):
#         return self._repo.add(title)
 
#     def delete_task(self, task_id):
#         return self._repo.remove(task_id)    
    
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.models import Task, User
 
class TaskNotFoundError(Exception):
    pass
 
class NotAuthorizedError(Exception):
    pass
 
class UserNotFoundError(Exception):
    pass
 
class TaskService:
    def __init__(self, tasks, users):
        self._tasks = tasks
        self._users = users
 
    def list_tasks(self, current_user: User):
        return self._tasks.all_for_user(current_user.id)
 
    # def create_task(self, title): return self._repo.add(title)
    
    def get_task(self, task_id: int, current_user: User):
        task = self._tasks.find(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        if task.owner_id != current_user.id:
            raise TaskNotFoundError(task_id)
        return task
 
    def create_task(self, title: str, current_user: User):
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty")
        task = Task(title=title, owner_id=current_user.id)
         
        return self._tasks.add(title=title, owner_id=current_user.id)
 
    def delete_task(self, task_id: int, current_user: User) -> None:
        task = self.get_task(task_id, current_user)
        if task is None:
            raise TaskNotFoundError(task_id)
        if task.owner_id != current_user.id:
            raise TaskNotFoundError(task_id)
        return self._tasks.remove(task.id)