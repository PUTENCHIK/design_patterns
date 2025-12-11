import time
import uvicorn
from typing import List, Optional
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from datetime import date
from contextlib import asynccontextmanager

from src.core.schemes import (FilterScheme, NomenclatureGroupScheme,
                              NomenclatureScheme, MeasureUnitScheme,
                              StorageScheme)
from src.core.response_format import ResponseFormat
from src.core.http_responses import (TextResponse, JsonResponse, ErrorResponse,
                                     FormatResponse, JsonFileResponse)

from src.dtos.filter_dto import FilterDto
from src.dtos.nomenclature_group_dto import NomenclatureGroupDto
from src.dtos.nomenclature_dto import NomenclatureDto
from src.dtos.measure_unit_dto import MeasureUnitDto
from src.dtos.storage_dto import StorageDto

from src.logics.tbs_calculator import TbsCalculator
from src.logics.factory_entities import FactoryEntities
from src.logics.factory_converters import FactoryConverters
from src.logics.remains_calculator import RemainsCalculator

from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.measure_unit_model import MeasureUnitModel
from src.models.storage_model import StorageModel

from src.logging.logger import Logger

from src.filtration.filter_operator import FilterOperator as op
from src.filtration.filter_prototype import FilterPrototype

from src.singletons.repository import Repository
from src.singletons.model_manager import ModelManager
from src.singletons.start_service import StartService
from src.singletons.observe_service import ObserveService
from src.singletons.settings_manager import SettingsManager


logger = Logger()
settings_file = "data/settings.json"
remains_file = "data/remains.json"
start_service = StartService()
settings_manager = SettingsManager()
factory_entities = FactoryEntities()
factory_converters = FactoryConverters()


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings_manager.load(settings_file)
    start_service.start(settings_file, remains_file)
    yield
    settings_manager.save_block_date()
    start_service.save_remains()


