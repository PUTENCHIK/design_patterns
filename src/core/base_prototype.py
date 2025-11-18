from typing import Self, Optional
from src.core.validator import Validator as vld


"""Класс-прототип"""
class BasePrototype:
    # Список моделей
    __data: list = []

    def __init__(self, data: list):
        vld.is_list(data, "data")
        self.__data = data
    
    @property
    def data(self) -> list:
        return self.__data

    def clone(self, data: Optional[list] = None) -> Self:
        return BasePrototype(
            self.__data if data is None else data
        )
