from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    done = 'done'


class TaskPriority(str, Enum):
    low = 'low'
    normal = 'normal'
    high = 'high'


class TaskBase(BaseModel):
    """Shared fields across all task schemas."""
    title: str
    description: str | None = None


class TaskProgress(TaskBase):
    """Extends TaskBase with priority and status."""
    priority: TaskPriority | None = TaskPriority.normal
    status: TaskStatus | None = TaskStatus.todo


class TaskCreate(TaskProgress):
    """Payload to create a new task."""
    pass


class TaskUpdate(BaseModel):
    """All fields optional — only send what you want to change."""
    title: str | None = None
    description: str | None = None
    priority: TaskPriority | None = None
    status: TaskStatus | None = None
    is_done: bool | None = None


class TaskResponse(TaskProgress):
    """What the API returns to the client."""
    id: UUID
    is_done: bool
    created_at: datetime


class Task(TaskProgress):
    """Internal task object stored in memory."""
    id: UUID = Field(default_factory=uuid4)
    is_done: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
