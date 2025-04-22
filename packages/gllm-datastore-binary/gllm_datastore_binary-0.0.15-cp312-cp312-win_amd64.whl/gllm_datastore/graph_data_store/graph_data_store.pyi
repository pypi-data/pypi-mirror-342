import abc
from abc import ABC, abstractmethod
from typing import Any

class BaseGraphDataStore(ABC, metaclass=abc.ABCMeta):
    """Abstract base class for a graph data store interface."""
    @abstractmethod
    def upsert_node(self, label: str, identifier_key: str, identifier_value: str, properties: dict[str, Any] | None) -> Any:
        """Upsert a node in the graph.

        Args:
            label (str): The label of the node.
            identifier_key (str): The key of the identifier.
            identifier_value (str): The value of the identifier.
            properties (dict[str, Any] | None, optional): The properties of the node. Defaults to None.

        Returns:
            Any: The result of the operation.
        """
    @abstractmethod
    def upsert_relationship(self, node_source_key: str, node_source_value: str, relation: str, node_target_key: str, node_target_value: str, properties: dict[str, Any] | None) -> Any:
        """Upsert a relationship between two nodes in the graph.

        Args:
            node_source_key (str): The key of the source node.
            node_source_value (str): The value of the source node.
            relation (str): The type of the relationship.
            node_target_key (str): The key of the target node.
            node_target_value (str): The value of the target node.
            properties (dict[str, Any] | None, optional): The properties of the relationship. Defaults to None.

        Returns:
            Any: The result of the operation.
        """
    @abstractmethod
    def delete_node(self, label: str, identifier_key: str, identifier_value: str) -> Any:
        """Delete a node from the graph.

        Args:
            label (str): The label of the node.
            identifier_key (str): The key of the identifier.
            identifier_value (str): The identifier of the node.

        Returns:
            Any: The result of the operation.
        """
    @abstractmethod
    def delete_relationship(self, node_source_key: str, node_source_value: str, relation: str, node_target_key: str, node_target_value: str) -> Any:
        """Delete a relationship between two nodes in the graph.

        Args:
            node_source_key (str): The key of the source node.
            node_source_value (str): The identifier of the source node.
            relation (str): The type of the relationship.
            node_target_key (str): The key of the target node.
            node_target_value (str): The identifier of the target node.

        Returns:
            Any: The result of the operation.
        """
    @abstractmethod
    def query(self, query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Query the graph store.

        Args:
            query (str): The query to be executed.
            parameters (dict[str, Any] | None, optional): The parameters of the query. Defaults to None.

        Returns:
            list[dict[str, Any]]: The result of the query.
        """
    @abstractmethod
    def close(self) -> None:
        """Close the graph data store."""

class GraphDataStore(BaseGraphDataStore, metaclass=abc.ABCMeta):
    """A graph data store interface.

    This class is deprecated and will be removed in a future release. Use BaseGraphDataStore instead.
    """
