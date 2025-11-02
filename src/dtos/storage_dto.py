from typing import Self
from src.core.validator import Validator as vld
from src.core.abstract_dto import AbstractDto


"""DTO для модели StorageModel"""
class StorageDto(AbstractDto):
    # Уникальный код DTO (наследуется от AbstractDto)

    # Наименование DTO (наследуется от AbstractDto)

    # Адрес
    __address: str

    def __init__(self):
        super().__init__()
    
    """Поле адреса"""
    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        vld.is_str(value, "storage address")
        self.__address = value
    
    def load(self, data: dict) -> Self:
        return super().load(data)
