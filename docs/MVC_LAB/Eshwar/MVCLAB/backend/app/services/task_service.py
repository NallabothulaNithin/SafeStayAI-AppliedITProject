# class TaskService:
#     def __init__(self):
#         self.tasks = [
#             {"id": 1, "title": "Learn MVC"},
#             {"id": 2, "title": "Build Docker App"},     
#         ]

#     def list_tasks(self):
#         return self.tasks   


#     def create_task(self, title: str):
#         new_id = max(task["id"] for task in self.tasks) + 1 if self.tasks else 1
#         new_task = {"id": new_id, "title": title}
#         self.tasks.append(new_task)
#         return new_task 
    
#     def get_task(self, task_id: int):
#         for task in self.tasks:
#             if task["id"] == task_id:
#                 return task
#         return None
    
#     def delete_task(self, task_id: int):
#         for i, task in enumerate(self.tasks):
#             if task["id"] == task_id:
#                 del self.tasks[i]
#                 return True
#         return False


from app.repositories.task_repositories import TaskRepository
from app.repositories.user_repositories import UserRepository
from app.models import Task, User



class TaskNotFoundError(Exception):
    pass
class UserNotFoundError(Exception):
    pass
class NotAuthorizedError(Exception):
    pass

class TaskService:
    def __init__(self, tasks, users):
        # print("INIT CALLED")
        # self._repo = repo or TaskRepository()
        # self.get_tasks = tasks
        # self._users = users
        self._tasks = tasks
        self._users = users
        self._repo = tasks

    def list_tasks(self, current_user: User):
        return self._tasks.all_for_user(current_user.id)

    def create_task(self, title: str, current_user: User):
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty or whitespace")
        return self._tasks.add(title, current_user.id)

    def delete_task(self, task_id: int, current_user: User) -> None:
        task = self._tasks.find(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        if task.owner_id != current_user.id:
            raise NotAuthorizedError()
        self._tasks.remove(task_id)

    def get_task(self, task_id: int, current_user: User):
        task = self._repo.find(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        if task.owner_id != current_user.id:
            raise NotAuthorizedError()
        return task
    
    




    """ Strip title; raise ValueError if Empty.
    Look up the user; raise UserNotFoundError if not found."""

