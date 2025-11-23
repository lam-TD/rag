from app.config.database import DatabaseConfig


class PGVector:
    def __init__(self, config: DatabaseConfig) -> None:
        self._config = config

    def get_engine(self):
        return ""
