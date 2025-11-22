from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    """Load config from .env file"""

    # app configuaration
    app_name: str = ""
    app_port: str | int = 8000
    app_debug: bool = False

    # database configuaration
    db_host: str = ""
    db_port: str | int = ""
    db_url: str = ""
    db_name: str = ""
    db_username: str = ""
    db_password: str = ""

    model_config = SettingsConfigDict(env_file=".env.dev")


@lru_cache
def get_env():
    return Env()
