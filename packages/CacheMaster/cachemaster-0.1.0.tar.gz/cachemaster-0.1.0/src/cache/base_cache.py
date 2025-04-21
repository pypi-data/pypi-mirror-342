import logging
import time
from typing import Callable, Dict, List, Optional, Union


class CacheException(Exception):
    """Base exception for cache errors."""

    pass


class CacheKeyError(CacheException):
    """Exception for invalid cache keys."""

    pass


# Custom exceptions and warnings
class CacheKeyWarning(RuntimeWarning):
    pass


class InvalidCacheKey(ValueError):
    pass


# Constants
DEFAULT_TIMEOUT = object()
MEMCACHE_MAX_KEY_LENGTH = 250


# Utility functions
def memcache_key_warnings(key: str):
    if len(key) > MEMCACHE_MAX_KEY_LENGTH:
        yield f"Cache key will cause errors if used with memcached: {key!r} (longer than {MEMCACHE_MAX_KEY_LENGTH})"
    if any(ord(char) < 33 or ord(char) == 127 for char in key):
        yield f"Cache key contains characters that will cause errors if used with memcached: {key!r}"


def default_key_func(key: str, key_prefix: str, version: int) -> str:
    """Default function to generate keys."""
    return f"{key_prefix}:{version}:{key}"


def get_key_func(key_func: Optional[Callable]) -> Callable:
    """Decide which key function to use. Default to `default_key_func`."""
    return key_func if callable(key_func) else default_key_func


