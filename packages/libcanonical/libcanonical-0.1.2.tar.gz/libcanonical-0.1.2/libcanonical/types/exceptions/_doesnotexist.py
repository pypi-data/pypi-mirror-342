from ._base import BaseCanonicalException


class DoesNotExist(BaseCanonicalException):
    """This exception may be raised when attempting for perform an operation
    on a resource that does not exist.
    """
    http_status_code: int = 404