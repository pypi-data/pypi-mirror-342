import pydantic

from libcanonical.types.base64 import Base64
from ._baseencryptionresult import BaseEncryptionResult


class AESEncryptionResult(BaseEncryptionResult):
    """The result of an encryption operation using the AES algorithm."""
    aad: Base64 = pydantic.Field(
        default=Base64(),
        title="Additional Authenticated Data (AAD)",
        description=(
            "The Base64-encoded input data to the authenticated encryption "
            "function that is authenticated but not encrypted."
        )
    )

    ct: Base64 = pydantic.Field(
        default=...,
        title="Ciphertext",
        description=(
            "The Base64-encoded encryption result."
        )
    )

    iv: Base64 = pydantic.Field(
        default=...,
        title="Initialization Vector (IV)",
        description=(
            "A binary vector used as the input to initialize the algorithm for "
            "the encryption of a plaintext block sequence to increase security "
            "by introducing additional cryptographic variance and to synchronize "
            "cryptographic equipment. The initialization vector need not be secret."
        )
    )

    tag: Base64 = pydantic.Field(
        default=...,
        title="Authentication tag",
        description=(
            "A cryptographic checksum on data that is designed to reveal both "
            "accidental errors and the intentional modification of the data."
        )
    )