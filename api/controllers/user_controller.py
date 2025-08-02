from flask import request, Response
from flask_bcrypt import Bcrypt
from typing import Dict, Any, Union, Tuple
from api.utils.responses import returnError, returnSuccess
from api.db.mongo import mongo
from api.utils.jwt import generate_token
from api.db.collections import get_users_collection

bcrypt = Bcrypt()

def hash_password(password: str) -> str:
    hashed: bytes = bcrypt.generate_password_hash(password)
    return hashed.decode("utf-8")

def register_user() -> Tuple[Response, int]:
    data: Union[Dict[str, Any], None] = request.get_json()
    
    if not data:
        return returnError("Invalid or missing JSON body.", status_code=400)

    email: str | None = data.get("email")
    password: str | None = data.get("password")
    username: str | None = data.get("username")
    
    if not email or not password or not username:
        return returnError("Email, password, and username are required.", status_code=401)
    
    db = get_users_collection()
    
    if db.find_one({"email": email}) or db.find_one({"username": username}):
        return returnError("Email or username already exists.", status_code=409)

    hashed_password: str = bcrypt.generate_password_hash(password).decode("utf-8")
    
    user_document: Dict[str, str] = {
        "email": email,
        "password": hashed_password,
        "username": username
    }

    get_users_collection().insert_one(user_document)
    
    return returnSuccess("User registered successfully.", data={
        "user": {
            "email": email,
            "username": username
        }
    }, status_code=201)

def login_user() -> Tuple[Response, int]:
    data: Union[Dict[str, Any], None] = request.get_json()

    if not data:
        return returnError("Invalid or missing JSON body.", status_code=400)

    email: str | None = data.get("email")
    password: str | None = data.get("password")

    if not email or not password:
        return returnError("Email and password are required.", status_code=401)

    user: Union[Dict[str, Any], None] = get_users_collection().find_one({"email": email})

    if not user or not bcrypt.check_password_hash(user.get("password", ""), password):
        return returnError("Invalid email or password.", status_code=401)

    token: str = generate_token(user["_id"])

    return returnSuccess("User logged in successfully.", data={
        "user": {
            "email": user["email"],
            "username": user["username"],
            "token": token
        }
    }, status_code=200)
