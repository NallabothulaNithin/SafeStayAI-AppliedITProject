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

class TaskService:
    def __init__(self, repo=None):
        print("INIT CALLED")
        self._repo = repo or TaskRepository()

    def list_tasks(self):
        return self._repo.all()

    def create_task(self, title):
        return self._repo.add(title)

    def delete_task(self, task_id):
        return self._repo.remove(task_id)


