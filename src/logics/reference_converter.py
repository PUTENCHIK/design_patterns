from src.core.validator import Validator as vld
from src.core.abstract_model import AbstractModel
from src.core.abstract_converter import AbstractConverter
from src.utils import get_properties


"""Конвертер, обрабатывающий объекты, являющиеся AbstractModel"""
class ReferenceConverter(AbstractConverter):
    
    # Если True, то модели конвертируются в объекты, а иначе - заменяются 
    # уникальным кодом
    is_deep: bool

    def __init__(
        self,
        is_deep: bool = True
    ):
        super().__init__()
        self.is_deep = is_deep
    
    """Переопределённый метод convert
    
    Проходится по полям AbstractModel и формирует словарь формата
    'поле: конвертированное значение поля'
    """
    def convert(self, object_: AbstractModel) -> dict:
        from src.logics.factory_converters import FactoryConverters

        vld.validate(object_, AbstractModel, "object")

        factory = FactoryConverters()
        result = dict()
        props = get_properties(object_)
        for prop in props:
            value = getattr(object_, prop)

            if isinstance(value, AbstractModel):
                if self.is_deep:
                    result[prop] = self.convert(value)
                else:
                    result[prop + "_code"] = factory \
                        .create(value.unique_code, self.is_deep) \
                        .convert(value.unique_code)
            else:
                result[prop] = factory.create(value, self.is_deep) \
                    .convert(value)

        return result
