import pathlib
from typing import Union
from datetime import datetime
from pydantic import BaseModel

from src.core.validator import Validator as vld
from src.core.event_type import EventType
from src.core.event_params import *
from src.core.exceptions import ParamException
from src.core.ihandleable import IHandleable
from src.logging.logging_level import LoggingLevel
from src.logging.logging_mode import LoggingMode
from src.singletons.settings_manager import SettingsManager
from src.singletons.observe_service import ObserveService


"""
Класс-синглтон логов

Отслеживает события ObserveService и делает логи в зависимости от настроек
приложения
"""
class Logger(IHandleable):
    
    # Экземпляр класса-синглтона
    __instance = None

    # Формат сообщений логгера
    format_: str = "{datetime} - {level} - \"{text}\""

    # Приоритеты уровней логирования
    levels_priorities = [LoggingLevel.DEBUG, LoggingLevel.INFO,
                         LoggingLevel.WARNING, LoggingLevel.ERROR]
    
    # Директория для логирования
    __logging_dir: pathlib.Path

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            ObserveService.add(cls.__instance)
            cls.__instance.logging_dir = "./logs/"
        return cls.__instance
    
    """Поле пути до директории сохранения логов"""
    @property
    def logging_dir(self) -> pathlib.Path:
        return self.__logging_dir

    @logging_dir.setter
    def logging_dir(self, value: Union[str, pathlib.Path]):
        vld.validate(value, (str, pathlib.Path), "logging directory")
        if isinstance(value, str):
            value = pathlib.Path(value)
        value.mkdir(exist_ok=True)
        if not value.is_dir():
            raise ParamException(f"Path {value} is not directory")
        self.__logging_dir = value.absolute()

    """Метод логирования сообщений"""
    def log(
        self,
        level: LoggingLevel,
        text: str
    ):
        vld.validate(level, LoggingLevel, "logging level")
        vld.is_str(text, "log text")

        logging_level = SettingsManager().settings.logging_level

        # Если уровень логирования приложения выше, чем уровень лога
        if self.levels_priorities.index(level) < \
                self.levels_priorities.index(logging_level):
            return

        content = self.format_.format(
            datetime=datetime.now(),
            level=level.name,
            text=text.strip()
        )
        if SettingsManager().settings.logging_mode in \
                [LoggingMode.CONSOLE, LoggingMode.CONSOLE_FILE]:
            print(content)
        if SettingsManager().settings.logging_mode in \
                [LoggingMode.FILE, LoggingMode.CONSOLE_FILE]:
            self.write_into_file(content)

    """Метод получения файла логов на текущую дату"""
    def get_log_filename(self) -> str:
        dt = datetime.now()
        return f"log{dt.year}{dt.month}{dt.day}.log"

    """Метод записи в файл логов"""
    def write_into_file(self, content: str):
        self.logging_dir.mkdir(exist_ok=True)
        filename = self.get_log_filename()
        log_file_path = self.logging_dir / filename
        log_file_path.touch(exist_ok=True)
        with open(log_file_path, mode="a", encoding="utf-8") as file:
            file.write(content + "\n")
            file.close()

    """Обработка всех событий и их логирование"""
    def handle(self, event: EventType, params: BaseModel):
        super().handle(event, params)
        match event:
            case EventType.TRY_ADD_MODEL:
                self.log(LoggingLevel.INFO,
                         f"Try to add {params.model_type} "
                         f"with code '{params.unique_code}'")
            case EventType.MODEL_ADDED:
                self.log(LoggingLevel.INFO,
                         f"{params.model_type} with code "
                         f"'{params.unique_code}' was added")
            case EventType.TRY_EDIT_FIELD_MODEL:
                self.log(LoggingLevel.INFO,
                         f"Try to change field '{params.field}' to "
                         f"'{params.value}' at {params.model_type} with code "
                         f"'{params.unique_code}'")
            case EventType.MODEL_FIELD_EDITED:
                self.log(LoggingLevel.INFO,
                         f"'{params.field}' was changed to '{params.value}' "
                         f"at {params.model_type} with code "
                         f"'{params.unique_code}'")
            case EventType.TRY_DELETE_MODEL:
                self.log(LoggingLevel.INFO,
                         f"Try to delete model '{params.unique_code}'")
            case EventType.BLOCK_MODEL_DELETING:
                self.log(LoggingLevel.WARNING,
                         f"Deleting model '{params.unique_code}' was blocked "
                         f"by model '{params.blocked_code}'")
            case EventType.MODEL_DELETED:
                self.log(LoggingLevel.INFO,
                         f"Model '{params.unique_code}' was deleted")
            case EventType.SETTINGS_VALUE_CHANGED:
                self.log(LoggingLevel.INFO,
                         f"Settings field '{params.field}' was changed to "
                         f"'{params.value}'")
            case EventType.WEB_ROUTE_CALLED:
                self.log(LoggingLevel.DEBUG,
                         f"Called {params.method} {params.route} request "
                         f"with body {params.request_body}")
            case EventType.WEB_ROUTE_ANSWERED:
                self.log(LoggingLevel.DEBUG,
                         f"Formed answer for {params.method} {params.route} "
                         f"request with body: {params.request_body}; status: "
                         f"{params.status_code}, time: {params.time:.4f}s")
