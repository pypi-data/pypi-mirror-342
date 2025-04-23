import asyncio
import time
from typing import Callable
from typing import TypeVar
from types import TracebackType


R = TypeVar('R')


class DelayContext:

    @property
    def remaining(self):
        elapsed = time.monotonic() - self.started
        remaining = max(self.delay - elapsed, 0.0)
        if remaining > 0.0 and self.timeout:
            timeout = self.timeout - self.latency
            remaining = min(timeout, remaining)
        return remaining

    def __init__(self, delay: float, timeout: float | None = None, latency: float = 1.0):
        self.delay = delay
        self.timeout = timeout or 0.0
        self.latency = latency
        if self.timeout == 0.0:
            self.latency = 0.0

    def sleep(self, func: Callable[[float], R]) -> R:
        return func(self.remaining)

    async def __aenter__(self):
        self.started = time.monotonic()
        return self

    async def __aexit__(
        self,
        cls: type[BaseException],
        exc: BaseException,
        tb: TracebackType
    ):
        if exc:
            raise exc
        await self.sleep(asyncio.sleep)

    def __enter__(self):
        self.started = time.monotonic()
        return self

    def __exit__(
        self,
        cls: type[BaseException],
        exc: BaseException,
        tb: TracebackType
    ):
        if exc:
            raise exc
        self.sleep(time.sleep)


delay = DelayContext