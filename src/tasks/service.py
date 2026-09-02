from uuid import UUID

from src.tasks.schemas import (Task, TaskCreate, TaskPriority, TaskStatus,
                               TaskUpdate)

# In-memory store — will be replaced with a real DB in Stage 3
_tasks_db: dict[str, Task] = {}


def create_task(payload: TaskCreate) -> Task:
    task = Task(**payload.model_dump())
    _tasks_db[str(task.id)] = task
    return task


def get_all_tasks(
        status: TaskStatus | None = None, 
        priority: TaskPriority | None = None,
        page: int = 1,
        limit: int = 10
) -> tuple[list[Task], int]:
    """
    Returns paginated and filtered tasks with total count.
    
    Args:
        status: Optional status filter
        priority: Optional priority filter
        page: Page number (default 1)
        limit: Items per page (default 10)
    
    Returns:
        Tuple of (paginated_tasks, total_count)
    """
    filtered_tasks = list(_tasks_db.values())

    # Apply filters
    if status is not None:
        filtered_tasks = [t for t in filtered_tasks if t.status == status]

    if priority is not None:
        filtered_tasks = [t for t in filtered_tasks if t.priority == priority]

    # Get total count before pagination
    total_count = len(filtered_tasks)

    # Apply pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_tasks = filtered_tasks[start_idx:end_idx]

    return paginated_tasks, total_count


def get_task_by_id(task_id: UUID) -> Task | None:
    return _tasks_db.get(str(task_id))


def update_task(task_id: UUID, payload: TaskUpdate) -> Task | None:
    task = _tasks_db.get(str(task_id))
    if not task:
        return None
    updated = task.model_copy(update=payload.model_dump(exclude_unset=True))
    _tasks_db[str(task_id)] = updated
    return updated


def delete_task(task_id: UUID) -> bool:
    task = _tasks_db.pop(str(task_id), None)
    return task is not None
