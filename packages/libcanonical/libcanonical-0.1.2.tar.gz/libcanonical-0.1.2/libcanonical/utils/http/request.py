import pydantic


class Request(pydantic.BaseModel):
    host: str = pydantic.Field(
        default=...,
        description=(
            "The IP address of the client, as seen by the "
            "server."
        )
    )

    url: str = pydantic.Field(
        default=...,
        description="The full URL that was requested."
    )