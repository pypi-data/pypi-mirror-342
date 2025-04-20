from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING, Any, TypeVar, cast

from polycrud import exceptions
from polycrud.entity import ModelEntity

from ..constants import NULL_VALUE
from ._utils import QueryType, build_cache_key, get_model_class_from_args, get_query_type, get_tags

if TYPE_CHECKING:
    from polycrud.connectors.pyredis import AsyncRedisConnector
F = TypeVar("F", bound=Callable[..., Any])

_logger = logging.getLogger(__name__)
ModelT = TypeVar("ModelT", bound=ModelEntity)


class _Settings:
    redis_cache: AsyncRedisCache


def setup(redis_connector: AsyncRedisConnector, ttl: int = 3600 * 4, prefix: str | None = None) -> None:
    if hasattr(_Settings, "redis_cache"):
        raise RuntimeError("Redis cache is already set up.")
    _Settings.redis_cache = AsyncRedisCache(redis_connector=redis_connector, ttl=ttl, prefix=prefix)
    _Settings.redis_cache.redis_connector.connect()


def acache() -> Callable[[F], F]:
    def decorator(fn: F) -> F:
        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # If no cache is set up, just call the function
            _use_cache = kwargs.pop("_use_cache") if "_use_cache" in kwargs else True
            if not hasattr(_Settings, "redis_cache") or not _use_cache:
                return await fn(*args, **kwargs)

            # Determine the class name and model class from the arguments
            fn_name = fn.__name__
            cls_name = args[0].__class__.__name__
            ttl = kwargs.get("_cache_ttl", None)

            try:
                model_class = get_model_class_from_args(args, kwargs)
                model_name = model_class.__name__ if model_class is not None else "Any"
            except TypeError:
                _logger.debug(f"Could not determine model class for {cls_name}.{fn_name}, use as Any")
                return await fn(*args, **kwargs)

            query_type = get_query_type(fn_name)

            if not hasattr(_Settings, "redis_cache"):
                return await fn(*args, **kwargs)

            redis_cache = _Settings.redis_cache
            cache_key = build_cache_key(cls_name, model_name, fn_name, kwargs)

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
                await redis_cache.invalidate_tags(tags)

                return await fn(*args, **kwargs)

            # Handle read operations
            cached = await redis_cache.get(cache_key, model_class)
            if cached or cached == NULL_VALUE:
                _logger.debug(f"Cache hit: {cache_key}")
                if cached == NULL_VALUE:
                    # If cached value is NULL_VALUE, return None
                    return None
                return cached

            _logger.debug(f"Cache miss: {cache_key}")
            result = await fn(*args, **kwargs)

            # Determine tags based on query type
            if result is None:
                tags = [f"{cls_name}:{model_name}"]
            else:
                tags = {
                    QueryType.FindOne: [f"{cls_name}:{model_name}:{getattr(result, 'id', '')}"],
                    QueryType.FindMany: [f"{cls_name}:{model_name}"],
                }.get(query_type, [cls_name])  # type: ignore

            await redis_cache.set(cache_key, result, ttl=ttl, tags=tags)
            return result

        return cast(F, wrapper)

    return decorator


class AsyncRedisCache:
    def __init__(self, redis_connector: AsyncRedisConnector, ttl: int = 3600 * 4, prefix: str | None = "polycrud") -> None:
        self.ttl = ttl
        self.prefix = prefix
        self.redis_connector = redis_connector
        self.redis_connector.connect()

    async def initialize(self) -> None:
        try:
            self.redis_connector.connect()
            if not await self.redis_connector.health_check():
                self.redis_connector.connect()
        except Exception as e:
            _logger.error(f"Failed to initialize Redis connection: {str(e)}")
            raise exceptions.RedisConnectionError(f"Could not connect to Redis: {str(e)}") from e

    async def get(self, key: str, model_cls: type[ModelT] | None = None) -> ModelT | bytes | None:
        try:
            if model_cls is None:
                value = await self.redis_connector.get_object(None, key=self._format_key(key))
            else:
                value = await self.redis_connector.get_object(model_cls, key=self._format_key(key))  # type: ignore
            if value == NULL_VALUE:
                return NULL_VALUE
            return value
        except Exception as e:
            _logger.warning(f"Redis get failed for key={key}: {e}")
            await self._handle_exception(e, "get", key)
            return None

    async def set(self, key: str, value: Any, ttl: int | None = None, tags: list[str] | None = None) -> None:
        try:
            full_key = self._format_key(key)
            await self.redis_connector.set_object(full_key, value, ttl or self.ttl)
            if tags:
                await self._add_tags(full_key, tags)
        except Exception as e:
            _logger.warning(f"Redis set failed for key={key}: {e}")
            await self._handle_exception(e, "set", key)

    async def _add_tags(self, key: str, tags: list[str]) -> None:
        if not self.redis_connector.client:
            return
        try:
            pipe = self.redis_connector.client.pipeline()
            for tag in tags:
                await pipe.sadd(f"tag:{tag}", key)  # type: ignore
            await pipe.execute()
        except Exception as e:
            _logger.warning(f"Redis add_tags failed for key={key}: {e}")
            await self._handle_exception(e, "add_tags", key)

    async def invalidate_tags(self, tags: list[str]) -> None:
        if not tags or not self.redis_connector.client:
            return
        try:
            pipe = self.redis_connector.client.pipeline()
            all_keys = set()
            for tag in tags:
                keys = await self.redis_connector.client.smembers(f"tag:{tag}")  # type: ignore
                all_keys.update(keys)

            if all_keys:
                await pipe.delete(*all_keys)

            # Delete the tag sets themselves
            for tag in tags:
                await pipe.delete(f"tag:{tag}")

            await pipe.execute()
        except Exception as e:
            _logger.warning(f"Redis invalidate_tags failed: {e}")
            await self._handle_exception(e, "invalidate_tags", ", ".join(tags))

    async def pop(self, key: str) -> None:
        try:
            await self.redis_connector.delete_key(self._format_key(key))
        except Exception as e:
            _logger.warning(f"Redis pop failed for key={key}: {e}")
            await self._handle_exception(e, "pop", key)

    def _format_key(self, key: str) -> str:
        return f"{self.prefix}:{key}" if self.prefix else key

    async def _handle_exception(self, exception: Exception, operation: str, key: str) -> None:
        """Handle Redis exceptions, attempting to reconnect if it's a connection issue."""
        _logger.error(f"Redis {operation} operation failed for key '{key}': {str(exception)}")

        # Try to reconnect if it seems like a connection issue
        try:
            if isinstance(exception, ConnectionError | TimeoutError) or "connection" in str(exception).lower():
                _logger.info("Attempting to reconnect to Redis...")
                self.redis_connector.connect()
                if await self.redis_connector.health_check():
                    _logger.info("Successfully reconnected to Redis")
                else:
                    _logger.error("Redis health check failed after reconnection attempt")
        except Exception as reconnect_error:
            _logger.error(f"Failed to reconnect to Redis: {str(reconnect_error)}")
