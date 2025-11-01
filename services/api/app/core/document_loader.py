from langchain.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, TokenTextSplitter

SEPARATORS = [
    "\n\n",
    "\n",
    " ",
    ".",
    ",",
    "\u200b",  # Zero-width space
    "\uff0c",  # Fullwidth comma
    "\u3001",  # Ideographic comma
    "\uff0e",  # Fullwidth full stop
    "\u3002",  # Ideographic full stop
    "",
]


def load_document(file_path: str) -> list:
    """Load a document from the given file path."""
    document = TextLoader(file_path).load()
    return document


def make_token_splitter(
    model_name: str = "gpt-4o-mini",
    chunk_tokens: int = 1500,
    overlap_tokens: int = 150,
) -> TokenTextSplitter:
    # Dùng khi cần kiểm soát chi phí theo token
    from langchain_text_splitters import TokenTextSplitter

    return TokenTextSplitter(
        model_name=model_name,
        chunk_size=chunk_tokens,
        chunk_overlap=overlap_tokens,
        disallowed_special=(),
    )


def split_document(document: str) -> list[str]:
    """Split the document into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100, chunk_overlap=20, separators=SEPARATORS
    )
    return text_splitter.split_text(load_document(document)[0].page_content)
