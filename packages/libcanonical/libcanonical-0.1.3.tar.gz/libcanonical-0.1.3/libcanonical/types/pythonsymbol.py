from typing import Any
from typing import Generic
from typing import TypeVar

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core import core_schema

from libcanonical.utils import import_symbol

T = TypeVar('T')


class PythonSymbol(Generic[T]):
    __module__: str = 'libcanonical.types'
    value: T

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(cls),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.fromqualname)
                ]),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema(max_length=128))

    @classmethod
    def fromqualname(cls, qualname: str):
        try:
            return cls(
                qualname,
                symbol=import_symbol(qualname)
            )
        except ImportError:
            raise ValueError(f'Unknown Python symbol: {repr(qualname)}')

    def __init__(self, qualname: str, symbol: T) -> None:
        self.qualname = qualname
        self.value = symbol

    def __str__(self):
        return self.qualname