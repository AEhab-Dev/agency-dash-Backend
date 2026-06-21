from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional


class ProjectCreate(BaseModel):
    name: str
    client_name: str
    deadline: date
    status: str = "Active"


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    client_name: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    name: str
    client_name: str
    deadline: date
    status: str
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}