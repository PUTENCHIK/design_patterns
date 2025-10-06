import unittest
from src.core.exceptions import WrongTypeException
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.models.nomenclature_model import NomenclatureModel


class TestStartService(unittest.TestCase):
    __start_service: StartService = StartService()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start()
    
    # Метод __create_measure_units() создаёт единицы измерения
    def test_startservice_create_measure_units_create_units_added_units(self):
        # Подготовка
        count = len(self.__start_service.measure_units)
        # Проверка
        assert count > 0
    
    # Метод __create_measure_units() создаёт единицу измерения 'килограмм',
    # базовая единица которого - это грамм из того же словаря
    def test_startservice_create_measure_units_create_units_kilo_contains_gramm(self):
        # Подготовка
        units = self.__start_service.measure_units
        names = Repository.get_measure_unit_names()
        gramm = units[names["gramm"]]
        kilo = units[names["kilo"]]
        # Проверка
        assert kilo.base_unit == gramm
    
    # Повторный вызов метода start() не должен обновлять единицы измерения
    def test_startservice_start_run_method_again_measure_units_are_same(self):
        # Подготовка
        names = Repository.get_measure_unit_names()
        name1, name2 = names["gramm"], names["kilo"]
        units = self.__start_service.measure_units
        # Действие
        self.__start_service.start()
        new_units = self.__start_service.measure_units
        # Проверка
        assert units[name1] == new_units[name1]
        assert units[name2] == new_units[name2]
    
    # Повторный вызов метода start() не должен обновлять группы номенклатур
    def test_startservice_start_run_method_again_nomenclature_groups_are_same(self):
        # Подготовка
        names = Repository.get_nomenclature_group_names()
        name = names["raw_material"]
        unit = self.__start_service.nomenclature_groups[name]
        # Действие
        self.__start_service.start()
        new_unit = self.__start_service.nomenclature_groups[name]
        # Проверка
        assert unit == new_unit
    
    # Метод __create_nomeclatures() создаёт номенклатуры
    def test_startservice_create_nomeclatures_create_nomeclatures_added_nomenclatures(self):
        # Подготовка
        count = len(self.__start_service.nomenclatures)
        # Проверка
        assert count > 0
    
    # Метод get_nomenclature() возвращает номенклатуру при передаче
    # имени существующего объекта
    def test_startservice_get_nomenclature_pass_existing_name_returns_object(self):
        # Подготовка
        name = "Курица"
        self.__start_service.data[Repository.nomenclatures_key].append(
            NomenclatureModel(name)
        )
        # Действие
        eggs = self.__start_service.get_nomenclature("Яйца")
        chicken = self.__start_service.get_nomenclature(name)
        # Проверка
        assert isinstance(eggs, NomenclatureModel)
        assert isinstance(chicken, NomenclatureModel)
    
    # Метод get_nomenclature() возвращает None при передаче имени
    # несуществующего объекта
    def test_startservice_get_nomenclature_pass_not_existing_name_returns_none(self):
        # Подготовка
        name = "Несуществующий продукт"
        # Действие
        chicken = self.__start_service.get_nomenclature(name)
        # Проверка
        assert chicken is None
    
    # Метод get_nomenclature() бросает исключение при передаче
    # невалидного значения имени
    def test_startservice_get_nomenclature_pass_invalid_name_raises_exception(self):
        # Проверка
        with self.assertRaises(WrongTypeException):
            self.__start_service.get_nomenclature(0)


if __name__ == "__main__":
    unittest.main()
