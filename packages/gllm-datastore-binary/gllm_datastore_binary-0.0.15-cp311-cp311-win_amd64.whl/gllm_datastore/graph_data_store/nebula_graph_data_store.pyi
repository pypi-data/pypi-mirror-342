from _typeshed import Incomplete
from gllm_datastore.graph_data_store.graph_data_store import BaseGraphDataStore as BaseGraphDataStore
from nebula3.gclient.net import Session as Session
from typing import Any

class NebulaGraphDataStore(BaseGraphDataStore):
    """Implementation of BaseGraphDataStore for Nebula Graph.

    Attributes:
        connection_pool (ConnectionPool): The connection pool for Nebula Graph.
        space (str): The space name.
        user (str): The username.
        password (str): The password.
        operation_wait_time (int): The timeout in seconds.
    """
    connection_pool: Incomplete
    space: Incomplete
    user: Incomplete
    password: Incomplete
    operation_wait_time: Incomplete
    def __init__(self, url: str, port: int, user: str, password: str, space: str, operation_wait_time: int = 5) -> None:
        """Initialize NebulaGraphDataStore.

        Args:
            url (str): The URL of the graph store.
            port (int): The port of the graph store.
            user (str): The user of the graph store.
            password (str): The password of the graph store.
            space (str): The space name.
            operation_wait_time (int, optional): The operation wait time in seconds. Defaults to 5.
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
    def get_nodes(self, label: str | None = None) -> list[dict[str, Any]]:
        """Get all nodes with optional label filter.

        Args:
            label (str | None, optional): The label of the nodes. Defaults to None.

        Returns:
            list[dict[str, Any]]: The result of the query.
        """
    def get_relationships(self, source_value: str | None = None, relation: str | None = None) -> list[dict[str, Any]]:
        """Get relationships with optional filters.

        Args:
            source_value (str | None, optional): The source vertex identifier. Defaults to None.
            relation (str | None, optional): The relationship type. Defaults to None.

        Returns:
            list[dict[str, Any]]: The result of the query.
        """
