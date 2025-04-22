from _typeshed import Incomplete
from gllm_datastore.graph_data_store.graph_data_store import BaseGraphDataStore as BaseGraphDataStore
from typing import Any

class Neo4jGraphDataStore(BaseGraphDataStore):
    """Implementation of BaseGraphDataStore for Neo4j.

    Attributes:
        driver (Driver): The Neo4j driver.
    """
    driver: Incomplete
    def __init__(self, uri: str, user: str, password: str) -> None:
        """Initialize Neo4jGraphDataStore.

        Args:
            uri (str): The URI of the graph store.
            user (str): The user of the graph store.
            password (str): The password of the graph store.
        """
    def upsert_node(self, label: str, identifier_key: str, identifier_value: str, properties: dict[str, Any] | None = None) -> Any:
        """Upsert a node in the graph.

        Args:
            label (str): The label of the node.
            identifier_key (str): The key of the identifier.
            identifier_value (str): The value of the identifier.
            properties (dict[str, Any] | None, optional): The properties of the node. Defaults to None.

        Returns:
            Any: The result of the operation.
        """
    def upsert_relationship(self, node_source_key: str, node_source_value: str, relation: str, node_target_key: str, node_target_value: str, properties: dict[str, Any] | None = None) -> Any:
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
    def delete_node(self, label: str, identifier_key: str, identifier_value: str) -> Any:
        """Delete a node from the graph.

        Args:
            label (str): The label of the node.
            identifier_key (str): The key of the identifier.
            identifier_value (str): The identifier of the node.

        Returns:
            Any: The result of the operation.
        """
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
    def query(self, query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Query the graph store.

        Args:
            query (str): The query to be executed.
            parameters (dict[str, Any] | None, optional): The parameters of the query. Defaults to None.

        Returns:
            list[dict[str, Any]]: The result of the query.
        """
    def close(self) -> None:
        """Close the graph data store."""
