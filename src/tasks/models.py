
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String

from src.database import Base
from src.tasks.schemas import TaskPriority, TaskStatus


class Task(Base):
  """SQLAlchemy ORM model for Task (Database)."""
  __tablename__ = "tasks"

  id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
  title = Column(String(255), nullable=False)
  description = Column(String(500), nullable=True)
  status = Column(SQLEnum(TaskStatus), default=TaskStatus.todo, nullable=False)
  priority = Column(SQLEnum(TaskPriority), default=TaskPriority.normal, nullable=False)
  is_done = Column(Boolean, default=False, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


  def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"