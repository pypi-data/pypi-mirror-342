from typing import Iterable

from .mediatype import get_best_match


class MediaTypeSelector:

    def __init__(self, allow: Iterable[str]):
        self.allow = set(allow)

    def select(self, header: str | None):
        if header is None:
            return None
        return get_best_match(header, self.allow)