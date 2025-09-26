import uuid
from abc import ABC


class AbstractModel(ABC):
    __unique_code: str

    def __init__(self):
        self.__unique_code = uuid.uuid4().hex
    
    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        #валидация строки
        self.__unique_code = value
    
    def __eq__(self, value: str) -> bool:
        if not isinstance(value, str):
            raise TypeError("Value must be string")
        return self.unique_code == value
