from typing import Any
from typing import Callable
from typing import Generic
from typing import TypeVar


C = TypeVar('C')
T = TypeVar('T')


class _classproperty(Generic[T]):
    func: Callable[..., T]

    def __init__(self, func: Any):
        self.func = func # type: ignore

    def __get__(self, _: Any, cls: Any) -> T:
        return self.func(cls)


def classproperty(
    func: Callable[..., T]
) -> _classproperty[T]:
    return _classproperty(func)


class MissingDependency:

    def __init__(self, message: str):
        self.message = message

    def __getattr__(self, attname: str) -> Any:
        raise ImportError(self.message)