from enum import Enum, auto


"""Типы событий"""
class EventType(Enum):

    # Инициализация добавления модели в репозиторий
    TRY_ADD_MODEL = auto()

    # Модель добавлена в репозиторий
    MODEL_ADDED = auto()

    # Инициализация изменения поля модели
    TRY_EDIT_FIELD_MODEL = auto()

    # Поле модели изменена
    MODEL_FIELD_EDITED = auto()
    
    # Инициализация удаления модели из репозитория
    TRY_DELETE_MODEL = auto()

    # Блокировка удаления модели
    BLOCK_MODEL_DELETING = auto()

    # Модель удалена из репозитория
    MODEL_DELETED = auto()

    # Поле настроек изменено
    SETTINGS_VALUE_CHANGED = auto()

    # Обращение к маршруту в main.py
    WEB_ROUTE_CALLED = auto()

    # Отправка ответа на запрос в main.py
    WEB_ROUTE_ANSWERED = auto()

