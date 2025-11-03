import unittest
from src.models.transaction_model import TransactionModel
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.singletons.start_service import StartService


class TestTransactionModel(unittest.TestCase):
    
    # Синглтон сервиса
    __start_manager: StartService

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_manager = StartService()

    # Тест инициализации модели транзакции
    def test_transactionmodel_init_set_nomenclature_and_measure_unit_are_same(self):
        # Подготовка
        nomen = self.__start_manager.repository.get(name="яйца")
        unit = self.__start_manager.repository.get(name="штука")
        # Действие
        trans = TransactionModel(
            nomenclature=nomen,
            measure_unit=unit
        )
        # Проверка
        assert trans.nomenclature == nomen
        assert trans.measure_unit == unit


if __name__ == "__main__":
    unittest.main()