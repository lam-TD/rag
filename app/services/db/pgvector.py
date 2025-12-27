from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.database import DatabaseConfig, get_db_config


class PGVector:
    def __init__(self, config: DatabaseConfig):
        self._config = config

        self._engine: AsyncEngine
        self._sessionmaker: async_sessionmaker[AsyncSession]

    # ------------------- Public API -------------------

    def get_engine(self) -> AsyncEngine:
        """
        Lấy (và cache) AsyncEngine cho connection tương ứng.

        - connection = None  -> dùng default
        - connection = "sqlite"
        - connection = "pgvector"
        """

        conf = self._config

        # Lưu ý: URL phải dùng driver async (sqlite+aiosqlite, postgresql+psycopg, ...)
        db_url = f"postgresql+psycopg://{conf.username}:{conf.password}@{conf.host}:{conf.port}/{conf.name}"
        print(db_url)
        engine = create_async_engine(
            db_url,
            echo=True,
            future=True,
        )
        return engine

    def get_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        """
        Lấy (và cache) async_sessionmaker cho connection tương ứng.
        """

        engine = self.get_engine()

        session_local = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
        self._sessionmaker = session_local
        return session_local

    async def dispose_all(self) -> None:
        """
        Giải phóng tất cả engine (có thể gọi ở shutdown event của FastAPI).
        """
        await self._engine.dispose()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db_config = get_db_config()
    db = PGVector(config=db_config)
    async_session_factory = db.get_sessionmaker()

    async with async_session_factory() as session:
        yield session
