from _typeshed import Incomplete
from gllm_datastore.graph_data_store.llama_index_graph_rag_data_store import LlamaIndexGraphRAGDataStore as LlamaIndexGraphRAGDataStore
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from typing import Any

class LlamaIndexNeo4jGraphRAGDataStore(LlamaIndexGraphRAGDataStore, Neo4jPropertyGraphStore):
    """Graph RAG data store for Neo4j. This class extends the Neo4jPropertyGraphStore class from LlamaIndex.

    Attributes:
        neo4j_version_tuple (tuple[int, ...]): The Neo4j version tuple.
    """
    neo4j_version_tuple: Incomplete
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the LlamaIndexNeo4jGraphRAGDataStore.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
    def delete_by_document_id(self, document_id: str, **kwargs: Any) -> None:
        """Delete nodes and edges by document ID.

        Args:
            document_id (str): The document ID.
            **kwargs (Any): Additional keyword arguments.
        """
