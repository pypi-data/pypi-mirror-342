import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from enum import StrEnum
from gllm_datastore.cache_data_store.utils import generate_key_from_func as generate_key_from_func
from gllm_datastore.utils import convert_ttl_to_seconds as convert_ttl_to_seconds
from typing import Any, Callable, ParamSpec, TypeVar

P = ParamSpec('P')
T = TypeVar('T')

class CacheMatchingStrategy(StrEnum):
    """An enumeration of cache matching strategies.

    Attributes:
        EXACT (str): The cache key must match the query exactly.
        FUZZY (str): The cache key must match the query with fuzzy matching.
    """
    EXACT = 'exact'
    FUZZY = 'fuzzy'

class BaseCacheDataStore(ABC, metaclass=abc.ABCMeta):
    """A base class for cache data store used in Gen AI applications.

    The `BaseCacheDataStore` class provides a framework for storing and retrieving cache data.

    Attributes:
        retrieval_method (Callable[[str], Any]): The method to retrieve cache data based on the matching strategy.
        fuzzy_distance_ratio (float): The ratio of key length to use as maximum Levenshtein distance
            for fuzzy matching (e.g., 0.1 means 10% of key length). Must be between 0 and 1.

    Supported matching strategies:
        1. EXACT
           The cache matches when the key is an exact match.
        2. FUZZY
           The cache matches when the key has a Levenshtein distance of less than or equal to the maximum allowed
           distance. The maximum allowed distance is calculated by multiplying the `fuzzy_distance_ratio` with the key
           length. Since the fuzzy matching heavily depends on the syntactic similarity between the key and the cached
           key, it should only be used when the key is a plain string. Fuzzy matching SHOULD NOT be used when the key
           is a hash / encryption of the input data.
    """
    retrieval_method: Incomplete
    fuzzy_distance_ratio: Incomplete
    def __init__(self, matching_strategy: CacheMatchingStrategy = ..., fuzzy_distance_ratio: float = 0.05) -> None:
        """Initialize a new instance of the `BaseCacheDataStore` class.

        Args:
            matching_strategy (CacheMatchingStrategy, optional): The matching strategy to use.
                Defaults to CacheMatchingStrategy.EXACT.
            fuzzy_distance_ratio (float, optional): The ratio of key length to use as maximum Levenshtein distance
                for fuzzy matching (e.g., 0.05 means 5% of key length). Must be between 0 and 1. Defaults to 0.05.

        Raises:
            ValueError: If the matching strategy is not supported or if fuzzy_distance_ratio is not between 0 and 1.
        """
    def store(self, key: str, value: Any, ttl: int | str | None = None) -> None:
        '''Stores cache data in the storage.

        This method preprocesses the TTL (time-to-live) value to seconds if provided, and then calls the `_store`
        method to store the cache data in the storage.

        Args:
            key (str): The key to store the cache data.
            value (Any): The cache data to store.
            ttl (int | str | None): The time-to-live (TTL) for the cache data. Must either be an integer in seconds
                or a string (e.g. "1h", "1d", "1w", "1y"). If None, the cache data will not expire.
        '''
    def retrieve(self, key: str) -> Any:
        """Retrieves cache data from the storage.

        Args:
            key (str): The key to retrieve the cache data.

        Returns:
            Any: The retrieved cache data.
        """
    @abstractmethod
    def retrieve_all_keys(self) -> list[str]:
        """Retrieves all keys from the storage.

        This method must be implemented by the subclasses to define the logic for retrieving all keys from the storage.

        Returns:
            list[str]: A list of all keys in the storage.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
    @abstractmethod
    def delete(self, key: str | list[str]) -> None:
        """Deletes cache data from the storage.

        This method must be implemented by the subclasses to define the logic for deleting cache data from the storage.

        Args:
            key (str | list[str] | None): The key(s) to delete the cache data.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
    @abstractmethod
    def clear(self) -> None:
        """Clears all cache data from the storage.

        This method must be implemented by the subclasses to define the logic for clearing all cache data from the
        storage.

        Args:
            None

        Raises:
            NotImplementedError: If the method is not implemented.
        """
    def cache(self, key_func: Callable[P, str] | None = None, name: str = '', ttl: int | str | None = None) -> Callable[[Callable[P, T]], Callable[P, T]]:
        '''Decorator for caching function results.

        This decorator caches the results of the decorated function using this cache storage.
        The cache key is generated using the provided key function or a default key generation
        based on the function name and arguments.

        Synchronous and asynchronous functions are supported.

        Args:
            key_func (Callable[P, str] | None, optional): Function to generate cache keys.
                Must accept the same parameters as the decorated function.
            name (str, optional): Name to use in the default key generation if key_func is None.
            ttl (int | str | None, optional): The time-to-live for the cached data. Can be an integer
                in seconds or a string (e.g. "1h", "1d", "1w", "1y"). If None, the cache data will not expire.
                Defaults to None. In this case, the cache will not expire.

        Example:
            ```python
            def get_user_cache_key(user_id: int) -> str:
                return f"user:{user_id}"

            @cache_store.cache(key_func=get_user_cache_key, ttl="1h")
            async def get_user(user_id: int) -> User:
                return await db.get_user(user_id)

            # will use/store cache with key "user:1", expiring after 1 hour
            user1 = await get_user(1)
            ```

        Returns:
            Callable: A decorator function.
        '''
