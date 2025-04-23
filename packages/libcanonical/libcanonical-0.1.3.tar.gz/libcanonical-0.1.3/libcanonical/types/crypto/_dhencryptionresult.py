from ._baseencryptionresult import BaseEncryptionResult


class DHEncryptionResult(BaseEncryptionResult):
    epk: dict[str, int | str]

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
        raise NotImplementedError