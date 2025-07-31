from functools import wraps
from flask import jsonify
from werkzeug.exceptions import HTTPException
import traceback

def safe_route(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except HTTPException as http_err:
            return jsonify({
                "status": "error",
                "message": http_err.description,
                "code": http_err.code
            }), http_err.code

        except TypeError as type_err:
            return jsonify({
                "status": "error",
                "message": f"Incorrect arguments passed: {str(type_err)}",
                "trace": traceback.format_exc()
            }), 400

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Internal Server Error",
                "error": str(e),
                "trace": traceback.format_exc()
            }), 500
    return wrapper
