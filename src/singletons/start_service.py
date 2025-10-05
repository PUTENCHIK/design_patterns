from typing import Optional
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.singletons.repository import Repository


class StartService:
    # Ссылка на экземпляр StartService
    __instance = None

    # Ссылка на объект Repository
    __repository: Optional[Repository] = Repository()

    def __init__(self):
        self.data[Repository.measure_unit_key] = dict()
        self.data[Repository.nomenclature_group_key] = dict()

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
    def measure_units(self) -> dict:
        return self.data[Repository.measure_unit_key]

    """Метод генерации эталонных единиц измерения"""
    def __create_measure_units(self):
        gramm = MeasureUnitModel.create_gramm()
        kilo = MeasureUnitModel.create_kilo(gramm)
        if gramm.name not in self.measure_units:
            self.measure_units[gramm.name] = gramm
        if kilo.name not in self.measure_units:
            self.measure_units[kilo.name] = kilo
    
    """Эталонные группы номенклатуры репозитория"""
    @property
    def nomenclature_groups(self) -> dict:
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

    
    """Метод вызова методов генерации эталонных данных"""
    def start(self):
        self.__create_measure_units()
        self.__create_nomenclature_groups()
