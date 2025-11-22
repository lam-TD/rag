from pydantic_settings import BaseSettings

from app.config.env import get_env


class DatabaseConfig(BaseSettings):
    host: str = ""
    port: str | int = ""
    name: str = ""
    username: str = ""
    password: str = ""


def get_db_config():
    env = get_env()
    return DatabaseConfig(host=env.db_host, port=env.db_port)
