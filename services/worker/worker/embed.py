import os, httpx, numpy as np
from tenacity import retry, stop_after_attempt, wait_exponential

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
EMBED_DIM = int(os.getenv("EMBED_DIM", "3072"))

headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=1, max=10))
def embed_texts(texts: list[str]) -> np.ndarray:
    payload = {"model": EMBEDDING_MODEL, "input": texts}
    with httpx.Client(timeout=60) as client:
        r = client.post(f"{OPENAI_BASE_URL}/embeddings", json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
    vecs = [item["embedding"] for item in data["data"]]
    arr = np.array(vecs, dtype=np.float32)
    assert arr.shape[1] == EMBED_DIM, f"Expected {EMBED_DIM}, got {arr.shape[1]}"
    return arr
