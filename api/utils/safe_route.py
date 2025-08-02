from functools import wraps
from flask import jsonify, Response
from werkzeug.exceptions import HTTPException
import traceback
from typing import Callable, Any, TypeVar, cast, Union, Tuple

# Generic type for decorator
F = TypeVar("F", bound=Callable[..., Union[Response, Tuple[Response, int]]])

def safe_route(handler: F) -> F:
    @wraps(handler)
    def wrapper(*args: Any, **kwargs: Any) -> Union[Response, Tuple[Response, int]]:
        try:
            return handler(*args, **kwargs)
        except HTTPException as http_err:
            return jsonify({
                "status": "error",
                "message": http_err.description or 'Unknown error occurred',
                "code": http_err.code or 500
            }), http_err.code or 500 


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

    return cast(F, wrapper)
