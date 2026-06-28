from fastapi import APIRouter, HTTPException, Depends
from app.schemas import Task, TaskCreate
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService, TaskNotFoundError
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user_repository import UserRepository

router = APIRouter()
 
 
def get_task_repo(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)
 
def get_task_service(tasks: TaskRepository = Depends(get_task_repo), users: UserRepository = Depends(get_user_repo)) -> TaskService:
    return TaskService(tasks, users)
 
# GET tasks
@router.get("/", response_model=list[Task])
def get_tasks(service: TaskService = Depends(get_task_service)) -> list[dict]:
    return service.list_tasks()
 
# POST tasks
@router.post("/", response_model=Task, status_code=201)
def create_task(payload: TaskCreate, service: TaskService = Depends(get_task_service)):
    return service.create_task(payload.title,payload.owner_id)
 
# GET /tasks/{task_id}
@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)) -> Task:
    try:
        return service.get_task(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
 
# DELETE /tasks/{task_id}
@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    try:
        service.delete_task(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
 