import unittest
from src.models.company_model import CompanyModel
from src.settings_manager import SettingsManager


class TestModels(unittest.TestCase):
    
    # Полностью пустое имя
    def test_no_name_company_model(self):
        model = CompanyModel()
        assert model.name == ""

    # Имя из пробелов
    def test_empty_name_company_model(self):
        model = CompanyModel()
        model.name = " "
        assert model.name == ""
    
    # Непустое имя
    def test_new_name_company_model(self):
        model = CompanyModel()
        model.name = "Danny"
        assert model.name != ""

    # Загрузка существующего валидного файла настроек
    def test_load_data_company_model(self):
        manager = SettingsManager()

        assert manager.load("settings.json")
    
    # Проверка на синглтон  SettingsManager
    def test_equal_company_models(self):
        manager1 = SettingsManager()
        manager2 = SettingsManager()

        assert manager1.company_settings == manager2.company_settings
