# # app/schemas.py — the data contract (part of Model)
# from pydantic import BaseModel

# class TaskCreate(BaseModel):
#     title: str

# class Task(TaskCreate):
#     id: int

from pydantic import BaseModel, ConfigDict, Field


# Remove owner_id — the server now takes it from the current user.
class TaskCreate(BaseModel):
   title:    str = Field(..., min_length=1, max_length=200)

class Task(BaseModel):
    id: int
    title: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


                                     # NEW 
  
  
class User(BaseModel): 
    id:   int 
    name: str 
    model_config = ConfigDict(from_attributes=True)    