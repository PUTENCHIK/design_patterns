from typing import Self
from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.core.exceptions import WrongTypeException


"""Модель склада"""
class StorageModel(AbstractModel):
    # Наименование
    __name: str = ""

    """Наименование склада"""
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        vld.is_str(value, "name")
        self.__name = value
    
    """Перегрузка оператора стравнения склада с другим складом"""
    def __eq__(self, other: Self) -> bool:
        vld.validate(other, StorageModel, "other object")
        return self.unique_code == other.unique_code
