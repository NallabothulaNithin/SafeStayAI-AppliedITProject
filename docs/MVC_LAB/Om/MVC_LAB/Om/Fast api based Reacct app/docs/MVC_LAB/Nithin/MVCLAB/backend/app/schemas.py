from pydantic import BaseModel, Field, ConfigDict

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    owner_id: int

class Task(TaskCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    owner_id: int

class User(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)        