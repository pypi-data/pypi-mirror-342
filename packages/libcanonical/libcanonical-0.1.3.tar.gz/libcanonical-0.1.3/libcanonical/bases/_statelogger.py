import logging
from typing import Any
from typing import ClassVar
from typing import Literal


LogLevel = Literal[
    #'TRACE',
    'DEBUG',
    'INFO',
    #'SUCCESS',
    'WARNING',
    'ERROR',
    'CRITICAL',
    #'FATAL'
]


class StateLogger:
    __module__: str = 'libcanonical.types'
    logger: ClassVar[logging.Logger]
    logger_name: ClassVar[str] = 'canonical'

    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        if not hasattr(cls, 'logger'):
            cls.logger = logging.getLogger(cls.__module__)
        if hasattr(cls, 'logger_name'):
            cls.logger = logging.getLogger(__name__)

    def get_logging_parameters(self) -> dict[str, Any]:
        """Hook to return a dictionary holding parameters for the
        local :class:`logging.Logger` instance.
        """
        return {}

    def log(self, level: LogLevel, message: str, *args: Any, **extra: Any):
        match level:
            case 'DEBUG':
                log = self.logger.debug
            case 'INFO':
                log = self.logger.info
            case 'WARNING':
                log = self.logger.warning
            case 'ERROR':
                log = self.logger.error
            case 'CRITICAL':
                log = self.logger.critical
            case _: raise ValueError(f"Unknown log level: {level}")
        return log(
            message,
            *args,
            extra={
                **self.get_logging_parameters(),
                **extra
            }
        )