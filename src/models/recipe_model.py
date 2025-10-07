from typing import Self, Optional, List, Tuple
from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.models.nomenclature_model import NomenclatureModel


"""Модель рецепта"""
class RecipeModel(AbstractModel):
    # Наименование (наследуется от AbstractModel)

    # Описание рецепта (255, опционально)
    __description: Optional[str] = None

    # Список ингредиентов блюда
    __ingredients: List[Tuple[NomenclatureModel, int]] = list()

    def __init__(
        self,
        name: Optional[str] = None
    ):
        super().__init__()
        if name is not None:
            self.name = name
    
    """Поле текстового описания рецепта"""
    @property
    def description(self) -> Optional[str]:
        return self.__description

    @description.setter
    def description(self, value: Optional[str]):
        vld.is_str(value, "description", True, 255)
        self.__description = value
    
    """Поле со словарём ингредиентов рецепта"""
    @property
    def ingredients(self) -> List[Tuple[NomenclatureModel, int]]:
        return self.__ingredients
