from enum import Enum
from pydantic import BaseModel
from typing import Any

class FilterOperator(str, Enum):
    """Valid filter operators."""
    EQUALS = 'eq'
    NOT_EQUALS = 'neq'
    GREATER_THAN = 'gt'
    GREATER_THAN_EQUALS = 'gte'
    LESS_THAN = 'lt'
    LESS_THAN_EQUALS = 'lte'
    IN = 'in'
    NOT_IN = 'nin'
    LIKE = 'like'

class SortOrder(str, Enum):
    """Valid sort orders."""
    ASCENDING = 'asc'
    DESCENDING = 'desc'

class FilterCondition(BaseModel):
    """Model for a single filter condition."""
    field: str
    operator: FilterOperator
    value: str | int | float | bool | list[Any]

class SortCondition(BaseModel):
    """Model for a single sort condition."""
    field: str
    order: SortOrder

class DefaultRetrievalSchema(BaseModel):
    """Default schema for retrieval parameters."""
    query: str
    filters: list[FilterCondition] | None
    sort: list[SortCondition] | None
