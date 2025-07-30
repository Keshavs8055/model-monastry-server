from flask import jsonify

def returnError(message, status_code=400):
    return jsonify({'status': 'error', 'message': message}), status_code

def returnSuccess(message, data=None, status_code=200):
    response = {'status': 'success', 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code