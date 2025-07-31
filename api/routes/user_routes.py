from flask import Blueprint
from api.controllers.user_controller import register_user, login_user
from api.utils.safe_route import safe_route

auth_bp = Blueprint("auth_bp", __name__)

auth_bp.route("/register", methods=["POST"])(safe_route(register_user))
auth_bp.route("/login", methods=["POST"])(safe_route(login_user))
