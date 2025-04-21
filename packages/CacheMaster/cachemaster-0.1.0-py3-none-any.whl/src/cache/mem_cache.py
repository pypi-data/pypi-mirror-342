from collections import OrderedDict
import pickle
from threading import Lock
import time
from typing import Any, Dict, Optional, Union

from src.cache.base_cache import DEFAULT_TIMEOUT, BaseCache, CacheException

# Global in-memory store of cache data. Keyed by name, to provide multiple named local memory caches.
_caches: Dict[str, OrderedDict] = {}
_expire_info: Dict[str, Dict[str, float]] = {}
_locks: Dict[str, Lock] = {}


class LocMemCache(BaseCache):
    """
    A thread-safe in-memory cache backend.

    Supports:
        - Thread-safe access via Lock.
        - Automatic expiration handling.
        - Optional memory size limiting.
    """

    pickle_protocol = pickle.HIGHEST_PROTOCOL

    def __init__(self, name: str = "", max_size: Optional[int] = None, *args, **kwargs):
        """
        Args:
            name (str): Name of the cache.
            max_size (Optional[int]): Maximum memory size (bytes) before eviction.
        """
        super().__init__(*args, **kwargs)
        self._cache = _caches.setdefault(name, OrderedDict())
        self._expire_info = _expire_info.setdefault(name, {})
        self._lock = _locks.setdefault(name, Lock())
        self.max_size = max_size  # New: Max size for cache eviction

    def add(
        self, key: str, value: Any, timeout: Union[int, object] = DEFAULT_TIMEOUT, version: Optional[int] = None
    ) -> bool:
        key = self.make_key(key, version=version)
        self.validate_key(key)
        pickled_value = pickle.dumps(value, self.pickle_protocol)
        with self._lock:
            if self._has_expired(key):
                self._set(key, pickled_value, timeout)
                return True
        return False

    def get(self, key: str, default: Any = None, version: Optional[int] = None) -> Any:
        key = self.make_key(key, version=version)
        self.validate_key(key)
        with self._lock:
            if self._has_expired(key):
                self._delete(key)
                return default
            pickled_value = self._cache[key]
            self._cache.move_to_end(key, last=False)
        return pickle.loads(pickled_value)

    def set(
        self, key: str, value: Any, timeout: Union[int, object] = DEFAULT_TIMEOUT, version: Optional[int] = None
    ) -> None:
        """
        Store a key in the cache with an expiration timeout.

        Args:
            key (str): Cache key.
            value (Any): Value to store.
            timeout (int | object): Expiration time (default is cache-wide setting).
            version (Optional[int]): Versioning support.
        """
        key = self.make_key(key, version=version)
        self.validate_key(key)
        pickled_value = pickle.dumps(value, self.pickle_protocol)

        with self._lock:
            # Enforce max size if defined
            while self.max_size and sum(len(v) for v in self._cache.values()) + len(pickled_value) > self.max_size:
                key_to_remove, _ = self._cache.popitem(last=False)
                del self._expire_info[key_to_remove]

            self._set(key, pickled_value, timeout)

    def touch(self, key: str, timeout: Union[int, object] = DEFAULT_TIMEOUT, version: Optional[int] = None) -> bool:
        key = self.make_key(key, version=version)
        self.validate_key(key)
        with self._lock:
            if self._has_expired(key):
                return False
            self._expire_info[key] = self.get_backend_timeout(timeout)  # type: ignore[assignment]
            return True

    def incr(self, key: str, delta: int = 1, version: Optional[int] = None) -> int | float:
        """
        Increment a cache key's value.

        Args:
            key (str): Cache key.
            delta (int): Value to increment.
            version (Optional[int]): Versioning support.

        Returns:
            int: New incremented value.

        Raises:
            CacheException: If key is missing or non-numeric.
        """
        key = self.make_key(key, version=version)
        self.validate_key(key)

        with self._lock:
            if self._has_expired(key):
                self._delete(key)
                raise CacheException(f"Key '{key}' not found for increment operation.")

            pickled_value = self._cache[key]
            value = pickle.loads(pickled_value)

            if not isinstance(value, (int, float)):
                raise CacheException(f"Key '{key}' contains non-numeric value: {value}")

            new_value = value + delta
            self._cache[key] = pickle.dumps(new_value, self.pickle_protocol)
            self._cache.move_to_end(key, last=False)

        return new_value

    def decr(self, key: str, delta: int = 1, version: Optional[int] = None) -> int:
        """Decrement a cache key's value."""
        return self.incr(key, -delta, version=version)  # type: ignore[return-value]

    def has_key(self, key: str, version: Optional[int] = None) -> bool:
        key = self.make_key(key, version=version)
        self.validate_key(key)
        with self._lock:
            if self._has_expired(key):
                self._delete(key)
                return False
            return True

    def delete(self, key: str, version: Optional[int] = None) -> bool:
        """Remove a key from the cache."""
        key = self.make_key(key, version=version)
        self.validate_key(key)

        with self._lock:
            return self._delete(key) if key in self._cache else False

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self._expire_info.clear()

    def _has_expired(self, key: str) -> bool:
        """Check if a key has expired."""
        exp = self._expire_info.get(key, None)
        return exp is not None and exp <= time.time()

    def _set(self, key: str, value: Any, timeout: Union[int, object] = DEFAULT_TIMEOUT) -> None:
        if len(self._cache) >= self._max_entries:
            self._cull()
        self._cache[key] = value
        self._cache.move_to_end(key, last=False)
        backend_timeout = self.get_backend_timeout(timeout)
        if backend_timeout is None:
            raise CacheException("Backend timeout cannot be None.")
        self._expire_info[key] = self.get_backend_timeout(timeout)  # type: ignore[assignment]

    def _cull(self) -> None:
        """Remove old items from the cache when it exceeds max entries."""
        if self._cull_frequency == 0:
            self._cache.clear()
            self._expire_info.clear()
            return

        # Remove expired keys first
        expired_keys = [key for key in self._cache.keys() if self._has_expired(key)]
        for key in expired_keys:
            self._delete(key)

        # If still over max entries, remove the oldest keys
        while len(self._cache) > self._max_entries:
            key, _ = self._cache.popitem(last=False)
            del self._expire_info[key]

    def _delete(self, key: str) -> bool:
        try:
            del self._cache[key]
            del self._expire_info[key]
        except KeyError:
            return False
        return True
