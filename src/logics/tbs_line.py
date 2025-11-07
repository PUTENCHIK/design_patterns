from typing import Optional, Union
from datetime import datetime
from src.core.validator import Validator as vld
from src.core.exceptions import OperationException
from src.models.transaction_model import TransactionModel
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_model import NomenclatureModel


"""Объект для хранения информации ОСВ об одной номенклатуре"""
class TbsLine:
    # Номенклатура
    __nomenclature: NomenclatureModel

    # Единица измерения (базовая для номенклатуры)
    __measure_unit: MeasureUnitModel

    # Начальный остаток
    __start_count: float = 0.0

    # Приход
    __income: float = 0.0

    # Расход
    __outgo: float = 0.0

    # Остаток на дату окончания (вычисляемое поле)
    
    def __init__(
        self,
        nomenclature: NomenclatureModel,
        start_count: Optional[float] = None,
        income: Optional[float] = None,
        outgo: Optional[float] = None,
    ):
        self.nomenclature = nomenclature
        base_unit, _ = self.nomenclature.measure_unit.get_base_unit()
        self.measure_unit = base_unit
        if start_count is not None:
            self.start_count = start_count
        if income is not None:
            self.income = income
        if outgo is not None:
            self.outgo = outgo

    """Поле номенклатуры"""
    @property
    def nomenclature(self) -> NomenclatureModel:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        vld.validate(value, NomenclatureModel, "nomenclature")
        self.__nomenclature = value
    
    """Поле единицы измерения"""
    @property
    def measure_unit(self) -> MeasureUnitModel:
        return self.__measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: MeasureUnitModel):
        vld.validate(value, MeasureUnitModel, "measure_unit")
        self.__measure_unit = value
    
    """Поле начального остатка"""
    @property
    def start_count(self) -> float:
        return self.__start_count
    
    @start_count.setter
    def start_count(self, value: Union[int, float]):
        vld.is_number(value, "start_count")
        self.__start_count = value
    
    """Поле прихода"""
    @property
    def income(self) -> float:
        return self.__income

    @income.setter
    def income(self, value: Union[int, float]):
        vld.is_number(value, "income")
        self.__income = value
    
    """Поле расхода"""
    @property
    def outgo(self) -> float:
        return self.__outgo

    @outgo.setter
    def outgo(self, value: Union[int, float]):
        vld.is_number(value, "outgo")
        self.__outgo = value
    
    """Поле конечного остатка"""
    @property
    def end_count(self) -> float:
        return self.__start_count + self.__income + self.__outgo
    
    """
    Метод, добавляющий значение транзакции к соответствующему полю __count
    в зависимости от даты транзакции
    """
    def add(self, trans: TransactionModel, start: datetime, end: datetime):
        vld.validate(trans, TransactionModel, "transaction")
        vld.validate(start, datetime, "start date")
        vld.validate(end, datetime, "end date")

        if self.nomenclature != trans.nomenclature:
            raise OperationException(
                f"Nomenclature of transaction must be "
                f"'{self.nomenclature.name}', not '{trans.nomenclature.name}'"
            )
        
        base_unit, coef = trans.measure_unit.get_base_unit()
        if self.measure_unit != base_unit:
            raise OperationException(
                f"Impossible to compare measure unit of transaction "
                f"('{trans.measure_unit.name}'), which super base unit is "
                f"'{base_unit.name}', and base unit of tbs line: "
                f"'{self.measure_unit.name}'"
            )

        count = trans.count * coef
        if trans.datetime < start:
            # Транзакция проведена до начальной даты
            self.__counts_before_start += [count]
        elif trans.datetime <= end:
            # Транзакция проведена в период между начальной и конечной датами
            self.__counts_before_end += [count]
        else:
            # Транзакция проведена после конечной даты и не влияет на ОСВ
            pass
