from pydantic import BaseModel, Field

from src.tasks.schemas import TaskResponse


class PaginationMetadata(BaseModel):
    """Pagination metadata base model"""
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    limit: int = Field(description="Items per page")
    pages: int = Field(description="Total number of pages")


class PaginatedTaskResponse(BaseModel):
    """Paginated response wrapper"""
    data: list[TaskResponse]
    total: int
    page: int
    limit: int
    pages: int