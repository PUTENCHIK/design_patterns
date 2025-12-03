from abc import ABC, abstractmethod
from src.core.validator import Validator as vld


class AbstractEventParams(ABC):

    @abstractmethod
    def __init__(self):
        super().__init__()


class DeleteModelEventParams(AbstractEventParams):

    # Уникальный код удаляемой модели
    __unique_code: str

    def __init__(self, unique_code: str):
        super().__init__()
        self.unique_code = unique_code
    
    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        vld.is_str(value, "unique_code")
        self.__unique_code = value
