from typing import List, Any, Optional, Dict, Tuple
from datetime import datetime
from src.core.validator import Validator as vld
from src.core.exceptions import ParamException
from src.utils import get_properties


"""Репозиторий данных"""
class Repository:
    # Ссылка на объект Repository
    __instance = None

    # Словарь наименований моделей
    __data = dict()

    # Вложенный словарь с данными о транзакциях
    __transactions_data: Dict[str, Dict[str, List[Tuple[datetime, float]]]]

    # Ключ для единиц измерения
    measure_unit_key: str = "measure_units"

    # Ключ для групп номенклатуры
    nomenclature_group_key: str = "nomenclature_groups"
    
    # Ключ для номенклатур
    nomenclatures_key: str = "nomenclatures"

    # Ключ для рецептов
    recipes_key: str = "recipes"

    # Ключ для складов
    storages_key: str = "storages"

    # Ключ для транзакций
    transactions_key: str = "transactions"

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
        return [getattr(Repository, f) for f in get_properties(Repository)
                if f.endswith("_key")]
    
    """Данные о транзакциях"""
    @property
    def transactions_data(self) -> Dict[str, Dict[str, List[Tuple[datetime, float]]]]:
        return self.__transactions_data
    
    @transactions_data.setter
    def transactions_data(self, value: Dict):
        vld.is_dict(value, "transactions_data")
        self.__transactions_data = value

    """Инициализация списков в словаре данных"""    
    def initalize(self):
        # Все ключи будут ссылаться на словари формата name: object
        # с соответствующими объектами
        for key in Repository.keys():
            self.data[key] = dict()
        self.transactions_data = dict()
    
    """Метод получения объекта в памяти по имени"""
    def get_by_name(self, name: str) -> Optional[Any]:
        vld.is_str(name, "item_name")
        for key in self.keys():
            items: list = self.data[key].values()
            items = [item
                     for item in items
                     if item.name.lower() == name.lower()]
            if len(items):
                return items[0]
        
        return None

    """Метод получения объекта в памяти по уникальному коду"""
    def get_by_unique_code(self, unique_code: str) -> Optional[Any]:
        vld.is_str(unique_code, "item_unique_code")
        for key in self.keys():
            items: dict = self.data[key]
            for item in items.values():
                if item.unique_code == unique_code:
                    return item
        return None

    """Универсальный метод получения объекта в памяти"""
    def get(
        self,
        unique_code: Optional[str] = None,
        name: Optional[str] = None
    ) -> Optional[Any]:
        if unique_code is not None:
            return self.get_by_unique_code(unique_code)
        elif name is not None:
            return self.get_by_name(name)
        else:
            raise ParamException(
                "Must be transmitted either unique_code, or name, "
                "but both is None"
            )
