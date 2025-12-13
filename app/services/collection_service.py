from app.models.collection import Collection
from app.repositories.collection_repository import CollectionRepository
from app.schemas.collection import CollectionCreateRequest


class CollectionService:
    def __init__(self, repository: CollectionRepository):
        self.repository = repository

    async def paginate(self, offset: int = 0, limit: int = 10) -> list:
        return await self.repository.paginate(offset=offset, limit=limit)

    async def create(self, request: CollectionCreateRequest) -> Collection:
        collection = Collection(
            name=request.name,
            embedding_model=request.embedding_model,
            cmetadata=request.cmetadata or {},
        )

        return await self.repository.create(collection)
