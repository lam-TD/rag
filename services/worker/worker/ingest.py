from __future__ import annotations
import hashlib, math
from typing import List, Tuple
from sqlalchemy import text
from .db import get_engine
from .embed import embed_texts
from .s3io import read_text_object

# --- Chunking đơn giản theo ký tự (an toàn cho MVP) ---
def chunk_text(s: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
    if chunk_size <= overlap:
        overlap = max(0, chunk_size // 5)
    chunks = []
    i = 0
    n = len(s)
    while i < n:
        chunk = s[i : i + chunk_size]
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def upsert_chunks(document_id: str, version_id: str, texts: List[str]):
    """Upsert chunks + embeddings vào bảng chunks; chunk_idx tăng dần."""
    if not texts:
        return
    # embed
    vecs = embed_texts(texts)  # shape (m, 3072)
    engine = get_engine()
    with engine.begin() as conn:
        for idx, (t, v) in enumerate(zip(texts, vecs.tolist())):
            conn.execute(
                text("""
INSERT INTO chunks (document_id, version_id, chunk_idx, text, embedding, meta)
VALUES (:doc, :ver, :idx, :txt, :emb, '{}'::jsonb)
ON CONFLICT DO NOTHING
                """),
                {"doc": document_id, "ver": version_id, "idx": idx, "txt": t, "emb": v},
            )

def ingest_txt(document_id: str, version_id: str, s3_key: str, expected_sha256: str | None = None):
    txt = read_text_object(s3_key)
    if expected_sha256:
        got = sha256_bytes(txt.encode("utf-8", errors="ignore"))
        if got != expected_sha256:
            raise ValueError(f"sha256 mismatch: got {got}, expected {expected_sha256}")

    parts = chunk_text(txt, 1500, 200)
    # batch embeddings để tiết kiệm round-trip
    BATCH = 128
    for i in range(0, len(parts), BATCH):
        batch = parts[i:i+BATCH]
        upsert_chunks(document_id, version_id, batch)