class BaseCache:
    _missing_key = object()

    def __init__(self, *args, **kwargs):
        self.default_timeout = self._parse_timeout(kwargs)
        self._max_entries = self._parse_max_entries(kwargs)
        self._cull_frequency = self._parse_cull_frequency(kwargs)
        self.key_prefix = kwargs.get("KEY_PREFIX", "")
        self.version = kwargs.get("VERSION", 1)
        self.key_func = get_key_func(kwargs.get("KEY_FUNCTION"))

    def _parse_timeout(self, kwargs: Dict) -> int:
        timeout = kwargs.get("timeout", kwargs.get("TIMEOUT", 300))
        return self._to_int(timeout, default=300)

    def _parse_max_entries(self, kwargs: Dict) -> int:
        options = kwargs.get("OPTIONS", {})
        max_entries = kwargs.get("max_entries", options.get("MAX_ENTRIES", 300))
        return self._to_int(max_entries, default=300)

    def _parse_cull_frequency(self, kwargs: Dict) -> int:
        options = kwargs.get("OPTIONS", {})
        cull_frequency = kwargs.get("cull_frequency", options.get("CULL_FREQUENCY", 3))
        return self._to_int(cull_frequency, default=3)

    def _to_int(self, value, default: int) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def get_backend_timeout(self, timeout=DEFAULT_TIMEOUT) -> Optional[float]:
        """
        Return the timeout value in absolute terms.

        Args:
            timeout: The timeout value. If None, uses the default.

        Returns:
            A float representing the absolute expiration time, or None if no expiration.
        """
        if timeout is DEFAULT_TIMEOUT:
            timeout = self.default_timeout
        if timeout is None:
            return -1  # Indicates no expiration
        return time.time() + max(0, timeout)  # Ensure timeout is always positive

    def make_key(self, key: str, version: Optional[int] = None) -> str:
        """
        Construct the key used by all other methods. By default, use the key_func to generate a key (which, by default,
        prepends the `key_prefix' and 'version'). A different key function can be provided at the time of cache
        construction; alternatively, you can subclass the cache backend to provide custom key making behavior.
        Args:
            key: Key to be used for generating the cache key.
            version: An optional version to add to the cache key.

        Returns: The final cache key.

        """
        version = version or self.version
        logging.debug(f"Generated cache key: {key}")
        return self.key_func(key, self.key_prefix, version)

    def make_and_validate_key(self, key: str, version: Optional[int] = None) -> str:
        """Helper to make and validate keys."""
        key = self.make_key(key, version=version)
        self.validate_key(key)
        return key

    def validate_key(self, key: str, auto_truncate: bool = True):
        """
        Validate the cache key and apply necessary transformations.

        Args:
            key (str): The key to validate.
            auto_truncate (bool): If True, truncates keys that exceed max length.

        Raises:
            CacheKeyError: If the key contains invalid characters.
        """
        if auto_truncate and len(key) > MEMCACHE_MAX_KEY_LENGTH:
            key = key[:MEMCACHE_MAX_KEY_LENGTH]

        for warning in memcache_key_warnings(key):
            raise CacheKeyError(warning)

    def add(self, key: str, value, timeout=DEFAULT_TIMEOUT, version: Optional[int] = None) -> bool:
        """Set a value in the cache if the key does not already exist."""
        raise NotImplementedError("subclasses of BaseCache must provide an add() method")

    def get(self, key: str, default=None, version: Optional[int] = None):
        """Fetch a given key from the cache."""
        raise NotImplementedError("subclasses of BaseCache must provide a get() method")

    def set(self, key: str, value, timeout=DEFAULT_TIMEOUT, version: Optional[int] = None):
        """Set a value in the cache."""
        raise NotImplementedError("subclasses of BaseCache must provide a set() method")

    def touch(self, key: str, timeout=DEFAULT_TIMEOUT, version: Optional[int] = None) -> bool:
        """Update the key's expiry time using timeout."""
        raise NotImplementedError("subclasses of BaseCache must provide a touch() method")

    def delete(self, key: str, version: Optional[int] = None) -> bool:
        """Delete a key from the cache and return whether it succeeded."""
        raise NotImplementedError("subclasses of BaseCache must provide a delete() method")

    def get_many(self, keys: List[str], version: Optional[int] = None) -> Dict[str, Union[str, object]]:
        """Fetch a bunch of keys from the cache."""
        return {
            k: val for k in keys if (val := self.get(k, self._missing_key, version=version)) is not self._missing_key
        }

    def get_or_set(self, key: str, default, timeout=DEFAULT_TIMEOUT, version: Optional[int] = None):
        """Fetch or set a key in the cache."""
        val = self.get(key, self._missing_key, version=version)
        if val is self._missing_key:
            if callable(default):
                default = default()
            self.add(key, default, timeout=timeout, version=version)
            return self.get(key, default, version=version)
        return val

    def has_key(self, key: str, version: Optional[int] = None) -> bool:
        """Return True if the key is in the cache and has not expired."""
        return self.get(key, self._missing_key, version=version) is not self._missing_key

    def incr(self, key: str, delta: int = 1, version: Optional[int] = None) -> int | float:
        """
        Increment a cache key's value.

        Args:
            key (str): The cache key.
            delta (int): The increment value.

        Returns:
            int: The new value after increment.

        Raises:
            CacheException: If the key does not exist.
        """
        value = self.get(key, self._missing_key, version=version)
        if value is self._missing_key:
            raise CacheException(f"Key '{key}' not found for increment operation.")

        if not isinstance(value, (int, float)):
            raise CacheException(f"Key '{key}' contains non-numeric value: {value}")

        new_value = value + delta
        self.set(key, new_value, version=version)
        return new_value

    def decr(self, key: str, delta: int = 1, version: Optional[int] = None) -> int | float:
        """
        Decrement a cache key's value.
        """
        return self.incr(key, -delta, version=version)

    def __contains__(self, key: str) -> bool:
        """Return True if the key is in the cache and has not expired."""
        return self.has_key(key)

    def set_many(self, data: Dict[str, str], timeout=DEFAULT_TIMEOUT, version: Optional[int] = None) -> List[str]:
        """Set a bunch of values in the cache at once."""
        failed_keys = []
        for key, value in data.items():
            try:
                self.set(key, value, timeout=timeout, version=version)
            except Exception:
                failed_keys.append(key)
        return failed_keys

    def delete_many(self, keys: List[str], version: Optional[int] = None):
        """Delete a bunch of values in the cache at once."""
        for key in keys:
            self.delete(key, version=version)

    def clear(self):
        """
        Remove all values from the cache.

        Raises:
            NotImplementedError: Should be implemented by subclasses.
        """
        raise NotImplementedError(
            "The 'clear' method must be implemented in the subclass (e.g., RedisCache, MemCache)."
        )

    def incr_version(self, key: str, delta: int = 1, version: Optional[int] = None) -> int:
        """Add delta to the cache version for the supplied key."""
        version = version or self.version
        value = self.get(key, self._missing_key, version=version)
        if value is self._missing_key:
            raise ValueError(f"Key '{key}' not found")
        new_version = version + delta
        self.set(key, value, version=new_version)
        self.delete(key, version=version)
        return new_version

    def decr_version(self, key: str, delta: int = 1, version: Optional[int] = None) -> int:
        """Subtract delta from the cache version for the supplied key."""
        return self.incr_version(key, -delta, version=version)

    def close(self, **kwargs):
        """Close the cache connection."""
        pass
