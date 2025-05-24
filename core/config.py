import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 9999
    WORKERS_COUNT: int = 1


class TestConfig(Config): ...


class LocalConfig(Config):
    ENV: str = "local"


class ProductionConfig(Config):
    DEBUG: bool = False


def get_config():
    config_type = {
        "local": LocalConfig(),
        "production": ProductionConfig(),
        "test": TestConfig(),
    }
    return config_type["local"]


config: Config = get_config()
