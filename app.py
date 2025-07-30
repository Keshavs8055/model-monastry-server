from flask import Flask
from flask_cors import CORS
from config import Config
from api.db.mongo import init_app
from api.utils.register import registerBlueprints

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
init_app(app)
registerBlueprints(app)


@app.route('/health')
def health_check():
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True)
