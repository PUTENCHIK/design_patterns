class CompanyModel:
    __name: str = ""            # Наименование
    __inn: str = ""             # ИНН (12)
    __account: str = ""         # Счёт (11)
    __corr_account: str = ""    # Корреспондентский счет (11)
    __bik: str = ""             # БИК (9)
    __ownership: str = ""       # Вид собственности (5)

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
        value = value.strip()
        if value and len(value) == 12 and value.isdigit():
            self.__inn = value

    @property
    def account(self) -> str:
        return self.__account
    
    @account.setter
    def account(self, value: str):
        value = value.strip()
        if value and len(value) == 11 and value.isdigit():
            self.__account = value

    @property
    def corr_account(self) -> str:
        return self.__corr_account
    
    @corr_account.setter
    def corr_account(self, value: str):
        value = value.strip()
        if value and len(value) == 11 and value.isdigit():
            self.__corr_account = value

    @property
    def bik(self) -> str:
        return self.__bik
    
    @bik.setter
    def bik(self, value: str):
        value = value.strip()
        if value and len(value) == 9 and value.isdigit():
            self.__corr_account = value

    @property
    def ownership(self) -> str:
        return self.__ownership
    
    @ownership.setter
    def ownership(self, value: str):
        value = value.strip()
        if value and len(value) == 5:
            self.__ownership = value

    def __init__(self):
        pass
