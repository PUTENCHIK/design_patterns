from typing import Optional, Self, Union
from src.core.abstract_model import AbstractModel
from src.core.validator import Validator as vld


"""Модель единиц измерения для моделей номенклатуры"""
class MeasureUnitModel(AbstractModel):
    # Коэффициент пересчёта
    __coefficient: float = 0.0

    # Наименование
    __name: str = ""

    # Базовая единица измерения
    __base_unit: Optional[Self] = None
    
    def __init__(
        self,
        coef: float,
        name: str,
        base_unit: Optional[Self] = None
    ):
        super().__init__()
        self.coefficient = coef
        self.name = name
        self.base_unit = base_unit

    """Поле коэффициента пересчёта"""
    @property
    def coefficient(self) -> float:
        return self.__coefficient
    
    @coefficient.setter
    def coefficient(self, value: Union[float, int]):
        vld.is_number(value, "unit coefficient")
        self.__coefficient = float(value)
    
    """Наименование единицы измерения"""
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        vld.is_str(value, "measure unit's name")
        self.__name = value.strip()
    
    """Базовая единица измерения"""
    @property
    def base_unit(self) -> Self:
        return self.__base_unit
    
    @base_unit.setter
    def base_unit(self, value: Optional[Self]):
        vld.validate(value, MeasureUnitModel,
                     "base_unit", could_be_none=True)
        self.__base_unit = value
