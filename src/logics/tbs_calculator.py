from typing import List
from datetime import date, datetime
from src.core.validator import Validator as vld
from src.logics.tbs_line import TbsLine
from src.models.storage_model import StorageModel
from src.singletons.start_service import StartService


"""Класс для расчёта оборотно-сальдовой ведомости"""
class TbsCalculator:
    
    @staticmethod
    def calculate(
        storage: StorageModel, 
        start: date, 
        end: date
    ) -> List[TbsLine]:
        vld.validate(storage, StorageModel, "storage")
        vld.validate(start, date, "start date")
        vld.validate(end, date, "end date")

        start = datetime(start.year, start.month, start.day)
        end = datetime(end.year, end.month, end.day, 23, 59, 59)

        result = list()
        data = StartService().repository.transactions_data

        for nom_key, stor_dict in data.items():
            nomenclature = StartService().repository.get(unique_code=nom_key)
            line = TbsLine(nomenclature=nomenclature)
            list_ = stor_dict.get(storage.unique_code, list())
            for dt, count in list_:
                if dt < start:
                    line.start_count += count
                elif dt <= end:
                    if count > 0:
                        line.income += count
                    else:
                        line.outgo += count
                
            result += [line]

        return result
