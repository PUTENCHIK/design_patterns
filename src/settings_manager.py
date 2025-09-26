import json
import pathlib
from src.settings import Settings

"""
TODO
1. Счета, бик и инн - числа
2. Валидация полей должна быть вынесена в отдельные функции
3. Правильное оформление тестов (есть рекомендации Microsoft в репозитории преподавателя)
4. Поля в settings.json могут задаваться как int/str
"""
class SettingsManager:
    __instance = None
    __file_name: str = ""
    __settings: Settings = None

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Settings file name must be string")
        value = value.strip()
        if not value:
            raise ValueError("Settings file name can't be empty")
        if not pathlib.Path(value).exists():
            raise FileNotFoundError(f"No such file: {value}")
        self.__file_name = value
    
    @property
    def settings(self) -> Settings:
        return self.__settings

    @settings.setter
    def settings(self, value: Settings):
        if isinstance(value, Settings):
            self.__settings = value

    def __init__(self):
        self.default()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def load(self, file_name: str) -> bool:
        self.file_name = file_name
        path = pathlib.Path(self.file_name).absolute()
        if not path.exists():
            return False
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                return self.convert(json.load(file))
        except:
            return False
    
    def convert(self, data: dict) -> bool:
        item = data["company"]
        self.settings.company.name = item["name"]
        self.settings.company.inn = item["inn"]
        self.settings.company.account = item["account"]
        self.settings.company.corr_account = item["corr_account"]
        self.settings.company.bik = item["bik"]
        self.settings.company.ownership = item["ownership"]
        return True
    
    def default(self):
        self.settings = Settings()
        self.settings.company.name = "Default Name"
        self.settings.company.inn = "000000000000"
        self.settings.company.account = "00000000000"
        self.settings.company.corr_account = "00000000000"
        self.settings.company.bik = "000000000"
        self.settings.company.ownership = "owner"
