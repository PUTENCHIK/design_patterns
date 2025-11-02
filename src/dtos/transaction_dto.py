from typing import Self, Union
from src.core.validator import Validator as vld
from src.core.abstract_dto import AbstractDto


"""DTO для модели TransactionModel"""
class TransactionDto(AbstractDto):
    # Уникальный код DTO (наследуется от AbstractDto)

    # Наименование DTO (наследуется от AbstractDto)

    # Дата и время проведения
    __datetime: str

    # Номенклатура
    __nomenclature_name: str

    # Склад
    __storage_name: str

    # Количество
    __count: float

    # Единица измерения
    __measure_unit_name: str
    
    def __init__(self):
        super().__init__()
    
    """Поле даты и времени"""
    @property
    def datetime(self) -> str:
        return self.__datetime
    
    @datetime.setter
    def datetime(self, value: str):
        vld.is_str(value, "datetime")
        self.__datetime = value
    
    """Поле номенклатуры"""
    @property
    def nomenclature_name(self) -> str:
        return self.__nomenclature_name
    
    @nomenclature_name.setter
    def nomenclature_name(self, value: str):
        vld.is_str(value, "nomenclature name")
        self.__nomenclature_name = value
    
    """Поле склада"""
    @property
    def storage_name(self) -> str:
        return self.__storage_name
    
    @storage_name.setter
    def storage_name(self, value: str):
        vld.is_str(value, "storage name")
        self.__storage_name = value
    
    """Поле количества"""
    @property
    def count(self) -> float:
        return self.__count
    
    @count.setter
    def count(self, value: Union[int, float]):
        vld.is_number(value, "count")
        self.__count = float(value)
    
    """Поле единицы измерения"""
    @property
    def measure_unit_name(self) -> str:
        return self.__measure_unit_name
    
    @measure_unit_name.setter
    def measure_unit_name(self, value: str):
        vld.is_str(value, "measure unit name")
        self.__measure_unit_name = value
    
    def load(self, data: dict) -> Self:
        return super().load(data)