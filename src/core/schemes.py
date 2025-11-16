from typing import Any
from pydantic import BaseModel
from src.filtration.filter_operator import FilterOperator


class FilterScheme(BaseModel):
    field: str
    operator: FilterOperator
    value: Any
