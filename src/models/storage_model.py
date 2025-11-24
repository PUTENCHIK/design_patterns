from typing import Optional, Self
from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.dtos.storage_dto import StorageDto
from src.singletons.repository import Repository


"""Модель склада"""
class StorageModel(AbstractModel):
    # Наименование (наследуется от AbstractModel)

    # Адрес
    __address: Optional[str] = None

    def __init__(
        self,
        name: Optional[str] = None,
        address: Optional[str] = None
    ):
        super().__init__()
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address

    """Адрес склада"""
    @property
    def address(self) -> Optional[str]:
        return self.__address
    
    @address.setter
    def address(self, value: str):
        vld.is_str(value, "storage address")
        self.__address = value
    
    """Универсальный фабричный метод"""
    @staticmethod
    def create(name: str, address: str) -> Self:
        return StorageModel(name, address)

    """Фабричный метод из DTO"""
    @staticmethod
    def from_dto(dto: StorageDto, repo: Repository) -> Self:
        model = StorageModel(
            name=dto.name,
            address=dto.address
        )
        model.unique_code = dto.unique_code

        return model
