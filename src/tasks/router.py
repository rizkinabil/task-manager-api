from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.tasks import service
from src.tasks.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api/v1", tags=["Tasks"])


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    return service.create_task(payload)


@router.get("/tasks", response_model=list[TaskResponse])
def get_all_tasks():
    return service.get_all_tasks()


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
