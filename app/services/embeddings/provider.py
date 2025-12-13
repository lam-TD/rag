from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from abc import ABC, abstractmethod


__all__ = [
    "EmbeddingProvider",
    "JinaProvider",
    "OllamaProvider",
    "ProviderFactory",
]


class EmbeddingProvider(ABC):
    """Interface Strategy cho nhà cung cấp embedding."""

    @abstractmethod
    def embed_texts(
        self, texts: list[str], *, task: str, dim: int
    ) -> list[list[float]]:
        """
        Trả về danh sách vector theo thứ tự đầu vào.
        Phải đảm bảo mỗi vector có đúng chiều `dim`, nếu không -> raise ValueError.
        """
        raise NotImplementedError


class JinaProvider(EmbeddingProvider):
    """
    Gọi Jina Embeddings v3 (HTTP thuần).
    API giả định OpenAI-like: POST /v1/embeddings
    Payload tối thiểu: {"model": "...", "input": [...], "task": "...", "dimensions": 1024}
    """

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        model: str = "jina-embeddings-v3",
        timeout: int = 60,
    ) -> None:
        self._base = base_url.rstrip("/")
        self._api_key = api_key
        self._model = model
        self._timeout = timeout
        self._ssl_ctx = ssl.create_default_context()

    def _post(self, path: str, payload: dict[str, object]) -> dict[str, object]:
        url = f"{self._base}{path}"
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(
                req, timeout=self._timeout, context=self._ssl_ctx
            ) as resp:
                raw = resp.read().decode("utf-8")
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            raise RuntimeError(f"Jina request failed: {exc}") from exc
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Jina response is not valid JSON") from exc
        if not isinstance(parsed, dict):
            raise RuntimeError("Jina response has unexpected structure")
        return parsed  # type: ignore[return-value]

    def embed_texts(
        self, texts: list[str], *, task: str, dim: int
    ) -> list[list[float]]:
        payload: dict[str, object] = {
            "model": self._model,
            "input": texts,
            "task": task,
            "dimensions": dim,
        }
        res = self._post("/v1/embeddings", payload)
        data = res.get("data")
        if not isinstance(data, list):
            raise RuntimeError("Jina response missing 'data' list")

        out: list[list[float]] = []
        for item in data:
            if not isinstance(item, dict):
                raise RuntimeError("Invalid item in 'data'")
            emb = item.get("embedding")
            if not isinstance(emb, list) or not all(
                isinstance(x, (float, int)) for x in emb
            ):
                raise RuntimeError("Invalid 'embedding' format")
            vec = [float(x) for x in emb]
            if len(vec) != dim:
                raise ValueError(f"Dimension mismatch: expected {dim}, got {len(vec)}")
            out.append(vec)
        if len(out) != len(texts):
            raise RuntimeError("Embedding count does not match inputs")
        return out


class OllamaProvider(EmbeddingProvider):
    """
    Gọi Ollama local embeddings (loop từng câu; vẫn thuần urllib).
    Chỉ dùng khi bạn muốn thay đổi provider nhanh để thử nghiệm.
    """

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "nomic-embed-text",
        timeout: int = 60,
    ) -> None:
        self._host = host.rstrip("/")
        self._model = model
        self._timeout = timeout

    def embed_texts(
        self, texts: list[str], *, task: str, dim: int
    ) -> list[list[float]]:  # noqa: ARG002
        out: list[list[float]] = []
        for t in texts:
            payload = {"model": self._model, "prompt": t}
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self._host}/api/embeddings",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                    raw = resp.read().decode("utf-8")
            except (urllib.error.HTTPError, urllib.error.URLError) as exc:
                raise RuntimeError(f"Ollama request failed: {exc}") from exc
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise RuntimeError("Ollama response is not valid JSON") from exc
            emb = parsed.get("embedding")
            if not isinstance(emb, list) or not all(
                isinstance(x, (float, int)) for x in emb
            ):
                raise RuntimeError("Invalid 'embedding' in Ollama response")
            vec = [float(x) for x in emb]
            if len(vec) != dim:
                raise ValueError(f"Dimension mismatch: expected {dim}, got {len(vec)}")
            out.append(vec)
        return out


class ProviderFactory:
    """Factory tạo provider theo tên ngắn gọn."""

    @staticmethod
    def create(name: str, **kwargs: object) -> EmbeddingProvider:
        key = name.strip().lower()
        if key == "jina":
            return JinaProvider(**kwargs)  # type: ignore[arg-type]
        if key == "ollama":
            return OllamaProvider(**kwargs)  # type: ignore[arg-type]
        raise ValueError(f"Unknown provider: {name}")
