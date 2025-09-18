import json
import pathlib
from src.models.company_model import CompanyModel

"""
TODO
1. Метод convert - часть load с получением значений из файла
2. Setting инкапсулирует CompanyModel
3. В Settings только CompanyModel, а в CompanyModel все свойства и поля
4. Задание делать в отдельной ветке, в конце Pull Request в master и в отклик - ссылка на Pull Request
"""
class SettingsManager:
    __file_name: str = ""
    __company: CompanyModel = None

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        if not value.strip():
            return
        if not pathlib.Path(value).exists():
            return
        self.__file_name = value.strip()

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.default()

    def __new__(cls, file_name: str):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SettingsManager, cls).__new__(cls)
        return cls.instance

    def company_settings(self) -> CompanyModel:
        return self.__company
    
    def load(self) -> bool:
        if not self.__file_name.strip():
            raise FileNotFoundError(f"No target file: {self.file_name}")
        try:
            file = open(self.file_name)
            data = json.load(file)
            if "company" in data:
                item = data["company"]
                self.__company.name = item["name"]
                self.__company.inn = item["inn"]
                return True
            return False
        except:
            return False
    
    def default(self):
        self.__company = CompanyModel()
        self.__company.name = "Дефолт"