from src.models.company_model import CompanyModel


class Settings:
    __company: CompanyModel = None

    @property
    def company(self) -> CompanyModel:
        return self.__company
