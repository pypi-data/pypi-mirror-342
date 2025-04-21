

class AwaitableBool(int):
    """A bool that can be awaited. For sync/async cross-compatibility."""

    async def _async(self):
        return bool(self)

    def __await__(self):
        return self._async().__await__()