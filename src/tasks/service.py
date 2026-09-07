from uuid import UUID

from sqlalchemy.orm import Session

from src.tasks.models import Task
from src.tasks.schemas import TaskCreate, TaskPriority, TaskStatus, TaskUpdate


def create_task(db: Session, payload: TaskCreate) -> Task:
    """Create a new task in database."""
    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        is_done=False
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


def get_all_tasks(
        db: Session,
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
    query = db.query(Task)

    # Apply filters
    if status is not None:
        query = query.filter(Task.status == status)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    # Get total count before pagination
    total_count = query.count()

    # Apply pagination
    offset= (page - 1) * limit
    paginated_tasks = query.offset(offset).limit(limit).all()

    return paginated_tasks, total_count


def get_task_by_id(db: Session, task_id: UUID) -> Task | None:
    """Get a single task by ID."""
    return db.query(Task).filter(Task.id == str(task_id)).first()


def update_task(db: Session, task_id: UUID, payload: TaskUpdate) -> Task | None:
    """Update task by ID."""

    task = get_task_by_id(db, task_id)

    if not task:
        return None

    # Update only provided fields

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: UUID) -> bool:
    """Delete single task by ID."""
    task = get_task_by_id(db, task_id)
    if not task:
        return False

    db.delete(task)
    db.commit()

    return True
