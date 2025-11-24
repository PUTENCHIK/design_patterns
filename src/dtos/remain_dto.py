from typing import Self, Union
from src.core.validator import Validator as vld
from src.core.abstract_dto import AbstractDto


"""DTO для модели RemainModel"""
class RemainDto(AbstractDto):

    # Номенклатура
    __nomenclature_code: str = ""

    # Склад
    __storage_code: str = ""

    # Единица измерения
    __measure_unit_code: str = ""

    # Значение остатка
    __value: float = 0

    def __init__(self):
        super().__init__()

    def load(self, data) -> Self:
        return super().load(data)
    
    """Поле номенклатуры"""
    @property
    def nomenclature_code(self) -> str:
        return self.__nomenclature_code
    
    @nomenclature_code.setter
    def nomenclature_code(self, value: str):
        vld.is_str(value, "nomenclature code")
        self.__nomenclature_code = value
    
    """Поле склада"""
    @property
    def storage_code(self) -> str:
        return self.__storage_code
    
    @storage_code.setter
    def storage_code(self, value: str):
        vld.is_str(value, "storage code")
        self.__storage_code = value
    
    """Поле единицы измерения"""
    @property
    def measure_unit_code(self) -> str:
        return self.__measure_unit_code
    
    @measure_unit_code.setter
    def measure_unit_code(self, value: str):
        vld.is_str(value, "measure unit code")
        self.__measure_unit_code = value
    
    """Поле значения остатка"""
    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, value: Union[int, float]):
        vld.is_number(value, "value")
        self.__value = float(value)
