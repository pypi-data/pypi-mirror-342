from enum import Enum
import inspect
import logging
from typing import Any, Callable, Dict, List, Literal, Optional

from src.cache.base_cache import CacheException
from src.cache.mem_cache import LocMemCache
from src.cache.redis_cache import RedisCache

logger = logging.getLogger(__name__)


class CacheType(Enum):
    LOCAL_CACHE = "LOCAL"
    REDIS_CACHE = "REDIS"


class CoreCache:
    app_name: str
    cache_type: CacheType

    def __init__(
        self, app_name: str, cache_type: Literal[CacheType.LOCAL_CACHE, CacheType.REDIS_CACHE], *args, **kwargs
    ) -> None:
        self.app_name = app_name
        self.cache_type = CacheType(cache_type)

        self.local_cache = None
        self.redis_cache = None

        if self.cache_type == CacheType.LOCAL_CACHE:
            self.local_cache = LocMemCache(*args, **kwargs)
        elif self.cache_type == CacheType.REDIS_CACHE:
            redis_url = kwargs.get("redis_url")
            if not redis_url:
                logger.warning("Redis URL is missing. Using default Redis URL:- redis://localhost:6379/0.")
            self.redis_cache = RedisCache("redis://localhost:6379/0", *args, **kwargs)

    def decorator_cache(self, namespace: str, timeout: int, keys: Optional[List[str]] = None) -> Callable:
        """
        A decorator to cache function results.

        Args:
            namespace (str): Cache namespace.
            timeout (int): Cache expiration time.
            keys (List[str], optional): Keys to identify cache. Defaults to function arguments.

        Returns:
            Callable: Wrapped function.
        """

        def cache_decorator(func: Callable) -> Callable:
            if keys is None:
                keys_from_func = list(inspect.signature(func).parameters.keys())
            else:
                keys_from_func = keys

            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await self._handle_cache(func, args, kwargs, namespace, timeout, keys_from_func)

            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                return self._handle_cache(func, args, kwargs, namespace, timeout, keys_from_func)

            return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

        return cache_decorator

    async def _handle_cache(
        self, func: Callable, args: Any, kwargs: Any, namespace: str, timeout: int, keys: List[str]
    ) -> Any:
        """Handles caching logic for both sync and async functions."""

        all_args = self._get_all_args(func, args, kwargs)

        if not set(keys).issubset(all_args):
            raise CacheException("Invalid cache keys provided in decorator.")

        required_key = self._generate_cache_key(namespace, func.__name__, keys, all_args)

        cache_response = self._get_from_cache(required_key)
        if cache_response is not None:
            logger.info(f"Cache hit: {required_key}")
            return cache_response

        logger.info(f"Cache miss: {required_key}. Executing function.")
        response = await func(*args, **kwargs) if inspect.iscoroutinefunction(func) else func(*args, **kwargs)

        self._set_in_cache(required_key, response, timeout)
        return response

    def _get_all_args(self, func: Callable, args: Any, kwargs: Any) -> Dict[str, Any]:
        args_name = inspect.getfullargspec(func)[0]
        args_dict = dict(zip(args_name, args))
        return {**args_dict, **kwargs}

    def _generate_cache_key(self, namespace: str, func_name: str, keys: List[str], all_args: Dict[str, Any]) -> str:
        suffix = "".join(f".{key}.{all_args[key]}" for key in keys)
        return f"{self.app_name}.{namespace}.{func_name}{suffix}"

    def _get_from_cache(self, key: str) -> Any:
        """Retrieve value from the cache."""
        cache = self.local_cache if self.cache_type == CacheType.LOCAL_CACHE else self.redis_cache
        if not cache:
            logger.warning(f"Cache backend `{self.cache_type}` is not initialized.")
            return None
        return cache.get(key)

    def _set_in_cache(self, key: str, value: Any, timeout: int) -> None:
        """Set value in the cache."""
        cache = self.local_cache if self.cache_type == CacheType.LOCAL_CACHE else self.redis_cache
        if not cache:
            logger.warning(f"Cache backend `{self.cache_type}` is not initialized.")
            return
        cache.set(key, value, timeout)
