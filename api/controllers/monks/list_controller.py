from api.db.collections import get_monks_collection
from api.utils.responses import returnError, returnSuccess
from flask import g

def list_monks_handler():
    col = get_monks_collection()
    docs = list(col.find({"user_id": g.user["_id"]}).sort("created_at", -1))
    for d in docs:
        d["_id"] = str(d["_id"])
        d["file_id"] = str(d.get("file_id"))
    return returnSuccess("Monks list", data={"monks": docs})
