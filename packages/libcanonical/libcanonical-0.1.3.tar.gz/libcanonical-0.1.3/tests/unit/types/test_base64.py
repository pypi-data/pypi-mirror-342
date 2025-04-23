from libcanonical.types import Base64



def test_to_int():
    a = Base64.fromb64(b'AQAB')
    b = int(a)
    assert b == 65537


def test_from_int():
    a = Base64.fromint(65537)
    assert a == b'\x01\x00\x01'
