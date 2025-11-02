from typing import List
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

    # Значения транзакций до начальной даты
    __counts_before_start: List[float]

    # Значения транзакций в промежутке между начальной и конечной датами
    __counts_before_end: List[float]

    # Приход (вычисляемое поле)

    # Расход (вычисляемое поле)

    # Остаток на дату окончания (вычисляемое поле)
    
    def __init__(self, transaction: TransactionModel):
        self.nomenclature = transaction.nomenclature
        base_unit, _ = self.nomenclature.measure_unit.get_base_unit()
        self.measure_unit = base_unit
        self.__counts_before_start = list()
        self.__counts_before_end = list()

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
        return sum(self.__counts_before_start)
    
    """Поле прихода"""
    @property
    def income(self) -> float:
        return sum([value
                    for value in self.__counts_before_end
                    if value > 0])
    
    """Поле расхода"""
    @property
    def outgo(self) -> float:
        return sum([value
                    for value in self.__counts_before_end
                    if value < 0])
    
    """Поле конечного остатка"""
    @property
    def end_count(self) -> float:
        return self.start_count + self.income + self.outgo
    
    """
    Метод, добавляющий значение транзакции к соответствующему полю __count
    в зависимости от даты транзакции
    """
    def add(self, trans: TransactionModel, start: datetime, end: datetime):
        vld.validate(trans, TransactionModel, "transaction")

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
