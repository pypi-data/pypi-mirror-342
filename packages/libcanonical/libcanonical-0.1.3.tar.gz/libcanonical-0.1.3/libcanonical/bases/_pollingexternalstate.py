from ._externalstate import ExternalState


class PollingExternalState(ExternalState):
    """An :class:`~libcanonical.bases.ExternalState` implementation that
    uses polling as it's transport mechanism.
    """
    __module__: str = 'libcanonical.bases'

    #: The interval between queries at the remote source for the
    #: current state.
    interval: float = 10.0

    #

    async def poll(self) -> None:
        """Polls the remote source for data."""
        raise NotImplementedError