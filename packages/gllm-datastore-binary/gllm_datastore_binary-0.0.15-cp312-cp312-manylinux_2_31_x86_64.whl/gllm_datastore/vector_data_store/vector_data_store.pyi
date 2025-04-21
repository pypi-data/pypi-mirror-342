import abc
from abc import ABC, abstractmethod
from gllm_core.schema.chunk import Chunk as Chunk
from gllm_datastore.constants import DEFAULT_TOP_K as DEFAULT_TOP_K
from typing import Any

class BaseVectorDataStore(ABC, metaclass=abc.ABCMeta):
    """Abstract base class for vector data stores in the retrieval system.

    This class defines the interface for all vector data store implementations.
    Subclasses must implement the `query` and `query_by_id` methods.
    """
    @abstractmethod
    async def query(self, query: str, top_k: int = ..., retrieval_params: dict[str, Any] | None = None) -> list[Chunk]:
        """Executes a query on the data store.

        This method must be implemented by subclasses.

        Args:
            query (str): The query string to execute.
            top_k (int, optional): The maximum number of results to return. Defaults to DEFAULT_TOP_K.
            retrieval_params (dict[str, Any] | None, optional): Additional parameters for the query.
                Defaults to None.

        Returns:
            list[Chunk]: A list of query results.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
    @abstractmethod
    async def query_by_id(self, id_: str | list[str]) -> list[Chunk]:
        """Retrieves chunks by their IDs.

        This method must be implemented by subclasses.

        Args:
            id_ (str | list[str]): A single ID or a list of IDs to retrieve.

        Returns:
            list[Chunk]: A list of retrieved chunks.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
    @abstractmethod
    async def add_chunks(self, chunk: Chunk | list[Chunk], **kwargs) -> list[str]:
        """Adds a chunk or a list of chunks in the data store.

        This method must be implemented by subclasses.

        Args:
            chunk (Chunk | list[Chunk]): A single chunk or a list of chunks to index.
            **kwargs: Additional keyword arguments to pass to the method.

        Returns:
            list[str]: A list of unique identifiers (IDs) assigned to the added chunks.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
    @abstractmethod
    async def delete_chunks(self, **kwargs: Any) -> None:
        """Deletes a chunk or a list of chunks from the data store.

        This method must be implemented by subclasses.

        Args:
            kwargs: Additional keyword arguments to pass to the method.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
