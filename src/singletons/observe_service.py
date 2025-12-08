from typing import List, Any
from fastapi import Request, Response
from pydantic import BaseModel
from src.core.validator import Validator as vld
from src.core.event_type import EventType
from src.core.ihandleable import IHandleable
from src.core.event_params import *


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
    def create_event(self, event: EventType, params: BaseModel):
        for instance in self.__handlers:
            instance.handle(event, params)
    
    """Вызвать событие попытки добавления новой модели в репозиторий"""
    def try_add_model_event(self, model: Any):
        from src.core.abstract_model import AbstractModel

        vld.validate(model, AbstractModel, "model")
        self.create_event(
            EventType.TRY_ADD_MODEL,
            ModelAddParams(unique_code=model.unique_code,
                           model_type=type(model).__name__)
        )
    
    """Вызвать событие подтверждения добавления"""
    def model_added_event(self, model: Any):
        from src.core.abstract_model import AbstractModel

        vld.validate(model, AbstractModel, "model")
        self.create_event(
            EventType.MODEL_ADDED,
            ModelAddParams(unique_code=model.unique_code,
                           model_type=type(model).__name__)
        )
    
    """Вызвать событие попытки изменения поля модели"""
    def try_edit_model_field_event(self, model: Any, field: str, value: Any):
        from src.core.abstract_model import AbstractModel

        vld.validate(model, AbstractModel, "model")
        vld.is_str(field, "field name")
        self.create_event(
            EventType.TRY_EDIT_FIELD_MODEL,
            ModelEditFieldParams(
                unique_code=model.unique_code,
                model_type=type(model).__name__,
                field=field,
                value=value
            )
        )
    
    """Вызвать событие подтверждения изменения модели"""
    def model_field_edited_event(self, model: Any, field: str, value: Any):
        from src.core.abstract_model import AbstractModel

        vld.validate(model, AbstractModel, "model")
        vld.is_str(field, "field name")
        self.create_event(
            EventType.MODEL_FIELD_EDITED,
            ModelEditFieldParams(
                unique_code=model.unique_code,
                model_type=type(model).__name__,
                field=field,
                value=value
            )
        )

    """Вызвать событие попытки удаления модели из репозитория"""
    def try_delete_model_event(self, unique_code: str):
        vld.is_str(unique_code, "unique_code")
        self.create_event(
            EventType.TRY_DELETE_MODEL,
            ModelBaseParams(unique_code=unique_code)
        )
    
    """Вызвать событие блокировки удаления модели"""
    def block_model_deleting(self, unique_code: str, blocked_code: str):
        vld.is_str(unique_code, "unique_code")
        vld.is_str(blocked_code, "blocked_code")
        self.create_event(
            EventType.BLOCK_MODEL_DELETING,
            BlockModelDeleting(unique_code=unique_code,
                               blocked_code=blocked_code)
        )
    
    """Вызвать событие подтверждения удаления модели"""
    def model_deleted_event(self, unique_code: str):
        vld.is_str(unique_code, "unique_code")
        self.create_event(
            EventType.MODEL_DELETED,
            ModelBaseParams(unique_code=unique_code)
        )
    
    """Вызвать событие изменения поля настроек"""
    def settings_value_changed_event(self, field: str, value: Any):
        vld.is_str(field, "field")
        self.create_event(
            EventType.SETTINGS_VALUE_CHANGED,
            SettingsFieldParams(field=field, value=value)
        )
    
    """Вызвать событие получения веб-запроса"""
    def web_route_called_event(self, request: Request):
        vld.validate(request, Request, "request")
        self.create_event(
            EventType.WEB_ROUTE_CALLED,
            WebRequestCalledParams(method=request.method,
                                   route=request.url.path,
                                   request_body=request.query_params,)
        )
    
    """Вызвать событие отправки ответа на веб-запрос"""
    def web_route_answered_event(
        self,
        request: Request,
        response: Response,
        time: float
    ):
        vld.validate(request, Request, "request")
        self.create_event(
            EventType.WEB_ROUTE_ANSWERED,
            WebRequestAnsweredParams(method=request.method,
                                     route=request.url.path,
                                     request_body=request.query_params,
                                     status_code=response.status_code,
                                     time=time)
        )
