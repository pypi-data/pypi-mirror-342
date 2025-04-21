from typing import Any
from typing import Literal

import pydantic



EncodingLiteral = Literal[
    'base64',
    'hex',
    'utf-8',
]


KindLiteral = Literal[
    'body',
    'headers',
    #'json',
    'query',
]


class HTTPRequestRef(pydantic.BaseModel):
    kind: KindLiteral = pydantic.Field(
        default=...,
        description=(
            "Specifies the component of the HTTP request that "
            "is being referenced."
        )
    )

    name: str = pydantic.Field(
        default='',
        description=(
            "Indicates where to find the the referent.\n\n"
            "- For `body`, this field is ignored.\n\n"
            "- For `headers` and `query`, the `name` field."
            "indicates the name of the header or query parameter.\n\n"
            "Note that when `kind=query`, repeated query parameters "
            "are parsed as a list and the `encoding` is applied to "
            "each member in the list."
        )
    )

    encoding: EncodingLiteral = pydantic.Field(
        default=...,
        description=(
            "The content encoding of the referent."
        )
    )

    def model_post_init(self, _: Any) -> None:
        if self.kind != 'body' and not self.name:
            raise ValueError("The `.name` field is required.")