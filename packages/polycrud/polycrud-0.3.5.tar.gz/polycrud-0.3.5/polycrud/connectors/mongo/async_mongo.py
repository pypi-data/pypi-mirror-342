from __future__ import annotations

import logging
from collections.abc import AsyncGenerator, Iterable
from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from datetime import datetime
from enum import Enum
from typing import Any, Optional, TypeAlias, TypeVar

import pymongo
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession, AsyncIOMotorCollection, AsyncIOMotorDatabase

from polycrud import exceptions
from polycrud.cache import acache
from polycrud.connectors.base import DEFAULT_CACHE_TTL, AsyncBaseConnector
from polycrud.entity import ModelEntity

Logger = logging.getLogger(__name__)
_transaction_context: ContextVar[Transaction] = ContextVar("_transaction")
_DocumentType: TypeAlias = dict[str, Any]
Transaction: TypeAlias = AsyncIOMotorClientSession
T = TypeVar("T", bound=ModelEntity)
P = TypeVar("P")


class Sort(Enum):
    DESCENDING = pymongo.DESCENDING
    ASCENDING = pymongo.ASCENDING


class AsyncMongoConnector(AsyncBaseConnector):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        auth_source: str,
        **kwargs: Any,
    ) -> None:
        self.db_config = {"host": host, "port": port, "username": username, "password": password, "auth_source": auth_source, **kwargs}
        self.client: AsyncIOMotorClient[Any] | None = None
        self.db: AsyncIOMotorDatabase[Any] | None = None

    async def connect(self) -> None:
        """
        Connect to the data source.
        """
        if self.client is None:
            auth_source = self.db_config.pop("auth_source")
            self.client = AsyncIOMotorClient(**self.db_config)
            Logger.info("Connected to MongoDB at %s:%d", self.db_config["host"], self.db_config["port"])

            self.db = self.client.get_database(auth_source)

    async def disconnect(self) -> None:
        """
        Disconnect from the data source.
        """
        if self.client:
            self.client.close()
            Logger.info("Disconnected from MongoDB")
            self.client = None

    async def create_index(self, collection: type[T], fields: str | tuple[str, ...], unique: bool = True) -> None:
        await self._get_collection(collection).create_index(fields, unique=unique)

    @acache()
    async def find_one(
        self, collection: type[T], *, _use_cache: bool | None = None, _cache_ttl: int = DEFAULT_CACHE_TTL, **kwargs: Any
    ) -> T | None:
        result = await self._get_collection(collection).find_one(self._to_mongo_dict(kwargs, True), session=_transaction_context.get(None))
        if result is None:
            return None
        doc = self._to_entity_dict(result)
        return collection(**doc)

    @acache()
    async def find_many(
        self,
        collection: type[T],
        *,
        limit: int = 10_000,
        offset: int = 0,
        sort_by: str = "_id",
        sort_dir: Sort = Sort.DESCENDING,
        _use_cache: bool | None = None,
        _cache_ttl: int = DEFAULT_CACHE_TTL,
        **kwargs: Any,
    ) -> list[T]:
        doc = self._to_mongo_dict(kwargs, True)
        sort = [(sort_by, sort_dir.value)]
        cursor = self._get_collection(collection).find(doc, sort=sort, limit=limit, skip=offset, session=_transaction_context.get(None))
        results = await cursor.to_list(length=None)
        entities = [self._to_entity_dict(x) for x in results]
        return [collection(**x) for x in entities]

    @acache()
    async def update_one(
        self,
        obj: T,
        *,
        attributes: Iterable[str] = None,
        exclude_fields: Iterable[str] = None,
        _use_cache: bool | None = None,
        _cache_ttl: int = DEFAULT_CACHE_TTL,
    ) -> T:
        doc = self._to_mongo_dict(self._model_dump(obj, attributes, exclude_fields, serialize_as_any=True), False)
        #     Logger.debug("process db.update record %s", obj.__class__.__name__)
        assert isinstance(obj.id, str)
        updated_doc = await self._get_collection(obj).find_one_and_update(
            {"_id": ObjectId(obj.id)},
            {"$set": doc},
            return_document=pymongo.ReturnDocument.AFTER,
            session=_transaction_context.get(None),
        )
        return obj.__class__(**self._to_entity_dict(updated_doc)) if not obj else obj

    @acache()
    async def insert_one(self, obj: T, *, _use_cache: bool | None = None, _cache_ttl: int = DEFAULT_CACHE_TTL) -> T:
        doc = self._to_mongo_dict(self._model_dump(obj), False)
        try:
            Logger.debug("process db.insert %s", obj.__class__.__name__)
            result = await self._get_collection(obj).insert_one(doc, session=_transaction_context.get(None))
            doc["_id"] = result.inserted_id
            return obj.__class__(**self._to_entity_dict(doc))
        except exceptions.DuplicateKeyError as e:
            raise exceptions.DuplicateKeyError(f"Duplicate records {obj.__class__.__name__}") from e

    @acache()
    async def insert_many(self, objs: list[T], *, _use_cache: bool | None = None, _cache_ttl: int = DEFAULT_CACHE_TTL) -> list[T]:
        col = set(type(o) for o in objs)
        if len(col) > 1:
            raise exceptions.InvalidArgumentError("All objects must belong to the same collection")

        typ = list(col)[0]
        docs = [self._to_mongo_dict(self._model_dump(o), False) for o in objs]
        try:
            # Logger.debug("process db.insert list class %s", typ.__class__.__name__)
            insert_result = await self._get_collection(typ).insert_many(docs, session=_transaction_context.get(None))
            objs = []
            for doc, id in zip(docs, insert_result.inserted_ids, strict=True):
                doc["_id"] = id
                objs.append(typ(**self._to_entity_dict(doc)))
            return objs
        except exceptions.DuplicateKeyError as e:
            raise exceptions.DuplicateKeyError(f"Duplicate records {typ.__name__}") from e

    @acache()
    async def delete_one(
        self, collection: type[T], *, id: str, _use_cache: bool | None = None, _cache_ttl: int = DEFAULT_CACHE_TTL
    ) -> None:
        if not id:
            return

        txn = _transaction_context.get(None)
        Logger.debug("process db.delete record %s", collection.__name__)
        doc = await self._get_collection(collection).find_one_and_delete({"_id": ObjectId(id)}, session=txn)
        if doc is None:
            raise exceptions.NotFoundError("Error finding record in pymongo")
        doc["collection"] = collection.__name__
        doc["deleted_at"] = datetime.now()

    @acache()
    async def delete_many(
        self,
        collection: type[T],
        *,
        ids: list[str],
        _use_cache: bool | None = None,
        _cache_ttl: int = DEFAULT_CACHE_TTL,
    ) -> None:
        if not ids:
            return

        txn = _transaction_context.get(None)
        _ids = [ObjectId(x) for x in ids]
        cursor = self._get_collection(collection).find({"_id": {"$in": _ids}}, session=txn)
        docs = await cursor.to_list(length=None)
        if len(docs) != len(_ids):
            raise exceptions.NotFoundError("Error finding record to delete")
        #         Logger.debug("process db.delete list %s", collection.__name__)
        deleted_at = datetime.now()
        for doc in docs:
            doc["collection"] = collection.__name__
            doc["deleted_at"] = deleted_at
        await self._get_collection(collection).delete_many({"_id": {"$in": ids}}, session=txn)

    @acache()
    async def count(
        self, collection: type[T], *, _use_cache: bool | None = None, _cache_ttl: int = DEFAULT_CACHE_TTL, **kwargs: Any
    ) -> int:
        return await self._get_collection(collection).count_documents(
            self._to_mongo_dict(kwargs, True), session=_transaction_context.get(None)
        )

    @acache()
    async def aggregate(
        self,
        collection: type[T] | str,
        *,
        pipeline: list[dict[str, Any]],
        _use_cache: bool | None = None,
        _cache_ttl: int = DEFAULT_CACHE_TTL,
    ) -> list[dict[str, Any]]:
        cursor = self._get_collection(collection).aggregate(pipeline, session=_transaction_context.get(None))
        results = await cursor.to_list(length=None)
        return results

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[None, None]:
        session: Optional[Transaction] = None
        token: Optional[Token[Transaction]] = None
        try:
            assert self.client is not None
            session = await self.client.start_session(causal_consistency=True)
            token = _transaction_context.set(session)
            async with session.start_transaction():
                yield
        except Exception as e:
            if session and session.in_transaction():
                await session.abort_transaction()
            raise e
        finally:
            if session:
                await session.end_session()
            if token:
                _transaction_context.reset(token)

    async def health_check(self) -> bool:
        """
        Check the health of the connection.
        """
        try:
            assert self.client is not None
            await self.client.admin.command("ping")
            return True
        except Exception as e:
            Logger.error(f"Error connecting to MongoDB: {e}")
            return False

    def _get_collection(self, target: ModelEntity | type | str) -> AsyncIOMotorCollection[Any]:
        assert self.db is not None
        if isinstance(target, str):
            return self.db[target]
        if isinstance(target, type):
            return self.db[target.__name__]
        return self.db[type(target).__name__]

    @staticmethod
    def _model_dump(
        obj: T, include: Iterable[str] | None = None, exclude: Iterable[str] | None = None, serialize_as_any: bool = False
    ) -> dict[str, Any]:
        doc = obj.model_dump(
            include=set(include) if include else None, exclude=set(exclude) if exclude else None, serialize_as_any=serialize_as_any
        )
        now = datetime.now()
        if "created_at" in doc and not doc["created_at"]:
            doc["created_at"] = now

        if exclude is None or "modified_at" not in exclude:
            doc["modified_at"] = now
        return doc

    def _to_mongo_dict(self, doc: _DocumentType, query: bool) -> _DocumentType:
        doc = {k: self._to_mongo_value(v, query) for k, v in doc.items()}
        if "id" in doc:
            doc["_id"] = ObjectId(doc.pop("id"))
        return doc

    def _to_mongo_value(self, v: Any, query: bool) -> Any:
        # if isinstance(v, str):
        #     if ObjectId.is_valid(v):
        #         return ObjectId(v)
        #     return ObjectId(v.encode() if v else None)
        if isinstance(v, set | list):
            values = [self._to_mongo_value(x, False) for x in v]
            if query:
                return {"$in": values}
            return values
        return v

    def _to_entity_dict(self, doc: _DocumentType) -> _DocumentType:
        doc = {k: self._to_entity_value(v) for k, v in doc.items()}
        doc["id"] = doc.pop("_id") if "_id" in doc else ""
        return doc

    def _to_entity_value(self, v: Any) -> Any:
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, list):
            return [self._to_entity_value(x) for x in v]
        return v
