from enum import Enum


"""Перечисление с операторами фильтрации моделей"""
class FilterOperator(Enum):
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    GRATER = "GRATER"
    LESSER = "LESSER"
    GRATER_EQUAL = "GRATER_EQUAL"
    LESSER_EQUAL = "LESSER_EQUAL"
    LIKE = "LIKE"
    CONTAINS = "CONTAINS"
