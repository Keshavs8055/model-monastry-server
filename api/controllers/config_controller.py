import pandas as pd
from api.utils.pre_processing import preprocess_data
from api.utils.responses import returnSuccess, returnError
from flask import request, g
from api.db.collections import get_users_collection, get_user_files_collection


def preprocess_file():
    user_id = g.user['_id']
    config = request.get_json().get("config")

    if not config:
        return returnError("Missing preprocessing config.")

    # Get most recent file for user (or pass file_id explicitly)
    user_file = get_user_files_collection().find_one({"user_id": user_id}, sort=[("created_at", -1)])
    
    if not user_file:
        return returnError("Upload a file first.", 400)
    
    get_user_files_collection().update_one(
        {"_id": user_file['_id']},
        {"$set": {"config": config}}
    )

    # TODO: Check routing for files
    df = pd.read_csv(user_file['path'])
    processed_df = preprocess_data(df, config)

    preview = processed_df.head(10).to_dict(orient='records')
    # Save config and preview
    get_user_files_collection().update_one(
        {"_id": user_file['_id']},
        {"$set": {"config": config, "processed_preview": preview}}
    )

    return returnSuccess("Preprocessing applied.", data={"preview": preview})