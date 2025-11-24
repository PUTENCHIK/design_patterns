from typing import List, Any
from src.core.abstract_model import AbstractModel
from src.core.response_format import ResponseFormat
from src.core.abstract_response import AbstractResponse
from src.utils import get_properties, is_primitive


"""Класс для формирования ответа в формате HTML таблицы"""
class ResponseHtmlTable(AbstractResponse):

    def __init__(self):
        super().__init__()
    
    def build(
        self,
        data: List,
        is_deep: bool = True,
    ) -> str:
        content = super().build(data, ResponseFormat.HTML_TABLE, is_deep)

        if len(data) == 0:
            return content

        props = get_properties(data[0])
        content += self.tag("thead", self.get_row(props, True))

        for item in data:
            values = [getattr(item, prop) for prop in props]
            content += self.get_row(values)

        return self.tag("table", content)
    
    def get_row(
        self,
        items: List[Any],
        is_head: bool = False,
    ) -> str:
        tags = []
        for item in items:
            if is_primitive(item):
                pass
            elif isinstance(item, AbstractModel):
                item = item.name
            else:
                item = str(item)
            tags += [self.tag("th" if is_head else "td", item)]
        return self.tag("tr", "".join(tags))
    
    def tag(
        self, name: str, content: str
    ) -> str:
        return f"<{name}>{content}</{name}>"
