from _typeshed import Incomplete
from gllm_datastore.cache_data_store.cache_data_store import BaseCacheDataStore as BaseCacheDataStore, CacheMatchingStrategy as CacheMatchingStrategy

class RedisCacheDataStore(BaseCacheDataStore):
    """A cache data store that stores data in Redis.

    The `RedisCacheDataStore` class utilizes Redis to store the cache data.

    Attributes:
        client (StrictRedis): The Redis client.
        retrieval_method (Callable[[str], Any]): The method to retrieve cache data based on the matching strategy.
        fuzzy_distance_ratio (float): The ratio of key length to use as maximum Levenshtein distance
            for fuzzy matching (e.g., 0.05 means 5% of key length). Must be between 0 and 1.
    """
    client: Incomplete
    def __init__(self, host: str, port: int, password: str, db: int = 0, ssl: bool = False, matching_strategy: CacheMatchingStrategy = ..., fuzzy_distance_ratio: float = 0.05) -> None:
        """Initializes a new instance of the RedisCacheDataStore class.

        Args:
            host (str): The host of the Redis server.
            port (int): The port of the Redis server.
            password (str): The password for the Redis server.
            db (int, optional): The database number. Defaults to 0.
            ssl (bool, optional): Whether to use SSL. Defaults to False.
            matching_strategy (CacheMatchingStrategy, optional): The matching strategy to use.
                Defaults to CacheMatchingStrategy.EXACT.
            fuzzy_distance_ratio (float, optional): The ratio of key length to use as maximum Levenshtein distance
                for fuzzy matching (e.g., 0.05 means 5% of key length). Must be between 0 and 1. Defaults to 0.05.

        Raises:
            ValueError: If the fuzzy distance ratio is not between 0 and 1.
        """
    def retrieve_all_keys(self) -> list[str]:
        """Retrieves all keys from the storage.

        This method filters out and deletes any expired keys before returning the list.

        Returns:
            list[str]: A list of all keys in the storage.
        """
    def delete(self, key: str | list[str]) -> None:
        """Deletes cache data from the storage.

        Args:
            key (str | list[str]): The key(s) to delete the cache data.
        """
    def clear(self) -> None:
        """Clears all cache data from the storage."""
