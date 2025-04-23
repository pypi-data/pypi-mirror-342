from ._base import BaseCanonicalException


class Undecryptable(BaseCanonicalException):
    """This exception may be raised when the decryption of a ciphertext
    is attempted but the operation failed.
    """
    http_status_code: int = 503