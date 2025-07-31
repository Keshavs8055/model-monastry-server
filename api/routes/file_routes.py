from flask import Blueprint
from api.controllers.file_controller import upload_file
from api.utils.safe_route import safe_route

file_bp = Blueprint('file_bp', __name__)

file_bp.route('/upload', methods=['POST'])(safe_route(upload_file))
