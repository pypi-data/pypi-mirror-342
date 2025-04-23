import collections.abc
import json
import logging
from typing import Any


class JSONFormatter(logging.Formatter):
    __module__: str = 'libcanonical.utils.logging'

    def format(self, record: logging.LogRecord) -> str:
        super().format(record)
        params: dict[str, Any] = {
            'message': record.msg
        }
        if isinstance(record.msg, collections.abc.Mapping):
            params.update(record.msg) # type: ignore
        else:
            params['message'] = super().formatMessage(record)
        if record.exc_info:
            assert record.exc_info[0] is not None
            params['exception'] = {
                'type': f'{record.exc_info[0].__module__}.{record.exc_info[0].__name__}',
                'stack': self.formatException(record.exc_info)
            }
        return json.dumps(params)