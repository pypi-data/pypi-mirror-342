import hashlib

from .base64 import Base64

__all__: list[str] = [
    'DigestSHA256'
]


class DigestSHA256(Base64):
    __module__: str = 'libcanonical.types'
    dig = 'sha256'
    max_length = 32
    min_length = 32

    @classmethod
    def hasher(cls):
        return hashlib.new(cls.dig)