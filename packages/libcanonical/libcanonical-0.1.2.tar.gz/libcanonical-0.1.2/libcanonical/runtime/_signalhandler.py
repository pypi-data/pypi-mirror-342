import inspect
import signal
from typing import Callable
from types import FrameType
from typing import Any


class SignalHandler:
    """Mixin class to bind interrupt signals. An interrupt signal is bound
    by defining an ``on_{lowercased signal}`` on the inherting class.

    .. code:: python

        class Main(SignalHandler):

            def on_sigint(self):
                print("Caught SIGINT!")

    Note that if the inherting class override the :meth:`__init__` method,
    it must call :func:`super()`. :class:`SignalHandler` ignores any
    positional and keyword arguments.
    """

    def __init__(self, *_: Any, **__: Any) -> None:
        self.__bind_signals()

    def __bind_signals(self):
        f: Callable[[FrameType], None] | Callable[[], None] | None
        for _, value in inspect.getmembers(signal):
            if not isinstance(value, signal.Signals):
                continue
            f = getattr(self, f'on_{str.lower(value.name)}', None)
            if f is None:
                continue
            signal.signal(value, self.__signal_handler(f))

    def __signal_handler(
        self,
        f: Callable[[FrameType], None] | Callable[[], None]
    ) -> Callable[[int, FrameType | None], None]:
        handler: Callable[[int, FrameType | None], None]
        signature = inspect.signature(f)
        arglen = len(signature.parameters.values())
        match arglen:
            case 0: handler = lambda _, __: f() # type: ignore
            case 1: handler = lambda _, frame: f(frame) # type: ignore
            case _:
                raise TypeError(
                    "Invalid signature for signal handler "
                    f"{type(self).__name__}.{f.__name__}, "
                    f"expected at most 1 parameters, got {arglen}"
                )
        return handler