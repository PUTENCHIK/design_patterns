import unittest
from src.logics.prototype_report import PrototypeReport
from src.singletons.start_service import StartService
from src.singletons.repository import Repository


class TestPrototypeReport(unittest.TestCase):
    def test_prototypereport_filter_(self):
        start_service = StartService()
        start_service.start("tests/data/settings.json")
        transactions = list(start_service.transactions.values())
        nomenclatures = list(start_service.nomenclatures.values())

        prototype = PrototypeReport(transactions)
        first = nomenclatures[0]

        next = prototype.filter_by_nomenclature(prototype, first)

        assert len(next.data) > 0
        assert len(prototype.data) > 0
        assert len(prototype.data) >= len(next.data)

    def test_prototypereport_(self):
        pass


if __name__ == "__main__":
    unittest.main()
