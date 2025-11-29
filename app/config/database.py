from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.env import get_env


class DatabaseConfig(BaseSettings):
    host: str = ""
    port: str | int = ""
    name: str = ""
    username: str = ""
    password: str = ""
    echo: bool = True


def get_db_config():
    env = get_env()
    return DatabaseConfig(
        host=env.db_host,
        port=env.db_port,
        name=env.db_name,
        password=env.db_password,
        username=env.db_username,
    )
