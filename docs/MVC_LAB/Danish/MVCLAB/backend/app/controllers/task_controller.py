from fastapi import APIRouter, HTTPException, Depends
from app.schemas import Task,  TaskCreate, User
from app.services.task_service import TaskService
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.task_repositories import TaskRepository
from app.services.task_service import TaskService
from app.schemas import Task, TaskCreate
from app.repositories.user_repositories import UserRepository
from app.auth.dependencies import get_current_user
from app.services.task_service import TaskService, TaskNotFoundError, NotAuthorizedError
router = APIRouter()
#service = TaskService()

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_task_repo(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)

def get_task_service(task_repo: TaskRepository = Depends(get_task_repo), user_repo: UserRepository = Depends(get_user_repo)) -> TaskService:
    return TaskService(task_repo, user_repo)

@router.get("/", response_model=list[Task])
def get_tasks(user: User = Depends(get_current_user), service: TaskService = Depends(get_task_service)):
    return service.list_tasks(user)

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, user: User = Depends(get_current_user), service: TaskService = Depends(get_task_service)):
    try:
        task = service.get_task(task_id, user)
        return task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    except NotAuthorizedError:
        raise HTTPException(status_code=403, detail="Not authorized to access this task") 

@router.post("/", response_model=Task, status_code=201)
def create_task(payload: TaskCreate, user: User = Depends(get_current_user), service: TaskService = Depends(get_task_service)):
    
    try:
        return service.create_task(payload.title, user)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, user: User = Depends(get_current_user), service: TaskService = Depends(get_task_service)):
    try:
        service.delete_task(task_id, user)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    except NotAuthorizedError:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
    