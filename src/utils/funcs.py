from typing import Any, List
from src.core.exceptions import ParamException


def get_fields(object_: Any) -> List[str]:
    if object_ is None:
        raise ParamException(f"Object can't be none")
    
    return [f for f in dir(object_) if not f.startswith("__")]
