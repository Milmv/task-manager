from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from datetime import datetime, timezone
import enum
from database import Base


class StatusEnum(str, enum.Enum):
    waiting = "в ожидании"
    in_progress = "в работе"
    completed = "завершено"


class PriorityEnum(str, enum.Enum):
    low = "низкий"
    medium = "средний"
    high = "высокий"
    urgent = "срочный"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String, default="")
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.waiting)
    priority = Column(SQLEnum(PriorityEnum), default=PriorityEnum.medium)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))