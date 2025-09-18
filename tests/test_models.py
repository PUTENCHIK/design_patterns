import json
import pathlib
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

    # Имя из файла настроек
    def test_load_data_company_model(self):
        manager = SettingsManager("settings.json")

        assert manager.load()
    
    # Сравнение моделей
    def test_equal_company_models(self):
        file_path = "settings.json"

        manager1 = SettingsManager(file_path)
        manager2 = SettingsManager(file_path)

        assert manager1.company_settings == manager2.company_settings
