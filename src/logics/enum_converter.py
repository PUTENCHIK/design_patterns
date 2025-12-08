from enum import Enum
from src.core.validator import Validator as vld
from src.core.abstract_converter import AbstractConverter


class EnumConverter(AbstractConverter):
    
    def __init__(self):
        super().__init__()
    
    """Переопределённый метод convert"""
    def convert(self, object_: Enum):
        vld.validate(object_, Enum, "object")

        return object_.name
