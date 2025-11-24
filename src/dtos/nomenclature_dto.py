from typing import Self
from src.core.validator import Validator as vld
from src.core.abstract_dto import AbstractDto


"""DTO для модели NomenclatureModel"""
class NomenclatureDto(AbstractDto):
    # Группа номенклатуры
    __group_code: str = ""

    # Единица измерения
    __measure_unit_code: str = ""

    def __init__(self):
        super().__init__()

    def load(self, data) -> Self:
        return super().load(data)
    
    """Поле группы номенклатуры"""
    @property
    def group_code(self) -> str:
        return self.__group_code
    
    @group_code.setter
    def group_code(self, value: str):
        vld.is_str(value, "group code")
        self.__group_code = value
    
    """Поле единицы измерения"""
    @property
    def measure_unit_code(self) -> str:
        return self.__measure_unit_code
    
    @measure_unit_code.setter
    def measure_unit_code(self, value: str):
        vld.is_str(value, "measure unit code")
        self.__measure_unit_code = value
