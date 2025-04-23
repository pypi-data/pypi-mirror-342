import asyncio
import contextlib
import inspect
import logging.config
import signal
import time
import os
from typing import cast
from typing import Any
from typing import AsyncGenerator
from typing import Awaitable
from typing import Callable
from typing import Coroutine
from typing import TypeVar

from libcanonical.environ import EnvironmentVariables
from libcanonical.types import ApplicationRuntimeState
from libcanonical.utils import logger
from libcanonical.utils.logging import LoggingConfigDict
from ._signalhandler import SignalHandler
from ._logging import LOGGING_CONFIG


R = TypeVar('R')


class MainProcess(SignalHandler):
    """The main process of an application."""
    environment: type[EnvironmentVariables] = EnvironmentVariables
    handle_signals: bool = True
    instance_id: str
    interval: float = 0.01
    logger = logger
    log_tracebacks: bool = True
    loop: asyncio.AbstractEventLoop
    max_age: int = 0
    min_runtime: int = 0
    must_drop: bool = True
    must_exit: bool = False
    must_reload: bool = False
    started: int
    state: ApplicationRuntimeState | None = None
    suspended: bool = False
    teardown_deadline: float = 120.0
    uid: int
    _step: int = 0

    class ConfigurationFailure(Exception):

        def __init__(self, message: str):
            self.message = message

    @property
    def step(self) -> int:
        return self._step

    @classmethod
    def run(cls, name: str, **kwargs: Any):
        self = cls(name=name, **kwargs)
        self.main()

    @property
    def age(self) -> int:
        return int(time.monotonic() - self.started)

    @property
    def runtime(self) -> int:
        return int(time.monotonic() - self.started)

    def __init__(
        self, *,
        name: str,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.name = name
        self.environ = self.environment.parse(self.name)
        self.instance_id = bytes.hex(os.urandom(16))
        self.timestamp = time.monotonic()
        self.__lifecycle = self._lifecycle()

    def configure(self, reloading: bool = False) -> None | Coroutine[None, None, None]:
        """A hook to configure and setup the process, prior to entering the
        main event loop. This method is also invoked when the application is
        requested to reload using ``SIGHUP``.

        Args:
            reloading (bool): indicates if this method was invoked during
                a reload. If `reloading` is ``False``, then the main event
                loop is not running.

        Returns:
            None
        """
        pass

    def get_logging_config(self) -> LoggingConfigDict:
        return cast(LoggingConfigDict, LOGGING_CONFIG)

    def initialize(self) -> None:
        """Initializes the application on the current system."""
        return

    def is_initialized(self):
        """Return a boolean indicating if the application is initialized."""
        return all([
            os.path.exists(self.environ.vardir)
        ])

    def is_started(self):
        return self.state == ApplicationRuntimeState.STARTUP

    def is_live(self):
        return self.state is not None and any([
            self.state >= ApplicationRuntimeState.BOOTING,
            self.state == ApplicationRuntimeState.TEARDOWN
        ])

    def is_ready(self):
        return self.state == ApplicationRuntimeState.READY

    def is_runlimit_reached(self) -> bool:
        """Hook to indicate that the run limit is reached and the process
        must exit.
        """
        return False

    def is_stopped(self):
        return self.must_exit

    def is_suspended(self):
        return self.suspended

    def log_step(self, duration: float):
        self.logger.debug(
            "Completed main event in %.02fs (step: %s)",
            duration,
            self.step
        )

    def main(self) -> None:
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.__main__())

    def main_event(self) -> None | Coroutine[None, None, None]:
        """The main event of the process. Subclasses must override
        this method.
        """
        raise NotImplementedError

    def on_completed(self):
        """A hook that is invoked when the process exits succesfully."""
        return

    def on_sigint(self) -> None:
        """Invoked when the process receives a ``SIGINT`` signal."""
        self.logger.info("Caught SIGINT (pid: %s)", os.getpid())
        if self.must_exit:
            # If we already received a SIGINT, assume that the
            # process is not existing and the user wants to
            # kill it off.
            os.kill(os.getpid(), signal.SIGKILL)
        self.must_exit = True

    def on_sighup(self) -> None:
        """Invoked when the process receives a ``SIGHUP`` signal."""
        self.must_reload = True

    def on_sigterm(self) -> None:
        """Invoked when the process receives a ``SIGTERM`` signal."""
        # TODO: Implement this as must_kill
        self.must_exit = True

    def on_sigusr1(self) -> None:
        """Hook to handle ``SIGUSR1``. Subclasses may override this method
        without calling :func:`super()`.
        """
        pass

    def on_sigusr2(self) -> None:
        """Hook to handle ``SIGUSR2``. Subclasses may override this method
        without calling :func:`super()`.
        """
        pass

    def setup_logging(self):
        """Configures the loggers for the application."""
        logging.config.dictConfig(dict(self.get_logging_config()))

    def stop(self):
        self.must_exit = True

    @contextlib.asynccontextmanager
    async def suspend(self, duration: float):
        if self.is_suspended():
            raise RuntimeError("Cannot suspend while suspended.")
        try:
            self.suspended = True
            yield
            elapsed = 0.0
            while elapsed < duration:
                await asyncio.sleep(0.1)
                if self.must_exit or self.must_reload:
                    self.suspended = False
                    break
                elapsed += 0.1
        finally:
            self.suspended = False

    def teardown(self) -> None | Coroutine[None, None, None]:
        """Called during application teardown. Subclasses may override
        this method without calling :func:`super()`.
        """
        pass

    async def setstate(self, state: ApplicationRuntimeState | None):
        self.state = state
        await self.__lifecycle.asend(self.state)

    async def __main__(self) -> None:
        assert self.state is None
        self.started = int(time.monotonic())
        await self.setstate(self.state)
        if not (await self._run(self._configure)):
            self.logger.critical("Failed configuration, exiting main event loop.")
            await asyncio.sleep(5)
            return
        self.logger.debug("Starting main event loop")
        if self.uid == 0:
            self.logger.warning("This process is running as a privileged user.")
        while True:
            if self.step == 0:
                await self.setstate(ApplicationRuntimeState.READY)
            t0 = time.time()
            if self.is_runlimit_reached():
                self.stop()
            if self.must_exit:
                self.logger.info(
                    "Shutting down %s (pid: %s)",
                    self.name,
                    self.pid
                )
                await self._teardown()
                break
            if self.must_reload and not await self._run(self._configure, reloading=True):
                self.stop()
                continue
            self._step += 1
            try:
                await self._run(self.main_event)
            except Exception as e:
                self._log_exception(e)
                await asyncio.sleep(1)
            finally:
                duration = time.time() - t0
                self.log_step(duration)
                t = self.min_runtime - duration
                if t > 0:
                    async with self.suspend(t):
                        self.logger.debug("Sleeping for %s seconds.", t)
                else:
                    await asyncio.sleep(max(self.interval - duration, 0.0))

    def _initialize(self):
        if self.is_stopped():
            return
        self.initialize()

    def _log_exception(self, e: BaseException, *args: Any, **kwargs: Any):
        self.logger.error(
            "Caught %s",
            type(e).__name__
        )
        if self.log_tracebacks:
            self.logger.exception("The traceback was:")

    async def _configure(self, reloading: bool = False):
        if not reloading:
            await self.setstate(ApplicationRuntimeState.STARTUP)
        if reloading:
            self.logger.warning("Reloading %s (pid: %s)", self.name, self.pid)
        self.setup_logging()
        self.uid = os.getuid()
        self.pid = os.getpid()
        if not reloading and not self.is_initialized():
            self._initialize()
        try:
            await self._run(self.configure, reloading=reloading)
            success = True
        except self.ConfigurationFailure as e:
            self.logger.critical(e.message)
            success = False
        except Exception as e:
            self._log_exception(e)
            success = False
        finally:
            self.must_reload = False
        return success

    async def _lifecycle(self) -> AsyncGenerator[ApplicationRuntimeState | None, ApplicationRuntimeState | None]:
        while True:
            state = yield
            match state:
                case ApplicationRuntimeState.BOOTING:
                    self.logger.info("Application state: BOOTING")
                case ApplicationRuntimeState.LIVE:
                    self.logger.info("Application state: LIVE")
                case ApplicationRuntimeState.READY:
                    self.logger.info("Application state: READY")
                case ApplicationRuntimeState.BUSY:
                    self.logger.info("Application state: BUSY")
                case ApplicationRuntimeState.TEARDOWN:
                    self.logger.info("Application state: TEARDOWN")
                case ApplicationRuntimeState.BOOTFAILURE:
                    self.logger.info("Application state: BOOTFAILURE")
                case ApplicationRuntimeState.RELOADFAILURE:
                    self.logger.info("Application state: RELOADFAILURE")
                case ApplicationRuntimeState.FATAL:
                    self.logger.info("Application state: FATAL")
                case ApplicationRuntimeState.STARTUP:
                    self.logger.info("Application state: STARTUP")
                case None:
                    self.logger.info("Initialized application runtime state")

    async def _run(
        self,
        func: Callable[..., R | Awaitable[R]],
        *args: Any,
        **kwargs: Any
    ):
        result = func(*args, **kwargs)
        if inspect.iscoroutinefunction(func):
            assert inspect.isawaitable(result)
            result = await result
        return result

    async def _teardown(self):
        await self.setstate(ApplicationRuntimeState.TEARDOWN)
        try:
            await self._run(self.teardown)
            await self._run(self.on_completed)
        except Exception as e:
            self._log_exception(e)