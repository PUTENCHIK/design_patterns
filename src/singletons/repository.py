from typing import List, Any, Optional
from src.core.validator import Validator as vld


"""Репозиторий данных"""
class Repository:
    # Ссылка на объект Repository
    __instance = None

    # Словарь наименований моделей
    __data = dict()

    # Ключ для единиц измерения
    measure_unit_key: str = "measure_units"

    # Ключ для групп номенклатуры
    nomenclature_group_key: str = "nomenclature_groups"
    
    # Ключ для номенклатур
    nomenclatures_key: str = "nomenclatures"

    # Ключ для рецептов
    recipes_key: str = "recipes"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    """Словарь с объектами приложения"""
    @property
    def data(self) -> dict:
        return self.__data
    
    """Метод получения всех ключей Reposity по шаблону `*_key`"""
    @staticmethod
    def keys() -> List[str]:
        return [getattr(Repository, f) for f in dir(Repository)
                if not f.startswith("_") and f.endswith("_key")]
    
    """Инициализация списков в словаре данных"""    
    def initalize(self):
        # Все ключи будут ссылаться на словари формата name: object
        # с соответствующими объектами
        for key in Repository.keys():
            self.data[key] = dict()
    
    """Метод получения объекта в памяти по имени"""
    def get(self, item_name: str) -> Optional[Any]:
        vld.is_str(item_name, "item_name")
        for key in self.keys():
            items: dict = self.data[key]
            for _, item in items.items():
                if item.name.lower() == item_name.lower():
                    return item
        return None
