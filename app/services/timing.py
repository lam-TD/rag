# timing.py
import time, logging
from contextlib import contextmanager

log = logging.getLogger("ingest")

@contextmanager
def span(name: str, ctx: dict):
    t0 = time.perf_counter()
    try:
        yield
    finally:
        dt = (time.perf_counter() - t0) * 1000
        log.info("span", extra={"span": name, "ms": round(dt,2), **ctx})