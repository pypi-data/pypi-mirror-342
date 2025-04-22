from __future__ import annotations

import logging
import traceback
from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING, Any, TypeVar, cast

from polycrud import exceptions
from polycrud.constants import NULL_VALUE
from polycrud.entity import ModelEntity

from ._utils import QueryType, build_cache_key, get_model_class_from_args, get_query_type, get_tags

if TYPE_CHECKING:
    from polycrud.connectors.pyredis import RedisConnector
F = TypeVar("F", bound=Callable[..., Any])

_logger = logging.getLogger(__name__)
ModelT = TypeVar("ModelT", bound=ModelEntity)


class _Settings:
    redis_cache: RedisCache | None = None
    is_ready: bool = False


def setup(redis_connector: RedisConnector, ttl: int = 3600 * 4, prefix: str | None = None) -> None:
    if _Settings.redis_cache is not None:
        raise RuntimeError("Redis cache is already set up.")
    _Settings.redis_cache = RedisCache(redis_connector=redis_connector, ttl=ttl, prefix=prefix)
    _Settings.is_ready = True


def cache() -> Callable[[F], F]:
    def decorator(fn: F) -> F:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not _Settings.is_ready:
                if _Settings.redis_cache is not None:
                    _logger.debug(f"Redis cache is not ready, skipping cache for {fn.__name__}")
                return fn(*args, **kwargs)

            # If no cache is set up, just call the function
            _use_cache = kwargs.pop("_use_cache") if "_use_cache" in kwargs else True
            if _Settings.redis_cache is None or not _use_cache:
                return fn(*args, **kwargs)

            # Determine the class name and model class from the arguments
            fn_name = fn.__name__
            cls_name = args[0].__class__.__name__
            ttl = kwargs.get("_cache_ttl", None)

            try:
                model_class = get_model_class_from_args(args, kwargs)
                model_name = model_class.__name__ if model_class is not None else "Any"
            except Exception:
                # If we can't determine the model class, just call the function
                _logger.debug(f"Could not determine model class for {cls_name}.{fn_name}, skipping cache")
                return fn(*args, **kwargs)

            query_type = get_query_type(fn_name)
            redis_cache = _Settings.redis_cache

            updated_kwargs = kwargs.copy()
            if fn_name == "raw_query" and len(args[1]) > 1 and isinstance(args[1], str):
                # If the function is raw_query and the second argument is greater than 1, skip caching
                updated_kwargs["query"] = args[1]
            cache_key = build_cache_key(cls_name, model_name, fn_name, updated_kwargs)

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

                tags = get_tags(cls_name, model_name)
                tags += [f"{cls_name}:{model_name}:{oid}" for oid in obj_ids if oid]
                redis_cache.invalidate_tags(tags)

                return fn(*args, **kwargs)

            # Handle read operations
            cached = redis_cache.get(cache_key, model_class)
            if cached is not None or cached == NULL_VALUE:
                _logger.debug(f"Cache hit: {cache_key}")
                if cached == NULL_VALUE:
                    # If the cached value is NULL_VALUE, return None
                    return None
                return cached

            _logger.debug(f"Cache miss: {cache_key}")
            result = fn(*args, **kwargs)

            # Determine tags based on query type
            if result is None:
                tags = [f"{cls_name}:{model_name}"]
            else:
                tags = {
                    QueryType.FindOne: [f"{cls_name}:{model_name}:{getattr(result, 'id', '')}"],
                    QueryType.FindMany: [f"{cls_name}:{model_name}"],
                }.get(query_type, [cls_name])  # type: ignore

            redis_cache.set(cache_key, result, ttl=ttl, tags=tags)
            return result

        return cast(F, wrapper)

    return decorator


def redis_cache_is_healthy() -> bool:
    """Check if the Redis cache is healthy."""
    if not _Settings.redis_cache:
        return False
    if _Settings.redis_cache.redis_connector.health_check():
        _Settings.is_ready = True
    else:
        _Settings.is_ready = False
    return _Settings.is_ready


class RedisCache:
    def __init__(self, redis_connector: RedisConnector, ttl: int = 3600 * 4, prefix: str | None = "polycrud") -> None:
        self.ttl = ttl
        self.prefix = prefix
        self.redis_connector = redis_connector
        self.redis_connector.connect()

    def initialize(self) -> None:
        try:
            self.redis_connector.connect()
            if not self.redis_connector.health_check():
                self.redis_connector.connect()
        except Exception as e:
            _logger.error(f"Failed to initialize Redis connection: {str(e)}")
            raise exceptions.RedisConnectionError(f"Could not connect to Redis: {str(e)}") from e

    def get(self, key: str, model_cls: type[ModelT] | None = None) -> ModelT | bytes | None:
        if not self.redis_connector:
            return None
        try:
            if model_cls is None:
                value = self.redis_connector.get_object(None, key=self._format_key(key))
            else:
                value = self.redis_connector.get_object(model_cls, key=self._format_key(key))  # type: ignore
            if value == NULL_VALUE:
                return NULL_VALUE
            return value
        except Exception as e:
            _logger.warning(f"Redis get failed for key={key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int | None = None, tags: list[str] | None = None) -> None:
        if not self.redis_connector.client:
            return
        try:
            full_key = self._format_key(key)
            self.redis_connector.set_object(full_key, value, ttl or self.ttl)
            if tags:
                self._add_tags(full_key, tags)
        except Exception as e:
            traceback.print_exc()
            _logger.warning(f"Redis set failed for key={key}: {e}")

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

    def pop(self, key: str) -> None:
        if not self.redis_connector.client:
            _logger.warning("Redis pop failed: Redis client is not connected.")
            return
        try:
            self.redis_connector.delete_key(self._format_key(key))
        except Exception as e:
            _logger.warning(f"Redis pop failed for key={key}: {e}")

    def _format_key(self, key: str) -> str:
        return f"{self.prefix}:{key}" if self.prefix else key
