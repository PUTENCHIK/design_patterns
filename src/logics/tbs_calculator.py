from typing import List, Dict
from datetime import datetime
from src.core.validator import Validator as vld
from src.logics.tbs_line import TbsLine
from src.models.storage_model import StorageModel
from src.models.transaction_model import TransactionModel
from src.singletons.repository import Repository
from src.singletons.start_service import StartService


"""Класс для расчёта оборотно-сальдовой ведомости"""
class TbsCalculator:
    
    @staticmethod
    def calculate(
        storage: StorageModel, 
        start: datetime, 
        end: datetime
    ) -> List[TbsLine]:
        vld.validate(storage, StorageModel, "storage")
        vld.validate(start, datetime, "start date")
        vld.validate(end, datetime, "end date")
        key = Repository.transactions_key
        items: List[TransactionModel] = list(
            StartService().data[key].values()
        )
        transactions = [item
                        for item in items
                        if (item.storage == storage and
                            item.datetime <= end)]
        data: Dict[str, TbsLine] = dict()
        for transaction in transactions:
            code = transaction.nomenclature.unique_code
            if code not in data:
                data[code] = TbsLine(transaction)
            line = data[code]
            line.add(transaction, start, end)
        
        return list(data.values())
        