
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Index, String, Uuid

from src.database import Base


class User(Base):
    """SQLAlchemy ORM Model for User"""
    __tablename__ = "users"
    

    id = Column(Uuid, primary_key=True, default=uuid4)
    email = Column(String(255), Unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


    # Indexes for common queries
    __table_args__ = (
        Index('idx_email', 'email')
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"