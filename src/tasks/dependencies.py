
from typing import Generator, Optional

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.tasks.schemas import TaskPriority, TaskStatus


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class FilterParams:
    """Pagination and filter parameters."""
    def __init__(
        self,
        status: Optional[TaskStatus] = Query(None),
        priority: Optional[TaskPriority] = Query(None),
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100)
    ):
        self.status = status
        self.priority = priority
        self.page = page
        self.limit = limit