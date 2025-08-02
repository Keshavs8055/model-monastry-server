from functools import wraps
from bson import ObjectId
from flask import request, Response
from flask import g
from typing import Callable, Any, TypeVar, cast
from api.db.collections import get_users_collection
from api.utils.responses import returnError
from api.utils.jwt import decode_token
from typing import Union, Tuple

F = TypeVar("F", bound=Callable[..., Any])

def token_required(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Union[Response, Tuple[Response, int]]:
        auth_header: str | None = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith('Bearer'):
            return returnError("Invalid Token passed", 401)
        
        user_id = decode_token(auth_header)  # decode_token already returns Response on error

        if not isinstance(user_id, str):  # decode_token returned an error Response
            return user_id  # Return the error response tuple directly

        print(user_id)
        
        g.user = get_users_collection().find_one({"_id": ObjectId(user_id)})
        
        if not g.user:
            return returnError("User not found", 404)
        
        return func(*args, **kwargs)
    
    return cast(F, wrapper)
