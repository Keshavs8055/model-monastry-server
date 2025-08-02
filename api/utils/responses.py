from flask import jsonify, Response
from typing import Any, Optional, Tuple, Dict


def returnError(message: str, status_code: int = 400) -> Tuple[Response, int]:
    return jsonify({'status': 'error', 'message': message}), status_code

def returnSuccess(
    message: str,
    data: Optional[Any] = None,
    status_code: int = 200
) -> Tuple[Response, int]:
    response: Dict[str, Any] = {
        'status': 'success',
        'message': message
    }

    if data is not None:
        response['data'] = data

    return jsonify(response), status_code
