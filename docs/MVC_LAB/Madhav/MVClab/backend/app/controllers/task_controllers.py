from fastapi import APIRouter, HTTPException, Depends
from app.schemas import Task, TaskCreate, User
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService, TaskNotFoundError, UserNotFoundError
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.auth.dependencies import get_current_user
from app.services.task_service import TaskService, TaskNotFoundError, NotAuthorizedError

router = APIRouter()
 
 
def get_task_repo(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)
 
def get_task_service(tasks: TaskRepository = Depends(get_task_repo), users: UserRepository = Depends(get_user_repo)) -> TaskService:
    return TaskService(tasks, users)
 
# GET tasks
@router.get("/", response_model=list[Task])
def get_tasks(user: User = Depends(get_current_user), 
              service: TaskService = Depends(get_task_service)):
    return service.list_tasks(user)
 
# POST tasks
@router.post("/", response_model=Task, status_code=201)
def create_task(payload: TaskCreate, user: User = Depends(get_current_user), 
                service: TaskService = Depends(get_task_service)):
    try:
        return service.create_task(payload.title, user)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
 
# GET /tasks/{task_id}
@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, user: User = Depends(get_current_user), 
             service: TaskService = Depends(get_task_service), current_user: User = Depends(get_current_user)) -> Task:
    try:
        return service.get_task(task_id, current_user)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
 
# DELETE /tasks/{task_id}
@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, user: User = Depends(get_current_user), 
                service: TaskService = Depends(get_task_service), current_user: User = Depends(get_current_user)):
    try:
        service.delete_task(task_id, current_user)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
 