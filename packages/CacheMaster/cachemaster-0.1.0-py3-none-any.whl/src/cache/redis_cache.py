import itertools
import json
import logging
import pickle
import re

import redis

from src.cache.base_cache import DEFAULT_TIMEOUT, BaseCache, CacheException

logger = logging.getLogger(__name__)


class RedisSerializer:
    """Handles serialization for Redis cache."""

    def __init__(self, protocol=None, use_json=False):
        self.use_json = use_json
        self.protocol = pickle.HIGHEST_PROTOCOL if protocol is None else protocol

    def dumps(self, obj):
        """Serialize data using JSON or Pickle."""
        return json.dumps(obj).encode() if self.use_json else pickle.dumps(obj, self.protocol)

    def loads(self, data):
        """Deserialize data using JSON or Pickle."""
        try:
            return json.loads(data) if self.use_json else pickle.loads(data)
        except (ValueError, pickle.UnpicklingError):
            return data


class RedisCacheClient:
    def __init__(self, servers, serializer=None, pool_class=None, parser_class=None, **options):
        """
        Initializes Redis connection pools.

        Args:
            servers (list or str): List of Redis server URLs.
            serializer (RedisSerializer): Custom serializer (default: Pickle).
            pool_class: Redis connection pool class.
            parser_class: Redis parser class.
            **options: Additional options for Redis connection.
        """
        if isinstance(servers, str):
            self._servers = re.split("[;,]", servers)
        else:
            self._servers = servers

        if not self._servers:
            raise CacheException("No Redis servers provided.")

        self._pools = {}
        self._round_robin = itertools.cycle(range(len(self._servers)))  # Round-robin iterator
        self._serializer = serializer or RedisSerializer()
        self._pool_class = pool_class or redis.ConnectionPool
        self._pool_options = {"parser_class": parser_class or redis.connection.DefaultParser, **options}
        self._clients = {}

        logger.info(f"Redis connection initialized with servers: {self._servers}")

    def _get_connection_pool_index(self, write: bool) -> int:
        """
        Selects a Redis connection pool index.

        - If `write=True`, always use the primary server (index 0).
        - Otherwise, use a round-robin approach to balance read requests.
        """
        if write or len(self._servers) == 1:
            return 0  # Always use the primary server for writings
        return next(self._round_robin)  # Round-robin selection for reads

    def _get_connection_pool(self, write: bool):
        """
        Retrieves a Redis connection pool.

        Ensures that the connection pool is initialized before returning.
        """
        index = self._get_connection_pool_index(write)
        if index not in self._pools:
            try:
                self._pools[index] = self._pool_class.from_url(self._servers[index], **self._pool_options)
            except Exception as e:
                logger.error(f"Failed to create Redis connection pool for {self._servers[index]}: {e}")
                raise CacheException(f"Redis connection pool error: {e!s}")
        return self._pools[index]

    def get_client(self, *, write=False):
        """
        Returns a Redis client.

        - Uses the primary server for writings.
        - Distributes reads across available replicas.
        - Handles connection errors gracefully.
        """
        try:
            key = f"write_{write}"
            if key not in self._clients:
                pool = self._get_connection_pool(write)
                if not pool:
                    raise CacheException("No available Redis connection pool.")
                self._clients[key] = redis.Redis(connection_pool=pool)
            return self._clients[key]
        except Exception as e:
            logger.error(f"Failed to get Redis client: {e!s}")
            raise CacheException("Redis connection failed.")

    def add(self, key, value, timeout):
        """Add a value to Redis only if the key does not exist."""
        client = self.get_client(write=True)
        value = self._serializer.dumps(value)

        if timeout == 0:
            return bool(client.set(key, value, nx=True)) and client.delete(key)
        return bool(client.set(key, value, ex=timeout, nx=True))

    def get(self, key, default=None):
        """Retrieve a value from Redis."""
        client = self.get_client()
        value = client.get(key)
        return default if value is None else self._serializer.loads(value)

    def set(self, key, value, timeout):
        """Store a value in Redis with an optional timeout."""
        client = self.get_client(write=True)
        value = self._serializer.dumps(value)

        if timeout == 0:
            client.delete(key)
        else:
            client.set(key, value, ex=timeout)

    def touch(self, key, timeout):
        """Update the expiration time of a key."""
        client = self.get_client(write=True)
        if timeout is None:
            return bool(client.persist(key))
        return bool(client.expire(key, timeout))

    def delete(self, key):
        """Remove a key from Redis."""
        client = self.get_client(write=True)
        return bool(client.delete(key))

    def get_many(self, keys):
        """Retrieve multiple keys at once from Redis."""
        client = self.get_client()
        ret = client.mget(keys)
        return {k: self._serializer.loads(v) for k, v in zip(keys, ret) if v is not None}

    def has_key(self, key):
        """Check if a key exists in Redis."""
        client = self.get_client()
        return bool(client.exists(key))

    def incr(self, key, delta=1):
        """Increment a key's value by a given delta."""
        client = self.get_client()
        if not client.exists(key):
            raise CacheException(f"Key '{key}' not found.")
        return client.incr(key, delta)

    def set_many(self, data, timeout):
        """Store multiple key-value pairs in Redis."""
        client = self.get_client(write=True)
        pipeline = client.pipeline()
        pipeline.mset({k: self._serializer.dumps(v) for k, v in data.items()})

        if timeout is not None:
            for key in data:
                pipeline.expire(key, timeout)
        pipeline.execute()

    def delete_many(self, keys):
        """Delete multiple keys from Redis."""
        client = self.get_client(write=True)
        client.delete(*keys)

    def close(self):
        """Close all Redis connection pools."""
        for pool in self._pools.values():
            pool.disconnect()
        self._pools.clear()
        logger.info("Redis connections closed.")

    def clear(self):
        """Clears all keys in Redis."""
        client = self.get_client(write=True)
        client.flushdb()
        logger.warning("Redis database cleared!")


