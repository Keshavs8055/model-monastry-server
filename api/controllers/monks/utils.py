import os
import time
import traceback
from datetime import datetime
from typing import Any

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score
)

from config.logger import setup_logger
from api.utils.responses import returnError, returnSuccess
from api.db.collections import (
    get_user_files_collection,
    get_monks_collection,
    get_jobs_collection
)

logger = setup_logger(__name__)
# Map algorithm strings to classes
MODEL_MAP = {
    "linear_regression": {"task": "regression", "class": LinearRegression},
    "decision_tree_regressor": {"task": "regression", "class": DecisionTreeRegressor},
    "decision_tree": {"task": "classification", "class": DecisionTreeClassifier},
    "logistic_regression": {"task": "classification", "class": LogisticRegression},
    "knn_classifier": {"task": "classification", "class": KNeighborsClassifier},
    "knn_regressor": {"task": "regression", "class": KNeighborsRegressor}
}

MODELS_DIR = "models"  # base dir; ensure it exists at runtime
os.makedirs(MODELS_DIR, exist_ok=True)

# ---------- helpers ----------
def _get_user_latest_file(user_id):
    return get_user_files_collection().find_one(
        {"user_id": user_id},
        sort=[("upload_time", -1)]
    )

def _ensure_user_file_exists_or_error(user_id):
    user_file = _get_user_latest_file(user_id)
    if not user_file:
        return None, returnError("No uploaded file found. Upload a file first.", 400)
    return user_file, None

def _evaluate_regression(y_true, y_pred):
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mse": float(mean_squared_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred))
    }

def _evaluate_classification(y_true, y_pred):
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average='macro', zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average='macro', zero_division=0))
    }

def _save_model_for_user(user_id, model_obj, base_name):
    user_dir = os.path.join(MODELS_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    filename = f"{base_name}_{int(time.time())}.joblib"
    path = os.path.join(user_dir, filename)
    joblib.dump(model_obj, path)
    return path

# ---------- background job worker ----------
def _train_background(job_id: Any):
    """
    Background thread to perform training. Updates the jobs collection and monks collection.
    """
    jobs_col = get_jobs_collection()
    monks_col = get_monks_collection()

    job = jobs_col.find_one({"_id": job_id})
    if not job:
        logger.error("Job not found in DB: %s", job_id)
        return

    try:
        jobs_col.update_one({"_id": job_id}, {"$set": {"status": "running", "started_at": datetime.utcnow()}})
        user_id = job["user_id"]
        file_id = job["file_id"]
        algorithm = job["algorithm"]
        config = job.get("config", {})

        # Fetch file doc (fresh)
        user_file = get_user_files_collection().find_one({"_id": file_id, "user_id": user_id})
        if not user_file:
            raise RuntimeError("Uploaded file not found for user")

        df = pd.read_csv(user_file["path"])
        # Apply preprocessing: expect a utility preprocess_data(df, config)
        from api.utils.pre_processing import preprocess_data
        processed = preprocess_data(df, config)

        target = config.get("target_column")
        if not target or target not in processed.columns:
            raise RuntimeError("Invalid or missing target column in config")

        X = processed.drop(columns=[target])
        y = processed[target]

        # Basic encoding: convert object columns to category codes if any (simple approach)
        for col in X.select_dtypes(include=['object', 'category']).columns:
            X[col] = X[col].astype('category').cat.codes

        # For y in classification, encode if object
        if MODEL_MAP[algorithm]["task"] == "classification" and y.dtype == "object":
            y = y.astype('category').cat.codes

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.get("test_size", 0.2), random_state=42)

        ModelClass = MODEL_MAP[algorithm]["class"]
        model = ModelClass(**(config.get("model_params", {}) or {}))

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Evaluate
        if MODEL_MAP[algorithm]["task"] == "regression":
            metrics = _evaluate_regression(y_test, y_pred)
        else:
            metrics = _evaluate_classification(y_test, y_pred)

        # Save model
        base_name = f"{algorithm}"
        model_path = _save_model_for_user(user_id, model, base_name)

        # Create monk record
        monk_doc = {
            "user_id": user_id,
            "file_id": file_id,
            "name": f"{algorithm}_{int(time.time())}",
            "model_path": model_path,
            "config": config,
            "metrics": metrics,
            "created_at": datetime.utcnow()
        }
        res = monks_col.insert_one(monk_doc)

        # Update job as success
        jobs_col.update_one({"_id": job_id}, {"$set": {"status": "success", "monk_id": res.inserted_id, "finished_at": datetime.utcnow(), "metrics": metrics}})
        logger.info("Job %s completed successfully for user %s", job_id, str(user_id))

    except Exception as e:
        logger.exception("Training job failed: %s", e)
        jobs_col.update_one({"_id": job_id}, {"$set": {"status": "failed", "error": str(e), "trace": traceback.format_exc(), "finished_at": datetime.utcnow()}})
