from typing import Any
from typing import Optional
from typing import TypedDict


LoggerConfigDict = TypedDict('LoggerConfigDict', {
    'handlers': list[str],
    'level': str,
    'propagate': bool
})


class LoggingConfigDict(TypedDict):
    version: int
    disable_existing_loggers: bool
    filters: Optional[dict[str, Any]]
    loggers: dict[str, LoggerConfigDict]