from __future__ import annotations

import threading
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeVar

from .providers import EmbeddingProvider
from .types import ChunkDict, Repository

__all__ = [
    "ChunkStep",
    "CleanStep",
    "DedupStep",
    "EmbedStep",
    "Pipeline",
    "Step",
    "StoreStep",
    "ratelimit",
    "retry",
]


T = TypeVar("T")


def retry(
    max_attempts: int = 3, backoff: float = 0.5
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator retry theo cấp số nhân đơn giản.
    - max_attempts: số lần thử
    - backoff: thời gian chờ cơ sở (giây). Lần n: backoff * 2^(n-1)
    """

    def wrap(fn: Callable[..., T]) -> Callable[..., T]:
        def inner(*args: object, **kwargs: object) -> T:
            last_exc: Exception | None = None
            for i in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    time.sleep(backoff * (2.0**i))
            assert last_exc is not None
            raise last_exc

        return inner

    return wrap


def ratelimit(qps: float) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator giới hạn tần suất gọi (QPS).
    Dùng Lock để an toàn luồng.
    """
    lock = threading.Lock()
    min_interval = 1.0 / max(qps, 1e-9)
    last_ts = 0.0

    def deco(fn: Callable[..., T]) -> Callable[..., T]:
        def inner(*args: object, **kwargs: object) -> T:
            nonlocal last_ts
            with lock:
                now = time.time()
                wait = min_interval - (now - last_ts)
                if wait > 0.0:
                    time.sleep(wait)
                last_ts = time.time()
            return fn(*args, **kwargs)

        return inner

    return deco


class Step(ABC):
    """Bước trong Pipeline."""

    @abstractmethod
    def run(self, ctx: dict[str, Any]) -> dict[str, Any]:
        """Thực thi bước và trả về context đã cập nhật."""
        raise NotImplementedError


class CleanStep(Step):
    """Làm sạch tối giản: trim, loại trang quá ngắn, thay NBSP."""

    def __init__(self, min_len: int = 50) -> None:
        self._min_len = min_len

    def run(self, ctx: dict[str, Any]) -> dict[str, Any]:
        pages: list[dict[str, Any]] = ctx.get("pages", [])
        cleaned: list[dict[str, Any]] = []
        for p in pages:
            text = str(p.get("text", "")).replace("\u00a0", " ").strip()
            if len(text) >= self._min_len:
                cleaned.append({"page": int(p.get("page", 0)), "text": text})
        ctx["pages"] = cleaned
        return ctx


class ChunkStep(Step):
    """Cắt theo ký tự, có overlap, trên từng trang."""

    def __init__(self, size: int = 1000, overlap: int = 200) -> None:
        if size <= 0:
            raise ValueError("size must be > 0")
        if overlap < 0 or overlap >= size:
            raise ValueError("overlap must be in [0, size)")
        self._size = size
        self._overlap = overlap

    def run(self, ctx: dict[str, Any]) -> dict[str, Any]:
        doc_id = str(ctx.get("doc_id", "unknown"))
        pages: list[dict[str, Any]] = ctx.get("pages", [])
        chunks: list[ChunkDict] = []
        for pg in pages:
            page_no = int(pg.get("page", 0))
            text = str(pg.get("text", ""))
            i = 0
            n = len(text)
            while i < n:
                j = min(i + self._size, n)
                piece = text[i:j].strip()
                if piece:
                    chunks.append(ChunkDict(doc_id=doc_id, page=page_no, text=piece))
                i = max(j - self._overlap, j)
        ctx["chunks"] = chunks
        return ctx


class DedupStep(Step):
    """Khử trùng lặp thô theo tiền tố 200 ký tự."""

    def __init__(self, key_prefix: int = 200) -> None:
        self._key_prefix = key_prefix

    def run(self, ctx: dict[str, Any]) -> dict[str, Any]:
        chunks: list[ChunkDict] = ctx.get("chunks", [])
        seen: set[str] = set()
        out: list[ChunkDict] = []
        for c in chunks:
            key = c.get("text", "")[: self._key_prefix]
            if key and key not in seen:
                seen.add(key)
                out.append(c)
        ctx["chunks"] = out
        return ctx


class EmbedStep(Step):
    """Gọi provider.embed_texts theo batch, có retry + rate limit."""

    def __init__(
        self,
        provider: EmbeddingProvider,
        *,
        batch: int = 32,
        dim: int = 1024,
        task: str = "retrieval.passage",
        qps: float = 8.0,
    ) -> None:
        if batch <= 0:
            raise ValueError("batch must be > 0")
        self._provider = provider
        self._batch = batch
        self._dim = dim
        self._task = task
        self._call = ratelimit(qps)(retry(3)(self._provider.embed_texts))

    def run(self, ctx: dict[str, Any]) -> dict[str, Any]:
        chunks: list[ChunkDict] = ctx.get("chunks", [])
        texts = [str(c.get("text", "")) for c in chunks]
        all_vecs: list[list[float]] = []
        for i in range(0, len(texts), self._batch):
            batch_texts = texts[i : i + self._batch]
            vecs = self._call(batch_texts, task=self._task, dim=self._dim)
            all_vecs.extend(vecs)
        for c, v in zip(chunks, all_vecs, strict=False):
            c["embedding"] = v
        ctx["chunks"] = chunks
        return ctx


class StoreStep(Step):
    """Ghi hàng loạt vào kho lưu trữ (DB/CSV/… tuỳ bạn hiện thực)."""

    def __init__(self, repo: Repository) -> None:
        self._repo = repo

    def run(self, ctx: dict[str, Any]) -> dict[str, Any]:
        chunks: list[ChunkDict] = ctx.get("chunks", [])
        if chunks:
            self._repo.bulk_insert(chunks)
        return ctx


class Pipeline:
    """Runner tuần tự các bước, có đo thời gian từng bước."""

    def __init__(self, steps: list[Step]) -> None:
        self._steps = steps

    def run(self, ctx: dict[str, Any]) -> dict[str, Any]:
        spans: list[tuple[str, float]] = []
        for step in self._steps:
            t0 = time.perf_counter()
            ctx = step.run(ctx)
            dt_ms = (time.perf_counter() - t0) * 1000.0
            spans.append((step.__class__.__name__, round(dt_ms, 2)))
        ctx["_spans"] = spans
        return ctx
