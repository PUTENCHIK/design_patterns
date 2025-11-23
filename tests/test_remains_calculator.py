import unittest
from datetime import date
from src.dtos.filter_dto import FilterDto
from src.logics.remains_calculator import RemainsCalculator
from src.filtration.filter_operator import FilterOperator as op
from src.filtration.filter_prototype import FilterPrototype
from src.singletons.start_service import StartService
from src.singletons.settings_manager import SettingsManager


class TestRemainsCalculator(unittest.TestCase):
    # Объект сервиса
    __start_service: StartService = StartService()

    # Объект менеджера настроек
    __settings_manager: SettingsManager = SettingsManager()

    def setUp(self):
        self.__settings_manager.load("tests/data/settings_valid.json")
        self.__start_service.start("tests/data/settings_models.json")

        return super().setUp()
    
    # При передаче методу calculate() даты до даты блокировки, он возвращает
    # столько же остатков, сколько было сохранено для даты блокировки
    def test_remainscalculator_calculate_date_before_block_date_returns_remains_from_repo(self):
        # Подготовка
        block_remains = list(self.__start_service.remains.values())
        
        # Действие
        remains = RemainsCalculator.calculate(date(2025, 1, 1))
        
        # Проверка
        assert len(block_remains) == len(remains)
    
    # При подсчёте остатков на 31.01.2025 все остатки находятся на
    # главном складе, и соль в количестве 9800, а молоко - 2.5
    def test_remainscalculator_calculate_valid_date_returns_remains_on_single_storage(self):
        # Подготовка
        date_ = date(2025, 1, 31)
        storage = self.__start_service.repository.get_by_name("Главный склад")
        if storage is None:
            raise Exception("No need storage into repository")
        
        # Действие
        remains = RemainsCalculator.calculate(date_)
        
        # Проверка
        main_storage_remains = FilterPrototype(remains).clone([
            FilterDto("storage", op.EQUAL, storage)
        ])
        salt_remain = FilterPrototype(remains).clone([
            FilterDto("nomenclature.name", op.EQUAL, "соль")
        ])
        milk_remain = FilterPrototype(remains).clone([
            FilterDto("nomenclature.name", op.EQUAL, "молоко")
        ])

        assert len(main_storage_remains.data) == len(remains)
        assert len(salt_remain.data) == 1 and salt_remain.data[0].value == 9800
        assert len(milk_remain.data) == 1 and milk_remain.data[0].value == 2.5
    
    # При подсчёте остатков на 02.02.2025 на главном складе 4 позиции остатков,
    # а на втором - 1
    def test_remainscalculator_calculate_valid_date_returns_remains_on_two_storages(self):
        # Подготовка
        date_ = date(2025, 2, 2)
        stor1 = self.__start_service.repository.get_by_name("Главный склад")
        stor2 = self.__start_service.repository.get_by_name("Второй склад")
        if stor1 is None or stor2 is None:
            raise Exception("No need storages into repository")
        
        # Действие
        remains = RemainsCalculator.calculate(date_)
        
        # Проверка
        main_storage_remains = FilterPrototype(remains).clone([
            FilterDto("storage", op.EQUAL, stor1)
        ])
        second_storage_remains = FilterPrototype(remains).clone([
            FilterDto("storage", op.EQUAL, stor2)
        ])

        assert len(main_storage_remains.data) == 4
        assert len(second_storage_remains.data) == 1
    
    # При подсчёте остатков за период с 01.02.2025 по 02.02.2025 возвращается
    # только 1 остаток
    def test_remainscalculator_getremainsforperiod_period_before_transactions_returns_empty_list(self):
        # Подготовка
        start = date(2025, 2, 1)
        end = date(2025, 2, 2)
        nom = self.__start_service.repository.get_by_name("подсолнечное масло")
        storage = self.__start_service.repository.get_by_name("Второй склад")
        if nom is None or storage is None:
            raise Exception("No need nomenclature or storage into repository")
        
        # Действие
        remains = RemainsCalculator.get_remains_for_period(
            start_date=start,
            end_date=end
        )
        
        # Проверка
        assert len(remains) == 1
        assert remains[0].nomenclature == nom
        assert remains[0].storage == storage


if __name__ == "__main__":
    unittest.main()
