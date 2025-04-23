import pydantic


class Plaintext(pydantic.BaseModel):
    pt: bytes
    aad: bytes | None = None
    
    def __bytes__(self) -> bytes:
        return self.pt