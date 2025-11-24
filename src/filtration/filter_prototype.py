import operator
from typing import List, Self, Any, Optional
from src.core.exceptions import ParamException
from src.core.base_prototype import BasePrototype
from src.dtos.filter_dto import FilterDto
from src.filtration.filter_operator import FilterOperator as op
from src.utils import is_primitive, get_inner_value


"""Класс-прототип с универсальной фильтрацией списков моделей"""
class FilterPrototype(BasePrototype):

    __match_operators = {
        op.EQUAL: operator.eq,
        op.NOT_EQUAL: operator.ne,
        op.GRATER: operator.gt,
        op.LESSER: operator.lt,
        op.GRATER_EQUAL: operator.ge,
        op.LESSER_EQUAL: operator.le,
    }
    
    def __init__(self, data):
        super().__init__(data)
    
    def clone(
        self,
        data: Optional[List[FilterDto]] = None
    ) -> Self:
        if data is None:
            return super().clone()
        
        result = list()
        for model in self.data:
            flag = True
            for filter in data:
                value = get_inner_value(model, filter.field)
                # if not is_primitive(value):
                #     raise ParamException(
                #         f"'{filter.field}' of {type(model).__name__} is "
                #         f"'{type(value).__name__}' not primitive"
                #     )
                if not self.compare(value, filter):
                    flag = False
                    break
            if flag:
                result += [model]
        
        return super().clone(result)
    
    def compare(
        self,
        left: Any,
        filter: FilterDto
    ) -> bool:
        if filter.operator == op.LIKE:
            return str(left) in str(filter.value)
        elif filter.operator == op.CONTAINS:
            return left is not None and str(filter.value) in str(left)
        else:
            oper = self.__match_operators[filter.operator]
            return oper(left, filter.value)
    