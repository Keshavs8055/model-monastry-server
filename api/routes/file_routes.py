from flask import Blueprint
from api.controllers.file_controller import upload_file, configure_model

file_bp = Blueprint('file_bp', __name__)

file_bp.route('/upload', methods=['POST'])(upload_file)
