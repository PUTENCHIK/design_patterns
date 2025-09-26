import unittest
from src.models.company_model import CompanyModel
from src.settings_manager import SettingsManager
from src.models.storage_model import StorageModel


class TestModels(unittest.TestCase):
    
    # Полностью пустое имя
    def test_no_name_company_model(self):
        model = CompanyModel()
        assert model.name == ""

    # Имя из пробелов
    def test_empty_name_company_model(self):
        model = CompanyModel()
        with self.assertRaises(ValueError):
            model.name = " "
    
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

        assert manager1.settings == manager2.settings
        assert manager1.settings.company == manager2.settings.company
    
    # Загрузка данных компании из settings.json
    def test_load_settings_valid_data(self):
        manager = SettingsManager()

        assert manager.load("settings.json")
        assert manager.settings.company.name == "Danny MAD Entertainment"
        assert manager.settings.company.inn == "385693061393"
        assert manager.settings.company.account == "34583289581"
        assert manager.settings.company.corr_account == "95847306800"
        assert manager.settings.company.bik == "458205943"
        assert manager.settings.company.ownership == "owner"
    
    # Загрузка данных компании из тестового файла в другой директории
    def test_load_settings_different_path(self):
        manager = SettingsManager()

        assert manager.load("tests/data/test_settings.json")
        assert manager.settings.company.name == "Test Company"
        assert manager.settings.company.inn == "123456789123"
        assert manager.settings.company.account == "12345678912"
        assert manager.settings.company.corr_account == "12345678912"
        assert manager.settings.company.bik == "123456789"
        assert manager.settings.company.ownership == "owner"
    
    # Присваивание полям модели компании невалидных данных
    def test_appropriate_model_unvalid_data(self):
        company = CompanyModel()

        with self.assertRaises(TypeError):
            company.name = 1
        with self.assertRaises(ValueError):
            company.name = ""
        
        with self.assertRaises(TypeError):
            company.inn = 123123
        with self.assertRaises(ValueError):
            company.inn = "not inn"
        
        with self.assertRaises(TypeError):
            company.account = 0x123
        with self.assertRaises(ValueError):
            company.account = "not account"
        
        with self.assertRaises(TypeError):
            company.corr_account = True
        with self.assertRaises(ValueError):
            company.corr_account = "not corr_account"
        
        with self.assertRaises(TypeError):
            company.bik = list()
        with self.assertRaises(ValueError):
            company.bik = "not bik"
        
        with self.assertRaises(TypeError):
            company.ownership = dict()
        with self.assertRaises(ValueError):
            company.ownership = "too long ownership"
    
    # Загрузка данных двух компаний из разных директорий
    def test_load_data_any_directory(self):
        manager = SettingsManager()
        settings_path1 = "../settings1.json" # /home/maxim/study/settings1.json
        settings_path2 = "/home/maxim/study/design_patterns/tests/data/inner_dir/settings2.json"

        assert manager.load(settings_path1)
        assert manager.settings.company.name == "Company 1"
        assert manager.load(settings_path2)
        assert manager.settings.company.name == "Company 2 from inner directory"
    
    # Проверка на сравнение двух разных моделей склада
    def test_equals_storage_model_create(self):
        storage1 = StorageModel()
        storage2 = StorageModel()

        assert storage1 != storage2

    # Проверка на сравнение двух моделей склада с одинаковым ID
    def test_equals_storage_model_create(self):
        storage1 = StorageModel()
        storage2 = StorageModel()
        storage2.id = storage1.id

        assert storage1 == storage2


if __name__ == "__main__":
    unittest.main()
