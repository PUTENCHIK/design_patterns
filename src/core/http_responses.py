from json import dumps
from flask import Response
from typing import Any


"""Текстовый HTTP ответ со статусом 200"""
class TextResponse(Response):

    def __init__(self, text: str):
        super().__init__(
            status=200,
            response=str(text),
            content_type="text/plain"
        )


"""HTTP ответ с контентом в формате JSON и со статусом 200"""
class JsonResponse(Response):

    def __init__(self, content: Any):
        super().__init__(
            status=200,
            response=dumps(content, ensure_ascii=False),
            content_type="application/json"
        )


"""HTTP ответ со статусом 4xx и описанием ошибки в формате JSON"""
class ErrorResponse(Response):

    def __init__(self, error: str, status: int = 400):
        super().__init__(
            status=status,
            response=dumps({"error": str(error)}),
            content_type="application/json"
        )


"""HTTP ответ с контентом в переданном формате и со статусом 200"""
class FormatResponse(Response):

    # Сопоставление текстового формата и содержания content_type
    match = {
        "csv": "text/plain; charset=utf-8",
        "json": "application/json",
        "markdown": "text/markdown; charset=utf-8",
        "xml": "text/xml",
    }

    def __init__(self, content: str, content_type: str):
        ct = self.match.get(content_type, "text/plain")
        if ct == "json":
            content = dumps(content)
        super().__init__(
            status=200,
            response=content,
            content_type=ct,
        )
