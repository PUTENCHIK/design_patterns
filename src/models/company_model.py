import json
from pathlib import Path


class CompanyModel:
    __name: str = ""
    __inn: str = ""

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        if value.strip():
            self.__name = value.strip()
    
    @property
    def inn(self) -> str:
        return self.__inn
    
    @inn.setter
    def inn(self, value: str):
        if value.strip():
            self.__inn = value.strip()

    def __init__(self):
        pass
