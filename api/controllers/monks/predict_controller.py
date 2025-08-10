from api.db.collections import get_monks_collection
from api.utils.responses import returnError, returnSuccess
from flask import g, request
import os
import pandas as pd
import joblib

def predict_with_monk_handler(monk_id):
    """
    Accepts a single-row JSON body or list of rows to predict.
    """
    from bson import ObjectId
    col = get_monks_collection()
    monk = col.find_one({"_id": ObjectId(monk_id), "user_id": g.user["_id"]})
    if not monk:
        return returnError("Monk not found", 404)

    model_path = monk.get("model_path")
    if not model_path or not os.path.exists(model_path):
        return returnError("Model file missing", 500)

    payload = request.get_json()
    if not payload:
        return returnError("Missing input data", 400)

    # Normalize input to DataFrame
    rows = payload if isinstance(payload, list) else [payload]
    df = pd.DataFrame(rows)

    # apply same preprocessing as in monk['config']
    from api.utils.pre_processing import preprocess_data
    cfg = monk.get("config", {})
    df_proc = preprocess_data(df, cfg)

    # simple encoding for object columns
    for col in df_proc.select_dtypes(include=['object', 'category']).columns:
        df_proc[col] = df_proc[col].astype('category').cat.codes

    model = joblib.load(model_path)
    preds = model.predict(df_proc)

    return returnSuccess("Prediction successful", data={"predictions": preds.tolist()})
