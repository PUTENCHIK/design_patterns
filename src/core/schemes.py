from typing import Any
from pydantic import BaseModel
from src.filtration.filter_operator import FilterOperator as op


class FilterScheme(BaseModel):
    field: str
    operator: op
    value: Any
