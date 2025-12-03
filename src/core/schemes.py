from typing import Any, Union, Optional
from pydantic import BaseModel
from src.filtration.filter_operator import FilterOperator as op


class FilterScheme(BaseModel):
    field: str
    operator: op
    value: Any


class NomenclatureGroupScheme(BaseModel):
    name: str


class NomenclatureScheme(BaseModel):
    name: str
    group_code: str
    measure_unit_code: str


class MeasureUnitScheme(BaseModel):
    name: str
    coefficient: Union[int, float]
    base_unit_code: Optional[str]


class StorageScheme(BaseModel):
    name: str
    address: str
