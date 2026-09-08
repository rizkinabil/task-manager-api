
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Index, String, Uuid
from sqlalchemy.orm import relationship

from src.database import Base
from src.tasks.schemas import TaskPriority, TaskStatus


class Task(Base):
  """SQLAlchemy ORM model for Task (Database)."""
  __tablename__ = "tasks"

  id = Column(Uuid, primary_key=True, default=lambda: str(uuid4()))
  owner_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
  title = Column(String(255), nullable=False)
  description = Column(String(500), nullable=True)
  status = Column(SQLEnum(TaskStatus), default=TaskStatus.todo, nullable=False)
  priority = Column(SQLEnum(TaskPriority), default=TaskPriority.normal, nullable=False)
  is_done = Column(Boolean, default=False, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

  # Relationship to User (optional, for ORM convenience)
  owner = relationship("User", backref="tasks")

  # Indexes for common queries
  __table_args__ = (
      Index('idx_owner_id', 'owner_id'),
      Index('idx_owner_status', 'owner_id', 'status'),
  )


  def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, owner_id={self.owner_id})>"