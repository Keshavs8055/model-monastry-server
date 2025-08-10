import threading
from datetime import datetime

from flask import request, g

from config.logger import setup_logger
from api.utils.responses import returnError, returnSuccess
from api.db.collections import (
    get_user_files_collection,
    get_jobs_collection
)
from api.controllers.monks.utils import _get_user_latest_file
from api.controllers.monks.utils import MODEL_MAP, _train_background

logger = setup_logger(__name__)


# ---------- controllers (HTTP) ----------
def train_monk_handler():
    """
    API contract:
    POST /api/monk/train
    body: {
        "file_id": "<optional - otherwise use latest>",
        "config": { ... preprocessing + training config ... },
        "algorithm": "linear_regression" (must be key in MODEL_MAP)
    }
    returns: job_id (immediate), 202 Accepted
    """
    user = g.user
    user_id = user["_id"]

    payload = request.get_json() or {}
    config = payload.get("config") or {}
    algorithm = payload.get("algorithm")
    file_id = payload.get("file_id")  # optional; ObjectId from client

    if not algorithm or algorithm not in MODEL_MAP:
        return returnError("Invalid or missing algorithm", 400)

    # fetch file (explicit or latest)
    if file_id:
        # validate ownership
        file_doc = get_user_files_collection().find_one({"_id": file_id, "user_id": user_id})
    else:
        file_doc = _get_user_latest_file(user_id)

    if not file_doc:
        return returnError("No uploaded file found for user. Upload first.", 400)

    # ensure config includes target
    if not config.get("target_column"):
        return returnError("Missing target_column in config", 400)

    # store job doc
    jobs_col = get_jobs_collection()
    job_doc = {
        "user_id": user_id,
        "file_id": file_doc["_id"],
        "algorithm": algorithm,
        "config": config,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    job_res = jobs_col.insert_one(job_doc)

    job_id = job_res.inserted_id
    logger.info("Queued training job %s for user %s (algorithm=%s)", job_id, str(user_id), algorithm)

    # start background thread (lightweight). For production, replace with Celery
    t = threading.Thread(target=_train_background, args=(job_id,), daemon=True)
    t.start()

    return returnSuccess("Training started", data={"job_id": str(job_id)}, status_code=202)



