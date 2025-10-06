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
    
    """Метод добавления ингредиентов в рецепт"""
    def add_ingredient(
        self,
        nomenclature: NomenclatureModel,
        count: int
    ) -> bool:
        vld.validate(nomenclature, NomenclatureModel, "nomenclature")
        vld.is_int(count, "count")
        # Если такой же ингредиент или с таким же названием уже есть,
        # то его не добавлять
        for nom, _ in self.ingredients:
            if nom == nomenclature or nom.name == nomenclature.name:
                return False
        
        # Ингредиент в словаре не найден - можно добавить
        self.__ingredients.append((nomenclature, count))
        return True

    """Фабричный метод для создания рецепта омлета (OmeletteRecipe.md)"""
    @staticmethod
    def create_omlette_recipe(
        eggs_nomenclature: NomenclatureModel,
        sunflower_oil_nomenclature: NomenclatureModel,
        milk_nomenclature: NomenclatureModel,
        sausages_nomenclature: NomenclatureModel,
        salt_nomenclature: NomenclatureModel,
    ) -> Self:
        vld.validate(eggs_nomenclature, NomenclatureModel,
                     "eggs_nomenclature")
        vld.validate(sunflower_oil_nomenclature, NomenclatureModel,
                     "sunflower_oil_nomenclature")
        vld.validate(milk_nomenclature, NomenclatureModel,
                     "milk_nomenclature")
        vld.validate(sausages_nomenclature, NomenclatureModel,
                     "sausages_nomenclature")
        vld.validate(salt_nomenclature, NomenclatureModel,
                     "salt_nomenclature")

        recipe = RecipeModel()
        recipe.name = "Омлет"
        recipe.add_ingredient(eggs_nomenclature, 3)
        recipe.add_ingredient(sunflower_oil_nomenclature, 10)
        recipe.add_ingredient(milk_nomenclature, 200)
        recipe.add_ingredient(sausages_nomenclature, 1)
        recipe.add_ingredient(salt_nomenclature, 5)

        return recipe
