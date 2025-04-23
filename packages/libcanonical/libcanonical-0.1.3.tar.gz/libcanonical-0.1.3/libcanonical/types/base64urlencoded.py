import base64

from .base64 import Base64

__all__: list[str] = [
    'Base64URLEncoded'
]



class Base64URLEncoded(Base64):
    __module__: str = 'libcanonical.types'

    @classmethod
    def b64decode(cls, value: str):
        return base64.urlsafe_b64decode(value)

    @classmethod
    def b64encode(cls, value: bytes | str) -> str:
        if isinstance(value, str):
            value = str.encode(value, 'utf-8')
        return  bytes.decode(base64.urlsafe_b64encode(value), 'ascii')