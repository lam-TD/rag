from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    """Load config from .env file"""

    model_config = SettingsConfigDict(env_file=".env.dev", extra="ignore")

    # app configuaration
    app_name: str = ""
    app_port: str | int = 8000
    app_debug: bool = False

    # database configuaration
    db_host: str = ""
    db_port: str | int = ""
    db_name: str = ""
    db_username: str = ""
    db_password: str = ""

    # embedding configuration
    embedding_default: str = ""
    embedding_api_key: str = ""
    embedding_base_url: str = ""
    embedding_default_model: str = ""



def get_env():
    return Env()
