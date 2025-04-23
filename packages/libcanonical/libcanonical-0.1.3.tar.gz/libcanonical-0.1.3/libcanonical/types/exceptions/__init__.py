from ._conflict import Conflict
from ._doesnotexist import DoesNotExist
from ._fatalexception import FatalException
from ._undecryptable import Undecryptable


__all__: list[str] = [
    'Conflict',
    'ExceptionRaiser',
    'DoesNotExist',
    'FatalException',
    'Undecryptable',
]


class ExceptionRaiser:
    """Mixin class that provides an interface to raise standard exceptions
    defined by the :mod:`libcanonical.types.exceptions` package.
    """
    __module__: str = 'libcanonical.types'
    Conflict        = Conflict
    DoesNotExist    = DoesNotExist
    Undecryptable   = Undecryptable