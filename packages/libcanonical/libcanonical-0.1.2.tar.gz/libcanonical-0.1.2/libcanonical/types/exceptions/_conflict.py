from ._base import BaseCanonicalException


class Conflict(BaseCanonicalException):
    """This exception may be raised when a destructive operation is
    attempted on a resource, that consitutes a data integrity contstaint
    violation.
    """
    http_status_code: int = 409