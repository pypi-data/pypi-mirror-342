from _typeshed import Incomplete
from chromadb.types import Where as Where, WhereDocument as WhereDocument
from enum import Enum
from gllm_core.schema.chunk import Chunk
from gllm_datastore.constants import DEFAULT_TOP_K as DEFAULT_TOP_K
from gllm_datastore.utils.converter import from_langchain as from_langchain, to_langchain as to_langchain
from gllm_datastore.vector_data_store.vector_data_store import BaseVectorDataStore as BaseVectorDataStore
from langchain_core.documents import Document as Document
from langchain_core.embeddings import Embeddings as Embeddings
from typing import Any

DEFAULT_NUM_CANDIDATES: int

class ChromaClientType(str, Enum):
    """Enum for different types of ChromaDB clients.

    Attributes:
        MEMORY (str): Client type for an in-memory data store.
        PERSISTENT (str): Client type for a persistent data store.
        HTTP (str): Client type for a client-server architecture.
    """
    MEMORY = 'memory'
    PERSISTENT = 'persistent'
    HTTP = 'http'

class ChromaVectorDataStore(BaseVectorDataStore):
    """Datastore for interacting with ChromaDB.

    This class provides methods to interact with ChromaDB for vector storage and retrieval
    using the langchain-chroma integration.

    Attributes:
        collection_name (str): The name of the ChromaDB collection to use.
        embedding: The model used to generate embeddings.
        client: The ChromaDB client instance.
            1. MEMORY: In-memory client (chromadb.Client)
            2. PERSISTENT: Persistent client (chromadb.PersistentClient)
            3. HTTP: HTTP client for client-server architecture (chromadb.HttpClient)
        vector_store (Chroma): The langchain Chroma vector store instance.
        num_candidates (int): The maximum number of candidates to consider during search.
    """
    collection_name: Incomplete
    embedding: Incomplete
    vector_store: Incomplete
    num_candidates: Incomplete
    def __init__(self, collection_name: str, embedding: Embeddings | None = None, client_type: ChromaClientType = ..., persist_directory: str | None = None, host: str | None = None, port: int | None = None, num_candidates: int = ..., **kwargs: Any) -> None:
        """Initialize the ChromaDB vector data store with langchain-chroma.

        Args:
            collection_name (str): Name of the collection to use in ChromaDB.
            embedding (Embeddings | None): Function to generate embeddings.
            client_type (ChromaClientType, optional): Type of ChromaDB client to use.
                Defaults to ChromaClientType.MEMORY.
            persist_directory (str | None, optional): Directory to persist vector store data.
                Required for PERSISTENT client type. Defaults to None.
            host (str | None, optional): Host address for ChromaDB server.
                Required for HTTP client type. Defaults to None.
            port (int | None, optional): Port for ChromaDB server.
                Required for HTTP client type. Defaults to None.
            num_candidates (int, optional): Maximum number of candidates to consider during search.
                Defaults to DEFAULT_NUM_CANDIDATES.
            **kwargs: Additional parameters for Chroma initialization.

        Note:
            num_candidates (int, optional): This constant affects the maximum number of results to consider
            during the search. Index with more documents would need a higher value for the whole documents
            to be considered during search. This happens due to a bug with Chroma's search algorithm as discussed
            in this issue: [3] https://github.com/langchain-ai/langchain/issues/1946
        """
    async def query(self, query: str, top_k: int = ..., retrieval_params: dict[str, dict[str, str]] | None = None) -> list[Chunk]:
        '''Query the vector data store for similar chunks.

        Args:
            query (str): The query string to find similar chunks for.
            top_k (int, optional): Maximum number of results to return. Defaults to DEFAULT_TOP_K.
            retrieval_params (dict[str, Any] | None, optional): Additional parameters for retrieval.
                - filter (Where, optional): A Where type dict used to filter the retrieval by the metadata keys.
                    E.g. `{"$and": [{"color" : "red"}, {"price": {"$gte": 4.20}]}}`.
                - where_document (WhereDocument, optional): A WhereDocument type dict used to filter the retrieval by
                    the document content. E.g. `{$contains: {"text": "hello"}}`.
                Defaults to None.

        Returns:
            list[Chunk]: A list of Chunk objects matching the query.
        '''
    async def query_by_id(self, id: str | list[str]) -> list[Chunk]:
        """Retrieve chunks by their IDs.

        Args:
            id (str | list[str]): A single ID or a list of IDs to retrieve.

        Returns:
            list[Chunk]: A list of retrieved Chunk objects.
        """
    async def add_chunks(self, chunks: Chunk | list[Chunk], **kwargs) -> list[str]:
        """Add chunks to the vector data store.

        Args:
            chunks (Chunk | list[Chunk]): A single chunk or list of chunks to add.
            **kwargs: Additional keyword arguments for the add operation.

        Returns:
            list[str]: List of IDs of the added chunks.
        """
    async def delete_chunks(self, ids: list[str] = None, where: Where | None = None, where_document: WhereDocument | None = None) -> None:
        '''Delete chunks from the vector data store.

        Args:
            ids (list[str], optional): List of IDs of chunks to delete. Defaults to None. If not provided, the deletion
                all chunks will be based on the `where` and `where_document` filters. If all are None, all chunks will
                be deleted.
            where (Where | None, optional): A Where type dict used to filter the deletion by the metadata keys.
                E.g. `{"$and": [{"color" : "red"}, {"price": {"$gte": 4.20}]}}`. Defaults to None.
            where_document (WhereDocument | None, optional): A WhereDocument type dict used to filter the deletion by
                the document content. E.g. `{$contains: {"text": "hello"}}`. Defaults to None.

        Note:
            If no parameters are provided, all chunks in the collection will be deleted. Please use with caution.
        '''
