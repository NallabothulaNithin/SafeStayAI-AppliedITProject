# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database import get_db
# from app.repositories.task_repository import TaskRepository
# from app.schemas import Task, TaskCreate
# from app.services.task_service import TaskService, TaskNotFoundError

# router = APIRouter()

# # ---------------- OLD IMPLEMENTATION ----------------
# # from fastapi import APIRouter, HTTPException
# # from app.schemas import Task, TaskCreate
# # from app.services.task_service import TaskService
# #
# # router = APIRouter()
# # service = TaskService()
# #
# #
# # @router.get("/", response_model=list[Task])
# # def get_tasks():
# #     return service.list_tasks()
# #
# #
# # @router.get("/{task_id}", response_model=Task)
# # def get_task(task_id: int):
# #     task = service.get_task(task_id)
# #
# #     if task is None:
# #         raise HTTPException(status_code=404, detail="Task not found")
# #
# #     return task
# #
# #
# # @router.post("/", response_model=Task, status_code=201)
# # def create_task(payload: TaskCreate):
# #     return service.create_task(payload.title)
# #
# #
# # @router.delete("/{task_id}", status_code=204)
# # def delete_task(task_id: int):
# #     deleted = service.delete_task(task_id)
# #
# #     if not deleted:
# #         raise HTTPException(status_code=404, detail="Task not found")
# # ----------------------------------------------------


# # Dependency factories. FastAPI resolves the chain per request.
# def get_task_repo(db: Session = Depends(get_db)) -> TaskRepository:
#     return TaskRepository(db)


# def get_task_service(
#     repo: TaskRepository = Depends(get_task_repo),
# ) -> TaskService:
#     return TaskService(repo)


# @router.get("/", response_model=list[Task])
# def get_tasks(service: TaskService = Depends(get_task_service)):
#     return service.list_tasks()


# @router.get("/{task_id}", response_model=Task)
# def get_task(
#     task_id: int,
#     service: TaskService = Depends(get_task_service),
# ):
#     try:
#         return service.get_task(task_id)
#     except TaskNotFoundError:
#         raise HTTPException(status_code=404, detail="Task not found")


# @router.post("/", response_model=Task, status_code=201)
# def create_task(
#     payload: TaskCreate,
#     service: TaskService = Depends(get_task_service),
# ):
#     try:
#         return service.create_task(payload.title)
#     except ValueError as exc:
#         raise HTTPException(status_code=422, detail=str(exc))


# @router.delete("/{task_id}", status_code=204)
# def delete_task(
#     task_id: int,
#     service: TaskService = Depends(get_task_service),
# ):
#     if not service.delete_task(task_id):
#         raise HTTPException(status_code=404, detail="Task not found")
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas import Task, TaskCreate
from app.services.task_service import TaskService, TaskNotFoundError

router = APIRouter()


# Dependency factories. FastAPI resolves the chain per request.
def get_task_repo(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:   
    return UserRepository(db)

def get_task_service(tasks: TaskRepository = Depends(get_task_repo), users: UserRepository = Depends(get_user_repo)) -> TaskService:
    return TaskService(tasks, users)


@router.get("/", response_model=list[Task])
def get_tasks(service: TaskService = Depends(get_task_service)):
    return service.list_tasks()


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """Try service.get_task; map TaskNotFoundError -> HTTPException 404."""
    try:
        return service.get_task(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.post("/", response_model=Task, status_code=201)
def create_task(payload: TaskCreate, service: TaskService = Depends(get_task_service)):
    """Try service.create_task(payload.title); map ValueError -> HTTPException 422."""
    try:
        return service.create_task(payload.title, payload.owner_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """If service.delete_task returns False, raise HTTPException 404."""
    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")