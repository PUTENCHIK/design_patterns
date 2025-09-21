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
        if not isinstance(value, str):
            raise TypeError("Field 'name' must be string")
        value = value.strip()
        if not value:
            raise ValueError("")
        self.__name = value
    
    @property
    def inn(self) -> str:
        return self.__inn
    
    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Field 'inn' must be string")
        value = value.strip()
        if len(value) != 12 or not value.isdigit():
            raise ValueError("")
        self.__inn = value

    @property
    def account(self) -> str:
        return self.__account
    
    @account.setter
    def account(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Field 'account' must be string")
        value = value.strip()
        if len(value) != 11 or not value.isdigit():
            raise ValueError("")
        self.__account = value

    @property
    def corr_account(self) -> str:
        return self.__corr_account
    
    @corr_account.setter
    def corr_account(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Field 'corr_account' must be string")
        value = value.strip()
        if len(value) != 11 or not value.isdigit():
            raise ValueError("")
        self.__corr_account = value

    @property
    def bik(self) -> str:
        return self.__bik
    
    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Field 'bik' must be string")
        value = value.strip()
        if len(value) != 9 or not value.isdigit():
            raise ValueError("")
        self.__bik = value

    @property
    def ownership(self) -> str:
        return self.__ownership
    
    @ownership.setter
    def ownership(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Field 'ownership' must be string")
        value = value.strip()
        if len(value) != 5:
            raise ValueError("")
        self.__ownership = value

    def __init__(self):
        pass
