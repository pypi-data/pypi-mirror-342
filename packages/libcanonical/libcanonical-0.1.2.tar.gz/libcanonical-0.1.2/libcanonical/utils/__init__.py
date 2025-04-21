import inspect
import operator
from collections import abc
from collections import OrderedDict
from functools import reduce
from itertools import chain
from typing import Any
from typing import Callable

from ._chunks import chunks
from ._delay import delay
from ._deephash import deephash
from ._logging import logger
from ._retry import retry
from .deferred import Deferred
from .loader import import_symbol


__all__: list[str] = [
    'chunks',
    'deephash',
    'delay',
    'import_symbol',
    'logger',
    'retry',
    'Deferred',
]


class class_property:
    __module__: str = 'oauthx.utils'

    def __init__(self, func: Callable[..., Any]):
        self.func = func

    def __get__(self, instance: Any, cls: Any) -> Any:
        return self.func(cls)


def merge_signatures(
    signatures: list[inspect.Signature],
    extra: list[inspect.Parameter] | None = None
) -> inspect.Signature:
    """Merge signatures to that FastAPI can inject the dependencies."""
    extra = extra or []
    params: dict[str, inspect.Parameter] = OrderedDict()
    for param in chain(chain(*[x.parameters.values() for x in signatures]), extra):
        if param.name in {'self', 'cls'}:
            continue
        if param.name.startswith('_'):
            continue
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            continue
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            continue
        params[param.name] = param

    return signatures[0].replace(
        parameters=list(sorted(params.values(), key=lambda p: (p.kind, p.default != inspect._empty))) # type: ignore
    )


def merged_call(func: Callable[..., Any], kwargs: Any) -> Any:
    sig = inspect.signature(func)
    return func(**{k: v for k, v in kwargs.items() if k in sig.parameters})


def throw(cls: type[Exception], *args: Any, **kwargs: Any):
    raise cls(*args, **kwargs)


def jsonpath(mapping: abc.Mapping[str, Any], path: str) -> Any:
    if not str.startswith(path, '/'):
        raise ValueError("Path must start with a slash.")
    parts: list[str] = []
    for p in str.split(str.lstrip(path, '/'), '/'):
        p = p.replace('~0', '~')
        p = p.replace('~1', '/')
        parts.append(p)
    return reduce(operator.getitem, parts, mapping)
    