from api.db.collections import get_jobs_collection  
from api.utils.responses import returnError, returnSuccess
from flask import g

def job_status_handler(job_id):
    jobs_col = get_jobs_collection()
    
    from bson import ObjectId
    job = jobs_col.find_one({"_id": ObjectId(job_id), "user_id": g.user["_id"]})
    
    if not job:
        return returnError("Job not found", 404)
    # filter fields for response
    job_resp = {
        "job_id": str(job["_id"]),
        "status": job.get("status"),
        "error": job.get("error"),
        "monk_id": str(job.get("monk_id")) if job.get("monk_id") else None,
        "metrics": job.get("metrics")
    }
    return returnSuccess("Job status", data=job_resp)

