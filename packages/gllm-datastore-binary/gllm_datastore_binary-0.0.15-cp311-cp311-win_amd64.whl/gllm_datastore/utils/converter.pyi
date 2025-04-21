from gllm_core.schema import Chunk
from langchain_core.documents import Document

def from_langchain(doc: Document) -> Chunk:
    """Create a standardized Chunk from a LangChain Document.

    Args:
        doc (Document): The document to create a Chunk from.

    Returns:
        Chunk: The standardized Chunk object.
    """
def to_langchain(chunk: Chunk) -> Document:
    """Create a LangChain Document from a standardized Chunk.

    Args:
        chunk (Chunk): The standardized Chunk to create a Document from.

    Returns:
        Document: The LangChain Document object.
    """
