from httpx import AsyncClient


class TikaExtractor:
    def __init__(self, base_url: str, timeout: int = 60) -> None:
        self._client = AsyncClient(base_url=base_url, timeout=timeout)

    async def extract(self, file_bytes: bytes) -> str:
        headers = {"Accept": "text/plain"}

        response = await self._client.put(
            url="/tika", content=file_bytes, headers=headers
        )
        response.raise_for_status()

        text = response.text

        return text

    async def aclose(self) -> None:
        await self._client.aclose()
