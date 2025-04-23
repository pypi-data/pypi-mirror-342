import pydantic

from libcanonical.types.base64 import Base64


class BaseEncryptionResult(pydantic.BaseModel):
    alg: str = pydantic.Field(
        default=...,
        title="Algorithm",
        description="The algorithm used to perform the encryption function."
    )

    kid: str | None = pydantic.Field(
        default=None,
        title="Key Identifier",
        description=(
            "Identifies the key used to perform the encryption function."
        )
    )

    ct: Base64 = pydantic.Field(
        default=...,
        title="Ciphertext",
        description=(
            "The Base64-encoded encryption result."
        )
    )

    def __bytes__(self) -> bytes:
        return self.ct