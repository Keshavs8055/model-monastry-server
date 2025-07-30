from api.routes.file_routes import file_bp
from api.routes.user_routes import auth_bp

def registerBlueprints(app):
    app.register_blueprint(file_bp, url_prefix='/api/file')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')