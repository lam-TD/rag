from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.collection import Collection


class ModelNotFound(Exception):
    pass


class CollectionRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _query_by_id(self, collection_id: str | int) -> Select:
        return select(Collection).where(Collection.id == collection_id)

    async def find(self, collection_id: str | int) -> Collection | None:
        result = await self.db_session.execute(self._query_by_id(collection_id))
        return result.scalar_one_or_none()

    async def find_or_fail(self, collection_id: str | int) -> Collection:
        collection = await self.find(collection_id)
        if collection is None:
            raise ModelNotFound(
                "Collection not found"
            )  # Replace with custom exception if needed
        return collection

    async def all(self) -> list[Collection]:
        result = await self.db_session.execute(
            select(Collection).order_by(Collection.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(self, collection: Collection) -> Collection:
        self.db_session.add(collection)
        await self.db_session.commit()
        await self.db_session.refresh(collection)
        return collection

    async def paginate(self, offset: int = 0, limit: int = 10) -> list[Collection]:
        result = await self.db_session.execute(
            select(Collection)
            .order_by(Collection.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
