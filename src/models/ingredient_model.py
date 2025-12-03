from typing import Optional, Self
from src.core.validator import Validator as vld
from src.core.event_type import EventType
from src.core.exceptions import OperationException
from src.core.event_params import AbstractEventParams, DeleteModelEventParams
from src.core.abstract_model import AbstractModel
from src.dtos.ingredient_dto import IngredientDto
from src.models.nomenclature_model import NomenclatureModel
from src.models.measure_unit_model import MeasureUnitModel
from src.singletons.repository import Repository


"""Модель ингредиента рецепта"""
class IngredientModel(AbstractModel):
    # Наименование (наследуется от AbstractModel)

    # Номенклатура, описывающая ингредиент
    __nomenclature: NomenclatureModel

    # Единица измерения, в которой указывается count
    __measure_unit: MeasureUnitModel

    # Количество ингредиента (в measure_unit)
    __count: int
    
    def __init__(
        self,
        nomenclature: Optional[NomenclatureModel],
        measure_unit: Optional[MeasureUnitModel],
        count: Optional[int],
    ):
        super().__init__()
        if nomenclature is not None:
            self.nomenclature = nomenclature
        if measure_unit is not None:
            self.measure_unit = measure_unit
        if count is not None:
            self.count = count
    
    """Поле наименования"""
    @property
    def name(self) -> str:
        return f"ингредиент '{self.nomenclature.name}'"

    """Поле номенклатуры"""
    @property
    def nomenclature(self) -> NomenclatureModel:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        vld.validate(value, NomenclatureModel, "nomenclature")
        self.__nomenclature = value
    
    """Поле единицы измерения"""
    @property
    def measure_unit(self) -> MeasureUnitModel:
        return self.__measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: MeasureUnitModel):
        vld.validate(value, MeasureUnitModel, "measure_unit")
        self.__measure_unit = value
    
    """Поле количества ингредиента"""
    @property
    def count(self) -> int:
        return self.__count
    
    @count.setter
    def count(self, value: int):
        vld.is_int(value, "count")
        self.__count = value
    
    """Универсальный фабричный метод"""
    @staticmethod
    def create(
        nomenclature: NomenclatureModel,
        measure_unit: MeasureUnitModel,
        count: int,
    ) -> Self:
        return IngredientModel(nomenclature, measure_unit, count)
    
    """Фабричный метод из DTO"""
    @staticmethod
    def from_dto(dto: IngredientDto, repo: Repository) -> Self:
        nomenclature = repo.get(unique_code=dto.nomenclature_code)
        measure_unit = repo.get(unique_code=dto.measure_unit_code)
        model = IngredientModel(
            nomenclature=nomenclature,
            measure_unit=measure_unit,
            count=dto.count,
        )
        if dto.unique_code is not None:
            model.unique_code = dto.unique_code

        return model
    
    """Обработка событий моделей ингредиентов"""
    def handle(self, event: EventType, params: AbstractEventParams):
        super().handle(event, params)
        if event == EventType.DELETE_MODEL:
            vld.validate(params, DeleteModelEventParams, "params")
            params: DeleteModelEventParams = params
            # Если удаляется единица измерения ингредиента
            if self.measure_unit is not None and \
                    self.measure_unit == params.unique_code:
                raise OperationException(
                    f"Impossible to delete measure unit '{self.measure_unit}' "
                    f"because it's unit of ingredient '{self}'"
                )
            # Если удаляется номенклатура ингредиента
            elif self.nomenclature is not None and \
                    self.nomenclature == params.unique_code:
                raise OperationException(
                    f"Impossible to delete nomenclature "
                    f"'{self.nomenclature}' because it's nomenclature of "
                    f"ingredient '{self}'"
                )
