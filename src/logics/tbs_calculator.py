from typing import List, Dict
from datetime import date, datetime
from src.core.validator import Validator as vld
from src.dtos.filter_dto import FilterDto
from src.logics.tbs_line import TbsLine
from src.models.storage_model import StorageModel
from src.models.transaction_model import TransactionModel
from src.filtration.filter_operator import FilterOperator as op
from src.filtration.filter_prototype import FilterPrototype
from src.singletons.repository import Repository
from src.singletons.start_service import StartService


"""Класс для расчёта оборотно-сальдовой ведомости"""
class TbsCalculator:
    
    @staticmethod
    def calculate(
        storage: StorageModel, 
        start: date, 
        end: date,
        zero_turnovers: bool = True,
        without_start_count: bool = False
    ) -> List[TbsLine]:
        vld.validate(storage, StorageModel, "storage")
        vld.validate(start, date, "start date")
        vld.validate(end, date, "end date")

        start = datetime(start.year, start.month, start.day)
        end = datetime(end.year, end.month, end.day, 23, 59, 59)
        transactions = list(StartService().transactions.values())

        filters = [
            FilterDto("storage.unique_code",
                      op.EQUAL,
                      storage.unique_code),
            FilterDto("datetime",
                      op.LESSER_EQUAL,
                      end),
        ]
        if without_start_count:
            filters += [
                FilterDto("datetime",
                          op.GRATER_EQUAL,
                          start)
            ]

        prototype = FilterPrototype(transactions).clone(filters)
        transactions: List[TransactionModel] = prototype.data

        data: Dict[str, TbsLine] = dict()
        for transaction in transactions:
            code = transaction.nomenclature.unique_code
            if code not in data:
                data[code] = TbsLine(transaction)
            line = data[code]
            line.add(transaction, start, end)

        if zero_turnovers:
            tbs_keys = data.keys()
            all_keys = StartService().data[Repository.nomenclatures_key].keys()
            other_keys = set(all_keys) - set(tbs_keys)
            for key in other_keys:
                nomenclature = StartService().repository.get(unique_code=key)
                if nomenclature is None:
                    continue
                data[key] = TbsLine(TransactionModel(
                    nomenclature=nomenclature,
                    storage=storage,
                    count=0,
                    measure_unit=nomenclature.measure_unit
                ))

        return list(data.values())
