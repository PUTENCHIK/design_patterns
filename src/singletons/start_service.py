from typing import Optional, List, Dict
from src.core.validator import Validator as vld
from src.models.recipe_model import RecipeModel
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.singletons.repository import Repository


"""Класс, наполняющий приложение эталлоными объектами разных типов"""
class StartService:
    # Ссылка на экземпляр StartService
    __instance = None

    # Ссылка на объект Repository
    __repository: Optional[Repository] = Repository()

    def __init__(self):
        self.data[Repository.measure_unit_key] = dict()
        self.data[Repository.nomenclature_group_key] = dict()
        self.data[Repository.nomenclatures_key] = list()
        self.data[Repository.recipes_key] = list()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    """Словарь данных репозитория"""
    @property
    def data(self) -> dict:
        return self.__repository.data

    """Эталонные единицы измерения репозитория"""
    @property
    def measure_units(self) -> Dict[str, MeasureUnitModel]:
        return self.data[Repository.measure_unit_key]

    """Метод генерации эталонных единиц измерения"""
    def __create_measure_units(self):
        names = Repository.get_measure_unit_names()
        gramm = MeasureUnitModel.create_gramm()
        milliliter = MeasureUnitModel.create_milliliter()
        kilo = MeasureUnitModel.create_kilo(gramm)
        egg = MeasureUnitModel(75, names["egg"], gramm)
        sausage = MeasureUnitModel(75, names["sausage"], gramm)
        if gramm.name not in self.measure_units:
            self.measure_units[gramm.name] = gramm
        if kilo.name not in self.measure_units:
            self.measure_units[kilo.name] = kilo
        if milliliter.name not in self.measure_units:
            self.measure_units[milliliter.name] = milliliter
        if egg.name not in self.measure_units:
            self.measure_units[egg.name] = egg
        if sausage.name not in self.measure_units:
            self.measure_units[sausage.name] = sausage
    
    """Эталонные группы номенклатуры репозитория"""
    @property
    def nomenclature_groups(self) -> Dict[str, NomenclatureGroupModel]:
        return self.data[Repository.nomenclature_group_key]
    
    """Метод генерации эталонных групп номенклатуры"""
    def __create_nomenclature_groups(self):
        names = Repository.get_nomenclature_group_names()
        if names["raw_material"] not in self.nomenclature_groups:
            self.nomenclature_groups[names["raw_material"]] = \
                NomenclatureGroupModel(names["raw_material"])
        if names["product"] not in self.nomenclature_groups:
            self.nomenclature_groups[names["product"]] = \
                NomenclatureGroupModel(names["product"])
        if names["consumable"] not in self.nomenclature_groups:
            self.nomenclature_groups[names["consumable"]] = \
                NomenclatureGroupModel(names["consumable"])
    
    """Список номенклатур"""
    @property
    def nomenclatures(self) -> List[NomenclatureModel]:
        return self.data[Repository.nomenclatures_key]

    """Метод добавления номенклатур"""
    def __create_nomeclatures(self):
        groups_names = Repository.get_nomenclature_group_names()
        units_names = Repository.get_measure_unit_names()
        raw_material = self.nomenclature_groups[groups_names["raw_material"]]
        mu_egg = self.measure_units[units_names["egg"]]
        mu_milli = self.measure_units[units_names["milliliter"]]
        mu_sausage = self.measure_units[units_names["sausage"]]
        mu_gramm = self.measure_units[units_names["gramm"]]

        eggs = NomenclatureModel.create_eggs(raw_material, mu_egg)
        sunflower_oil = NomenclatureModel.create_sunflower_oil(
            raw_material, mu_milli
        )
        milk = NomenclatureModel.create_milk(raw_material, mu_milli)
        sausages = NomenclatureModel.create_sausages(raw_material, mu_sausage)
        salt = NomenclatureModel.create_salt(raw_material, mu_gramm)

        self.nomenclatures.append(eggs)
        self.nomenclatures.append(sunflower_oil)
        self.nomenclatures.append(milk)
        self.nomenclatures.append(sausages)
        self.nomenclatures.append(salt)

    """Метод получения номенклатуры по имени"""
    def get_nomenclature(self, name: str) -> Optional[NomenclatureModel]:
        vld.is_str(name, "nomenclature name")

        for nom in self.data[Repository.nomenclatures_key]:
            if nom.name == name:
                return nom
        
        return None
    
    """Список рецептов"""
    @property
    def recipes(self) -> List[RecipeModel]:
        return self.data[Repository.recipes_key]

    """Метод добавления рецептов"""
    def __create_recipes(self):
        omelette = RecipeModel("Омлет")
        eggs = self.get_nomenclature("Яйца")
        sunflower_oil = self.get_nomenclature("Подсолнечное масло")
        milk = self.get_nomenclature("Молоко")
        sausages = self.get_nomenclature("Сосиски")
        salt = self.get_nomenclature("Соль")

        omelette.add_ingredient(eggs, 3)
        omelette.add_ingredient(sunflower_oil, 10)
        omelette.add_ingredient(milk, 200)
        omelette.add_ingredient(sausages, 1)
        omelette.add_ingredient(salt, 5)
        self.recipes.append(omelette)
    
    """Метод вызова методов генерации эталонных данных"""
    def start(self):
        self.__create_measure_units()
        self.__create_nomenclature_groups()
        self.__create_nomeclatures()
        self.__create_recipes()
