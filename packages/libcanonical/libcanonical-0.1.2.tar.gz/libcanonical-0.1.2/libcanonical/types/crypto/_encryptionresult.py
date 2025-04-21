from typing import Union

import pydantic

from ._aesencryptionresult import AESEncryptionResult
from ._bytesencryptionresult import BytesEncryptionResult
from ._dhencryptionresult import DHEncryptionResult


EncryptionResultType = Union[
    AESEncryptionResult,
    BytesEncryptionResult,
    DHEncryptionResult
]
    

class EncryptionResult(pydantic.RootModel[EncryptionResultType]):

    @property
    def aad(self) -> bytes:
        return self.root.aad

    @property
    def iv(self) -> bytes | None:
        return self.root.iv

    @property
    def tag(self) -> bytes | None:
        return self.root.tag

    def __bytes__(self) -> bytes:
        return bytes(self.root)