from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.services.llm import google_gen_ai


ENV_FILE = Path(".env.dev")


class Env(BaseSettings):
    """Load config from .env file"""

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

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


def _env_file_version() -> int:
    try:
        return ENV_FILE.stat().st_mtime_ns
    except FileNotFoundError:
        return 0


@lru_cache(maxsize=1)
def _load_env(_: int) -> Env:
    # The argument is only used to invalidate the cache when the env file changes.
    return Env()


def get_env():
    return _load_env(_env_file_version())
