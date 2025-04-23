from typing import Any
from typing import Callable
from typing import TypeVar

import phonenumbers
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core import core_schema


T = TypeVar('T')


class Phonenumber(str):

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(max_length=128),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(cls),
                core_schema.chain_schema([
                    core_schema.str_schema(max_length=128),
                    core_schema.no_info_plain_validator_function(cls.fromstring)
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
        schema = handler(core_schema.str_schema(max_length=18))
        schema['title'] = 'Phonenumber'
        schema['description'] = (
            "The ITU-T phone number format, defined by E.164, is an international "
            "numbering standard that ensures a globally unique structure for "
            "telephone numbers, consisting of a country code (1–3 digits), a "
            "national destination code (NDC), and a subscriber number, with a "
            "maximum length of 15 digits."
        )
        return schema

    @property
    def maskable(self) -> bytes:
        return str.encode(f'phonenumber:{self.lower()}', 'ascii')

    @classmethod
    def fromstring(cls, v: Any, _: Any = None) -> str:
        if not isinstance(v, str):
            raise TypeError("string required")
        try:
            p = phonenumbers.parse(v)
            if not phonenumbers.is_valid_number(p):
                raise ValueError("Not a valid phonenumber.")
        except (phonenumbers.NumberParseException, TypeError):
            raise ValueError("Not a valid phonenumber.")
        return cls(
            phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
        )

    @classmethod
    def parse(
        cls,
        v: str,
        region: str | None = None
    ):
        try:
            p = phonenumbers.parse(v, region=region)
            if not phonenumbers.is_valid_number(p):
                raise ValueError("Not a valid phonenumber.")
        except (phonenumbers.NumberParseException, TypeError):
            raise ValueError("Not a valid phonenumber.")
        return cls(
            phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
        )

    def mask(self, masker: Callable[[bytes], T]) -> T:
        return masker(self.maskable)

    def __repr__(self) -> str: # pragma: no cover
        return f'<Phonenumber: {str(self)}>'