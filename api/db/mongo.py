from flask import Flask, g
from flask_pymongo import PyMongo
from pymongo.database import Database
from typing import Any, cast

mongo: PyMongo = PyMongo()

def init_app(app: Flask):
    mongo.init_app(app)
    print("MongoDB initialized with app configuration.")
    return mongo


def get_db() -> Database[Any]:
    db = getattr(g, "_database", None)
    if db is None:
        db = mongo.db
        g._database = db
    return cast(Database[Any], db)
