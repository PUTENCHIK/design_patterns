from typing import Optional, Self, Union
from datetime import datetime as dt_type
from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.dtos.transaction_dto import TransactionDto
from src.models.storage_model import StorageModel
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.singletons.repository import Repository
from src.singletons.settings_manager import SettingsManager


"""Модель транзакции"""
class TransactionModel(AbstractModel):

    # Уникальный номер (наследуется от AbstractModel)

    # Наименование (наследуется от AbstractModel)

    # Дата и время проведения
    __datetime: dt_type

    # Номенклатура
    __nomenclature: NomenclatureModel

    # Склад
    __storage: StorageModel

    # Количество
    __count: float

    # Единица измерения
    __measure_unit: MeasureUnitModel

    def __init__(
        self,
        datetime: Optional[dt_type] = None,
        nomenclature: Optional[NomenclatureModel] = None,
        storage: Optional[StorageModel] = None,
        count: Optional[float] = None,
        measure_unit: Optional[MeasureUnitModel] = None,
    ):
        super().__init__()
        if datetime is not None:
            self.datetime = datetime
        if nomenclature is not None:
            self.nomenclature = nomenclature
        if storage is not None:
            self.storage = storage
        if count is not None:
            self.count = count
        if measure_unit is not None:
            self.measure_unit = measure_unit
    
    """Поле наименования"""
    @property
    def name(self) -> str:
        return f"транзакция #{self.unique_code}"

    """Поле даты и времени"""
    @property
    def datetime(self) -> dt_type:
        return self.__datetime
    
    @datetime.setter
    def datetime(self, value: dt_type):
        vld.validate(value, dt_type, "datetime")
        self.__datetime = value
    
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
    
    """Поле количества"""
    @property
    def count(self) -> float:
        return self.__count
    
    @count.setter
    def count(self, value: Union[int, float]):
        vld.is_number(value, "count")
        self.__count = float(value)
    
    """Поле единицы измерения"""
    @property
    def measure_unit(self) -> MeasureUnitModel:
        return self.__measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: MeasureUnitModel):
        vld.validate(value, MeasureUnitModel, "measure_unit")
        self.__measure_unit = value
    
    """Универсальный фабричный метод"""
    @staticmethod
    def create(
        datetime: dt_type,
        nomenclature: NomenclatureModel,
        storage: StorageModel,
        count: float,
        measure_unit: MeasureUnitModel,
    ) -> Self:
        return TransactionModel(datetime, nomenclature, storage, count,
                                measure_unit)
    
    """Фабричный метод из DTO"""
    @staticmethod
    def from_dto(dto: TransactionDto, repo: Repository):
        datetime = dt_type.strptime(
            dto.datetime,
            SettingsManager().settings.datetime_format
        )
        nomenclature = repo.get(unique_code=dto.nomenclature_code)
        storage = repo.get(unique_code=dto.storage_code)
        unit = repo.get(unique_code=dto.measure_unit_code)
        model = TransactionModel(
            datetime=datetime,
            nomenclature=nomenclature,
            storage=storage,
            count=dto.count,
            measure_unit=unit
        )
        model.unique_code = dto.unique_code

        return model
