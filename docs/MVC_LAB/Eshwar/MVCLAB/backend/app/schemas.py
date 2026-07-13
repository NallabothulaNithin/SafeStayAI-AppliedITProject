from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    password: str = Field(..., min_length=6, max_length=200)

class User(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    # owner_id: int

class Task(TaskCreate):
    id: int 
    owner: User   
    model_config = ConfigDict(from_attributes=True)

  