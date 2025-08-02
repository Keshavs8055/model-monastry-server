from flask import Blueprint
from api.controllers.file_controller import upload_file
from api.utils.auth_decorator import token_required
from api.utils.safe_route import safe_route
from api.controllers.config_controller import preprocess_file


file_bp = Blueprint('file_bp', __name__)

@file_bp.route('/upload', methods=['POST'])
@token_required
@safe_route
def upload_handler():
    return upload_file()


@file_bp.route('/preprocess', methods=['POST'])
@token_required
@safe_route
def preprocess_handler():
    return preprocess_file()

# TODO - Get route to preview file