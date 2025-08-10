from pymongo.collection import Collection
from typing import Any
from api.db.mongo import get_db

def get_users_collection() -> Collection[Any]:
    return get_db()["users"]

def get_user_files_collection() -> Collection[Any]:
    return get_db()["user_files"]

def get_monks_collection() -> Collection[Any]:
    return get_db()["monks"]

def get_jobs_collection() -> Collection[Any]:
    return get_db()["jobs"]

# MONK:
# {
#   "_id": ObjectId,
#   "user_id": ObjectId,
#   "name": "monk_linear_20250810_1234",
#   "model_path": "models/<user_id>/monk_123.joblib",
#   "config": { ... },             // preprocessing + training config
#   "metrics": { ... },
#   "created_at": ISODate(...)
# }

# JOB:
# {
#   "_id": ObjectId,
#   "user_id": ObjectId,
#   "file_id": ObjectId,
#   "monk_id": ObjectId (optional),
#   "algorithm": "linear_regression",
#   "status": "pending|running|success|failed",
#   "error": "...",
#   "created_at": ISODate(),
#   "finished_at": ISODate()
# }

