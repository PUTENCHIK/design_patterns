import operator
from typing import List, Self, Any
from src.core.exceptions import ParamException
from src.core.base_prototype import BasePrototype
from src.dtos.filter_dto import FilterDto
from src.filtration.filter_operator import FilterOperator
from src.utils import is_primitive, get_inner_value


"""Класс-прототип с универсальной фильтрацией списков моделей"""
class FilterPrototype(BasePrototype):

    __match_operators = {
        FilterOperator.EQUAL: operator.eq,
        FilterOperator.NOT_EQUAL: operator.ne,
        FilterOperator.GRATER: operator.gt,
        FilterOperator.LESSER: operator.lt,
        FilterOperator.GRATER_EQUAL: operator.ge,
        FilterOperator.LESSER_EQUAL: operator.le,
    }
    
    def __init__(self, data):
        super().__init__(data)
    
    def clone(self, data = None):
        return super().clone(data)
    
    def filter(
        self,
        filters: List[FilterDto]
    ) -> Self:
        result = list()
        for model in self.data:
            flag = True
            for filter in filters:
                value = get_inner_value(model, filter.field)
                if not is_primitive(value):
                    raise ParamException(
                        f"'{filter.field}' of {type(model).__name__} is "
                        f"'{type(value).__name__}' not primitive"
                    )
                if not self.compare(value, filter):
                    flag = False
                    break
            if flag:
                result += [model]
        
        return self.clone(result)
    
    def compare(
        self,
        left: Any,
        filter: FilterDto
    ) -> bool:
        if filter.operator == FilterOperator.LIKE:
            return left in str(filter.value)
        elif filter.operator == FilterOperator.CONTAINS:
            return left is not None and str(filter.value) in left
        else:
            op = self.__match_operators[filter.operator]
            return op(left, filter.value)
    