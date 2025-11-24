import json
from datetime import date, datetime
from src.core.validator import Validator as vld
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

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.default()
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
    
    """Метод загрузки файла настроек"""
    def load(self, file_name: str) -> bool:
        self.settings.default()
        self.file_name = file_name
        try:
            with open(self.file_name, mode='r', encoding='utf-8') as file:
                settings = json.load(file)
                return (
                    self.convert_company_data(
                        settings["company"]) and
                    self.convert_response_format(
                        settings["default_response_format"]) and
                    self.convert_first_start(
                        settings["first_start"]) and
                    self.convert_datetime_format(
                        settings["datetime_format"]) and
                    self.convert_block_date(
                        settings["block_date"]
                    )
                )
        except:
            return False
    
    """Метод извлечения данных компании из загуженного файла настроек"""
    def convert_company_data(self, data: dict) -> bool:
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
    
    """Метод загрузки формата ответов по умолчанию из файла настроек"""
    def convert_response_format(self, data: str) -> bool:
        from src.logics.factory_entities import FactoryEntities
        try:
            format = FactoryEntities.match_formats[data]
            self.settings.response_format = format
            return True
        except KeyError:
            return False
    
    """Метод загрузки параметра запуска сервиса в первый раз"""
    def convert_first_start(self, data: str) -> bool:
        try:
            self.settings.first_start = bool(data)
            return True
        except KeyError:
            return False
    
    """Метод загрузки формата даты и времени"""
    def convert_datetime_format(self, data: str) -> bool:
        try:
            self.settings.datetime_format = data
            return True
        except KeyError:
            return False
    
    """Метод загрузки даты блокировки складских остатков"""
    def convert_block_date(self, data: str) -> bool:
        try:
            dt = datetime.strptime(data, "%Y-%m-%d")
            self.settings.block_date = date(dt.year, dt.month, dt.day)
            return True
        except Exception:
            return False
    
    """Метод инициализации стандартных значений полей"""
    def default(self):
        self.settings = SettingsModel()
        self.settings.company.name = "Default Name"
        self.settings.company.ownership = "owner"
    
    """Метод сохранения даты блокировки в файле настроек"""
    def save_block_date(self):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            content = json.load(file)
            file.close()
        
        if content:
            content["block_date"] = str(self.settings.block_date)
            result = json.dumps(content, ensure_ascii=False, indent=4)
            with open(self.file_name, 'w', encoding='utf-8') as file:
                file.write(result)
                file.close()
