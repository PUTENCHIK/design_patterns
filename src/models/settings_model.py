from typing import Union
from datetime import date
from src.core.validator import Validator as vld
from src.core.exceptions import ParamException
from src.core.abstract_model import AbstractModel
from src.core.response_format import ResponseFormat
from src.models.company_model import CompanyModel
from src.logging.logging_mode import LoggingMode
from src.logging.logging_level import LoggingLevel
from src.singletons.observe_service import ObserveService


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

    # Самая ранняя дата, с которой считаются остатки
    start_date: date = date(1900, 1, 1)

    # Дата блокировки складских остатков
    __block_date: date

    # Уровень логирования
    __logging_level: LoggingLevel = LoggingLevel.DEBUG

    # Режим логирования
    __logging_mode: LoggingMode = LoggingMode.CONSOLE_FILE

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
        ObserveService().settings_value_changed_event("response_format", value)
    
    """Поле запуска в первый раз"""
    @property
    def first_start(self) -> bool:
        return self.__first_start
    
    @first_start.setter
    def first_start(self, value: bool):
        vld.validate(value, bool, "first_start")
        self.__first_start = value
        ObserveService().settings_value_changed_event("first_start", value)

    """Поле формата даты и времени"""
    @property
    def datetime_format(self) -> str:
        return self.__datetime_format
    
    @datetime_format.setter
    def datetime_format(self, value: str):
        vld.is_str(value, "datetime_format")
        self.__datetime_format = value
        ObserveService().settings_value_changed_event("datetime_format", value)
    
    """Поле даты закрытого периода"""
    @property
    def block_date(self) -> date:
        return self.__block_date
    
    @block_date.setter
    def block_date(self, value: date):
        vld.validate(value, date, "block_date")
        if value < self.start_date:
            raise ParamException(
                f"Block date must be later than start date: {self.start_date}"
            )
        self.__block_date = value
        ObserveService().settings_value_changed_event("block_date", value)
    
    """Поле уровня логирования"""
    @property
    def logging_level(self) -> LoggingLevel:
        return self.__logging_level
    
    @logging_level.setter
    def logging_level(self, value: Union[str, LoggingLevel]):
        vld.validate(value, (str, LoggingLevel), "logging_level")
        if isinstance(value, LoggingLevel):
            self.__logging_level = value
            ObserveService().settings_value_changed_event(
                "logging_level",
                self.logging_level
            )
        else:
            if value.lower() in LoggingLevel:
                self.__logging_level = LoggingLevel(value)
                ObserveService().settings_value_changed_event(
                    "logging_level",
                    self.logging_level
                )
            else:
                raise ParamException(
                    f"No such logging level: {value}, available: "
                    f"{LoggingLevel._member_names_}"
                )
    
    """Поле режима логирования"""
    @property
    def logging_mode(self) -> LoggingMode:
        return self.__logging_mode
    
    @logging_mode.setter
    def logging_mode(self, value: Union[str, LoggingMode]):
        vld.validate(value, (str, LoggingMode), "logging_mode")
        if isinstance(value, LoggingMode):
            self.__logging_mode = value
            ObserveService().settings_value_changed_event(
                "logging_mode",
                self.logging_mode
            )
        else:
            if value.lower() in LoggingMode:
                self.__logging_mode = LoggingMode(value)
                ObserveService().settings_value_changed_event(
                    "logging_mode",
                    self.logging_mode
                )
            else:
                raise ParamException(
                    f"No such logging mode: {value}, available: "
                    f"{LoggingMode._member_names_}"
                )
    
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
        self.__block_date = self.start_date
