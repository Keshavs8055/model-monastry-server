from flask import Blueprint
from api.controllers.file_controller import upload_file
from api.utils.safe_route import safe_route
from api.controllers.config_controller import preprocess_file

file_bp = Blueprint('file_bp', __name__)

file_bp.route('/upload', methods=['POST'])(safe_route(upload_file))
file_bp.route('/config/preprocess', methods=['POST'])(safe_route(preprocess_file))

# TODO
# Get route to preview file