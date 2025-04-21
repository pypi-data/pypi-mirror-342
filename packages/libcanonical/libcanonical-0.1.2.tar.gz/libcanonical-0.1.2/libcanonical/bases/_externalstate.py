import atexit
import asyncio
import threading
import time

from ._lifecycled import Lifecycled
from ._statelogger import StateLogger


class ExternalState(threading.Thread, StateLogger, Lifecycled):
    """The base class for external state implementations. This class should typically not
    be used; instead use either :class:`libcanonical.bases.PollingExternalState` or
    :class:`libcanonical.bases.StreamingExternalState`.
    """
    __module__: str = 'libcanonical.bases'
    _interval: float = 10.0
    last_update: float = 0.0
    must_stop: bool = False
    step: int = 0

    @property
    def age(self):
        return (time.time() - self.last_update)

    def __init__(
        self,
        interval: float = 10.0,
        immediate: bool = False,
        max_age: float | None = None
    ):
        super().__init__(
            daemon=True,
            target=self.__main_event_loop
        )
        self._interval = interval
        self._max_age = max_age
        self._ready_event = threading.Event()
        if immediate:
            self.start()
        atexit.register(self.on_exit)

    def __main_event_loop(self):
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.setup())
        while True:
            self.step += 1
            if self.must_stop:
                break
            if self.must_update():
                try:
                    self.loop.run_until_complete(self.main_event())
                    self.last_update = time.time()
                    self.setready()
                except Exception as e:
                    self.logger.exception(
                        "Caught fatal %s: %s",
                        type(e).__name__,
                        repr(e)
                    )
            time.sleep(0.1)

        self.loop.run_until_complete(self.teardown())

    async def main_event(self) -> None:
        raise NotImplementedError

    def must_update(self):
        return self.step == 1 or (time.time() - self.last_update) > self._interval

    def on_exit(self):
        self.must_stop = True

    def setready(self):
        self._ready_event.set()

    def wait(self, timeout: float | None = None):
        return self._ready_event.wait(timeout=timeout)

    async def setup(self, reloading: bool = False) -> None:
        raise NotImplementedError

    async def teardown(self, exception: BaseException | None = None) -> bool:
        raise NotImplementedError