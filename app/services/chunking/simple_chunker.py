from typing import Any, Dict, List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.chunking.interface import TextChunk, TextChunker


class SimpleChunker(TextChunker):
    """
    Chunker đơn giản:
      - Chia text theo paragraph (dựa trên 2 dòng trống)
      - Gộp paragraph thành chunk tới khi gần max_chars
      - Nếu paragraph quá dài, tách nhỏ theo word
      - Hỗ trợ overlap theo ký tự

    Phù hợp cho MVP RAG (Tika -> chunk -> embedding).
    """

    def __init__(
        self, default_max_chars: int = 1200, default_overlap_chars: int = 200
    ) -> None:
        self.default_max_chars = default_max_chars
        self.default_overlap_chars = default_overlap_chars

    def chunk(
        self,
        text: str,
        max_chars: int | None = None,
        overlap_chars: int | None = None,
        base_metadata: Dict[str, Any] | None = None
    ) -> List[str]:
        if not text or not text.strip():
            return []

        max_chars = max_chars or self.default_max_chars
        overlap_chars = (
            overlap_chars if overlap_chars is not None else self.default_overlap_chars
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_chars, chunk_overlap=overlap_chars
        )

        texts = text_splitter.split_text(text)

        idx = 0
        chunks: List[str] = []

        for value in texts:
            idx += 1
            chunks.append(value)

        return chunks
