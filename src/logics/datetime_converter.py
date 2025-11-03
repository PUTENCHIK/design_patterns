from datetime import datetime 
from src.core.validator import Validator as vld
from src.core.abstract_converter import AbstractConverter
from src.singletons.settings_manager import SettingsManager


"""Конвертер класса datetime.datetime

Приводит объекты datetime к строковому представлению"""
class DatetimeConverter(AbstractConverter):

    def __init__(self):
        super().__init__()
    
    """Переопределённый метод convert
    
    Приводит datetime к строковому представлению в заданном формате"""
    def convert(self, object_: datetime) -> str:
        vld.validate(object_, datetime, "object")

        return object_.strftime(SettingsManager().settings.datetime_format)
