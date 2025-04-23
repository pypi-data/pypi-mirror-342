from typing import Any
from typing import TypeVar

from pydantic_core import CoreSchema
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from pydantic import GetJsonSchemaHandler


__all__: list[str] = [
    'HexEncoded'
]

T = TypeVar('T', bound='HexEncoded')


class HexEncoded(bytes):
    __module__: str = 'libcanonical.types'

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.chain_schema([
                core_schema.union_schema([
                    core_schema.is_instance_schema(bytes),
                    core_schema.chain_schema([
                        core_schema.is_instance_schema(str),
                        core_schema.no_info_plain_validator_function(cls.fromstring),
                        core_schema.no_info_plain_validator_function(cls.validate)
                    ])
                ]),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(cls.serialize)
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())

    @classmethod
    def fromstring(cls, v: str):
        if v.startswith('0x'):
            v = v[2:]
        return cls.fromhex(v)

    @classmethod
    def validate(cls, instance: T) -> T:
        return instance

    def serialize(self) -> str:
        return f"0x{self.hex()}"