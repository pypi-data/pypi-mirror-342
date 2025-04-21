from typing import overload
from typing import Awaitable
from typing import Literal
from typing import Protocol


class ISigner(Protocol):

    @overload
    def sign(
        self,
        message: bytes | str
    ) -> Awaitable[bytes]:
        ...

    @overload
    def sign(
        self,
        message: bytes | str,
        *,
        blocking: Literal[False]
    ) -> Awaitable[bytes]:
        ...

    @overload
    def sign(
        self,
        message: bytes | str,
        *,
        blocking: Literal[True]
    ) -> bytes:
        ...

    def sign(
        self,
        message: bytes | str,
        *,
        blocking: bool = False
    ) -> bytes | Awaitable[bytes]:
        ...