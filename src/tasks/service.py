from uuid import UUID
from src.tasks.schemas import Task, TaskCreate, TaskUpdate

# In-memory store — will be replaced with a real DB in Stage 3
_tasks_db: dict[str, Task] = {}


def create_task(payload: TaskCreate) -> Task:
    task = Task(**payload.model_dump())
    _tasks_db[str(task.id)] = task
    return task


def get_all_tasks() -> list[Task]:
    return list(_tasks_db.values())


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
