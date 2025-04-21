from collections import abc
from typing import Any

from libcanonical.utils import jsonpath
from .stringtype import StringType


class JSONPath(StringType):
    __module__: str = 'libcanonical.types'

    @classmethod
    def validate(cls, v: str, _: Any = None):
        if not str.startswith(v, '/'):
            raise ValueError("A JSON path must start with a slash.")
        return cls(v)

    def get(self, mapping: abc.Mapping[str, Any]) -> Any:
        try:
            value = jsonpath(mapping, self)
        except (KeyError, TypeError):
            value = None
        return value