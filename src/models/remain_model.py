from typing import Union
from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.dtos.remain_dto import RemainDto
from src.models.nomenclature_model import NomenclatureModel
from src.models.storage_model import StorageModel
from src.models.measure_unit_model import MeasureUnitModel
from src.singletons.repository import Repository


"""Модель остатка на определённую дату"""
class RemainModel(AbstractModel):
    
    # Номенклатура
    __nomenclature: NomenclatureModel

    # Склад
    __storage: StorageModel

    # Единица измерения остатка
    __measure_unit: MeasureUnitModel

    # Значение остатка
    __value: float

    def __init__(
        self,
        nomenclature: NomenclatureModel,
        storage: StorageModel,
        measure_unit: MeasureUnitModel,
        value: float,
    ):
        super().__init__()
        self.nomenclature = nomenclature
        self.storage = storage
        self.measure_unit = measure_unit
        self.value = value
    
    """Поле наименования (процедурное)"""
    @property
    def name(self) -> str:
        return f"остаток #{self.unique_code}"

    """Поле номенклатуры"""
    @property
    def nomenclature(self) -> NomenclatureModel:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        vld.validate(value, NomenclatureModel, "nomenclature")
        self.__nomenclature = value
    
    """Поле склада"""
    @property
    def storage(self) -> StorageModel:
        return self.__storage
    
    @storage.setter
    def storage(self, value: StorageModel):
        vld.validate(value, StorageModel, "storage")
        self.__storage = value
    
    """Поле единицы измерения"""
    @property
    def measure_unit(self) -> MeasureUnitModel:
        return self.__measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: MeasureUnitModel):
        vld.validate(value, MeasureUnitModel, "measure_unit")
        self.__measure_unit = value
    
    """Поле значения остатка"""
    @property
    def value(self) -> float:
        return self.__value
    
    @value.setter
    def value(self, value: Union[int, float]):
        vld.is_number(value, "value")
        self.__value = float(value)
    
    """Хэш-ключ"""
    def hash_key(self) -> str:
        return f"{self.storage.unique_code}_" \
            f"{self.nomenclature.unique_code}_" \
            f"{self.measure_unit.unique_code}"

    """Фабричный метод из DTO"""
    @staticmethod
    def from_dto(dto: RemainDto, repo: Repository):
        nomenclature = repo.get(unique_code=dto.nomenclature_code)
        storage = repo.get(unique_code=dto.storage_code)
        unit = repo.get(unique_code=dto.measure_unit_code)
        model = RemainModel(
            nomenclature=nomenclature,
            storage=storage,
            measure_unit=unit,
            value=dto.value
        )
        model.unique_code = dto.unique_code

        return model
