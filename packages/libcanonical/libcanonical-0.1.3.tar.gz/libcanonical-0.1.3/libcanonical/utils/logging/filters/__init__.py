import logging


class TracebackInfoFilter(logging.Filter):
    """Clear or restore the exception on log records"""

    def __init__(self, clear: bool = True):
        self.clear = clear

    def filter(self, record: logging.LogRecord):
        if self.clear:
            record.exc_info = None
            record.exc_text = None
        return True