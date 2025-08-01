import os
import pandas as pd
from flask import session
from utils.preprocessing import preprocess_data
from utils.responses import returnSuccess, returnError
from api.db import mongo
from flask_jwt_extended import get_jwt_identity

def preprocess_file(request):
    user_id = get_jwt_identity()
    config = request.get_json()

    if not config:
        return returnError("Missing preprocessing config.")

    # Get most recent file for user (or pass file_id explicitly)
    user_file = mongo.db.user_files.find_one({"user_id": user_id}, sort=[("created_at", -1)])

    if not user_file:
        return returnError("No uploaded file found for user.")

    # TODO: Check routing for files
    df = pd.read_csv(user_file['path'])
    processed_df = preprocess_data(df, config)

    preview = processed_df.head(10).to_dict(orient='records')

    # Save config and preview
    mongo.db.user_files.update_one(
        {"_id": user_file['_id']},
        {"$set": {"config": config, "processed_preview": preview}}
    )

    return returnSuccess("Preprocessing applied.", data={"preview": preview})