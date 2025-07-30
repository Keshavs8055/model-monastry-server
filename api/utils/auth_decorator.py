from flask import request
from api.utils.responses import returnError
from api.utils.jwt import decode_token

def token_required(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return returnError("Missing or invalid auth token", 401)

        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if not payload:
            return returnError("Invalid or expired token", 401)

        request.user_id = payload["user_id"]
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
