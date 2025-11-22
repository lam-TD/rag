from typing import Optional
from httpx import AsyncClient


class JinaEmbedding:

    def __init__(
        self,
        api_key: str,
        base_url: str,
        default_model: str,
        timeout: float = 60.0,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model
        self._client = AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
        )

    async def embed_texts(self, text, *, model: Optional[str] = None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        model = model or self.default_model
        payload = {
            "model": model,
            "task": "text-matching",
            "input": [text],
        }

        try:
            response = await self._client.post(
                "/v1/embeddings", json=payload, headers=headers
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(e)

            return None
