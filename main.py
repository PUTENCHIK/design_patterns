import connexion
from flask import request

from src.core.response_format import ResponseFormat
from src.core.http_responses import (TextResponse, JsonResponse, ErrorResponse,
                                     FormatResponse)
from src.logics.factory_entities import FactoryEntities
from src.logics.factory_converters import FactoryConverters
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.singletons.settings_manager import SettingsManager


settings_file = "data/settings.json"
start_service = StartService()
settings_manager = SettingsManager()
factory_entities = FactoryEntities()
factory_converters = FactoryConverters()

app = connexion.FlaskApp(__name__)

"""Проверить доступность REST API"""
@app.route("/api/status", methods=['GET'])
def status():
    return TextResponse("success")


"""Доступные форматы ответов"""
@app.route("/api/responses/formats", methods=['GET'])
def get_response_formats():
    content = [format.name.lower() for format in ResponseFormat]
    return JsonResponse(content)


"""Типы моделей, доступные для формирования ответов"""
@app.route("/api/responses/models", methods=['GET'])
def get_response_models():
    content = [key for key in Repository.keys()]
    return JsonResponse(content)


"""Сформировать ответ для моделей (model) в переданном формате (format)"""
@app.route("/api/responses/build", methods=['GET'])
def build_response():
    format = request.args.get('format')
    formats = [format.name.lower() for format in ResponseFormat]
    if format is None:
        return ErrorResponse("param 'format' must be transmitted")
    format = format.lower()
    if format not in formats:
        return ErrorResponse(
            f"not such format '{format}'. Available: {formats}"
        )
    
    model = request.args.get('model')
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


@app.route("/api/recipes", methods=['GET'])
def get_recipes():
    key = Repository.recipes_key
    recipes = list(start_service.repository.data[key].values())
    result = factory_converters.convert(recipes)

    return JsonResponse(result)


@app.route("/api/recipes/<unique_code>", methods=['GET'])
def get_recipe(unique_code: str):
    recipe = start_service.repository.get(unique_code=unique_code)
    result = factory_converters.convert(recipe)

    return JsonResponse(result)


if __name__ == '__main__':
    start_service.start(settings_file)
    settings_manager.load(settings_file)
    app.run(host="localhost", port=8080)
