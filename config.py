import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_EXPIRY_SECONDS = int(os.getenv("JWT_EXPIRY_SECONDS", 3600)) 