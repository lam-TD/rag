# strategy_factory.py
from __future__ import annotations
from abc import ABC, abstractmethod
import json
import urllib.request


# ==== Strategy ====
class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_texts(
        self, texts: list[str], *, task: str, dim: int
    ) -> list[list[float]]: ...


# ---- Jina v3 implementation (HTTP) ----
class JinaProvider(EmbeddingProvider):
    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        model: str = "jina-embeddings-v3",
    ):
        self.base = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def _post(self, path: str, payload: dict, timeout=60):
        req = urllib.request.Request(
            f"{self.base}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                **({"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}),
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))

    def embed_texts(
        self, texts: list[str], *, task: str = "retrieval.passage", dim: int = 1024
    ) -> list[list[float]]:
        payload = {"model": self.model, "input": texts, "task": task, "dimensions": dim}
        data = self._post("/v1/embeddings", payload)
        vecs = [item["embedding"] for item in data["data"]]
        for v in vecs:
            if len(v) != dim:
                raise ValueError(f"Dimension mismatch: expected {dim}, got {len(v)}")
        return vecs


# ---- (tuỳ chọn) Ollama implementation (loop từng câu) ----
class OllamaProvider(EmbeddingProvider):
    def __init__(
        self, host: str = "http://localhost:11434", model: str = "nomic-embed-text"
    ):
        self.host = host.rstrip("/")
        self.model = model

    def embed_texts(
        self, texts: list[str], *, task: str = "retrieval.passage", dim: int = 1024
    ) -> list[list[float]]:
        out = []
        for t in texts:
            payload = {"model": self.model, "prompt": t}
            req = urllib.request.Request(
                f"{self.host}/api/embeddings",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read().decode("utf-8"))
            v = data["embedding"]
            if len(v) != dim:
                raise ValueError(f"Dimension mismatch: expected {dim}, got {len(v)}")
            out.append(v)
        return out


# ==== Factory ====
class ProviderFactory:
    @staticmethod
    def create(name: str, **kw) -> EmbeddingProvider:
        if name == "jina":
            return JinaProvider(**kw)
        if name == "ollama":
            return OllamaProvider(**kw)
        raise ValueError(f"Unknown provider: {name}")
