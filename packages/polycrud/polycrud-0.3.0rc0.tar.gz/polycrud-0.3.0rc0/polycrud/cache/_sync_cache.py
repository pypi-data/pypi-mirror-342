from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

from polycrud import exceptions
from polycrud.connectors.pyredis import RedisConnector
from polycrud.entity import ModelEntity
from polycrud.utils import helper

from ._utils import QueryType, _get_query_type, _get_tags

F = TypeVar("F", bound=Callable[..., Any])

_logger = logging.getLogger(__name__)
ModelT = TypeVar("ModelT", bound=ModelEntity)


class _Settings:
    redis_cache: RedisCache


def setup(redis_connector: RedisConnector, ttl: int = 3600 * 4, prefix: str | None = None) -> None:
    if hasattr(_Settings, "redis_cache"):
        raise RuntimeError("Redis cache is already set up.")
    _Settings.redis_cache = RedisCache(redis_connector=redis_connector, ttl=ttl, prefix=prefix)


def cache() -> Callable[[F], F]:
    def decorator(fn: F) -> F:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # If no cache is set up, just call the function
            if not hasattr(_Settings, "redis_cache") or kwargs.get("_use_cache"):
                return fn(*args, **kwargs)

            # Determine the class name and model class from the arguments
            fn_name = fn.__name__
            cls_name = args[0].__class__.__name__
            ttl = kwargs.get("_cache_ttl", None)
            model_class = (
                args[1]
                if len(args) > 1 and isinstance(args[1], type)
                else args[1].__class__
                if len(args) > 1 and isinstance(args[1], ModelEntity)
                else args[1][0].__class__
                if len(args) > 1 and isinstance(args[1], list)
                else kwargs.get("collection")
                or (kwargs["obj"].__class__ if "obj" in kwargs else None)
                or (kwargs["objs"][0].__class__ if "objs" in kwargs else None)
            )
            if model_class is None:
                raise TypeError("Collection class not found in arguments.")

            # coll_name = coll_cls.__name__
            query_type = _get_query_type(fn_name)

            if not hasattr(_Settings, "redis_cache"):
                return fn(*args, **kwargs)

            redis_cache = _Settings.redis_cache
            key_hash = helper.deep_container_fingerprint([cls_name, model_class.__name__, kwargs])
            cache_key = f"{cls_name}:{model_class.__name__}:{fn_name}:{key_hash}"

            # Handle mutation operations
            if query_type in {
                QueryType.DeleteOne,
                QueryType.UpdateOne,
                QueryType.DeleteMany,
                QueryType.InsertMany,
                QueryType.InsertOne,
            }:
                obj_ids = []

                if query_type == QueryType.DeleteOne:
                    obj_ids = [kwargs.get("id")]
                elif query_type == QueryType.UpdateOne:
                    obj = kwargs.get("obj") or args[1]
                    obj_ids = [getattr(obj, "id", None)]
                elif query_type == QueryType.DeleteMany:
                    obj_ids = kwargs.get("ids", [])

                tags = _get_tags(cls_name, model_class.__name__)
                tags += [f"{cls_name}:{model_class.__name__}:{oid}" for oid in obj_ids if oid]
                redis_cache.invalidate_tags(tags)

                return fn(*args, **kwargs)

            # Handle read operations
            if cached := redis_cache.get(cache_key, model_class):
                _logger.debug(f"Cache hit: {cache_key}")
                return cached

            _logger.debug(f"Cache miss: {cache_key}")
            result = fn(*args, **kwargs)

            # Determine tags based on query type
            if result is None:
                tags = [f"{cls_name}:{model_class.__name__}"]
            else:
                tags = {
                    QueryType.FindOne: [f"{cls_name}:{model_class.__name__}:{getattr(result, 'id', '')}"],
                    QueryType.FindMany: [f"{cls_name}:{model_class.__name__}"],
                }.get(query_type, [cls_name])  # type: ignore

            redis_cache.set(cache_key, result, ttl=ttl, tags=tags)
            return result

        return cast(F, wrapper)

    return decorator


class RedisCache:
    def __init__(self, redis_connector: RedisConnector, ttl: int = 3600 * 4, prefix: str | None = "polycrud") -> None:
        self.ttl = ttl
        self.prefix = prefix
        self.redis_connector = redis_connector
        self.redis_connector.connect()
        try:
            self.redis_connector.connect()
            if not self.redis_connector.health_check():
                self.redis_connector.connect()
        except Exception as e:
            _logger.error(f"Failed to initialize Redis connection: {str(e)}")
            raise exceptions.RedisConnectionError(f"Could not connect to Redis: {str(e)}") from e

    def get(self, key: str, model_cls: type[ModelT]) -> ModelT | None:
        try:
            return self.redis_connector.get_object(model_cls, key=self._format_key(key))
        except Exception as e:
            _logger.warning(f"Redis get failed for key={key}: {e}")
            self._handle_exception(e, "get", key)
            return None

    def set(self, key: str, value: Any, ttl: int | None = None, tags: list[str] | None = None) -> None:
        try:
            full_key = self._format_key(key)
            self.redis_connector.set_object(full_key, value, ttl or self.ttl)
            if tags:
                self._add_tags(full_key, tags)
        except Exception as e:
            _logger.warning(f"Redis set failed for key={key}: {e}")
            self._handle_exception(e, "set", key)

    def _add_tags(self, key: str, tags: list[str]) -> None:
        if not self.redis_connector.client:
            return
        try:
            pipe = self.redis_connector.client.pipeline()
            for tag in tags:
                pipe.sadd(f"tag:{tag}", key)
            pipe.execute()
        except Exception as e:
            _logger.warning(f"Redis add_tags failed for key={key}: {e}")
            self._handle_exception(e, "add_tags", key)

    def invalidate_tags(self, tags: list[str]) -> None:
        if not tags or not self.redis_connector.client:
            return
        try:
            pipe = self.redis_connector.client.pipeline()
            all_keys: set[str] = {
                key
                for tag in tags
                for key in self.redis_connector.client.smembers(f"tag:{tag}")  # type: ignore
            }
            if all_keys:
                pipe.delete(*all_keys)
            pipe.delete(*[f"tag:{tag}" for tag in tags])
            pipe.execute()
        except Exception as e:
            _logger.warning(f"Redis invalidate_tags failed: {e}")
            self._handle_exception(e, "invalidate_tags", ", ".join(tags))

    def pop(self, key: str) -> None:
        try:
            self.redis_connector.delete_key(self._format_key(key))
        except Exception as e:
            _logger.warning(f"Redis pop failed for key={key}: {e}")
            self._handle_exception(e, "pop", key)

    def _format_key(self, key: str) -> str:
        return f"{self.prefix}:{key}" if self.prefix else key

    def _handle_exception(self, exception: Exception, operation: str, key: str) -> None:
        """Handle Redis exceptions, attempting to reconnect if it's a connection issue."""
        _logger.error(f"Redis {operation} operation failed for key '{key}': {str(exception)}")

        # Try to reconnect if it seems like a connection issue
        try:
            if isinstance(exception, ConnectionError | TimeoutError) or "connection" in str(exception).lower():
                _logger.info("Attempting to reconnect to Redis...")
                self.redis_connector.connect()
                if self.redis_connector.health_check():
                    _logger.info("Successfully reconnected to Redis")
                else:
                    _logger.error("Redis health check failed after reconnection attempt")
        except Exception as reconnect_error:
            _logger.error(f"Failed to reconnect to Redis: {str(reconnect_error)}")
