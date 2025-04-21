import sys

from ._colourizedformatter import ColourizedFormatter


class DefaultFormatter(ColourizedFormatter):
    __module__: str = 'libcanonical.utils.logging'

    def should_use_colors(self) -> bool:
        return sys.stderr.isatty()  # pragma: no cover