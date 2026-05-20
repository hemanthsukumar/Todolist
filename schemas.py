import pydantic
from pydantic import BaseModel
from typing import Optional
from datetime import date

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: str = "Low"
    deadline: Optional[date] = None

class Task(TaskCreate):
    id: int
    completed: bool

    if getattr(pydantic, "VERSION", "").startswith("2"):
        model_config = {"from_attributes": True}
    else:
        class Config:
            orm_mode = True
