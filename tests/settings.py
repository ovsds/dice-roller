import enum

import pydantic_settings


class Environment(enum.Enum):
    development = "DEV"
    ci = "CI"
    container = "CONTAINER"


class PytestSettings(pydantic_settings.BaseSettings):
    environment: Environment = Environment.development

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="TESTS_",
    )


__all__ = [
    "PytestSettings",
]
