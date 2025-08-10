from api.db.collections import get_monks_collection
from api.utils.responses import returnError, returnSuccess
from flask import g

def get_monk_handler(monk_id):
    from bson import ObjectId
    col = get_monks_collection()
    monk = col.find_one({"_id": ObjectId(monk_id), "user_id": g.user["_id"]})
    if not monk:
        return returnError("Monk not found", 404)
    monk["_id"] = str(monk["_id"])
    monk["file_id"] = str(monk.get("file_id"))
    return returnSuccess("Monk fetched", data={"monk": monk})
