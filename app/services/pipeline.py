# pipeline.py
from __future__ import annotations
from abc import ABC, abstractmethod
import time, math, threading

# ---- Decorators: retry + rate limit (qps) ----
def retry(max_attempts=3, backoff=0.5):
    def wrap(fn):
        def inner(*a, **k):
            last = None
            for i in range(max_attempts):
                try:
                    return fn(*a, **k)
                except Exception as e:
                    last = e
                    time.sleep(backoff * (2 ** i))
            raise last
        return inner
    return wrap

def ratelimit(qps: float):
    lock = threading.Lock()
    min_interval = 1.0 / max(qps, 1e-9)
    last = [0.0]
    def deco(fn):
        def inner(*a, **k):
            with lock:
                now = time.time()
                wait = min_interval - (now - last[0])
                if wait > 0: time.sleep(wait)
                last[0] = time.time()
            return fn(*a, **k)
        return inner
    return deco

# ---- Base step ----
class Step(ABC):
    @abstractmethod
    def run(self, ctx: dict) -> dict: ...

# ---- Concrete steps ----
class CleanStep(Step):
    def run(self, ctx: dict) -> dict:
        pages: list[dict] = ctx["pages"]
        cleaned = []
        for p in pages:
            text = p["text"].replace("\u00A0"," ").strip()
            if len(text) >= 50:
                cleaned.append({"page": p["page"], "text": text})
        ctx["pages"] = cleaned
        return ctx

class ChunkStep(Step):
    def __init__(self, size=1000, overlap=200):
        self.size=size; self.overlap=overlap
    def run(self, ctx: dict) -> dict:
        chunks=[]
        for pg in ctx["pages"]:
            t = pg["text"]
            i=0
            while i < len(t):
                j=min(i+self.size, len(t))
                piece=t[i:j].strip()
                if piece:
                    chunks.append({"doc_id": ctx["doc_id"], "page": pg["page"], "text": piece})
                i = max(j - self.overlap, j)
        ctx["chunks"]=chunks
        return ctx

class DedupStep(Step):
    def run(self, ctx: dict) -> dict:
        seen=set(); out=[]
        for c in ctx["chunks"]:
            key=c["text"][:200]
            if key in seen: continue
            seen.add(key); out.append(c)
        ctx["chunks"]=out
        return ctx

class EmbedStep(Step):
    def __init__(self, provider, batch=32, dim=1024, task="retrieval.passage", qps=8.0):
        self.provider=provider; self.batch=batch; self.dim=dim; self.task=task
        self._call = ratelimit(qps)(retry(3)(self.provider.embed_texts))

    def run(self, ctx: dict) -> dict:
        texts=[c["text"] for c in ctx["chunks"]]
        vecs=[]
        for i in range(0, len(texts), self.batch):
            batch=texts[i:i+self.batch]
            vecs.extend(self._call(batch, task=self.task, dim=self.dim))
        for c, v in zip(ctx["chunks"], vecs):
            c["embedding"]=v
        return ctx

class StoreStep(Step):
    def __init__(self, repo): self.repo=repo
    def run(self, ctx: dict) -> dict:
        self.repo.bulk_insert(ctx["chunks"])  # tuỳ bạn hiện thực
        return ctx

# ---- Pipeline runner ----
class Pipeline:
    def __init__(self, steps: list[Step]): self.steps=steps
    def run(self, ctx: dict) -> dict:
        for s in self.steps:
            t0=time.perf_counter()
            ctx=s.run(ctx)
            ctx.setdefault("_spans",[]).append((s.__class__.__name__, round((time.perf_counter()-t0)*1000,2)))
        return ctx