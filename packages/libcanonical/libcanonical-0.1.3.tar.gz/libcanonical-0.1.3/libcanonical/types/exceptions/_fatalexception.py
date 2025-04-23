import sys


class FatalException(SystemExit):
    """Represent an exception condition which prevents an process from
    continuing to run.
    """
    exitcode: int = 1

    def __init__(self, reason: str):
        sys.stderr.write(reason + '\n')
        sys.stderr.flush()
        super().__init__(self.exitcode)