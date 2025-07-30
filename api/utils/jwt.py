import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY, JWT_EXPIRY_SECONDS
from api.utils.responses import returnError

def generate_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.now() + timedelta(seconds=JWT_EXPIRY_SECONDS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return returnError('Token has expired', status_code=401)
    except jwt.InvalidTokenError:
        return returnError('Invalid token', status_code=401)
