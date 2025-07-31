from flask import request
from flask_bcrypt import Bcrypt
from api.utils.responses import returnError, returnSuccess
from api.db.mongo import mongo


bcrypt = Bcrypt()

def register_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    username = data.get("username")
    
    if not email or not password or not username:
        return returnError("Email, password, and username are required.", status_code=401)
    
    if mongo.db.users.find_one({"email": email}) or mongo.db.users.find_one({"username": username}):
        return returnError("Email or username already exists.", status_code=409)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_document = {
        "email": email,
        "password": hashed_password,
        "username": username
    }
    mongo.db.users.insert_one(user_document)
    return returnSuccess("User registered successfully.", data={
        "user": {
            "email": email,
            "username": username
        }
    }, status_code=201)


def login_user(email, password):
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return returnError("Email and password are required.", status_code=401)

    user = mongo.db.users.find_one({"email": email})
    
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return returnError("Invalid email or password.", status_code=401)

    return returnSuccess("User logged in successfully.", data={
        "user": {
            "email": user["email"],
            "username": user["username"]
        }
    }, status_code=200)