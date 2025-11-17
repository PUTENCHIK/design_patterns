import unittest
from datetime import datetime
from src.core.exceptions import ParamException
from src.dtos.filter_dto import FilterDto
from src.filtration.filter_prototype import FilterPrototype
from src.filtration.filter_operator import FilterOperator as op
from src.singletons.start_service import StartService


class TestFilterPrototype(unittest.TestCase):
    # Путь до файла с тестовыми настройками
    __file_name: str = "tests/data/settings_models.json"

    # Объект сервиса
    __start_service: StartService = StartService()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start(self.__file_name)

    # Тест с использованием двух фильтров, применяемых к моделям транзакций
    def test_filterprototype_filter_filter_transactions_by_nomenclature_and_unit_returns_valid_prototype(self):
        # Подготовка
        transactions = list(self.__start_service.transactions.values())
        prototype = FilterPrototype(transactions)
        # Действие
        filtered = prototype.filter([
            FilterDto("nomenclature.name", op.EQUAL, "соль"),
            FilterDto("measure_unit.name", op.LIKE, "грамм")
        ])
        # Проверка
        assert len(filtered.data) > 0
        assert len(prototype.data) > 0
        assert len(prototype.data) >= len(filtered.data)

    # Тест с фильтром транзакций по дате
    def test_filterprototype_filter_filter_transaction_by_datetime_returns_empty_prototype(self):
        # Подготовка
        transactions = list(self.__start_service.transactions.values())
        prototype = FilterPrototype(transactions)
        # Действие
        filtered = prototype.filter([
            FilterDto("datetime", op.GRATER_EQUAL, datetime(2025, 3, 1))
        ])
        # Проверка
        assert len(filtered.data) == 0
    
    # Фильтрация по несуществующему полю выкидывает исключение ParamException
    def test_filterprototype_filter_filter_transaction_by_date_returns_empty_prototype(self):
        # Подготовка
        transactions = list(self.__start_service.transactions.values())
        prototype = FilterPrototype(transactions)
        # Проверка
        with self.assertRaises(ParamException):
            prototype.filter([
                FilterDto("datetime.name", op.GRATER, datetime(2025, 1, 1))
            ])
    
    # Фильтрация для получения базовых единиц измерения
    def test_filterprototype_filter_filter_units_returns_base_units(self):
        # Подготовка
        units = list(self.__start_service.measure_units.values())
        prototype = FilterPrototype(units)
        # Подготовка
        filtered = prototype.filter([
            FilterDto("name", op.LIKE, "грамм литр"),
            FilterDto("coefficient", op.EQUAL, 1)
        ])
        # Проверка
        assert len(filtered.data) == 2


if __name__ == "__main__":
    unittest.main()
