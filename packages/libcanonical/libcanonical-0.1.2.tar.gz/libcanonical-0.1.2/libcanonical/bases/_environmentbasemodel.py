import os
import sys
import pathlib
import tempfile

import pydantic


class EnvironmentBaseModel(pydantic.BaseModel):
    model_config = {'populate_by_name': True}

    loglevel: str = pydantic.Field(
        default='INFO',
        alias='LOGLEVEL'
    )

    tmpdir: pathlib.Path = pydantic.Field(
        default=pathlib.Path(tempfile.gettempdir()),
        alias='TMPDIR'
    )

    vardir: pathlib.Path = pydantic.Field(
        default=pathlib.Path('var').absolute(),
        alias='VARDIR'
    )

    #@pydantic.field_validator('tmpdir', 'vardir', mode='after')
    #@classmethod
    #def validate_directory(
    #    cls,
    #    value: str | pathlib.Path,
    #    writable: bool = True
    #) -> pathlib.Path:
    #    if not os.path.exists(value):
    #        raise ValueError("no such directory")
    #    if not os.access(value, os.R_OK):
    #        raise ValueError("not allowed to read directory")
    #    if not os.path.isdir(value):
    #        raise ValueError("not a directory")
    #    if writable and not os.access(value, os.W_OK):
    #        raise ValueError("directory is not writable")
    #    return pathlib.Path(value)

    @classmethod
    def model_validate_env(cls, environ: dict[str, str] | None = None):
        environ = dict(environ or os.environ)
        try:
            return cls.model_validate(environ)
        except pydantic.ValidationError as exception:
            print("Unable to load environment variables", file=sys.stderr)
            for error in exception.errors():
                print(f"{error['loc'][0]}: {error['msg']} ({repr(error['input'])})")
            raise SystemExit(1)
