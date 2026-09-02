from math import ceil
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from src.pagination import PaginatedTaskResponse
from src.tasks import service
from src.tasks.schemas import (TaskCreate, TaskPriority, TaskResponse,
                               TaskStatus, TaskUpdate)

router = APIRouter(prefix="/api/v1", tags=["Tasks"])


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    return service.create_task(payload)


@router.get("/tasks", response_model=PaginatedTaskResponse)
def get_all_tasks(
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    tasks, total_count = service.get_all_tasks(status=status, priority=priority, page=page, limit=limit)
    total_pages = ceil(total_count / limit) if total_count > 0 else 0
    
    return PaginatedTaskResponse(
        data=[TaskResponse.model_validate(t.model_dump()) for t in tasks],
        total=total_count,
        page=page,
        limit=limit,
        pages=total_pages
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID):
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: UUID, payload: TaskUpdate):
    task = service.update_task(task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID):
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
