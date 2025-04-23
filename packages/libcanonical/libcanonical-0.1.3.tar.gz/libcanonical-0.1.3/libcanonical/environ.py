import ipaddress
import os
import pathlib
from typing import Literal

import pydantic
from jinja2 import Template
from jinja2 import StrictUndefined


class EnvironmentVariables(pydantic.BaseModel):
    debug: bool = pydantic.Field(
        alias='DEBUG',
        default=False
    )

    deployment_env: Literal['development', 'testing', 'staging', 'production'] = pydantic.Field(
        alias='DEPLOYMENT_ENV',
        default='production'
    )

    name: str = pydantic.Field(
        default=...
    )

    loglevel: str = pydantic.Field(
        alias='LOGLEVEL',
        default='INFO'
    )

    etcdir: pathlib.Path = pydantic.Field(
        alias='ETCDIR',
        default=...
    )

    vardir: pathlib.Path = pydantic.Field(
        alias='VARDIR',
        default=...
    )

    #: The bind address of the primary HTTP interface.
    http_bind_address: ipaddress.IPv4Address = pydantic.Field(
        alias='HTTP_HOST',
        default=ipaddress.IPv4Address('127.0.0.1')
    )

    #: The port of the primary HTTP interface.
    http_bind_port: int = pydantic.Field(
        alias='HTTP_PORT',
        default=8000
    )

    @pydantic.model_validator(mode='before')
    def validate_params(cls, params: dict[str, str]):
        name = params.get('name')
        if not isinstance(name, str):
            raise pydantic.ValidationError()
        if not params.get('VARDIR'):
            params['ETCDIR'] = f'/etc/{name}'
        if not params.get('VARDIR'):
            params['VARDIR'] = f'/var/lib/{name}'
        return params

    @classmethod
    def parse(cls, app_name: str):
        return cls.model_validate({**os.environ, 'name': app_name})

    def parse_config_file(self, filename: str) -> str:
        """Parses a configuration file relative to :attr:`etcdir`."""
        t = Template(
            source=open(self.etcdir.joinpath(filename)).read(),
            variable_start_string='${',
            variable_end_string='}',
            undefined=StrictUndefined
        )
        return t.render(
            env={
                **os.environ,
                **self.model_dump(
                    mode='json',
                    by_alias=True,
                    exclude_none=True
                )
            }
        )


defaults = EnvironmentVariables.parse('.canonical')