from math import ceil
from typing import Optional, cast
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.pagination import PaginatedTaskResponse
from src.tasks import service
from src.tasks.dependencies import FilterParams, get_db
from src.tasks.schemas import (TaskCreate, TaskPriority, TaskResponse,
                               TaskStatus, TaskUpdate)

router = APIRouter(prefix="/api/v1", tags=["Tasks"])


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    return service.create_task(db, payload)


@router.get("/tasks", response_model=PaginatedTaskResponse)
def get_all_tasks(
    filters: FilterParams = Depends(), 
    db: Session = Depends(get_db)
):
    """Get paginated tasks with optional filtering."""
    tasks, total_count = service.get_all_tasks(
        db,
        status=filters.status,
        priority=filters.priority,
        page=filters.page,
        limit=filters.limit
    )
    
    total_pages = ceil(total_count / filters.limit) if total_count > 0 else 0
    
    return PaginatedTaskResponse(
        data=cast(list[TaskResponse], tasks),
        total=total_count,
        page=filters.page,
        limit=filters.limit,
        pages=total_pages
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    task = service.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: UUID, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = service.update_task(db, task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    deleted = service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
