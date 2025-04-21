from typing import Any
from typing import cast
from typing import Self

import langcodes
from langcodes import Language
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core import core_schema


class BCP47(Language):
    __module__: str = 'canonical.ext.i18n.types'

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.no_info_plain_validator_function(cls),
                core_schema.chain_schema([
                    core_schema.is_instance_schema(str),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())

    @classmethod
    def fromstring(cls, value: str) -> Self:
        value = langcodes.standardize_tag(value, macro=True)
        return cast(Self, cls.get(value))