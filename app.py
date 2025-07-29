from flask import Flask
from flask_cors import CORS
from config import Config
from api.db.mongo import init_app
from api.routes.file_routes import file_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
init_app(app)

app.register_blueprint(file_bp, url_prefix='/api/file')

if __name__ == '__main__':
    app.run(debug=True)
