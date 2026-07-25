  
from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy import select 
from sqlalchemy.orm import Session 
  
from app.database import get_db 
from app.models import User 
from app.schemas import Task as TaskSchema, User as UserSchema 
from app.auth.dependencies import get_current_user
  
router = APIRouter() 
  
  
@router.get("/", response_model=list[UserSchema]) 
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)): 
    """Return all users. 
    Hint: list(db.scalars(select(User))) 
    """ 
    return list(db.scalars(select(User))) 
  
  
@router.get("/{user_id}/tasks", response_model=list[TaskSchema]) 
def list_user_tasks(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)): 
    """Fetch the user (404 if missing); return user.tasks.""" 

    user = db.get(User, user_id) 
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found") 
    return user.tasks
