from ._baseencryptionresult import BaseEncryptionResult


class BytesEncryptionResult(BaseEncryptionResult):
    """The result of an encryption operation using the AES algorithm."""

    @property
    def aad(self) -> bytes:
        return b''

    @property
    def iv(self) -> None:
        return None

    @property
    def tag(self) -> None:
        return None

    def __bytes__(self) -> bytes:
        return self.ct