import abc
from abc import ABC, abstractmethod
from typing import Any

class BaseGraphRAGDataStore(ABC, metaclass=abc.ABCMeta):
    """Abstract base class for graph RAG data stores in the retrieval system.

    This class defines the interface for all graph data store implementations.
    """
    @abstractmethod
    def query(self, query: str, **kwargs: Any) -> Any:
        """Query the graph RAG data store.

        Args:
            query (str): The query to be executed.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Any: The result of the query.
        """
    @abstractmethod
    def delete_by_document_id(self, document_id: str, **kwargs: Any) -> None:
        """Delete nodes and edges by document ID.

        Args:
            document_id (str): The document ID.
            **kwargs (Any): Additional keyword arguments.
        """
