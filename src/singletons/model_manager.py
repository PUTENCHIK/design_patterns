from typing import Optional
from src.core.validator import Validator as vld
from src.core.exceptions import ParamException, OperationException
from src.core.abstract_dto import AbstractDto
from src.core.abstract_model import AbstractModel
from src.singletons.start_service import StartService
from src.singletons.repository import Repository
from src.utils import get_properties


"""Класс для добавления, изменения и удаления объектов из репозитория"""
class ModelManager:
    
    """Метод для добавления новой модели в репозиторий"""
    @staticmethod
    def add_model(
        repo_key: str,
        model_type: AbstractModel,
        dto: AbstractDto
    ) -> Optional[AbstractModel]:
        model = model_type.from_dto(dto, StartService().repository)

        if repo_key not in Repository.keys():
            raise ParamException(
                f"No such key in repository: {repo_key}"
            )
        StartService().repository.data[repo_key][model.unique_code] = model

        return model
    
    """Метод для изменения моделей"""
    @staticmethod
    def edit_model(
        unique_code: str,
        model_type: AbstractModel,
        dto: AbstractDto
    ) -> Optional[AbstractModel]:
        model = StartService().repository.get_by_unique_code(unique_code)
        if model is None:
            raise OperationException(
                f"No '{model_type.__name__}' model with id: {unique_code}"
            )
        vld.validate(model, model_type, "model to edit")

        edited_model = model_type.from_dto(dto, StartService().repository)
        for prop in get_properties(model):
            if prop == "unique_code":
                continue
            edited_value = getattr(edited_model, prop)
            if getattr(model, prop) != edited_value:
                setattr(model, prop, edited_value)
        
        return model
    
    """Метод удаления модели по уникальному коду"""
    @staticmethod
    def delete_model(
        unique_code: str,
        model_type: AbstractModel,
    ) -> bool:
        model = StartService().repository.get_by_unique_code(unique_code)
        if model is None:
            raise OperationException(
                f"No '{model_type.__name__}' model with id: {unique_code}"
            )
        vld.validate(model, model_type, "model to delete")

        for key in Repository.keys():
            if unique_code in StartService().repository.data[key]:
                StartService().repository.data[key].pop(unique_code)
        
        return True
