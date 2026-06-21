from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    assignee: str
    due_date: date
    status: str = "To Do"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class TaskOut(BaseModel):
    id: int
    project_id: int
    title: str
    assignee: str
    due_date: date
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}