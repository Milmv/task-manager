from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from models import StatusEnum, PriorityEnum


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    status: Optional[StatusEnum] = StatusEnum.waiting
    priority: Optional[PriorityEnum] = PriorityEnum.medium


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum
    priority: PriorityEnum
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
