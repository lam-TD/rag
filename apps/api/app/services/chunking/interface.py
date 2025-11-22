from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TextChunk:
    """
    Một đoạn text sau khi chunk.

    - index: thứ tự chunk trong tài liệu (0, 1, 2, ...)
    - content: nội dung chunk
    - metadata: bạn có thể nhét doc_id, page, source, ...
    """

    index: int
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class TextChunker(ABC):
    """
    Interface chung cho mọi loại chunker.
    Sau này bạn muốn thêm:
      - TokenBasedChunker
      - MarkdownAwareChunker
    thì chỉ cần implement cùng interface.
    """

    @abstractmethod
    def chunk(
        self,
        text: str,
        max_chars: Optional[int] = None,
        overlap_chars: Optional[int] = None,
        base_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[TextChunk]:
        """
        Chia text thành nhiều chunk.

        - max_chars: số ký tự tối đa cho mỗi chunk
        - overlap_chars: số ký tự overlap giữa các chunk (để giữ context)
        - base_metadata: metadata chung sẽ được copy vào từng chunk
        """
        ...
