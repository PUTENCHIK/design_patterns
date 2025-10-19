import json
from src.core.validator import Validator as vld
from src.core.response_format import ResponseFormat
from src.models.settings_model import SettingsModel


"""Менеджер настроек

Предназначен для управления настройками и хранения параметров приложения.
"""
class SettingsManager:
    # Ссылка на экземпляр SettingsManager
    __instance = None

    # Абсолютный путь до файла с загруженными настройками
    __file_name: str = ""

    # Инкупсулирумый объект настроек
    __settings: SettingsModel

    def __init__(self):
        self.default()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    """Абсолютный путь к файлу с настройками"""
    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        self.__file_name = vld.is_file_exists(value)
    
    """Настройки с хранящейся моделью компании"""
    @property
    def settings(self) -> SettingsModel:
        return self.__settings

    @settings.setter
    def settings(self, value: SettingsModel):
        vld.validate(value, SettingsModel, "settings")
        self.__settings = value
    
    """Поле формата настроек, инкапсулируемое settings"""
    @property
    def response_format(self) -> ResponseFormat:
        return self.settings.response_format
    
    @response_format.setter
    def response_format(self, value: ResponseFormat):
        self.settings.response_format = value
    
    """Метод загрузки файла настроек"""
    def load(self, file_name: str) -> bool:
        self.file_name = file_name
        try:
            with open(self.file_name, mode='r', encoding='utf-8') as file:
                settings = json.load(file)
                if "company" in settings:
                    return self.convert(settings["company"])
        except:
            return False
    
    """Метод извлечения данных компании из загуженного файла настроек"""
    def convert(self, data: dict) -> bool:
        vld.is_dict(data, "data")

        # Поля модели компании, которые могут быть заполнены
        company_model_fields = [
            field for field in dir(self.settings.company)
            if not field.startswith("_")
        ]
        # Ключи загруженного объекта настроек
        matching_keys = [
            key for key in data.keys()
            if key in company_model_fields
        ]

        try:
            for key in matching_keys:
                setattr(self.settings.company, key, data[key])
            return True
        except:
            return False
    
    """Метод инициализации стандартных значений полей"""
    def default(self):
        self.settings = SettingsModel()
        self.settings.company.name = "Default Name"
        self.settings.company.ownership = "owner"
