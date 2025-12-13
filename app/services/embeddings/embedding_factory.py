from __future__ import annotations

from app.core.settings import EmbeddingProviderName, Settings
from app.services.embedding_protocols import EmbeddingServiceProtocol
from app.services.jina_embedding_service import (
    JinaEmbeddingClientConfig,
    JinaEmbeddingService,
)
from app.services.openai_embedding_service import (
    OpenAIEmbeddingClientConfig,
    OpenAIEmbeddingService,
)
from app.services.local_embedding_service import (
    LocalEmbeddingClientConfig,
    LocalEmbeddingService,
)


class EmbeddingServiceFactory:
    """
    Factory chịu trách nhiệm tạo EmbeddingService đúng provider.

    - Config provider mặc định ở Settings.embedding_provider
    - Có thể override per-call bằng parameter provider (nếu muốn).
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def create(
        self, provider: EmbeddingProviderName | None = None
    ) -> EmbeddingServiceProtocol:
        provider_name = provider or self._settings.embedding_provider

        if provider_name == "jina":
            config = JinaEmbeddingClientConfig(
                base_url=self._settings.jina_base_url,
                api_key=self._settings.jina_api_key,
            )
            return JinaEmbeddingService(config=config)

        if provider_name == "openai":
            config = OpenAIEmbeddingClientConfig(
                base_url=self._settings.openai_base_url,
                api_key=self._settings.openai_api_key,
            )
            return OpenAIEmbeddingService(config=config)

        if provider_name == "local":
            config = LocalEmbeddingClientConfig(
                base_url=self._settings.local_embedding_base_url,
                api_key=self._settings.local_embedding_api_key,
            )
            return LocalEmbeddingService(config=config)

        msg = f"Unsupported embedding provider: {provider_name}"
        raise ValueError(msg)
