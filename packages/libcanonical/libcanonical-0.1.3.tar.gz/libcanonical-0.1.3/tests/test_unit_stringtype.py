import pydantic
import pytest

from canonical import StringType


class ConstrainedStringType(StringType):
    pattern = r'^[0-9]+$'
    min_length = 2
    max_length = 3


@pytest.mark.parametrize('v', [
    'aaa',
    '1',
    '1234'
])
def test_invalid_model(v: str):
    class Model(pydantic.BaseModel):
        value: ConstrainedStringType

    with pytest.raises(pydantic.ValidationError):
        Model.model_validate({'value': v})