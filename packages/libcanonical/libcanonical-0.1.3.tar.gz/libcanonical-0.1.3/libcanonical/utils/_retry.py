import asyncio
import functools
import inspect
import logging
import threading
import time
from typing import Callable
from typing import Iterable
from typing import ParamSpec
from typing import TypeVar


P = ParamSpec('P')
T = TypeVar('T')


class _Retry:
    logger: logging.Logger = logging.getLogger('canonical')
    exception_classes: tuple[type[BaseException], ...]
    logging_message: str = "Caught retryable %(exception_class)s (thread: %(thread)s, attempts: %(attempts)s)"

    def __init__(
        self,
        types: Iterable[type[BaseException]],
        max_attempts: int | None = None,
        delay: int | float = 10,
        reason: str | None = None
    ):
        self.delay = delay
        self.exception_classes = tuple(types)
        self.max_attempts = max_attempts
        if reason:
            self.logging_message = reason

    def on_exception(self, exception: BaseException, attempts: int):
        if not isinstance(exception, self.exception_classes):
            return True
        if self.max_attempts and attempts > self.max_attempts:
            return True
        t = threading.current_thread()
        self.logger.warning(
            self.logging_message,
            extra={
                'attempts': attempts,
                'exception_class': f'{type(exception).__name__}',
                'thread_id': t.ident
            }
        )

    def call_sync(self, f: Callable[P, T]) -> Callable[P, T]:
        handles = self.exception_classes

        @functools.wraps(f)
        def d(*args: P.args, **kwargs: P.kwargs):
            attempts = 0
            while True:
                attempts += 1
                try:
                    result = f(*args, **kwargs)
                    break
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    if not isinstance(e, handles):
                        raise
                    if self.max_attempts and attempts > self.max_attempts:
                        raise e from e
                    t = threading.current_thread()
                    self.logger.warning(
                        self.logging_message,
                        extra={
                            'attempts': attempts,
                            'exception_class': f'{type(e).__name__}',
                            'thread_id': t.ident
                        }
                    )
                    time.sleep(self.delay)
            return result

        return d # type: ignore

    def __call__(
        self,
        f: Callable[P, T]
    ) -> Callable[P, T]:
        if not inspect.iscoroutinefunction(f):
            return self.call_sync(f)
        assert inspect.iscoroutinefunction(f)
        handles = self.exception_classes

        @functools.wraps(f)
        async def d(*args: P.args, **kwargs: P.kwargs):
            attempts = 0
            while True:
                attempts += 1
                try:
                    result = await f(*args, **kwargs)
                    break
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    if not isinstance(e, handles):
                        raise
                    if self.max_attempts and attempts > self.max_attempts:
                        raise e from e
                    t = threading.current_thread()
                    self.logger.warning(
                        self.logging_message,
                        extra={
                            'attempts': attempts,
                            'exception_class': f'{type(e).__name__}',
                            'thread_id': t.ident
                        }
                    )
                    await asyncio.sleep(self.delay)
            return result

        return d # type: ignore


retry = _Retry