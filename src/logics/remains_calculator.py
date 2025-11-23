from typing import List
from datetime import date, timedelta
from src.core.validator import Validator as vld
from src.dtos.filter_dto import FilterDto
from src.logics.tbs_calculator import TbsCalculator
from src.models.remain_model import RemainModel
from src.filtration.filter_operator import FilterOperator
from src.filtration.filter_prototype import FilterPrototype
from src.singletons.start_service import StartService
from src.singletons.settings_manager import SettingsManager


"""Класс для расчёта остатков на момент переданной даты"""
class RemainsCalculator:
    
    @staticmethod
    def get_remains_for_period(
        start_date: date,
        end_date: date,
    ) -> List[RemainModel]:
        vld.validate(start_date, date, "start_date")
        vld.validate(end_date, date, "end_date")
        storages = StartService().storages.values()
        remains = list()

        for storage in storages:
            # Для каждого склада получаем остатки за период
            tbs_lines = TbsCalculator.calculate(
                storage=storage,
                start=start_date,
                end=end_date,
                zero_turnovers=False,
                without_start_count=True
            )
            # Фильтруем линии ОСВ, у которых конечный остаток равен 0
            without_zero = FilterPrototype(tbs_lines)
            tbs_lines = without_zero.clone([
                FilterDto("end_count", FilterOperator.NOT_EQUAL, 0)
            ]).data
            for line in tbs_lines:
                remains += [
                    RemainModel(nomenclature=line.nomenclature,
                                storage=storage,
                                measure_unit=line.measure_unit,
                                value=line.end_count)
                ]
        return remains

    @staticmethod
    def calculate(
        date_: date
    ) -> List[RemainModel]:
        block_remains = list(StartService().remains.values())
        block_date = SettingsManager().settings.block_date

        # Переданная дата раньше даты блокировки
        if date_ <= block_date:
            return block_remains
        # Иначе - нужно добавить остатки открытого периода
        else:
            all_remains = {
                r.hash_key(): r
                for r in block_remains
            }
            open_remains = RemainsCalculator.get_remains_for_period(
                start_date=block_date + timedelta(days=1),
                end_date=date_,
            )
            for new_remain in open_remains:
                if new_remain.hash_key() in all_remains:
                    all_remains[new_remain.hash_key()].value += \
                        new_remain.value
                else:
                    all_remains[new_remain.hash_key()] = new_remain
            
            return list(all_remains.values())
