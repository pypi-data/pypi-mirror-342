from _typeshed import Incomplete
from gllm_datastore.cache_data_store.cache_data_store import BaseCacheDataStore as BaseCacheDataStore, CacheMatchingStrategy as CacheMatchingStrategy

class FileSystemCacheDataStore(BaseCacheDataStore):
    '''A cache data store that stores data in the file system.

    The `FileSystemCacheDataStore` class utilizes the file system to store cache data.

    Attributes:
        cache_dir (str): The directory to store the cache data.
        cache_version (str): The version of the cache data.
        current_version_dir (str): The directory to store the cache data for the current version.
        serialization_format (str): The serialization format to use for storing the cache data.
            The supported serialization formats are "json" and "pickle".
        compression_extension (str): The extension to use for the compression of the cache data.
        matching_strategy (CacheMatchingStrategy): The matching strategy to use.
        logger (Logger): The logger to use for logging.
        retrieval_method (Callable[[str], Any]): The method to retrieve cache data based on the matching strategy.
        fuzzy_distance_ratio (float): The ratio of key length to use as maximum Levenshtein distance
            for fuzzy matching (e.g., 0.05 means 5% of key length). Must be between 0 and 1.
    '''
    logger: Incomplete
    cache_dir: Incomplete
    cache_version: Incomplete
    current_version_dir: Incomplete
    serialization_format: Incomplete
    compression_extension: Incomplete
    def __init__(self, cache_dir: str, cache_version: str = '1.0.0', serialization_format: str = 'json', matching_strategy: CacheMatchingStrategy = ..., fuzzy_distance_ratio: float = 0.05) -> None:
        '''Initializes a new instance of the FileSystemCacheDataStore class.

        Args:
            cache_dir (str): The directory to store the cache data.
            cache_version (str, optional): The version of the cache data. Defaults to "1.0.0".
            serialization_format (str, optional): The serialization format to use for storing the cache data.
                The supported serialization formats are "json" and "pickle". Defaults to "json".
            matching_strategy (CacheMatchingStrategy, optional): The matching strategy to use.
                Defaults to CacheMatchingStrategy.EXACT.
            fuzzy_distance_ratio (float, optional): The ratio of key length to use as maximum Levenshtein distance
                for fuzzy matching (e.g., 0.05 means 5% of key length). Must be between 0 and 1. Defaults to 0.05.

        Raises:
            ValueError: If the serialization format is not supported.
        '''
    def retrieve_all_keys(self) -> list[str]:
        """Retrieves all keys from the file system cache data store.

        This method filters out and deletes any expired keys before returning the list.

        Returns:
            list[str]: A list of all keys in the file system cache data store.
        """
    def delete(self, key: str | list[str]) -> None:
        """Deletes cache data from the file system cache data store.

        Args:
            key (str | list[str]): The key(s) to delete the cache data.

        Raises:
            Exception: If there's exist cache file that cannot be deleted.
        """
    def clear(self) -> None:
        """Clears all cache data from the file system cache data store cahe directory."""
