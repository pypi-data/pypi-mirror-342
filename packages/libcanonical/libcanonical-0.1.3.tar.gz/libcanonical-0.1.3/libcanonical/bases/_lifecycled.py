import inspect
from typing import Any
from typing import Coroutine
from types import TracebackType


class Lifecycled:
    __module__: str = 'libcanonical.bases'

    def setup(
        self,
        reloading: bool = False
    ) -> None | Coroutine[Any, Any, None]:
        raise NotImplementedError

    def teardown(
        self,
        exception: BaseException | None = None
    ) -> bool | Coroutine[Any, Any, bool]:
        raise NotImplementedError

    async def __aenter__(self):
        result = self.setup(reloading=False)
        if inspect.isawaitable(result):
            await result
        return self

    async def __aexit__(
        self,
        cls: type[BaseException] | None = None,
        exception: BaseException | None = None,
        traceback: TracebackType | None = None
    ) -> bool:
        result = self.teardown()
        if inspect.isawaitable(result):
            await result
        assert isinstance(result, bool)
        return result