import time
import random
import pathlib
import unittest
from datetime import datetime, date

from src.dtos.filter_dto import FilterDto
from src.logics.factory_entities import FactoryEntities
from src.models.transaction_model import TransactionModel
from src.filtration.filter_operator import FilterOperator as op
from src.filtration.filter_prototype import FilterPrototype
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.singletons.settings_manager import SettingsManager


class ResultLine:

    block_date: str
    transactions_count: int
    time_record: float

    def __init__(
        self,
        block_date: datetime,
        transactions_count: int,
        time_record: float
    ):
        self.block_date = block_date
        self.transactions_count = transactions_count
        self.time_record = time_record


class TestRemainsCalculatorTimeRecords(unittest.TestCase):

    # Количество генерируемых транзакций
    transactions_count: int = 5000

    # Дата первой генерируемой транзакции
    start_date: datetime = datetime(2010, 1, 1)

    # Дата последней генерируемой транзакции
    end_date: datetime = datetime(2025, 1, 1)

    # Директория, в которую будут сохраняться файлы
    __save_directory: str = "tests/remains_time_record/"

    # Объект менеджера настроек
    __settings_manager: SettingsManager = SettingsManager()

    # Объект сервиса
    __start_service: StartService = StartService()

    def setUp(self):
        self.__settings_manager.load("tests/data/settings_valid.json")
        self.__start_service.start("tests/data/settings_models.json")
        return super().setUp()

    # Метод процедурной генерации множества транзакций
    def _create_bunch_of_trainsactions(self):
        self.__start_service.repository.clear(Repository.transactions_key)
        noms = list(self.__start_service.nomenclatures.values())
        storages = list(self.__start_service.storages.values())

        dt = datetime(self.start_date.year,
                      self.start_date.month,
                      self.start_date.day)
        delta = (self.end_date - self.start_date) / self.transactions_count

        for _ in range(self.transactions_count):
            nom = random.choice(noms)
            transaction = TransactionModel(
                datetime=dt,
                nomenclature=nom,
                storage=random.choice(storages),
                measure_unit=nom.measure_unit,
                count=random.randint(10, 100) / 10 * \
                    (1 if random.randint(0, 1) else -1)
            )
            self.__start_service.transactions[transaction.unique_code] = \
                transaction
            dt = dt + delta
    
    # Нагрузочный тест с сохранением результатов замеров подсчёта остатков для
    # разных дат блокировки
    def test_save_time_records(self):
        self._create_bunch_of_trainsactions()
        dir_ = pathlib.Path(self.__save_directory)
        dir_.mkdir(exist_ok=True)

        trans_file_path = dir_ / "transactions.md"
        trans_file_path.touch()
        with open(trans_file_path, 'w', encoding="utf-8") as file:
            results = FactoryEntities().create("html_table").build(
                list(self.__start_service.transactions.values())
            )
            file.write(results)
            file.close()
        
        result_file_path = dir_ / "results.md"
        result_file_path.touch()

        results = list()
        transactions = list(self.__start_service.transactions.values())
        prototype = FilterPrototype(transactions)

        test_dates_count = 5
        delta = (self.end_date - self.start_date) / test_dates_count
        block_datetimes = [self.start_date + delta * i
                           for i in range(test_dates_count+1)]
        block_dates = [date(d.year, d.month, d.day)
                       for d in block_datetimes]
        for block_date, block_datetime in zip(block_dates, block_datetimes):
            self.__settings_manager.settings.block_date = block_date
            time_start = time.time()
            self.__start_service.calc_remains()
            time_end = time.time()

            block_trans = prototype.clone([
                FilterDto("datetime", op.LESSER_EQUAL, block_datetime)
            ])

            results += [
                ResultLine(block_date,
                           len(block_trans.data),
                           time_end - time_start)
            ]
        
        with open(result_file_path, 'w', encoding="utf-8") as file:
            result = FactoryEntities().create("html").build(results)
            file.write(
                "# Результаты тестирования скорости подсчёта остатков\n\n"
            )
            file.write(f"Всего транзакций: {len(prototype.data)}\n\n")
            file.write(result)
            file.close()


if __name__ == "__main__":
    unittest.main()
