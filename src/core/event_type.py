from enum import Enum, auto


"""Типы событий"""
class EventType(Enum):
    
    # Удаление модели из репозитория
    DELETE_MODEL = auto()
