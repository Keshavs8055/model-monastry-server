import pandas as pd
from api.utils.pre_processing import preprocess_data
from api.utils.responses import returnSuccess, returnError
from flask import request, g
from api.db.collections import get_user_files_collection
from config.logger import setup_logger

logger = setup_logger(__name__)

# TODO: Define the expected structure of the preprocessing config
# Example structure:
# {
#   "drop_columns": ["user_id", "session_id"],
#   "rename_columns": { "old_name": "new_name" },
#   "fill_na": { "age": 0, "gender": "unknown" },
#   "normalize_columns": ["income", "expenses"],
#   "encode_columns": ["gender"],
#   "log_transform": ["sales"],
#   "cast_types": { "age": "int", "income": "float" },
#   "remove_duplicates": true,
#   "shuffle": true,
#   "split_ratio": { "train": 0.8, "test": 0.2 },
#   "target_column": "churn"
# }


def preprocess_file():
    user_id = g.user['_id']
    logger.info(f"Starting preprocessing for user_id: {user_id}")

    config = request.get_json().get("config")

    if not config:
        logger.warning("Missing preprocessing config.")
        return returnError("Missing preprocessing config.")

    config = {k.lower(): v for k, v in config.items()}
    logger.debug(f"Received config: {config}")

    user_file = get_user_files_collection().find_one({"user_id": user_id}, sort=[("created_at", -1)])

    if not user_file:
        logger.warning("No uploaded file found for user.")
        return returnError("Upload a file first.", 400)

    logger.info(f"Using file: {user_file['path']}")

    get_user_files_collection().update_one(
        {"_id": user_file['_id']},
        {"$set": {"config": config}}
    )

    try:
        df = pd.read_csv(user_file['path'])
        logger.debug(f"Loaded DataFrame with shape: {df.shape}")
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        return returnError("Failed to read file.", 500)

    try:
        processed_df = preprocess_data(df, config)
        preview = processed_df.head(10).to_dict(orient='records')

        get_user_files_collection().update_one(
            {"_id": user_file['_id']},
            {"$set": {"config": config, "processed_preview": preview}}
        )

        logger.info("Preprocessing complete and preview saved.")
        return returnSuccess("Preprocessing applied.", data={"preview": preview})
    except Exception as e:
        logger.exception("Failed during preprocessing.")
        return returnError("Error during preprocessing.", 500)
