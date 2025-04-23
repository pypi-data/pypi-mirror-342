import re
from typing import cast
from typing import Any
from typing import Generic
from typing import TypeVar


T = TypeVar('T')


class RegexClassifier(Generic[T]):
    """Classifies object T with tags."""
    patterns: list[re.Pattern[str] | str] | re.Pattern[str]
    flags: int = 0

    @classmethod
    def __init_subclass__(cls, *args: Any, **kwargs: Any) -> None:
        if not hasattr(cls, 'patterns'):
            return
        if isinstance(cls.patterns, str):
            cls.patterns = re.compile(cls.patterns, flags=cls.flags)
        if isinstance(cls.patterns, re.Pattern):
            cls.patterns = [cls.patterns]
        for i, pattern in enumerate(cls.patterns):
            if isinstance(pattern, re.Pattern):
                continue
            cls.patterns[i] = re.compile(pattern, flags=cls.flags)

    def __init__(self) -> None:
        if not hasattr(self, 'patterns'):
            self.patterns = []

    def add_patterns(self, patterns: list[str | re.Pattern[str]]):
        assert isinstance(self.patterns, list)
        for p in patterns:
            if isinstance(p, str):
                p = re.compile(p, self.flags)
            self.patterns.append(p)

    def wants(self, obj: T) -> bool:
        """Return a boolean indicating if the classifier is interested
        in `obj`.
        """
        assert isinstance(self.patterns, list)
        return any([self.run_pattern(cast(re.Pattern[str], p), obj) for p in self.patterns])

    def run_pattern(self, pattern: re.Pattern[str], obj: T) -> re.Match[str] | None:
        if isinstance(obj, str) or hasattr(obj, '__str__'):
            return pattern.match(str(obj))
        raise TypeError(
            f"{type(obj).__name__} can not be cast to string. Override the "
            f"{type(self).__name__}.run_pattern() method or supply a string "
            "type."
        )

    def classify(self, obj: T) -> None:
        raise NotImplementedError