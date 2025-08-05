import jwt
from datetime import datetime, timedelta
from typing import Union, Dict, Any
from app_config import SECRET_KEY, JWT_EXPIRY_SECONDS
from api.utils.responses import returnError

if not isinstance(SECRET_KEY, str) or not SECRET_KEY:
        raise ValueError("SECRET_KEY must be a non-empty string")

def generate_token(user_id: Union[str, int]) -> str:
    payload: Dict[str, Any] = {
        "user_id": str(user_id),
        "exp": datetime.now() + timedelta(seconds=JWT_EXPIRY_SECONDS)
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

from typing import Tuple
from flask import Response
from typing import Union, Tuple
from flask import Response


def decode_token(auth_token: str) -> Union[str, Tuple[Response, int]]:
    print('headers in decode: ' + auth_token)
    token = auth_token.split(' ')[1]

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get('user_id')
        if not user_id:
            return returnError('Missing user_id in token', 401)
        return user_id

    except jwt.ExpiredSignatureError:
        return returnError('Token has expired', 401)
    except jwt.InvalidTokenError:
        return returnError('Invalid token', 401)
