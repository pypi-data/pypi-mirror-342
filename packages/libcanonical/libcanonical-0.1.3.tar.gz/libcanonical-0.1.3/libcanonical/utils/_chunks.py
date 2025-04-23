from typing import Sequence
from typing import Generator
from typing import TypeVar

T = TypeVar('T')


def chunks(iterable: Sequence[T], n: int = 1) -> Generator[list[T], None, None]:
    l = len(iterable)
    for ndx in range(0, l, n):
        yield list(iterable[ndx:min(ndx + n, l)])