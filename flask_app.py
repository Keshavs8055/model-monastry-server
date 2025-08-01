from flask import Flask
from config import Config
from flask_cors import CORS
from api.db.mongo import init_app
from api.routes.user_routes import auth_bp
from api.routes.file_routes import file_bp


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    CORS(app)
    init_app(app)
    
    
    app.register_blueprint(file_bp, url_prefix='/api/file')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app
    
