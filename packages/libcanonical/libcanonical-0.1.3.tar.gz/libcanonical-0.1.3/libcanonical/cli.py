"""Extensions to the :class:`typer.Typer` command-line application
framework.
"""
import logging.config
from typing import Any

import typer
from typer import Option

from .runtime import LOGGING_CONFIG


__all__: list[str] = [
    'Option',
    'Typer'
]


class Typer(typer.Typer):
    logging_config: dict[str, Any] = LOGGING_CONFIG

    def configure(self):
        pass

    def _configure(self):
        logging.config.dictConfig(self.get_logging_config())
        self.configure()

    def get_logging_config(self):
        return self.logging_config

    def __call__(self, *args: Any, **kwargs: Any):
        self._configure()
        return super().__call__(*args, **kwargs)