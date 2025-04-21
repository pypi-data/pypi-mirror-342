import os
import pathlib

import pydantic


class EnvironmentVariables(pydantic.BaseModel):
    name: str = pydantic.Field(
        default=...
    )

    loglevel: str = pydantic.Field(
        alias='LOGLEVEL',
        default='INFO'
    )

    vardir: pathlib.Path = pydantic.Field(
        alias='VARDIR',
        default=...
    )

    @pydantic.model_validator(mode='before')
    def validate_params(cls, params: dict[str, str]):
        name = params.get('name')
        if not isinstance(name, str):
            raise pydantic.ValidationError()
        if not params.get('VARDIR'):
            params['VARDIR'] = f'/var/lib/{name}'
        return params

    @classmethod
    def parse(cls, app_name: str):
        return cls.model_validate({**os.environ, 'name': app_name})


defaults = EnvironmentVariables.parse('.canonical')