from typing import AsyncIterator
from typing import Protocol
from typing import TypeVar


T = TypeVar('T', bound='ITransaction')


class ITransaction(Protocol):
    __module__: str = 'tensorshield.types.protocols'

    async def transaction(
        self: T,
        transaction: T | None = None
    ) -> AsyncIterator[T]:
        ...