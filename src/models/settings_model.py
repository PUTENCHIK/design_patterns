from src.core.abstract_model import AbstractModel
from src.models.company_model import CompanyModel


"""Модель настроек

Инкапсулирует модель компании.
"""
class SettingsModel(AbstractModel):
    # Ссылка на объект модели компании
    __company: CompanyModel = None

    def __init__(self):
        super().__init__()
        self.__company = CompanyModel()

    """Поле компании"""
    @property
    def company(self) -> CompanyModel:
        return self.__company