class RedisCache(BaseCache):
    def __init__(self, server, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(server, str):
            self._servers = re.split("[;,]", server)
        else:
            self._servers = server

        self._class = RedisCacheClient
        self._options = kwargs.get("OPTIONS", {})
        self._client = None

    def start(self):
        self._cache()

    def _cache(self):
        if self._client is None:
            self._client = self._class(self._servers, **self._options)
        return self._client

    def get_backend_timeout(self, timeout=DEFAULT_TIMEOUT):
        if timeout == DEFAULT_TIMEOUT:
            timeout = self.default_timeout
        return None if timeout is None else max(0, int(timeout))

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache().add(key, value, self.get_backend_timeout(timeout))

    def get(self, key, default=None, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache().get(key, default)

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_and_validate_key(key, version=version)
        self._cache().set(key, value, self.get_backend_timeout(timeout))

    def touch(self, key, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache().touch(key, self.get_backend_timeout(timeout))

    def delete(self, key, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache().delete(key)

    def get_many(self, keys, version=None):
        key_map = {self.make_and_validate_key(key, version=version): key for key in keys}
        ret = self._cache().get_many(key_map.keys())
        return {key_map[k]: v for k, v in ret.items()}

    def has_key(self, key, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache().has_key(key)

    def incr(self, key, delta=1, version=None):
        key = self.make_and_validate_key(key, version=version)
        return self._cache().incr(key, delta)

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        safe_data = {self.make_and_validate_key(k, version=version): v for k, v in data.items()}
        self._cache().set_many(safe_data, self.get_backend_timeout(timeout))
        return []

    def delete_many(self, keys, version=None):
        safe_keys = [self.make_and_validate_key(k, version=version) for k in keys]
        self._cache().delete_many(safe_keys)

    def clear(self):
        return self._cache().clear()

    def close(self):
        """Ensure the connection pool is closed."""
        if self._client:
            self._client.close()
            self._client = None

    @property
    def client(self):
        return self._cache().get_client()
