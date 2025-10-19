import connexion
from flask import request

from src.core.response_format import ResponseFormat
from src.logics.factory_entities import FactoryEntities
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.singletons.settings_manager import SettingsManager


settings_file = "data/settings.json"
start_service = StartService()
settings_manager = SettingsManager()
factory = FactoryEntities()

app = connexion.FlaskApp(__name__)


"""Проверить доступность REST API"""
@app.route("/api/status", methods=['GET'])
def status():
    return {"status": "success"}


"""Доступные форматы ответов"""
@app.route("/api/responses/formats", methods=['GET'])
def get_response_formats():
    return [
        format.name.lower()
        for format in ResponseFormat
    ]

"""Типы моделей, доступные для формирования ответов"""
@app.route("/api/responses/models", methods=['GET'])
def get_response_models():
    return [
        key
        for key in Repository.keys()
    ]


"""Сформировать ответ для моделей (model) в переданном формате (format)"""
@app.route("/api/responses/build", methods=['GET'])
def build_response():
    format = request.args.get('format')
    if format is None:
        return {"error": "param 'format' must be transmitted"}
    format = format.lower()
    if format not in get_response_formats():
        return {
            "error": f"not such format '{format}'. Available: "
                    f"{get_response_formats()}"
        }
    
    model_type = request.args.get('model')
    if model_type is None:
        return {"error": "param 'model' must be transmitted"}
    if model_type not in get_response_models():
        return {
            "error": f"not such model '{model_type}'. "
                    f"Available: {get_response_models()}"
        }

    models = list(start_service.repository.data[model_type].values())

    return {"result": factory.create(format).build(models)}


if __name__ == '__main__':
    start_service.start(settings_file)
    settings_manager.load(settings_file)
    app.run(host="localhost", port=8080)
