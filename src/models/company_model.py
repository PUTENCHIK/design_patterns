from __future__ import annotations
from typing import Optional
from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel


"""Модель компании

Предназначена для хранения данных об организации
"""
class CompanyModel(AbstractModel):
    # Наименование организации
    __name: str = ""

    # ИНН (12 символов)
    __inn: Optional[int] = None

    # Счёт (11 символов)
    __account: Optional[int] = None

    # Корреспондентский счет (11 символов)
    __corr_account: Optional[int] = None

    # БИК (9 символов)
    __bic: Optional[int] = None

    # Вид собственности (5 символов)
    __ownership: str = ""

    def __init__(
        self,
        settings = None
    ):
        super().__init__()
        if settings is not None:
            from src.models.settings_model import SettingsModel
            
            vld.validate(settings, SettingsModel, "settings")
            self.name = settings.company.name
            self.inn = settings.company.inn
            self.account = settings.company.account
            self.corr_account = settings.company.corr_account
            self.bic = settings.company.bic
            self.ownership = settings.company.ownership

    """Наименование организации"""
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        vld.is_str(value, "name")
        self.__name = value
    
    """ИНН организации"""
    @property
    def inn(self) -> Optional[int]:
        return self.__inn
    
    @inn.setter
    def inn(self, value: Optional[int]):
        vld.is_positive_int(value=value,
                            field_name="inn",
                            could_be_none=True,
                            len_=12,
                            strictly_len=True)
        self.__inn = value

    """Номер счёта компании"""
    @property
    def account(self) -> Optional[int]:
        return self.__account
    
    @account.setter
    def account(self, value: Optional[int]):
        vld.is_positive_int(value=value,
                            field_name="account",
                            could_be_none=True,
                            len_=11,
                            strictly_len=True)
        self.__account = value

    """Корреспондентский счёт"""
    @property
    def corr_account(self) -> Optional[int]:
        return self.__corr_account
    
    @corr_account.setter
    def corr_account(self, value: Optional[int]):
        vld.is_positive_int(value=value,
                            field_name="corr_account",
                            could_be_none=True,
                            len_=11,
                            strictly_len=True)
        self.__corr_account = value

    """БИК компании"""
    @property
    def bic(self) -> Optional[int]:
        return self.__bic
    
    @bic.setter
    def bic(self, value: Optional[int]):
        vld.is_positive_int(value=value,
                            field_name="bic",
                            could_be_none=True,
                            len_=9,
                            strictly_len=True)
        self.__bic = value

    """Вид собственности"""
    @property
    def ownership(self) -> str:
        return self.__ownership
    
    @ownership.setter
    def ownership(self, value: str):
        vld.is_str(value, "ownership", len_=5)
        self.__ownership = value
