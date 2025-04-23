import pydantic
import pytest

from canonical import ISO3166Alpha2


class Model(pydantic.BaseModel):
    country: ISO3166Alpha2


@pytest.mark.parametrize("value", [
    "NL",
    "BE",
    "DE"
])
def test_valid_codes(value: str):
    ISO3166Alpha2.validate(value)
    obj = Model.model_validate({'country': value})
    assert isinstance(obj.country, ISO3166Alpha2)


@pytest.mark.parametrize("value", [
    "B1",
    "ABC",
])
def test_invalid_codes(value: str):
    with pytest.raises(ValueError):
        ISO3166Alpha2.validate(value)


def test_eu_greece():
    code = ISO3166Alpha2.validate('EL')
    assert code == 'GR'


def test_eu_northern_ireland():
    code = ISO3166Alpha2.validate('XI')
    assert code == 'XI'


def test_eu_united_kingdom():
    code = ISO3166Alpha2.validate('UK')
    assert code == 'GB'


def test_name_nl():
    code = ISO3166Alpha2.validate('NL')
    assert code == 'NL'
    assert code.name == 'The Netherlands'


def test_name_be():
    code = ISO3166Alpha2.validate('BE')
    assert code == 'BE'
    assert code.name == 'Belgium'