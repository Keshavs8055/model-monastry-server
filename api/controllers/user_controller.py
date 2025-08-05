from flask import request, Response
from flask_bcrypt import Bcrypt
from typing import Dict, Any, Union, Tuple
from api.utils.responses import returnError, returnSuccess
from api.utils.jwt import generate_token
from api.db.collections import get_users_collection
from config.logger import setup_logger 

logger = setup_logger(__name__)  
bcrypt = Bcrypt()

def hash_password(password: str) -> str:
    hashed: bytes = bcrypt.generate_password_hash(password)
    return hashed.decode("utf-8")

def register_user() -> Tuple[Response, int]:
    logger.info("Register user request received")
    data: Union[Dict[str, Any], None] = request.get_json()
    
    if not data:
        logger.warning("Missing or invalid JSON body in registration")
        return returnError("Invalid or missing JSON body.", status_code=400)

    email: str | None = data.get("email")
    password: str | None = data.get("password")
    username: str | None = data.get("username")

    if not email or not password or not username:
        logger.warning("Missing registration fields - email/password/username")
        return returnError("Email, password, and username are required.", status_code=401)

    db = get_users_collection()
    
    if db.find_one({"email": email}) or db.find_one({"username": username}):
        logger.warning(f"Duplicate registration attempt - Email: {email} or Username: {username}")
        return returnError("Email or username already exists.", status_code=409)

    try:
        hashed_password: str = bcrypt.generate_password_hash(password).decode("utf-8")
        user_document: Dict[str, str] = {
            "email": email,
            "password": hashed_password,
            "username": username
        }

        db.insert_one(user_document)
        logger.info(f"User registered - Email: {email}, Username: {username}")
    except Exception as e:
        logger.exception("Database error during user registration")
        return returnError("Internal server error during registration", status_code=500)

    return returnSuccess("User registered successfully.", data={
        "user": {
            "email": email,
            "username": username
        }
    }, status_code=201)

def login_user() -> Tuple[Response, int]:
    logger.info("Login request received")
    data: Union[Dict[str, Any], None] = request.get_json()

    if not data:
        logger.warning("Missing or invalid JSON body in login")
        return returnError("Invalid or missing JSON body.", status_code=400)

    email: str | None = data.get("email")
    password: str | None = data.get("password")

    if not email or not password:
        logger.warning("Missing login fields - email/password")
        return returnError("Email and password are required.", status_code=401)

    try:
        user: Union[Dict[str, Any], None] = get_users_collection().find_one({"email": email})

        if not user or not bcrypt.check_password_hash(user.get("password", ""), password):
            logger.warning(f"Failed login attempt - Email: {email}")
            return returnError("Invalid email or password.", status_code=401)

        token: str = generate_token(user["_id"])
        logger.info(f"User logged in successfully - Email: {email}")
    except Exception as e:
        logger.exception("Error during login process")
        return returnError("Internal server error during login", status_code=500)

    return returnSuccess("User logged in successfully.", data={
        "user": {
            "email": user["email"],
            "username": user["username"],
            "token": token
        }
    }, status_code=200)
