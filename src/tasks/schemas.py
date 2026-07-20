from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime


class TaskCreate(BaseModel):
    """Payload to create a new task."""
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    """All fields optional — only send what you want to change."""
    title: str | None = None
    description: str | None = None
    is_done: bool | None = None


class TaskResponse(BaseModel):
    """What the API returns to the client."""
    id: UUID
    title: str
    description: str | None
    is_done: bool
    created_at: datetime


class Task(BaseModel):
    """Internal task object stored in memory."""
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str | None = None
    is_done: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
