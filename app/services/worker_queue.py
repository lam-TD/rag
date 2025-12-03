# worker_queue.py
from __future__ import annotations
from dataclasses import dataclass
from queue import Queue, Empty
import threading, time

@dataclass
class EmbedJob:
    doc_id: str
    chunks: list[dict]         # [{"text": "...", "page": 3, ...}]
    task: str = "retrieval.passage"
    dim: int = 1024

class EmbedWorker(threading.Thread):
    def __init__(self, q: Queue, provider, repo, batch=32, qps=8.0):
        super().__init__(daemon=True)
        self.q=q; self.provider=provider; self.repo=repo
        self.batch=batch; self.min_interval = 1.0/max(qps,1e-9)
        self._last = 0.0

    def _ratelimit(self):
        now=time.time(); wait=self.min_interval-(now-self._last)
        if wait>0: time.sleep(wait)
        self._last=time.time()

    def run(self):
        while True:
            try:
                job: EmbedJob = self.q.get(timeout=1)
            except Empty:
                continue
            # embed theo batch
            texts=[c["text"] for c in job.chunks]
            vecs=[]
            for i in range(0, len(texts), self.batch):
                self._ratelimit()
                batch=texts[i:i+self.batch]
                # retry đơn giản
                for attempt in range(3):
                    try:
                        vecs.extend(self.provider.embed_texts(batch, task=job.task, dim=job.dim))
                        break
                    except Exception:
                        time.sleep(0.5*(2**attempt))
                        if attempt==2: raise
            # gắn embedding và lưu
            for c,v in zip(job.chunks, vecs):
                c["embedding"]=v
            self.repo.bulk_insert(job.chunks)
            self.q.task_done()

# ---- Khởi tạo hàng đợi và worker ----
def start_workers(n, provider, repo, **opts):
    q = Queue(maxsize=100)
    workers = [EmbedWorker(q, provider, repo, **opts) for _ in range(n)]
    for w in workers: w.start()
    return q, workers