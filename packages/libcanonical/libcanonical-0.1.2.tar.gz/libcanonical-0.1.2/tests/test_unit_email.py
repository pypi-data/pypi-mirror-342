import pydantic
import pytest

from canonical import EmailAddress


class Model(pydantic.BaseModel):
    email: EmailAddress


@pytest.mark.parametrize('v', [
    'abc@example.com',
])
def test_validate(v: str):
    adapter = pydantic.TypeAdapter(EmailAddress)
    adapter.validate_python(v)


@pytest.mark.parametrize('v', [
    'example.com',
    ('f' * 320) + '@example.com'
])
def test_invalid(v: str):
    adapter = pydantic.TypeAdapter(EmailAddress)
    with pytest.raises(ValueError):
        adapter.validate_python(v)


def test_as_model_attribute():
    obj = Model.model_validate({'email': 'abc@example.com'})
    assert isinstance(obj.email, EmailAddress)


def test_domain():
    adapter = pydantic.TypeAdapter(EmailAddress)
    e = adapter.validate_python('abc@example.com')
    assert e.domain == 'example.com'
