from flask_app import create_app
from config.logger import setup_logger

app = create_app()

logger = setup_logger(__name__)

@app.route('/health')
def health_check():
    return 'OK'

def handle_exception(e):
    logger.exception("Unhandled exception:")
    return {"error": "Something went wrong"}, 500

if __name__ == '__main__':
    app.run(debug=True)
