# api/routes/monk_routes.py
from flask import Blueprint

from api.controllers.monks.train_controller import train_monk_handler
from api.controllers.monks.list_controller import list_monks_handler
from api.controllers.monks.get_controller import get_monk_handler
from api.controllers.monks.status_controller import job_status_handler
from api.controllers.monks.predict_controller import predict_with_monk_handler

from api.utils.auth_decorator import token_required
from api.utils.safe_route import safe_route


monk_bp = Blueprint("monk_bp", __name__)

@monk_bp.route("/train", methods=["POST"])
@token_required
@safe_route
def train_monk():
    return train_monk_handler()


@monk_bp.route("/monks", methods=["GET"])
@token_required
@safe_route
def list_monks():
    return list_monks_handler()

@monk_bp.route("/monk/<monk_id>", methods=["GET"])
@token_required
@safe_route
def get_monk(monk_id):
    return get_monk_handler(monk_id)

@monk_bp.route("/job/<job_id>", methods=["GET"])
@token_required
@safe_route
def job_status(job_id):
    return job_status_handler(job_id)

@monk_bp.route("/monk/<monk_id>/predict", methods=["POST"])
@token_required
@safe_route
def predict_monk(monk_id):
    return predict_with_monk_handler(monk_id)
