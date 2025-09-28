from typing import Optional, Any, Union, Type, List, Tuple
from src.core.exceptions import (InvalidValueException, WrongTypeException,
                                 ParamException)


"""Вспомогательный класс для валидации полей и объектов"""
class Validator:

    """Общий метод валидации значений

    Args:
        value (Any): валидируемое значение.
        types (Union[Type, List[Type]]): тип валидируемого значения
            или список допустимых типов значения.
        field_name (str): строковое название поля.
        could_be_none (bool, optional): может ли поле быть None.
            По-умолчанию False.
        len_ (Optional[int], optional): ожидаемая длина строкового
            представления значения. По-умолчанию False.
        strictly_len (bool, optional): строго ли длина значения
            дожна быть = параметру len_, или может быть <=.
            По-умолчанию False.
    
    Returns:
        bool: True если поле прошло валидацию по типу и значению,
            иначе False.
    
    Raises:
        ParamException: неверно переданный параметр types
        NotValidValueException: невалидное значение.
        WrongTypeException: несоответствие типа поля и ожидаемого типа.
    """
    @staticmethod
    def validate(
        value: Any,
        types: Union[Type, Tuple[Type], List[Type]],
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:

        if could_be_none and value is None:
            return True
        elif (not could_be_none and value is None or
              not len(str(value).strip())):
            raise InvalidValueException(
                f"'{field_name}' is none or empty"
            )
        
        if isinstance(types, (tuple, list)):
            # Если types - это массив типов, то value должен являться
            # одним из типов в types, иначе  WrongTypeException
            flag = False
            for type_ in types:
                if isinstance(value, type_):
                    flag = True
                    break
            if not flag:
                raise WrongTypeException(
                    f"'{field_name}' must be {', or '.join(types)}, "
                    f"not '{type(value).__name__}'"
                )
        elif isinstance(types, type):
            if not isinstance(value, types) or type(value) is not types:
                raise WrongTypeException(
                    f"'{field_name}' is {type(value).__name__}, not {types}"
                )
        else:
            raise ParamException(
                "Param 'types' must be either type or list/tuple of types, "
                f"not {type(types).__name__}"
            )
        
        if len_:
            real_len = len(str(value).strip())
            if not strictly_len and real_len > len_:
                raise InvalidValueException(
                    f"Length of '{field_name}' must be less than {len_}, "
                    f"now it's {real_len}"
                )
            elif strictly_len and real_len != len_:
                raise InvalidValueException(
                    f"Length of '{field_name}' must be equal {len_}, "
                    f"now it's {real_len}"
                )
        
        return True

    """Метод проверки на строку"""
    @staticmethod
    def is_str(
        value: Any,
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:
        return Validator.validate(value, str, field_name,
                                  could_be_none,len_, strictly_len)
    
    """Метод проверки на целочисленное значение"""
    @staticmethod
    def is_int(
        value: Any,
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:
        return Validator.validate(value, int, field_name,
                                  could_be_none, len_, strictly_len)
    
    """Метод проверки на положительное целое число"""
    def is_positive_int(
        value: Any,
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:
        result = Validator.is_int(value, field_name,
                                  could_be_none, len_, strictly_len)
        return result if could_be_none else value > 0
    
    """Метод проверки на словарь"""
    def is_dict(
        value: Any,
        field_name: str,
    ) -> bool:
        return Validator.validate(value, dict, field_name)

    """Метод проверки на число с плавающей точкой"""
    def is_float(
        value: Any,
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:
        return Validator.validate(value, float, field_name,
                                  could_be_none, len_, strictly_len)
    
    """Метод проверки на число (целое или с плавающей точкой)"""
    def is_number(
        value: Any,
        field_name: str,
        could_be_none: bool = False,
        len_: Optional[int] = None,
        strictly_len: bool = False,
    ) -> bool:
        return Validator.validate(value, (int, float), field_name,
                                  could_be_none, len_, strictly_len)
