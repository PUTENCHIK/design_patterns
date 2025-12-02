import uuid
from abc import ABC, abstractmethod
from typing import Union, Self
from src.core.validator import Validator as vld
from src.core.ihandleable import IHandleable
from src.core.exceptions import WrongTypeException
from src.singletons.observe_service import ObserveService


"""Абстрактная модель с полем уникального кода для однозначной
идентификации объектов. От AbstractModel наследуются все модели приложения.
"""
class AbstractModel(ABC, IHandleable):
    # Уникальный ID модели
    __unique_code: str

    # Наименование модели (50)
    __name: str = ""

    @abstractmethod
    def __init__(self):
        super().__init__()
        self.__unique_code = uuid.uuid4().hex
        ObserveService().add(self)
    
    """Атрибут уникального кода"""
    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        vld.is_str(value, "unique_code")
        self.__unique_code = value.strip()
    
    """Наименование модели"""
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        vld.is_str(value, "name", len_=50)
        self.__name = value.strip()
    
    """Перегрузка оператора сравнения"""
    def __eq__(self, other: Union[str, Self]) -> bool:
        if isinstance(other, str):
            return self.unique_code == other
        elif isinstance(other, AbstractModel):
            return self.unique_code == other.unique_code
        elif other is None:
            return False
        else:
            raise WrongTypeException(
                f"Imposible compare with '{type(other)}'"
            )
    
    """Перегрузка оператора неравества"""
    def __ne__(self, other: Union[str, Self]) -> bool:
        return not self.__eq__(other)
    
    """Перевод модели в строку"""
    def __str__(self):
        return self.unique_code
    
    """Абстрактный фабричный метод из DTO"""
    @staticmethod
    @abstractmethod
    def from_dto(dto, repo) -> Self:
        pass

    """Метод обработки событий"""
    def handle(self, event, params):
        super().handle(event, params)
