from typing import List
from src.core.validator import Validator as vld
from src.core.event_type import EventType
from src.core.event_params import AbstractEventParams, DeleteModelEventParams
from src.core.ihandleable import IHandleable


"""Класс-синглтон, хранящий экземпляры объектов с обработкой событий"""
class ObserveService:

    # Экземпляр класса ObserveService
    __instance = None

    # Экземпляры объектов, имеющие логику для обработки событий
    __handlers: List[IHandleable] = list()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    """Добавить объект под наблюдение"""
    @staticmethod
    def add(instance: IHandleable):
        vld.validate(instance, IHandleable, "instance")
        from src.core.abstract_model import AbstractModel
        if instance is None:
            return
        if type(instance) is AbstractModel:
            return
        if instance not in ObserveService.__handlers:
            ObserveService.__handlers += [instance]
    
    """Удалить из-под наблюдения"""
    @staticmethod
    def delete(instance: IHandleable):
        vld.validate(instance, IHandleable, "instance")
        from src.core.abstract_model import AbstractModel
        if instance is None:
            return
        if type(instance) is AbstractModel:
            return
        if instance not in ObserveService.__handlers:
            ObserveService.__handlers.remove(instance)
    
    """Вызвать событие у всех наблюдаемых экземпляров"""
    def create_event(self, event: EventType, params: AbstractEventParams):
        for instance in self.__handlers:
            instance.handle(event, params)
    
    """Вызвать событие удаления модели из репозитория"""
    def delete_model_event(self, unique_code: str):
        vld.is_str(unique_code, "unique_code")
        self.create_event(
            EventType.DELETE_MODEL,
            DeleteModelEventParams(unique_code)
        )
    