# # app/schemas.py — the data contract (part of Model)
# from pydantic import BaseModel

# class TaskCreate(BaseModel):
#     title: str

# class Task(TaskCreate):
#     id: int

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


class Task(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
    # TODO: add the line that lets Pydantic read from ORM objects.
    # Hint: model_config = ConfigDict(from_attributes=True)