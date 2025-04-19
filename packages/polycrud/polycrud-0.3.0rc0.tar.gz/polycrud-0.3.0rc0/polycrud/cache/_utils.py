from enum import Enum
from typing import Any


class QueryType(str, Enum):
    FindOne = "find_one"
    FindMany = "find_many"
    FullTextSearch = "full_text_search"
    Aggregate = "aggregate"
    RawQuery = "raw_query"
    InsertOne = "insert_one"
    InsertMany = "insert_many"
    UpdateOne = "update_one"
    DeleteOne = "delete_one"
    DeleteMany = "delete_many"


def _get_query_type(fn_name: str) -> QueryType | None:
    return next((qt for qt in QueryType if qt in fn_name), None)


def _get_tags(base: str, collection: str, obj_id: Any = None) -> list[str]:
    tags = [base, f"{base}:{collection}"]
    if obj_id is not None:
        tags.append(f"{base}:{collection}:{obj_id}")
    return tags
