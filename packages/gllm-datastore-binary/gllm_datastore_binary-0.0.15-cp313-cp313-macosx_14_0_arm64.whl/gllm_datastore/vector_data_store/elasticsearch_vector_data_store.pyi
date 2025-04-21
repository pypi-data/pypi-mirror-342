from _typeshed import Incomplete
from gllm_core.schema import Chunk
from gllm_datastore.constants import DEFAULT_REQUEST_TIMEOUT as DEFAULT_REQUEST_TIMEOUT, DEFAULT_TOP_K as DEFAULT_TOP_K
from gllm_datastore.utils.converter import from_langchain as from_langchain, to_langchain as to_langchain
from gllm_datastore.vector_data_store.vector_data_store import BaseVectorDataStore as BaseVectorDataStore
from langchain_core.embeddings import Embeddings as Embeddings
from typing import Any

class ElasticsearchVectorDataStore(BaseVectorDataStore):
    """DataStore for interacting with Elasticsearch.

    This class provides methods for executing queries and retrieving documents
    from Elasticsearch. It relies on the LangChain's ElasticsearchStore  for
    vector operations and the underlying Elasticsearch client management.

    Attributes:
        store (ElasticsearchStore): The ElasticsearchStore instance for vector operations.
        index_name (str): The name of the Elasticsearch index.
        logger (Logger): The logger object.
    """
    index_name: Incomplete
    store: Incomplete
    logger: Incomplete
    def __init__(self, index_name: str, embedding: Embeddings | None = None, connection: Any | None = None, url: str | None = None, cloud_id: str | None = None, user: str | None = None, api_key: str | None = None, password: str | None = None, vector_query_field: str = 'vector', query_field: str = 'text', distance_strategy: str | None = None, strategy: Any | None = None, request_timeout: int = ...) -> None:
        '''Initializes an instance of the ElasticsearchVectorDataStore class.

        Args:
            index_name (str): The name of the Elasticsearch index.
            embedding (Embeddings | None, optional): The Embeddings object for vector operations. Defaults to None.
            connection (Any | None, optional): The Elasticsearch connection object. Defaults to None.
            url (str | None, optional): The URL of the Elasticsearch server. Defaults to None.
            cloud_id (str | None, optional): The cloud ID of the Elasticsearch cluster. Defaults to None.
            user (str | None, optional): The username for authentication. Defaults to None.
            api_key (str | None, optional): The API key for authentication. Defaults to None.
            password (str | None, optional): The password for authentication. Defaults to None.
            vector_query_field (str, optional): The field name for vector queries. Defaults to "vector".
            query_field (str, optional): The field name for text queries. Defaults to "text".
            distance_strategy (str | None, optional): The distance strategy for retrieval. Defaults to None.
            strategy (Any | None, optional): The retrieval strategy for retrieval. Defaults to None, in which case
                DenseVectorStrategy() is used.
            request_timeout (int, optional): The request timeout. Defaults to DEFAULT_REQUEST_TIMEOUT.
        '''
    async def query(self, query: str, top_k: int = ..., retrieval_params: dict[str, Any] | None = None) -> list[Chunk]:
        """Queries the Elasticsearch data store.

        Args:
            query (str): The query string.
            top_k (int, optional): The number of top results to retrieve. Defaults to DEFAULT_TOP_K.
            retrieval_params (dict[str, Any] | None, optional): Additional retrieval parameters. Defaults to None.

        Returns:
            list[Chunk]: A list of Chunk objects representing the retrieved documents.
        """
    async def query_by_id(self, id_: str | list[str]) -> list[Chunk]:
        """Queries the data store by ID and returns a list of Chunk objects.

        Args:
            id_: The ID of the document to query.

        Returns:
            A list of Chunk objects representing the queried documents.

        Note:
            This method not implement yet. Because the ElasticsearchStore
            still not implement the get_by_ids method yet.
        """
    async def autocomplete(self, query: str, field: str, size: int = 20, fuzzy_tolerance: int = 1, min_prefix_length: int = 3, filter_query: dict[str, Any] | None = None) -> list[str]:
        """Provides suggestions based on a prefix query for a specific field.

        Args:
            query (str): The query string.
            field (str): The field name for autocomplete.
            size (int, optional): The number of suggestions to retrieve. Defaults to 20.
            fuzzy_tolerance (int, optional): The level of fuzziness for suggestions. Defaults to 1.
            min_prefix_length (int, optional): The minimum prefix length to trigger fuzzy matching. Defaults to 3.
            filter_query (dict[str, Any] | None, optional): The filter query. Defaults to None.

        Returns:
            list[str]: A list of suggestions.
        """
    async def autosuggest(self, query: str, search_fields: list[str], autocomplete_field: str, size: int = 20, min_length: int = 3, filter_query: dict[str, Any] | None = None) -> list[str]:
        """Generates suggestions across multiple fields using a multi_match query to broaden the search criteria.

        Args:
            query (str): The query string.
            search_fields (list[str]): The fields to search for.
            autocomplete_field (str): The field name for autocomplete.
            size (int, optional): The number of suggestions to retrieve. Defaults to 20.
            min_length (int, optional): The minimum length of the query. Defaults to 3.
            filter_query (dict[str, Any] | None, optional): The filter query. Defaults to None.

        Returns:
            list[str]: A list of suggestions.
        """
    async def shingles(self, query: str, field: str, size: int = 20, min_length: int = 3, filter_query: dict[str, Any] | None = None) -> list[str]:
        """Searches using shingles for prefix and fuzzy matching.

        Args:
            query (str): The query string.
            field (str): The field name for autocomplete.
            size (int, optional): The number of suggestions to retrieve. Defaults to 20.
            min_length (int, optional): The minimum length of the query. Defaults to 3.
            filter_query (dict[str, Any] | None, optional): The filter query. Defaults to None.

        Returns:
            list[str]: A list of suggestions.
        """
    async def add_chunks(self, chunk: Chunk | list[Chunk], **kwargs: Any) -> list[str]:
        """Adds a chunk or a list of chunks to the data store.

        Args:
            chunk (Chunk | list[Chunk]): The chunk or list of chunks to add.
            kwargs (Any): Additional keyword arguments.

        Returns:
            list[str]: A list of unique identifiers (IDs) assigned to the added chunks.
        """
    async def add_embeddings(self, text_embeddings: list[tuple[str, list[float]]], metadatas: list[dict] | None = None, ids: list[str] | None = None, **kwargs) -> list[str]:
        """Adds text embeddings to the data store.

        Args:
            text_embeddings (list[tuple[str, list[float]]]): Pairs of string and embedding to add to the store.
            metadatas (list[dict], optional): Optional list of metadatas associated with the texts. Defaults to None.
            ids (list[str], optional): Optional list of unique IDs. Defaults to None.
            kwargs (Any): Additional keyword arguments.

        Returns:
            list[str]: A list of unique identifiers (IDs) assigned to the added embeddings.
        """
    async def delete_chunks(self, query: dict[str, Any], **kwargs: Any) -> None:
        '''Deletes a chunk or a list of chunks from the data store.

        Args:
            query (dict[str, Any]): The query to filter the chunks to delete.
                For example, `{"term": {"metadata.id": "doc123"}}`.
            kwargs (Any): Additional keyword arguments.

        Returns:
            None
        '''
