import unittest
from src.core.abstract_model import AbstractModel


class TestAbstractModel(unittest.TestCase):

    # Инициализация двух абстрактных моделей
    def test_abstractmodel_eq_compare_models_not_returns_false(self):
        # Подготовка
        model1 = AbstractModel()
        model2 = AbstractModel()
        # Проверка
        assert model1 != model2
    
    # Инициализация двух абстрактных моделей
    def test_abstractmodel_eq_compare_models_with_same_id_returns_true(self):
        # Подготовка
        model1 = AbstractModel()
        model2 = AbstractModel()
        model1.unique_code = model2.unique_code
        # Проверка
        assert model1.unique_code == model2.unique_code


if __name__ == "__main__":
    unittest.main()
