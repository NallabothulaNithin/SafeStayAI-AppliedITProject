from fastapi import APIRouter, HTTPException
from app.schemas import Task, TaskCreate
from app. services. task_service import TaskService

router = APIRouter()
service = TaskService()

@router.get("/", response_model=list[Task])
def list_tasks():
    return service.list_tasks()

@router.post("/", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    return service.create_task(payload.title)

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")