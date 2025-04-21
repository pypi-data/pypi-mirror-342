from typing import Any
from typing import Callable
from typing import TypeVar

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic.networks import validate_email
from pydantic_core import CoreSchema
from pydantic_core import core_schema

from .domainname import DomainName


T = TypeVar('T')


class EmailAddress(str):
    __module__: str = 'libcanonical.types'

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(max_length=320),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(cls),
                core_schema.chain_schema([
                    core_schema.str_schema(max_length=320),
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
        schema = handler(core_schema.str_schema(max_length=128))
        schema['title'] = 'EmailAddress'
        schema['description'] = (
            "An RFC email address follows the format defined in RFC 5322 "
            "and related standards, consisting of a local part, an ”@” symbol, "
            "and a domain part, with specific rules for allowed characters, "
            "quoting, and internationalization to ensure compatibility across "
            "email systems."
        )
        return schema

    @classmethod
    def fromstring(cls, v: Any, _: Any = None) -> 'EmailAddress':
        v = str.lower(v)
        return cls(validate_email(v)[1]) # type: ignore

    @property
    def domain(self) -> DomainName:
        return DomainName(str.split(self, '@')[-1])

    @property
    def maskable(self) -> bytes:
        return str.encode(f'email:{self.lower()}', 'ascii')

    def mask(self, masker: Callable[[bytes], T]) -> T:
        return masker(self.maskable)

    def __repr__(self) -> str: # pragma: no cover
        return f'<EmailAddress: {str(self)}>'