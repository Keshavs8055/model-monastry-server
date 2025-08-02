from pymongo.collection import Collection
from typing import Any
from api.db.mongo import get_db

def get_users_collection() -> Collection[Any]:
    return get_db()["users"]

def get_user_files_collection() -> Collection[Any]:
    return get_db()["user_files"]
