from typing import Any
from fastapi import Request, Response
from pydantic import BaseModel


class ModelBaseParams(BaseModel):
    # Уникальный код удаляемой модели
    unique_code: str


class BlockModelDeleting(ModelBaseParams):
    # Код модели, заблокировавшей удаление
    blocked_code: str


class ModelAddParams(ModelBaseParams):
    # Тип модели
    model_type: str


class ModelEditFieldParams(ModelAddParams):
    # Изменяемое поле
    field: str
    # Новое значение
    value: Any


class SettingsFieldParams(BaseModel):
    # Изменяемое поле настроек
    field: str
    # Новое значение
    value: Any


class WebRequestCalledParams(BaseModel):
    # Метод запроса
    method: str
    # Маршрут запроса
    route: str
    # Тело запроса
    request_body: dict


class WebRequestAnsweredParams(WebRequestCalledParams):
    # Статус ответа
    status_code: int
    # Время, потраченное на формирование ответа
    time: float
