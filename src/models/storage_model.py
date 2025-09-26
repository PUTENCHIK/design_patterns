import uuid
from typing import Self


"""
TODO
1. Валидаторы для name
2. Для модели с ID нужно добавить Abstract class
"""
class StorageModel:
    __id: str
    __name: str = ""

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        self.__name = value
    
    def __init__(self):
        self.id = uuid.uuid4()
    
    def __eq__(self, value: Self) -> bool:
        if not isinstance(value, StorageModel):
            raise TypeError("StorageModel could be compared only with StorageModel")
        return self.id == value.id
