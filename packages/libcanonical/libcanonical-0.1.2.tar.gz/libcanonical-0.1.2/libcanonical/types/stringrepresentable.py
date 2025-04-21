

class StringRepresentable:
    __module__: str = 'libcanonical.types'

    def __repr__(self) -> str: # pragma: no cover
        return f'<{type(self).__name__}: {str(self)}>'