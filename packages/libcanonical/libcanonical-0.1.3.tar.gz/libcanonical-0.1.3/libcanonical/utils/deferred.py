from typing import Any
from typing import Callable


NOT_AVAILABLE = object()


class Deferred:

    def __init__(self, resolve: Callable[[], Any]):
        self.__resolve = resolve
        self.__result = NOT_AVAILABLE

    def __str__(self) -> str:
        if self.__result == NOT_AVAILABLE:
            self.__result = self.__resolve()
        return str(self.__result)

    def __getattr__(self, attname: str) -> Any:
        if self.__result == NOT_AVAILABLE:
            self.__result = self.__resolve()
        return getattr(self.__result, attname)