from src.core.validator import Validator as vld
from src.core.event_type import EventType
from src.core.event_params import AbstractEventParams


"""
Интерфейс для объектов, имеющих метод handle() с обработкой некоторых событий
"""
class IHandleable:
    
    # Метод для обработки событий
    def handle(self, event: EventType, params: AbstractEventParams):
        vld.validate(event, EventType, "event")
        vld.validate(params, AbstractEventParams, "params")
