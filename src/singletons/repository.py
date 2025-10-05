"""Репозиторий данных"""
class Repository:
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

    """Словарь с эталонными объектами приложения"""
    @property
    def data(self) -> dict:
        return self.__data
    
    """Наименования единиц измерения"""
    @staticmethod
    def get_measure_unit_names() -> dict:
        return {
            "gramm": "гр",
            "kilo": "кг",
            "milliliter": "мл",
            "egg": "яйцо",
            "sausage": "сосиска",
        }
    
    """Наименования групп номенклатуры"""
    @staticmethod
    def get_nomenclature_group_names() -> dict:
        return {
            "raw_material": "сырьё",
            "product": "товар",
            "consumable": "расходник",
        }
