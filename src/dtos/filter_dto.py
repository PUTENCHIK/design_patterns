from typing import Any, Optional
from src.core.validator import Validator as vld
from src.core.abstract_dto import AbstractDto
from src.filtration.filter_operator import FilterOperator as op


"""DTO для хранения данных о фильтере моделей"""
class FilterDto(AbstractDto):
    # Название поля модели или вложенного поля внутренней модели
    __field: str

    # Оператор фильтра
    __operator: op

    # Значение для сравнения со значением поля модели
    __value: Any
    
    def __init__(
        self,
        field: Optional[str] = None,
        operator: Optional[op] = None,
        value: Optional[Any] = None,
    ):
        super().__init__()
        if field is not None:
            self.field = field
        if operator is not None:
            self.operator = operator
        if value is not None:
            self.value = value
    
    def load(self, data: dict):
        return super().load(data)
    
    """Название поля модели"""
    @property
    def field(self) -> str:
        return self.__field
    
    @field.setter
    def field(self, value: str):
        vld.is_str(value, "field")
        self.__field = value
    
    """Оператор фильтра"""
    @property
    def operator(self) -> op:
        return self.__operator
    
    @operator.setter
    def operator(self, value: op):
        vld.validate(value, op, "operator")
        self.__operator = value
    
    """Значение для сравнения"""
    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value: Any):
        self.__value = value
