from pydantic import BaseModel
from src.core.validator import Validator as vld
from src.core.event_type import EventType


"""
Интерфейс для объектов, имеющих метод handle() с обработкой некоторых событий
"""
class IHandleable:
    
    # Метод для обработки событий
    def handle(self, event: EventType, params: BaseModel):
        vld.validate(event, EventType, "event")
        vld.validate(params, BaseModel, "params")
