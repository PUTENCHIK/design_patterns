from typing import Optional
from src.core.abstract_model import AbstractModel


"""Модель для характеристики группы номенклатуры"""
class NomenclatureGroupModel(AbstractModel):
    # Наименование (50)
    # Наследуется от AbstractModel

    def __init__(
        self,
        name: Optional[str] = None
    ):
        super().__init__()
        if name is not None:
            self.name = name
