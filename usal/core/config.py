from typing import ClassVar, TypeVar

from pydantic import BaseModel
from wireup.errors import UnknownParameterError

from usal.core.container import container

Model = TypeVar("Model", bound="ConfigModel")


class ConfigModel(BaseModel):
    __key__ = ClassVar[str]

    @classmethod
    def build(cls: type[Model]) -> Model:
        model = cls.may_be_build()

        if model is None:
            raise ValueError(
                f"Missing configuration for {cls.__key__}. Please add the key to your yaml config file."
            )

        return model

    @classmethod
    def may_be_build(cls: type[Model]) -> Model | None:
        key = str(cls.__key__)

        if str(key) == "__main__":
            params = container.params.get_all()
        else:
            try:
                params = container.params.get(key)
            except UnknownParameterError:
                return None
        return cls.model_validate(params)


class AppConfig(ConfigModel):
    __key__ = "application"

    app_name: str
    app_version: str


class DatabaseConfig(ConfigModel):
    __key__ = "database"

    user: str
    password: str
    host: str
    port: int
    branch: str
    instance: str
    timezone: str
    tls_file: str


class Config(ConfigModel):
    __key__ = "__main__"

    application: AppConfig
    database: DatabaseConfig


class LogfireConfig(ConfigModel):
    __key__ = "logfire"

    token: str


class AWSConfig(ConfigModel):
    __key__ = "aws"

    url: str
    access_key: str
    secret_key: str
    region: str
    bucket_name: str


class FirebaseConfig(ConfigModel):
    __key__ = "firebase"

    api_key: str


class SystemTypeConfig(ConfigModel):
    __key__ = "system_type"

    type_: str


class ValkeyConfig(ConfigModel):
    __key__ = "valkey"

    host: str
    port: int


class EmailConfig(ConfigModel):
    __key__ = "email"

    password: str
    username: str
    port: int
    host: str
