

class AwaitableBytes(bytes):
    """A byte-sequence that can be awaited. For sync/async
    cross-compatibility.
    """

    async def _async(self):
        return bytes(self)

    def __await__(self):
        return self._async().__await__()