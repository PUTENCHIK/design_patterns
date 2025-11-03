from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.core.response_format import ResponseFormat
from src.models.company_model import CompanyModel


"""Модель настроек

Инкапсулирует модель компании.
"""
class SettingsModel(AbstractModel):
    # Ссылка на объект модели компании
    __company: CompanyModel = None

    # Формат ответов (по умолчанию JSON)
    __response_format: ResponseFormat

    # Запущен ли сервис в первый раз
    __first_start: bool

    # Формат даты и времени
    __datetime_format: str

    def __init__(self):
        super().__init__()
        self.default()

    """Поле компании"""
    @property
    def company(self) -> CompanyModel:
        return self.__company
    
    """Поле формата ответов"""
    @property
    def response_format(self) -> ResponseFormat:
        return self.__response_format
    
    @response_format.setter
    def response_format(self, value: ResponseFormat):
        vld.validate(value, ResponseFormat, "response format")
        self.__response_format = value
    
    """Поле запуска в первый раз"""
    @property
    def first_start(self) -> bool:
        return self.__first_start
    
    @first_start.setter
    def first_start(self, value: bool):
        vld.validate(value, bool, "first_start")
        self.__first_start = value

    """Поле формата даты и времени"""
    @property
    def datetime_format(self) -> str:
        return self.__datetime_format
    
    @datetime_format.setter
    def datetime_format(self, value: str):
        vld.is_str(value, "datetime_format")
        self.__datetime_format = value
    
    """Фабричный метод из DTO"""
    @staticmethod
    def from_dto(dto, repo):
        return super().from_dto(dto, repo)
    
    """Метод значений по умолчанию"""
    def default(self):
        self.__company = CompanyModel()
        self.__response_format = ResponseFormat.JSON
        self.__first_start = True
        self.__datetime_format = "%Y-%m-%d %H:%M:%S"
