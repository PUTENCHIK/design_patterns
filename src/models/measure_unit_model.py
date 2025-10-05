from typing import Optional, Self, Union
from src.core.abstract_model import AbstractModel
from src.core.validator import Validator as vld
from src.singletons.repository import Repository


"""Модель единиц измерения для моделей номенклатуры"""
class MeasureUnitModel(AbstractModel):
    # Коэффициент пересчёта
    __coefficient: float = 0.0

    # Наименование (наследуется от AbstractModel)

    # Базовая единица измерения
    __base_unit: Optional[Self] = None
    
    def __init__(
        self,
        coef: Union[int, float],
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
    
    """Базовая единица измерения"""
    @property
    def base_unit(self) -> Self:
        return self.__base_unit
    
    @base_unit.setter
    def base_unit(self, value: Optional[Self]):
        vld.validate(value, MeasureUnitModel,
                     "base_unit", could_be_none=True)
        self.__base_unit = value

    """Универсальный фабричный метод"""
    @staticmethod
    def create(
        coef: Union[int, float],
        name: str,
        base_unit: Optional[Self] = None
    ) -> Self:
        return MeasureUnitModel(coef, name, base_unit)
    
    """Фабричный метод для создания грамма"""
    @staticmethod
    def create_gramm() -> Self:
        return MeasureUnitModel.create(
            1, Repository.get_measure_unit_names()["gramm"]
        )
    
    """Фабричный метод для создания килограмма"""
    @staticmethod
    def create_kilo(inner_gramm: Self) -> Self:
        return MeasureUnitModel.create(
            1, Repository.get_measure_unit_names()["kilo"], inner_gramm
        )