app = FastAPI(lifespan=lifespan)
groups_router = APIRouter(
    prefix="/api/nomenclature_groups",
    tags=["nomenclature_groups"]
)
nomenclatures_router = APIRouter(
    prefix="/api/nomenclatures",
    tags=["nomenclatures"]
)
units_router = APIRouter(
    prefix="/api/measure_units",
    tags=["measure_units"]
)
storages_router = APIRouter(
    prefix="/api/storages",
    tags=["storages"]
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    ObserveService().web_route_called_event(request)

    start_time = time.time()
    response = await call_next(request)
    time_processed = time.time() - start_time

    ObserveService().web_route_answered_event(
        request, response, time_processed
    )
    return response


@app.get("/api/status")
def status():
    """Проверить доступность REST API"""
    return TextResponse("success")


@app.get("/api/settings")
def get_app_settings():
    """Получить настройки приложения"""
    result = FactoryConverters().convert(settings_manager.settings)
    return JsonResponse(result)


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


@app.get("/api/remains/block-date")
def get_block_date():
    """
    Дата блокировки складских оборотов
    """
    return JsonResponse(
        {"value": str(settings_manager.settings.block_date)}
    )


@app.post("/api/remains/block-date")
def set_block_date(value: date):
    """
    Установка новой даты блокировки складских оборотов
    """
    try:
        if settings_manager.settings.block_date != value:
            settings_manager.settings.block_date = value
            start_service.calc_remains()
            message = "block date updated"
        else:
            message = f"block date already is {value}"
        return JsonResponse(
            {"result": message}
        )
    except Exception as ex:
        return ErrorResponse(
            f"Failed to set new block date: {ex}"
        )


@app.get("/api/remains")
def get_remains_on_date(date_: date):
    """
    Получение остатков на складах на момент переданной даты
    """
    remains = RemainsCalculator.calculate(date_)
    return HTMLResponse(
        factory_entities.create(ResponseFormat.HTML_TABLE).build(remains)
    )


@groups_router.get("/")
def get_nomenclature_group(unique_code: str):
    """
    Получение группы номенклатуры по уникальному коду
    """
    groups = list(start_service.nomenclature_groups.values())
    group = FilterPrototype(groups).clone([
        FilterDto("unique_code", op.EQUAL, unique_code)
    ]).data
    group = group[0] if len(group) > 0 else None
    
    return JsonResponse(factory_converters.convert(group))


@groups_router.post("/")
def add_nomenclature_group(dto: NomenclatureGroupScheme):
    """
    Добавление новой группы номенклатуры
    """
    try:
        model = ModelManager.add_model(
            repo_key=Repository.nomenclature_group_key,
            model_type=NomenclatureGroupModel,
            dto=NomenclatureGroupDto().load(dto.model_dump())
        )
        return JsonResponse(factory_converters.convert(model))
    except Exception as e:
        return ErrorResponse(e)


@groups_router.put("/")
def edit_nomenclature_group(unique_code: str, dto: NomenclatureGroupScheme):
    """
    Изменение группы номенклатуры
    """
    try:
        model = ModelManager.edit_model(
            unique_code=unique_code,
            model_type=NomenclatureGroupModel,
            dto=NomenclatureGroupDto().load(dto.model_dump())
        )
        return JsonResponse(factory_converters.convert(model))
    except Exception as e:
        return ErrorResponse(e)


@groups_router.delete("/")
def delete_nomenclature_group(unique_code: str):
    """
    Удаление группы номенклатуры
    """
    try:
        result = ModelManager.delete_model(
            unique_code=unique_code,
            model_type=NomenclatureGroupModel
        )
        return JsonResponse({"result": result})
    except Exception as e:
        return ErrorResponse(e)


@nomenclatures_router.get("/")
def get_nomenclature(unique_code: str):
    """
    Получение номенклатуры по уникальному коду
    """
    nomenclatures = list(start_service.nomenclatures.values())
    nomenclature = FilterPrototype(nomenclatures).clone([
        FilterDto("unique_code", op.EQUAL, unique_code)
    ]).data
    nomenclature = nomenclature[0] if len(nomenclature) > 0 else None
    
    return JsonResponse(factory_converters.convert(nomenclature))


@nomenclatures_router.post("/")
def add_nomenclature(dto: NomenclatureScheme):
    """
    Добавление новой номенклатуры
    """
    try:
        model = ModelManager.add_model(
            repo_key=Repository.nomenclatures_key,
            model_type=NomenclatureModel,
            dto=NomenclatureDto().load(dto.model_dump())
        )
        return JsonResponse(factory_converters.convert(model))
    except Exception as e:
        return ErrorResponse(e)


@nomenclatures_router.put("/")
def edit_nomenclature(unique_code: str, dto: NomenclatureScheme):
    """
    Изменение номенклатуры
    """
    try:
        model = ModelManager.edit_model(
            unique_code=unique_code,
            model_type=NomenclatureModel,
            dto=NomenclatureDto().load(dto.model_dump(exclude_none=True))
        )
        return JsonResponse(factory_converters.convert(model))
    except Exception as e:
        return ErrorResponse(e)


@nomenclatures_router.delete("/")
def delete_nomenclature(unique_code: str):
    """
    Удаление номенклатуры
    """
    try:
        result = ModelManager.delete_model(
            unique_code=unique_code,
            model_type=NomenclatureModel
        )
        return JsonResponse({"result": result})
    except Exception as e:
        return ErrorResponse(e)


@units_router.get("/")
def get_measure_unit(unique_code: str):
    """
    Получение единицы измерения по уникальному коду
    """
    units = list(start_service.measure_units.values())
    unit = FilterPrototype(units).clone([
        FilterDto("unique_code", op.EQUAL, unique_code)
    ]).data
    unit = unit[0] if len(unit) > 0 else None
    
    return JsonResponse(factory_converters.convert(unit))


@units_router.post("/")
def add_measure_unit(dto: MeasureUnitScheme):
    """
    Добавление новой единицы измерения
    """
    try:
        model = ModelManager.add_model(
            repo_key=Repository.measure_unit_key,
            model_type=MeasureUnitModel,
            dto=MeasureUnitDto().load(dto.model_dump())
        )
        return JsonResponse(factory_converters.convert(model))
    except Exception as e:
        return ErrorResponse(e)


@units_router.put("/")
def edit_measure_unit(unique_code: str, dto: MeasureUnitScheme):
    """
    Изменение единицы измерения
    """
    try:
        model = ModelManager.edit_model(
            unique_code=unique_code,
            model_type=MeasureUnitModel,
            dto=MeasureUnitDto().load(dto.model_dump(exclude_none=True))
        )
        return JsonResponse(factory_converters.convert(model))
    except Exception as e:
        return ErrorResponse(e)


@units_router.delete("/")
def delete_measure_unit(unique_code: str):
    """
    Удаление единицы измерения
    """
    try:
        result = ModelManager.delete_model(
            unique_code=unique_code,
            model_type=MeasureUnitModel
        )
        return JsonResponse({"result": result})
    except Exception as e:
        return ErrorResponse(e)


@storages_router.get("/")
def get_storage(unique_code: str):
    """
    Получение склада по уникальному коду
    """
    storages = list(start_service.storages.values())
    storage = FilterPrototype(storages).clone([
        FilterDto("unique_code", op.EQUAL, unique_code)
    ]).data
    storage = storage[0] if len(storage) > 0 else None
    
    return JsonResponse(factory_converters.convert(storage))


@storages_router.post("/")
def add_storage(dto: StorageScheme):
    """
    Добавление нового склада
    """
    try:
        model = ModelManager.add_model(
            repo_key=Repository.storages_key,
            model_type=StorageModel,
            dto=StorageDto().load(dto.model_dump())
        )
        return JsonResponse(factory_converters.convert(model))
    except Exception as e:
        return ErrorResponse(e)


@storages_router.put("/")
def edit_storage(unique_code: str, dto: StorageScheme):
    """
    Изменение склада
    """
    try:
        model = ModelManager.edit_model(
            unique_code=unique_code,
            model_type=StorageModel,
            dto=StorageDto().load(dto.model_dump(exclude_none=True))
        )
        return JsonResponse(factory_converters.convert(model))
    except Exception as e:
        return ErrorResponse(e)


@storages_router.delete("/")
def delete_storage(unique_code: str):
    """
    Удаление склада
    """
    try:
        result = ModelManager.delete_model(
            unique_code=unique_code,
            model_type=StorageModel
        )
        return JsonResponse({"result": result})
    except Exception as e:
        return ErrorResponse(e)


app.include_router(groups_router)
app.include_router(nomenclatures_router)
app.include_router(units_router)
app.include_router(storages_router)

if __name__ == "__main__":
    uvicorn.run(app=app,
                host="0.0.0.0",
                port=8080)
