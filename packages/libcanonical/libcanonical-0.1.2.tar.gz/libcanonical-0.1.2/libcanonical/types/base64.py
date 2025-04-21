import json
from typing import Any
from typing import ClassVar
from typing import TypeVar

from pydantic_core import CoreSchema
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from pydantic import GetJsonSchemaHandler

from libcanonical.utils.encoding import b64decode
from libcanonical.utils.encoding import b64encode
from libcanonical.utils.encoding import b64encode_int
from libcanonical.utils.encoding import bytes_to_number


__all__: list[str] = [
    'Base64'
]

T = TypeVar('T', bound='Base64')


class Base64(bytes):
    __module__: str = 'libcanonical.types'
    description: ClassVar[str | None] = None
    type_name: ClassVar[str | None] = None
    max_length: ClassVar[int | None] = None
    min_length: ClassVar[int | None] = None

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.no_info_plain_validator_function(cls.fromb64),
            python_schema=core_schema.union_schema([
                core_schema.chain_schema([
                    core_schema.is_instance_schema(cls),
                    core_schema.bytes_schema(
                        max_length=cls.max_length,
                        min_length=cls.min_length
                    ),
                    core_schema.no_info_plain_validator_function(cls)
                ]),
                core_schema.chain_schema([
                    core_schema.is_instance_schema(str),
                    core_schema.no_info_plain_validator_function(cls.fromb64),
                    core_schema.bytes_schema(
                        max_length=cls.max_length,
                        min_length=cls.min_length
                    ),
                    core_schema.no_info_plain_validator_function(cls)
                ]),
                core_schema.chain_schema([
                    core_schema.is_instance_schema(int),
                    core_schema.no_info_plain_validator_function(cls.fromint),
                    core_schema.bytes_schema(
                        max_length=cls.max_length,
                        min_length=cls.min_length
                    ),
                    core_schema.no_info_plain_validator_function(cls)
                ]),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        schema = handler(core_schema.str_schema())
        if cls.description:
            schema['description'] = cls.description
        if cls.type_name:
            schema['title'] = cls.type_name
        return schema

    @classmethod
    def b64decode(cls, value: bytes | str):
        return b64decode(value)

    @classmethod
    def b64encode(cls, value: bytes | str) -> str:
        return  b64encode(value, encoder=str)

    @classmethod
    def fromint(cls, value: int):
        return cls(b64decode(b64encode_int(value)))

    @classmethod
    def fromb64(cls, value: bytes | str):
        return cls(b64decode(value))

    @classmethod
    def fromdict(cls, value: dict[str, Any]):
        return cls(str.encode(json.dumps(value), 'utf-8'))

    @classmethod
    def fromstring(cls, value: str):
        return cls(str.encode(value))

    @classmethod
    def validate(cls, instance: T) -> T:
        return instance

    def is_empty(self):
        return not bool(self)

    def urlencode(self):
        return b64encode(self)

    def __str__(self):
        return b64encode(self, encoder=str)

    def __int__(self):
        return bytes_to_number(self)

    def __repr__(self):
        return str(self)