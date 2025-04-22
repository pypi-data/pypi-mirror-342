from gllm_datastore.vector_data_store.elasticsearch_vector_data_store import ElasticsearchVectorDataStore as ElasticsearchVectorDataStore

class ElasticsearchDataStore(ElasticsearchVectorDataStore):
    """A vector data store for interacting with Elasticsearch.

    This class is a subclass of ElasticsearchVectorDataStore.
    It is deprecated and will be removed in a future release.
    Use ElasticsearchVectorDataStore instead.
    """
