import uvicorn
from typing import List, Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import date

from src.core.schemes import FilterScheme
from src.core.response_format import ResponseFormat
from src.core.http_responses import (TextResponse, JsonResponse, ErrorResponse,
                                     FormatResponse, JsonFileResponse)

from src.dtos.filter_dto import FilterDto

from src.logics.tbs_calculator import TbsCalculator
from src.logics.factory_entities import FactoryEntities
from src.logics.factory_converters import FactoryConverters

from src.filtration.filter_operator import FilterOperator as op
from src.filtration.filter_prototype import FilterPrototype

from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.singletons.settings_manager import SettingsManager


settings_file = "data/settings.json"
start_service = StartService()
settings_manager = SettingsManager()
factory_entities = FactoryEntities()
factory_converters = FactoryConverters()

app = FastAPI()


@app.get("/api/status")
def status():
    """Проверить доступность REST API"""
    return TextResponse("success")


@app.get("/api/responses/formats")
def get_response_formats():
    """Доступные форматы ответов"""
    content = [format.name.lower() for format in ResponseFormat]
    return JsonResponse(content)


@app.get("/api/responses/models")
def get_response_models():
    """Типы моделей, доступные для формирования ответов"""
    content = [key for key in Repository.keys()]
    return JsonResponse(content)


@app.get("/api/responses/build")
def build_response(format: str, model: str):
    """
    Сформировать ответ для моделей в переданном формате:
    - `format`: строковое обозначение формата ответа
    - `model`: строковое обозначения типа моделей
    """
    formats = [format.name.lower() for format in ResponseFormat]
    if format is None:
        return ErrorResponse("param 'format' must be transmitted")
    format = format.lower()
    if format not in formats:
        return ErrorResponse(
            f"not such format '{format}'. Available: {formats}"
        )
    
    model_types = [key for key in Repository.keys()]
    if model is None:
        return ErrorResponse("param 'model' must be transmitted")
    if model not in model_types:
        return ErrorResponse(
            f"not such model '{model}'. Available: {model_types}"
        )

    models = list(start_service.repository.data[model].values())
    result = factory_entities.create(format).build(models)

    return FormatResponse(result, format)


@app.get("/api/recipes")
def get_recipes():
    """Получить список рецептов в формате JSON"""
    key = Repository.recipes_key
    recipes = list(start_service.repository.data[key].values())
    result = factory_converters.convert(recipes)

    return JsonResponse(result)


@app.get("/api/recipes/{unique_code}")
def get_recipe(unique_code: str):
    """
    Получить рецепт в формате JSON по его уникальному коду:
    - `unique_code`: уникальный код рецепта в хранилище
    """
    recipe = start_service.repository.get(unique_code=unique_code)
    result = factory_converters.convert(recipe)

    return JsonResponse(result)


@app.get("/api/tbs")
def get_tbs(
    storage_code: str,
    start: date,
    end: date, 
):
    """
    Таблица оборотно-сальдовой ведомости (Trial Balance Sheet, TBS)
    - `storage_code`: уникальный код склада
    - `start`: начальная дата отчёта
    - `end`: дата окончания отчёта
    """
    storage = start_service.repository.get(unique_code=storage_code)
    if storage is None:
        return ErrorResponse(f"Storage with code '{storage_code}' is null")
    
    if start >= end:
        return ErrorResponse(f"End date must be later than start date")
    
    tbs_lines = TbsCalculator.calculate(storage, start, end)
    return HTMLResponse(
        factory_entities.create(ResponseFormat.HTML_TABLE).build(tbs_lines)
    )


@app.post("/api/tbs/filtration")
def get_tbs(
    storage_code: str,
    start: date,
    end: date, 
    filters: Optional[List[FilterScheme]] = None
):
    """
    Таблица оборотно-сальдовой ведомости (Trial Balance Sheet, TBS) с полем 
    для дополнительной фильтрации строк ОСВ
    - `storage_code`: уникальный код склада
    - `start`: начальная дата отчёта
    - `end`: дата окончания отчёта
    - `filters`: опциональные фильтры, применяемые к транзакциям
    """
    storage = start_service.repository.get(unique_code=storage_code)
    if storage is None:
        return ErrorResponse(f"Storage with code '{storage_code}' is null")
    
    if start >= end:
        return ErrorResponse(f"End date must be later than start date")
    
    tbs_lines = TbsCalculator.calculate(storage, start, end)
    try:
        if filters is not None:
            prototype = FilterPrototype(tbs_lines).clone(filters)
            tbs_lines = prototype.data
        return HTMLResponse(
            factory_entities.create(ResponseFormat.HTML_TABLE)\
                .build(tbs_lines)
        )
    except Exception as e:
        return ErrorResponse(e)


@app.post("/api/catalog/download")
def save_all_data():
    """
    Скачивание JSON файла с данными обо всех моделях, хранимых в Repository
    """

    data = start_service.data
    file_content = factory_converters.convert(data)

    return JsonFileResponse(file_content)


@app.get("/api/catalog/filtration/operators")
def get_filtration_operators():
    """Доступные операторы фильтрации моделей"""
    content = [operator.value for operator in op]
    return JsonResponse(content)


@app.post("/api/catalog/filtration")
def get_filtered_data(model_type: str, filters: List[FilterScheme]):
    """
    Отфильтрованные модели репозитория
    - `model_type`: обозначение фильтруемых моделей
    - `filters`: список фильтров, применяемых к моделям
    """
    model_types = [key for key in Repository.keys()]
    if model_type not in model_types:
        return ErrorResponse(
            f"Not such model '{model_type}'. Available: {model_types}"
        )
    
    models = list(start_service.repository.data[model_type].values())
    filters_dto = [FilterDto().load(filter.model_dump())
                   for filter in filters]
    
    try:
        prototype = FilterPrototype(models).clone(filters_dto)
        models = prototype.data
        result = factory_converters.convert(models)
        return JsonResponse(result)
    except Exception as e:
        return ErrorResponse(e)
    

if __name__ == "__main__":
    settings_manager.load(settings_file)
    start_service.start(settings_file)
    uvicorn.run(app=app,
                host="localhost",
                port=8081)
