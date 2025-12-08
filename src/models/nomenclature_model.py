from typing import Optional, Self
from pydantic import BaseModel
from src.core.validator import Validator as vld
from src.core.event_type import EventType
from src.core.exceptions import OperationException
from src.core.event_params import ModelBaseParams
from src.core.abstract_model import AbstractModel
from src.dtos.nomenclature_dto import NomenclatureDto
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.singletons.repository import Repository
from src.singletons.observe_service import ObserveService


"""Модель номенклатуры"""
class NomenclatureModel(AbstractModel):
    # Наименование (255)
    __name: Optional[str] = None

    # Группа номенклатуры
    __group: Optional[NomenclatureGroupModel] = None

    # Единица измерения
    __measure_unit: Optional[MeasureUnitModel] = None

    def __init__(
        self,
        name: Optional[str] = None,
        group: Optional[NomenclatureGroupModel] = None,
        unit: Optional[MeasureUnitModel] = None,
    ):
        super().__init__()
        if name is not None:
            self.name = name
        if group is not None:
            self.group = group
        if unit is not None:
            self.measure_unit = unit

    """Поле наименования"""
    @property
    def name(self) -> Optional[str]:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        vld.is_str(value, "name", len_=255)
        self.__name = value.strip()
    
    """Поле группы номенклатуры"""
    @property
    def group(self) -> Optional[NomenclatureGroupModel]:
        return self.__group
    
    @group.setter
    def group(self, value: Optional[NomenclatureGroupModel]):
        vld.validate(value, NomenclatureGroupModel, "group", True)
        self.__group = value
    
    """Поле, хранящее объект единицы измерения"""
    @property
    def measure_unit(self) -> Optional[MeasureUnitModel]:
        return self.__measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: Optional[MeasureUnitModel]):
        vld.validate(value, MeasureUnitModel, "measure_unit", True)
        self.__measure_unit = value
    
    """Универсальный фабричный метод"""
    @staticmethod
    def create(
        name: Optional[str] = None,
        group: Optional[NomenclatureGroupModel] = None,
        unit: Optional[MeasureUnitModel] = None,
    ) -> Self:
        return NomenclatureModel(name, group, unit)
    
    """Фабричный метод из DTO"""
    @staticmethod
    def from_dto(dto: NomenclatureDto, repo: Repository) -> Self:
        group = repo.get(unique_code=dto.group_code)
        unit = repo.get(unique_code=dto.measure_unit_code)
        model = NomenclatureModel(
            name=dto.name,
            group=group,
            unit=unit,
        )
        if dto.unique_code is not None:
            model.unique_code = dto.unique_code

        return model

    """Обработка событий моделей номенклатуры"""
    def handle(self, event: EventType, params: BaseModel):
        super().handle(event, params)
        match event:
            case EventType.TRY_DELETE_MODEL:
                vld.validate(params, ModelBaseParams, "params")
                params: ModelBaseParams = params
                # Если удаляется единица измерения номенклатуры
                if self.measure_unit is not None and \
                        self.measure_unit == params.unique_code:
                    ObserveService().block_model_deleting(
                        params.unique_code,
                        self.unique_code
                    )
                    raise OperationException(
                        f"Impossible to delete measure unit '{self.measure_unit}' "
                        f"because it's unit of nomenclature '{self}'"
                    )
                # Если удаляется группа номенклатуры
                elif self.group is not None and \
                        self.group == params.unique_code:
                    ObserveService().block_model_deleting(
                        params.unique_code,
                        self.unique_code
                    )
                    raise OperationException(
                        f"Impossible to delete nomenclature group '{self.group}' "
                        f"because it's group of nomenclature '{self}'"
                    )
